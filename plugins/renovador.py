#!/usr/bin/env python3
"""
Módulo Renovador — Renovación automática de tokens
Verifica y renueva tokens de servicios.
"""
import os, re, json, subprocess
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
ENV_FILE = MIU_DIR / ".env"
TOKEN_STATE = MIU_DIR / "nutrientes" / "token_state.json"

def run(args=None):
    print("🔑 Verificando tokens...")
    cambios = []
    
    # 1. Cargar .env
    if not ENV_FILE.exists():
        return {"error": ".env no encontrado"}
    with open(ENV_FILE) as f:
        lines = f.readlines()
    
    # 2. Verificar GitHub token
    token_gh = None
    for line in lines:
        if line.startswith("GITHUB_TOKEN"):
            token_gh = line.split("=")[1].strip().strip('"')
            break
    if token_gh:
        # Verificar si el token es válido (request a GitHub)
        r = subprocess.run(
            f"curl -s -H 'Authorization: token {token_gh}' https://api.github.com/user",
            shell=True, capture_output=True, text=True
        )
        if "login" in r.stdout:
            print("✅ GitHub token válido")
        else:
            print("⚠️ GitHub token inválido o expirado. Sugerir renovación.")
            cambios.append("GITHUB_TOKEN requiere renovación (usa miu_github.py --refresh)")
    
    # 3. Verificar HuggingFace token
    token_hf = None
    for line in lines:
        if line.startswith("HUGGINGFACE_TOKEN"):
            token_hf = line.split("=")[1].strip().strip('"')
            break
    if token_hf:
        r = subprocess.run(
            f"curl -s -H 'Authorization: Bearer {token_hf}' https://huggingface.co/api/whoami",
            shell=True, capture_output=True, text=True
        )
        if "name" in r.stdout:
            print("✅ HuggingFace token válido")
        else:
            print("⚠️ HuggingFace token inválido. Sugerir renovación.")
            cambios.append("HUGGINGFACE_TOKEN requiere renovación (usa huggingface-cli login)")
    
    # 4. Verificar Telegram bot token
    token_tg = None
    for line in lines:
        if line.startswith("BOT_TABLET_TOKEN"):
            token_tg = line.split("=")[1].strip().strip('"')
            break
    if token_tg:
        r = subprocess.run(
            f"curl -s https://api.telegram.org/bot{token_tg}/getMe",
            shell=True, capture_output=True, text=True
        )
        if "ok" in r.stdout and '"ok":true' in r.stdout:
            print("✅ Telegram token válido")
        else:
            print("⚠️ Telegram token inválido. Sugerir renovación.")
            cambios.append("BOT_TABLET_TOKEN requiere renovación")
    
    # Guardar estado
    TOKEN_STATE.parent.mkdir(exist_ok=True)
    with open(TOKEN_STATE, "w") as f:
        json.dump({"ultima_verificacion": str(Path().resolve()), "cambios": cambios}, f, indent=2)
    
    print(f"✅ Renovación completada. {len(cambios)} cambios sugeridos.")
    return {"cambios": cambios}

if __name__ == "__main__":
    print(run())
