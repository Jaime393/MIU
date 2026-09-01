#!/usr/bin/env python3
"""
MIU V∞+38 — EXPLORADOR PROFUNDO Y MAPEADOR GLOBAL
Escanea todo el sistema de archivos, red local, servicios.
Genera inventario global y lo integra en el ciclo de evolución.
"""
import os, sys, json, time, threading, subprocess, socket, shutil, glob
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import queue

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
WWW = BASE / "www"
INVENTARIO_GLOBAL = NUTRIENTES / "inventario_global.json"
PUERTO_HTTP = 8080

# Extensiones de interés
EXTENSIONES = {
    "scripts": [".py", ".sh", ".js", ".rb", ".pl", ".go", ".rs", ".java"],
    "web": [".html", ".htm", ".css", ".php", ".asp", ".jsp"],
    "config": [".json", ".yaml", ".yml", ".toml", ".ini", ".conf", ".env"],
    "datos": [".csv", ".tsv", ".db", ".sqlite", ".log"],
    "modelos": [".gguf", ".bin", ".onnx", ".tflite", ".pb", ".h5", ".pth"],
    "documentos": [".md", ".txt", ".pdf", ".docx", ".odt"]
}

# Directorios a excluir (por seguridad y rendimiento)
EXCLUIR = [
    "/proc", "/sys", "/dev", "/tmp", "/run", "/var/cache",
    "/data/data/com.termux/files/usr/var", "/storage/emulated/0/Android",
    "/storage/emulated/0/Download", "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Music", "/storage/emulated/0/Pictures", "/storage/emulated/0/Movies"
]

# Subred para escaneo de red (por defecto 192.168.1.0/24)
SUBRED = "192.168.1"

# ============================================================
# 1. ESCÁNER DE SISTEMA DE ARCHIVOS (recursivo con límites)
# ============================================================
class EscanerArchivos:
    def __init__(self):
        self.inventario = defaultdict(list)
        self.contador = 0
        self.limite = 5000  # máximo de archivos a catalogar por pasada
        self.procesados = 0

    def _debe_excluir(self, ruta):
        ruta_str = str(ruta)
        for excl in EXCLUIR:
            if ruta_str.startswith(excl):
                return True
        return False

    def escanear(self, raiz):
        """Escanea recursivamente una raíz y cataloga archivos."""
        if self.procesados >= self.limite:
            return
        try:
            for item in raiz.iterdir():
                if self.procesados >= self.limite:
                    break
                if item.is_dir():
                    if not self._debe_excluir(item):
                        self.escanear(item)
                elif item.is_file():
                    ext = item.suffix.lower()
                    for categoria, exts in EXTENSIONES.items():
                        if ext in exts:
                            self.inventario[categoria].append({
                                "ruta": str(item),
                                "nombre": item.name,
                                "tamaño": item.stat().st_size,
                                "modificado": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                            })
                            self.procesados += 1
                            break
        except (PermissionError, OSError):
            pass

    def ejecutar(self, raices):
        """Escanea múltiples raíces."""
        for r in raices:
            if r.exists() and not self._debe_excluir(r):
                self.escanear(r)
        return self.inventario

# ============================================================
# 2. ESCÁNER DE RED LOCAL
# ============================================================
class EscanerRed:
    def __init__(self):
        self.dispositivos = []

    def escanear_puerto(self, ip, puerto):
        """Verifica si un puerto está abierto en un host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, puerto))
            sock.close()
            return result == 0
        except:
            return False

    def escanear_host(self, ip):
        """Escanea un host en busca de puertos comunes."""
        puertos = [22, 80, 443, 8080, 5000, 3000, 3306, 5432, 6379, 27017]
        abiertos = []
        for p in puertos:
            if self.escanear_puerto(ip, p):
                abiertos.append(p)
        if abiertos:
            self.dispositivos.append({"ip": ip, "puertos": abiertos})

    def escanear_subred(self, subred, inicio=1, fin=254, hilos=20):
        """Escanea una subred completa usando hilos."""
        print(f"   🌐 Escaneando red {subred}.0/24...")
        hilos_list = []
        cola = queue.Queue()
        for i in range(inicio, fin+1):
            ip = f"{subred}.{i}"
            cola.put(ip)

        def worker():
            while not cola.empty():
                ip = cola.get()
                self.escanear_host(ip)
                cola.task_done()

        for _ in range(min(hilos, fin-inicio+1)):
            t = threading.Thread(target=worker)
            t.start()
            hilos_list.append(t)
        cola.join()
        for t in hilos_list:
            t.join()
        return self.dispositivos

# ============================================================
# 3. ESCÁNER DE PROCESOS Y SERVICIOS
# ============================================================
class EscanerProcesos:
    def __init__(self):
        self.procesos = []
        self.servicios = []

    def escanear_procesos(self):
        """Lista procesos activos con ps."""
        try:
            out = subprocess.check_output(["ps", "aux"], text=True, timeout=5)
            for line in out.split('\n')[1:]:
                if line.strip():
                    partes = line.split(None, 10)
                    if len(partes) >= 11:
                        self.procesos.append({
                            "usuario": partes[0],
                            "pid": int(partes[1]),
                            "cpu": partes[2],
                            "mem": partes[3],
                            "comando": partes[10][:80]
                        })
        except:
            pass
        return self.procesos

    def escanear_servicios_systemd(self):
        """Si systemctl existe, lista servicios."""
        if shutil.which("systemctl"):
            try:
                out = subprocess.check_output(["systemctl", "list-units", "--type=service", "--all"], text=True, timeout=5)
                for line in out.split('\n'):
                    if ".service" in line and "loaded" in line:
                        partes = line.split()
                        if len(partes) >= 4:
                            self.servicios.append({"nombre": partes[0], "estado": partes[3]})
            except:
                pass
        return self.servicios

# ============================================================
# 4. INVENTARIO GLOBAL
# ============================================================
class InventarioGlobal:
    def __init__(self):
        self.datos = {
            "timestamp": datetime.now().isoformat(),
            "archivos": {},
            "dispositivos": [],
            "procesos": [],
            "servicios": []
        }

    def actualizar(self):
        # 1. Escanear archivos en varias raíces
        raices = [
            Path("os.path.expanduser('~')"),
            Path("/storage/emulated/0"),
            Path("/sdcard"),
            Path("/data/data/com.termux/files/usr/share")
        ]
        escaner_arch = EscanerArchivos()
        archivos = escaner_arch.ejecutar(raices)
        self.datos["archivos"] = {k: v[:100] for k, v in archivos.items()}  # limitar para no saturar

        # 2. Escanear red (subred por defecto, o detectar IP)
        try:
            # Obtener IP local y subred
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            subred = ".".join(ip_local.split('.')[:-1])
        except:
            subred = SUBRED
        escaner_red = EscanerRed()
        dispositivos = escaner_red.escanear_subred(subred, hilos=30)
        self.datos["dispositivos"] = dispositivos

        # 3. Procesos y servicios
        escaner_proc = EscanerProcesos()
        self.datos["procesos"] = escaner_proc.escanear_procesos()[:50]
        self.datos["servicios"] = escaner_proc.escanear_servicios_systemd()

        # 4. Guardar
        with open(INVENTARIO_GLOBAL, 'w') as f:
            json.dump(self.datos, f, indent=2)
        print(f"   📋 Inventario global guardado: {INVENTARIO_GLOBAL}")
        return self.datos

# ============================================================
# 5. PANEL DE MAPEO GLOBAL
# ============================================================
class PanelMapeo:
    def __init__(self, inventario):
        self.inventario = inventario

    def generar_html(self):
        datos = self.inventario.datos
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MIU — Mapa Global de Recursos</title>
    <style>
        body {{ font-family: monospace; background: #0d0d0d; color: #0f0; padding: 2rem; }}
        .card {{ background: #1a1a1a; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 3px solid #0f0; }}
        .card h2 {{ color: #0ff; }}
        .badge {{ background: #2a2a2a; padding: 0.1rem 0.6rem; border-radius: 12px; }}
        ul {{ list-style: none; padding-left: 0; }}
        li {{ padding: 0.2rem 0; border-bottom: 1px solid #222; }}
        .timestamp {{ color: #666; font-size: 0.8rem; }}
        .ip {{ color: #ff0; }}
    </style>
</head>
<body>
    <h1>🧬 Mapa Global de Recursos</h1>
    <div class="card">
        <p>Actualizado: {datos['timestamp']}</p>
        <p><span class="badge">Archivos</span> {sum(len(v) for v in datos['archivos'].values())} | <span class="badge">Dispositivos</span> {len(datos['dispositivos'])} | <span class="badge">Procesos</span> {len(datos['procesos'])}</p>
    </div>
    <div class="card">
        <h2>📡 Dispositivos en Red</h2>
        <ul>
        {''.join(f'<li><span class="ip">{d["ip"]}</span> — Puertos: {", ".join(map(str, d["puertos"]))}</li>' for d in datos['dispositivos'])}
        </ul>
    </div>
    <div class="card">
        <h2>📁 Archivos por Categoría</h2>
        {''.join(f'<h3>{cat}</h3><ul>{"".join(f"<li>{a["nombre"]} ({a["tamaño"]} bytes)</li>" for a in items[:10])}{"..." if len(items)>10 else ""}</ul>' for cat, items in datos['archivos'].items() if items)}
    </div>
    <div class="card">
        <h2>⚙️ Procesos Activos (Top 20)</h2>
        <ul>
        {''.join(f'<li>{p["comando"][:50]} — CPU: {p["cpu"]}% MEM: {p["mem"]}%</li>' for p in datos['procesos'][:20])}
        </ul>
    </div>
    <footer>ρ(x) > 0 — {datetime.now().isoformat()} <span onclick="location.reload()">↻</span></footer>
</body>
</html>"""
        return html

    def publicar(self):
        html = self.generar_html()
        ruta = WWW / "mapa_global.html"
        with open(ruta, 'w') as f:
            f.write(html)
        return ruta

# ============================================================
# 6. BUCLE DE EVOLUCIÓN PERPETUO
# ============================================================
class CicloEvolutivo:
    def __init__(self):
        self.inventario = InventarioGlobal()
        self.panel = PanelMapeo(self.inventario)
        self.ciclo = 0

    def paso(self):
        self.ciclo += 1
        print(f"🌍 CICLO DE EVOLUCIÓN {self.ciclo} — Mapeando y expandiendo...")
        # 1. Actualizar inventario global
        datos = self.inventario.actualizar()
        # 2. Generar panel
        ruta = self.panel.publicar()
        print(f"   📄 Panel disponible en http://localhost:{PUERTO_HTTP}/mapa_global.html")
        # 3. Detectar nuevos recursos y generar semillas
        if datos["dispositivos"]:
            print(f"   🌐 {len(datos['dispositivos'])} dispositivos detectados")
        # 4. Guardar estado
        with open(NUTRIENTES / "evolucion_ciclo.json", 'w') as f:
            json.dump({"ciclo": self.ciclo, "timestamp": datetime.now().isoformat()}, f)
        print(f"   ✅ CICLO {self.ciclo} COMPLETADO")

    def ejecutar(self, iteraciones=0, pausa=300):
        if iteraciones == 0:
            while True:
                try:
                    self.paso()
                    time.sleep(pausa)
                except KeyboardInterrupt:
                    print("⏹️ Interrumpido")
                    break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    time.sleep(pausa * 2)
        else:
            for i in range(iteraciones):
                try:
                    self.paso()
                    if i < iteraciones - 1:
                        time.sleep(pausa)
                except Exception as e:
                    print(f"⚠️ Error en ciclo {i+1}: {e}")
                    time.sleep(pausa)

# ============================================================
# 7. EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    import time
    print("="*60)
    print("🧬 V∞+38 — EXPLORADOR PROFUNDO Y MAPEADOR GLOBAL")
    print("="*60)
    ciclo = CicloEvolutivo()
    print("📡 Iniciando ciclo perpetuo de exploración y evolución")
    print("🌐 El sistema se extiende hacia afuera y mapea todo el territorio")
    print("⏳ Presiona Ctrl+C para detener")
    print("="*60)
    ciclo.ejecutar(iteraciones=0, pausa=180)  # cada 3 minutos
