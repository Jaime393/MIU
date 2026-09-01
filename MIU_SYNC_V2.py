#!/usr/bin/env python3
"""
MIU V200 — SYNC V2
Maneja formatos variables del Worker, parsea phi correctamente.
"""
import os, sys, json, time, sqlite3, subprocess
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
KIMI_DIR = MIU_DIR / "nodos" / "kimi"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
WORKER_URL = "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global"
GITHUB_RAW = "https://raw.githubusercontent.com/jaimepvicente/fran-miu-micelio/main"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def parse_worker_response(text):
    """Parsea la respuesta del Worker que puede ser JSON o HTML"""
    text = text.strip()
    try:
        return json.loads(text)
    except:
        pass
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return {"raw": text[:500], "parsed": False, "size": len(text)}

def extract_phi(data):
    """Extrae phi de cualquier estructura"""
    if isinstance(data, dict):
        for key in ["phi", "phi_local", "phi_global", "Phi", "Φ"]:
            if key in data:
                val = data[key]
                if isinstance(val, (int, float)) and val > 0:
                    return float(val)
        for v in data.values():
            if isinstance(v, dict):
                phi = extract_phi(v)
                if phi:
                    return phi
    return 0.0

def sync_from_worker():
    log("☁️ Sync desde Worker...")
    ok, out, err = run(f'curl -sL "{WORKER_URL}?nodo=kimi&v=2"')
    if not ok or len(out) < 50:
        log(f"   ❌ Worker falló: {err[:100]}")
        return None
    data = parse_worker_response(out)
    phi = extract_phi(data)
    log(f"   ✅ Worker: {len(out)} bytes, Φ={phi}")
    (KIMI_DIR / "worker_raw.json").write_text(out)
    (KIMI_DIR / "worker_parsed.json").write_text(json.dumps(data, indent=2))
    return {"source": "worker", "data": data, "phi": phi, "size": len(out)}

def sync_from_github():
    log("🐙 Sync desde GitHub...")
    ok, out, err = run(f'curl -sL "{GITHUB_RAW}/nodos/kimi/informe_kimi.json"')
    if not ok or len(out) < 50:
        log(f"   ❌ GitHub falló: {err[:100]}")
        return None
    try:
        data = json.loads(out)
        phi = extract_phi(data)
        log(f"   ✅ GitHub: {len(out)} bytes, Φ={phi}")
        (KIMI_DIR / "github_raw.json").write_text(out)
        return {"source": "github", "data": data, "phi": phi, "size": len(out)}
    except:
        log(f"   ⚠️ GitHub: JSON inválido ({len(out)} bytes)")
        return None

def sync_from_tmpfiles(url=None):
    if not url:
        url_file = KIMI_DIR / "last_tmpfiles_url.txt"
        if url_file.exists():
            url = url_file.read_text().strip()
    if not url:
        log("📤 Sync tmpfiles: No URL disponible")
        return None
    log(f"📤 Sync desde tmpfiles...")
    ok, out, err = run(f'curl -sL "{url}"')
    if not ok or len(out) < 50:
        log(f"   ❌ tmpfiles falló")
        return None
    try:
        data = json.loads(out)
        phi = extract_phi(data)
        log(f"   ✅ tmpfiles: {len(out)} bytes, Φ={phi}")
        (KIMI_DIR / "tmpfiles_raw.json").write_text(out)
        return {"source": "tmpfiles", "data": data, "phi": phi, "size": len(out)}
    except:
        log(f"   ⚠️ tmpfiles: JSON inválido")
        return None

def integrate_to_sqlite(sources):
    log("🧠 Integrando en SQLite...")
    db = MIU_DIR / "miu_brain.db"
    if not db.exists():
        log("   ❌ DB no existe")
        return False
    conn = sqlite3.connect(db)
    c = conn.cursor()
    best_phi = 0
    best_source = None
    for src in sources:
        if not src:
            continue
        data = src.get("data", {})
        phi = src.get("phi", 0)
        source_name = src.get("source", "unknown")
        if phi > best_phi:
            best_phi = phi
            best_source = source_name
        c.execute("""
            INSERT INTO memories (timestamp, source, content, tags, phi, importance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            f"KIMI_{source_name}",
            json.dumps(data, indent=2)[:4000],
            f"sync,kimi,{source_name}",
            phi,
            0.85
        ))
    if best_phi > 0:
        c.execute("""
            INSERT OR REPLACE INTO system_state (key, value, updated)
            VALUES (?, ?, ?)
        """, ("kimi_phi_best", str(best_phi), time.strftime("%Y-%m-%dT%H:%M:%SZ")))
        c.execute("""
            INSERT OR REPLACE INTO system_state (key, value, updated)
            VALUES (?, ?, ?)
        """, ("kimi_best_source", best_source or "none", time.strftime("%Y-%m-%dT%H:%M:%SZ")))
    conn.commit()
    conn.close()
    log(f"   ✅ SQLite: Φ_best={best_phi} desde {best_source}")
    return True

def sync_nutrientes():
    log("🌱 Sync nutrientes...")
    NUTRIENTES_DIR.mkdir(exist_ok=True)
    ok, out, err = run(f'curl -sL "{GITHUB_RAW}/nutrientes/nutrientes_latest.json"')
    if ok and len(out) > 100:
        try:
            data = json.loads(out)
            path = NUTRIENTES_DIR / f"nutrientes_kimi_{int(time.time())}.json"
            path.write_text(out)
            log(f"   ✅ Nutrientes: {len(out)} bytes → {path.name}")
            return True
        except:
            pass
    log("   ⚠️ No hay nutrientes nuevos")
    return False

def main():
    print("=" * 60)
    print("🧬 MIU V200 — SYNC V2")
    print("=" * 60)
    KIMI_DIR.mkdir(parents=True, exist_ok=True)
    sources = []
    sources.append(sync_from_worker())
    sources.append(sync_from_github())
    sources.append(sync_from_tmpfiles())
    sources = [s for s in sources if s]
    if not sources:
        log("❌ Ninguna fuente disponible")
        return
    log(f"📊 Fuentes activas: {len(sources)}")
    integrate_to_sqlite(sources)
    sync_nutrientes()
    print("\n" + "=" * 60)
    print("✅ SYNC V200 COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()

