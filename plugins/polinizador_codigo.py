#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POLINIZADOR_CODIGO V1 — Propagación de patrones evolutivos
Detecta qué módulos carecen de patrones sanos y propone donantes.
"""
import os, json, re
from pathlib import Path
from datetime import datetime
from collections import Counter

MIU_DIR = Path(os.environ.get("MIU_DIR", "os.path.expanduser('~')/miu-ecosistema"))
SEMENTERA = MIU_DIR / "nutrientes" / "sementera.json"

def log(msg):
    print(f"🌱 {msg}")

PATRONES_SANOS = {
    "manejo_excepciones": {
        "detectar": r'try:\s*\n.*?except\b',
        "ausencia_critica": True,
        "peso": 3
    },
    "logging": {
        "detectar": r'(print\s*\(|logging\.|log\s*\()',
        "ausencia_critica": False,
        "peso": 2
    },
    "backup_antes_escribir": {
        "detectar": r'(shutil\.copy|\.bak|backup)',
        "ausencia_critica": True,
        "peso": 3
    },
    "variables_entorno": {
        "detectar": r'os\.environ\.get',
        "ausencia_critica": False,
        "peso": 2
    },
    "timeout_requests": {
        "detectar": r'(timeout\s*=|urllib\.request\.urlopen\(.*timeout)',
        "ausencia_critica": True,
        "peso": 3
    }
}

sementera = []

for py in MIU_DIR.rglob("*.py"):
    if "plugins" not in str(py):
        continue
    try:
        code = py.read_text(encoding="utf-8", errors="ignore")
    except:
        continue
    
    mod_scores = {}
    for patron_nombre, config in PATRONES_SANOS.items():
        tiene = bool(re.search(config["detectar"], code, re.DOTALL))
        mod_scores[patron_nombre] = tiene
    
    for patron_nombre, config in PATRONES_SANOS.items():
        if not mod_scores[patron_nombre] and config["ausencia_critica"]:
            donantes = []
            for otro in MIU_DIR.rglob("*.py"):
                if otro == py:
                    continue
                try:
                    otro_code = otro.read_text(encoding="utf-8", errors="ignore")
                    if re.search(config["detectar"], otro_code, re.DOTALL):
                        donantes.append(str(otro))
                except:
                    pass
            
            sementera.append({
                "receptor": str(py),
                "patron_faltante": patron_nombre,
                "donantes_potenciales": donantes[:3],
                "peso": config["peso"],
                "timestamp": datetime.now().isoformat()
            })

SEMENTERA.parent.mkdir(parents=True, exist_ok=True)
with open(SEMENTERA, "w") as f:
    json.dump({"propuestas": sementera, "total": len(sementera)}, f, indent=2, ensure_ascii=False)

faltantes = Counter([s["patron_faltante"] for s in sementera])
log(f"Sementera generada: {len(sementera)} propuestas")
for patron, n in faltantes.most_common():
    log(f"  • {patron}: {n} módulos necesitan")

print(f"🧬 {{'ok': True, 'propuestas': {len(sementera)}, 'por_patron': dict(faltantes)}}")
