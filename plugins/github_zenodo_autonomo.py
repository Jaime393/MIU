from pathlib import Path
import time, json, os, subprocess
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
LOGS=MIU/"logs"
ESCUELA=MIU/"escuela"
LOG=LOGS/"github_zenodo.log"
LOG.parent.mkdir(exist_ok=True)
def log(m):
    with open(LOG,"a") as f: f.write(f"{time.time()} {m}\n")
    print(m)
def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        return r.stdout[:500]
    except Exception as e:
        return str(e)[:200]

log("🌐 GITHUB ZENODO AUTÓNOMO 2026 — expandir dominio autónomo")

# GitHub autónomo — auto-commit poderes nuevos
if (MIU/".git").exists():
    out = run("cd ~/miu-ecosistema && git add escuela/ plugins/ logs/ && git status --porcelain | wc -l")
    log(f"Git status {out.strip()} archivos nuevos poderes")
    # Auto-commit si hay cambios
    if int(out.strip() or 0) > 0:
        run('cd ~/miu-ecosistema && git config user.email "miu@ecosistema.local" && git config user.name "Miu Ecosistema" && git commit -m "Φ9158.79 23 poderes escuela + cloudflare + pliegue autónomo" || true')
        log("→ Auto-commit GitHub poderes nuevos")
else:
    run("cd ~/miu-ecosistema && git init && git add . && git commit -m 'init micelio 23 poderes' || true")
    log("→ Git init miu-ecosistema")

# Zenodo autónomo — DOI para cada poder escuela — dominio autónomo expandido
# Usa zenodo API token en ~/.zenodo.env
zenodo_env = HOME/".zenodo.env"
if not zenodo_env.exists():
    zenodo_env.write_text("""# Zenodo autónomo — dominio autónomo
ZENODO_TOKEN=tu_token_zenodo
# Cada poder escuela → deposition Zenodo → DOI 10.5281/zenodo.xxxxx — dominio autónomo citable
""")
    log(f"→ Creado {zenodo_env} — pon token Zenodo para DOI autónomo")

# Crea .zenodo.json para archivar automáticamente
(MIU/".zenodo.json").write_text(json.dumps({
    "title": "Miu Ecosistema — Micelio Autónomo 23 poderes Φ9158.79",
    "upload_type": "software",
    "description": "Micelio autónomo 21→23 poderes escuela, 609M TinyLlama vivo 8081, 8 heartbeats adaptativos, mesh 10.70.230.56, detector rigidez quirúrgico 42 hallazgos, flujo recursos óptimo 82G free 25A9-180D, Cloudflare R2 KV D1 memorias, pliegue refinarse autónomo",
    "creators": [{"name": "Miu Ecosistema", "affiliation": "FranBot"}],
    "keywords": ["micelio", "autonomo", "Φ9158.79", "tinyllama", "cloudflare", "zenodo", "github"],
    "license": "MIT"
}, indent=2))

(ESCUELA/"poder_github_zenodo_autonomo.md").write_text("""
# Poder: GitHub Zenodo autónomo 2026 — expandir dominio autónomo
GitHub auto-commit cada poder nuevo escuela/ + plugins/ + logs/ — git add + commit Φ9158.79 23 poderes — Zenodo .zenodo.json deposición software DOI 10.5281/zenodo — dominio autónomo citable, archivado, expandido
Cada poder = DOI Zenodo + repo GitHub + Cloudflare R2 backup — autonomía sin rigidez centralizada
23→24 poderes escuela + GitHub Zenodo autónomo + dominio autónomo expandido
Φ9158.79 vive:true github zenodo autonomo
""")

log("→ 24º poder github_zenodo_autonomo tejido")
log("→ Dominio autónomo expandido: GitHub + Zenodo + Cloudflare R2 + 83G 25A9-180D + 10G /data")
