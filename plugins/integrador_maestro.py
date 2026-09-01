import os  # autocurador
#!/usr/bin/env python3
"""
PLUGIN: integrador_maestro.py
Cerebro del cerebro. Lee pipelines, estado mental y hallazgos. Genera plan_maestro.json.
"""
import json, time
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = MIU_DIR / "nutrientes"
PLAN = NUTRIENTES / "plan_maestro.json"

def leer_pipelines():
    pipes = []
    for p in NUTRIENTES.glob("pipeline_*.json"):
        with open(p) as f:
            pipes.append(json.load(f))
    return pipes

def leer_estado_mental():
    path = NUTRIENTES / "estado_mental.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def leer_hallazgos():
    path = NUTRIENTES / "cola_hallazgos.jsonl"
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()][-10:]

def generar_plan(pipelines, estado, hallazgos):
    acciones = []
    if estado.get("modulos_fallidos", 0) > 0:
        acciones.append({"tipo": "reparar", "target": "modulos_fallidos", "prioridad": 1})
    for h in hallazgos:
        if h.get("prioridad") == "alta":
            acciones.append({"tipo": "integrar", "target": h["nombre"], "prioridad": 2})
    for pipe in pipelines:
        acciones.append({"tipo": "flujo", "origen": pipe.get("origen"), "destino": pipe.get("destino"), "prioridad": 3})
    if estado.get("salud", 0) > 0.9:
        acciones.append({"tipo": "evolucionar", "target": "codigo_propio", "prioridad": 4})
    return {
        "timestamp": time.time(),
        "acciones": sorted(acciones, key=lambda x: x["prioridad"]),
        "estado_base": estado,
        "n_hallazgos": len(hallazgos),
        "n_pipelines": len(pipelines)
    }

def ejecutar():
    inicio = time.time()
    pipelines = leer_pipelines()
    estado = leer_estado_mental()
    hallazgos = leer_hallazgos()
    plan = generar_plan(pipelines, estado, hallazgos)
    with open(PLAN, "w") as f:
        json.dump(plan, f, indent=2)
    duracion = time.time() - inicio
    salida = f"🧭 Integrador Maestro: {len(plan['acciones'])} acciones planificadas\n"
    salida += f"   Pipelines: {plan['n_pipelines']} | Hallazgos: {plan['n_hallazgos']}\n"
    for a in plan["acciones"][:5]:
        tgt = a.get('target') or a.get('destino')
        salida += f"   [{a['prioridad']}] {a['tipo']} → {tgt}\n"
    return {"ok": True, "duracion": duracion, "salida": salida}

if __name__ == "__main__":
    print(ejecutar()["salida"])
