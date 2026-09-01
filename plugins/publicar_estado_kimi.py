#!/usr/bin/env python3
import os, json, subprocess
from pathlib import Path
from datetime import datetime, timezone
REPO = Path("os.path.expanduser('~')/FranBot")
WWW = REPO / "www"
SRC = Path("os.path.expanduser('~')/miu-ecosistema/nutrientes/estado_para_kimi.json")
def publicar():
    if not SRC.exists() or not REPO.exists():
        return False
    WWW.mkdir(parents=True, exist_ok=True)
    with open(SRC) as f:
        data = json.load(f)
    data["_publicado"] = datetime.now(timezone.utc).isoformat()
    with open(WWW / "estado_para_kimi.json", "w") as f:
        json.dump(data, f, indent=2)
    os.chdir(REPO)
    subprocess.run(["git", "add", "www/estado_para_kimi.json"], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"auto {datetime.now().strftime('%H:%M')}"], capture_output=True)
    subprocess.run(["git", "push", "origin", "master"], capture_output=True, timeout=30)
    print("✅ https://jaime393.github.io/FranBot/www/estado_para_kimi.json")
    return True
if __name__ == "__main__":
    publicar()
