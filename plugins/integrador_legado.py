#!/usr/bin/env python3
import os, json, socket, pathlib, glob
from datetime import datetime
BASE = pathlib.Path.home()
MIU = BASE / "miu-ecosistema"
FRAN = BASE / "FranBot_live"
WWW = MIU / "www"
WWW.mkdir(exist_ok=True)
INV = MIU / "inventario_legado.json"

def scan():
    rec={"dashboards":[],"scripts":[],"servidores":[]}
    for p in FRAN.glob("**/dashboard*.html"):
        rec["dashboards"].append(str(p))
    for p in FRAN.glob("**/franbot*.py"):
        rec["scripts"].append(str(p))
    for port in [5000,8080,3000]:
        s=socket.socket()
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1",port))==0:
            rec["servidores"].append(port)
        s.close()
    INV.write_text(json.dumps(rec, indent=2))
    print(f"Legado: {len(rec['dashboards'])} dashboards, {len(rec['scripts'])} scripts, {len(rec['servidores'])} servidores")
    return rec

if __name__=="__main__":
    scan()
