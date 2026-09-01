#!/usr/bin/env python3
"""
MIU V201 — AUTOREPARADOR LIGERO
Versión que no se cuelga. Solo escanea sintaxis, no ejecuta fixes complejos.
"""
import os, json, time
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
CRITICAL = ["miu_control.py", "miu_shell.py", "miu_initiative.py", "miu_scanner.py", "miu_doctor.py"]

def log(msg):
    print(f"🔧 {msg}")

def check_syntax(path):
    try:
        with open(path) as f:
            code = f.read()
        compile(code, path, "exec")
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def main():
    log("🧬 AUTOREPARADOR V201 — Escaneo rápido")
    log("=" * 40)
    reparados = []
    for fname in CRITICAL:
        path = MIU_DIR / fname
        if path.exists():
            ok, detail = check_syntax(path)
            status = "✅" if ok else "❌"
            log(f"   {status} {fname}: {detail}")
            if not ok and "indent" in detail.lower():
                try:
                    with open(path) as f:
                        lines = f.readlines()
                    fixed = [line.replace("\t", "    ").rstrip() + "\n" for line in lines]
                    backup = MIU_DIR / "backups" / f"{fname}.bak"
                    backup.parent.mkdir(exist_ok=True)
                    with open(backup, "w") as f:
                        f.writelines(lines)
                    with open(path, "w") as f:
                        f.writelines(fixed)
                    log(f"      🔧 Indentación corregida (backup en {backup})")
                    reparados.append(fname)
                except Exception as e:
                    log(f"      ❌ No se pudo reparar: {e}")
        else:
            log(f"   ❌ {fname}: NO EXISTE")
    log("=" * 40)
    log(f"✅ Escaneo completado. Reparados: {len(reparados)}")
    return {"reparados": reparados}

if __name__ == "__main__":
    main()
