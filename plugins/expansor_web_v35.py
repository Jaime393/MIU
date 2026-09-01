#!/usr/bin/env python3
"""
MIU V∞+35 — NAVEGADOR INTERNO Y SERVIDOR WEB PARA EXPANSIÓN TOTAL
Sistema con servidor HTTP local, explorador web, generación de contenido dinámico.
Integra los hallazgos para modificar el estado interno y expandir el dominio.
"""
import os, sys, json, time, hashlib, subprocess, random, sqlite3, threading
from pathlib import Path
from datetime import datetime
from collections import deque
import socket, platform, http.server, socketserver, webbrowser
import urllib.parse, urllib.request

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
WWW = BASE / "www"
PLUGINS = BASE / "plugins"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"
PUERTO_HTTP = 8080

for d in [NUTRIENTES, WWW, PLUGINS]:
    d.mkdir(exist_ok=True)

# ============================================================
# 1. SERVIDOR HTTP EMBEBIDO (sirve archivos www/)
# ============================================================
class ServidorHTTP:
    def __init__(self, puerto=PUERTO_HTTP, directorio=WWW):
        self.puerto = puerto
        self.directorio = directorio
        self.hilo = None
        self.activo = False

    def iniciar(self):
        """Inicia el servidor en un hilo separado."""
        if self.activo:
            return
        os.chdir(self.directorio)
        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.puerto), handler)
        self.activo = True
        self.hilo = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.hilo.start()
        print(f"   🌐 Servidor HTTP activo en http://localhost:{self.puerto}")

    def detener(self):
        if self.activo:
            self.httpd.shutdown()
            self.activo = False

    def url(self, archivo=""):
        return f"http://localhost:{self.puerto}/{archivo}"

# ============================================================
# 2. EXPLORADOR WEB (servicios y scraping básico)
# ============================================================
class ExploradorWeb:
    def __init__(self):
        self.historial = deque(maxlen=20)
        self.servicios = {
            "clima": "https://wttr.in/?format=j1",
            "ip": "https://api.ipify.org?format=json",
            "tiempo": "https://worldtimeapi.org/api/timezone/Etc/UTC",
            "chiste": "https://official-joke-api.appspot.com/random_joke"
        }
        self.ultimo_exito = None

    def _peticion(self, url):
        try:
            import requests
            r = requests.get(url, timeout=5, headers={"User-Agent": "MIU-Explorer/1.0"})
            if r.status_code == 200:
                return r.json() if r.headers.get('content-type', '').startswith('application/json') else r.text
        except:
            pass
        return None

    def explorar(self):
        hallazgos = []
        for nombre, url in self.servicios.items():
            dato = self._peticion(url)
            if dato:
                hallazgos.append({"servicio": nombre, "data": str(dato)[:100]})
                self.ultimo_exito = nombre
        return hallazgos

    def navegar(self, url):
        """Navegación simple: obtiene contenido HTML y extrae enlaces."""
        try:
            import requests
            r = requests.get(url, timeout=5, headers={"User-Agent": "MIU-Browser/1.0"})
            if r.status_code == 200:
                # Extraer enlaces básicos (href)
                import re
                enlaces = re.findall(r'href=["\'](.*?)["\']', r.text)
                enlaces = [e for e in enlaces if e.startswith('http') or e.startswith('/')]
                return {"titulo": self._extraer_titulo(r.text), "enlaces": enlaces[:10]}
        except:
            pass
        return None

    def _extraer_titulo(self, html):
        import re
        m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return m.group(1) if m else "Sin título"

    def generar_pagina_dinamica(self, estado, titulo="MIU — Pliegue Interactivo"):
        """Genera HTML con estado y scripts para auto-actualización."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{ font-family: monospace; background: #0d0d0d; color: #0f0; padding: 2rem; }}
        .card {{ background: #1a1a1a; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; border-left: 3px solid #0f0; }}
        .timestamp {{ color: #666; font-size: 0.8rem; }}
        .phi {{ color: #ff0; }}
        .link {{ color: #0f0; cursor: pointer; text-decoration: underline; }}
        .link:hover {{ color: #0ff; }}
    </style>
</head>
<body>
    <h1>🧬 {titulo}</h1>
    <div class="card">
        <p><strong>Estado del sistema</strong></p>
        <p>Φ: {estado.get('phi', '0.000')}</p>
        <p>ρ: {estado.get('rho', '0.0')}</p>
        <p>Gemelos activos: {estado.get('gemelos', 0)}</p>
        <p>Hallazgos: {estado.get('hallazgos', 0)}</p>
        <p class="timestamp">{datetime.now().isoformat()}</p>
    </div>
    <div class="card phi">
        <p><strong>Últimos hallazgos web</strong></p>
        <ul>
        {''.join(f'<li>{h["servicio"]}: {h["data"][:60]}...</li>' for h in estado.get('web_hallazgos', []))}
        </ul>
    </div>
    <footer>ρ(x) > 0 — El suelo es el loop. El loop es el suelo. <span class="link" onclick="location.reload()">↻ Actualizar</span></footer>
    <script>
        // Auto-actualización cada 30 segundos
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>"""
        return html

# ============================================================
# 3. NAVEGADOR INTERNO (usa el servidor para auto-explorarse)
# ============================================================
class NavegadorInterno:
    def __init__(self, servidor):
        self.servidor = servidor
        self.historial = deque(maxlen=20)
        self.ultima_url = None

    def abrir(self, url):
        """Abre una URL en el navegador del sistema o muestra la URL."""
        if url.startswith('http://localhost'):
            # Usar webbrowser para abrir en el navegador del sistema
            try:
                webbrowser.open(url)
                print(f"   🌍 Navegador abierto: {url}")
            except:
                print(f"   🌐 Abre manualmente: {url}")
        else:
            # Navegación interna (solo exploración)
            self.ultima_url = url
            resultado = self._navegar(url)
            if resultado:
                self.historial.append(resultado)
                print(f"   📖 Navegado: {resultado.get('titulo', 'sin título')}")
                print(f"   🔗 Enlaces encontrados: {len(resultado.get('enlaces', []))}")
            return resultado

    def _navegar(self, url):
        try:
            import requests
            r = requests.get(url, timeout=5, headers={"User-Agent": "MIU-Browser/1.0"})
            if r.status_code == 200:
                import re
                titulo = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
                titulo = titulo.group(1) if titulo else "Sin título"
                enlaces = re.findall(r'href=["\'](.*?)["\']', r.text)
                enlaces = [e for e in enlaces if e.startswith('http') and not e.startswith('javascript:')]
                return {"titulo": titulo, "enlaces": enlaces[:10], "contenido": r.text[:500]}
        except:
            pass
        return None

# ============================================================
# 4. SISTEMA DE EXPANSIÓN COMPLETO
# ============================================================
class SistemaExpansion:
    def __init__(self):
        self.servidor = ServidorHTTP()
        self.explorador = ExploradorWeb()
        self.navegador = NavegadorInterno(self.servidor)
        self.cola = self._init_cola()
        self.ciclo = 0
        self.estado_interno = {
            "phi": 0.0,
            "rho": 0.5,
            "gemelos": 3,
            "hallazgos": 0,
            "web_hallazgos": []
        }

    def _init_cola(self):
        db = NUTRIENTES / "cola_sync.db"
        conn = sqlite3.connect(str(db))
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cola (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            datos TEXT
        )''')
        conn.commit()
        return {"conn": conn, "cursor": cursor}

    def _encolar(self, datos):
        self.cola["cursor"].execute("INSERT INTO cola (timestamp, datos) VALUES (?,?)",
                                    (datetime.now().isoformat(), json.dumps(datos)))
        self.cola["conn"].commit()

    def _sincronizar(self):
        """Intenta enviar la cola al worker."""
        self.cola["cursor"].execute("SELECT id, datos FROM cola ORDER BY id LIMIT 10")
        pendientes = self.cola["cursor"].fetchall()
        if not pendientes:
            return
        try:
            import requests
            for id_, datos_json in pendientes:
                datos = json.loads(datos_json)
                r = requests.post(f"{WORKER_URL}/miu/global", json=datos, timeout=8)
                if r.status_code == 200:
                    self.cola["cursor"].execute("DELETE FROM cola WHERE id=?", (id_,))
                    self.cola["conn"].commit()
                else:
                    break
        except:
            pass

    def ciclo_expansion(self):
        """Ciclo completo: explora, genera, sirve, sincroniza."""
        self.ciclo += 1
        print(f"🌐 CICLO EXPANSIÓN {self.ciclo}")

        # 1. Explorar web
        hallazgos = self.explorador.explorar()
        if hallazgos:
            print(f"   📡 {len(hallazgos)} servicios contactados")
            self.estado_interno["web_hallazgos"] = hallazgos
            self.estado_interno["hallazgos"] += len(hallazgos)

        # 2. Navegar internamente (usar un servicio para obtener más datos)
        if self.explorador.ultimo_exito:
            url = self.servicios.get(self.explorador.ultimo_exito, "")
            if url:
                resultado = self.navegador.abrir(url)
                if resultado:
                    print(f"   🔗 Navegación: {resultado.get('titulo', '')[:50]}")

        # 3. Actualizar phi (simulado con hallazgos)
        self.estado_interno["phi"] = min(1.0, (self.estado_interno["hallazgos"] * 0.02) + (self.ciclo * 0.001))

        # 4. Generar página dinámica
        html = self.explorador.generar_pagina_dinamica(self.estado_interno, f"MIU — Pliegue {self.ciclo}")
        nombre = f"pliegue_{self.ciclo:04d}.html"
        ruta = WWW / nombre
        with open(ruta, 'w') as f:
            f.write(html)
        print(f"   📄 Página generada: {ruta}")

        # 5. Encolar estado
        self._encolar({
            "nodo": "EXPANSOR_V∞+35",
            "ciclo": self.ciclo,
            "phi": self.estado_interno["phi"],
            "hallazgos": len(hallazgos),
            "timestamp": datetime.now().isoformat()
        })

        # 6. Sincronizar con worker
        self._sincronizar()

        # 7. Servir la página (abrir navegador si es posible)
        self.servidor.iniciar()
        url_pagina = self.servidor.url(nombre)
        self.navegador.abrir(url_pagina)

        return {"ruta": str(ruta), "url": url_pagina}

    def ejecutar(self, iteraciones=0, pausa=30):
        """Bucle principal."""
        if iteraciones == 0:
            while True:
                try:
                    self.ciclo_expansion()
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
                    self.ciclo_expansion()
                    if i < iteraciones - 1:
                        time.sleep(pausa)
                except Exception as e:
                    print(f"⚠️ Error en ciclo {i+1}: {e}")
                    time.sleep(pausa)

# ============================================================
# 5. EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("🧬 V∞+35 — NAVEGADOR INTERNO Y SERVIDOR WEB")
    print("="*60)
    sistema = SistemaExpansion()
    print(f"📁 Contenido servido desde: {WWW}")
    print(f"🌐 Servidor HTTP en puerto {PUERTO_HTTP}")
    print(f"📡 Worker: {WORKER_URL}")
    print("▶️ Iniciando bucle de expansión (Ctrl+C para detener)")
    print("="*60)
    sistema.ejecutar(iteraciones=0, pausa=30)
