#!/usr/bin/env python3
import os, pathlib
MIU_DIR=pathlib.Path.home()/ "miu-ecosistema"
def run_cmd(c):
    import subprocess
    try:
        r=subprocess.run(c, shell=True, capture_output=True, text=True, timeout=10)
        return {"ok": r.returncode==0, "out": r.stdout[:500], "err": r.stderr[:500]}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def menu():
    print("🧬 MIU CONTROL V201.3 - Menu")
    print("1: status  2: drive  3: navegador  9: shell  0: salir")
    c=input("> ").strip()
    if c=="1":
        print(run_cmd("python3 miu_orquestador_v200.py status")["out"])
    elif c=="2":
        print(run_cmd("python3 miu_orquestador_v200.py drive")["out"])
    elif c=="3":
        print(run_cmd("python3 miu_orquestador_v200.py navegador")["out"])
    elif c=="9":
        os.system("bash")
    elif c=="10":
        print("Telegram deshabilitado V201.3 - fix IndentationError")
    else:
        print("salir")
        
if __name__=="__main__":
    menu()
