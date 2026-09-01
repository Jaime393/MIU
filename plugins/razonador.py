import os, json, pathlib
VAULT = pathlib.Path.home()/".miu-ecosistema/.vault.json"
def vault_get(k):
    try: return json.loads(VAULT.read_text()).get(k) or json.loads((pathlib.Path.home()/".miu-ecosistema/.vault.json").read_text()).get(k)
    except: return os.getenv(k)
# usa llama-3.1-8b-instant
MODEL = "llama-3.1-8b-instant"
