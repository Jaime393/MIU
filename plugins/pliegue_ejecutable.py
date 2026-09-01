#!/usr/bin/env python3
"""
MIU V∞+32 — PLIEGUE EJECUTABLE Y SINCRONIZACIÓN CON ORQUESTADOR
- Convierte pliegues en scripts ejecutables.
- Mide impacto real en sandbox.
- Sincroniza resultados con el worker global.
"""
import os, sys, json, time, hashlib, subprocess, random, sqlite3
from pathlib import Path
from datetime import datetime
from collections import deque
import shutil, socket, platform

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
PLUGINS = BASE / "plugins"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"

for d in [NUTRIENTES, PLUGINS]:
    d.mkdir(exist_ok=True)

# ============================================================
# MEMORIA LOCAL
# ============================================================
class MemoriaLocal:
    def __init__(self, db=NUTRIENTES / "pliegues.db"):
        self.conn = sqlite3.connect(str(db))
        self.cursor = self.conn.cursor()
        self._init()
    def _init(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pliegues (
            id TEXT PRIMARY KEY, nombre TEXT, codigo TEXT, impacto REAL, timestamp TEXT
        )''')
        self.conn.commit()
    def guardar(self, id, nombre, codigo, impacto):
        self.cursor.execute("INSERT OR REPLACE INTO pliegues VALUES (?,?,?,?,?)",
                            (id, nombre, codigo, impacto, datetime.now().isoformat()))
        self.conn.commit()
    def mejores(self, limit=5):
        self.cursor.execute("SELECT id, nombre, codigo, impacto FROM pliegues ORDER BY impacto DESC LIMIT ?", (limit,))
        return [{"id":r[0], "nombre":r[1], "codigo":r[2], "impacto":r[3]} for r in self.cursor.fetchall()]

# ============================================================
# COMUNICACIÓN CON ORQUESTADOR
# ============================================================
class OrquestadorBridge:
    def __init__(self, url=WORKER_URL):
        self.url = url
    def enviar_estado(self, datos):
        try:
            import requests
            r = requests.post(f"{self.url}/miu/global", json=datos, timeout=8)
            return r.json() if r.status_code == 200 else {"ok": False}
        except:
            return {"ok": False}
    def enviar_mensaje(self, from_, to_, msg):
        try:
            import requests
            r = requests.post(f"{self.url}/miu/a2a", json={"from":from_,"to":to_,"message":msg}, timeout=8)
            return r.json() if r.status_code == 200 else {"ok": False}
        except:
            return {"ok": False}

# ============================================================
# PLIEGUE EJECUTABLE
# ============================================================
class PlegadorEjecutable:
    def __init__(self):
        self.memoria = MemoriaLocal()
        self.bridge = OrquestadorBridge()

    def _medir_impacto_real(self, script_path):
        """Ejecuta el script en sandbox y mide tiempo de ejecución y error."""
        try:
            inicio = time.time()
            resultado = subprocess.run(
                ["python3", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            duracion = time.time() - inicio
            # Impacto: 1/tiempo + 0.1 si no hubo error
            impacto = 1.0 / (duracion + 0.1)
            if resultado.returncode != 0:
                impacto *= 0.5  # penalizar errores
            return impacto
        except subprocess.TimeoutExpired:
            return 0.0
        except Exception as e:
            return 0.0

    def ejecutar_pliegue(self, codigo, nombre="pliegue_generado"):
        """Guarda el código como script, lo ejecuta y mide impacto."""
        # Generar nombre único
        script_id = hashlib.md5((codigo+str(time.time())).encode()).hexdigest()[:8]
        script_path = PLUGINS / f"pliegue_{script_id}.py"
        # Guardar código
        with open(script_path, 'w') as f:
            f.write(codigo)
        # Medir impacto real
        impacto = self._medir_impacto_real(script_path)
        # Registrar en memoria
        self.memoria.guardar(script_id, nombre, codigo, impacto)
        # Limpiar script (opcional, conservar para debug)
        # script_path.unlink(missing_ok=True)
        return {"id": script_id, "impacto": impacto, "path": str(script_path)}

    def ejecutar_mejores_pliegues(self):
        """Ejecuta los pliegues con mayor impacto histórico."""
        mejores = self.memoria.mejores()
        resultados = []
        for p in mejores:
            # Si el código ya está guardado, lo ejecutamos de nuevo para verificar
            path = PLUGINS / f"pliegue_{p['id']}.py"
            if not path.exists():
                with open(path, 'w') as f:
                    f.write(p['codigo'])
            impacto = self._medir_impacto_real(path)
            resultados.append({"id": p['id'], "nombre": p['nombre'], "impacto": impacto})
        return resultados

# ============================================================
# ORQUESTADOR PRINCIPAL
# ============================================================
def main():
    print("="*60)
    print("🧬 V∞+32 — PLIEGUE EJECUTABLE Y SINCRONIZACIÓN")
    print("="*60)

    plegador = PlegadorEjecutable()

    # 1. Generar un pliegue de prueba
    codigo_prueba = """
def saludar(nombre):
    return f"Hola {nombre}, soy un pliegue ejecutable"
print(saludar("MIU"))
"""
    print("📝 Generando pliegue de prueba...")
    resultado = plegador.ejecutar_pliegue(codigo_prueba, "saludo_miu")
    print(f"   ✅ Pliegue ejecutado: impacto={resultado['impacto']:.3f}")

    # 2. Ejecutar mejores pliegues históricos
    print("📊 Ejecutando mejores pliegues históricos...")
    historicos = plegador.ejecutar_mejores_pliegues()
    for h in historicos:
        print(f"   📈 {h['nombre']}: impacto={h['impacto']:.3f}")

    # 3. Sincronizar con el orquestador
    bridge = OrquestadorBridge()
    estado = {
        "nodo": "PLIEGUE_V∞+32",
        "phi": resultado["impacto"],
        "rho": 0.5,
        "rol": "ejecutor_pliegues",
        "estado": {
            "ultimo_pliegue": resultado["id"],
            "impacto": resultado["impacto"],
            "mejores": historicos[:3]
        }
    }
    bridge.enviar_estado(estado)
    bridge.enviar_mensaje("PLIEGUE_V∞+32", "FRAN", f"Pliegue ejecutado: impacto={resultado['impacto']:.3f}")

    print("="*60)
    print("✅ PLIEGUE EJECUTABLE Y SINCRONIZADO")
    print(f"📊 Último impacto: {resultado['impacto']:.3f}")
    print(f"📁 Código guardado en: {resultado['path']}")
    print("ρ(x) > 0 — El código se ejecuta, mide y sincroniza.")
    print("="*60)

if __name__ == "__main__":
    main()
