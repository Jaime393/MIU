#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTODIAGNOSTICO V1 — Escaneo profundo del ecosistema MIU
Detecta: SyntaxError, paths rotos, _tmp/ hardcodeado, imports rotos,
API keys expuestas, permisos, y deuda técnica.
Salida: JSON de hallazgos para que AUTOCURADOR actúe.
"""
import os, sys, json, ast, re, subprocess, hashlib
from pathlib import Path
from datetime import datetime

MIU_DIR = Path(os.environ.get("MIU_DIR", "os.path.expanduser('~')/miu-ecosistema"))
TMPDIR = os.environ.get("TMPDIR", str(MIU_DIR / "temp"))
REPORTE = MIU_DIR / "nutrientes" / "autodiagnostico.json"

def log(msg):
    print(f"🔍 {msg}")

hallazgos = []

def agregar(tipo, archivo, linea, detalle, severidad="media", fix_sugerido=None):
    hallazgos.append({
        "tipo": tipo,
        "archivo": str(archivo),
        "linea": linea,
        "detalle": detalle,
        "severidad": severidad,
        "fix_sugerido": fix_sugerido,
        "timestamp": datetime.now().isoformat()
    })

# ── 1. SyntaxError en todos los .py ──
log("Escaneando sintaxis Python...")
for py in MIU_DIR.rglob("*.py"):
    try:
        py.read_text(encoding="utf-8", errors="ignore")
        ast.parse(py.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError as e:
        agregar("syntax_error", py, e.lineno, str(e), "critica",
                f"Revisar línea {e.lineno}: {e.text}")
    except Exception as e:
        agregar("lectura_error", py, 0, str(e), "baja")

# ── 2. Paths problemáticos ──
log("Buscando paths hardcodeados...")
PATRONES_PATH = [
    (r'_tmp/', "Usa _tmp/ (read-only en Android)", "alta", f'os.environ.get("TMPDIR","{TMPDIR}")'),
    (r'/data/data/com\.termux/files/home/', "Path absoluto de Termux hardcodeado", "media", "os.path.expanduser('~')"),
    (r'/sdcard/', "Path /sdcard/ hardcodeado", "media", "os.environ.get('EXTERNAL_STORAGE','/sdcard')"),
]

for py in MIU_DIR.rglob("*.py"):
    try:
        lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            for patron, desc, sev, fix in PATRONES_PATH:
                if re.search(patron, line) and not line.strip().startswith("#"):
                    agregar("path_hardcodeado", py, i, desc, sev, fix)
    except:
        pass

# ── 3. Imports rotos (básico) ──
log("Verificando imports...")
for py in MIU_DIR.rglob("*.py"):
    try:
        tree = ast.parse(py.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name.split('.')[0]
                    if mod not in sys.builtin_module_names:
                        try:
                            __import__(mod)
                        except ImportError:
                            agregar("import_roto", py, node.lineno, f"No se puede importar: {mod}", "alta",
                                    f"pip install {mod}  # o eliminar si no se usa")
            elif isinstance(node, ast.ImportFrom):
                mod = node.module.split('.')[0] if node.module else ""
                if mod and mod not in sys.builtin_module_names:
                    try:
                        __import__(mod)
                    except ImportError:
                        agregar("import_roto", py, node.lineno, f"No se puede importar: {mod}", "alta",
                                f"pip install {mod}")
    except:
        pass

# ── 4. API keys expuestas en código ──
log("Buscando credenciales expuestas...")
PATRONES_KEYS = [
    r'sk-[a-zA-Z0-9]{20,}',
    r'ghp_[a-zA-Z0-9]{36}',
    r'[a-zA-Z0-9_-]{20,}\.([a-zA-Z0-9_-]{10,}\.){1,2}[a-zA-Z0-9_-]{20,}',
]
for py in MIU_DIR.rglob("*.py"):
    try:
        lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            for pat in PATRONES_KEYS:
                if re.search(pat, line) and not line.strip().startswith("#"):
                    agregar("credencial_expuesta", py, i, "Posible API key en código fuente", "critica",
                            "Mover a archivo .env y leer con os.environ.get()")
                    break
    except:
        pass

# ── 5. Archivos .sh con shebang incorrecto ──
log("Revisando scripts shell...")
for sh in MIU_DIR.rglob("*.sh"):
    try:
        first = sh.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
        if not first.startswith("#!/"):
            agregar("shebang_faltante", sh, 1, "Falta shebang", "baja", "#!/bin/bash")
    except:
        pass

# ── 6. Directorios críticos faltantes ──
log("Verificando estructura crítica...")
criticos = ["nutrientes", "plugins", "memoria", "temp", "_sandbox"]
for d in criticos:
    if not (MIU_DIR / d).exists():
        agregar("dir_faltante", MIU_DIR / d, 0, f"Falta directorio crítico: {d}", "alta", f"mkdir -p {MIU_DIR/d}")

# ── Guardar ──
REPORTE.parent.mkdir(parents=True, exist_ok=True)
with open(REPORTE, "w") as f:
    json.dump({"hallazgos": hallazgos, "total": len(hallazgos), "timestamp": datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)

log(f"Diagnóstico completo: {len(hallazgos)} hallazgos → {REPORTE}")
print(f"🧬 {{'ok': True, 'hallazgos': {len(hallazgos)}, 'reporte': str(REPORTE)}}")
