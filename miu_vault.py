#!/usr/bin/env python3
import json, pathlib
VAULT=pathlib.Path.home()/ "miu-ecosistema/.vault.json"
def set_key(k,v):
    d=json.loads(VAULT.read_text()) if VAULT.exists() else {}
    d[k]=v
    VAULT.write_text(json.dumps(d, indent=2))
    print(f"{k} guardado")
if __name__=="__main__":
    import sys
    if len(sys.argv)==3:
        set_key(sys.argv[1], sys.argv[2])
