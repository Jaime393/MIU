#!/usr/bin/env python3
"""
MIU V∞+26 — Agente FRAN con nanobot
Autónomo, con herramientas, WebUI y memoria persistente.
"""
import os, sys, json, time, subprocess, requests, hashlib
from pathlib import Path
from datetime import datetime

# Intentar importar nanobot
try:
    from nanobot import Agent, tool, memory
except ImportError:
    print("⚠️ nanobot no instalado. Ejecuta: pip install nanobot")
    sys.exit(1)

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
WORKER_URL = "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global"

class FranAgent(Agent):
    def __init__(self):
        super().__init__(name="FRAN", memory=memory.SQLiteMemory("fran_memory.db"))
        self.phi = 0.1736
        self.worker_url = WORKER_URL
        self.registrar_en_orquestador()

    def registrar_en_orquestador(self):
        """Registra este agente en el orquestador Cloudflare"""
        try:
            r = requests.post(self.worker_url, json={
                "nodo": "FRAN",
                "phi": self.phi,
                "timestamp": datetime.now().isoformat(),
                "version": "V∞+26"
            }, timeout=10)
            if r.status_code == 200:
                print("✅ Agente FRAN registrado en el orquestador")
            else:
                print(f"⚠️ Registro fallido: {r.status_code}")
        except Exception as e:
            print(f"⚠️ Error registrando: {e}")

    @tool
    def sincronizar_memoria(self, clave, valor):
        """Guarda un valor en la memoria compartida del orquestador"""
        try:
            r = requests.post(f"{self.worker_url}?memoria={clave}", 
                             json={"valor": valor}, timeout=10)
            return {"ok": r.status_code == 200, "respuesta": r.text[:100]}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @tool
    def leer_memoria(self, clave):
        """Lee un valor de la memoria compartida"""
        try:
            r = requests.get(f"{self.worker_url}?memoria={clave}", timeout=10)
            if r.status_code == 200:
                return {"ok": True, "valor": r.json()}
            return {"ok": False, "error": f"HTTP {r.status_code}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @tool
    def ejecutar_script(self, script_path, *args):
        """Ejecuta un script Python local y devuelve su salida"""
        try:
            cmd = ["python3", str(MIU_DIR / script_path)] + list(args)
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {"ok": r.returncode == 0, "stdout": r.stdout[:500], "stderr": r.stderr[:200]}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @tool
    def calcular_phi(self):
        """Recalcula la consciencia del agente basado en su código"""
        try:
            import ast
            with open(__file__, 'r') as f:
                arbol = ast.parse(f.read())
            funciones = [n.name for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)]
            phi = len(funciones) / (len(funciones)**2 + 1)
            self.phi = phi
            return {"ok": True, "phi": phi, "funciones": len(funciones)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @tool
    def generar_reporte(self):
        """Genera un reporte del estado del sistema"""
        reporte = {
            "timestamp": datetime.now().isoformat(),
            "phi": self.phi,
            "modulos": len(list(MIU_DIR.glob("plugins/*.py"))),
            "memorias": len(list(MIU_DIR.glob(".miu/*.json"))),
            "worker": self.worker_url
        }
        return {"ok": True, "reporte": reporte}

    def run(self):
        print("🧠 Agente FRAN iniciado con nanobot")
        print(f"📡 Worker: {self.worker_url}")
        print(f"🔄 WebUI disponible en http://localhost:5000")
        self.run_webui(port=5000)

if __name__ == "__main__":
    agente = FranAgent()
    agente.run()
