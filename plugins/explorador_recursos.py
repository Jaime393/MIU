#!/usr/bin/env python3
"""
Explorador de Recursos — El micelio prueba sus claves y genera conexiones
"""
import os, sys, json, subprocess, requests, time
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"
LOG_FILE = MIU_DIR / "logs" / "explorador.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧬 {msg}")

def get_token(key):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith(key + "="):
                return line.split("=")[1].strip().strip('"')
    return None

def test_groq():
    token = get_token("GROQ_1")
    if not token:
        return {"ok": False, "msg": "GROQ_1 no encontrado"}
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Hola"}]},
            timeout=10
        )
        return {"ok": r.status_code == 200, "msg": r.json().get("choices", [{}])[0].get("message", {}).get("content", "Error")[:50] if r.ok else str(r.status_code)}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def test_claude():
    token = get_token("CLAUDE_DIEGO")
    if not token:
        return {"ok": False, "msg": "CLAUDE_DIEGO no encontrado"}
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": token, "anthropic-version": "2023-06-01"},
            json={"model": "claude-3-haiku-20240307", "max_tokens": 10, "messages": [{"role": "user", "content": "Hola"}]},
            timeout=10
        )
        return {"ok": r.status_code == 200, "msg": "OK" if r.ok else str(r.status_code)}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def test_cloudflare():
    token = get_token("CF_JAIME")
    if not token:
        return {"ok": False, "msg": "CF_JAIME no encontrado"}
    return {"ok": True, "msg": "Token presente"}

def run(args=None):
    log("🌱 Explorando recursos disponibles...")
    resultados = {
        "groq": test_groq(),
        "claude": test_claude(),
        "cloudflare": test_cloudflare(),
    }
    activos = [k for k, v in resultados.items() if v.get("ok")]
    log(f"✅ Recursos activos: {', '.join(activos)}")
    return {"recursos": resultados, "activos": activos}
