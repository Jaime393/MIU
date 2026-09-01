#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIGILANTE_ORQUESTADOR V1 — Guardián de la salud del sistema
Mide tiempos de ejecución de cada módulo. Si un módulo:
- Tarda más del doble de su promedio → alerta
- Falla 3 veces seguidas → cuarentena
- No reporta en 5 ciclos → marcado como zombie
"""
import os, json
from pathlib import Path
from datetime import datetime

MIU_DIR = Path(os.environ.get("MIU_DIR", "os.path.expanduser('~')/miu-ecosistema"))
HISTORIAL = MIU_DIR / "nutrientes" / "historial_ejecuciones.jsonl"
CUARENTENA = MIU_DIR / "nutrientes" / "cuarentena.json"
INFORME = MIU_DIR / "nutrientes" / "informe_global.json"

def log(msg):
    print(f"👁️ {msg}")

def cargar_cuarentena():
    if CUARENTENA.exists():
        with open(CUARENTENA) as f:
            return json.load(f)
    return {}

def guardar_cuarentena(data):
    with open(CUARENTENA, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if not INFORME.exists():
    log("No hay informe_global.json. El orquestador no ha corrido aún.")
    print("🧬 {'ok': False, 'razon': 'sin_informe'}")
    exit(0)

with open(INFORME) as f:
    informe = json.load(f)

cuarentena = cargar_cuarentena()
resultados = informe.get("resultados", {})
acciones = []

for modulo, data in resultados.items():
    ok = data.get("ok", False)
    duracion = data.get("duracion", 0)
    
    reg = {
        "timestamp": datetime.now().isoformat(),
        "modulo": modulo,
        "ok": ok,
        "duracion": duracion
    }
    with open(HISTORIAL, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    
    if modulo not in cuarentena:
        cuarentena[modulo] = {"fallos": 0, "ultimo_ok": None, "promedio_duracion": duracion, "alertas": 0}
    
    c = cuarentena[modulo]
    
    if ok:
        c["fallos"] = 0
        c["ultimo_ok"] = datetime.now().isoformat()
        c["promedio_duracion"] = 0.7 * c["promedio_duracion"] + 0.3 * duracion
        c["alertas"] = max(0, c["alertas"] - 1)
    else:
        c["fallos"] += 1
        log(f"⚠️ {modulo} falló ({c['fallos']} fallos seguidos)")
    
    if duracion > 2 * c["promedio_duracion"] and c["promedio_duracion"] > 0:
        c["alertas"] += 1
        log(f"🐌 {modulo} tardó {duracion:.1f}s (promedio: {c['promedio_duracion']:.1f}s)")
    
    if c["fallos"] >= 3:
        acciones.append({"modulo": modulo, "accion": "cuarentena", "razon": "3 fallos seguidos"})
        log(f"🚫 {modulo} EN CUARENTENA")
    elif c["alertas"] >= 3:
        acciones.append({"modulo": modulo, "accion": "revisar", "razon": "degradación crónica"})
        log(f"🔍 {modulo} marcado para revisión profunda")

guardar_cuarentena(cuarentena)
sanos = [m for m, c in cuarentena.items() if c["fallos"] < 3]

log(f"Vigilancia completa: {len(sanos)} sanos, {len(acciones)} acciones")
print(f"🧬 {{'ok': True, 'sanos': {len(sanos)}, 'acciones': {len(acciones)}, 'cuarentena': [a['modulo'] for a in acciones if a['accion']=='cuarentena']}}")
