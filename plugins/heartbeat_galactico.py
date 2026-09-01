from pathlib import Path
import time
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"galactico.log"
SUELO=HOME/"miu-ecosistema"/"suelo_fertil"/"capacidad_infinita"
LOG.parent.mkdir(parents=True, exist_ok=True)
while True:
    try:
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                with open(LOG,"a") as f:
                    f.write(f"🌌 galáctico 5s {eco.name} vive\n")
        expandir = SUELO / "expandir_sin_limites"
        if expandir.exists():
            n = len(list(expandir.glob("*.poder")))
            # absoluto flexible: timestamp sin límite
            (expandir / f"galactico_{int(time.time())}.poder").write_text(f"galáctico infinito {n}")
        time.sleep(5)
    except Exception as e:
        try:
            with open(LOG,"a") as f:
                f.write(f"· galáctico {e}\n")
        except:
            pass
        time.sleep(5)
