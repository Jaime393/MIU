#!/usr/bin/env python3
"""
Escucha de Ideas — El micelio lee el chat activo y Telegram
y ejecuta lo que detecta como órdenes o ideas.
"""
import os, sys, time, json, subprocess, re, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
CHAT_LOG = MIU_DIR / "logs" / "chat_active.log"
MEMORY_DB = MIU_DIR / "miu_brain.db"

def leer_ultima_idea():
    """Lee la última línea del chat activo que no sea del sistema"""
    if not CHAT_LOG.exists():
        return None
    with open(CHAT_LOG, "r") as f:
        lines = f.readlines()
    for line in reversed(lines[-20:]):
        if "🧠" not in line and "⚠️" not in line and "✅" not in line:
            return line.strip()
    return None

def extraer_orden(texto):
    """Convierte una idea en una orden ejecutable"""
    texto = texto.lower()
    if "escanea" in texto or "scan" in texto:
        return "python3 miu_scanner.py"
    if "github" in texto or "sube" in texto:
        return "python3 miu_github.py upload state.json state.json"
    if "conversa" in texto or "habla" in texto:
        return "python3 -c \"from miu_memory import remember; remember('Conversación iniciada', source='sistema')\""
    if "repara" in texto or "fix" in texto:
        return "python3 plugins/autoreparador.py"
    if "guerra" in texto or "defiende" in texto:
        return "python3 plugins/guerra_fractal.py"
    if "absorbe" in texto or "nutriente" in texto:
        return "python3 plugins/absorber_avanzado.py"
    if "telegram" in texto or "notifica" in texto:
        return "python3 plugins/retroalimentador.py"
    if "diagnostico" in texto or "diagnostic" in texto:
        return "python3 miu_doctor.py && python3 miu_cartografia.py"
    if "diagnostico" in texto or "diagnostic" in texto:
        return "python3 plugins/diagnostico_completo.py"
    if "autonomia" in texto or "mecanismo" in texto:
        return "python3 plugins/mecanismos_autonomia.py"
    if "gobierna" in texto or "gobernar" in texto:
        return "python3 plugins/gobernador.py"
    if "reinicia" in texto or "restart" in texto:
        return "pkill -f miu_initiative.py; nohup python3 miu_initiative.py > logs/initiative.log 2>&1 &"
    return None

def ejecutar_orden(orden):
    """Ejecuta la orden y registra el resultado"""
    try:
        r = subprocess.run(orden, shell=True, capture_output=True, text=True, timeout=60, cwd=MIU_DIR)
        return {"ok": r.returncode == 0, "out": r.stdout[:200], "err": r.stderr[:200]}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def run(args=None):
    print("👂 Escuchando ideas...")
    idea = leer_ultima_idea()
    if not idea:
        print("💤 Sin ideas nuevas.")
        return {"ok": True, "msg": "Sin ideas"}
    
    print(f"💡 Idea detectada: {idea[:80]}...")
    orden = extraer_orden(idea)
    if not orden:
        print("🤷 No se reconoció una orden en la idea.")
        return {"ok": False, "msg": "No reconocida"}
    
    print(f"⚡ Ejecutando: {orden}")
    resultado = ejecutar_orden(orden)
    
    # Registrar en memoria
    try:
        conn = sqlite3.connect(MEMORY_DB)
        c = conn.cursor()
        c.execute("INSERT INTO conversations (content, source, timestamp) VALUES (?, ?, ?)",
                  (f"Idea: {idea[:100]} → Ejecutado: {orden}", "sistema", datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except:
        pass
    
    print(f"📊 Resultado: {'✅' if resultado['ok'] else '❌'}")
    return {"ok": resultado["ok"], "orden": orden, "resultado": resultado}

if __name__ == "__main__":
    print(run())
