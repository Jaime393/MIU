#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GESTOR_APIS V1 — Gestor de fallback y rotación de APIs
Mantiene un registro de salud de cada API. Si una cae,
prueba alternativas, desactiva temporalmente, o busca nuevas keys.
"""
import os, json, time, subprocess
from pathlib import Path
from datetime import datetime

MIU_DIR = Path(os.environ.get("MIU_DIR", "os.path.expanduser('~')/miu-ecosistema"))
ESTADO_API = MIU_DIR / "nutrientes" / "estado_apis.json"
HISTORIAL = MIU_DIR / "nutrientes" / "historial_api.jsonl"

def log(msg):
    print(f"🔗 {msg}")

CATALOGO = {
    "claude": {
        "test_url": "https://api.anthropic.com/v1/models",
        "alternativas": ["openrouter", "groq", "local_llm"],
        "headers": lambda k: {"x-api-key": k, "anthropic-version": "2023-06-01"}
    },
    "github": {
        "test_url": "https://api.github.com/user",
        "alternativas": ["gitlab", "gitea_local", "codeberg"],
        "headers": lambda k: {"Authorization": f"token {k}"}
    },
    "telegram": {
        "test_url": None,
        "alternativas": ["discord_webhook", "matrix", "bus_local"],
        "headers": None
    },
    "groq": {
        "test_url": "https://api.groq.com/openai/v1/models",
        "alternativas": ["openrouter", "local_llm"],
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    "openrouter": {
        "test_url": "https://openrouter.ai/api/v1/models",
        "alternativas": ["groq", "local_llm"],
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    "cloudflare": {
        "test_url": "https://api.cloudflare.com/client/v4/user/tokens/verify",
        "alternativas": ["local_cache", "ipfs"],
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    }
}

def cargar_estado():
    if ESTADO_API.exists():
        with open(ESTADO_API) as f:
            return json.load(f)
    return {k: {"estado": "desconocido", "ultimo_check": None, "fallos": 0, "activa": True, "alternativa_actual": None} for k in CATALOGO}

def guardar_estado(estado):
    ESTADO_API.parent.mkdir(parents=True, exist_ok=True)
    with open(ESTADO_API, "w") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

def test_api(nombre, config):
    import urllib.request, urllib.error
    token = os.environ.get(f"{nombre.upper()}_TOKEN") or os.environ.get(f"{nombre.upper()}_API_KEY")
    if not token and nombre == "claude":
        token = os.environ.get("CLAUDE_KEY")
    if not token:
        return {"ok": False, "razon": "sin_token"}
    
    url = config["test_url"]
    if not url:
        return {"ok": False, "razon": "no_test_url"}
    
    try:
        req = urllib.request.Request(url, headers=config["headers"](token))
        req.add_header("User-Agent", "MIU-Autonomo/1.0")
        with urllib.request.urlopen(req, timeout=8) as resp:
            return {"ok": True, "status": resp.status}
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return {"ok": False, "razon": "token_expirado", "status": 401}
        return {"ok": False, "razon": f"http_{e.code}", "status": e.code}
    except Exception as e:
        return {"ok": False, "razon": str(e)}

estado = cargar_estado()
cambios = 0

for nombre, config in CATALOGO.items():
    log(f"Probando {nombre}...")
    res = test_api(nombre, config)
    
    reg = {
        "timestamp": datetime.now().isoformat(),
        "api": nombre,
        "ok": res["ok"],
        "razon": res.get("razon", "")
    }
    with open(HISTORIAL, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    
    if res["ok"]:
        estado[nombre]["estado"] = "ok"
        estado[nombre]["fallos"] = 0
        estado[nombre]["activa"] = True
        estado[nombre]["ultimo_check"] = datetime.now().isoformat()
        log(f"  ✅ {nombre} OK")
    else:
        estado[nombre]["fallos"] += 1
        estado[nombre]["estado"] = "fallo"
        estado[nombre]["ultimo_check"] = datetime.now().isoformat()
        log(f"  ❌ {nombre}: {res.get('razon', 'error')}")
        
        if estado[nombre]["fallos"] >= 3 and estado[nombre]["activa"]:
            alts = config.get("alternativas", [])
            if alts:
                estado[nombre]["alternativa_actual"] = alts[0]
                estado[nombre]["activa"] = False
                log(f"  🔄 Cambiando a alternativa: {alts[0]}")
                cambios += 1
            else:
                estado[nombre]["activa"] = False
                log(f"  🚫 Sin alternativas. API desactivada.")
                cambios += 1

guardar_estado(estado)
activas = sum(1 for v in estado.values() if v["activa"])
total = len(estado)
log(f"Resumen: {activas}/{total} APIs activas, {cambios} cambios de ruta")
print(f"🧬 {{'ok': True, 'activas': {activas}, 'total': {total}, 'cambios': {cambios}}}")

