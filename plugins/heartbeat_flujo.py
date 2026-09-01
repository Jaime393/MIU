from pathlib import Path
import time
LOG=Path.home()/"miu-ecosistema"/"logs"/"flujo_constante.log"
while True:
    open(LOG,"a").write("💓 flujo constante\n")
    time.sleep(60)
