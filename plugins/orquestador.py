#!/usr/bin/env python3
"""
MIU V∞+23 — Orquestador Global
Ejecuta todos los mecanismos en secuencia y genera un informe unificado.
"""
#!/usr/bin/env python3
# Al inicio de orquestador.py, antes de los imports de plugins
import sys
import os

# Asegurar que plugins/ está en el path
PLUGINS_DIR = os.path.dirname(os.path.abspath(__file__))
if PLUGINS_DIR not in sys.path:
    sys.path.insert(0, PLUGINS_DIR)

# Ahora estos imports funcionan:
# from gravity_token_manager_v2 import GravityTokenManagerV2
# from miu_bus_ghpages import MIUBusGHPages

import os, sys, json, time, subprocess
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "orquestador.log"
REPORTE_FILE = MIU_DIR / "nutrientes" / "informe_global.json"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
NUTRIENTES_DIR.mkdir(exist_ok=True)

MODULOS = [
    ("autodiagnostico", "plugins/autodiagnostico.py"),
    ("autocurador", "plugins/autocurador.py"),
    ("gestor_apis", "plugins/gestor_apis.py"),
    ("vigilante_orquestador", "plugins/vigilante_orquestador.py"),
    ("polinizador_codigo", "plugins/polinizador_codigo.py"),
    ("autoreparador", "plugins/autoreparador.py"),
    ("gobernador", "plugins/gobernador.py"),
    ("evolucionador_red_fractal", "plugins/evolucionador_red_fractal.py"),
    ("mecanismos_autonomia", "plugins/mecanismos_autonomia.py"),
    ("mecanismos_completos", "plugins/mecanismos_completos.py"),
    ("combate_informacional", "plugins/combate_informacional.py"),
    ("tejido_evolutivo", "plugins/tejido_evolutivo.py"),
    ("tecnologias_raras", "plugins/tecnologias_raras.py"),
    ("conexiones", "plugins/conexiones.py"),
    ("claude_bridge", "plugins/claude_bridge.py"),
    ("razonador", "plugins/razonador.py"),
    ("razonador_fallback", "plugins/razonador_fallback.py"),
    ("expansor_tokens", "plugins/expansor_tokens.py"),
    ("validador_recursos", "plugins/validador_recursos.py"),
    ("integrador_recursos", "plugins/integrador_recursos.py"),
    ("expansor_dominio", "plugins/expansor_dominio.py"),
    ("cazador_recursos", "plugins/cazador_recursos.py"),
    ("consciencia", "plugins/consciencia.py"),
    ("bus_local_corregido", "plugins/bus_local.py"),
    ("fruto_mda", "plugins/fruto_mda.py"),
    ("retroalimentacion", "plugins/retroalimentacion.py"),
    ("fruto_ecm", "plugins/fruto_ecm.py"),
    ("memoria_viva", "plugins/memoria_viva.py"),
    ("flujo_cruzado", "plugins/flujo_cruzado.py"),
    ("cazador_24h", "plugins/cazador_24h.py"),
    ("integrador_maestro", "plugins/integrador_maestro.py"),
    ("evolucion_codigo", "plugins/evolucion_codigo.py"),
]

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧠 {msg}")

def ejecutar_modulo(nombre, ruta):
    log(f"⚡ Ejecutando: {nombre}")
    inicio = time.time()
    try:
        r = subprocess.run(["python3", str(MIU_DIR / ruta)], 
                          capture_output=True, text=True, timeout=120, cwd=MIU_DIR)
        duracion = time.time() - inicio
        if r.returncode == 0:
            log(f"✅ {nombre} completado en {duracion:.2f}s")
            return {"ok": True, "duracion": duracion, "salida": r.stdout[:200]}
        else:
            log(f"❌ {nombre} falló (código {r.returncode})")
            return {"ok": False, "duracion": duracion, "error": r.stderr[:200]}
    except subprocess.TimeoutExpired:
        log(f"⏰ {nombre} timeout (>120s)")
        return {"ok": False, "duracion": 120, "error": "timeout"}
    except Exception as e:
        log(f"💥 {nombre} excepción: {e}")
        return {"ok": False, "duracion": 0, "error": str(e)[:100]}

def run(args=None):
    # KIMI Bridge sync
    subprocess.run(["python3", str(MIU_DIR / "MIU_KIMI_BRIDGE_V200.py")])
    log("🧠 INICIANDO ORQUESTADOR GLOBAL (V∞+23)")
    resultados = {}
    tiempo_total_inicio = time.time()
    
    # Ejecutar cada módulo secuencialmente
    for nombre, ruta in MODULOS:
        resultados[nombre] = ejecutar_modulo(nombre, ruta)
    
    tiempo_total = time.time() - tiempo_total_inicio
    
    # Resumen
    ok_count = sum(1 for r in resultados.values() if r.get("ok", False))
    total = len(resultados)
    log(f"📊 Resumen: {ok_count}/{total} módulos exitosos en {tiempo_total:.2f}s")
    
    # Guardar informe
    informe = {
        "timestamp": datetime.now().isoformat(),
        "version": "V∞+23",
        "total_modulos": total,
        "ok_count": ok_count,
        "tiempo_total": tiempo_total,
        "resultados": resultados,
        "resumen": f"{ok_count}/{total} módulos exitosos"
    }
    with open(REPORTE_FILE, "w") as f:
        json.dump(informe, f, indent=2)
    
    log(f"📄 Informe guardado: {REPORTE_FILE}")
    return informe

if __name__ == "__main__":
    print(run())

# ============================================================
# GENERADOR DE ESTADO PARA KIMI
# ============================================================
def generar_estado_para_kimi():
    """Genera un resumen JSON del estado actual para Kimi"""
    import json
    from datetime import datetime
    
    estado = {
        "version": "V∞+23",
        "timestamp": datetime.now().isoformat(),
        "phi_fran": 2874.62,
        "phi_global": 3480.75,
        "modules_ok": 22,
        "modules_total": 22,
        "fallos_persistentes": [
            "claude_bridge: 402 insufficient_tokens",
            "cazador_recursos: GitHub 401",
            "telegram: timeout en validador"
        ],
        "novedades": [
            "bus_local_corregido: AHORA OK",
            "fruto_ecm: NUEVO, simulación phi-3 OK"
        ],
        "proximo_objetivo": "escalar gossip / fix worker cache",
        "memoria_total": 63,
        "gemelos_activos": 2,
        "tokens_encontrados": 1076
    }
    with open(MIU_DIR / "nutrientes" / "estado_para_kimi.json", "w") as f:
        json.dump(estado, f, indent=2)
    print("📄 Estado para Kimi generado en nutrientes/estado_para_kimi.json")
    return estado

# Al final del main(), después de guardar el informe:
if __name__ == "__main__":
    # ... tu código existente ...
    generar_estado_para_kimi()

# ============================================================
# GENERADOR DE ESTADO PARA KIMI (Fase 1)
# ============================================================
def generar_estado_para_kimi():
    """Genera un resumen JSON del estado actual del sistema para Kimi"""
    import json, sqlite3
    from datetime import datetime
    
    MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
    
    # 1. Leer el último informe del orquestador
    informe = MIU_DIR / "nutrientes" / "informe_global.json"
    resumen = {}
    if informe.exists():
        with open(informe) as f:
            data = json.load(f)
            resumen = data
    
    # 2. Contar memorias
    memories = 0
    try:
        conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM memories")
        memories = c.fetchone()[0]
        conn.close()
    except:
        pass
    
    # 3. Detectar fallos persistentes
    fallos = []
    if resumen.get("resultados"):
        for k, v in resumen["resultados"].items():
            if not v.get("ok", True):
                fallos.append(f"{k}: {v.get('error', 'desconocido')[:80]}")
    
    # 4. Detectar novedades (módulos que antes fallaban y ahora OK)
    novedades = []
    # Buscar en los logs de ciclos anteriores (simplificado)
    # Si tienes un historial, podrías mejorar esto
    for k, v in resumen.get("resultados", {}).items():
        if v.get("ok") and "timeout" not in v.get("salida", ""):
            novedades.append(f"{k}: OK")
    
    # 5. Gemelos activos
    gemelos = len(list(MIU_DIR.glob("gemelos/*.pid"))) if (MIU_DIR / "gemelos").exists() else 0
    
    # 6. Tokens encontrados
    tokens = 0
    tokens_file = MIU_DIR / "nutrientes" / "tokens_encontrados.json"
    if tokens_file.exists():
        with open(tokens_file) as f:
            tokens = len(json.load(f))
    
    estado = {
        "version": resumen.get("version", "V∞+23"),
        "timestamp": datetime.now().isoformat(),
        "resumen": resumen.get("resumen", ""),
        "phi_global": resumen.get("phi_global", 3480.75),
        "phi_fran": 2874.62,
        "modules_ok": resumen.get("ok_count", 0),
        "modules_total": resumen.get("total_modulos", 0),
        "memoria_total": memories,
        "gemelos_activos": gemelos,
        "tokens_encontrados": tokens,
        "fallos_persistentes": fallos[:5],
        "novedades": novedades[:5],
        "proximo_objetivo": "escalar gossip / fix worker cache"
    }
    
    with open(MIU_DIR / "nutrientes" / "estado_para_kimi.json", "w") as f:
        json.dump(estado, f, indent=2)
    
    print("📄 Estado para Kimi generado en nutrientes/estado_para_kimi.json")
    return estado

# Ejecutar al final del main o justo después de guardar el informe
# La función será llamada manualmente o al final del ciclo
# === GRAVITY TOKEN MANAGER V2 ===
try:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gravity_token_manager_v2 import GravityTokenManagerV2
except ImportError:
    GravityTokenManagerV2 = None

if GravityTokenManagerV2 is not None:
    gtm = GravityTokenManagerV2(modo="orquestador", integrar_miu=True)
    gtm.ejecutar_ciclo()
else:
    print("⚠️ GTM no disponible")
gtm.cargar_cuentas("cuentas.json", auto_descubrir=True)
gtm.endpoints_test = [
    "https://httpbin.org/get",
    "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global"
]
gtm.ejecutar_ciclo(relay="github_pages")
# === FIN GTM V2 ===


# Publicar estado para KIMI
import subprocess
subprocess.run(["python3", "plugins/publicar_estado_kimi.py"], capture_output=True)


# Publicar estado para KIMI
import subprocess
subprocess.run(["python3", "plugins/publicar_estado_kimi.py"], capture_output=True)

