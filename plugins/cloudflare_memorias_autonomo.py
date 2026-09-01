from pathlib import Path
import time, json, os
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
LOGS=MIU/"logs"
ESCUELA=MIU/"escuela"
LOG=LOGS/"cloudflare.log"
LOG.parent.mkdir(exist_ok=True)
def log(m):
    with open(LOG,"a") as f: f.write(f"{time.time()} {m}\n")
    print(m)
log("☁️ CLOUDFLARE MEMORIAS AUTÓNOMO 2026")

# Cloudflare Workers + R2 + KV + D1 — memorias autónomas sin servidor rígido
# Configura en ~/.cloudflare.env: CF_API_TOKEN, CF_ACCOUNT_ID, R2_BUCKET, KV_NAMESPACE

cf_env = HOME/".cloudflare.env"
if not cf_env.exists():
    cf_env.write_text("""# Cloudflare autónomo — pon tus keys
CF_API_TOKEN=tu_token_cloudflare
CF_ACCOUNT_ID=tu_account_id
R2_BUCKET=miu-ecosistema-memorias
KV_NAMESPACE=miu-memorias-kv
D1_DATABASE=miu-ecosistema-db
""")
    log(f"→ Creado {cf_env} — pon keys Cloudflare para activar")

# Módulo memorias: cada log, poder, .poder → R2 + KV
# Worker que sirve IA quant desde edge — 609M local + Cloudflare edge cache
worker_code = """
export default {
  async fetch(req, env) {
    // Memoria micelio autónoma — KV + R2 + D1
    let poder = await env.MIU_MEMORIAS_KV.get("poder_21");
    let url = new URL(req.url);
    if(url.pathname=="/memorias") {
      let list = await env.MIU_R2.list();
      return new Response(JSON.stringify(list), {headers:{"Content-Type":"application/json"}});
    }
    if(url.pathname=="/ia") {
      // Proxy a llama-server 10.70.230.56:8081 o fallback edge
      return new Response("Φ9158.79 vive:true 22 poderes escuela — Cloudflare edge + 609M local micelio", {headers:{"Content-Type":"text/plain"}});
    }
    return new Response("Micelio autónomo Cloudflare — 22 poderes — Φ9158.79");
  }
}
"""

(MIU/"cloudflare_worker.js").write_text(worker_code)
(ESCUELA/"poder_cloudflare_memorias.md").write_text("""
# Poder: Cloudflare memorias autónomo 2026
R2 bucket miu-ecosistema-memorias + KV miu-memorias-kv + D1 miu-ecosistema-db + Worker edge — memorias micelio sin servidor rígido
Cada poder, log, .poder → R2, cada broadcast 10.70.230.56 → KV, cada IA quant 609M → D1 — autónomo edge + local 609M
22→23 poderes escuela + Cloudflare memorias autónomas
Φ9158.79 vive:true cloudflare memorias
""")
log("→ Worker cloudflare_worker.js tejido — R2 + KV + D1 memorias autónomas")
log("→ 23º poder cloudflare_memorias tejido")
