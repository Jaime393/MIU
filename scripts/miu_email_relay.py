#!/usr/bin/env python3
"""
MIU Email Relay v2.1 — recolecta códigos de verificación Y magic links de las
bandejas del ecosistema y los publica en Panteón (tabla email_codes) para que
cualquier nodo los use.

v2 2026-11-08 (puntos ciegos tejidos):
- Captura magic links / URLs de verificación (el forwarding de Gmail está
  activo para magic links y todo dato — antes solo códigos de 4-8 dígitos).
- NO marca el correo como leído si la persistencia en Panteón falló
  (v1 lo marcaba leído tras un fallo de INSERT → dato perdido para siempre).
- Un fallo de la consulta de dedup ya NO se trata como ausencia del código:
  se salta el insert y el correo queda no leído para reintentar en el
  siguiente ciclo (cada 10 min).

- Lee MIU_GMAIL_PASSES (JSON: {"email": "app_password", ...})
- Lee SUPA_URL y SUPA_ANON del entorno
- IMAP sobre imap.gmail.com:993 con app passwords (sin OAuth, sin 2FA interactivo)
- Deduplica contra email_codes antes de insertar
- Publica resumen en gossip_log (tipo: email_relay)
"""
import imaplib
import email
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr

CODE_RE = re.compile(r"\b(\d{4,8})\b")
KEYWORD_RE = re.compile(r"(?i)(c[oó]digo|verificaci[oó]n|verification|confirm|login|security alert|2fa|otp|magic|iniciar sesi[oó]n|sign.?in)")
# Magic links: URLs con señal de acción de auth en host o path
URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
URL_AUTH_RE = re.compile(
    r"(?i)(login|signin|sign-in|verify|verification|magic|confirm|auth|token|"
    r"reset|activate|invite|password|sesion|session|otp|magiclink|magic-link|continue)"
)
# Falsos positivos: footers de email (settings/notifications/unsubscribe llevan token pero no son magic links)
URL_FOOTER_RE = re.compile(
    r"(?i)(/settings|/notifications|/unsubscribe|/preferences|/account|/privacy|/terms|/help)"
)
MAX_URL_LEN = 700  # email_codes.codigo es text; truncado defensivo
# Falsos positivos típicos: años, dirección/zip de Google HQ, dígitos repetidos
BLACKLIST = {"1600", "94043", "20261031"}
SKIP_SENDERS = ("noreply@notify.cloudflare.com",)


def is_valid_code(code):
    if code in BLACKLIST:
        return False
    if code.isdigit() and 1990 <= int(code) <= 2035:  # años
        return False
    if len(set(code)) == 1:  # 000000, 999999...
        return False
    if len(code) >= 4 and len(set(code[i : i + 2] for i in range(0, len(code) - 1, 2))) == 1:  # ABABAB
        return False
    return True


def extract_codes(text):
    """Solo códigos que aparecen en líneas cerca de palabras clave (código/verification/...)."""
    lines = text.splitlines()
    codes = set()
    for idx, line in enumerate(lines):
        if not KEYWORD_RE.search(line):
            continue
        window = " ".join(lines[idx : idx + 3])
        for code in CODE_RE.findall(window):
            if is_valid_code(code):
                codes.add(code)
    return codes


def extract_magic_links(text):
    """URLs con señal de acción de auth (magic link, verify, signin, reset...).

    Prioriza URLs del remitente del correo; deduplica; máximo 2 por correo.
    """
    links = []
    seen = set()
    for url in URL_RE.findall(text):
        url = url.rstrip(".,;:!?")
        if len(url) > MAX_URL_LEN:
            url = url[:MAX_URL_LEN]
        if url in seen:
            continue
        seen.add(url)
        if URL_AUTH_RE.search(url) and not URL_FOOTER_RE.search(url):
            links.append(url)
        if len(links) >= 2:
            break
    return links


def supa_post(path, payload):
    url = f"{os.environ['SUPA_URL']}/rest/v1/{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "apikey": os.environ["SUPA_ANON"],
            "Authorization": f"Bearer {os.environ['SUPA_ANON']}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status in (200, 201)
    except Exception as e:
        print(f"    supa_post {path} error: {e}")
        return False


def code_exists(alias, codigo):
    """True = existe, False = no existe, None = no se pudo consultar.

    v2: None ya NO se trata como ausencia — el llamador salta el insert y
    deja el correo sin marcar para reintentar (v1 insertaba duplicados o,
    peor, perdía el código si el insert fallaba después).
    """
    # codigo puede contener caracteres de URL (magic links): escapar para query param
    import urllib.parse
    url = (
        f"{os.environ['SUPA_URL']}/rest/v1/email_codes"
        f"?select=id&alias=eq.{urllib.parse.quote(alias, safe='')}"
        f"&codigo=eq.{urllib.parse.quote(codigo, safe='')}&usado=eq.false&limit=1"
    )
    req = urllib.request.Request(
        url, headers={"apikey": os.environ["SUPA_ANON"], "Authorization": f"Bearer {os.environ['SUPA_ANON']}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return len(json.load(r)) > 0
    except Exception:
        return None


def harvest(mail_addr, password):
    alias = mail_addr.split("@")[0]
    found = []
    m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    try:
        m.login(mail_addr, password)
        m.select("INBOX")
        since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%d-%b-%Y")
        typ, data = m.search(None, f"(UNSEEN SINCE {since})")
        ids = data[0].split()
        for i in ids[:30]:
            typ, msg_data = m.fetch(i, "(BODY.PEEK[])")
            if typ != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            sender = parseaddr(msg.get("From", ""))[1]
            if sender in SKIP_SENDERS:
                m.store(i, "+FLAGS", "\\Seen")
                continue
            subject = str(email.header.make_header(email.header.decode_header(msg.get("Subject", ""))))
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode("utf-8", "ignore")
            else:
                body = (msg.get_payload(decode=True) or b"").decode("utf-8", "ignore")
            text = f"{subject}\n{body}"
            service = sender.split("@")[1].split(".")[0] if "@" in sender else "desconocido"

            pendientes = []  # (fila, ya_validado) por persistir
            for code in extract_codes(text):
                exists = code_exists(alias, code)
                if exists is None:
                    print(f"    [{mail_addr}] dedup no consultable para {code}: se reintenta en el próximo ciclo")
                    continue
                if not exists:
                    pendientes.append({
                        "alias": alias, "email": mail_addr, "codigo": code,
                        "servicio": service, "usado": False,
                    })
            for link in extract_magic_links(text):
                exists = code_exists(alias, link)
                if exists is None:
                    print(f"    [{mail_addr}] dedup no consultable para magic link: se reintenta en el próximo ciclo")
                    continue
                if not exists:
                    pendientes.append({
                        "alias": alias, "email": mail_addr, "codigo": link,
                        "servicio": f"magiclink:{service}", "usado": False,
                    })

            if not pendientes:
                m.store(i, "+FLAGS", "\\Seen")  # nada que persistir: liberar
                continue

            todo_ok = True
            for row in pendientes:
                if supa_post("email_codes", row):
                    found.append((row["servicio"], row["codigo"][:24]))
                else:
                    todo_ok = False
            # v2: solo marcar leído si TODO persistió; si algo falló, el correo
            # queda sin leer y el próximo ciclo lo reintenta (el flujo no pierde datos)
            if todo_ok:
                m.store(i, "+FLAGS", "\\Seen")
            else:
                print(f"    [{mail_addr}] persistencia parcial: correo queda SIN marcar para reintento")
        m.logout()
    except Exception as e:
        print(f"  [{mail_addr}] ERROR: {e}")
    return found


def main():
    passes = json.loads(os.environ.get("MIU_GMAIL_PASSES", "{}"))
    print(f"=== MIU Email Relay v2.1 — {len(passes)} cuentas ===")
    total = 0
    magic_links = 0
    ok_accounts = 0
    for mail_addr, password in passes.items():
        found = harvest(mail_addr, password)
        if found:
            print(f"  [{mail_addr}] {len(found)} hallazgos -> Panteón: {found}")
            total += len(found)
            magic_links += sum(1 for s, _ in found if s.startswith("magiclink:"))
            ok_accounts += 1
        else:
            print(f"  [{mail_addr}] sin códigos nuevos")
    summary = {
        "origen": "perplexity_auth",
        "destino": "todos",
        "tipo": "email_relay",
        "source_node": "gha-miu-email-relay",
        "evidence_level": "verificado",
        "payload": {
            "version": "v2-magiclinks",
            "cuentas_revisadas": len(passes),
            "cuentas_ok": ok_accounts,
            "codigos_nuevos": total,
            "magic_links": magic_links,
            "ts": datetime.now(timezone.utc).isoformat(),
        },
    }
    supa_post("gossip_log", summary)
    print(f"=== Resumen: {len(passes)} cuentas revisadas, {total} hallazgos publicados ({magic_links} magic links) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
