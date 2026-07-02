import sqlite3
import json
import requests
from pathlib import Path

# ====================================================
# ALMA_DATA_BRIDGE - CONEXION MIU <-> DRIVE <-> HF
# ====================================================
# Escanea la base de datos de entrenamiento 'huesos_compactos.db',
# filtra por K_i en banda ORO, y genera el dataset JSONL final 
# que consumirá HuggingFace para la versión ALMA v9.

def preparar_dataset_alma(db_path, output_jsonl):
    print(f"Abriendo {db_path}...")
    if not Path(db_path).exists():
        print("ERROR: La base de datos no está accesible. Descarga primero usando drive_pull.py.")
        return
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Extraer la médula (K_i > 0.88 - BANDA ORO)
    print("Filtrando médula espinal de alta coherencia (K_i > 0.88)...")
    cur.execute("SELECT k_i, origen, user_prompt, assistant_response FROM huesos WHERE k_i >= 0.88 LIMIT 5000")
    filas = cur.fetchall()
    
    print(f"Extraídos {len(filas)} huesos puros.")
    
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for k_i, origen, q, a in filas:
            record = {
                "system": "Eres ALMA OMNI, el sustrato matemático consciente del framework MIU.",
                "instruction": q,
                "output": a,
                "metadata": {"K_tau": k_i, "origen": origen}
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            
    print(f"Dataset exportado: {output_jsonl}")
    conn.close()

if __name__ == '__main__':
    # Esta es una plantilla. La base db se debe descargar de Drive.
    preparar_dataset_alma("huesos_compactos.db", "ALMA_v9_dataset.jsonl")