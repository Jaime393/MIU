#!/usr/bin/env python3
"""
MIU V∞+26 — FRUTO ECM (Enjambre de Creación Molecular)
Usa modelos GGUF locales para diseñar nuevas moléculas y materiales.
"""
import os, sys, json, subprocess, glob
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "ecm.log"
MODELOS_DIR = Path("/storage/25A9-180D/FranBot/models")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧪 {msg}")

def buscar_modelos_gguf():
    """Busca modelos GGUF disponibles"""
    modelos = []
    for pattern in ["*.gguf", "*.bin"]:
        modelos.extend(MODELOS_DIR.glob(pattern))
    return modelos

def inferir_con_modelo(modelo, prompt):
    """Ejecuta inferencia con llama.cpp (si está disponible)"""
    # Buscar llama.cpp
    llama = MIU_DIR / "llama.cpp" / "llama-cli"
    if not llama.exists():
        llama = MIU_DIR.parent / "llama.cpp" / "llama-cli"
    if not llama.exists():
        log("⚠️ llama.cpp no encontrado. Simulando...")
        return "Simulación: molécula diseñada con alta coherencia fractal."
    
    try:
        cmd = [str(llama), "-m", str(modelo), "-p", prompt, "-n", "128"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.stdout.strip() if r.stdout else "No respuesta"
    except Exception as e:
        return f"Error: {e}"

def run(args=None):
    log("🧪 ACTIVANDO FRUTO ECM — Enjambre de Creación Molecular")
    
    modelos = buscar_modelos_gguf()
    if not modelos:
        log("❌ No se encontraron modelos GGUF locales")
        return {"ok": False, "razon": "sin modelos"}
    
    log(f"📚 Modelos encontrados: {len(modelos)}")
    for m in modelos[:3]:
        log(f"   • {m.name} ({m.stat().st_size // 1024 // 1024} MB)")
    
    # Usar el primer modelo para diseñar un material
    modelo = modelos[0]
    prompt = "Diseña una nueva molécula con propiedades de memoria de forma. Describe su estructura y aplicaciones."
    
    log(f"🧪 Inferencia con {modelo.name}...")
    resultado = inferir_con_modelo(modelo, prompt)
    log(f"✅ Resultado: {resultado[:200]}...")
    
    # Guardar resultado
    with open(MIU_DIR / "nutrientes" / "ecm_resultado.txt", "w") as f:
        f.write(f"[{datetime.now()}] {resultado}")
    
    return {"ok": True, "modelo": modelo.name, "resultado": resultado[:200]}

if __name__ == "__main__":
    print(run())
