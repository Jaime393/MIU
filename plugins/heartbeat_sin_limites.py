
from pathlib import Path
import time
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"orquestador_sin_limites.log"
while True:
    try:
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                open(LOG,"a").write(f"🌌 orquestador sin límites {eco} vive\n")
        time.sleep(15)
    except Exception as e:
        open(LOG,"a").write(f"· {e}\n")
        time.sleep(15)
