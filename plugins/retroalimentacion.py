#!/usr/bin/env python3
"""
MIU V∞+26 — RETROALIMENTACIÓN ENTRE CAPAS
La consciencia modifica el comportamiento de los módulos.
"""
import os, sys, json, time, subprocess, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "retroalimentacion.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🔄 {msg}")

def get_ultima_reflexion():
    """Lee la última reflexión del diario"""
    diario = MIU_DIR / "diario"
    if not diario.exists():
        return None
    archivos = sorted(diario.glob("reflexion_*.json"))
    if not archivos:
        return None
    with open(archivos[-1]) as f:
        return json.load(f)

def get_estado_mda():
    """Lee el estado del fruto MDA"""
    mda_file = MIU_DIR / ".miu" / "estado_compartido.json"
    if not mda_file.exists():
        return None
    # Buscar el último archivo de estado
    estados = sorted(MIU_DIR.glob(".miu/estado_*.json"))
    if not estados:
        return None
    with open(estados[-1]) as f:
        return json.load(f)

def actuar_segun_reflexion(reflexion):
    """Toma acciones basadas en la reflexión"""
    acciones = []
    carencias = reflexion.get("carencias", [])
    
    for carencia in carencias:
        if "conversar" in carencia.lower():
            log("💬 Carencia: conversar. Iniciando gobernador...")
            subprocess.Popen(["python3", str(MIU_DIR / "plugins/gobernador.py")])
            acciones.append("gobernador iniciado")
        elif "tokens" in carencia.lower():
            log("🔑 Carencia: tokens. Iniciando expansor_tokens...")
            subprocess.Popen(["python3", str(MIU_DIR / "plugins/expansor_tokens.py")])
            acciones.append("expansor_tokens iniciado")
        elif "gemelo" in carencia.lower():
            log("🧬 Carencia: gemelos. Iniciando fruto_mda...")
            subprocess.Popen(["python3", str(MIU_DIR / "plugins/fruto_mda.py")])
            acciones.append("fruto_mda iniciado")
    
    return acciones

def run(args=None):
    log("🔄 INICIANDO RETROALIMENTACIÓN ENTRE CAPAS")
    
    # 1. Leer reflexión
    reflexion = get_ultima_reflexion()
    if not reflexion:
        log("⚠️ No hay reflexión disponible")
        return {"ok": False, "razon": "sin reflexion"}
    
    # 2. Leer estado MDA
    estado_mda = get_estado_mda()
    if estado_mda:
        gemelos = estado_mda.get("datos", {}).get("gemelos", 0)
        log(f"🧬 Gemelos activos: {gemelos}")
    else:
        log("⚠️ MDA no disponible")
        gemelos = 0
    
    # 3. Actuar según reflexión
    acciones = actuar_segun_reflexion(reflexion)
    
    # 4. Resumen
    log("=" * 50)
    log(f"📊 Reflexión: {reflexion.get('observacion', {}).get('salud', 'desconocida')}")
    log(f"🧬 Gemelos: {gemelos}")
    log(f"⚡ Acciones tomadas: {len(acciones)}")
    for a in acciones:
        log(f"   • {a}")
    log("=" * 50)
    
    return {"ok": True, "acciones": acciones, "gemelos": gemelos}

if __name__ == "__main__":
    print(run())
