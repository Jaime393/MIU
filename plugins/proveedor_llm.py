#!/usr/bin/env python3
"""
PROVEEDOR LLM — Consulta modelos con credenciales recolectadas
Uso: python3 plugins/proveedor_llm.py "¿Qué es MIU?"
"""
import os, sys, json, urllib.request, urllib.error
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = MIU_DIR / "nutrientes"

def load_credentials():
    """Carga credenciales de credenciales_v2.json"""
    creds = {}
    path = NUTRIENTES / "credenciales_v2.json"
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        for h, c in data.items():
            t = c.get("tipo")
            if t in ("openrouter", "groq", "claude", "gemini"):
                if t not in creds:
                    creds[t] = []
                creds[t].append(c.get("token"))
    return creds

def query_openrouter(token, prompt):
    body = json.dumps({
        "model": "google/gemma-4-26b-a4b-it:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def query_groq(token, prompt):
    body = json.dumps({
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def query(prompt):
    """Intenta cada proveedor hasta que uno funcione."""
    creds = load_credentials()
    for servicio, tokens in creds.items():
        for token in tokens:
            if servicio == "openrouter":
                resp = query_openrouter(token, prompt)
                if not resp.startswith("Error"):
                    return {"ok": True, "servicio": servicio, "respuesta": resp}
            elif servicio == "groq":
                resp = query_groq(token, prompt)
                if not resp.startswith("Error"):
                    return {"ok": True, "servicio": servicio, "respuesta": resp}
    return {"ok": False, "error": "Ningún proveedor LLM disponible"}

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Hola, ¿qué es MIU?"
    result = query(prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))

