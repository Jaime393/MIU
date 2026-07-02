"""
PIPELINE DE PUBLICACIÓN ZENODO — Nodo Darwin Core
===================================================
Publica huesos MIU en Zenodo con DOI automático.
Requiere token de Zenodo en variable de entorno ZENODO_TOKEN.

Uso: python zenodo_publish.py huesos/hueso_23_dimensionalidad_fractal_cuantica.md
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

ZENODO_API = "https://zenodo.org/api"

class ZenodoPublisher:
    """Publica huesos MIU en Zenodo con DOI."""
    
    def __init__(self, token=None):
        self.token = token or os.getenv("ZENODO_TOKEN")
        if not self.token:
            print("[Zenodo] ⚠️  Sin token. Modo simulación (dry-run).")
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    def create_deposition(self, title, description, authors=None):
        if not self.token:
            return {"id": "SIMULADO", "doi": "10.5281/zenodo.SIMULADO"}
        metadata = {
            "metadata": {
                "title": title,
                "upload_type": "publication",
                "publication_type": "preprint",
                "description": description,
                "creators": authors or [{"name": "Jaime Vicente", "affiliation": "MIU Framework"}],
                "access_right": "open",
                "license": "cc-by-4.0",
                "keywords": ["MIU", "coherencia", "fractal", "K_i", "informational resonance"],
                "notes": f"Generado por Nodo Darwin Core MIU v9. {datetime.now().isoformat()}"
            }
        }
        resp = requests.post(f"{ZENODO_API}/deposit/depositions", json=metadata, headers={**self.headers, "Content-Type": "application/json"})
        if resp.status_code == 201:
            return resp.json()
        print(f"[Zenodo] Error: {resp.status_code}")
        return None
    
    def upload_file(self, deposition_id, file_path):
        if not self.token:
            print(f"[Zenodo] SIMULADO: {file_path} → deposition {deposition_id}")
            return {"filename": str(file_path)}
        file_path = Path(file_path)
        with open(file_path, "rb") as f:
            resp = requests.post(f"{ZENODO_API}/deposit/depositions/{deposition_id}/files", data={"name": file_path.name}, files={"file": (file_path.name, f)}, headers=self.headers)
        return resp.json() if resp.status_code == 201 else None
    
    def publish(self, deposition_id):
        if not self.token:
            print(f"[Zenodo] SIMULADO: publicación deposition {deposition_id}")
            return {"doi": "10.5281/zenodo.SIMULADO"}
        resp = requests.post(f"{ZENODO_API}/deposit/depositions/{deposition_id}/actions/publish", headers=self.headers)
        if resp.status_code == 202:
            result = resp.json()
            print(f"[Zenodo] ✅ Publicado: {result.get('doi')}")
            return result
        return None
    
    def publish_hueso(self, hueso_path):
        hueso_path = Path(hueso_path)
        if not hueso_path.exists():
            return None
        content = hueso_path.read_text(encoding="utf-8")
        title = hueso_path.stem.replace("_", " ").title()
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
        dep = self.create_deposition(f"[MIU] {title}", content[:2000])
        if not dep:
            return None
        self.upload_file(dep["id"], hueso_path)
        return self.publish(dep["id"])

if __name__ == "__main__":
    import sys
    publisher = ZenodoPublisher()
    if len(sys.argv) > 1:
        for hueso in sys.argv[1:]:
            result = publisher.publish_hueso(hueso)
            if result:
                print(f"  DOI: {result.get('doi')}")
    else:
        print("Uso: python zenodo_publish.py huesos/hueso_23.md")
