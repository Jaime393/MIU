#!/usr/bin/env python3
"""
MIU V153.3 — Doctor
Diagnóstico completo del ecosistema. Detecta, reporta, sugiere fixes.
"""
import os, sys, json, time, sqlite3, subprocess
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
REPORT_FILE = MIU_DIR / "miu_health_report.json"

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return "", str(e), 1

def check_file(path, min_size=0):
    p = MIU_DIR / path
    if not p.exists():
        return {"ok": False, "err": "missing"}
    s = p.stat().st_size
    if s < min_size:
        return {"ok": False, "err": f"too_small ({s} bytes)"}
    return {"ok": True, "size": s}

def check_python_imports():
    mods = ["requests", "sqlite3", "json", "time"]
    failed = []
    for m in mods:
        try:
            __import__(m)
        except:
            failed.append(m)
    return {"ok": len(failed) == 0, "missing": failed}

def check_github():
    sys.path.insert(0, str(MIU_DIR))
    try:
        from miu_github import list_repos
        r = list_repos()
        if r.get("ok"):
            return {"ok": True, "repos": r.get("count", 0)}
        return {"ok": False, "err": r.get("err", "unknown"), "status": r.get("status")}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def check_sqlite():
    db = MIU_DIR / "miu_brain.db"
    if not db.exists():
        return {"ok": False, "err": "missing"}
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        tables = {}
        for t in ["memories", "conversations", "commands", "system_state"]:
            c.execute(f"SELECT COUNT(*) FROM {t}")
            tables[t] = c.fetchone()[0]
        conn.close()
        return {"ok": True, "tables": tables}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def check_sd():
    links = list(MIU_DIR.glob("sd_*"))
    return {"ok": len(links) > 0, "links": [l.name for l in links]}

def check_processes():
    out, err, code = run("ps aux | grep -E 'bot_miu|miu_control' | grep -v grep")
    lines = [l for l in out.split("\n") if l.strip()]
    return {"ok": len(lines) > 0, "count": len(lines), "names": [l.split()[-1] for l in lines[:5]]}

def check_env():
    env_path = MIU_DIR / ".env"
    if not env_path.exists():
        return {"ok": False, "err": "missing"}
    with open(env_path) as f:
        content = f.read()
    keys = [line.split("=")[0] for line in content.split("\n") if "=" in line and not line.startswith("#")]
    critical = ["GITHUB_TOKEN", "BOT_TABLET_TOKEN", "OR_JAIME"]
    missing = [k for k in critical if k not in keys or f'{k}=""' in content or f"{k}=''" in content]
    return {"ok": len(missing) == 0, "keys_found": len(keys), "missing_critical": missing}

def diagnose():
    print("🔬 MIU DOCTOR V153.3")
    print("=" * 50)
    
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "V153.3",
        "checks": {}
    }
    
    # Archivos críticos
    print("\n📁 Archivos críticos:")
    files = {
        "miu_memory.py": 1000,
        "miu_github.py": 1000,
        "miu_scanner.py": 1000,
        "miu_control.py": 1000,
        "protocolos/paf_01.py": 500,
        "protocolos/pae_01.py": 500,
        "protocolos/pcp_01.py": 500,
        "seeds/SEED.sh": 100,
        "dashboard/index.html": 100,
    }
    all_ok = True
    for f, min_s in files.items():
        r = check_file(f, min_s)
        report["checks"][f] = r
        status = "✅" if r["ok"] else "❌"
        print(f"   {status} {f}")
        if not r["ok"]:
            all_ok = False
            print(f"      → {r['err']}")
    
    # Python
    print("\n🐍 Python:")
    r = check_python_imports()
    report["checks"]["python_imports"] = r
    print(f"   {'✅' if r['ok'] else '❌'} Módulos ({', '.join(r.get('missing', [])) or 'todos OK'})")
    
    # GitHub
    print("\n🐙 GitHub:")
    r = check_github()
    report["checks"]["github"] = r
    if r["ok"]:
        print(f"   ✅ Conectado ({r['repos']} repos)")
    else:
        print(f"   ❌ {r.get('err', 'Error desconocido')}")
        print(f"      → Crea token en https://github.com/settings/tokens (scope: repo)")
    
    # SQLite
    print("\n🧠 SQLite:")
    r = check_sqlite()
    report["checks"]["sqlite"] = r
    if r["ok"]:
        for t, n in r["tables"].items():
            print(f"   ✅ {t}: {n} registros")
    else:
        print(f"   ❌ {r.get('err')}")
    
    # SD
    print("\n💾 SD Card:")
    r = check_sd()
    report["checks"]["sd"] = r
    print(f"   {'✅' if r['ok'] else '❌'} Enlaces: {', '.join(r.get('links', [])) or 'ninguno'}")
    
    # Procesos
    print("\n⚡ Procesos:")
    r = check_processes()
    report["checks"]["processes"] = r
    print(f"   {'✅' if r['ok'] else '❌'} {r['count']} activos")
    if r.get("names"):
        for n in r["names"]:
            print(f"      → {n}")
    
    # ENV
    print("\n🔐 Variables de entorno:")
    r = check_env()
    report["checks"]["env"] = r
    if r["ok"]:
        print(f"   ✅ {r['keys_found']} keys configuradas")
    else:
        print(f"   ❌ Faltan: {', '.join(r.get('missing_critical', []))}")
    
    # Guardar reporte
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    
    # Resumen
    print("\n" + "=" * 50)
    total = len(report["checks"])
    ok = sum(1 for v in report["checks"].values() if v.get("ok"))
    print(f"📊 SALUD: {ok}/{total} checks OK")
    if ok == total:
        print("🌐 El imperio está saludable. ρ(x) > 0.")
    else:
        print("🔧 Hay carencias. Ejecuta los fixes sugeridos arriba.")
    print(f"📄 Reporte: {REPORT_FILE}")
    print("=" * 50)
    
    return report

if __name__ == "__main__":
    diagnose()
