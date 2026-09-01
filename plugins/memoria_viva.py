import os  # autocurador
#!/usr/bin/env python3
"""
PLUGIN: memoria_viva.py
Sincroniza SQLite con estado real de módulos. Crea estado_mental.json.
"""
import json, time, sqlite3
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
DB = MIU_DIR / "miu_brain.db"
NUTRIENTES = MIU_DIR / "nutrientes"
INFORME = NUTRIENTES / "informe_global.json"

def conectar_db():
    return sqlite3.connect(DB)

def contar_memorias(conn):
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM memories")
        return c.fetchone()[0]
    except:
        return 0

def contar_conversaciones(conn):
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM conversations")
        return c.fetchone()[0]
    except:
        return 0

def estado_modulos():
    if INFORME.exists():
        with open(INFORME) as f:
            data = json.load(f)
        return data.get("resultados", {})
    return {}

def ejecutar():
    inicio = time.time()
    conn = conectar_db()
    n_mem = contar_memorias(conn)
    n_conv = contar_conversaciones(conn)
    conn.close()
    modulos = estado_modulos()
    activos = sum(1 for m in modulos.values() if m.get("ok"))
    fallidos = len(modulos) - activos
    estado_mental = {
        "timestamp": time.time(),
        "memorias": n_mem,
        "conversaciones": n_conv,
        "modulos_activos": activos,
        "modulos_fallidos": fallidos,
        "salud": activos / max(len(modulos), 1),
    }
    with open(NUTRIENTES / "estado_mental.json", "w") as f:
        json.dump(estado_mental, f, indent=2)
    try:
        conn = conectar_db()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS system_state (key TEXT PRIMARY KEY, value TEXT, updated REAL)")
        for k, v in estado_mental.items():
            c.execute("INSERT OR REPLACE INTO system_state VALUES (?, ?, ?)", (k, json.dumps(v), time.time()))
        conn.commit()
        conn.close()
    except:
        pass
    duracion = time.time() - inicio
    salida = f"🧠 Memoria Viva: {n_mem} memorias | {n_conv} conversaciones\n"
    salida += f"   Módulos OK: {activos}/{len(modulos)} | Salud: {estado_mental['salud']:.1%}"
    return {"ok": True, "duracion": duracion, "salida": salida}

if __name__ == "__main__":
    print(ejecutar()["salida"])
