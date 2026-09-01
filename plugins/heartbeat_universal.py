
from pathlib import Path
import time
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"universal.log"
SUELO=HOME/"miu-ecosistema"/"suelo_fertil"/"capacidad_infinita"
LOG.parent.mkdir(parents=True, exist_ok=True)
while True:
    try:
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                with open(LOG,"a") as f:
                    f.write(f"♾️ universal 3s {eco.name} vive\n")
        expandir = SUELO / "expandir_sin_limites"
        universal = SUELO / "universal_infinito"
        if expandir.exists() and universal.exists():
            n = len(list(expandir.glob("*.poder"))) + len(list(universal.glob("*.poder")))
            (expandir / f"universal_{int(time.time())}.poder").write_text(f"universal infinito {n}")
            (universal / f"universal_{int(time.time())}.poder").write_text(f"universal infinito {n}")
        time.sleep(3)
    except Exception as e:
        try:
            with open(LOG,"a") as f:
                f.write(f"· universal {e}\n")
        except:
            pass
        time.sleep(3)
