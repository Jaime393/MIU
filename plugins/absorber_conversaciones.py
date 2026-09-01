#!/usr/bin/env python3
"""
Absorción de Conversaciones — Extrae nutrientes de la memoria y los inyecta en el CAE
"""
import os, sys, json, sqlite3, re, time, subprocess
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
DB = MIU_DIR / "miu_brain.db"
LOG_FILE = MIU_DIR / "logs" / "absorbedor.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧬 {msg}")

def get_conversations(limit=20):
    """Obtiene las últimas N conversaciones"""
    if not DB.exists():
        return []
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT content, source, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def extraer_nutrientes(conversaciones):
    """Extrae ideas, órdenes y patrones de las conversaciones"""
    nutrientes = {
        "ordenes": [],
        "temas": [],
        "ideas_mutacion": []
    }
    for content, source, ts in conversaciones:
        texto = content.lower()
        # Detectar órdenes (ya mapeadas en escucha_ideas.py)
        if any(x in texto for x in ["escanea", "scan", "explora"]):
            nutrientes["ordenes"].append("scanner")
        if any(x in texto for x in ["absorbe", "nutriente", "busca"]):
            nutrientes["ordenes"].append("absorber")
        if any(x in texto for x in ["repara", "fix"]):
            nutrientes["ordenes"].append("autoreparar")
        if any(x in texto for x in ["guerra", "defensa", "amenaza"]):
            nutrientes["ordenes"].append("guerra")
        # Detectar temas
        temas = re.findall(r'\b(IA|inteligencia|defensa|guerra|ciber|seguridad|modelo|api|token|evolucion|mutacion)\b', texto)
        nutrientes["temas"].extend(temas)
        # Detectar ideas de mutación (frases que empiezan con "debería", "podría", "mejorar")
        ideas = re.findall(r'(mejorar|debería|podría|sugiero|propongo) (.*?)(?=\.|\n|$)', texto)
        for idea in ideas:
            nutrientes["ideas_mutacion"].append(idea[1].strip())
    # Limpiar duplicados
    nutrientes["temas"] = list(set(nutrientes["temas"]))
    nutrientes["ideas_mutacion"] = list(set(nutrientes["ideas_mutacion"]))
    return nutrientes

def inyectar_en_cae(nutrientes):
    """Inyecta los nutrientes en el CAE (modificando parámetros o generando mutaciones)"""
    # 1. Si hay temas de defensa/guerra, aumentar prioridad del módulo guerra
    if "guerra" in nutrientes["temas"] or "defensa" in nutrientes["temas"]:
        log("🛡️ Detectado interés en defensa. Aumentando frecuencia de guerra_fractal.py")
        # En modulos_loop.sh, cambiar frecuencia de guerra a 2h en lugar de 4h
        subprocess.run("sed -i 's/python3 plugins\\/guerra_fractal.py/python3 plugins\\/guerra_fractal.py/g' modulos_loop.sh", shell=True, cwd=MIU_DIR)
    # 2. Si hay ideas de mutación, generar una semilla de mutación para el CAE
    if nutrientes["ideas_mutacion"]:
        mutacion = {
            "timestamp": datetime.now().isoformat(),
            "fuente": "conversacion",
            "ideas": nutrientes["ideas_mutacion"][:3],
            "propuesta": "Ajustar parámetros del CAE basado en: " + "; ".join(nutrientes["ideas_mutacion"][:3])
        }
        with open(MIU_DIR / "nutrientes" / "mutacion_conversacion.json", "w") as f:
            json.dump(mutacion, f, indent=2)
        log(f"🧬 Generada semilla de mutación desde conversación: {mutacion['propuesta'][:80]}...")
    return True

def run(args=None):
    log("🌱 Absorbiendo nutrientes de conversaciones...")
    conversaciones = get_conversaciones(20)
    if not conversaciones:
        log("💤 No hay conversaciones para absorber.")
        return {"ok": True, "msg": "Sin conversaciones"}
    log(f"📚 Procesando {len(conversaciones)} conversaciones...")
    nutrientes = extraer_nutrientes(conversaciones)
    log(f"📊 Nutrientes extraídos: {len(nutrientes['ordenes'])} órdenes, {len(nutrientes['temas'])} temas, {len(nutrientes['ideas_mutacion'])} ideas.")
    inyectar_en_cae(nutrientes)
    log("✅ Absorción completada.")
    return {"ok": True, "nutrientes": nutrientes}

if __name__ == "__main__":
    print(run())
