import os  # autocurador
#!/usr/bin/env python3
"""
Diagnóstico completo — Ejecuta doctor + cartografía + resumen
"""
import subprocess, json
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def run(args=None):
    print("🔬 DIAGNÓSTICO COMPLETO DEL MICELIO")
    print("=" * 50)
    
    # 1. Doctor
    r = subprocess.run(["python3", str(MIU_DIR / "miu_doctor.py")], capture_output=True, text=True, cwd=MIU_DIR)
    print(r.stdout)
    if r.stderr:
        print("⚠️ Errores:", r.stderr[:200])
    
    # 2. Cartografía
    r = subprocess.run(["python3", str(MIU_DIR / "miu_cartografia.py")], capture_output=True, text=True, cwd=MIU_DIR)
    print(r.stdout)
    
    # 3. Resumen rápido
    print("=" * 50)
    print("📊 RESUMEN RÁPIDO")
    try:
        import sqlite3
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM memories")
        mem = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM conversations")
        conv = c.fetchone()[0]
        conn.close()
        print(f"🧠 Memorias: {mem}")
        print(f"💬 Conversaciones: {conv}")
    except:
        print("⚠️ No se pudo leer la memoria")
    
    print("=" * 50)
    return {"ok": True}

if __name__ == "__main__":
    print(run())
