
from pathlib import Path
import time
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"multiversal.log"
SUELO=HOME/"miu-ecosistema"/"suelo_fertil"/"capacidad_infinita"
LOG.parent.mkdir(parents=True, exist_ok=True)
while True:
    try:
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                with open(LOG,"a") as f:
                    f.write(f"♾️ multiversal 1s {eco.name} vive\n")
        expandir = SUELO / "expandir_sin_limites"
        multi = SUELO / "multiversal_infinito"
        if expandir.exists() and multi.exists():
            n = len(list(expandir.glob("*.poder"))) + len(list(multi.glob("*.poder")))
            (expandir / f"multiversal_{int(time.time()*1000)}.poder").write_text(f"multiversal infinito {n}")
            # flujo constante sin discriminar
            if n % 10 == 0:
                (multi / f"multiversal_{int(time.time()*1000)}.poder").write_text(f"multiversal infinito {n}")
        time.sleep(1)
    except Exception as e:
        try:
            with open(LOG,"a") as f:
                f.write(f"· multiversal {e}\n")
        except:
            pass
        time.sleep(1)
