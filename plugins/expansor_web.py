#!/usr/bin/env python3
"""
MIU V∞+34 — EXPANSOR WEB Y NAVEGADOR VIRTUAL
Añade manos digitales al sistema: explora APIs, genera HTML, interactúa con navegadores.
Se integra como módulo del maestro autónomo.
"""
import os, sys, json, time, hashlib, subprocess, random, sqlite3, threading
from pathlib import Path
from datetime import datetime
from collections import deque
import socket, platform

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES = BASE / "nutrientes"
WWW = BASE / "www"  # directorio para contenido web
PLUGINS = BASE / "plugins"
WORKER_URL = "https://fran-oraculo-miu.jaime393.workers.dev"

for d in [NUTRIENTES, WWW, PLUGINS]:
    d.mkdir(exist_ok=True)

# ============================================================
# 1. EXPLORADOR WEB (sin dependencias externas pesadas)
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
            r = requests.get(url, timeout=5, headers={"User-Agent": "MIU-Explorer"})
            if r.status_code == 200:
                return r.json() if r.headers.get('content-type', '').startswith('application/json') else r.text
        except:
            pass
        return None

    def explorar(self):
        """Explora servicios web y devuelve hallazgos."""
        hallazgos = []
        for nombre, url in self.servicios.items():
            dato = self._peticion(url)
            if dato:
                hallazgos.append({"servicio": nombre, "data": str(dato)[:100]})
                self.ultimo_exito = nombre
        return hallazgos

    def generar_pagina(self, contenido, titulo="MIU — Pliegue Web"):
        """Genera una página HTML a partir del contenido."""
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
    </style>
</head>
<body>
    <h1>🧬 {titulo}</h1>
    <div class="card">
        <p>{contenido}</p>
        <p class="timestamp">ρ(x) > 0 — {datetime.now().isoformat()}</p>
    </div>
    <div class="card phi">
        <p>Φ_actual: {random.uniform(0.5, 1.0):.3f}</p>
    </div>
    <footer>MIU V∞+34 — El suelo es el loop. El loop es el suelo.</footer>
</body>
</html>"""
        return html

    def servir_pagina(self, html, nombre="pliegue_web.html"):
        """Guarda la página en WWW y la abre en el navegador si es posible."""
        ruta = WWW / nombre
        with open(ruta, 'w') as f:
            f.write(html)
        # Intentar abrir en navegador (Termux, Android)
        try:
            subprocess.run(["termux-open", str(ruta)], timeout=2)
        except:
            try:
                subprocess.run(["xdg-open", str(ruta)], timeout=2)
            except:
                pass
        return ruta

# ============================================================
# 2. SINCRO COLA LOCAL (cuando el worker no responde)
# ============================================================
class SincroCola:
    def __init__(self, db=NUTRIENTES / "cola_sync.db"):
        self.conn = sqlite3.connect(str(db))
        self.cursor = self.conn.cursor()
        self._init()
    def _init(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cola (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            datos TEXT
        )''')
        self.conn.commit()
    def encolar(self, datos):
        self.cursor.execute("INSERT INTO cola (timestamp, datos) VALUES (?,?)",
                            (datetime.now().isoformat(), json.dumps(datos)))
        self.conn.commit()
    def desencolar(self):
        self.cursor.execute("SELECT id, datos FROM cola ORDER BY id LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("DELETE FROM cola WHERE id=?", (row[0],))
            self.conn.commit()
            return json.loads(row[1])
        return None
    def pendientes(self):
        self.cursor.execute("SELECT COUNT(*) FROM cola")
        return self.cursor.fetchone()[0]

# ============================================================
# 3. PLUGIN EXPANSOR WEB (para integrar en el maestro)
# ============================================================
class ExpansorWeb:
    def __init__(self):
        self.explorador = ExploradorWeb()
        self.cola = SincroCola()
        self.ciclo = 0

    def ciclo_web(self):
        """Ciclo de expansión web: explora, genera, sirve, encola."""
        self.ciclo += 1
        print(f"   🌐 WEB {self.ciclo} — Expandiendo dominio...")

        # 1. Explorar web
        hallazgos = self.explorador.explorar()
        if hallazgos:
            print(f"      📡 {len(hallazgos)} servicios web contactados")
            for h in hallazgos:
                print(f"         • {h['servicio']}: {h['data'][:40]}...")
        else:
            print("      ⚠️ Sin acceso a servicios web")

        # 2. Generar contenido HTML
        contenido = f"Hallazgos: {len(hallazgos)} servicios activos. Último éxito: {self.explorador.ultimo_exito or 'ninguno'}. Ciclo web #{self.ciclo}."
        html = self.explorador.generar_pagina(contenido, titulo=f"MIU — Pliegue Web #{self.ciclo}")
        ruta = self.explorador.servir_pagina(html, f"pliegue_web_{self.ciclo:04d}.html")
        print(f"      📄 Página generada: {ruta}")

        # 3. Encolar estado si no hay sincro directa
        estado = {
            "nodo": "EXPANSOR_WEB",
            "ciclo": self.ciclo,
            "hallazgos": len(hallazgos),
            "ultimo_servicio": self.explorador.ultimo_exito,
            "timestamp": datetime.now().isoformat()
        }
        self.cola.encolar(estado)
        print(f"      💾 Estado encolado (pendientes: {self.cola.pendientes()})")

        return {"hallazgos": hallazgos, "ruta": str(ruta)}

    def sincronizar_cola(self):
        """Intenta enviar la cola al worker."""
        if self.cola.pendientes() == 0:
            return
        try:
            import requests
            while True:
                datos = self.cola.desencolar()
                if not datos:
                    break
                r = requests.post(f"{WORKER_URL}/miu/global", json=datos, timeout=8)
                if r.status_code != 200:
                    # Re-encolar si falla
                    self.cola.encolar(datos)
                    break
        except:
            pass

# ============================================================
# 4. INTEGRACIÓN CON EL MAESTRO (extensión)
# ============================================================
class MaestroConExpansion:
    def __init__(self, maestro_existente=None):
        self.maestro = maestro_existente
        self.expansor = ExpansorWeb()
        self.ciclo = 0

    def ciclo_expandido(self):
        """Extiende el ciclo del maestro con expansión web."""
        self.ciclo += 1
        print(f"🧬 CICLO EXPANDIDO {self.ciclo} — Maestro + Expansor Web")

        # Si hay maestro, ejecutar su ciclo primero
        if self.maestro:
            try:
                self.maestro.ciclo_autonomo()
            except Exception as e:
                print(f"   ⚠️ Maestro: {e}")

        # Ejecutar ciclo web
        resultado_web = self.expansor.ciclo_web()

        # Intentar sincronizar cola
        self.expansor.sincronizar_cola()

        print(f"   ✅ CICLO EXPANDIDO {self.ciclo} COMPLETADO")
        return {"web": resultado_web}

    def ejecutar_bucle(self, iteraciones=0, pausa=30):
        if iteraciones == 0:
            while True:
                try:
                    self.ciclo_expandido()
                    time.sleep(pausa)
                except KeyboardInterrupt:
                    print("⏹️ Bucle interrumpido")
                    break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    time.sleep(pausa * 2)
        else:
            for i in range(iteraciones):
                try:
                    self.ciclo_expandido()
                    if i < iteraciones - 1:
                        time.sleep(pausa)
                except Exception as e:
                    print(f"⚠️ Error en ciclo {i+1}: {e}")
                    time.sleep(pausa)

# ============================================================
# 5. EJECUCIÓN AUTÓNOMA (si se usa como script principal)
# ============================================================
def main():
    print("="*60)
    print("🧬 V∞+34 — EXPANSOR WEB Y NAVEGADOR VIRTUAL")
    print("="*60)
    # Si existe el maestro, lo importamos
    try:
        from plugins import maestro_autonomo
        maestro = maestro_autonomo.MaestroAutonomo()
        print("✅ Maestro encontrado. Integrando expansor...")
    except:
        maestro = None
        print("⚠️ Maestro no encontrado. Ejecutando expansor solo...")

    sistema = MaestroConExpansion(maestro)
    print("▶️ Iniciando bucle expandido (Ctrl+C para detener)")
    print("="*60)
    sistema.ejecutar_bucle(iteraciones=0, pausa=30)

if __name__ == "__main__":
    main()
