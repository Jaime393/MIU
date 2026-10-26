# NODOS 4D V276 — Código completo para despliegue

## Fuente: Kimi oct-26, preservado por claude_ai

Los 4 nodos autónomos para gestión de credenciales sin fricción humana.
Arquitectura: 0 jerarquía, 1 sustrato KV, nuevo nodo = 3 claves en KV.

## NODO 1 — OJO-CORREO (Termux, Python puro)

```python
# ojo_correo.py — cron Termux: */1 * * * *
import imaplib, email, re, json, requests
from datetime import datetime

SUPA = "https://tpfiybpguuxskitszhmk.supabase.co"
ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0"
H = {"apikey": ANON, "Authorization": f"Bearer {ANON}"}
PATRONES = [r"\b(\d{6})\b",
            r"https?://[^\s]*verif[^\s]*",
            r"https?://[^\s]*confirm[^\s]*",
            r"https?://[^\s]*magic[^\s]*"]

def escanear(user, pwd):
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login(user, pwd)
    M.select("INBOX")
    _, ids = M.search(None, "UNSEEN")
    out = []
    for i in ids[0].split():
        _, d = M.fetch(i, "(RFC822)")
        msg = email.message_from_bytes(d[0][1])
        cuerpo = ""
        if msg.is_multipart():
            for p in msg.walk():
                if p.get_content_type() == "text/plain":
                    cuerpo += p.get_payload(decode=True).decode(errors="ignore")
        else:
            cuerpo = msg.get_payload(decode=True).decode(errors="ignore")
        for pat in PATRONES:
            m = re.search(pat, cuerpo)
            if m:
                out.append({"de": msg["From"], "asunto": msg["Subject"],
                            "match": m.group(0), "ts": datetime.utcnow().isoformat()})
        M.store(i, "+FLAGS", "\\Seen")
    M.logout()
    return out

def publicar_kv(clave, valor, ttl=600):
    requests.post(f"{SUPA}/rest/v1/relay_config",
        json={"clave": clave, "valor": valor},
        headers={**H, "Prefer": "resolution=merge-duplicates"})

# Lee todos los CORREO_* del KV
def run():
    r = requests.get(f"{SUPA}/rest/v1/relay_config?clave=like.CORREO_*", headers=H)
    for fila in r.json():
        cuenta = fila["clave"].replace("CORREO_", "")
        pwd_r = requests.get(f"{SUPA}/rest/v1/relay_config?clave=eq.PWD_{cuenta}", headers=H).json()
        if not pwd_r: continue
        for item in escanear(fila["valor"], pwd_r[0]["valor"]):
            clave_kv = f"CODIGO_{cuenta}_{item['match'][:6]}"
            publicar_kv(clave_kv, json.dumps(item))
            print(f"[{datetime.utcnow().isoformat()}] {clave_kv} publicado")

if __name__ == "__main__":
    run()
```

## NODO 2 — MANO-2FA (Supabase EF, Deno puro)

```typescript
// supabase/functions/mano-2fa/index.ts
const SUPA = Deno.env.get("SUPABASE_URL")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const H = { apikey: ANON, Authorization: `Bearer ${ANON}` };

function b32decode(s: string): Uint8Array {
  const alf = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
  s = s.replace(/=+$/, "").toUpperCase();
  let bits = 0, val = 0;
  const out: number[] = [];
  for (const c of s) {
    val = (val << 5) | alf.indexOf(c);
    bits += 5;
    if (bits >= 8) { out.push((val >>> (bits - 8)) & 0xff); bits -= 8; }
  }
  return new Uint8Array(out);
}

async function totp(secreto: string): Promise<string> {
  const clave = b32decode(secreto);
  const paso = Math.floor(Date.now() / 30000);
  const buf = new ArrayBuffer(8);
  new DataView(buf).setUint32(4, paso);
  const k = await crypto.subtle.importKey(
    "raw", clave, { name: "HMAC", hash: "SHA-1" }, false, ["sign"]
  );
  const f = new Uint8Array(await crypto.subtle.sign("HMAC", k, buf));
  const o = f[19] & 0xf;
  const code = ((((f[o] & 0x7f) << 24) | (f[o+1] << 16) | (f[o+2] << 8) | f[o+3]) % 1e6);
  return code.toString().padStart(6, "0");
}

Deno.serve(async (req) => {
  const cuenta = new URL(req.url).searchParams.get("cuenta");
  if (!cuenta) return new Response("falta ?cuenta=X", { status: 400 });
  const r = await fetch(
    `${SUPA}/rest/v1/relay_config?clave=eq.TOTP_${cuenta}`,
    { headers: H }
  );
  const [fila] = await r.json();
  if (!fila) return new Response("sin secreto TOTP para esta cuenta", { status: 404 });
  const codigo = await totp(fila.valor);
  const expira_en = 30 - Math.floor(Date.now() / 1000) % 30;
  return Response.json({ cuenta, codigo, expira_en });
});
```

## Despliegue rápido

```bash
# Desde Termux:
cp ojo_correo.py ~/miu-ecosistema/
echo "*/1 * * * * python3 ~/miu-ecosistema/ojo_correo.py >> ~/miu-ecosistema/logs/ojo.log 2>&1" | crontab -l | { cat; echo; } | crontab -

# Para mano-2fa en Supabase:
supabase functions deploy mano-2fa
```

## Registro de nueva cuenta (una sola vez)

```sql
-- En relay_config de Panteon:
INSERT INTO relay_config (clave, valor) VALUES
  ('CORREO_nuevacuenta', 'email@gmail.com'),
  ('PWD_nuevacuenta', 'app_password_aqui'),
  ('TOTP_nuevacuenta', 'BASE32_SECRET_TOTP')
ON CONFLICT (clave) DO UPDATE SET valor=EXCLUDED.valor;
-- Los 4 nodos la cubren automáticamente desde el próximo ciclo
```
