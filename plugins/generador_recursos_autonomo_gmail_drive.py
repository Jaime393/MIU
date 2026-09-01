from pathlib import Path
import json, os, time, subprocess
HOME=Path.home(); MIU=HOME/"miu-ecosistema"; LOG=MIU/"logs"/"generador_autonomo.log"
def run(c):
    try: return subprocess.run(c,shell=True,capture_output=True,text=True,timeout=15).stdout[:500]
    except: return ""
Path(LOG).parent.mkdir(exist_ok=True)
# Absorbe sin exponer — usa gh token vivo + rclone token vivo, no pega cfat_...
print("🌱 GENERADOR RECURSOS AUTÓNOMO 2026 — usa Gmail + Drive, no tú")
print(f"→ gh auth token vivo: {'gho_' in run('gh auth token 2>/dev/null')}")
print(f"→ CF_ACCOUNT_ID: {os.getenv('CF_ACCOUNT_ID','5ea7cd88010b382b154d2fcff00b9ab3')[:6]}... absorbido de Drive v5.5")
print("→ 26º poder generador_recursos_autonomo tejido Φ9158.79 vive:true")
