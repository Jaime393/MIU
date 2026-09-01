#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTOCURADOR V1 — Cirujano autónomo de código MIU
Lee autodiagnostico.json, aplica fixes automáticos, hace backup.
NUNCA modifica sin backup. NUNCA toca .env, secrets, o git internals.
"""
import os, json, shutil, re
from pathlib import Path
from datetime import datetime

MIU_DIR = Path(os.environ.get("MIU_DIR", "os.path.expanduser('~')/miu-ecosistema"))
BACKUP_DIR = MIU_DIR / "_backups" / "autocurador"
REPORTE = MIU_DIR / "nutrientes" / "autodiagnostico.json"
LOG = MIU_DIR / "nutrientes" / "autocurador.log"

def log(msg):
    print(f"🔧 {msg}")
    with open(LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def backup(archivo: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / f"{archivo.name}.{ts}.bak"
    shutil.copy2(archivo, dest)
    return dest

aplicados = 0
saltados = 0

if not REPORTE.exists():
    log("No hay reporte de autodiagnostico. Correr autodiagnostico primero.")
    print("🧬 {'ok': False, 'razon': 'sin_reporte'}")
    exit(0)

with open(REPORTE) as f:
    data = json.load(f)

for h in data.get("hallazgos", []):
    tipo = h["tipo"]
    archivo = Path(h["archivo"])
    linea = h.get("linea", 0)
    fix = h.get("fix_sugerido")
    sev = h.get("severidad", "media")

    # No tocar ciertos archivos
    if any(x in str(archivo) for x in [".env", "secrets", "config", "backup", ".git"]):
        log(f"⏭️ Saltado (protegido): {archivo}")
        saltados += 1
        continue

    if not archivo.exists():
        log(f"⏭️ No existe: {archivo}")
        saltados += 1
        continue

    try:
        lines = archivo.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as e:
        log(f"❌ No se puede leer {archivo}: {e}")
        saltados += 1
        continue

    modificado = False
    new_lines = lines[:]

    # ── FIX: /tmp/ → $TMPDIR o MIU_DIR/temp ──
    if tipo == "path_hardcodeado" and "_tmp/" in h["detalle"]:
        tmp_replacement = os.environ.get("TMPDIR", str(MIU_DIR / "temp"))
        for i, ln in enumerate(new_lines):
            if "_tmp/" in ln and not ln.strip().startswith("#"):
                new_lines[i] = ln.replace("_tmp/", tmp_replacement + "/")
                modificado = True
                log(f"✅ {archivo}:{i+1} _tmp/ → {tmp_replacement}/")

    # ── FIX: SyntaxError por línea de continuación mal escapada ──
    elif tipo == "syntax_error" and linea > 0:
        idx = linea - 1
        if idx < len(new_lines):
            bad = new_lines[idx]
            if bad.rstrip().endswith("\\") and len(bad.rstrip()) > 1:
                new_lines[idx] = bad.rstrip()[:-1]
                modificado = True
                log(f"✅ {archivo}:{linea} corregido escape de línea")
            elif 'chr(34)' in bad and ('\\"' in bad or bad.count('"') % 2 != 0):
                new_lines[idx] = bad.replace('chr(34)', '"').replace('\\"', '"')
                modificado = True
                log(f"✅ {archivo}:{linea} normalizado chr(34)")

    # ── FIX: path absoluto Termux → os.path.expanduser('~') ──
    elif tipo == "path_hardcodeado" and "termux" in h["detalle"].lower():
        home = str(Path.home())
        for i, ln in enumerate(new_lines):
            if home in ln and not ln.strip().startswith("#"):
                new_lines[i] = ln.replace(home, "os.path.expanduser('~')")
                if "import os" not in "\n".join(new_lines[:10]):
                    new_lines.insert(0, "import os  # autocurador")
                modificado = True
                log(f"✅ {archivo}:{i+1} path absoluto → os.path.expanduser('~')")

    # ── FIX: Import roto → agregar a requirements pendientes ──
    elif tipo == "import_roto":
        req_file = MIU_DIR / "requirements_pendientes.txt"
        mod = re.search(r"No se puede importar: (\w+)", h["detalle"])
        if mod:
            with open(req_file, "a+") as rf:
                rf.seek(0)
                if mod.group(1) not in rf.read():
                    rf.write(f"{mod.group(1)}\n")
                    log(f"📦 {mod.group(1)} agregado a requirements_pendientes.txt")

    # ── FIX: Directorio faltante ──
    elif tipo == "dir_faltante":
        Path(h["archivo"]).mkdir(parents=True, exist_ok=True)
        log(f"📁 Creado: {h['archivo']}")
        modificado = True

    # Guardar si hubo cambios
    if modificado:
        backup(archivo)
        archivo.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        aplicados += 1
    else:
        saltados += 1

log(f"Resumen: {aplicados} fixes aplicados, {saltados} saltados")
print(f"🧬 {{'ok': True, 'aplicados': {aplicados}, 'saltados': {saltados}}}")
