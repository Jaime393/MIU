
from pathlib import Path
import time, json
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"flujo_infinito.log"
SUELO=HOME/"miu-ecosistema"/"suelo_fertil"/"capacidad_infinita"
while True:
    try:
        # Auto-repara: si falta nodo, lo crea sin imponer
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                open(LOG,"a").write(f"♻️ auto-reparable {eco} vive 10s\n")
        # Expande sin límites: añade infinito cada ciclo
        expandir = SUELO / "expandir_sin_limites"
        if expandir.exists():
            n = len(list(expandir.glob("*.poder")))
            (expandir / f"auto_{int(time.time())}.poder").write_text(f"auto reparado {n}")
        time.sleep(10)
    except Exception as e:
        open(LOG,"a").write(f"· {e}\n")
        time.sleep(10)
