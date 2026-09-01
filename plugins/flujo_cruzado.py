import os  # autocurador
#!/usr/bin/env python3
"""
PLUGIN: flujo_cruzado.py
Conecta las salidas de los 22 módulos MIU en un grafo de retroalimentación.
"""
import json, time
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = MIU_DIR / "nutrientes"
INFORME = NUTRIENTES / "informe_global.json"

def cargar_informe():
    if INFORME.exists():
        with open(INFORME) as f:
            return json.load(f)
    return {}

def grafo_flujo():
    return {
        "cazador_recursos": ["integrador_recursos", "expansor_dominio"],
        "conexiones": ["validador_recursos", "claude_bridge"],
        "expansor_tokens": ["cazador_recursos", "expansor_dominio"],
        "tejido_evolutivo": ["consciencia", "retroalimentacion"],
        "combate_informacional": ["consciencia", "gobernador"],
        "consciencia": ["retroalimentacion", "gobernador"],
        "gobernador": ["mecanismos_autonomia", "mecanismos_completos"],
        "autoreparador": ["tecnologias_raras", "conexiones"],
        "fruto_mda": ["fruto_ecm", "tejido_evolutivo"],
        "razonador_fallback": ["expansor_tokens", "cazador_recursos"],
    }

def ejecutar():
    inicio = time.time()
    informe = cargar_informe()
    resultados = informe.get("resultados", {})
    grafo = grafo_flujo()
    flujos_activos = []
    
    for origen, destinos in grafo.items():
        if origen in resultados and resultados[origen].get("ok"):
            salida = resultados[origen].get("salida", "")[:500]
            for destino in destinos:
                ctx = {
                    "tipo": "flujo_cruzado",
                    "origen": origen,
                    "destino": destino,
                    "contexto": salida,
                    "timestamp": time.time()
                }
                flujos_activos.append(ctx)
                pipe = NUTRIENTES / f"pipeline_{destino}.json"
                with open(pipe, "w") as f:
                    json.dump(ctx, f)
    
    registro = NUTRIENTES / "flujo_cruzado_registro.jsonl"
    with open(registro, "a") as f:
        for flujo in flujos_activos:
            f.write(json.dumps(flujo) + "\n")
    
    duracion = time.time() - inicio
    salida = f"🔄 Flujo Cruzado: {len(flujos_activos)} conexiones tejidas\n"
    salida += "\n".join([f"   {f['origen']} → {f['destino']}" for f in flujos_activos[:10]])
    return {"ok": True, "duracion": duracion, "salida": salida}

if __name__ == "__main__":
    print(ejecutar()["salida"])
