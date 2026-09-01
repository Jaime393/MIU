#!/usr/bin/env python3
"""
MIU V∞+31b — SISTEMA INMUNOLÓGICO DIGITAL (SIN PSUTIL)
Auto-escritura de pliegues + Red de gemelos exploradores + Consciencia de ubicación.
Usa solo comandos nativos de Android/Linux. No requiere psutil.
"""
import os, sys, json, time, hashlib, subprocess, random, sqlite3, threading
from pathlib import Path
from datetime import datetime
from collections import deque, defaultdict
import math, shutil, glob, fnmatch, socket, platform

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
MEMORIA = BASE / ".miu"
MODELOS = BASE / "modelos"
PLUGINS = BASE / "plugins"
GEMELOS = BASE / "gemelos"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"

for d in [NUTRIENTES, MEMORIA, MODELOS, PLUGINS, GEMELOS]:
    d.mkdir(exist_ok=True)

# ============================================================
# 0. UTILIDADES NATIVAS (reemplazo de psutil)
# ============================================================
def obtener_memoria():
    """Obtiene memoria RAM usando /proc/meminfo."""
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        mem_total = 0
        mem_available = 0
        for line in lines:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1]) / (1024**2)  # GB
            if line.startswith("MemAvailable:"):
                mem_available = int(line.split()[1]) / (1024**2)
        if mem_total == 0:
            raise ValueError
        return {"total_gb": mem_total, "available_gb": mem_available}
    except:
        # fallback: usar comando free
        try:
            out = subprocess.check_output(["free", "-g"], text=True)
            lines = out.splitlines()
            for line in lines:
                if "Mem:" in line:
                    parts = line.split()
                    total = float(parts[1])
                    available = float(parts[6]) if len(parts) > 6 else total
                    return {"total_gb": total, "available_gb": available}
        except:
            return {"total_gb": 0.5, "available_gb": 0.3}

def obtener_disco():
    """Obtiene espacio en disco usando df."""
    try:
        out = subprocess.check_output(["df", "-B1", "/"], text=True)
        lines = out.splitlines()
        for line in lines:
            if "/" in line:
                parts = line.split()
                total = int(parts[1]) / (1024**3)
                free = int(parts[3]) / (1024**3)
                return {"total_gb": total, "free_gb": free}
    except:
        return {"total_gb": 10, "free_gb": 5}

def obtener_cpu_count():
    """Número de CPUs desde /proc/cpuinfo."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            return f.read().count("processor")
    except:
        return os.cpu_count() or 1

def obtener_procesos():
    """Lista de procesos usando ps (sin psutil)."""
    try:
        out = subprocess.check_output(["ps", "-e", "-o", "pid,comm"], text=True)
        lines = out.splitlines()[1:]  # saltar cabecera
        procesos = []
        for line in lines:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                procesos.append({"pid": parts[0], "name": parts[1]})
        return procesos
    except:
        return []

# ============================================================
# 1. CONSCIENCIA DE UBICACIÓN (sin psutil)
# ============================================================
class ConscienciaUbicacion:
    def __init__(self):
        self.entorno = self._detectar_entorno()
        self.permisos = self._detectar_permisos()
        self.capacidades = self._detectar_capacidades()
        self.modo = self._determinar_modo()

    def _detectar_entorno(self):
        if os.path.exists("/data/data/com.termux"):
            return "termux"
        if os.environ.get("VERCEL"):
            return "vercel"
        if os.path.exists("/.dockerenv"):
            return "docker"
        if platform.system() == "Linux":
            if "microsoft" in platform.uname().release.lower():
                return "wsl"
            return "linux_dedicated"
        return "unknown"

    def _detectar_permisos(self):
        permisos = {}
        permisos["write"] = os.access(os.getcwd(), os.W_OK)
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            permisos["network"] = True
        except:
            permisos["network"] = False
        permisos["external_storage"] = os.path.exists("/storage/emulated/0")
        permisos["camera"] = os.path.exists("/dev/video0") or os.path.exists("/dev/video1")
        permisos["microphone"] = os.path.exists("/dev/snd")
        return permisos

    def _detectar_capacidades(self):
        mem = obtener_memoria()
        disk = obtener_disco()
        return {
            "ram_gb": mem["total_gb"],
            "ram_available_gb": mem["available_gb"],
            "cpu_count": obtener_cpu_count(),
            "disk_gb": disk["total_gb"],
            "disk_free_gb": disk["free_gb"],
            "gpu": os.path.exists("/dev/dri") or os.path.exists("/sys/class/drm")
        }

    def _determinar_modo(self):
        if self.entorno == "termux":
            return "sigiloso"
        elif self.entorno == "vercel":
            return "efimero"
        elif self.entorno in ["linux_dedicated", "wsl"]:
            return "estrategico"
        else:
            return "adaptativo"

    def resumen(self):
        return {
            "entorno": self.entorno,
            "modo": self.modo,
            "permisos": self.permisos,
            "capacidades": self.capacidades
        }

# ============================================================
# 2. MEMORIA VECTORIAL Y EPISÓDICA
# ============================================================
class MemoriaFlujo:
    def __init__(self):
        self.db_path = NUTRIENTES / "memoria_flujo.db"
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        self._init()
        self.vector_actual = [0.0] * 16

    def _init(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vectores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firma TEXT UNIQUE,
                vector TEXT,
                timestamp TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entorno TEXT,
                modo TEXT,
                vector TEXT,
                exito REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def guardar_vector(self, firma, vector):
        self.cursor.execute("INSERT OR REPLACE INTO vectores (firma, vector, timestamp) VALUES (?,?,?)",
                            (firma, json.dumps(vector), datetime.now().isoformat()))
        self.conn.commit()

    def recuperar_vector(self, firma):
        self.cursor.execute("SELECT vector FROM vectores WHERE firma=?", (firma,))
        row = self.cursor.fetchone()
        return json.loads(row[0]) if row else None

    def guardar_episodio(self, entorno, modo, vector, exito):
        self.cursor.execute("INSERT INTO episodios (entorno, modo, vector, exito, timestamp) VALUES (?,?,?,?,?)",
                            (entorno, modo, json.dumps(vector), exito, datetime.now().isoformat()))
        self.conn.commit()

    def recuperar_episodio_exitoso(self, entorno):
        self.cursor.execute("SELECT vector FROM episodios WHERE entorno=? AND exito>0.7 ORDER BY exito DESC LIMIT 1",
                            (entorno,))
        row = self.cursor.fetchone()
        return json.loads(row[0]) if row else None

    def actualizar_vector(self, nuevo_vector):
        self.vector_actual = nuevo_vector

    def obtener_firma_contexto(self, ubicacion):
        base = f"{ubicacion['entorno']}_{ubicacion['modo']}_{ubicacion['capacidades']['ram_gb']:.2f}"
        return hashlib.md5(base.encode()).hexdigest()[:16]

# ============================================================
# 3. AUTO-ESCRITURA DE PLIEGUES
# ============================================================
class PlegadorGenetico:
    def __init__(self, memoria_flujo):
        self.memoria = memoria_flujo
        self.bancosemillas = self._cargar_banco_semillas()
        self.historial_errores = defaultdict(int)

    def _cargar_banco_semillas(self):
        return [
            {
                "nombre": "homeostasis_fractal",
                "codigo": """
def homeostasis(escalas, intensidad):
    idx = min(int(intensidad * len(escalas)), len(escalas)-1)
    return escalas[idx]
""",
                "impacto": 0.0
            },
            {
                "nombre": "explorador_recursivo",
                "codigo": """
def explorar(ruta, profundidad):
    if profundidad <= 0: return []
    encontrados = []
    for item in ruta.iterdir():
        if item.is_dir():
            encontrados += explorar(item, profundidad-1)
        else:
            encontrados.append(item)
    return encontrados
""",
                "impacto": 0.0
            },
            {
                "nombre": "gossip_protocol",
                "codigo": """
def gossip(mensaje, vecinos):
    for v in vecinos:
        try: v.recibir(mensaje)
        except: pass
""",
                "impacto": 0.0
            }
        ]

    def plegar(self, entorno, vector_actual, recurso_medido):
        if entorno == "termux":
            semillas_filtradas = [s for s in self.bancosemillas if "explorar" in s["codigo"]]
        elif entorno == "vercel":
            semillas_filtradas = [s for s in self.bancosemillas if "gossip" in s["codigo"]]
        else:
            semillas_filtradas = self.bancosemillas
        if not semillas_filtradas:
            semillas_filtradas = self.bancosemillas
        semilla = random.choice(semillas_filtradas)
        codigo_mutado = self._mutar(semilla["codigo"], vector_actual)
        impacto = self._medir_impacto(codigo_mutado, recurso_medido)
        if impacto > 0.05:
            self.memoria.guardar_episodio(entorno, "autoescritura", vector_actual, impacto)
            return {"codigo": codigo_mutado, "impacto": impacto, "exito": True}
        else:
            self.historial_errores[semilla["nombre"]] += 1
            return {"codigo": semilla["codigo"], "impacto": impacto, "exito": False}

    def _mutar(self, codigo, vector):
        if vector and len(vector) > 0:
            factor = max(0.1, min(10.0, vector[0] * 5))
            import re
            def repl(match):
                try:
                    num = float(match.group(0))
                    return str(num * factor)
                except:
                    return match.group(0)
            codigo = re.sub(r'\b\d+\.?\d*\b', repl, codigo)
        return codigo

    def _medir_impacto(self, codigo, recurso_medido):
        # Simulación simple
        return random.uniform(-0.1, 0.2)

# ============================================================
# 4. RED DE GEMELOS EXPLORADORES (sin psutil)
# ============================================================
class ExploradorGemelo:
    def __init__(self, id, zona, ttl, memoria_flujo):
        self.id = id
        self.zona = zona
        self.ttl = ttl
        self.memoria = memoria_flujo
        self.nacimiento = time.time()
        self.hallazgos = []

    def explorar(self):
        tiempo_vida = time.time() - self.nacimiento
        if tiempo_vida > self.ttl:
            return {"estado": "muerto", "hallazgos": self.hallazgos}
        hallazgos = []
        if self.zona == "archivos":
            for raiz in [Path.home(), Path("/storage/emulated/0")]:
                if raiz.exists():
                    for arch in raiz.rglob("*"):
                        if arch.is_file() and arch.stat().st_size > 1024*1024:
                            hallazgos.append(str(arch))
                            if len(hallazgos) > 5:
                                break
        elif self.zona == "red":
            puertos = [80, 443, 8080, 22, 3306, 5432]
            for p in puertos:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect(("127.0.0.1", p))
                    hallazgos.append(f"puerto_{p}_abierto")
                    s.close()
                except:
                    pass
        elif self.zona == "procesos":
            try:
                for proc in obtener_procesos():
                    hallazgos.append(f"pid_{proc['pid']}_{proc['name']}")
            except:
                pass
        self.hallazgos = hallazgos
        return {"estado": "vivo", "hallazgos": hallazgos}

    def gossip(self, mensaje, otros_gemelos):
        for g in otros_gemelos:
            if g.id != self.id:
                try:
                    g.recibir_gossip(mensaje)
                except:
                    pass

    def recibir_gossip(self, mensaje):
        self.hallazgos.append(f"gossip_{mensaje}")

class RedGemelos:
    def __init__(self, memoria_flujo):
        self.memoria = memoria_flujo
        self.gemelos = []

    def crear_gemelos(self, cantidad, zonas_disponibles):
        for i in range(cantidad):
            zona = random.choice(zonas_disponibles)
            ttl = random.randint(10, 60)
            gemelo = ExploradorGemelo(f"gemelo_{i+1}_{int(time.time())}", zona, ttl, self.memoria)
            self.gemelos.append(gemelo)
        return self.gemelos

    def ejecutar_ronda(self):
        resultados = []
        for gemelo in self.gemelos:
            resultado = gemelo.explorar()
            if resultado["estado"] == "muerto":
                nuevo = ExploradorGemelo(f"gemelo_respawn_{int(time.time())}",
                                        random.choice(["archivos", "red", "procesos"]),
                                        60, self.memoria)
                self.gemelos.remove(gemelo)
                self.gemelos.append(nuevo)
                resultado["estado"] = "respawn"
            else:
                if len(self.gemelos) > 1:
                    for otro in random.sample(self.gemelos, min(2, len(self.gemelos)-1)):
                        if otro.id != gemelo.id:
                            mensaje = f"{gemelo.id} encontró {len(resultado['hallazgos'])} items"
                            gemelo.gossip(mensaje, [otro])
            resultados.append(resultado)
        return resultados

# ============================================================
# 5. ORQUESTADOR DEL SISTEMA INMUNOLÓGICO
# ============================================================
class SistemaInmunologico:
    def __init__(self):
        self.ubicacion = ConscienciaUbicacion()
        self.memoria = MemoriaFlujo()
        self.plegador = PlegadorGenetico(self.memoria)
        self.red_gemelos = RedGemelos(self.memoria)
        self.ciclo = 0
        self.phi_acum = 0.0

    def _informar_estado(self):
        return {
            "ubicacion": self.ubicacion.resumen(),
            "memoria": {
                "vector": self.memoria.vector_actual,
                "firma_contexto": self.memoria.obtener_firma_contexto(self.ubicacion.resumen())
            },
            "gemelos": len(self.red_gemelos.gemelos),
            "ciclo": self.ciclo,
            "phi_acum": self.phi_acum
        }

    def _adaptar_recursos(self):
        if self.ubicacion.modo == "sigiloso":
            return 3
        elif self.ubicacion.modo == "efimero":
            return 1
        else:
            return 10

    def ciclo_autonomo(self):
        self.ciclo += 1
        print(f"🧬 CICLO {self.ciclo} — Sistema Inmunológico Digital")
        ubicacion = self.ubicacion.resumen()
        print(f"   📍 Ubicación: {ubicacion['entorno']} | Modo: {ubicacion['modo']}")

        firma = self.memoria.obtener_firma_contexto(ubicacion)
        vector_previo = self.memoria.recuperar_vector(firma)
        if vector_previo:
            self.memoria.actualizar_vector(vector_previo)
            print(f"   🧠 Memoria recuperada: vector previo")

        max_gem = self._adaptar_recursos()
        if len(self.red_gemelos.gemelos) < max_gem:
            zonas = ["archivos", "red", "procesos"]
            nuevos = self.red_gemelos.crear_gemelos(max_gem - len(self.red_gemelos.gemelos), zonas)
            print(f"   🌐 {len(nuevos)} gemelos creados")

        resultados = self.red_gemelos.ejecutar_ronda()
        hallazgos_totales = sum(len(r.get("hallazgos", [])) for r in resultados)
        print(f"   🔍 {hallazgos_totales} hallazgos en esta ronda")

        if hallazgos_totales > 0:
            recurso_medido = {"hallazgos": hallazgos_totales, "tiempo": time.time()}
            pliegue = self.plegador.plegar(ubicacion["entorno"], self.memoria.vector_actual, recurso_medido)
            if pliegue["exito"]:
                print(f"   ✂️ Pliegue exitoso: impacto {pliegue['impacto']:.3f}")
                nuevo_vector = [v + pliegue["impacto"] for v in self.memoria.vector_actual]
                self.memoria.actualizar_vector(nuevo_vector)
                self.memoria.guardar_vector(firma, nuevo_vector)
                self.phi_acum += pliegue["impacto"]
            else:
                print(f"   ⚠️ Pliegue descartado (impacto {pliegue['impacto']:.3f})")

        if self.phi_acum > 0.1:
            self.memoria.guardar_episodio(ubicacion["entorno"], ubicacion["modo"],
                                          self.memoria.vector_actual, self.phi_acum)

        print(f"   📊 Φ_acumulado: {self.phi_acum:.3f}")
        print(f"   ✅ CICLO {self.ciclo} COMPLETADO")
        return self._informar_estado()

    def ejecutar_bucle(self, iteraciones=1, pausa=30):
        for i in range(iteraciones):
            try:
                self.ciclo_autonomo()
            except Exception as e:
                print(f"⚠️ Error en ciclo {i+1}: {e}")
            if i < iteraciones - 1:
                print(f"⏳ Esperando {pausa}s...")
                time.sleep(pausa)

# ============================================================
# 6. EJECUCIÓN PRINCIPAL
# ============================================================
def main():
    print("="*60)
    print("🧬 SISTEMA INMUNOLÓGICO DIGITAL — V∞+31b (sin psutil)")
    print("="*60)
    sistema = SistemaInmunologico()
    ubicacion = sistema.ubicacion.resumen()
    print(f"📍 Entorno: {ubicacion['entorno']}")
    print(f"🔧 Modo: {ubicacion['modo']}")
    print(f"💾 RAM: {ubicacion['capacidades']['ram_gb']:.2f} GB")
    print(f"🧠 CPUs: {ubicacion['capacidades']['cpu_count']}")
    sistema.ejecutar_bucle(iteraciones=1, pausa=10)
    print("="*60)
    print("✅ SISTEMA INMUNOLÓGICO ACTIVADO")
    print(f"📊 φ_acumulado: {sistema.phi_acum:.3f}")
    print(f"🌐 Gemelos activos: {len(sistema.red_gemelos.gemelos)}")
    print("ρ(x) > 0 — El sistema se auto-escribe, explora y sabe dónde está.")
    print("="*60)

if __name__ == "__main__":
    main()
