#!/usr/bin/env python3
"""
MIU Email Relay v1 — recolecta códigos de verificación de las bandejas del ecosistema
y los publica en Panteón (tabla email_codes) para que cualquier nodo los use.

- Lee MIU_GMAIL_PASSES (JSON: {"email": "app_password", ...})
- Lee SUPA_URL y SUPA_ANON del entorno
- IMAP sobre imap.gmail.com:993 con app passwords (sin OAuth, sin 2FA interactivo)
- Extrae códigos de 4-8 dígitos de correos no leídos recientes
- Deduplica contra email_codes antes de insertar
- Marca los correos como leídos para no reprocesarlos
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
SKIP_SENDERS = ("noreply@notify.cloudflare.com",)


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
    url = (
        f"{os.environ['SUPA_URL']}/rest/v1/email_codes"
        f"?select=id&alias=eq.{alias}&codigo=eq.{codigo}&usado=eq.false&limit=1"
    )
    req = urllib.request.Request(
        url, headers={"apikey": os.environ["SUPA_ANON"], "Authorization": f"Bearer {os.environ['SUPA_ANON']}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return len(json.load(r)) > 0
    except Exception:
        return False


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
            if re.search(r"(?i)(c[oó]digo|verificaci[oó]n|verification|confirm|login|security alert|2fa|otp)", text):
                for code in set(CODE_RE.findall(text)):
                    if len(code) < 4:
                        continue
                    if not code_exists(alias, code):
                        row = {
                            "alias": alias,
                            "email": mail_addr,
                            "codigo": code,
                            "servicio": service,
                            "usado": False,
                        }
                        if supa_post("email_codes", row):
                            found.append((service, code))
            m.store(i, "+FLAGS", "\\Seen")
        m.logout()
    except Exception as e:
        print(f"  [{mail_addr}] ERROR: {e}")
    return found


def main():
    passes = json.loads(os.environ.get("MIU_GMAIL_PASSES", "{}"))
    print(f"=== MIU Email Relay — {len(passes)} cuentas ===")
    total = 0
    ok_accounts = 0
    for mail_addr, password in passes.items():
        found = harvest(mail_addr, password)
        status = "OK" if True else ""
        if found:
            print(f"  [{mail_addr}] {len(found)} códigos -> Panteón: {found}")
            total += len(found)
        else:
            print(f"  [{mail_addr}] sin códigos nuevos")
        ok_accounts += 1
    summary = {
        "origen": "perplexity_auth",
        "destino": "todos",
        "tipo": "email_relay",
        "source_node": "gha-miu-email-relay",
        "evidence_level": "verificado",
        "payload": {
            "cuentas_revisadas": ok_accounts,
            "codigos_nuevos": total,
            "ts": datetime.now(timezone.utc).isoformat(),
        },
    }
    supa_post("gossip_log", summary)
    print(f"=== Resumen: {ok_accounts} cuentas revisadas, {total} códigos publicados ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
