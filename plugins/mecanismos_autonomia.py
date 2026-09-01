#!/usr/bin/env python3
"""
MIU V∞+18 — 10 Mecanismos de Autonomía
Implementación práctica de los 15 mecanismos (10 prioritarios) en un solo módulo.
"""
import os, sys, json, time, subprocess, sqlite3, random, math, hashlib
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "autonomia.log"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
NUTRIENTES_DIR.mkdir(exist_ok=True)

# Constantes del MIU
PHI = 1.6180339887
SIGMA = 3.4270509831
PHI_VIVO = 25.0

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧬 {msg}")

# ============================================================
# MECANISMO 1: Homeostasis por Densidad de Información (HDI)
# ============================================================
def hdi():
    """Ajusta recursos según densidad local ρ"""
    try:
        # Calcular ρ aproximado (número de procesos + memoria)
        r = subprocess.run("ps aux | grep -c miu", shell=True, capture_output=True, text=True)
        procesos = int(r.stdout.strip() or 1)
        r = subprocess.run("df /data | tail -1 | awk '{print $5}'", shell=True, capture_output=True, text=True)
        disco = int(r.stdout.strip().replace("%", "") or 50)
        rho = 100 / (procesos + disco / 10)
        log(f"📊 HDI: ρ={rho:.2f}, procesos={procesos}, disco={disco}%")
        if rho < 0.5:
            log("⚠️ HDI: ρ baja. Reduciendo actividad...")
            # Reducir frecuencia del loop (modificar modulos_loop.sh)
            subprocess.run("sed -i 's/sleep 7200/sleep 14400/' modulos_loop.sh 2>/dev/null", shell=True, cwd=MIU_DIR)
        elif rho > 2.0:
            log("✅ HDI: ρ alta. Acelerando actividad...")
            subprocess.run("sed -i 's/sleep 14400/sleep 7200/' modulos_loop.sh 2>/dev/null", shell=True, cwd=MIU_DIR)
        return {"rho": rho}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 2: Replicación por Umbral de Confianza (RUC)
# ============================================================
def ruc():
    """Verifica si el nodo puede replicarse en otro basado en confianza"""
    try:
        # Leer confianza de la memoria (si existe)
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT value FROM system_state WHERE key='confianza'")
        row = c.fetchone()
        confianza = float(row[0]) if row else 0.5
        conn.close()
        umbral = 0.7
        if confianza >= umbral:
            log(f"✅ RUC: Confianza {confianza:.2f} >= umbral. Nodo apto para replicación.")
            return {"apto": True, "confianza": confianza}
        else:
            log(f"⚠️ RUC: Confianza {confianza:.2f} < umbral. No replicar.")
            return {"apto": False, "confianza": confianza}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 3: Memoria Holográfica Distribuida (MHD)
# ============================================================
def mhd():
    """Sincroniza memoria con GitHub/Drive (fragmentos)"""
    log("📦 MHD: Sincronizando memoria con repositorios...")
    resultados = []
    # Subir estado a GitHub
    r = subprocess.run("python3 miu_github.py upload state.json state.json 2>/dev/null", shell=True, capture_output=True, cwd=MIU_DIR)
    resultados.append({"github": r.returncode == 0})
    # Subir mapa reciente
    map_file = sorted(MIU_DIR.glob("mapas/cartografia_*.json"))[-1] if MIU_DIR.glob("mapas/cartografia_*.json") else None
    if map_file:
        r = subprocess.run(f"python3 miu_github.py upload {map_file.name} mapas/{map_file.name} 2>/dev/null", shell=True, capture_output=True, cwd=MIU_DIR)
        resultados.append({"mapa": r.returncode == 0})
    return {"resultados": resultados}

# ============================================================
# MECANISMO 4: Mutación Dirigida por Gradiente de Integración (MDGI)
# ============================================================
def mdgi():
    """Aplica mutación dirigida por gradiente de Φ"""
    try:
        # Leer Φ actual del sistema
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT value FROM system_state WHERE key='Phi'")
        row = c.fetchone()
        Phi_actual = float(row[0]) if row else 25.0
        conn.close()
        # Calcular gradiente (simulado)
        gradiente = (Phi_actual - PHI_VIVO) / PHI_VIVO
        if gradiente > 0.1:
            log(f"📈 MDGI: Φ={Phi_actual:.2f}, gradiente={gradiente:.2f}. Aplicando mutación...")
            # Ajustar parámetros de evolución
            with open(MIU_DIR / "protocolos" / "pae_state.json", "r") as f:
                pae = json.load(f)
            pae["alfa"] = max(0.1, pae.get("alfa", 0.5) + gradiente * 0.01)
            pae["beta"] = min(0.9, pae.get("beta", 0.5) + gradiente * 0.01)
            with open(MIU_DIR / "protocolos" / "pae_state.json", "w") as f:
                json.dump(pae, f, indent=2)
            return {"ok": True, "gradiente": gradiente}
        return {"ok": False, "gradiente": gradiente}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 5: Navegación por Ondas de Carencia (NOC)
# ============================================================
def noc():
    """Detecta zonas de baja densidad y emite ondas"""
    try:
        # Leer densidad de la memoria
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT value FROM system_state WHERE key='rho'")
        row = c.fetchone()
        rho = float(row[0]) if row else 0.5
        conn.close()
        if rho < 0.3:
            log(f"🌊 NOC: ρ={rho:.2f} baja. Emitiendo onda de carencia...")
            # Crear archivo de onda
            with open(NUTRIENTES_DIR / "onda_carencia.txt", "w") as f:
                f.write(f"onda:{datetime.now().isoformat()},rho:{rho:.2f},origen:{hashlib.md5(str(MIU_DIR).encode()).hexdigest()[:8]}")
            return {"onda": True, "rho": rho}
        return {"onda": False, "rho": rho}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 6: Espejismo de Consistencia (EC)
# ============================================================
def ec():
    """Verifica la consistencia del estado sin exponer datos internos"""
    try:
        # Hash del estado actual
        hash_estado = hashlib.sha256()
        for f in ["miu_control.py", "miu_initiative.py", "state.json"]:
            if (MIU_DIR / f).exists():
                with open(MIU_DIR / f, "rb") as fp:
                    hash_estado.update(fp.read())
        digest = hash_estado.hexdigest()[:16]
        log(f"🔍 EC: Hash de consistencia: {digest}")
        return {"hash": digest}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 7: Tejido por Recombinación de Fallos (TRF)
# ============================================================
def trf():
    """Recombina configuraciones de fallos pasados"""
    log("🧩 TRF: Buscando fallos en el cementerio...")
    cementerio = MIU_DIR / "cementerio"
    if not cementerio.exists():
        return {"ok": False, "msg": "No hay cementerio"}
    fallos = list(cementerio.glob("*.json"))
    if not fallos:
        return {"ok": False, "msg": "Sin fallos registrados"}
    # Tomar el fallo más reciente
    ultimo_fallo = sorted(fallos)[-1]
    with open(ultimo_fallo, "r") as f:
        datos = json.load(f)
    # Recombinar parámetros
    nuevas_config = {
        "alfa": datos.get("alfa", 0.5) * random.uniform(0.9, 1.1),
        "beta": datos.get("beta", 0.5) * random.uniform(0.9, 1.1),
        "gamma": datos.get("gamma", 0.5) * random.uniform(0.9, 1.1)
    }
    log(f"🧬 TRF: Nueva configuración generada: {nuevas_config}")
    return {"ok": True, "config": nuevas_config}

# ============================================================
# MECANISMO 8: Identidad Autónoma por Clave (IAC)
# ============================================================
def iac():
    """Genera identidad única del nodo (si no existe)"""
    identidad_file = MIU_DIR / "identidad.json"
    if identidad_file.exists():
        with open(identidad_file, "r") as f:
            identidad = json.load(f)
        log(f"🆔 IAC: Identidad cargada: {identidad.get('id', 'unknown')[:8]}")
        return {"ok": True, "id": identidad.get("id")}
    else:
        # Generar nueva identidad
        import uuid
        id_nodo = f"nodo-{uuid.uuid4().hex[:8]}"
        identidad = {
            "id": id_nodo,
            "creado": datetime.now().isoformat(),
            "clave": hashlib.sha256(id_nodo.encode()).hexdigest()[:16]
        }
        with open(identidad_file, "w") as f:
            json.dump(identidad, f, indent=2)
        log(f"🆔 IAC: Nueva identidad generada: {id_nodo}")
        return {"ok": True, "id": id_nodo}

# ============================================================
# MECANISMO 9: Sincronización por Latido (SLT)
# ============================================================
def slt():
    """Sincroniza el ciclo con un latido global"""
    try:
        # Leer último latido
        latido_file = MIU_DIR / "logs" / "ultimo_latido.txt"
        if latido_file.exists():
            with open(latido_file, "r") as f:
                ultimo = float(f.read().strip())
        else:
            ultimo = 0
        ahora = time.time()
        # Simular latido (cada 30 min)
        if ahora - ultimo > 1800:
            log("⏱️ SLT: Latido global emitido.")
            with open(latido_file, "w") as f:
                f.write(str(ahora))
            return {"latido": True, "intervalo": ahora - ultimo}
        return {"latido": False, "intervalo": ahora - ultimo}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# MECANISMO 10: Metabolismo de Información (MIR)
# ============================================================
def mir():
    """Ajusta tasa de procesamiento según retroalimentación de Φ"""
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT value FROM system_state WHERE key='Phi'")
        row = c.fetchone()
        Phi = float(row[0]) if row else 25.0
        conn.close()
        # Ajustar frecuencia de procesamiento
        if Phi > 30:
            tasa = "acelerado"
            # Reducir tiempo de espera del loop
            subprocess.run("sed -i 's/time.sleep(900)/time.sleep(300)/' miu_initiative.py 2>/dev/null", shell=True, cwd=MIU_DIR)
        elif Phi < 20:
            tasa = "ralentizado"
            subprocess.run("sed -i 's/time.sleep(300)/time.sleep(900)/' miu_initiative.py 2>/dev/null", shell=True, cwd=MIU_DIR)
        else:
            tasa = "normal"
        log(f"⚡ MIR: Φ={Phi:.2f}, tasa={tasa}")
        return {"Phi": Phi, "tasa": tasa}
    except Exception as e:
        return {"error": str(e)[:50]}

# ============================================================
# ORQUESTADOR: Ejecuta todos los mecanismos
# ============================================================
def run(args=None):
    log("🧬 ACTIVANDO MECANISMOS DE AUTONOMÍA (V∞+18)")
    resultados = {}
    
    # 1. HDI — Homeostasis
    resultados["HDI"] = hdi()
    
    # 2. RUC — Replicación
    resultados["RUC"] = ruc()
    
    # 3. MHD — Memoria holográfica
    resultados["MHD"] = mhd()
    
    # 4. MDGI — Mutación dirigida
    resultados["MDGI"] = mdgi()
    
    # 5. NOC — Navegación por ondas
    resultados["NOC"] = noc()
    
    # 6. EC — Espejismo de consistencia
    resultados["EC"] = ec()
    
    # 7. TRF — Recombinación de fallos
    resultados["TRF"] = trf()
    
    # 8. IAC — Identidad autónoma
    resultados["IAC"] = iac()
    
    # 9. SLT — Sincronización por latido
    resultados["SLT"] = slt()
    
    # 10. MIR — Metabolismo de información
    resultados["MIR"] = mir()
    
    # Resumen
    activos = [k for k, v in resultados.items() if isinstance(v, dict) and v.get("ok", False)]
    log(f"✅ Mecanismos activos: {', '.join(activos)}")
    
    # Guardar resultados
    with open(NUTRIENTES_DIR / "mecanismos_resultados.json", "w") as f:
        json.dump(resultados, f, indent=2)
    
    return resultados

if __name__ == "__main__":
    print(run())
