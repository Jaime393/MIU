import os  # autocurador
#!/usr/bin/env python3
"""
Nodo Autónomo — Expansión y sincronización entre nodos
"""
import subprocess, json, time
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def run(args=None):
    print("🌱 Sincronizando con otros nodos...")
    
    # 1. Publicar estado en GitHub (para que otros nodos lo lean)
    try:
        subprocess.run(["python3", "miu_github.py", "upload", "miu-ecosistema", "state.json", "state.json"], cwd=MIU_DIR, timeout=30)
        print("✅ Estado publicado en GitHub")
    except Exception as e:
        print(f"❌ Error publicando: {e}")
    
    # 2. Buscar otros nodos (por ahora, solo GitHub)
    # (En el futuro, IPFS o libp2p)
    print("🔍 Buscando otros nodos...")
    # Simulación: leer repos de otros nodos
    r = subprocess.run("python3 miu_github.py list 2>/dev/null | grep miu-v153", shell=True, capture_output=True, text=True, cwd=MIU_DIR)
    otros = r.stdout.split("\n") if r.stdout else []
    
    print(f"📡 Encontrados {len(otros)} otros nodos")
    return {"otros": otros}
