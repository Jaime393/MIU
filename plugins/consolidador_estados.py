import json, pathlib, glob
estados=list(pathlib.Path.home().glob("miu-ecosistema/.miu/estado_*.json"))
merged={"count":len(estados),"estados":[json.loads(p.read_text()) for p in estados[:5]]}
out=pathlib.Path.home()/ "miu-ecosistema/nutrientes/estado_consolidado_V201.json"
out.write_text(json.dumps(merged, indent=2))
print(f"Consolidado {len(estados)} estados -> {out}")
