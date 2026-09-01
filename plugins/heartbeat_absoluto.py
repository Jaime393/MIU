
from pathlib import Path
import time, shutil
HOME=Path.home()
LOG=HOME/"miu-ecosistema"/"logs"/"flujo_absoluto.log"
while True:
    try:
        # absoluto sin discriminar: prueba /data y /storage
        for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("str(Path.home()/".."/".."/"storage"/"25A9-180D"/"FranBot")")]:
            if eco.exists():
                open(LOG,"a").write(f"💓 montón {eco} retroalimenta\n")
        time.sleep(30)
    except Exception as e:
        open(LOG,"a").write(f"· {e}\n")
        time.sleep(30)
