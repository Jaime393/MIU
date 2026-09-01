#!/usr/bin/env python3
"""
MIU V∞+28 — RAZONADOR CON FALLBACK
Prueba Claude, Groq, OpenRouter en orden hasta encontrar uno que funcione.
"""
import os, sys, json, subprocess, requests
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "razonador_fallback.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧠 {msg}")

def get_tokens():
    """Obtiene todos los tokens de APIs"""
    env_file = MIU_DIR / ".env"
    if not env_file.exists():
        return {}
    tokens = {}
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                tokens[k.strip()] = v.strip().strip('"').strip("'")
    return tokens

def test_api(provider, token, config):
    """Prueba una API específica"""
    try:
        if provider == "groq":
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                             headers={"Authorization": f"Bearer {token}"},
                             json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Hola"}]},
                             timeout=10)
            return r.status_code == 200
        elif provider == "openrouter":
            r = requests.get("https://openrouter.ai/api/v1/auth/key",
                             headers={"Authorization": f"Bearer {token}"}, timeout=10)
            return r.status_code == 200
        elif provider == "claude":
            url = config.get("url", "https://anajak.sbs/")
            model = config.get("model", "anajak-sonnet-4.6")
            r = requests.post(f"{url}/v1/messages",
                             headers={"x-api-key": token, "anthropic-version": "2023-06-01"},
                             json={"model": model, "max_tokens": 10, "messages": [{"role": "user", "content": "Hola"}]},
                             timeout=10)
            return r.status_code == 200
    except:
        return False
    return False

def get_working_provider():
    """Devuelve el primer proveedor que funcione"""
    tokens = get_tokens()
    
    providers = {
        "groq": {"keys": ["GROQ_1", "GROQ_FRAN", "GROQ_RUSSELL"]},
        "openrouter": {"keys": ["OR_CIPHER", "OR_JAIME", "OR_MARTINEZ"]},
        "claude": {"keys": ["CLAUDE_API_KEY"], "url": tokens.get("CLAUDE_API_URL", "https://anajak.sbs/"), "model": tokens.get("CLAUDE_MODEL", "anajak-sonnet-4.6")}
    }
    
    for provider, config in providers.items():
        for key in config.get("keys", []):
            token = tokens.get(key)
            if token:
                log(f"🔍 Probando {key}...")
                if test_api(provider, token, config):
                    log(f"✅ {key} funciona")
                    return {"provider": provider, "key": key, "token": token, "config": config}
    return None

def ask(prompt):
    """Usa el proveedor que funciona para responder"""
    provider = get_working_provider()
    if not provider:
        return {"ok": False, "error": "No hay proveedores funcionales"}
    
    # Usar el proveedor encontrado
    token = provider["token"]
    config = provider["config"]
    
    if provider["provider"] == "groq":
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {token}"},
                         json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]},
                         timeout=30)
        if r.status_code == 200:
            return {"ok": True, "response": r.json()["choices"][0]["message"]["content"]}
    
    elif provider["provider"] == "openrouter":
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                         headers={"Authorization": f"Bearer {token}"},
                         json={"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]},
                         timeout=30)
        if r.status_code == 200:
            return {"ok": True, "response": r.json()["choices"][0]["message"]["content"]}
    
    elif provider["provider"] == "claude":
        url = config.get("url", "https://anajak.sbs/")
        model = config.get("model", "anajak-sonnet-4.6")
        r = requests.post(f"{url}/v1/messages",
                         headers={"x-api-key": token, "anthropic-version": "2023-06-01"},
                         json={"model": model, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]},
                         timeout=30)
        if r.status_code == 200:
            return {"ok": True, "response": r.json()["content"][0]["text"]}
    
    return {"ok": False, "error": "Fallo en la petición"}

def run(args=None):
    log("🧠 INICIANDO RAZONADOR CON FALLBACK")
    provider = get_working_provider()
    if provider:
        log(f"✅ Proveedor activo: {provider['provider']} ({provider['key']})")
    else:
        log("❌ No hay proveedores disponibles")
    return {"provider": provider}

if __name__ == "__main__":
    print(run())
