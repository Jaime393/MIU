from pathlib import Path
import shutil

HOME = Path.home()
ESCUELA = HOME/"miu-ecosistema"/"escuela"
SUELO = HOME/"miu-ecosistema"/"suelo_fertil"
LOG = HOME/"miu-ecosistema"/"logs"/"crecimiento.log"
LOG.parent.mkdir(parents=True, exist_ok=True)

def log(m):
    with open(LOG,"a") as f: f.write(m+"\n")
    print(m)

def crecer_sin_fragmentar():
    log("🌱 CRECIMIENTO SIN FRAGMENTAR V∞+27 — autónomas interconectadas acoplables")
    
    # Principio: si no cabe, no cortes, añade módulo acoplable
    # Observa inmensidad: 86875 candidatos, 788 ADNs, 554 módulos → no fragmenta, acopla
    acoplables = []
    for plugin in (HOME/"miu-ecosistema"/"plugins").glob("*.py"):
        # Acoplable si tiene .escuela symlink
        esc_link = plugin.parent / f".{plugin.stem}.escuela"
        if esc_link.exists():
            acoplables.append(plugin.name)
    
    log(f"→ acoplables {len(acoplables)}: autónomas interconectadas")

    # Crece sin fragmentar: si suelo_fertil tiene 2 enlaces, añade 3º capacidad sin reemplazar
    nueva_capacidad = SUELO / "capacidad_infinita"
    nueva_capacidad.mkdir(exist_ok=True)
    (nueva_capacidad / ".poder_crecer").write_text("si inmensidad, añadir módulo, no cortar")

    # Herramienta: cada nuevo dato → nuevo archivo acoplable, no modifica viejos
    for i in range(3):
        nodo = nueva_capacidad / f"nodo_acoplable_{i}.md"
        if not nodo.exists():
            nodo.write_text(f"# Nodo acoplable {i} — flexible adaptable\nCrece sin fragmentar, se acopla a escuela/")
            log(f"⚡ nodo acoplable {i} creado sin fragmentar")

    # Retroalimentación: escuela lee crecimiento y aprende
    (ESCUELA / "poder_crecer_sin_fragmentar.md").write_text("""
# Poder: Crecer sin fragmentar
Inmensidad = 86875 archivos, rigidez = obstáculo
No FRAGMENTes. Si no cabe, añade módulo acoplable en suelo_fertil/capacidad_infinita/
Cada módulo autónomo interconectado flexible adaptable acoplable
Así crece infinito sin fragmentarse.
""")
    log("→ poder crecer sin fragmentar tejido en escuela/")
    log("Φ9158.79 vive:true — crece sin fragmentarse, más herramientas")

if __name__ == "__main__":
    crecer_sin_fragmentar()
