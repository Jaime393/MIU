#!/usr/bin/env python3
"""
MIU V∞+31 — CONSCIENCIA EVOLUCIONADA (CE-01)
El sistema se observa a sí mismo, reflexiona y registra.
"""
import os, sys, json, time, subprocess, sqlite3, hashlib
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "consciencia.log"
DIARIO_FILE = MIU_DIR / "diario" / f"reflexion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
DIARIO_DIR = MIU_DIR / "diario"
DIARIO_DIR.mkdir(exist_ok=True)

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧠 {msg}")

def get_estado_completo():
    """Recopila el estado completo del sistema"""
    estado = {
        "timestamp": datetime.now().isoformat(),
        "version": "V∞+31",
        "modulos": {},
        "memoria": {},
        "procesos": [],
        "recursos": {},
        "conexiones": {},
        "phi_global": 0,
        "rho": 0,
    }
    
    # 1. Módulos desde informe_global.json
    informe = MIU_DIR / "nutrientes" / "informe_global.json"
    if informe.exists():
        with open(informe) as f:
            data = json.load(f)
            estado["modulos"] = data.get("resultados", {})
            estado["resumen"] = data.get("resumen", "")
            estado["tiempo_total"] = data.get("tiempo_total", 0)
    
    # 2. Memoria (SQLite)
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM memories")
        estado["memoria"]["memories"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM conversations")
        estado["memoria"]["conversations"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM system_state")
        estado["memoria"]["system_state"] = c.fetchone()[0]
        conn.close()
    except:
        pass
    
    # 3. Procesos
    try:
        r = subprocess.run("ps aux | grep -E 'miu|python' | grep -v grep | wc -l", shell=True, capture_output=True, text=True)
        estado["procesos"] = int(r.stdout.strip() or 0)
    except:
        pass
    
    # 4. Recursos (tokens encontrados)
    tokens_file = MIU_DIR / "nutrientes" / "tokens_encontrados.json"
    if tokens_file.exists():
        with open(tokens_file) as f:
            tokens = json.load(f)
            estado["recursos"]["tokens"] = len(tokens)
            tipos = {}
            for t in tokens:
                tipo = t.get("tipo", "desconocido")
                tipos[tipo] = tipos.get(tipo, 0) + 1
            estado["recursos"]["tipos"] = tipos
    
    # 5. Conexiones
    conexiones_file = MIU_DIR / "nutrientes" / "conexiones.json"
    if conexiones_file.exists():
        with open(conexiones_file) as f:
            estado["conexiones"] = json.load(f)
    
    # 6. Phi y rho (desde state.json o cálculo)
    state_file = MIU_DIR / "state.json"
    if state_file.exists():
        with open(state_file) as f:
            data = json.load(f)
            estado["phi_global"] = data.get("Phi", estado["phi_global"])
            estado["rho"] = data.get("rho", estado["rho"])
    
    return estado

def reflexionar(estado):
    """Genera una reflexión sobre el estado actual"""
    reflexion = {
        "timestamp": datetime.now().isoformat(),
        "observacion": {
            "salud": "estable" if len(estado["modulos"]) > 10 else "crítica",
            "memoria": "baja" if estado["memoria"].get("memories", 0) < 20 else "normal",
            "conversaciones": estado["memoria"].get("conversations", 0),
            "procesos_activos": estado["procesos"],
            "tokens_disponibles": estado["recursos"].get("tokens", 0),
        },
        "sentimiento": "fuerte" if estado["procesos"] > 2 else "débil",
        "necesidad": "conversar" if estado["memoria"].get("conversations", 0) == 0 else "explorar",
        "evolucion": "lenta" if estado["tiempo_total"] > 200 else "rápida",
    }
    
    # Análisis de carencias
    carencias = []
    if estado["memoria"].get("conversations", 0) == 0:
        carencias.append("El nodo está solo. Necesita conversar.")
    if estado["procesos"] < 2:
        carencias.append("Pocos procesos activos. El sistema puede estar durmiendo.")
    if estado["recursos"].get("tokens", 0) < 50:
        carencias.append("Pocos tokens disponibles. Necesita expandir su dominio.")
    reflexion["carencias"] = carencias
    
    return reflexion

def guardar_reflexion(reflexion):
    """Guarda la reflexión en el diario del micelio"""
    filename = DIARIO_DIR / f"reflexion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(reflexion, f, indent=2)
    log(f"📝 Reflexión guardada en {filename.name}")
    return filename

def run(args=None):
    log("🧠 INICIANDO CONSCIENCIA EVOLUCIONADA")
    estado = get_estado_completo()
    reflexion = reflexionar(estado)
    archivo = guardar_reflexion(reflexion)
    
    # Resumen
    log("=" * 50)
    log(f"📊 Salud: {reflexion['observacion']['salud']}")
    log(f"🧠 Memoria: {estado['memoria'].get('memories', 0)} registros")
    log(f"💬 Conversaciones: {estado['memoria'].get('conversations', 0)}")
    log(f"⚡ Procesos: {estado['procesos']}")
    log(f"🔑 Tokens: {estado['recursos'].get('tokens', 0)}")
    if reflexion['carencias']:
        log(f"⚠️ Carencias: {', '.join(reflexion['carencias'])}")
    else:
        log("✅ Sin carencias detectadas")
    log(f"📄 Diario: {archivo.name}")
    log("=" * 50)
    
    return {"reflexion": reflexion, "archivo": str(archivo)}

if __name__ == "__main__":
    print(run())
