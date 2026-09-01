#!/usr/bin/env python3
"""
MIU V∞+25 — CLAUDE BRIDGE
Usa la API de Claude (Anthropic) para razonamiento y generación de respuestas.
"""
import os, sys, json, time, subprocess, requests, sqlite3
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"
LOG_FILE = MIU_DIR / "logs" / "claude_bridge.log"
CHAT_LOG = MIU_DIR / "logs" / "chat_active.log"

# URL y clave de Claude desde el .env (o directamente si no está)
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "https://anajak.sbs/")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "fmg-Eaa9zaMboQJ5gdiunm3g-xQ2-CDoZzJnTrdBNeU-88s")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🤖 {msg}")

def chat(msg):
    with open(CHAT_LOG, "a") as f:
        f.write(f"[{datetime.now()}] 🤖 {msg}\n")

def guardar_conversacion(content, source="claude"):
    """Guarda una conversación en la base de datos"""
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("INSERT INTO conversations (content, source, timestamp) VALUES (?, ?, ?)",
                  (content, source, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log(f"❌ Error guardando conversación: {e}")
        return False

def ask_claude(prompt, system="Eres un nodo del micelio MIU. Responde con precisión y claridad.", max_tokens=1024):
    """Envía una consulta a la API de Claude"""
    if not CLAUDE_API_KEY or not CLAUDE_API_URL:
        log("⚠️ CLAUDE_API_KEY o CLAUDE_API_URL no configurados")
        return {"ok": False, "error": "Falta configuración"}
    
    url = CLAUDE_API_URL.rstrip('/') + "/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "anajak-sonnet-4.6",  # O el modelo que tengas disponible
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            response = r.json()
            content = response["content"][0]["text"]
            log(f"✅ Claude respondió: {content[:100]}...")
            return {"ok": True, "content": content}
        else:
            log(f"❌ Claude error {r.status_code}: {r.text[:200]}")
            return {"ok": False, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        log(f"❌ Claude excepción: {e}")
        return {"ok": False, "error": str(e)[:100]}

def run(args=None):
    log("🤖 INICIANDO CLAUDE BRIDGE")
    # Probar conexión con una pregunta simple
    log("📡 Probando conexión con Claude...")
    result = ask_claude("Responde 'OK' si estás funcionando.", system="Responde solo con 'OK'.")
    if result.get("ok"):
        log("✅ Conexión con Claude establecida.")
        chat("🤖 Claude API conectada y funcionando.")
        # Guardar la respuesta como conversación
        guardar_conversacion(f"Claude conectado: {result['content'][:200]}")
        return {"ok": True, "respuesta": result["content"]}
    else:
        log(f"❌ Error conectando con Claude: {result.get('error', 'Desconocido')}")
        return {"ok": False, "error": result.get("error")}

if __name__ == "__main__":
    print(run())
