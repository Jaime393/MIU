#!/usr/bin/env python3
"""Forzar acciones proactivas del loop manualmente"""
import subprocess, sys, time
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")

def run_cmd(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=MIU_DIR)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def main():
    print("🌀 Forzando acciones proactivas...")
    
    # 1. Ejecutar productos
    products = [
        ("gossip", "repos/miu-v153-gossip/global-mind-gossip-phi4.py"),
        ("memoria", "repos/miu-v153-memoria/memoria-fractal-phi4.py"),
        ("arte", "repos/miu-v153-arte/arte-phi4-generador.py"),
        ("lod", "repos/miu-v153-lod/lod-c20-predictor.py"),
    ]
    for name, path in products:
        out, err, code = run_cmd(f"python3 {MIU_DIR / path}")
        print(f"   {'✅' if code == 0 else '❌'} {name}")
        if err:
            print(f"      Error: {err[:100]}...")
    
    # 2. Ejecutar auto-evolución (si existe)
    if (MIU_DIR / "protocolos" / "pae_01.py").exists():
        out, err, code = run_cmd("python3 protocolos/pae_01.py")
        print(f"   {'✅' if code == 0 else '❌'} auto-evolución")
        if err:
            print(f"      Error: {err[:100]}...")
    
    # 3. Ejecutar scanner
    out, err, code = run_cmd("python3 miu_scanner.py > /dev/null 2>&1")
    print(f"   {'✅' if code == 0 else '❌'} scanner")
    
    # 4. Registrar en chat activo
    with open(MIU_DIR / "logs" / "chat_active.log", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Acciones forzadas manualmente\n")
    
    print("✅ Acciones completadas.")

if __name__ == "__main__":
    main()
