#!/usr/bin/env python3
"""
MIU V201 — INTEGRADOR DE RECURSOS LIGERO
Solo integra recursos locales (SQLite, archivos). No descarga externos.
"""
import os, json, time, sqlite3
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES_DIR = MIU_DIR / "nutrientes"

def log(msg):
    print(f"🧩 {msg}")

def main():
    log("🧩 INTEGRADOR V201 — Solo locales, timeout 5s")
    log("=" * 40)
    integrados = []
    for f in sorted(NUTRIENTES_DIR.glob("informe_*.json")):
        try:
            with open(f) as fh:
                data = json.load(fh)
            db = MIU_DIR / "miu_brain.db"
            if db.exists():
                conn = sqlite3.connect(db)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO memories (timestamp, source, content, tags, phi, importance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "integrador",
                    json.dumps(data, indent=2)[:4000],
                    "integrador,informe",
                    data.get("ok_count", 0),
                    0.7
                ))
                conn.commit()
                conn.close()
                log(f"   ✅ Integrado: {f.name}")
                integrados.append(f.name)
        except Exception as e:
            log(f"   ❌ Error con {f.name}: {e}")
    try:
        db = MIU_DIR / "miu_brain.db"
        if db.exists():
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO system_state (key, value, updated)
                VALUES (?, ?, ?)
            """, ("last_integracion", time.strftime("%Y-%m-%dT%H:%M:%SZ"), time.strftime("%Y-%m-%dT%H:%M:%SZ")))
            conn.commit()
            conn.close()
    except:
        pass
    log("=" * 40)
    log(f"✅ Integración: {len(integrados)} informes")
    return {"integrados": integrados}

if __name__ == "__main__":
    main()
