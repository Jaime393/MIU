#!/usr/bin/env python3
"""
Conversador Autónomo — El micelio genera diálogos con IA para poblar memoria
"""
import os, sys, json, subprocess, requests, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"

def get_token():
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("GROQ_1="):
                return line.split("=")[1].strip().strip('"')
    return None

def conversar(prompt):
    token = get_token()
    if not token:
        return {"ok": False, "msg": "No hay token GROQ"}
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        if r.ok:
            return {"ok": True, "respuesta": r.json()["choices"][0]["message"]["content"]}
        return {"ok": False, "msg": str(r.status_code)}
    except Exception as e:
        return {"ok": False, "msg": str(e)[:50]}

def run(args=None):
    print("💬 Generando conversación autónoma...")
    temas = ["¿Qué es el micelio?", "Explica la Global Mind", "¿Cómo evoluciona un sistema autónomo?"]
    prompt = temas[int(time.time()) % len(temas)]
    resultado = conversar(prompt)
    if resultado.get("ok"):
        # Guardar en memoria
        try:
            conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
            c = conn.cursor()
            c.execute("INSERT INTO conversations (content, source, timestamp) VALUES (?, ?, ?)",
                      (f"IA: {resultado['respuesta'][:200]}", "groq", datetime.now().isoformat()))
            conn.commit()
            conn.close()
            print("✅ Conversación guardada en memoria")
        except Exception as e:
            print(f"⚠️ No se pudo guardar: {e}")
    return resultado
