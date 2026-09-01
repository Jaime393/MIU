import os  # autocurador
#!/usr/bin/env python3
"""
Módulo Tejedor — Decide qué nutrientes absorber según el estado del sistema.
"""
import json, subprocess, sys
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTE_DIR = MIU_DIR / "nutrientes"

def run(args=None):
    print("🧵 Tejiendo nutrientes según carencias...")
    
    # Leer estado del sistema (desde miu_doctor o scanner)
    try:
        r = subprocess.run(["python3", str(MIU_DIR / "miu_scanner.py")], 
                         capture_output=True, text=True, timeout=30, cwd=MIU_DIR)
        output = r.stdout
    except Exception as e:
        return {"error": f"No se pudo escanear: {e}"}
    
    # Detectar carencias (simplificado)
    carencias = []
    if "conversations: 0" in output:
        carencias.append("conversaciones")
    if "procesos: 0" in output or "❌ 0 activos" in output:
        carencias.append("procesos")
    if "memories: 0" in output:
        carencias.append("memoria")
    
    # Decidir qué absorber
    acciones = []
    if "conversaciones" in carencias:
        acciones.append("Ejecutar absorber.py para buscar APIs de chat o modelos de lenguaje")
    if "procesos" in carencias:
        acciones.append("Ejecutar renovador.py para verificar tokens y luego iniciar bot")
    if "memoria" in carencias:
        acciones.append("Ejecutar absorber.py para buscar datasets de entrenamiento")
    
    # Si no hay carencias, buscar proactivamente
    if not acciones:
        acciones.append("Ejecutar absorber.py para buscar nuevas tecnologías emergentes")
    
    # Guardar plan
    plan_file = NUTRIENTE_DIR / "plan_tejido.json"
    plan = {
        "timestamp": str(Path().resolve()),
        "carencias": carencias,
        "acciones": acciones
    }
    with open(plan_file, "w") as f:
        json.dump(plan, f, indent=2)
    
    print(f"🧩 Plan de tejido generado: {len(acciones)} acciones")
    for a in acciones:
        print(f"   • {a}")
    return plan

if __name__ == "__main__":
    print(run())
