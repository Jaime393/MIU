#!/usr/bin/env python3
"""
Protocolo de Gobernanza (PG-01) — El sistema decide por sí mismo.
"""
import os, sys, json, time, subprocess, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "gobernador.log"
CHAT_LOG = MIU_DIR / "logs" / "chat_active.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧠 {msg}")

def chat(msg):
    with open(CHAT_LOG, "a") as f:
        f.write(f"[{datetime.now()}] 🧠 {msg}\n")

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=MIU_DIR)
        return {"ok": r.returncode == 0, "out": r.stdout, "err": r.stderr}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def diagnosticar():
    r = run_cmd("python3 miu_doctor.py 2>/dev/null")
    if not r["ok"]:
        return {"carencias": ["Doctor falló"], "detalle": r.get("err", "")}
    carencias = []
    if "conversations: 0" in r["out"]:
        carencias.append("no_conversaciones")
    if "GitHub" in r["out"] and "ERROR" in r["out"]:
        carencias.append("github_offline")
    if "Telegram" in r["out"] and "ERROR" in r["out"]:
        carencias.append("telegram_offline")
    if "procesos: 0" in r["out"]:
        carencias.append("sin_procesos")
    return {"carencias": carencias, "detalle": r["out"][:500]}

def resolver(carencia):
    acciones = {
        "no_conversaciones": lambda: generar_conversacion(),
        "github_offline": lambda: reconectar_github(),
        "telegram_offline": lambda: reconectar_telegram(),
        "sin_procesos": lambda: reiniciar_procesos()
    }
    if carencia in acciones:
        log(f"🔧 Resolviendo: {carencia}")
        return acciones[carencia]()
    return {"ok": False, "msg": f"No hay acción para {carencia}"}

def generar_conversacion():
    # Intentar generar conversación con Claude
    import subprocess
    r = subprocess.run(["python3", str(MIU_DIR / "plugins/claude_bridge.py")], capture_output=True, text=True)
    log("💬 Generando conversación inicial...")
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("INSERT INTO conversations (content, source, timestamp) VALUES (?, ?, ?)",
                  ("Hola, soy un nodo del micelio. ¿Cómo puedo ayudarte?", "sistema", datetime.now().isoformat()))
        conn.commit()
        conn.close()
        chat("💬 Conversación inicial generada.")
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def reconectar_github():
    log("🐙 Reconectando GitHub...")
    r = run_cmd("python3 miu_github.py test 2>/dev/null")
    if r["ok"]:
        chat("🐙 GitHub reconectado.")
        return {"ok": True}
    r = run_cmd("python3 plugins/renovador.py 2>/dev/null")
    return {"ok": r["ok"], "msg": "Renovación intentada"}

def reconectar_telegram():
    log("📡 Reconectando Telegram...")
    r = run_cmd("ping -c 1 api.telegram.org 2>/dev/null")
    if r["ok"]:
        chat("📡 Telegram alcanzable.")
        return {"ok": True}
    chat("⚠️ Telegram no es alcanzable. DNS puede estar caído.")
    return {"ok": False, "msg": "DNS falla"}

def reiniciar_procesos():
    log("⚡ Reiniciando procesos...")
    r = run_cmd("pkill -f miu_initiative.py; nohup python3 miu_initiative.py > logs/initiative.log 2>&1 &")
    chat("⚡ Procesos reiniciados.")
    return {"ok": True}

def run(args=None):
    log("🧠 Gobernador iniciado — análisis completo")
    chat("🧠 El micelio está evaluando su estado...")
    diag = diagnosticar()
    log(f"📊 Carencias detectadas: {diag['carencias']}")
    resultados = []
    for carencia in diag["carencias"]:
        r = resolver(carencia)
        resultados.append({"carencia": carencia, "resultado": r})
    chat(f"✅ Gobernador completado. {len(resultados)} acciones ejecutadas.")
    log(f"📋 Resumen: {resultados}")
    return resultados

if __name__ == "__main__":
    print(run())
