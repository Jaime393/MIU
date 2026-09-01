#!/usr/bin/env python3
"""
MIU V∞+24 — Módulo de Conexiones
Prueba y establece conexiones con todos los recursos externos.
"""
import os, sys, json, time, subprocess, requests, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "conexiones.log"
ENV_FILE = MIU_DIR / ".env"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🔗 {msg}")

def get_token(key):
    if not ENV_FILE.exists():
        return None
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith(key + "="):
                return line.split("=")[1].strip().strip('"')
    return None

def test_github():
    log("🐙 Probando GitHub...")
    token = get_token("GITHUB_TOKEN")
    if not token:
        return {"ok": False, "msg": "Sin token"}
    try:
        r = requests.get("https://api.github.com/user", headers={"Authorization": f"token {token}"}, timeout=10)
        return {"ok": r.status_code == 200, "msg": f"Status {r.status_code}"}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def test_telegram():
    log("📡 Probando Telegram...")
    token = get_token("BOT_TABLET_TOKEN")
    if not token:
        return {"ok": False, "msg": "Sin token"}
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        return {"ok": r.status_code == 200, "msg": r.json().get("result", {}).get("username", "OK") if r.ok else str(r.status_code)}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def test_groq():
    log("🧠 Probando Groq...")
    token = get_token("GROQ_1")
    if not token:
        return {"ok": False, "msg": "Sin token"}
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {token}"},
                         json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Hola"}]},
                         timeout=10)
        return {"ok": r.status_code == 200, "msg": "OK" if r.ok else str(r.status_code)}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def test_cloudflare():
    log("☁️ Probando Cloudflare...")
    token = get_token("CF_JAIME")
    if not token:
        return {"ok": False, "msg": "Sin token"}
    return {"ok": True, "msg": "Token presente"}

def test_drive():
    log("💾 Probando Drive (rclone)...")
    r = subprocess.run("rclone listremotes 2>/dev/null", shell=True, capture_output=True, text=True)
    if r.stdout.strip():
        return {"ok": True, "msg": r.stdout.strip()}
    return {"ok": False, "msg": "No configurado"}

def run(args=None):
    log("🔗 INICIANDO MÓDULO DE CONEXIONES")
    resultados = {
        "github": test_github(),
        "telegram": test_telegram(),
        "groq": test_groq(),
        "cloudflare": test_cloudflare(),
        "drive": test_drive()
    }
    activos = [k for k, v in resultados.items() if v.get("ok")]
    log(f"✅ Conexiones activas: {', '.join(activos)}")
    with open(MIU_DIR / "nutrientes" / "conexiones.json", "w") as f:
        json.dump(resultados, f, indent=2)
    return resultados

if __name__ == "__main__":
    print(run())
