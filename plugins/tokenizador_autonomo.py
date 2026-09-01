#!/usr/bin/env python3
"""
MIU V∞+30 — TOKENIZADOR AUTÓNOMO
Busca, renueva y extrae tokens de Cloudflare usando navegadores headless
y recursos locales. No requiere interacción manual.
"""
import os, sys, json, time, re, subprocess, glob, shutil, socket
from pathlib import Path
from datetime import datetime, timedelta
import requests

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
BROWSER_DIRS = [
    Path("/data/data/com.termux/files/usr/share/firefox-esr"),
    Path("/data/data/com.termux/files/usr/share/chromium"),
    Path("/data/data/com.termux/files/usr/share/brave"),
]
HOME = Path("os.path.expanduser('~')")
VAULT = BASE / ".vault.json"
TOKEN_PATTERN = re.compile(r'cfut_[A-Za-z0-9_-]{30,}')
EMAIL = "jaimep.viccente@gmail.com"
PASSWORD = "la misma clave"  # Se obtendrá de .vault.json

# ============================================================
# 1. RASTREADOR DE TOKENS EN EL SISTEMA
# ============================================================
class RastreadorTokens:
    def __init__(self):
        self.tokens = set()
        self.cookies = {}

    def escanear_archivos(self):
        """Busca tokens en archivos del sistema."""
        print("🔍 Escaneando archivos en busca de tokens...")
        patron = re.compile(r'cfut_[A-Za-z0-9_-]{30,}')
        for ruta in HOME.glob("**/*"):
            try:
                if ruta.is_file() and ruta.stat().st_size < 1024*1024:
                    if 'cfut' in ruta.name or ruta.suffix in ['.json', '.txt', '.env', '.conf', '.log', '.vault']:
                        texto = ruta.read_text(errors='ignore')
                        tokens = patron.findall(texto)
                        for t in tokens:
                            self.tokens.add(t)
                            print(f"   ✅ Token encontrado en {ruta.name}")
            except:
                pass
        # Buscar en /storage/emulated/0 (SD)
        sd = Path("/storage/emulated/0")
        if sd.exists():
            for ruta in sd.glob("**/*.json"):
                try:
                    texto = ruta.read_text(errors='ignore')
                    tokens = patron.findall(texto)
                    for t in tokens:
                        self.tokens.add(t)
                        print(f"   ✅ Token encontrado en {ruta.name}")
                except:
                    pass
        return self.tokens

    def extraer_de_navegadores(self):
        """Extrae tokens de cookies y sesiones de navegadores."""
        print("🌐 Extrayendo tokens de navegadores...")
        for navegador in BROWSER_DIRS:
            if navegador.exists():
                # Buscar archivos de cookies o sesiones
                for archivo in navegador.glob("**/*.sqlite"):
                    try:
                        if "cookies" in archivo.name.lower():
                            # Usar sqlite3 para leer cookies
                            cmd = ["sqlite3", str(archivo), "SELECT host, name, value FROM moz_cookies WHERE name LIKE '%cfut%';"]
                            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                            for line in result.stdout.split('\n'):
                                if 'cfut_' in line:
                                    tokens = re.findall(r'cfut_[A-Za-z0-9_-]{30,}', line)
                                    for t in tokens:
                                        self.tokens.add(t)
                                        print(f"   ✅ Token extraído de cookie en {navegador.name}")
                    except:
                        pass
        return self.tokens

# ============================================================
# 2. AUTENTICACIÓN CON NAVEGADOR HEADLESS
# ============================================================
class AutenticadorHeadless:
    def __init__(self):
        self.navegador_path = self._encontrar_navegador()
        self.cookies_file = BASE / "cookies.json"

    def _encontrar_navegador(self):
        """Busca un navegador headless disponible."""
        # Intentar con chromium
        for cmd in ["chromium", "chromium-browser", "google-chrome", "firefox"]:
            ruta = shutil.which(cmd)
            if ruta:
                return ruta
        return None

    def autenticar(self, email, password):
        """Usa un navegador headless para autenticarse en Cloudflare."""
        if not self.navegador_path:
            print("⚠️ No se encontró navegador headless. Usando fallback.")
            return None

        print(f"🌐 Autenticando con {os.path.basename(self.navegador_path)}...")
        # Crear un script de Puppeteer/Playwright simple (usando Node)
        script_js = f"""
        const puppeteer = require('puppeteer-core');
        (async () => {{
            const browser = await puppeteer.launch({{
                executablePath: '{self.navegador_path}',
                headless: true,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }});
            const page = await browser.newPage();
            await page.goto('https://dash.cloudflare.com/login');
            await page.type('input[name="email"]', '{email}');
            await page.type('input[name="password"]', '{password}');
            await page.click('button[type="submit"]');
            await page.waitForNavigation();
            // Extraer cookies y tokens
            const cookies = await page.cookies();
            const token = await page.evaluate(() => {{
                // Buscar cfut_ en localStorage o cookies
                for (let key of Object.keys(localStorage)) {{
                    if (key.includes('cfut_')) return localStorage[key];
                }}
                return null;
            }});
            console.log(JSON.stringify({{cookies, token}}));
            await browser.close();
        }})();
        """
        script_path = BASE / "auth_script.js"
        with open(script_path, 'w') as f:
            f.write(script_js)

        try:
            result = subprocess.run(
                ["node", str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('token'):
                    return data['token']
                # Buscar en cookies
                for cookie in data.get('cookies', []):
                    if 'cfut_' in cookie.get('value', ''):
                        return cookie['value']
            return None
        except Exception as e:
            print(f"⚠️ Error en autenticación: {e}")
            return None

# ============================================================
# 3. FALLBACK: SOLICITUD DIRECTA A CLOUDFLARE API
# ============================================================
class AutenticadorAPI:
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD

    def obtener_token(self):
        """Usa la API de Cloudflare para obtener un token (fallback)."""
        print("🔑 Solicitando token a Cloudflare API...")
        url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
        # Intentar con credenciales de correo (requiere API Key)
        try:
            # Obtener API Key de .vault.json
            with open(VAULT, 'r') as f:
                vault = json.load(f)
            api_key = vault.get('cloudflare_api_key') or vault.get('api_key')
            if api_key:
                headers = {"Authorization": f"Bearer {api_key}"}
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('success'):
                        print("✅ Token verificado con API Key")
                        return api_key
        except:
            pass

        # Si no hay API Key, intentar con email+password (menos seguro)
        print("⚠️ Usando autenticación por email+password...")
        try:
            login_url = "https://dash.cloudflare.com/api/v4/login"
            data = {"email": self.email, "password": self.password}
            r = requests.post(login_url, json=data, timeout=15)
            if r.status_code == 200:
                cookies = r.cookies.get_dict()
                for key, value in cookies.items():
                    if 'cfut_' in value:
                        return value
        except:
            pass
        return None

# ============================================================
# 4. ORQUESTADOR DE TOKENS
# ============================================================
class OrquestadorTokens:
    def __init__(self):
        self.tokens = set()
        self.activos = []

    def recopilar_tokens(self):
        """Recopila tokens de todas las fuentes."""
        print("🧬 Recopilando tokens...")
        # 1. Escanear archivos
        rastreador = RastreadorTokens()
        self.tokens.update(rastreador.escanear_archivos())
        self.tokens.update(rastreador.extraer_de_navegadores())

        # 2. Si no hay tokens, autenticar
        if not self.tokens:
            print("⚠️ No se encontraron tokens. Intentando autenticación...")
            headless = AutenticadorHeadless()
            token = headless.autenticar(EMAIL, PASSWORD)
            if token:
                self.tokens.add(token)
                print(f"✅ Token obtenido por autenticación headless")

        # 3. Fallback a API
        if not self.tokens:
            print("⚠️ Fallback a API...")
            api = AutenticadorAPI()
            token = api.obtener_token()
            if token:
                self.tokens.add(token)
                print(f"✅ Token obtenido por API")

        # 4. Guardar tokens en .vault.json
        if self.tokens:
            try:
                with open(VAULT, 'r') as f:
                    vault = json.load(f)
            except:
                vault = {}
            vault['cfut_tokens'] = list(self.tokens)
            vault['last_update'] = datetime.now().isoformat()
            with open(VAULT, 'w') as f:
                json.dump(vault, f, indent=2)
            print(f"📦 {len(self.tokens)} tokens guardados en .vault.json")

        # 5. Verificar tokens (probar uno)
        for token in self.tokens:
            if self._verificar_token(token):
                self.activos.append(token)
                print(f"✅ Token activo: {token[:15]}...")
                return token

        print("❌ No se encontraron tokens válidos")
        return None

    def _verificar_token(self, token):
        """Verifica si un token es válido."""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            r = requests.get("https://api.cloudflare.com/client/v4/user", headers=headers, timeout=10)
            return r.status_code == 200
        except:
            return False

# ============================================================
# 5. EJECUCIÓN Y CICLO PERPETUO
# ============================================================
def ciclo_tokenizador():
    """Ciclo de renovación de tokens cada 24 horas."""
    print("="*60)
    print("🧬 V∞+30 — TOKENIZADOR AUTÓNOMO")
    print("="*60)
    orquestador = OrquestadorTokens()
    token = orquestador.recopilar_tokens()
    if token:
        print(f"✅ Token activo: {token[:15]}...")
        print(f"📦 Tokens totales: {len(orquestador.tokens)}")
        print(f"💾 Guardado en {VAULT}")
    else:
        print("❌ No se pudo obtener ningún token válido")
    print("="*60)
    return token

if __name__ == "__main__":
    # Ejecutar en bucle con pausa (24h)
    import time
    while True:
        try:
            ciclo_tokenizador()
            print("⏳ Próxima recopilación en 24 horas...")
            time.sleep(86400)  # 24 horas
        except KeyboardInterrupt:
            print("⏹️ Interrumpido")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(3600)  # 1 hora si falla
