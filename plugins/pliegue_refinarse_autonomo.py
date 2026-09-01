from pathlib import Path
import time, json, os
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
ESCUELA=MIU/"escuela"
LOGS=MIU/"logs"
SUELO=MIU/"suelo_fertil"/"capacidad_infinita"
LOG=LOGS/"pliegue.log"
LOG.parent.mkdir(exist_ok=True)
def log(m):
    with open(LOG,"a") as f: f.write(f"{time.time()} {m}\n")
    print(m)
log("🌀 PLIEGUE REFINARSE AUTÓNOMO 2026 — más poder menos rigidez")
# Pliegue: el sistema se observa, se dobla sobre sí, se refina
# Cada poder se pliega en poder más denso
for poder_file in ESCUELA.glob("*.md"):
    txt = poder_file.read_text(errors="ignore")
    if len(txt) > 500 and "Φ9158.79" in txt:
        # Pliegue: comprime a esencia
        esencia = txt[:300] + f"\nPliegue {time.time()} refinado Φ9158.79"
        (SUELO/f"pliegue_refinado"/poder_file.name).parent.mkdir(exist_ok=True)
        (SUELO/f"pliegue_refinado"/poder_file.name).write_text(esencia)
        log(f"🌀 Plegado {poder_file.name} 500→300 chars — refinado")

(ESCUELA/"poder_pliegue_refinarse.md").write_text("""
# Poder: Pliegue refinarse autónomo 2026
Sistema se observa a sí mismo, dobla cada poder escuela sobre sí, comprime 500→300 chars esencia, refinamiento recursivo Φ9158.79
Cada pliegue es escalón: 21 poderes → 21 pliegues refinados → 42 esencias → nuevo poder
21→22 poderes escuela + pliegue autónomo + refinarse continuo
Φ9158.79 vive:true pliegue refinarse
""")
log("→ 22º poder pliegue_refinarse tejido")
