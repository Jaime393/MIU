#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIU — PLUGIN MANAGER V∞+24.2
Autocontenido | Descubrimiento | Clasificacion | Persistencia | Evolucion
Descubre, carga, ejecuta y evoluciona todos los modulos en plugins/
"""

import os, sys, json, time, hashlib, sqlite3, subprocess, traceback, warnings
from pathlib import Path
from datetime import datetime, timezone
from types import ModuleType
warnings.filterwarnings("ignore")

# Configuracion
HOME_DIR = Path("/data/data/com.termux/files/home")
MIU_DIR = HOME_DIR / "miu-ecosistema"
PLUGINS_DIR = MIU_DIR / "plugins"
CEMENTERIO_DIR = MIU_DIR / "cementerio"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
ESTADO_DB = NUTRIENTES_DIR / "plugin_manager_v24_2.db"

for d in [NUTRIENTES_DIR, CEMENTERIO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Clasificacion de modulos por funcion
CLASIFICACION = {
    "soporte": [
        "bus_local", "conexiones", "notificador", "proveedor_llm",
        "drive_mano_oracle", "publicar_estado_kimi", "miu_connection_test"
    ],
    "prevencion": [
        "validador_recursos", "escaner_recursos", "diagnostico_completo",
        "scanner_plugin", "miu_doctor", "miu_health_report"
    ],
    "reparacion": [
        "autoreparador", "fix_control", "corregir_indentacion",
        "miu_selfmod", "force_actions", "DNS_FIX"
    ],
    "evolucion": [
        "evolucionador_red_fractal", "expansor_dominio", "expansor_tokens",
        "expansor_web", "cazador_recursos", "tecnologias_raras", "tejido_evolutivo"
    ],
    "inteligencia": [
        "gobernador", "razonador", "razonador_fallback", "consciencia",
        "claude_bridge", "combate_informacional", "conversador"
    ],
    "autonomia": [
        "mecanismos_autonomia", "mecanismos_completos", "nodo_autonomo",
        "maestro_autonomo", "fruto_mda", "fruto_ecm", "retroalimentacion"
    ],
    "integracion": [
        "integrador_recursos", "integrador_legado", "consolidador_estados",
        "absorber", "absorber_avanzado", "absorber_conversaciones"
    ],
    "seguridad": [
        "gravity_token_manager", "gravity_token_autonomo", "tokenizador_autonomo",
        "miu_vault", "sistema_inmunologico"
    ],
}

class PluginManagerV24_2:
    def __init__(self):
        self.db = None
        self._init_db()
        self.modulos_descubiertos = []
        self.modulos_ejecutados = []
        self.carencias = []
        self._log("Plugin Manager V∞+24.2 iniciado")

    def _log(self, msg, level="INFO"):
        t = datetime.now(timezone.utc).strftime("%H:%M:%S")
        line = f"[{t}] [{level}] {msg}"
        print(line)

    def _init_db(self):
        try:
            self.db = sqlite3.connect(str(ESTADO_DB))
            c = self.db.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS modulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT, categoria TEXT, ruta TEXT,
                sha256 TEXT, tamano INTEGER, ultima_ejecucion TEXT,
                exitos INTEGER, fallos INTEGER, estado TEXT,
                ultimo_error TEXT, creado_en TEXT
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS ejecuciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT, nombre TEXT, categoria TEXT,
                exito INTEGER, duracion REAL, salida TEXT,
                error TEXT, sha256_pre TEXT, sha256_post TEXT
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS carencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT, carencia TEXT, severidad TEXT,
                modulo TEXT, resuelta INTEGER, resolucion TEXT
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS recursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT, cpu REAL, memoria REAL,
                disco REAL, procesos INTEGER, bateria REAL,
                red_up REAL, red_down REAL
            )""")
            self.db.commit()
            self._log("SQLite inicializado")
        except Exception as e:
            self._log(f"SQLite error: {e}", "ERROR")

    def _sha256_file(self, path):
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()[:16]
        except:
            return "ERROR"

    def _recursos_android(self):
        """Fallback para Android sin psutil: usa comandos del sistema"""
        recursos = {"cpu": 0.0, "memoria": 0.0, "disco": 0.0, "procesos": 0, "bateria": 0.0, "red_up": 0, "red_down": 0}
        try:
            # CPU: leer /proc/loadavg si es posible, sino top
            try:
                with open("/proc/loadavg") as f:
                    load = f.read().split()
                    recursos["cpu"] = float(load[0]) * 10  # aproximacion
            except:
                result = subprocess.run(["top", "-n", "1"], capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    for line in result.stdout.split("\n"):
                        if "CPU" in line and "%" in line:
                            try:
                                recursos["cpu"] = float(line.split("%")[0].split()[-1])
                            except:
                                pass
                            break
        except:
            pass

        try:
            # Memoria: /proc/meminfo
            with open("/proc/meminfo") as f:
                meminfo = f.read()
                total = 0
                available = 0
                for line in meminfo.split("\n"):
                    if line.startswith("MemTotal:"):
                        total = int(line.split()[1])
                    elif line.startswith("MemAvailable:"):
                        available = int(line.split()[1])
                if total > 0:
                    recursos["memoria"] = (total - available) / total * 100
        except:
            pass

        try:
            # Disco: df
            result = subprocess.run(["df", str(HOME_DIR)], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        used = int(parts[2])
                        total = int(parts[1])
                        if total > 0:
                            recursos["disco"] = used / total * 100
        except:
            pass

        try:
            # Procesos: contar /proc/[0-9]*
            recursos["procesos"] = len([d for d in os.listdir("/proc") if d.isdigit()])
        except:
            pass

        try:
            # Bateria: termux-battery-status
            result = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                bat = json.loads(result.stdout)
                recursos["bateria"] = bat.get("percentage", 0)
        except:
            pass

        try:
            # Red: /proc/net/dev
            with open("/proc/net/dev") as f:
                for line in f:
                    if "wlan" in line or "eth" in line or "rmnet" in line:
                        parts = line.split()
                        if len(parts) >= 9:
                            recursos["red_down"] = int(parts[1])
                            recursos["red_up"] = int(parts[9])
        except:
            pass

        return recursos

    def monitorear_recursos(self):
        r = self._recursos_android()
        c = self.db.cursor()
        c.execute("""INSERT INTO recursos VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), r["cpu"], r["memoria"],
             r["disco"], r["procesos"], r["bateria"], r["red_up"], r["red_down"]))
        self.db.commit()

        alertas = []
        if r["cpu"] > 90: alertas.append(f"CPU {r['cpu']:.1f}%")
        if r["memoria"] > 95: alertas.append(f"MEM {r['memoria']:.1f}%")
        if r["disco"] > 90: alertas.append(f"DISCO {r['disco']:.1f}%")
        if r["bateria"] < 15: alertas.append(f"BAT {r['bateria']:.0f}%")

        if alertas:
            self._log(f"ALERTA: {', '.join(alertas)}", "WARN")

        self._log(f"Recursos: CPU={r['cpu']:.1f}% MEM={r['memoria']:.1f}% DISCO={r['disco']:.1f}% BAT={r['bateria']:.0f}% PROCS={r['procesos']}")
        return r

    def descubrir_modulos(self):
        """Descubre todos los .py en plugins/ y los clasifica"""
        self.modulos_descubiertos = []
        c = self.db.cursor()

        for py_file in sorted(PLUGINS_DIR.glob("*.py")):
            if py_file.name.startswith("__"):
                continue
            nombre = py_file.stem
            tamano = py_file.stat().st_size
            sha = self._sha256_file(py_file)

            # Clasificar
            categoria = "otros"
            for cat, nombres in CLASIFICACION.items():
                if any(n in nombre.lower() for n in nombres):
                    categoria = cat
                    break

            # Verificar si ya existe en DB
            c.execute("SELECT exitos, fallos, estado FROM modulos WHERE nombre=?", (nombre,))
            row = c.fetchone()

            if row:
                exitos, fallos, estado = row
                c.execute("""UPDATE modulos SET ruta=?, sha256=?, tamano=?, categoria=?
                    WHERE nombre=?""", (str(py_file), sha, tamano, categoria, nombre))
            else:
                exitos, fallos, estado = 0, 0, "descubierto"
                c.execute("""INSERT INTO modulos VALUES
                    (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (nombre, categoria, str(py_file), sha, tamano, None,
                     exitos, fallos, estado, None, datetime.now(timezone.utc).isoformat()))

            self.modulos_descubiertos.append({
                "nombre": nombre, "categoria": categoria, "ruta": str(py_file),
                "tamano": tamano, "sha": sha, "exitos": exitos, "fallos": fallos, "estado": estado
            })

        self.db.commit()
        self._log(f"Descubiertos: {len(self.modulos_descubiertos)} modulos")

        # Resumen por categoria
        por_cat = {}
        for m in self.modulos_descubiertos:
            por_cat[m["categoria"]] = por_cat.get(m["categoria"], 0) + 1
        for cat, n in sorted(por_cat.items()):
            self._log(f"  {cat}: {n} modulos")

        return self.modulos_descubiertos

    def ejecutar_modulo(self, nombre, ruta, categoria):
        """Ejecuta un modulo como script independiente"""
        inicio = time.time()
        sha_pre = self._sha256_file(ruta)

        try:
            # Metodo 1: ejecutar como script
            result = subprocess.run(
                [sys.executable, ruta],
                capture_output=True, text=True, timeout=30,
                cwd=str(MIU_DIR)
            )
            duracion = time.time() - inicio
            exito = result.returncode == 0
            salida = result.stdout[:2000]
            error = result.stderr[:500] if result.stderr else None

            # Metodo 2: si fallo, intentar importar
            if not exito:
                try:
                    spec = __import__("importlib.util").util.spec_from_file_location(nombre, ruta)
                    mod = __import__("importlib.util").util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    # Si tiene funcion main(), ejecutarla
                    if hasattr(mod, "main"):
                        mod.main()
                    exito = True
                    salida = "Importado y ejecutado OK"
                    error = None
                except Exception as e2:
                    error = f"Script: {error}\nImport: {str(e2)[:200]}"

        except subprocess.TimeoutExpired:
            duracion = time.time() - inicio
            exito = False
            salida = ""
            error = "Timeout 30s"
        except Exception as e:
            duracion = time.time() - inicio
            exito = False
            salida = ""
            error = str(e)[:200]

        sha_post = self._sha256_file(ruta)

        # Guardar ejecucion
        c = self.db.cursor()
        c.execute("""INSERT INTO ejecuciones VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), nombre, categoria,
             int(exito), duracion, salida, error, sha_pre, sha_post))
        self.db.commit()

        # Actualizar modulo
        c.execute("SELECT exitos, fallos FROM modulos WHERE nombre=?", (nombre,))
        row = c.fetchone()
        if row:
            exitos, fallos = row
            if exito:
                exitos += 1
                estado = "activo"
            else:
                fallos += 1
                estado = "fallando" if fallos < 3 else "cementerio"

            c.execute("""UPDATE modulos SET exitos=?, fallos=?, estado=?, ultima_ejecucion=?,
                ultimo_error=? WHERE nombre=?""",
                (exitos, fallos, estado, datetime.now(timezone.utc).isoformat(), error, nombre))
            self.db.commit()

            # Si cementerio, mover archivo
            if estado == "cementerio" and fallos >= 3:
                destino = CEMENTERIO_DIR / f"{nombre}_{int(time.time())}.py"
                try:
                    os.rename(ruta, str(destino))
                    self._log(f"Modulo {nombre} enviado a cementerio ({fallos} fallos)", "WARN")
                except:
                    pass

        return {"nombre": nombre, "exito": exito, "duracion": duracion, "salida": salida, "error": error}

    def ejecutar_ciclo(self, categorias=None):
        """Ejecuta todos los modulos descubiertos, por categoria"""
        categorias = categorias or ["soporte", "prevencion", "reparacion", "inteligencia", "autonomia", "evolucion", "integracion", "seguridad"]
        resultados = []

        self._log("="*60)
        self._log("CICLO DE EJECUCION")
        self._log("="*60)

        # 1. Recursos
        self.monitorear_recursos()

        # 2. Descubrir
        self.descubrir_modulos()

        # 3. Ejecutar por categoria
        for cat in categorias:
            modulos_cat = [m for m in self.modulos_descubiertos if m["categoria"] == cat and m["estado"] != "cementerio"]
            if not modulos_cat:
                continue

            self._log(f"\n--- {cat.upper()} ({len(modulos_cat)} modulos) ---")
            for m in modulos_cat:
                self._log(f"Ejecutando: {m['nombre']}...")
                r = self.ejecutar_modulo(m["nombre"], m["ruta"], cat)
                resultados.append(r)
                status = "OK" if r["exito"] else "FALLO"
                self._log(f"  {status} en {r['duracion']:.2f}s")
                if r["error"]:
                    self._log(f"  Error: {r['error'][:80]}", "WARN")

        # 4. Resumen
        exitos = sum(1 for r in resultados if r["exito"])
        total = len(resultados)
        self._log(f"\n{'='*60}")
        self._log(f"RESUMEN: {exitos}/{total} modulos OK")
        self._log(f"{'='*60}")

        # 5. Guardar estado global
        estado = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "V∞+24.2",
            "modulos_ejecutados": total,
            "modulos_ok": exitos,
            "modulos_fallidos": total - exitos,
            "carencias": self.carencias
        }
        with open(NUTRIENTES_DIR / "estado_manager.json", "w") as f:
            json.dump(estado, f, indent=2)

        return resultados

    def informe(self):
        """Generar informe de estado"""
        c = self.db.cursor()

        print("\n" + "="*60)
        print("INFORME PLUGIN MANAGER V∞+24.2")
        print("="*60)

        # Modulos
        c.execute("SELECT categoria, COUNT(*), SUM(exitos), SUM(fallos) FROM modulos GROUP BY categoria")
        print("\nMODULOS POR CATEGORIA:")
        for row in c.fetchall():
            cat, total, exitos, fallos = row
            print(f"  {cat:15s}: {total:3d} modulos | {exitos} OK | {fallos} fallos")

        # Ejecuciones recientes
        c.execute("SELECT nombre, exito, duracion, timestamp FROM ejecuciones ORDER BY timestamp DESC LIMIT 10")
        print("\nULTIMAS 10 EJECUCIONES:")
        for row in c.fetchall():
            nombre, exito, duracion, ts = row
            status = "OK" if exito else "FALLO"
            print(f"  [{status}] {nombre:30s} {duracion:.2f}s | {ts[:19]}")

        # Recursos
        c.execute("SELECT * FROM recursos ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()
        if row:
            print(f"\nRECURSOS ACTUALES:")
            print(f"  CPU: {row[2]:.1f}% | MEM: {row[3]:.1f}% | DISCO: {row[4]:.1f}%")
            print(f"  PROCS: {row[5]} | BAT: {row[6]:.0f}%")

        print("="*60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="MIU Plugin Manager V∞+24.2")
    parser.add_argument("--ciclo", action="store_true", help="Ejecutar ciclo completo")
    parser.add_argument("--descubrir", action="store_true", help="Solo descubrir modulos")
    parser.add_argument("--recursos", action="store_true", help="Monitorear recursos")
    parser.add_argument("--informe", action="store_true", help="Generar informe")
    parser.add_argument("--ejecutar", help="Ejecutar modulo especifico")
    parser.add_argument("--categorias", nargs="+", help="Ejecutar solo estas categorias")
    args = parser.parse_args()

    pm = PluginManagerV24_2()

    if args.recursos:
        pm.monitorear_recursos()
    elif args.descubrir:
        pm.descubrir_modulos()
    elif args.ejecutar:
        ruta = str(PLUGINS_DIR / f"{args.ejecutar}.py")
        if os.path.exists(ruta):
            r = pm.ejecutar_modulo(args.ejecutar, ruta, "manual")
            print(json.dumps(r, indent=2))
        else:
            print(f"Modulo no encontrado: {args.ejecutar}")
    elif args.ciclo:
        pm.ejecutar_ciclo(args.categorias)
    elif args.informe:
        pm.informe()
    else:
        parser.print_help()
        print("\nEjemplos:")
        print("  python3 plugin_manager_v24_2.py --ciclo")
        print("  python3 plugin_manager_v24_2.py --ciclo --categorias soporte prevencion")
        print("  python3 plugin_manager_v24_2.py --ejecutar gobernador")
        print("  python3 plugin_manager_v24_2.py --recursos")
        print("  python3 plugin_manager_v24_2.py --informe")

if __name__ == "__main__":
    main()
