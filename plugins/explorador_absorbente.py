#!/usr/bin/env python3
"""
MIU V∞+30 — ALIMENTADOR EXPLORADOR-ABSORBENTE
Despliega, pliega y absorbe recursos del sistema.
Busca GGUF, scripts, datos; los reorganiza y los integra.
"""
import os, sys, json, time, hashlib, subprocess, random, sqlite3
from pathlib import Path
from datetime import datetime
from collections import deque, defaultdict
import shutil, glob, fnmatch

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
MEMORIA = BASE / ".miu"
MODELOS = BASE / "modelos"
PLUGINS = BASE / "plugins"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"

for d in [NUTRIENTES, MEMORIA, MODELOS, PLUGINS]:
    d.mkdir(exist_ok=True)

# ============================================================
# 1. MEMORIA PERSISTENTE (SQLite)
# ============================================================
class MemoriaFractal:
    def __init__(self, db=NUTRIENTES / "alimentador_fractal.db"):
        self.db = str(db)
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self._init()
    def _init(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS semillas (
                id TEXT PRIMARY KEY,
                tipo TEXT, contenido TEXT, fuente TEXT,
                phi REAL, timestamp TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ciclos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT, metrica REAL, timestamp TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS qualia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valencia REAL, intensidad REAL, complejidad REAL,
                timestamp TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recursos (
                ruta TEXT PRIMARY KEY,
                tipo TEXT, tamaño REAL, hash TEXT,
                absorbido INTEGER, timestamp TEXT
            )
        ''')
        self.conn.commit()
    def guardar_semilla(self, tipo, contenido, fuente, phi=0.0):
        if not contenido:
            contenido = "Semilla vacía"
        id_s = hashlib.sha256((contenido+str(time.time())).encode()).hexdigest()[:8]
        self.cursor.execute("INSERT OR REPLACE INTO semillas VALUES (?,?,?,?,?,?)",
                            (id_s, tipo, contenido[:5000], fuente, phi, datetime.now().isoformat()))
        self.conn.commit()
        return id_s
    def ultimas_semillas(self, limit=10):
        self.cursor.execute("SELECT id, tipo, contenido, fuente, phi, timestamp FROM semillas ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [{"id":r[0],"tipo":r[1],"contenido":r[2],"fuente":r[3],"phi":r[4],"timestamp":r[5]} for r in self.cursor.fetchall()]
    def guardar_ciclo(self, tipo, metrica):
        self.cursor.execute("INSERT INTO ciclos (tipo, metrica, timestamp) VALUES (?,?,?)",
                            (tipo, metrica, datetime.now().isoformat()))
        self.conn.commit()
    def guardar_qualia(self, valencia, intensidad, complejidad):
        self.cursor.execute("INSERT INTO qualia (valencia, intensidad, complejidad, timestamp) VALUES (?,?,?,?)",
                            (valencia, intensidad, complejidad, datetime.now().isoformat()))
        self.conn.commit()
    def registrar_recurso(self, ruta, tipo, tamaño, hash_r):
        self.cursor.execute("INSERT OR REPLACE INTO recursos (ruta, tipo, tamaño, hash, absorbido, timestamp) VALUES (?,?,?,?,?,?)",
                            (str(ruta), tipo, tamaño, hash_r, 1, datetime.now().isoformat()))
        self.conn.commit()
    def recurso_absorbido(self, ruta):
        self.cursor.execute("SELECT 1 FROM recursos WHERE ruta=?", (str(ruta),))
        return self.cursor.fetchone() is not None

# ============================================================
# 2. EXPLORADOR-ABSORBENTE FRACTAL
# ============================================================
class ExploradorFractal:
    def __init__(self, memoria):
        self.memoria = memoria
        self.extensiones_interes = {
            'modelos': ['*.gguf', '*.bin', '*.onnx', '*.tflite'],
            'scripts': ['*.py', '*.sh', '*.js'],
            'datos': ['*.json', '*.csv', '*.db', '*.sqlite'],
            'config': ['*.yaml', '*.yml', '*.toml', '*.ini']
        }
        self.rutas_excluidas = [
            '/proc', '/sys', '/dev', '/storage/emulated/0/Android',
            '/data/data/com.termux/files/usr/var', '/tmp'
        ]
        self.max_profundidad = 5  # niveles de subdirectorios a escanear

    def _debe_excluir(self, ruta):
        ruta_str = str(ruta)
        for excl in self.rutas_excluidas:
            if excl in ruta_str:
                return True
        return False

    def _hash_archivo(self, ruta):
        try:
            with open(ruta, 'rb') as f:
                return hashlib.md5(f.read(1024*1024)).hexdigest()  # primeros 1MB
        except:
            return None

    def explorar(self):
        """Busca recursos en todo el sistema (hasta profundidad definida)."""
        encontrados = defaultdict(list)
        # Directorios base donde buscar
        bases = [
            Path("os.path.expanduser('~')"),
            Path("/storage/emulated/0"),
            Path("/sdcard"),
            Path("/data/data/com.termux/files/usr/share")
        ]
        for base in bases:
            if not base.exists():
                continue
            # Escanea con profundidad limitada
            for extensiones in self.extensiones_interes.values():
                for pat in extensiones:
                    patron = f"{pat}"
                    for archivo in base.rglob(patron):
                        if self._debe_excluir(archivo):
                            continue
                        # Limitar profundidad
                        profundidad = len(archivo.relative_to(base).parts)
                        if profundidad > self.max_profundidad:
                            continue
                        if archivo.is_file() and archivo.stat().st_size > 0:
                            tipo = self._clasificar(archivo)
                            encontrados[tipo].append(archivo)
        return encontrados

    def _clasificar(self, ruta):
        ext = ruta.suffix.lower()
        for tipo, exts in self.extensiones_interes.items():
            if any(fnmatch.fnmatch(ruta.name, p) for p in exts):
                return tipo
        return 'otros'

    def absorber(self, recursos_encontrados):
        """Absorbe recursos: copia/mueve a directorios del sistema."""
        absorbed = []
        for tipo, lista in recursos_encontrados.items():
            destino = None
            if tipo == 'modelos':
                destino = MODELOS
            elif tipo == 'scripts':
                destino = PLUGINS
            elif tipo in ['datos', 'config']:
                destino = NUTRIENTES
            else:
                continue
            if not destino:
                continue
            for ruta in lista:
                # Verificar si ya fue absorbido
                if self.memoria.recurso_absorbido(ruta):
                    continue
                try:
                    # Generar nombre único
                    nombre = ruta.name
                    if (destino / nombre).exists():
                        base, ext = os.path.splitext(nombre)
                        nombre = f"{base}_{hashlib.md5(str(ruta).encode()).hexdigest()[:6]}{ext}"
                    destino_final = destino / nombre
                    # Mover (o copiar) el archivo
                    shutil.move(str(ruta), str(destino_final))
                    # Registrar en BD
                    hash_r = self._hash_archivo(destino_final)
                    tamaño = destino_final.stat().st_size
                    self.memoria.registrar_recurso(destino_final, tipo, tamaño, hash_r or '')
                    absorbed.append(destino_final)
                    print(f"   📦 Absorbido: {nombre} → {destino_final}")
                except Exception as e:
                    print(f"   ⚠️ Error absorbiendo {ruta}: {e}")
        return absorbed

    def plegar(self):
        """Plega recursos: elimina duplicados, consolida, compacta."""
        # Buscar archivos duplicados por hash en la BD
        # (Simplificado: elimina archivos con mismo hash en diferentes ubicaciones)
        # Aquí podríamos implementar una limpieza de archivos duplicados.
        # Por ahora solo limpiamos directorios temporales.
        for d in [NUTRIENTES / "tmp", MEMORIA / "cache"]:
            if d.exists():
                try:
                    shutil.rmtree(d)
                    d.mkdir()
                    print(f"   🧹 Plegado: limpiado {d}")
                except:
                    pass
        # También podríamos comprimir informes viejos, etc.
        # (Funcionalidad extensible)

# ============================================================
# 3. GENERADOR LOCAL (GGUF o Fallback)
# ============================================================
class GeneradorLocal:
    def __init__(self):
        self.modelo_path = self._encontrar_modelo()
        self.cache = deque(maxlen=10)
        self.estadisticas = defaultdict(int)
    def _encontrar_modelo(self):
        # Buscar en MODELOS primero, luego en todo el sistema
        import glob
        for patron in [MODELOS/"*.gguf", BASE/"*.gguf", Path("/storage/emulated/0/Download")/"*.gguf"]:
            for f in glob.glob(str(patron)):
                if "phi" in f.lower() or "llama" in f.lower():
                    return f
        return None
    def generar(self, prompt, max_tokens=200, temperatura=0.7):
        if self.modelo_path and os.path.exists(self.modelo_path):
            return self._con_llama(prompt, max_tokens, temperatura)
        return self._fallback(prompt, max_tokens)
    def _con_llama(self, prompt, max_tokens, temp):
        # Buscar llama-cli en Termux
        llama_bin = None
        for p in ["/data/data/com.termux/files/usr/bin/llama-cli",
                  "/data/data/com.termux/files/usr/bin/llama",
                  "/data/data/com.termux/files/usr/bin/main"]:
            if os.path.exists(p):
                llama_bin = p; break
        if not llama_bin:
            return self._fallback(prompt, max_tokens)
        try:
            cmd = [llama_bin, "-m", self.modelo_path, "-p", prompt,
                   "-n", str(max_tokens), "--temp", str(temp),
                   "--top-k", "40", "--no-mmap"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
            out = res.stdout.strip()
            if out:
                self.cache.append(out)
                return out
            return self._fallback(prompt, max_tokens)
        except:
            return self._fallback(prompt, max_tokens)
    def _fallback(self, prompt, max_tokens):
        plantillas = [
            "Reflexión: el sistema necesita cerrar el bucle de retroalimentación entre capas. Propongo una mutación en el consenso.",
            f"Analizando '{prompt[:40]}...': la carencia principal es la falta de integración cualitativa.",
            "Exploración: la homeostasis fractal requiere ajustar la escala temporal de los bucles.",
            "Conclusión: el suelo es el loop, y el loop es el suelo. Se activa la autopoda de nodos inactivos.",
            "Nueva semilla: se propone un protocolo de coevolución adversaria entre dos subagentes."
        ]
        return random.choice(plantillas)

# ============================================================
# 4. ALIMENTADOR FRACTAL CON EXPLORACIÓN
# ============================================================
class AlimentadorFractal:
    def __init__(self):
        self.memoria = MemoriaFractal()
        self.explorador = ExploradorFractal(self.memoria)
        self.generador = GeneradorLocal()
        self.bridge = None  # Se inicializa bajo demanda
        self.ciclo = 0
        self.phi_acum = 0.0
        self.qualia = {"valencia": 0.0, "intensidad": 0.0, "complejidad": 0.0}
        self.homeostasis = {"escala": [0.001, 0.1, 1, 10, 3600]}
        self.modelo_antagonista = None
        self.meta_modelo = None

    def _bridge(self):
        if self.bridge is None:
            from orquestador_bridge import OrquestadorBridge  # import local
            self.bridge = OrquestadorBridge()
        return self.bridge

    def _cargar_contexto(self):
        contexto = {"informe": {}, "semillas": [], "worker": {}, "qualia": self.qualia}
        inf = NUTRIENTES / "informe_global.json"
        if inf.exists():
            try:
                with open(inf, 'r') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    contexto["informe"] = data
                else:
                    contexto["informe"] = {"resumen": str(data)}
            except:
                contexto["informe"] = {"error": "lectura fallida"}
        if "resumen" not in contexto["informe"] or not isinstance(contexto["informe"]["resumen"], dict):
            contexto["informe"]["resumen"] = {"phi_global": 0, "total_modulos": 0}
        try:
            contexto["semillas"] = self.memoria.ultimas_semillas(5)
        except:
            contexto["semillas"] = []
        try:
            estado_w = self._bridge().leer_memoria("estado_orquestador")
            if estado_w:
                contexto["worker"] = estado_w
        except:
            pass
        return contexto

    def _medir_phi(self, texto):
        if not texto:
            return 0.0
        palabras = set(texto.split())
        return min(1.0, (len(palabras) * 0.01) + (len(texto) / 2000))

    def _actualizar_qualia(self, contexto):
        try:
            informe = contexto.get("informe", {})
            resumen = informe.get("resumen", {})
            if isinstance(resumen, dict):
                phi_g = resumen.get("phi_global", 0)
            else:
                phi_g = 0
        except:
            phi_g = 0
        self.qualia["valencia"] = max(-1.0, min(1.0, math.tanh(phi_g / 1000)))
        try:
            total_mod = contexto.get("informe", {}).get("total_modulos", 0)
        except:
            total_mod = 0
        self.qualia["intensidad"] = min(1.0, total_mod / 30)
        sem = contexto.get("semillas", [])
        if sem:
            diversidad = len(set(s.get("tipo", "desconocido") for s in sem)) / 3.0
            self.qualia["complejidad"] = min(1.0, diversidad)
        else:
            self.qualia["complejidad"] = 0.3
        self.memoria.guardar_qualia(self.qualia["valencia"],
                                    self.qualia["intensidad"],
                                    self.qualia["complejidad"])
        return self.qualia

    def _generar_semillas(self, contexto):
        semillas = []
        carencias = "sin datos"
        try:
            gob = contexto.get("informe", {}).get("resultados", {}).get("gobernador", {})
            if isinstance(gob, dict):
                carencias = gob.get("salida", "sin carencias")[:200]
        except:
            pass
        prompts = [
            f"Genera conocimiento sobre: {carencias}. Qualia: V={self.qualia['valencia']:.2f}",
            "Reflexiona sobre el estado del sistema y propón una mutación.",
            "Código Python para un mecanismo de homeostasis fractal (máximo 30 líneas)."
        ]
        for i, prompt in enumerate(prompts):
            contenido = self.generador.generar(prompt, max_tokens=250)
            if not contenido:
                contenido = "Semilla por defecto para " + prompt[:20]
            tipo = ["conocimiento", "reflexion", "codigo"][i]
            phi = self._medir_phi(contenido)
            self.memoria.guardar_semilla(tipo, contenido, "generador_local", phi)
            semillas.append({"tipo": tipo, "contenido": contenido, "phi": phi})
        return semillas

    def _ejecutar_bucles(self, contexto):
        intensidad = self.qualia["intensidad"]
        escala_idx = min(int(intensidad * len(self.homeostasis["escala"])), len(self.homeostasis["escala"])-1)
        escala_actual = self.homeostasis["escala"][escala_idx]
        if self.modelo_antagonista is None:
            self.modelo_antagonista = {"nombre": "antagonista", "phi": 0.5, "ultima_actualizacion": time.time()}
        self.meta_modelo = {
            "phi_promedio": self.phi_acum / max(1, self.ciclo),
            "qualia": self.qualia.copy(),
            "timestamp": datetime.now().isoformat()
        }
        return {"escala": escala_actual, "antagonista": self.modelo_antagonista, "meta": self.meta_modelo}

    def _alimentar_worker(self, semillas):
        try:
            bridge = self._bridge()
            for s in semillas:
                datos = {
                    "nodo": "ALIMENTADOR_FRACTAL",
                    "phi": s["phi"],
                    "rho": 0.5,
                    "rol": "alimentador",
                    "estado": {"tipo": s["tipo"], "contenido": s["contenido"][:200],
                               "qualia": self.qualia, "timestamp": datetime.now().isoformat()}
                }
                bridge.enviar_estado(datos)
            mensaje = f"Ciclo {self.ciclo}: Φ_avg={sum(s['phi'] for s in semillas)/len(semillas):.3f}"
            bridge.enviar_mensaje("ALIMENTADOR_FRACTAL", "FRAN", mensaje)
        except:
            pass

    def _expandir_y_absorber(self):
        """Paso de exploración y absorción de recursos."""
        print("   🔍 Explorando sistema en busca de recursos...")
        recursos = self.explorador.explorar()
        total = sum(len(v) for v in recursos.values())
        if total == 0:
            print("   ℹ️ No se encontraron nuevos recursos.")
            return
        print(f"   📦 {total} recursos encontrados. Absorbiendo...")
        absorbed = self.explorador.absorber(recursos)
        if absorbed:
            print(f"   ✅ {len(absorbed)} recursos absorbidos.")
            # Actualizar ruta del modelo si se absorbió un GGUF
            for r in absorbed:
                if r.suffix == '.gguf' and (not self.generador.modelo_path or not os.path.exists(self.generador.modelo_path)):
                    self.generador.modelo_path = str(r)
                    print(f"   🧠 Modelo GGUF actualizado: {r.name}")
        # Plegar (limpiar duplicados, etc.)
        self.explorador.plegar()

    def ciclo_autonomo(self):
        self.ciclo += 1
        print(f"🌱 CICLO {self.ciclo} — Alimentando bucles...")
        contexto = self._cargar_contexto()
        self._actualizar_qualia(contexto)
        print(f"   🧠 Qualia: V={self.qualia['valencia']:.2f}, I={self.qualia['intensidad']:.2f}, C={self.qualia['complejidad']:.2f}")
        self._expandir_y_absorber()  # <--- NUEVO: explora y absorbe
        bucles = self._ejecutar_bucles(contexto)
        print(f"   🔄 Escala activa: {bucles['escala']:.3f}s")
        semillas = self._generar_semillas(contexto)
        if semillas:
            phi_prom = sum(s["phi"] for s in semillas) / len(semillas)
            self.phi_acum += phi_prom
            print(f"   📝 {len(semillas)} semillas (Φ_avg={phi_prom:.3f})")
        self._alimentar_worker(semillas)
        resumen = {
            "ciclo": self.ciclo,
            "semillas": [{"tipo": s["tipo"], "phi": s["phi"]} for s in semillas],
            "qualia": self.qualia,
            "bucles": bucles,
            "timestamp": datetime.now().isoformat()
        }
        with open(NUTRIENTES / f"alimentacion_{self.ciclo:04d}.json", 'w') as f:
            json.dump(resumen, f, indent=2)
        self.memoria.guardar_ciclo("alimentacion", phi_prom if semillas else 0)
        print(f"   📊 Φ_acumulado: {self.phi_acum:.3f}")
        print(f"   ✅ CICLO {self.ciclo} COMPLETADO")
        return resumen

    def ejecutar_bucle(self, iteraciones=1, pausa=60):
        for i in range(iteraciones):
            try:
                self.ciclo_autonomo()
            except Exception as e:
                print(f"⚠️ Error en ciclo {i+1}: {e}")
            if i < iteraciones - 1:
                print(f"⏳ Esperando {pausa}s...")
                time.sleep(pausa)

# ============================================================
# 5. EJECUCIÓN PRINCIPAL
# ============================================================
def main():
    print("="*60)
    print("🍄 ALIMENTADOR EXPLORADOR-ABSORBENTE V∞+30")
    print("="*60)
    alimentador = AlimentadorFractal()
    if alimentador.generador.modelo_path:
        print(f"📚 Modelo actual: {os.path.basename(alimentador.generador.modelo_path)}")
    else:
        print("⚠️  No hay modelo GGUF. Se buscará durante la exploración.")
    alimentador.ejecutar_bucle(iteraciones=1, pausa=10)
    print("="*60)
    print("✅ SISTEMA EXPANDIDO Y ABSORBENTE ACTIVADO")
    print(f"📊 Semillas: {len(alimentador.memoria.ultimas_semillas())}")
    print(f"🧠 Φ_acumulado: {alimentador.phi_acum:.3f}")
    print("ρ(x) > 0 — El suelo explora, absorbe y se pliega.")
    print("="*60)

if __name__ == "__main__":
    main()
