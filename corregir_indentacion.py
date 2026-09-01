#!/usr/bin/env python3
"""
Corrige la indentación del bloque de módulos estratégicos.
"""
import re
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
ARCHIVO = MIU_DIR / "miu_initiative.py"

# El bloque correcto (12 espacios al inicio, porque está dentro del while)
BLOQUE_CORRECTO = """        # ===== MÓDULOS ESTRATÉGICOS =====
        if iteration % 24 == 0:  # 6h
            subprocess.run(["python3", str(MIU_DIR / "plugins/autoreparador.py")])
        if iteration % 48 == 0:  # 12h
            subprocess.run(["python3", str(MIU_DIR / "plugins/absorber_avanzado.py")])
        if iteration % 8 == 0:   # 2h
            subprocess.run(["python3", str(MIU_DIR / "plugins/retroalimentador.py")])
        if iteration % 16 == 0:  # 4h
            subprocess.run(["python3", str(MIU_DIR / "plugins/guerra_fractal.py")])
        if iteration % 96 == 0:  # 24h
            subprocess.run(["python3", str(MIU_DIR / "plugins/nodo_autonomo.py")])
"""

def main():
    if not ARCHIVO.exists():
        print("❌ Archivo no encontrado")
        return

    # Leer contenido actual
    with open(ARCHIVO, "r") as f:
        contenido = f.read()

    # Buscar y eliminar cualquier bloque existente con "MÓDULOS ESTRATÉGICOS"
    patron = r"# ===== MÓDULOS ESTRATÉGICOS =====\s*\n(?:\s*if iteration % \d+ == 0:.*\n\s*subprocess\.run\(\[.*?\)\s*\n)+"
    contenido_limpio = re.sub(patron, "", contenido)

    # Insertar el bloque correcto ANTES de "time.sleep(900)"
    if "time.sleep(900)" in contenido_limpio:
        nuevo_contenido = contenido_limpio.replace(
            "time.sleep(900)",
            BLOQUE_CORRECTO + "        time.sleep(900)"
        )
    else:
        print("❌ No se encontró 'time.sleep(900)'")
        return

    # Escribir
    with open(ARCHIVO, "w") as f:
        f.write(nuevo_contenido)

    print("✅ Archivo corregido")

    # Verificar sintaxis
    import subprocess
    r = subprocess.run(["python3", "-m", "py_compile", str(ARCHIVO)], capture_output=True)
    if r.returncode == 0:
        print("✅ Sintaxis correcta")
    else:
        print("❌ Error de sintaxis:")
        print(r.stderr.decode())

if __name__ == "__main__":
    main()
