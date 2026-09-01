#!/usr/bin/env python3
"""
MIU V∞+25 — EXPANSOR DE TOKENS
Busca claves en cualquier directorio, enlace, SD, descargas.
Modo automático y expansible.
"""
import os, sys, json, re, time, shutil, subprocess, fnmatch
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "expansor.log"
ENV_FILE = MIU_DIR / ".env"
TOKENS_DB = MIU_DIR / "nutrientes" / "tokens_encontrados.json"

# ============================================================
# PATRONES DE TOKENS (expansibles)
# ============================================================
PATRONES = {
    "github": r'ghp_[a-zA-Z0-9]{36}',
    "github_old": r'[a-f0-9]{40}',
    "groq": r'gsk_[a-zA-Z0-9]{32,}',
    "openrouter": r'sk-or-v1-[a-zA-Z0-9]{40,}',
    "cloudflare": r'cf(at|k)_[a-zA-Z0-9]{20,}',
    "scaleway": r'sb_(publishable|secret)_[a-zA-Z0-9]+',
    "telegram": r'[0-9]{8,10}:[a-zA-Z0-9_-]{35}',
    "anthropic": r'sk-ant-api03-[a-zA-Z0-9_-]{40,}',
    "openai": r'sk-[a-zA-Z0-9]{20,}',
    "huggingface": r'hf_[a-zA-Z0-9]{20,}',
    "google": r'AIza[A-Za-z0-9_-]{35}',
    "generic": r'[A-Za-z0-9_-]{25,}',
}

# ============================================================
# DIRECTORIOS A EXPLORAR (expansibles)
# ============================================================
RUTAS_BASE = [
    Path("os.path.expanduser('~')"),
    Path("/storage/emulated/0/Download"),
    Path("/storage/emulated/0/Downloads"),
    Path("/sdcard/Download"),
    Path("/sdcard/Downloads"),
    Path("/storage/25A9-180D"),
    Path("/storage/emulated/0"),
    Path("/sdcard"),
    Path("/data/local/tmp"),
]

# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(f"🧬 {msg}")

def expandir_rutas(rutas):
    """Expande rutas base y añade enlaces simbólicos y subdirectorios comunes"""
    nuevas = []
    for r in rutas:
        if not r.exists():
            continue
        nuevas.append(r)
        # Buscar enlaces simbólicos
        for item in r.glob("*"):
            if item.is_symlink():
                try:
                    target = item.resolve()
                    if target.exists() and target.is_dir():
                        nuevas.append(target)
                except:
                    pass
        # Buscar subdirectorios comunes
        for sub in ["FranBot", "miu-ecosistema", "colmena", "cognitive", "llama.cpp"]:
            for p in r.glob(f"**/{sub}"):
                if p.is_dir() and p not in nuevas:
                    nuevas.append(p)
    # Eliminar duplicados y asegurar que existen
    final = []
    for r in nuevas:
        if r.exists() and r not in final:
            final.append(r)
    return final

def buscar_tokens_en_archivo(ruta):
    """Busca tokens en un archivo dado"""
    encontrados = []
    try:
        contenido = ruta.read_text(errors='ignore')
        for nombre, patron in PATRONES.items():
            for match in re.findall(patron, contenido):
                encontrados.append({
                    "archivo": str(ruta),
                    "tipo": nombre,
                    "token": match,
                    "preview": match[:8] + "..." + match[-4:],
                    "linea": contenido[:1000].find(match)  # aproximado
                })
    except:
        pass
    return encontrados

def buscar_tokens_en_directorio(ruta, max_archivos=200):
    """Busca tokens en todos los archivos de un directorio"""
    resultados = []
    archivos_procesados = 0
    for archivo in ruta.rglob("*"):
        if archivos_procesados > max_archivos:
            break
        if archivo.is_file() and archivo.stat().st_size < 1024*1024:  # <1MB
            ext = archivo.suffix.lower()
            if ext in ['.env', '.json', '.txt', '.cfg', '.conf', '.yml', '.yaml', '.ini', '.key', '.pem']:
                resultados += buscar_tokens_en_archivo(archivo)
                archivos_procesados += 1
    return resultados

def auto_exportar(tokens):
    """Exporta tokens encontrados a un archivo y sugiere añadir al .env"""
    if not tokens:
        return {"ok": False, "msg": "No se encontraron tokens"}
    
    # Guardar en base de datos
    with open(TOKENS_DB, "w") as f:
        json.dump(tokens, f, indent=2)
    
    # Mostrar resumen
    tipos = {}
    for t in tokens:
        tipos[t["tipo"]] = tipos.get(t["tipo"], 0) + 1
    
    log(f"📊 Tokens encontrados: {len(tokens)}")
    for tipo, count in tipos.items():
        log(f"   • {tipo}: {count}")
    
    # Sugerir añadir al .env
    log("💡 Sugerencia: Copia los tokens que quieras a .env")
    return {"ok": True, "total": len(tokens), "tipos": tipos}

def run(args=None):
    log("🔍 INICIANDO EXPANSIÓN DE TOKENS")
    
    # 1. Expandir rutas
    log("📁 Expandiendo rutas de búsqueda...")
    rutas = expandir_rutas(RUTAS_BASE)
    log(f"📍 {len(rutas)} rutas a explorar")
    
    # 2. Buscar tokens
    log("🔎 Buscando tokens...")
    todos = []
    for r in rutas:
        try:
            encontrados = buscar_tokens_en_directorio(r)
            if encontrados:
                log(f"   ✅ {r.name}: {len(encontrados)} tokens")
                todos += encontrados
        except Exception as e:
            log(f"   ⚠️ Error en {r}: {e}")
    
    # 3. Eliminar duplicados (mismo token, mismo tipo)
    vistos = set()
    unicos = []
    for t in todos:
        clave = (t["token"], t["tipo"])
        if clave not in vistos:
            vistos.add(clave)
            unicos.append(t)
    
    # 4. Exportar
    resultado = auto_exportar(unicos)
    
    log("✅ Expansión completada")
    return resultado

if __name__ == "__main__":
    print(run())
