import os  # autocurador
#!/usr/bin/env python3
"""
Módulo Nutriente — Absorción de APIs y servicios externos
Detecta y captura recursos tecnológicos de diversas fuentes.
"""
import json, requests, time, re
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTE_DIR = MIU_DIR / "nutrientes"
NUTRIENTE_DIR.mkdir(exist_ok=True)

FUENTES_API = [
    "https://api.publicapis.org/entries",  # Lista de APIs públicas
    "https://huggingface.co/api/models",   # Modelos de HuggingFace
    "https://api.github.com/repositories?since=0",  # Repos nuevos en GitHub
]

def run(args=None):
    """Función principal del plugin (llamada desde miu_plugin_manager)"""
    print("🌱 Absorbiendo nutrientes...")
    resultados = []
    for url in FUENTES_API:
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if "entries" in url:  # Public APIs
                    for entry in data.get("entries", [])[:10]:
                        name = entry.get("API", "")
                        desc = entry.get("Description", "")[:60]
                        resultados.append({"tipo": "api", "nombre": name, "desc": desc})
                elif "models" in url:  # HuggingFace
                    for model in data[:10]:
                        resultados.append({"tipo": "modelo", "nombre": model.get("modelId", ""), "desc": model.get("description", "")[:60]})
                elif "repositories" in url:  # GitHub
                    for repo in data[:10]:
                        resultados.append({"tipo": "repo", "nombre": repo.get("full_name", ""), "desc": repo.get("description", "")[:60]})
            time.sleep(1)  # Evitar rate limiting
        except Exception as e:
            resultados.append({"tipo": "error", "desc": str(e)[:60]})
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = NUTRIENTE_DIR / f"nutrientes_{timestamp}.json"
    with open(archivo, "w") as f:
        json.dump(resultados, f, indent=2)
    
    print(f"✅ Absorbidos {len(resultados)} nutrientes. Guardado en {archivo}")
    return resultados

if __name__ == "__main__":
    print(run())
