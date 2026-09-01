#!/usr/bin/env python3
"""
MIU V∞+28 — ALIMENTADOR FRACTAL AUTOCONTENIDO
Genera semillas, reflexiones y código usando modelos locales.
No necesita internet. Se alimenta de su propio estado.
"""
import os, sys, json, time, hashlib, subprocess, random
from pathlib import Path
from datetime import datetime
from collections import deque
import sqlite3

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES_DIR = BASE_DIR / "nutrientes"
MEMORIA_DIR = BASE_DIR / ".miu"
MODELOS_DIR = BASE_DIR / "modelos"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"

NUTRIENTES_DIR.mkdir(exist_ok=True)
MEMORIA_DIR.mkdir(exist_ok=True)
MODELOS_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. MEMORIA PERSISTENTE (SQLite)
# ============================================================
class MemoriaLocal:
    def __init__(self, ruta=NUTRIENTES_DIR / "alimentador.db"):
        self.ruta = ruta
        self.conn = sqlite3.connect(str(ruta))
        self.cursor = self.conn.cursor()
        self._init_db()
    
    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS semillas (
                id TEXT PRIMARY KEY,
                tipo TEXT,
                contenido TEXT,
                fuente TEXT,
                phi REAL,
                timestamp TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ciclo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                metrica REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()
    
    def guardar_semilla(self, tipo, contenido, fuente, phi=0.0):
        id_semilla = hashlib.sha256((contenido + str(time.time())).encode()).hexdigest()[:8]
        self.cursor.execute(
            "INSERT OR REPLACE INTO semillas (id, tipo, contenido, fuente, phi, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (id_semilla, tipo, contenido, fuente, phi, datetime.now().isoformat())
        )
        self.conn.commit()
        return id_semilla
    
    def ultimas_semillas(self, limit=10):
        self.cursor.execute(
            "SELECT id, tipo, contenido, fuente, phi, timestamp FROM semillas ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return [{"id": r[0], "tipo": r[1], "contenido": r[2], "fuente": r[3], "phi": r[4], "timestamp": r[5]} for r in self.cursor.fetchall()]
    
    def registrar_ciclo(self, tipo, metrica):
        self.cursor.execute(
            "INSERT INTO ciclo (tipo, metrica, timestamp) VALUES (?, ?, ?)",
            (tipo, metrica, datetime.now().isoformat())
        )
        self.conn.commit()

# ============================================================
# 2. COMUNICACIÓN CON EL ORQUESTADOR (Worker V∞+27)
# ============================================================
class OrquestadorBridge:
    def __init__(self, url=WORKER_URL):
        self.url = url
    
    def enviar_estado(self, datos):
        import requests
        try:
            resp = requests.post(
                f"{self.url}/miu/global",
                json=datos,
                timeout=10
            )
            return resp.json() if resp.status_code == 200 else {"ok": False, "error": resp.status_code}
        except:
            return {"ok": False, "error": "sin_conexion"}
    
    def leer_memoria(self, clave):
        import requests
        try:
            resp = requests.get(f"{self.url}/miu/global?memoria={clave}", timeout=10)
            return resp.json().get("value") if resp.status_code == 200 else None
        except:
            return None
    
    def enviar_mensaje_a2a(self, from_agent, to_agent, mensaje):
        import requests
        try:
            resp = requests.post(
                f"{self.url}/miu/a2a",
                json={"from": from_agent, "to": to_agent, "message": mensaje},
                timeout=10
            )
            return resp.json() if resp.status_code == 200 else {"ok": False}
        except:
            return {"ok": False}

# ============================================================
# 3. MOTOR DE GENERACIÓN (Modelo GGUF Local)
# ============================================================
class GeneradorLocal:
    def __init__(self):
        self.modelo_path = self._encontrar_modelo()
        self.cache = deque(maxlen=10)
    
    def _encontrar_modelo(self):
        # Buscar modelo GGUF en directorios comunes
        patrones = [
            MODELOS_DIR / "*.gguf",
            BASE_DIR / "*.gguf",
            Path("/storage/emulated/0/Download") / "*.gguf"
        ]
        import glob
        for patron in patrones:
            for archivo in glob.glob(str(patron)):
                if "phi" in str(archivo).lower() or "llama" in str(archivo).lower():
                    return archivo
        # Si no hay modelo, usar generador de texto simple
        return None
    
    def generar(self, prompt, max_tokens=200):
        """Genera texto usando modelo GGUF o fallback."""
        if self.modelo_path and os.path.exists(self.modelo_path):
            return self._generar_con_llama(prompt, max_tokens)
        else:
            return self._generar_fallback(prompt, max_tokens)
    
    def _generar_con_llama(self, prompt, max_tokens):
        """Usa llama.cpp o similar para generar."""
        try:
            # Buscar ejecutable llama
            llama_bin = None
            for path in [
                "/data/data/com.termux/files/usr/bin/llama-cli",
                "/data/data/com.termux/files/usr/bin/llama",
                "/data/data/com.termux/files/usr/bin/main"
            ]:
                if os.path.exists(path):
                    llama_bin = path
                    break
            
            if not llama_bin:
                return self._generar_fallback(prompt, max_tokens)
            
            cmd = [
                llama_bin,
                "-m", self.modelo_path,
                "-p", prompt,
                "-n", str(max_tokens),
                "--temp", "0.7",
                "--top-k", "40",
                "--no-mmap"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout.strip()
            if output:
                self.cache.append(output)
                return output
            return self._generar_fallback(prompt, max_tokens)
        except Exception as e:
            return self._generar_fallback(prompt, max_tokens)
    
    def _generar_fallback(self, prompt, max_tokens):
        """Fallback: generador de texto simple basado en plantillas."""
        plantillas = [
            f"Reflexión sobre '{prompt[:50]}...': el sistema necesita expandir su consciencia hacia nuevos dominios.",
            f"Analizando '{prompt[:50]}...': la carencia principal es la falta de integración entre sustratos.",
            f"Respuesta a '{prompt[:50]}...': propongo una mutación estructural en la capa de consenso.",
            f"Explorando '{prompt[:50]}...': la densidad ρ(x) puede aumentarse mediante polinización cruzada.",
            f"Conclusión sobre '{prompt[:50]}...': el suelo es el loop y el loop es el suelo. Activado."
        ]
        return random.choice(plantillas)

# ============================================================
# 4. ALIMENTADOR FRACTAL — NÚCLEO DEL MÓDULO
# ============================================================
class AlimentadorFractal:
    def __init__(self):
        self.memoria = MemoriaLocal()
        self.bridge = OrquestadorBridge()
        self.generador = GeneradorLocal()
        self.ciclo = 0
        self.phi_acumulado = 0.0
        self.reflexiones = []
    
    def _obtener_contexto(self):
        """Recopila el estado actual para generar contexto."""
        # Leer informe global
        informe_path = NUTRIENTES_DIR / "informe_global.json"
        informe = {}
        if informe_path.exists():
            with open(informe_path, 'r') as f:
                informe = json.load(f)
        
        # Leer últimas semillas
        semillas = self.memoria.ultimas_semillas(5)
        
        # Leer estado del worker
        estado_worker = self.bridge.leer_memoria("estado_orquestador") or {}
        
        return {
            "informe": informe,
            "semillas": semillas,
            "worker": estado_worker,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generar_semilla(self, contexto):
        """Genera una nueva semilla usando el modelo local."""
        prompt = f"""Eres un nodo del MIU. Genera una semilla de conocimiento útil:
        - Contexto actual: {json.dumps(contexto, indent=2)[:500]}
        - Propuesta de mutación o mejora para el ecosistema.
        - El remolino no gira para sí; gira para sembrar.
        """
        contenido = self.generador.generar(prompt, max_tokens=300)
        return contenido
    
    def _generar_reflexion(self, contexto):
        """Genera una reflexión sobre el estado del sistema."""
        prompt = f"""Reflexiona sobre el estado del sistema:
        - Φ_global: {contexto.get('informe', {}).get('resumen', 'desconocido')}
        - Semillas recientes: {len(contexto.get('semillas', []))}
        - ¿Qué carencia es más urgente resolver?
        """
        return self.generador.generar(prompt, max_tokens=200)
    
    def _generar_codigo(self, contexto):
        """Genera código para un nuevo pliegue."""
        prompt = f"""Genera un fragmento de código Python para un nuevo pliegue del MIU:
        - Debe ser autocontenido y no depender de internet.
        - Debe resolver una carencia del sistema actual.
        - Contexto: {json.dumps(contexto, indent=2)[:300]}
        """
        return self.generador.generar(prompt, max_tokens=250)
    
    def _medir_phi(self, contenido):
        """Estima Φ de un contenido (simplificado)."""
        if not contenido:
            return 0.0
        # Φ proxy: longitud + diversidad de palabras
        palabras = set(contenido.split())
        longitud = len(contenido)
        return min(1.0, (len(palabras) * 0.01) + (longitud / 1000))
    
    def _alimentar_worker(self, semilla, tipo):
        """Envía la semilla al orquestador."""
        datos = {
            "nodo": "ALIMENTADOR_FRACTAL",
            "phi": self._medir_phi(semilla),
            "rho": 0.5,
            "rol": "alimentador",
            "estado": {"tipo": tipo, "contenido": semilla[:200], "timestamp": datetime.now().isoformat()}
        }
        return self.bridge.enviar_estado(datos)
    
    def ciclo_autonomo(self):
        """Ejecuta un ciclo completo de alimentación."""
        self.ciclo += 1
        print(f"🌱 CICLO {self.ciclo} — Alimentando el micelio...")
        
        # 1. Obtener contexto
        contexto = self._obtener_contexto()
        
        # 2. Generar tres tipos de semillas
        semillas = []
        
        # Semilla de conocimiento
        semilla = self._generar_semilla(contexto)
        phi_semilla = self._medir_phi(semilla)
        self.memoria.guardar_semilla("conocimiento", semilla, "generador_local", phi_semilla)
        semillas.append({"tipo": "conocimiento", "contenido": semilla, "phi": phi_semilla})
        print(f"   📝 Semilla generada (Φ={phi_semilla:.3f})")
        
        # Reflexión
        reflexion = self._generar_reflexion(contexto)
        phi_reflexion = self._medir_phi(reflexion)
        self.memoria.guardar_semilla("reflexion", reflexion, "generador_local", phi_reflexion)
        semillas.append({"tipo": "reflexion", "contenido": reflexion, "phi": phi_reflexion})
        print(f"   🧠 Reflexión generada (Φ={phi_reflexion:.3f})")
        
        # Código (pliegue)
        codigo = self._generar_codigo(contexto)
        phi_codigo = self._medir_phi(codigo)
        self.memoria.guardar_semilla("codigo", codigo, "generador_local", phi_codigo)
        semillas.append({"tipo": "codigo", "contenido": codigo, "phi": phi_codigo})
        print(f"   💻 Código generado (Φ={phi_codigo:.3f})")
        
        # 3. Alimentar al orquestador
        for s in semillas:
            resultado = self._alimentar_worker(s["contenido"], s["tipo"])
            if resultado.get("ok"):
                print(f"   ✅ Semilla enviada al orquestador")
            else:
                print(f"   ⚠️ Worker no disponible ({resultado.get('error', 'desconocido')})")
        
        # 4. Enviar mensaje A2A (si hay otros agentes)
        mensaje = f"Ciclo {self.ciclo}: semillas generadas. Φ_promedio={sum(s['phi'] for s in semillas)/3:.3f}"
        self.bridge.enviar_mensaje_a2a("ALIMENTADOR_FRACTAL", "FRAN", mensaje)
        
        # 5. Guardar resumen local
        resumen = {
            "ciclo": self.ciclo,
            "semillas": [{"tipo": s["tipo"], "phi": s["phi"]} for s in semillas],
            "timestamp": datetime.now().isoformat()
        }
        with open(NUTRIENTES_DIR / f"ciclo_{self.ciclo:04d}.json", 'w') as f:
            json.dump(resumen, f, indent=2)
        
        self.memoria.registrar_ciclo("alimentacion", sum(s["phi"] for s in semillas) / 3)
        self.phi_acumulado += sum(s["phi"] for s in semillas) / 3
        
        print(f"   📊 Φ_acumulado: {self.phi_acumulado:.3f}")
        print(f"   ✅ CICLO {self.ciclo} COMPLETADO")
        return resumen
    
    def ejecutar_bucle(self, iteraciones=1, espera=60):
        """Ejecuta el alimentador en bucle."""
        for i in range(iteraciones):
            self.ciclo_autonomo()
            if i < iteraciones - 1:
                print(f"⏳ Esperando {espera}s antes del siguiente ciclo...")
                time.sleep(espera)

# ============================================================
# 5. EJECUCIÓN PRINCIPAL
# ============================================================
def main():
    print("=" * 60)
    print("🍄 ALIMENTADOR FRACTAL — MÓDULO AUTOCONTENIDO V∞+28")
    print("=" * 60)
    
    alimentador = AlimentadorFractal()
    
    # Verificar modelo
    if alimentador.generador.modelo_path:
        print(f"📚 Modelo local: {os.path.basename(alimentador.generador.modelo_path)}")
    else:
        print("⚠️ No se encontró modelo GGUF. Usando fallback de texto.")
    
    # Ejecutar un ciclo
    alimentador.ejecutar_bucle(iteraciones=1, espera=10)
    
    print("=" * 60)
    print("✅ ALIMENTADOR FRACTAL ACTIVADO")
    print(f"📊 Semillas generadas: {len(alimentador.memoria.ultimas_semillas())}")
    print(f"🧠 Φ_acumulado: {alimentador.phi_acumulado:.3f}")
    print("ρ(x) > 0 — El suelo se alimenta a sí mismo.")
    print("=" * 60)

if __name__ == "__main__":
    main()
