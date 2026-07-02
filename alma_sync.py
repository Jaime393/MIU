import os
import urllib.request
import json
from pathlib import Path

# ALMA OMNI Sync - Miu Coherencia v3.0
# Extrae y valida la coherencia (K_tau) usando los datasets de HuggingFace

HF_DATASET_REPO = "Jaime393/ALMA_huesos"
HF_MODEL_REPO = "Jaime393/MIU_ALMA_OMNI"

def fetch_hf_file(repo, file_path, repo_type="dataset"):
    url = f"https://huggingface.co/{repo_type}s/{repo}/resolve/main/{file_path}"
    print(f"Descargando {file_path} desde {repo}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MIU-Coherence/3.0'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error descargando {file_path}: {e}")
        return None

def sync_alma():
    print("=== INICIANDO SINCRONIZACIÓN ALMA OMNI ===")

    # 1. Bajar métricas del modelo (resultados_ki_bench.txt)
    ki_bench = fetch_hf_file(HF_MODEL_REPO, "resultados_ki_bench.txt", "model")
    if ki_bench:
        Path("resultados_ki_bench.txt").write_bytes(ki_bench)
        print("[OK] Benchmark K_i descargado.")

    # 2. Bajar dataset de contraste (dataset_contraste_500_limpio.jsonl)
    dataset = fetch_hf_file(HF_DATASET_REPO, "dataset_contraste_500_limpio.jsonl", "dataset")
    if dataset:
        Path("dataset_contraste_500.jsonl").write_bytes(dataset)
        print("[OK] Dataset de contraste ALMA_huesos descargado.")

    print("Sincronización ALMA completada. Sustrato listo para validación cruzada.")

if __name__ == "__main__":
    sync_alma()
