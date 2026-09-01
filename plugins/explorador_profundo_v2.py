#!/usr/bin/env python3
import socket, json, pathlib, datetime
BASE = pathlib.Path.home() / "miu-ecosistema/nutrientes"
BASE.mkdir(parents=True, exist_ok=True)

def scan_real():
    # solo puertos locales reales, no /24 entera
    puertos = [5000,8080,3000,8000]
    activos=[]
    for p in puertos:
        s=socket.socket()
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1",p))==0:
            activos.append(p)
        s.close()
    inv={"timestamp":datetime.datetime.now().isoformat(),"puertos_locales":activos,"nota":"V38 v2 sin falsos 254, solo localhost"}
    (BASE/"inventario_global_v2.json").write_text(json.dumps(inv, indent=2))
    print(f"V38 v2: puertos activos {activos}")

if __name__=="__main__":
    scan_real()
