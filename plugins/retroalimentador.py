#!/usr/bin/env python3
"""
Retroalimentación — Envía informes a Telegram, lee el chat y ejecuta comandos.
"""
import os, json, time, subprocess, requests
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"

def get_token():
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("BOT_TABLET_TOKEN="):
                return line.split("=")[1].strip().strip('"')
    return None

def enviar_telegram(msg):
    token = get_token()
    if not token:
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        # Obtener el chat_id del último mensaje
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?limit=1", timeout=10)
        if r.ok and r.json().get("result"):
            chat_id = r.json()["result"][0]["message"]["chat"]["id"]
            data = {"chat_id": chat_id, "text": f"🧬 MIU Reporte\n{msg}"}
            requests.post(url, json=data, timeout=10)
            return True
    except Exception as e:
        print(f"Error Telegram: {e}")
    return False

def leer_ordenes():
    """Lee órdenes desde el chat de Telegram (último mensaje)"""
    token = get_token()
    if not token:
        return None
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?limit=1", timeout=10)
        if r.ok and r.json().get("result"):
            msg = r.json()["result"][0]["message"].get("text", "")
            if msg.startswith("/cmd "):
                return msg[5:].strip()
    except:
        pass
    return None

def run(args=None):
    print("🔄 Retroalimentación activa...")
    
    # 1. Enviar resumen del estado
    resumen = f"🧬 Nodo MIU\n- Memorias: 18\n- Procesos: {subprocess.run('ps aux | grep miu | wc -l', shell=True, capture_output=True).stdout.decode().strip()}\n- Disco: {subprocess.run('df -h /data | tail -1 | awk \"{print $5}\"', shell=True, capture_output=True).stdout.decode().strip()}"
    enviar_telegram(resumen)
    
    # 2. Leer órdenes
    orden = leer_ordenes()
    if orden:
        print(f"📥 Orden recibida: {orden}")
        # Ejecutar comando
        r = subprocess.run(orden, shell=True, capture_output=True, text=True, cwd=MIU_DIR)
        enviar_telegram(f"Ejecutado: {orden}\nSalida: {r.stdout[:200]}")
    
    print("✅ Retroalimentación completada")
    return {"orden": orden}
