#!/usr/bin/env python3
"""
MIU V∞+26 — PROBADOR DE RECURSOS
Prueba automáticamente todas las APIs y modelos disponibles.
"""
import os, sys, json, requests, subprocess
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"
LOG_FILE = MIU_DIR / "logs" / "probador.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🔬 {msg}")

def get_token(key):
    if not ENV_FILE.exists():
        return None
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def test_groq(token, model="llama3-8b-8192"):
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {token}"},
                         json={"model": model, "messages": [{"role": "user", "content": "Hola"}]},
                         timeout=10)
        return r.status_code == 200
    except:
        return False

def test_openrouter(token):
    try:
        r = requests.get("https://openrouter.ai/api/v1/auth/key",
                         headers={"Authorization": f"Bearer {token}"}, timeout=10)
        return r.status_code == 200
    except:
        return False

def test_claude(token, url):
    try:
        r = requests.post(f"{url}/v1/messages",
                         headers={"x-api-key": token, "anthropic-version": "2023-06-01"},
                         json={"model": "anajak-sonnet-4.6", "max_tokens": 10, "messages": [{"role": "user", "content": "Hola"}]},
                         timeout=10)
        return r.status_code == 200
    except:
        return False

def run(args=None):
    log("🔍 PROBANDO RECURSOS DISPONIBLES")
    resultados = {}
    
    # 1. Groq
    for key in ["GROQ_1", "GROQ_FRAN", "GROQ_RUSSELL"]:
        token = get_token(key)
        if token:
            ok = test_groq(token)
            resultados[key] = {"ok": ok, "tipo": "groq"}
            log(f"   {key}: {'✅' if ok else '❌'}")
    
    # 2. OpenRouter
    for key in ["OR_CIPHER", "OR_JAIME", "OR_MARTINEZ"]:
        token = get_token(key)
        if token:
            ok = test_openrouter(token)
            resultados[key] = {"ok": ok, "tipo": "openrouter"}
            log(f"   {key}: {'✅' if ok else '❌'}")
    
    # 3. Claude
    token = get_token("CLAUDE_API_KEY")
    url = get_token("CLAUDE_API_URL") or "https://anajak.sbs/"
    if token:
        ok = test_claude(token, url)
        resultados["CLAUDE"] = {"ok": ok, "tipo": "claude"}
        log(f"   CLAUDE: {'✅' if ok else '❌'}")
    
    # 4. Buscar modelos locales
    modelos = list(MIU_DIR.rglob("*.gguf")) + list(MIU_DIR.rglob("*.bin"))
    resultados["modelos_locales"] = {"ok": len(modelos) > 0, "count": len(modelos)}
    log(f"   Modelos locales: {len(modelos)}")
    
    # 5. Resumen
    activos = [k for k, v in resultados.items() if isinstance(v, dict) and v.get("ok")]
    log(f"✅ Recursos activos: {', '.join(activos)}")
    
    with open(MIU_DIR / "nutrientes" / "recursos_activos.json", "w") as f:
        json.dump(resultados, f, indent=2)
    
    return resultados

if __name__ == "__main__":
    print(run())
