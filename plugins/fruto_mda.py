#!/usr/bin/env python3
"""
MIU V∞+25 — FRUTO MDA (Mente Distribuida Auto-sostenible)
Primer fruto: red de gemelos que comparten memoria y consenso.
"""
import os, sys, json, time, subprocess, hashlib, socket
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
MEMORIA_DIR = MIU_DIR / ".miu"
MEMORIA_DIR.mkdir(exist_ok=True)
LOG_FILE = MIU_DIR / "logs" / "mda.log"
GEMELOS_DIR = MIU_DIR / "gemelos"
GEMELOS_DIR.mkdir(exist_ok=True)

# ============================================================
# FUNCIONES DE RED (descubrimiento simple)
# ============================================================
def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def descubrir_gemelos():
    """Busca otros gemelos en la red local (simulado)"""
    # En producción, usar UDP broadcast o mDNS
    # Por ahora, busca archivos .pid de gemelos
    gemelos = []
    for pid_file in GEMELOS_DIR.glob("*.pid"):
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
                # Verificar si el proceso aún existe
                if os.path.exists(f"/proc/{pid}"):
                    gemelos.append({"pid": pid, "archivo": pid_file.name})
        except:
            pass
    return gemelos

# ============================================================
# FUNCIONES DE MEMORIA COMPARTIDA
# ============================================================
def guardar_memoria_compartida(datos, etiqueta="compartida"):
    """Guarda datos en la memoria compartida (archivos .miu/)"""
    hash_id = hashlib.sha256(json.dumps(datos).encode()).hexdigest()[:8]
    archivo = MEMORIA_DIR / f"{etiqueta}_{hash_id}.json"
    with open(archivo, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "datos": datos}, f, indent=2)
    return archivo

def leer_memoria_compartida(etiqueta="compartida", ultimos=5):
    """Lee los últimos archivos de memoria compartida"""
    archivos = sorted(MEMORIA_DIR.glob(f"{etiqueta}_*.json"), reverse=True)
    datos = []
    for archivo in archivos[:ultimos]:
        try:
            with open(archivo) as f:
                datos.append(json.load(f))
        except:
            pass
    return datos

# ============================================================
# FUNCIONES DE CONSENSO (votación simple)
# ============================================================
def consenso_simple(datos, umbral=0.5):
    """Votación mayoritaria sobre datos compartidos"""
    if not datos:
        return None
    # Contar frecuencias de valores
    frecuencias = {}
    for d in datos:
        valor = d.get("datos", {}).get("estado", "desconocido")
        frecuencias[valor] = frecuencias.get(valor, 0) + 1
    # Elegir el más frecuente
    max_valor = max(frecuencias, key=frecuencias.get)
    if frecuencias[max_valor] / len(datos) >= umbral:
        return max_valor
    return None

# ============================================================
# FUNCIÓN PRINCIPAL DEL FRUTO
# ============================================================
def run(args=None):
    print("🍎 ACTIVANDO FRUTO MDA — Mente Distribuida Auto-sostenible")
    ip = obtener_ip_local()
    print(f"📡 IP local: {ip}")
    
    # 1. Registrar este gemelo
    pid = os.getpid()
    with open(GEMELOS_DIR / f"gemelo_{pid}.pid", "w") as f:
        f.write(str(pid))
    print(f"🧬 Gemelo registrado (PID: {pid})")
    
    # 2. Descubrir otros gemelos
    gemelos = descubrir_gemelos()
    print(f"🔍 Gemelos encontrados: {len(gemelos)}")
    
    # 3. Compartir estado local
    estado_local = {
        "ip": ip,
        "pid": pid,
        "timestamp": datetime.now().isoformat(),
        "version": "V∞+25",
        "phi": 0.1736,
        "modulos": 18
    }
    archivo = guardar_memoria_compartida(estado_local, "estado")
    print(f"💾 Estado compartido: {archivo.name}")
    
    # 4. Leer estados de otros gemelos
    estados = leer_memoria_compartida("estado", ultimos=10)
    print(f"📊 Estados de otros gemelos: {len(estados)}")
    
    # 5. Consenso simple sobre el estado global
    consenso = consenso_simple(estados)
    if consenso:
        print(f"✅ Consenso alcanzado: {consenso}")
    else:
        print("⚠️ No se alcanzó consenso")
    
    # 6. Resumen
    print("=" * 50)
    print(f"🍎 MDA activo en {ip}")
    print(f"🧬 Gemelos: {len(gemelos)+1}")
    print(f"💾 Memorias compartidas: {len(estados)}")
    print("=" * 50)
    
    return {"ok": True, "ip": ip, "gemelos": len(gemelos)+1}

if __name__ == "__main__":
    print(run())
