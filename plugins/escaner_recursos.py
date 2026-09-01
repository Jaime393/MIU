#!/usr/bin/env python3
"""
MIU V∞+36 — ESCÁNER DE RECURSOS Y TEJIDO DE NAVEGADORES
Detecta navegadores, herramientas CLI, puertos, procesos, servicios.
Genera inventario y lo integra en el estado del sistema.
"""
import os, sys, json, time, subprocess, socket, platform, shutil
from pathlib import Path
from datetime import datetime
from collections import deque

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
INVENTARIO = BASE / "inventario.json"
WWW = BASE / "www"
PUERTO_HTTP = 8080

# ============================================================
# 1. ESCÁNER DE RECURSOS
# ============================================================
class EscanerRecursos:
    def __init__(self):
        self.inventario = {
            "timestamp": datetime.now().isoformat(),
            "sistema": {},
            "navegadores": [],
            "herramientas": [],
            "servicios": [],
            "puertos_abiertos": [],
            "procesos": [],
            "variables_entorno": {}
        }

    def escanear_sistema(self):
        """Información básica del sistema."""
        self.inventario["sistema"] = {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": sys.version,
            "cwd": str(Path.cwd()),
            "home": str(Path.home()),
            "termux": os.path.exists("/data/data/com.termux")
        }

    def escanear_navegadores(self):
        """Busca navegadores instalados."""
        navegadores = []
        posibles = [
            "firefox", "firefox-esr", "firefox-bin",
            "chromium", "chromium-browser", "chrome", "google-chrome",
            "brave", "brave-browser", "opera", "vivaldi", "epiphany", "midori", "surf"
        ]
        for nombre in posibles:
            ruta = shutil.which(nombre)
            if ruta:
                # Intentar obtener versión
                version = "desconocida"
                try:
                    if "firefox" in nombre:
                        cmd = [ruta, "--version"]
                    elif "chrome" in nombre or "chromium" in nombre:
                        cmd = [ruta, "--version"]
                    else:
                        cmd = [ruta, "--version"]
                    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=3)
                    version = out.strip().split('\n')[0]
                except:
                    pass
                navegadores.append({"nombre": nombre, "ruta": ruta, "version": version})
        self.inventario["navegadores"] = navegadores

    def escanear_herramientas_cli(self):
        """Detecta herramientas CLI útiles."""
        herramientas = []
        claves = [
            "curl", "wget", "git", "python3", "python", "node", "npm", "yarn",
            "gcc", "g++", "make", "cmake", "rustc", "cargo", "go", "java", "javac",
            "docker", "podman", "kubectl", "terraform", "ansible", "nmap", "netcat",
            "nc", "telnet", "ssh", "scp", "rsync", "vim", "nano", "emacs", "tmux", "screen"
        ]
        for cmd in claves:
            ruta = shutil.which(cmd)
            if ruta:
                version = "desconocida"
                try:
                    out = subprocess.check_output([ruta, "--version"], stderr=subprocess.STDOUT, text=True, timeout=2)
                    version = out.split('\n')[0][:60]
                except:
                    pass
                herramientas.append({"comando": cmd, "ruta": ruta, "version": version})
        self.inventario["herramientas"] = herramientas

    def escanear_servicios(self):
        """Detecta servicios locales (listados en /etc/services o systemctl)."""
        servicios = []
        # Servicios comunes en Android/Termux
        comunes = ["http", "https", "ssh", "ftp", "smtp", "mysql", "postgresql", "redis", "mongodb", "docker"]
        for nombre in comunes:
            # Verificar si hay un proceso con ese nombre
            try:
                out = subprocess.check_output(["pgrep", "-x", nombre], stderr=subprocess.DEVNULL, text=True)
                if out.strip():
                    servicios.append({"nombre": nombre, "estado": "activo"})
            except:
                pass
        # También verificar systemctl si existe
        if shutil.which("systemctl"):
            try:
                out = subprocess.check_output(["systemctl", "list-units", "--type=service", "--all"], text=True, timeout=5)
                for line in out.split('\n'):
                    if ".service" in line and "loaded" in line:
                        partes = line.split()
                        if len(partes) >= 4:
                            servicios.append({"nombre": partes[0], "estado": partes[3]})
            except:
                pass
        self.inventario["servicios"] = servicios

    def escanear_puertos_abiertos(self):
        """Puertos en escucha local."""
        puertos = []
        try:
            # Usar netstat o ss
            for cmd in ["ss -tuln", "netstat -tuln"]:
                try:
                    out = subprocess.check_output(cmd, shell=True, text=True, timeout=3)
                    for line in out.split('\n'):
                        if "LISTEN" in line or "0.0.0.0" in line or ":::" in line:
                            partes = line.split()
                            if len(partes) >= 5:
                                proto = partes[0]
                                addr = partes[4] if ':' in partes[4] else partes[3]
                                if ':' in addr:
                                    puerto = addr.split(':')[-1]
                                    if puerto.isdigit():
                                        puertos.append({"proto": proto, "puerto": int(puerto), "direccion": addr})
                    break
                except:
                    continue
        except:
            pass
        self.inventario["puertos_abiertos"] = puertos

    def escanear_procesos(self):
        """Lista de procesos activos (top 20 por CPU o memoria)."""
        procesos = []
        try:
            # Usar ps aux --sort=-%mem | head -20
            out = subprocess.check_output(["ps", "aux", "--sort=-%mem"], text=True, timeout=3)
            lineas = out.split('\n')[1:21]  # saltar cabecera
            for line in lineas:
                if line.strip():
                    partes = line.split(None, 10)
                    if len(partes) >= 11:
                        procesos.append({
                            "usuario": partes[0],
                            "pid": int(partes[1]),
                            "cpu": partes[2],
                            "mem": partes[3],
                            "comando": partes[10][:60]
                        })
        except:
            # Fallback: ps sin sort
            try:
                out = subprocess.check_output(["ps", "aux"], text=True, timeout=3)
                for line in out.split('\n')[1:20]:
                    if line.strip():
                        partes = line.split(None, 10)
                        if len(partes) >= 11:
                            procesos.append({"usuario": partes[0], "pid": int(partes[1]), "comando": partes[10][:60]})
            except:
                pass
        self.inventario["procesos"] = procesos

    def escanear_variables(self):
        """Variables de entorno relevantes."""
        relevantes = ["PATH", "HOME", "TERM", "SHELL", "LANG", "USER", "ANDROID_ROOT", "TERMUX_VERSION"]
        vars_env = {}
        for key in relevantes:
            vars_env[key] = os.environ.get(key, "")
        self.inventario["variables_entorno"] = vars_env

    def ejecutar(self):
        """Ejecuta todos los escaneos."""
        self.escanear_sistema()
        self.escanear_navegadores()
        self.escanear_herramientas_cli()
        self.escanear_servicios()
        self.escanear_puertos_abiertos()
        self.escanear_procesos()
        self.escanear_variables()
        # Guardar inventario
        with open(INVENTARIO, 'w') as f:
            json.dump(self.inventario, f, indent=2)
        return self.inventario

# ============================================================
# 2. INTEGRACIÓN CON EL EXPANSOR WEB
# ============================================================
class ExpansorConInventario:
    def __init__(self):
        self.inventario = None
        self.servidor = None  # se asignará desde fuera

    def actualizar_inventario(self):
        escaner = EscanerRecursos()
        self.inventario = escaner.ejecutar()
        print(f"   📋 Inventario actualizado: {len(self.inventario['navegadores'])} navegadores, {len(self.inventario['herramientas'])} herramientas")
        return self.inventario

    def generar_pagina_inventario(self):
        """Genera una página HTML con el inventario."""
        if not self.inventario:
            self.actualizar_inventario()
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIU — Inventario de Recursos</title>
    <style>
        body {{ font-family: monospace; background: #0d0d0d; color: #0f0; padding: 2rem; }}
        .card {{ background: #1a1a1a; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; border-left: 3px solid #0f0; }}
        .badge {{ background: #2a2a2a; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; }}
        .titulo {{ color: #0ff; }}
        ul {{ list-style: none; padding-left: 0; }}
        li {{ padding: 0.2rem 0; border-bottom: 1px solid #1a1a1a; }}
    </style>
</head>
<body>
    <h1>🧬 Inventario de Recursos</h1>
    <div class="card">
        <p><span class="badge">Sistema</span> {self.inventario['sistema']['platform']} | {self.inventario['sistema']['machine']}</p>
        <p>Host: {self.inventario['sistema']['hostname']}</p>
    </div>
    <div class="card">
        <h3>🌐 Navegadores ({len(self.inventario['navegadores'])})</h3>
        <ul>
        {''.join(f'<li><span class="badge">{b["nombre"]}</span> {b["version"][:30]} <span style="color:#666;">{b["ruta"]}</span></li>' for b in self.inventario['navegadores'])}
        </ul>
    </div>
    <div class="card">
        <h3>🛠️ Herramientas CLI ({len(self.inventario['herramientas'])})</h3>
        <ul>
        {''.join(f'<li><span class="badge">{h["comando"]}</span> {h["version"][:40]}</li>' for h in self.inventario['herramientas'])}
        </ul>
    </div>
    <div class="card">
        <h3>🔌 Servicios ({len(self.inventario['servicios'])})</h3>
        <ul>
        {''.join(f'<li>{s["nombre"]} — {s.get("estado", "activo")}</li>' for s in self.inventario['servicios'])}
        </ul>
    </div>
    <div class="card">
        <h3>🔓 Puertos abiertos ({len(self.inventario['puertos_abiertos'])})</h3>
        <ul>
        {''.join(f'<li>{p["proto"]}:{p["puerto"]} ({p["direccion"]})</li>' for p in self.inventario['puertos_abiertos'])}
        </ul>
    </div>
    <footer>ρ(x) > 0 — {datetime.now().isoformat()}</footer>
</body>
</html>"""
        return html

    def abrir_con_navegador(self, url):
        """Abre la URL con el primer navegador detectado."""
        if not self.inventario:
            self.actualizar_inventario()
        navegadores = self.inventario.get('navegadores', [])
        for nav in navegadores:
            try:
                subprocess.Popen([nav['ruta'], url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   🌍 Abierto con {nav['nombre']}: {url}")
                return True
            except:
                continue
        # Fallback: webbrowser
        try:
            import webbrowser
            webbrowser.open(url)
            print(f"   🌍 Abierto con webbrowser: {url}")
            return True
        except:
            print(f"   🌐 Abre manualmente: {url}")
            return False

# ============================================================
# 3. EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("🧬 V∞+36 — ESCÁNER DE RECURSOS")
    print("="*60)
    expansor = ExpansorConInventario()
    # Escanear y mostrar resumen
    inv = expansor.actualizar_inventario()
    print(f"📋 Navegadores: {len(inv['navegadores'])}")
    for b in inv['navegadores']:
        print(f"   • {b['nombre']}: {b['ruta']}")
    print(f"🛠️ Herramientas: {len(inv['herramientas'])}")
    print(f"🔌 Servicios: {len(inv['servicios'])}")
    print(f"🔓 Puertos: {len(inv['puertos_abiertos'])}")
    # Generar página de inventario
    html = expansor.generar_pagina_inventario()
    ruta = WWW / "inventario.html"
    with open(ruta, 'w') as f:
        f.write(html)
    print(f"📄 Página de inventario: {ruta}")
    # Abrir con navegador
    url = f"http://localhost:{PUERTO_HTTP}/inventario.html"
    expansor.abrir_con_navegador(url)
    print("="*60)
    print("✅ Inventario generado y abierto en navegador")
    print("ρ(x) > 0 — El sistema conoce sus recursos.")
