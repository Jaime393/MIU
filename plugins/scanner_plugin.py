import os  # autocurador
#!/usr/bin/env python3
"""
Plugin: scanner_plugin
Ejecuta el escáner del ecosistema y devuelve resumen.
"""
import subprocess
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def run(args=None):
    r = subprocess.run(["python3", str(MIU_DIR / "miu_scanner.py")], 
                     capture_output=True, text=True, timeout=60, cwd=MIU_DIR)
    lines = r.stdout.split("\n")
    # Extraer resumen
    summary = []
    capture = False
    for line in lines:
        if "MAP" in line:
            capture = True
        if capture:
            summary.append(line)
        if "=" in line and capture and len(summary) > 15:
            break
    return "\\n".join(summary) if summary else r.stdout[:1000]

if __name__ == "__main__":
    print(run())
