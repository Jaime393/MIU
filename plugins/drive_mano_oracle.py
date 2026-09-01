import os  # autocurador
#!/usr/bin/env python3
import requests, pathlib, json
from datetime import datetime

MIU_DIR = pathlib.Path("os.path.expanduser('~')/miu-ecosistema")
FOLDER_ID = "14dw8txLoEIQQPSav9-YAvfuNimW2tAZ8"

def subir_catbox(filepath):
    try:
        with open(filepath, 'rb') as f:
            r = requests.post("https://catbox.moe/user/api.php",
                              data={"reqtype": "fileupload"},
                              files={"fileToUpload": f},
                              timeout=60)
            if r.ok and r.text.startswith("https://"):
                url = r.text.strip()
                print(f"✅ catbox {filepath.name} -> {url}")
                return url
            print(f"❌ catbox {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"❌ catbox error {e}")
    return None

def subir_tmpfiles(filepath):
    try:
        with open(filepath, 'rb') as f:
            r = requests.post("https://tmpfiles.org/api/v1/upload",
                              files={"file": f}, timeout=60)
            if r.ok:
                j = r.json()
                url = j.get("data", {}).get("url")
                if url:
                    print(f"✅ tmpfiles {filepath.name} -> {url}")
                    return url
            print(f"❌ tmpfiles {r.text[:200]}")
    except Exception as e:
        print(f"❌ tmpfiles error {e}")
    return None

def subir(filepath):
    return subir_catbox(filepath) or subir_tmpfiles(filepath)

def run(args=None):
    candidatos = [
        MIU_DIR / "nutrientes" / "informe_global.json",
        MIU_DIR / "nutrientes" / "decision_razonador.txt",
    ]
    urls = {}
    for fp in candidatos:
        if fp.exists():
            u = subir(fp)
            if u:
                urls[fp.name] = u

    out = MIU_DIR / "nutrientes" / "drive_mano_urls.json"
    with open(out, "w") as f:
        json.dump({"timestamp": str(datetime.now()), "folder_id": FOLDER_ID, "urls": urls}, f, indent=2)
    print(f"\n🧬 Guardado: {out}")
    print(f"cat {out}")
    return {"ok": True, "urls": urls}

if __name__ == "__main__":
    print(run())
