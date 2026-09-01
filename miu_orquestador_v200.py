#!/usr/bin/env python3
import os, sys, json, pathlib, platform, shutil, subprocess

MIU = pathlib.Path.home() / "miu-ecosistema"
VAULT = MIU / ".vault.json"

def detect_env():
    env = {}
    env["is_termux"] = "com.termux" in os.environ.get("PREFIX","")
    env["is_proot"] = pathlib.Path("/.dockerenv").exists()
    env["has_git"] = shutil.which("git") is not None
    env["has_node"] = shutil.which("node") is not None
    env["can_api"] = shutil.which("termux-open-url") is not None
    env["is_kimi"] = pathlib.Path("/mnt/agents/output").exists()
    print(f"ENV: {env}")
    return env

def vault_set(k,v):
    data = {}
    if VAULT.exists():
        try: data = json.loads(VAULT.read_text())
        except: pass
    data[k]=v
    VAULT.write_text(json.dumps(data, indent=2))
    print(f"vault {k} guardado")

def vault_get(k):
    if not VAULT.exists(): return None
    try: return json.loads(VAULT.read_text()).get(k)
    except: return None

def relay_upload(fp):
    import requests
    fp = pathlib.Path(fp)
    try:
        with open(fp,'rb') as f:
            r = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}, timeout=30)
            if r.ok:
                url = r.json()["data"]["url"]
                print(f"OK tmpfiles -> {url}")
                vault_set("last_relay", url)
                return url
    except Exception as e:
        print(f"FAIL tmpfiles {e}")
    return None

def browser_open(url):
    env = detect_env()
    if env["is_termux"] and env["can_api"]:
        subprocess.run(["termux-open-url", url])
    else:
        subprocess.run(["am","start","-a","android.intent.action.VIEW","-d",url])

if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:]).lower()
    detect_env()
    if "drive" in cmd:
        relay_upload(MIU / "nutrientes/informe_global.json")
    elif "navegador" in cmd or "console" in cmd:
        browser_open("https://console.cloud.google.com")
    elif "status" in cmd:
        print("V200 listo. Comandos: drive, navegador, status")
    else:
        print("Uso: python3 miu_orquestador_v200.py [drive|navegador|status]")

def legado_panel():
    import pathlib, json
    p=pathlib.Path.home()/ "miu-ecosistema/inventario_legado.json"
    if p.exists():
        d=json.loads(p.read_text())
        print(f"Legado: {len(d.get('dashboards',[]))} dashboards, {len(d.get('scripts',[]))} scripts")
