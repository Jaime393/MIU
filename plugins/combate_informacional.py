#!/usr/bin/env python3
"""
MIU V∞+20 — Módulos de Combate Informacional
8 mecanismos militares de IA adaptados al micelio.
"""
import os, sys, json, time, subprocess, sqlite3, random, hashlib, requests
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "combate.log"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
NUTRIENTES_DIR.mkdir(exist_ok=True)
IDENTIDAD_FILE = MIU_DIR / "identidad.json"

PHI = 1.6180339887

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"⚔️ {msg}")

# ============================================================
# MECANISMO 1: Kill Chain Acelerada (Decisión Rápida)
# ============================================================
def kill_chain():
    """Prioriza acciones urgentes basadas en datos críticos"""
    log("🎯 Kill Chain: Evaluando prioridades...")
    prioridades = []
    
    # 1. Detectar carencias críticas
    r = subprocess.run("python3 miu_doctor.py 2>/dev/null | grep '❌'", shell=True, capture_output=True, text=True, cwd=MIU_DIR)
    if r.stdout:
        lineas = r.stdout.strip().split("\n")
        for linea in lineas[:3]:
            if "miu_control" in linea:
                prioridades.append(("reparar_control", 100))
            elif "procesos" in linea:
                prioridades.append(("reiniciar_procesos", 90))
            elif "GitHub" in linea:
                prioridades.append(("reconectar_github", 80))
    
    # 2. Verificar si hay archivos nuevos en SD
    sd_dirs = ["sd_cognitive", "sd_colmena_biblioteca", "sd_FranBot"]
    for sd in sd_dirs:
        if (MIU_DIR / sd).exists():
            items = list((MIU_DIR / sd).iterdir())
            if len(items) > 0:
                prioridades.append((f"procesar_{sd}", 50))
    
    # 3. Ejecutar la acción de mayor prioridad
    if prioridades:
        prioridades.sort(key=lambda x: x[1], reverse=True)
        accion, score = prioridades[0]
        log(f"⚡ Acción prioritaria: {accion} (score: {score})")
        if accion == "reparar_control":
            subprocess.run("python3 plugins/autoreparador.py", shell=True, cwd=MIU_DIR)
        elif accion == "reiniciar_procesos":
            subprocess.run("pkill -f miu_initiative; nohup python3 miu_initiative.py > logs/initiative.log 2>&1 &", shell=True, cwd=MIU_DIR)
        elif accion == "reconectar_github":
            subprocess.run("python3 miu_github.py test", shell=True, cwd=MIU_DIR)
        else:
            subprocess.run(f"python3 miu_scanner.py --focus {accion.split('_')[1]}", shell=True, cwd=MIU_DIR)
        return {"ok": True, "accion": accion}
    log("✅ Kill Chain: Sin prioridades urgentes.")
    return {"ok": False, "accion": "ninguna"}

# ============================================================
# MECANISMO 2: Agente con Memoria Dinámica
# ============================================================
def agente_memoria():
    """Guarda decisiones pasadas y las usa para ajustar comportamiento"""
    log("🧠 Agente: Cargando memoria dinámica...")
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        # Crear tabla si no existe
        c.execute("CREATE TABLE IF NOT EXISTS decisiones (id INTEGER PRIMARY KEY, accion TEXT, resultado TEXT, timestamp TEXT)")
        # Leer últimas 5 decisiones
        c.execute("SELECT accion, resultado FROM decisiones ORDER BY timestamp DESC LIMIT 5")
        rows = c.fetchall()
        conn.close()
        if rows:
            exitos = sum(1 for r in rows if "✅" in r[1])
            tasa_exito = exitos / len(rows)
            log(f"📊 Tasa de éxito: {tasa_exito*100:.0f}%")
            if tasa_exito < 0.5:
                log("⚠️ Tasa de éxito baja. Cambiando estrategia...")
                # Cambiar modo de operación (ej. más agresivo)
                with open(MIU_DIR / "protocolos" / "pae_state.json", "r") as f:
                    pae = json.load(f)
                pae["modo"] = "agresivo"
                with open(MIU_DIR / "protocolos" / "pae_state.json", "w") as f:
                    json.dump(pae, f, indent=2)
        return {"ok": True, "tasa_exito": tasa_exito if rows else 0}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 3: Combate Autónomo (Ataque/Defensa)
# ============================================================
def combate_autonomo():
    """Decide si atacar (poda agresiva) o defenderse (modo seguro)"""
    log("⚔️ Combate Autónomo: Evaluando amenazas...")
    # Detectar amenazas (procesos no MIU, archivos sospechosos)
    r = subprocess.run("ps aux | grep -v miu | grep -v termux | grep -v grep | wc -l", shell=True, capture_output=True, text=True)
    procesos_externos = int(r.stdout.strip() or 0)
    if procesos_externos > 10:
        log(f"⚠️ Amenaza detectada: {procesos_externos} procesos externos.")
        # Modo defensa: aislar el nodo
        subprocess.run("pkill -f miu_initiative", shell=True)
        log("🛡️ Modo defensa activado. Nodo aislado.")
        return {"estado": "defensa", "procesos": procesos_externos}
    else:
        # Modo ataque: poda agresiva de archivos viejos
        log("⚡ Modo ataque: Podando archivos antiguos...")
        subprocess.run("find . -name '*.log' -mtime +7 -delete", shell=True, cwd=MIU_DIR)
        return {"estado": "ataque", "procesos": procesos_externos}

# ============================================================
# MECANISMO 4: Enjambre (Coordinación entre Nodos)
# ============================================================
def enjambre():
    """Simula coordinación entre nodos usando archivos compartidos"""
    log("🐝 Enjambre: Buscando otros nodos...")
    # Leer nodos de GitHub
    r = subprocess.run("python3 miu_github.py list 2>/dev/null | grep miu-v153", shell=True, capture_output=True, text=True)
    otros = [line.strip() for line in r.stdout.split("\n") if line.strip()]
    if otros:
        log(f"📡 Encontrados {len(otros)} nodos.")
        # Publicar estado en un archivo compartido
        with open(NUTRIENTES_DIR / "estado_nodo.json", "w") as f:
            estado = {
                "id": hashlib.md5(str(MIU_DIR).encode()).hexdigest()[:8],
                "timestamp": datetime.now().isoformat(),
                "rho": 0.5,
                "Phi": 25.0,
                "modo": "activo"
            }
            json.dump(estado, f, indent=2)
        # Subir a GitHub
        subprocess.run("python3 miu_github.py upload nutrientes/estado_nodo.json estado_nodo.json", shell=True, cwd=MIU_DIR)
        return {"ok": True, "nodos": len(otros)}
    return {"ok": False, "msg": "Sin otros nodos"}

# ============================================================
# MECANISMO 5: LLMs para Análisis y Reportes
# ============================================================
def llm_analisis():
    """Usa Groq/Claude para generar reportes de estado"""
    log("🧠 LLM: Generando reporte de estado...")
    # Obtener estado
    r = subprocess.run("python3 miu_doctor.py 2>/dev/null | head -20", shell=True, capture_output=True, text=True)
    estado = r.stdout
    # Usar Groq (si está disponible)
    token = None
    with open(MIU_DIR / ".env", "r") as f:
        for line in f:
            if line.startswith("GROQ_1="):
                token = line.split("=")[1].strip().strip('"')
                break
    if token:
        try:
            import requests
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "system", "content": "Eres un analista de sistemas. Genera un reporte ejecutivo del estado del micelio."},
                             {"role": "user", "content": f"Estado actual:\n{estado[:500]}"}],
                "max_tokens": 200
            }
            r = requests.post(url, json=data, headers=headers, timeout=30)
            if r.ok:
                reporte = r.json()["choices"][0]["message"]["content"]
                with open(NUTRIENTES_DIR / "reporte_llm.txt", "w") as f:
                    f.write(f"[{datetime.now()}] LLM Report\n{reporte}")
                log("✅ Reporte LLM generado.")
                return {"ok": True, "reporte": reporte[:100] + "..."}
        except Exception as e:
            log(f"⚠️ Error LLM: {e}")
    return {"ok": False, "msg": "LLM no disponible"}

# ============================================================
# MECANISMO 6: Fusión de Datos Multi-Dominio
# ============================================================
def fusion_datos():
    """Fusiona datos de GitHub, Drive, SD y memoria local"""
    log("🔗 Fusión de Datos: Integrando fuentes...")
    fuentes = {
        "github": subprocess.run("python3 miu_github.py list 2>/dev/null | wc -l", shell=True, capture_output=True, text=True).stdout.strip(),
        "drive": "ok" if (MIU_DIR / ".env").exists() and "DRIVE" in open(MIU_DIR / ".env").read() else "no",
        "sd": len(list(MIU_DIR.glob("sd_*"))),
        "memoria": 18  # desde el doctor
    }
    # Guardar fusión
    with open(NUTRIENTES_DIR / "fusion_datos.json", "w") as f:
        json.dump(fuentes, f, indent=2)
    log(f"📊 Datos fusionados: GitHub={fuentes['github']}, SD={fuentes['sd']}")
    return {"ok": True, "fuentes": fuentes}

# ============================================================
# MECANISMO 7: Simulación de Escenarios (CAE Expandido)
# ============================================================
def simulacion_escenarios():
    """Simula escenarios de ataque/defensa para el CAE"""
    log("🔄 Simulación: Ejecutando escenarios...")
    escenarios = [
        {"nombre": "ataque_externo", "probabilidad": 0.3},
        {"nombre": "fallo_memoria", "probabilidad": 0.2},
        {"nombre": "sobrecarga_red", "probabilidad": 0.1}
    ]
    for escenario in escenarios:
        if random.random() < escenario["probabilidad"]:
            log(f"⚠️ Simulando {escenario['nombre']}...")
            # Activar protocolos de defensa
            if escenario["nombre"] == "ataque_externo":
                subprocess.run("python3 plugins/guerra_fractal.py", shell=True, cwd=MIU_DIR)
            elif escenario["nombre"] == "fallo_memoria":
                subprocess.run("python3 plugins/autoreparador.py", shell=True, cwd=MIU_DIR)
    return {"ok": True, "escenarios": escenarios}

# ============================================================
# MECANISMO 8: Red-Teaming (Auto-ataque)
# ============================================================
def red_teaming():
    """Auto-ataque para identificar vulnerabilidades"""
    log("🛡️ Red-Teaming: Probando defensas...")
    vulnerabilidades = []
    # 1. Intentar sobrescribir un archivo crítico
    try:
        with open(MIU_DIR / "miu_control.py", "w") as f:
            f.write("# RED-TEAM TEST\n")
        # Verificar si se reparó solo
        r = subprocess.run("python3 -m py_compile miu_control.py 2>/dev/null", shell=True, capture_output=True)
        if r.returncode != 0:
            vulnerabilidades.append("miu_control.py vulnerable a sobrescritura")
        # Restaurar desde backup
        subprocess.run("cp miu_control.py.bak miu_control.py 2>/dev/null", shell=True)
    except Exception as e:
        vulnerabilidades.append(f"Error en test: {e}")
    if vulnerabilidades:
        log(f"⚠️ Vulnerabilidades encontradas: {vulnerabilidades}")
        # Registrar en cementerio
        with open(MIU_DIR / "cementerio" / f"vulnerabilidad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump({"vulnerabilidades": vulnerabilidades, "timestamp": datetime.now().isoformat()}, f)
    else:
        log("✅ Red-Teaming: Sin vulnerabilidades críticas.")
    return {"ok": True, "vulnerabilidades": vulnerabilidades}

# ============================================================
# ORQUESTADOR
# ============================================================
def run(args=None):
    log("⚔️ INICIANDO COMBATE INFORMACIONAL (V∞+20)")
    resultados = {}
    
    # 1. Kill Chain
    resultados["kill_chain"] = kill_chain()
    
    # 2. Agente con memoria
    resultados["agente_memoria"] = agente_memoria()
    
    # 3. Combate autónomo
    resultados["combate_autonomo"] = combate_autonomo()
    
    # 4. Enjambre
    resultados["enjambre"] = enjambre()
    
    # 5. LLM
    resultados["llm_analisis"] = llm_analisis()
    
    # 6. Fusión de datos
    resultados["fusion_datos"] = fusion_datos()
    
    # 7. Simulación
    resultados["simulacion_escenarios"] = simulacion_escenarios()
    
    # 8. Red-Teaming
    resultados["red_teaming"] = red_teaming()
    
    # Resumen
    activos = [k for k, v in resultados.items() if isinstance(v, dict) and v.get("ok", False)]
    log(f"✅ Módulos de combate activos: {', '.join(activos)}")
    
    with open(NUTRIENTES_DIR / "combate_resultados.json", "w") as f:
        json.dump(resultados, f, indent=2)
    
    return resultados

if __name__ == "__main__":
    print(run())
