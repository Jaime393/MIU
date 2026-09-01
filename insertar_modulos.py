#!/usr/bin/env python3
"""
Inserta los módulos estratégicos en miu_initiative.py
con la indentación correcta.
"""
import re
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
ARCHIVO = MIU_DIR / "miu_initiative.py"
BACKUP = ARCHIVO.with_suffix(".py.bak6")

# El bloque a insertar (con indentación correcta)
BLOQUE = """
        # ===== MÓDULOS ESTRATÉGICOS =====
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
        print("❌ miu_initiative.py no encontrado")
        return

    # Backup
    ARCHIVO.rename(BACKUP)
    print(f"✅ Backup creado: {BACKUP.name}")

    # Leer el contenido original
    with open(BACKUP, "r") as f:
        contenido = f.read()

    # Buscar la línea "time.sleep(900)" y insertar el bloque justo antes
    patron = r"(\s*)time\.sleep\(900\)"
    match = re.search(patron, contenido)
    if not match:
        print("❌ No se encontró 'time.sleep(900)'. ¿El archivo está completo?")
        return

    # Insertar el bloque antes de time.sleep(900)
    nuevo_contenido = re.sub(
        patron,
        BLOQUE + "\n        " + match.group(1) + "time.sleep(900)",
        contenido
    )

    # Escribir el archivo modificado
    with open(ARCHIVO, "w") as f:
        f.write(nuevo_contenido)

    print("✅ miu_initiative.py actualizado correctamente")

    # Verificar sintaxis
    import subprocess
    r = subprocess.run(["python3", "-m", "py_compile", str(ARCHIVO)], capture_output=True)
    if r.returncode == 0:
        print("✅ Sintaxis correcta")
    else:
        print("❌ Error de sintaxis. Revisa el archivo.")
        print(r.stderr.decode())

if __name__ == "__main__":
    main()
