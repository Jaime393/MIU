#!/usr/bin/env python3
"""
MIU V∞+30 — CAZADOR DE RECURSOS (CR-01)
Busca tokens, scripts y configuraciones en repositorios, foros y fuentes públicas.
"""
import os, sys, json, re, time, requests, subprocess, sqlite3
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, quote_plus

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "cazador.log"
ENV_FILE = MIU_DIR / ".env"
TOKENS_DB = MIU_DIR / "nutrientes" / "tokens_encontrados.json"
RECURSOS_DB = MIU_DIR / "nutrientes" / "recursos_cazados.json"

# ============================================================
# PATRONES DE BÚSQUEDA
# ============================================================
PATRONES = {
    "github_token": r'ghp_[a-zA-Z0-9]{36}',
    "groq_token": r'gsk_[a-zA-Z0-9]{32,}',
    "openrouter_token": r'sk-or-v1-[a-zA-Z0-9_-]{40,}',
    "cloudflare_token": r'cf(at|k)_[a-zA-Z0-9]{20,}',
    "telegram_token": r'[0-9]{8,10}:[a-zA-Z0-9_-]{35}',
    "openai_token": r'sk-[a-zA-Z0-9]{20,}',
    "huggingface_token": r'hf_[a-zA-Z0-9]{20,}',
    "api_key_general": r'[a-zA-Z0-9_-]{25,}',
    "aws_key": r'AKIA[0-9A-Z]{16}',
    "claude_token": r'sk-ant-api03-[a-zA-Z0-9_-]{40,}',
}

# ============================================================
# FUENTES A ESCANEAR (expansible)
# ============================================================
FUENTES = {
    "github_search": [
        "https://api.github.com/search/code?q=extension:env+token",
        "https://api.github.com/search/code?q=extension:json+api_key",
        "https://api.github.com/search/code?q=GITHUB_TOKEN+extension:env",
        "https://api.github.com/search/code?q=GROQ_TOKEN+extension:env",
        "https://api.github.com/search/code?q=OPENROUTER_TOKEN+extension:env",
        "https://api.github.com/search/code?q=CLOUDFLARE_TOKEN+extension:env",
    ],
    "pastebin": [
        "https://pastebin.com/archive",
        "https://psbdmp.ws/api/v3/dumps/latest",
    ],
    "foros": [
        "https://www.reddit.com/r/learnprogramming/search.json?q=api+key",
        "https://www.reddit.com/r/learnpython/search.json?q=token",
        "https://stackoverflow.com/search?q=api+key+free",
    ],
    "repositorios_locales": [
        str(MIU_DIR / "repos"),
        str(MIU_DIR / "FranBot"),
        str(MIU_DIR / "/storage/"),
    ]
}

# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🔍 {msg}")

def buscar_en_github(query):
    """Busca en GitHub usando la API"""
    resultados = []
    url = f"https://api.github.com/search/code?q={quote_plus(query)}&per_page=30"
    try:
        r = requests.get(url, headers={"Accept": "application/json"}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("items", []):
                if item.get("repository", {}).get("full_name"):
                    resultados.append({
                        "fuente": "github",
                        "repositorio": item["repository"]["full_name"],
                        "archivo": item["path"],
                        "url": item["html_url"],
                        "score": item.get("score", 0),
                    })
        else:
            log(f"   GitHub error: {r.status_code}")
    except Exception as e:
        log(f"   GitHub excepción: {e}")
    return resultados

def buscar_en_pastebin():
    """Busca en Pastebin (simulado, ya que requiere API key)"""
    # En producción, usar la API real de Pastebin con clave propia
    return []

def buscar_en_foros():
    """Busca en foros (simulado)"""
    return []

def buscar_en_repositorios_locales():
    """Busca en repositorios locales (SD, repos clonados)"""
    resultados = []
    for ruta in FUENTES["repositorios_locales"]:
        path = Path(ruta)
        if not path.exists():
            continue
        log(f"📁 Escaneando {path.name}...")
        archivos = list(path.rglob("*.env")) + list(path.rglob("*.json")) + list(path.rglob("*.txt")) + list(path.rglob("*.cfg"))
        for archivo in archivos[:20]:  # Limitar para no saturar
            try:
                contenido = archivo.read_text(errors='ignore')
                for nombre, patron in PATRONES.items():
                    for match in re.findall(patron, contenido):
                        resultados.append({
                            "fuente": "local",
                            "archivo": str(archivo),
                            "tipo": nombre,
                            "token": match,
                            "preview": match[:12] + "..." + match[-4:],
                        })
            except:
                pass
    return resultados

def extraer_tokens_de_resultados(resultados):
    """Extrae tokens de los resultados de búsqueda"""
    tokens = []
    for r in resultados:
        if "token" in r:
            tokens.append(r)
        elif "archivo" in r and "contenido" not in r:
            # Intentar leer el archivo remoto (GitHub)
            if r.get("url"):
                try:
                    raw_url = r["url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                    response = requests.get(raw_url, timeout=10)
                    if response.status_code == 200:
                        contenido = response.text
                        for nombre, patron in PATRONES.items():
                            for match in re.findall(patron, contenido):
                                tokens.append({
                                    "fuente": r.get("fuente", "desconocida"),
                                    "repositorio": r.get("repositorio", ""),
                                    "archivo": r.get("archivo", ""),
                                    "tipo": nombre,
                                    "token": match,
                                    "preview": match[:12] + "..." + match[-4:],
                                })
                except:
                    pass
    return tokens

def validar_y_guardar_tokens(tokens):
    """Valida los tokens encontrados y los guarda en la base de datos"""
    if not tokens:
        return []
    
    # Cargar tokens existentes para evitar duplicados
    existentes = set()
    if TOKENS_DB.exists():
        with open(TOKENS_DB) as f:
            for t in json.load(f):
                existentes.add(t.get("token", ""))
    
    nuevos = []
    for t in tokens:
        if t["token"] not in existentes:
            nuevos.append(t)
            existentes.add(t["token"])
    
    if nuevos:
        # Guardar en la base de datos
        with open(TOKENS_DB, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
        data.extend(nuevos)
        with open(TOKENS_DB, "w") as f:
            json.dump(data, f, indent=2)
        
        # También guardar en el archivo de recursos cazados
        with open(RECURSOS_DB, "w") as f:
            json.dump({"timestamp": datetime.now().isoformat(), "nuevos": nuevos}, f, indent=2)
        
        log(f"✅ {len(nuevos)} nuevos tokens encontrados y guardados")
    else:
        log("ℹ️ No se encontraron tokens nuevos")
    
    return nuevos

def run(args=None):
    log("🔍 INICIANDO CAZADOR DE RECURSOS (CR-01)")
    log("🌐 Buscando en repositorios públicos...")
    
    todos_resultados = []
    
    # 1. GitHub
    log("📡 GitHub:")
    for query in FUENTES["github_search"][:3]:  # Limitar para no saturar
        resultados = buscar_en_github(query)
        if resultados:
            log(f"   ✅ {len(resultados)} resultados en {query.split('=')[-1][:30]}")
            todos_resultados.extend(resultados)
        else:
            log(f"   ❌ Sin resultados en {query.split('=')[-1][:30]}")
    
    # 2. Repositorios locales
    log("📁 Repositorios locales:")
    resultados = buscar_en_repositorios_locales()
    if resultados:
        log(f"   ✅ {len(resultados)} tokens en repositorios locales")
        todos_resultados.extend(resultados)
    else:
        log("   ❌ Sin tokens en repositorios locales")
    
    # 3. Extraer tokens de los resultados
    log("🔎 Extrayendo tokens de los resultados...")
    tokens = extraer_tokens_de_resultados(todos_resultados)
    
    # 4. Validar y guardar
    nuevos = validar_y_guardar_tokens(tokens)
    
    # 5. Resumen
    log("=" * 50)
    log(f"✅ Nuevos tokens encontrados: {len(nuevos)}")
    for t in nuevos[:5]:
        log(f"   • {t.get('tipo', 'desconocido')}: {t['preview']} ({t.get('fuente', 'desconocida')})")
    if len(nuevos) > 5:
        log(f"   ... y {len(nuevos)-5} más")
    log("=" * 50)
    
    return {"nuevos": len(nuevos), "tokens": nuevos[:10]}

if __name__ == "__main__":
    print(run())
