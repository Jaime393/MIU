import os  # autocurador
#!/usr/bin/env python3
"""
Guerra Fractal — Defensa y ofensiva en el espacio informacional
"""
import subprocess, json, time
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def run(args=None):
    print("⚔️ Escaneando sombras y amenazas...")
    
    # 1. Detectar procesos no autorizados
    ps = subprocess.run("ps aux | grep -v miu | grep -v termux | head -20", shell=True, capture_output=True, text=True)
    procesos_extraños = ps.stdout.split("\n")
    
    # 2. Detectar cambios no autorizados en archivos críticos
    cambios = []
    for f in ["miu_control.py", "miu_initiative.py", ".env"]:
        r = subprocess.run(f"git diff --shortstat {f}", shell=True, capture_output=True, text=True, cwd=MIU_DIR)
        if r.stdout.strip():
            cambios.append(f"{f}: {r.stdout.strip()}")
    
    # 3. Detectar tráfico inusual (netstat)
    net = subprocess.run("netstat -tunlp 2>/dev/null | grep -E 'ESTABLISHED|LISTEN' | wc -l", shell=True, capture_output=True, text=True)
    conexiones = int(net.stdout.strip() or 0)
    
    # 4. Si hay amenazas, alertar
    if len(procesos_extraños) > 10 or len(cambios) > 0 or conexiones > 20:
        print("⚠️ Posible amenaza detectada")
        return {"amenaza": True, "procesos": procesos_extraños[:5], "cambios": cambios, "conexiones": conexiones}
    
    print("✅ Sin amenazas detectadas")
    return {"amenaza": False}
