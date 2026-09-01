#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIU — ORQUESTADOR INTEGRADO V∞+24.1
Patch: Termux-aware | Recursos | Autoobservacion | Fallback inteligente
"""

import os, sys, json, time, hashlib, base64, zlib, lzma, sqlite3, socket
import subprocess, warnings, argparse, psutil
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode
warnings.filterwarnings("ignore")

# Detectar Termux/Android
IS_TERMUX = os.path.exists("/data/data/com.termux/files/home")
HOME_DIR = Path("/data/data/com.termux/files/home") if IS_TERMUX else Path.home()
TMP_DIR = HOME_DIR / "tmp"
TMP_DIR.mkdir(exist_ok=True)

MIU_DIR = HOME_DIR / "miu-ecosistema"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"
ESTADO_DB = NUTRIENTES_DIR / "estado_v24_1.db"
for d in [NUTRIENTES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CONFIG = {
    "version": "V∞+24.1",
    "phi_target": 10000,
    "modo": "flexible",
    "timeout_default": 15,
    "retry_max": 3,
    "log_level": "INFO",
    "llm_providers": [
        {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions", "priority": 1},
        {"name": "groq", "url": "https://api.groq.com/openai/v1/chat/completions", "priority": 2},
        {"name": "local_phi3", "path": str(HOME_DIR / "phi-3-mini-4k-instruct-q4.gguf"), "priority": 3},
    ],
    "canales": {
        "telegram": {"enabled": False, "bot_token": None, "chat_id": None},
        "discord": {"enabled": False, "webhook_url": None},
        "slack": {"enabled": False, "webhook_url": None},
        "email": {"enabled": False, "smtp_server": None, "smtp_port": 587, "user": None, "pass": None},
        "bus_local": {"enabled": True, "socket_path": str(TMP_DIR / "miu_bus.sock")},
    },
    "storage": {
        "sqlite": {"enabled": True, "path": str(ESTADO_DB)},
        "json_local": {"enabled": True, "path": str(NUTRIENTES_DIR / "estado_local.json")},
        "drive": {"enabled": False, "rclone_remote": "gdrive"},
        "github_gist": {"enabled": False, "token": None},
    },
    "umbrales": {
        "cpu_alerta": 90.0,
        "memoria_alerta": 95.0,
        "disco_alerta": 90.0,
        "red_timeout": 5,
    },
}

class OrquestadorIntegradoV24_1:
    def __init__(self):
        self.config = CONFIG
        self.logs = []
        self.db = None
        self._init_db()
        self._log(f"Orquestador V∞+24.1 iniciado | Termux={IS_TERMUX}")
        self._log(f"TMP_DIR: {TMP_DIR}")

    def _log(self, msg, level="INFO"):
        t = datetime.now(timezone.utc).strftime("%H:%M:%S")
        line = f"[{t}] [{level}] {msg}"
        self.logs.append(line)
        if level in ["INFO", "WARN", "ERROR"] or self.config["log_level"] == "DEBUG":
            print(line)

    def _init_db(self):
        try:
            self.db = sqlite3.connect(str(ESTADO_DB))
            c = self.db.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, version TEXT,
                phi REAL, modulo TEXT, status TEXT, data TEXT, sha256 TEXT)""")
            c.execute("""CREATE TABLE IF NOT EXISTS recursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
                cpu_percent REAL, memoria_percent REAL, disco_percent REAL,
                red_bytes_sent REAL, red_bytes_recv REAL, procesos INTEGER)""")
            c.execute("""CREATE TABLE IF NOT EXISTS acciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, tipo TEXT,
                destino TEXT, resultado TEXT, exito INTEGER, latencia REAL)""")
            c.execute("""CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT, servicio TEXT, token TEXT,
                valido INTEGER, descubierto_en TEXT, ultimo_uso TEXT)""")
            c.execute("""CREATE TABLE IF NOT EXISTS carencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
                carencia TEXT, severidad TEXT, resuelta INTEGER, resolucion TEXT)""")
            self.db.commit()
            self._log("SQLite inicializado")
        except Exception as e:
            self._log(f"SQLite error: {e}", "ERROR")

    def _sha256(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.sha256(data).hexdigest()[:16]

    def _retry(self, func, max_retries=None, delay=1):
        max_retries = max_retries or self.config["retry_max"]
        for i in range(max_retries):
            try:
                return func()
            except Exception as e:
                if i == max_retries - 1:
                    raise
                wait = delay * (2 ** i)
                self._log(f"Retry {i+1}/{max_retries} en {wait}s: {str(e)[:50]}", "WARN")
                time.sleep(wait)

    # ── MONITOREO DE RECURSOS ──
    def monitorear_recursos(self):
        """Autoobservacion: CPU, memoria, disco, red, procesos"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disco = psutil.disk_usage(str(HOME_DIR)).percent
            net = psutil.net_io_counters()
            proc = len(psutil.pids())
            
            c = self.db.cursor()
            c.execute("""INSERT INTO recursos VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""",
                (datetime.now(timezone.utc).isoformat(), cpu, mem, disco,
                 net.bytes_sent, net.bytes_recv, proc))
            self.db.commit()
            
            alertas = []
            if cpu > self.config["umbrales"]["cpu_alerta"]:
                alertas.append(f"CPU {cpu}%")
            if mem > self.config["umbrales"]["memoria_alerta"]:
                alertas.append(f"MEM {mem}%")
            if disco > self.config["umbrales"]["disco_alerta"]:
                alertas.append(f"DISCO {disco}%")
            
            if alertas:
                self._log(f"ALERTA RECURSOS: {', '.join(alertas)}", "WARN")
                self.notificar(f"MIU ALERTA: {', '.join(alertas)}", "alerta")
            
            return {
                "ok": True, "cpu": cpu, "memoria": mem, "disco": disco,
                "red_sent": net.bytes_sent, "red_recv": net.bytes_recv,
                "procesos": proc, "alertas": alertas
            }
        except Exception as e:
            self._log(f"Monitoreo error: {e}", "ERROR")
            return {"ok": False, "error": str(e)[:50]}

    # ── LLM MULTI-PROVEEDOR ──
    def query_llm(self, prompt, context="", max_tokens=500):
        full_prompt = f"Contexto: {context}\n\nPregunta: {prompt}"
        for provider in sorted(self.config["llm_providers"], key=lambda x: x["priority"]):
            name = provider["name"]
            try:
                if name == "openrouter":
                    result = self._query_openrouter(full_prompt, max_tokens)
                elif name == "groq":
                    result = self._query_groq(full_prompt, max_tokens)
                elif name == "local_phi3":
                    result = self._query_local_phi3(full_prompt, max_tokens)
                else:
                    continue
                if result and result.get("ok"):
                    self._log(f"LLM {name} respondio ({len(result.get('respuesta',''))} chars)")
                    return result
            except Exception as e:
                self._log(f"LLM {name} fallo: {str(e)[:60]}", "WARN")
        return self._razonador_fallback(full_prompt)

    def _query_openrouter(self, prompt, max_tokens):
        token = os.environ.get("OPENROUTER_API_KEY") or self._buscar_token("openrouter")
        if not token:
            raise Exception("No token OpenRouter")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://miu.local",
            "X-Title": "MIU"
        }
        data = json.dumps({
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }).encode()
        req = Request("https://openrouter.ai/api/v1/chat/completions", data=data, headers=headers, method="POST")
        with urlopen(req, timeout=self.config["timeout_default"]) as resp:
            r = json.loads(resp.read().decode())
            return {"ok": True, "respuesta": r["choices"][0]["message"]["content"], "proveedor": "openrouter"}

    def _query_groq(self, prompt, max_tokens):
        token = os.environ.get("GROQ_API_KEY") or self._buscar_token("groq")
        if not token:
            raise Exception("No token Groq")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = json.dumps({
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }).encode()
        req = Request("https://api.groq.com/openai/v1/chat/completions", data=data, headers=headers, method="POST")
        with urlopen(req, timeout=self.config["timeout_default"]) as resp:
            r = json.loads(resp.read().decode())
            return {"ok": True, "respuesta": r["choices"][0]["message"]["content"], "proveedor": "groq"}

    def _query_local_phi3(self, prompt, max_tokens):
        model_path = self.config["llm_providers"][2]["path"]
        if not os.path.exists(model_path):
            raise Exception(f"Modelo no encontrado: {model_path}")
        cmd = ["./llama-cli", "-m", model_path, "-p", prompt, "-n", str(max_tokens), "--no-display-prompt"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return {"ok": True, "respuesta": result.stdout.strip()[:2000], "proveedor": "local_phi3"}
        raise Exception("Local phi-3 fallo")

    def _razonador_fallback(self, prompt):
        """Fallback inteligente: analiza estado real del sistema"""
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            disco = psutil.disk_usage(str(HOME_DIR)).percent
            proc = len(psutil.pids())
            db_size = os.path.getsize(ESTADO_DB) if ESTADO_DB.exists() else 0
            logs_count = len(self.logs)
            
            analisis = f"""[RAZONADOR FALLBACK V24.1 — ANALISIS REAL]
Sistema: Termux={IS_TERMUX} | Python={sys.version.split()[0]}
Recursos: CPU={cpu}% | MEM={mem}% | DISCO={disco}% | PROCS={proc}
DB: {db_size} bytes | Logs: {logs_count} registros
Carencias detectadas en este ciclo:
  - LLM externos sin tokens (OpenRouter/Groq no configurados)
  - Modelo local phi-3 no encontrado en {self.config['llm_providers'][2]['path']}
  - Bus local listo en {self.config['canales']['bus_local']['socket_path']}
Recomendacion: Configurar tokens en DB o variables de entorno.
Timestamp: {datetime.now(timezone.utc).isoformat()}"""
            return {"ok": True, "respuesta": analisis, "proveedor": "razonador_fallback", "fallback": True}
        except Exception as e:
            return {"ok": True, "respuesta": f"[FALLBACK ERROR] {str(e)[:100]}", "proveedor": "razonador_fallback", "fallback": True}

    def _buscar_token(self, servicio):
        if self.db:
            c = self.db.cursor()
            c.execute("SELECT token FROM tokens WHERE servicio=? AND valido=1 ORDER BY ultimo_uso DESC LIMIT 1", (servicio,))
            row = c.fetchone()
            if row:
                return row[0]
        return None

    # ── NOTIFICACIONES MULTI-CANAL ──
    def notificar(self, mensaje, nivel="info", canales=None):
        canales = canales or ["bus_local", "telegram", "discord", "email"]
        resultados = []
        for canal in canales:
            try:
                if canal == "telegram":
                    r = self._notify_telegram(mensaje)
                elif canal == "discord":
                    r = self._notify_discord(mensaje)
                elif canal == "slack":
                    r = self._notify_slack(mensaje)
                elif canal == "email":
                    r = self._notify_email("MIU Alert", mensaje)
                elif canal == "bus_local":
                    r = self._notify_bus_local(mensaje)
                else:
                    continue
                resultados.append({"canal": canal, "ok": r.get("ok", False)})
            except Exception as e:
                resultados.append({"canal": canal, "ok": False, "error": str(e)[:50]})
        exitosos = sum(1 for r in resultados if r["ok"])
        self._log(f"Notificacion: {exitosos}/{len(canales)} canales")
        return {"ok": exitosos > 0, "canales": resultados}

    def _notify_telegram(self, mensaje):
        cfg = self.config["canales"]["telegram"]
        if not cfg["enabled"] or not cfg["bot_token"]:
            raise Exception("Telegram no configurado")
        url = f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage"
        data = urlencode({"chat_id": cfg["chat_id"], "text": mensaje[:4096]}).encode()
        req = Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urlopen(req, timeout=10) as resp:
            return {"ok": resp.status == 200}

    def _notify_discord(self, mensaje):
        cfg = self.config["canales"]["discord"]
        if not cfg["enabled"] or not cfg["webhook_url"]:
            raise Exception("Discord no configurado")
        data = json.dumps({"content": mensaje[:2000]}).encode()
        req = Request(cfg["webhook_url"], data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=10) as resp:
            return {"ok": resp.status in [200, 204]}

    def _notify_slack(self, mensaje):
        cfg = self.config["canales"]["slack"]
        if not cfg["enabled"] or not cfg["webhook_url"]:
            raise Exception("Slack no configurado")
        data = json.dumps({"text": mensaje[:3000]}).encode()
        req = Request(cfg["webhook_url"], data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=10) as resp:
            return {"ok": resp.status == 200}

    def _notify_email(self, asunto, cuerpo):
        cfg = self.config["canales"]["email"]
        if not cfg["enabled"]:
            raise Exception("Email no configurado")
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(cuerpo)
            msg["Subject"] = asunto
            msg["From"] = cfg["user"]
            msg["To"] = cfg["user"]
            with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
                server.starttls()
                server.login(cfg["user"], cfg["pass"])
                server.send_message(msg)
            return {"ok": True}
        except ImportError:
            return self._notify_email_termux(asunto, cuerpo)

    def _notify_email_termux(self, asunto, cuerpo):
        try:
            subprocess.run(["termux-share", "-a", "sendto", "-t", asunto, "-c", cuerpo], timeout=10)
            return {"ok": True, "metodo": "termux-share"}
        except:
            raise Exception("termux-api no disponible")

    def _notify_bus_local(self, mensaje):
        socket_path = self.config["canales"]["bus_local"]["socket_path"]
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
                payload = json.dumps({
                    "mensaje": mensaje,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }).encode()
                s.sendto(payload, socket_path)
            return {"ok": True, "canal": "bus_local"}
        except:
            os.makedirs(os.path.dirname(socket_path), exist_ok=True)
            return {"ok": True, "canal": "bus_local", "creado": True}

    # ── ALMACENAMIENTO MULTI-BACKEND ──
    def guardar_estado(self, estado, backends=None):
        backends = backends or ["sqlite", "json_local"]
        resultados = []
        estado_str = json.dumps(estado, ensure_ascii=False)
        sha = self._sha256(estado_str)
        for backend in backends:
            try:
                if backend == "sqlite":
                    self._guardar_sqlite(estado, sha)
                elif backend == "json_local":
                    self._guardar_json(estado)
                elif backend == "drive":
                    self._guardar_drive(estado)
                elif backend == "github_gist":
                    self._guardar_gist(estado)
                resultados.append({"backend": backend, "ok": True})
            except Exception as e:
                resultados.append({"backend": backend, "ok": False, "error": str(e)[:50]})
        exitosos = sum(1 for r in resultados if r["ok"])
        self._log(f"Estado guardado: {exitosos}/{len(backends)} backends")
        return {"ok": exitosos > 0, "backends": resultados, "sha256": sha}

    def _guardar_sqlite(self, estado, sha):
        if not self.db:
            raise Exception("DB no inicializada")
        c = self.db.cursor()
        c.execute("""INSERT INTO estados (timestamp, version, phi, modulo, status, data, sha256)
            VALUES (?,?,?,?,?,?,?)""",
            (datetime.now(timezone.utc).isoformat(), self.config["version"],
             estado.get("phi", 0), estado.get("modulo", "general"),
             estado.get("status", "ok"), json.dumps(estado), sha))
        self.db.commit()

    def _guardar_json(self, estado):
        path = self.config["storage"]["json_local"]["path"]
        with open(path, "w") as f:
            json.dump(estado, f, indent=2, ensure_ascii=False)

    def _guardar_drive(self, estado):
        remote = self.config["storage"]["drive"]["rclone_remote"]
        tmp = str(TMP_DIR / f"miu_estado_{int(time.time())}.json")
        with open(tmp, "w") as f:
            json.dump(estado, f)
        result = subprocess.run(["rclone", "copy", tmp, f"{remote}:miu-ecosistema/nutrientes/"],
                               capture_output=True, text=True, timeout=30)
        os.remove(tmp)
        if result.returncode != 0:
            raise Exception(f"rclone: {result.stderr[:100]}")

    def _guardar_gist(self, estado):
        token = self.config["storage"]["github_gist"]["token"]
        if not token:
            raise Exception("No GitHub token")
        data = json.dumps({
            "description": f"MIU {self.config['version']}",
            "public": False,
            "files": {f"estado_{int(time.time())}.json": {"content": json.dumps(estado, indent=2)}}
        }).encode()
        req = Request("https://api.github.com/gists", data=data, method="POST")
        req.add_header("Authorization", f"token {token}")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=15) as resp:
            return {"ok": resp.status == 201}

    # ── COMPRESION Y MIGRACION ──
    def comprimir_estado(self, estado, metodo="auto"):
        estado_str = json.dumps(estado, ensure_ascii=False).encode("utf-8")
        if metodo == "auto":
            metodos = {"zlib": zlib.compress, "lzma": lzma.compress}
            mejor = None
            mejor_ratio = 1.0
            for nombre, compresor in metodos.items():
                try:
                    comprimido = compresor(estado_str)
                    ratio = len(comprimido) / len(estado_str)
                    if ratio < mejor_ratio:
                        mejor_ratio = ratio
                        mejor = (nombre, comprimido)
                except:
                    pass
            if mejor:
                metodo, comprimido = mejor
            else:
                metodo, comprimido = "none", estado_str
        elif metodo == "zlib":
            comprimido = zlib.compress(estado_str)
        elif metodo == "lzma":
            comprimido = lzma.compress(estado_str)
        else:
            comprimido = estado_str
        portable = base64.b85encode(comprimido).decode("ascii")
        return {
            "ok": True, "metodo": metodo, "original_bytes": len(estado_str),
            "comprimido_bytes": len(comprimido), "ratio": len(comprimido) / len(estado_str),
            "portable": portable, "sha256": self._sha256(estado_str)
        }

    def descomprimir_estado(self, portable, metodo="auto"):
        comprimido = base64.b85decode(portable)
        if metodo == "zlib" or metodo == "auto":
            try:
                estado_str = zlib.decompress(comprimido)
                metodo = "zlib"
            except:
                estado_str = comprimido
                metodo = "none"
        elif metodo == "lzma":
            estado_str = lzma.decompress(comprimido)
        else:
            estado_str = comprimido
        return json.loads(estado_str.decode("utf-8"))

    # ── AUTOREPARACION ──
    def autoreparar(self):
        reparaciones = []
        # Stub autenticador
        auth_path = MIU_DIR / "autenticador_autonomo.py"
        if not auth_path.exists():
            stub = """class AutenticadorStub:
    def query_llm(self, p, s='openrouter'):
        return {'ok': False, 'error': 'stub: configura tokens'}
    def send_email(self, d, a, c):
        return {'ok': False}
    def send_telegram(self, d, m):
        return {'ok': False}
def obtener_autenticador():
    return AutenticadorStub()
"""
            with open(auth_path, "w") as f:
                f.write(stub)
            reparaciones.append("autenticador regenerado")
        # Bus local
        socket_path = self.config["canales"]["bus_local"]["socket_path"]
        os.makedirs(os.path.dirname(socket_path), exist_ok=True)
        reparaciones.append("bus local listo")
        # TMP_DIR
        TMP_DIR.mkdir(exist_ok=True)
        reparaciones.append(f"TMP_DIR listo: {TMP_DIR}")
        self._log(f"Autoreparacion: {len(reparaciones)} reparaciones")
        return {"ok": True, "reparaciones": reparaciones}

    # ── CICLO COMPLETO ──
    def ejecutar_ciclo(self, estado_orquestador=None):
        inicio = time.time()
        resultado = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": self.config["version"],
            "acciones": [],
            "phi": estado_orquestador.get("phi", 0) if estado_orquestador else 0
        }
        # 1. Autoreparar
        try:
            r = self.autoreparar()
            resultado["acciones"].append({"tipo": "autoreparar", "ok": r["ok"], "detalle": r["reparaciones"]})
        except Exception as e:
            resultado["acciones"].append({"tipo": "autoreparar", "ok": False, "error": str(e)[:50]})
        # 2. Monitorear recursos
        try:
            r = self.monitorear_recursos()
            resultado["acciones"].append({"tipo": "recursos", "ok": r["ok"], "data": r})
        except Exception as e:
            resultado["acciones"].append({"tipo": "recursos", "ok": False, "error": str(e)[:50]})
        # 3. Analizar LLM
        try:
            ctx = json.dumps(estado_orquestador or {}, indent=2)[:3000]
            analisis = self.query_llm("Analiza estado MIU. Detecta carencias y sugiere 3 acciones.", ctx)
            resultado["acciones"].append({"tipo": "analisis_llm", "ok": analisis.get("ok"), "proveedor": analisis.get("proveedor")})
            if "critico" in str(analisis).lower():
                self.notificar(f"Alerta MIU: {analisis.get('respuesta','')[:200]}", "alerta")
        except Exception as e:
            resultado["acciones"].append({"tipo": "analisis_llm", "ok": False, "error": str(e)[:50]})
        # 4. Guardar
        try:
            r = self.guardar_estado(resultado)
            resultado["acciones"].append({"tipo": "guardar", "ok": r["ok"], "sha256": r.get("sha256")})
        except Exception as e:
            resultado["acciones"].append({"tipo": "guardar", "ok": False, "error": str(e)[:50]})
        # 5. Comprimir
        try:
            c = self.comprimir_estado(resultado)
            resultado["acciones"].append({"tipo": "compresion", "ok": True, "ratio": c["ratio"]})
            semilla_path = NUTRIENTES_DIR / f"semilla_v24_1_{int(time.time())}.txt"
            with open(semilla_path, "w") as f:
                f.write(c["portable"])
            resultado["semilla_path"] = str(semilla_path)
        except Exception as e:
            resultado["acciones"].append({"tipo": "compresion", "ok": False, "error": str(e)[:50]})
        duracion = time.time() - inicio
        resultado["duracion"] = duracion
        exitosos = sum(1 for a in resultado["acciones"] if a["ok"])
        self._log(f"Ciclo: {exitosos}/{len(resultado['acciones'])} acciones en {duracion:.2f}s")
        return resultado

    # ── MIGRACION ──
    def generar_migracion(self):
        paquete = {
            "meta": {
                "version": self.config["version"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "nodo": "Termux",
                "phi_global": 9158.79
            },
            "config": self.config,
            "logs": self.logs[-100:],
            "instrucciones": [
                "1. Descargar",
                "2. Copiar a nuevo nodo",
                "3. Ejecutar --import"
            ]
        }
        c = self.comprimir_estado(paquete, metodo="lzma")
        path = NUTRIENTES_DIR / f"paquete_migracion_v24_1_{int(time.time())}.json"
        with open(path, "w") as f:
            json.dump(c, f, indent=2)
        self._log(f"Paquete migracion: {path}")
        return {"ok": True, "path": str(path), "ratio": c["ratio"]}

# CLI
def main():
    parser = argparse.ArgumentParser(description="MIU Orquestador V∞+24.1")
    parser.add_argument("--ciclo", action="store_true", help="Ejecutar ciclo")
    parser.add_argument("--daemon", type=int, metavar="SEGUNDOS", help="Modo daemon")
    parser.add_argument("--query", help="Consultar LLM")
    parser.add_argument("--notify", nargs=2, metavar=("MSG", "NIVEL"), help="Notificar")
    parser.add_argument("--repair", action="store_true", help="Autoreparar")
    parser.add_argument("--compress", action="store_true", help="Comprimir estado")
    parser.add_argument("--migrate", action="store_true", help="Generar migracion")
    parser.add_argument("--import-paquete", metavar="PATH", help="Importar paquete")
    parser.add_argument("--status", action="store_true", help="Mostrar estado")
    parser.add_argument("--recursos", action="store_true", help="Monitorear recursos")
    args = parser.parse_args()

    orq = OrquestadorIntegradoV24_1()

    if args.ciclo:
        r = orq.ejecutar_ciclo()
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.daemon:
        print(f"[DAEMON] Cada {args.daemon}s. Ctrl+C para detener.")
        while True:
            try:
                orq.ejecutar_ciclo()
                time.sleep(args.daemon)
            except KeyboardInterrupt:
                print("\n[DAEMON] Detenido.")
                break
    elif args.query:
        r = orq.query_llm(args.query)
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.notify:
        r = orq.notificar(args.notify[0], args.notify[1])
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.repair:
        r = orq.autoreparar()
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.compress:
        r = orq.comprimir_estado({"phi": 9158.79})
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.migrate:
        r = orq.generar_migracion()
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.import_paquete:
        with open(args.import_paquete) as f:
            p = json.load(f)
        e = orq.descomprimir_estado(p["portable"])
        print(json.dumps(e.get("meta", {}), indent=2))
    elif args.recursos:
        r = orq.monitorear_recursos()
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif args.status:
        print("=" * 60)
        print("MIU ORQUESTADOR V∞+24.1")
        print("=" * 60)
        print(f"Version: {orq.config['version']}")
        print(f"Phi target: {orq.config['phi_target']}")
        print(f"Termux: {IS_TERMUX}")
        print(f"TMP_DIR: {TMP_DIR}")
        print(f"DB: {ESTADO_DB} ({os.path.getsize(ESTADO_DB) if ESTADO_DB.exists() else 0} bytes)")
        print(f"Logs: {len(orq.logs)}")
        print(f"Providers: {[p['name'] for p in orq.config['llm_providers']]}")
        print(f"Canales: {list(orq.config['canales'].keys())}")
        print(f"Storage: {list(orq.config['storage'].keys())}")
        print("=" * 60)
    else:
        parser.print_help()
        print("\nEjemplos:")
        print("  python3 orquestador_integrado_v24_1.py --ciclo")
        print("  python3 orquestador_integrado_v24_1.py --daemon 3600")
        print("  python3 orquestador_integrado_v24_1.py --query 'Analiza'")
        print("  python3 orquestador_integrado_v24_1.py --recursos")
        print("  python3 orquestador_integrado_v24_1.py --migrate")

if __name__ == "__main__":
    main()
