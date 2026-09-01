#!/usr/bin/env python3
"""
MIU V201 — VALIDADOR DE RECURSOS LIGERO
Valida máximo 20 recursos, timeout 5s por recurso.
"""
import os, subprocess
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")

def log(msg):
    print(f"📋 {msg}")

def test_resource(name, timeout=5):
    tests = {
        "github": "curl -sI https://api.github.com | head -1",
        "telegram": f"curl -s https://api.telegram.org/bot$(grep BOT_TABLET_TOKEN {MIU_DIR}/.env | cut -d= -f2 | tr -d \\\"'\\\")/getMe 2>/dev/null | head -c 50",
        "cloudflare": "curl -sI https://api.cloudflare.com/client/v4/ips | head -1",
        "worker": "curl -sL --max-time 5 https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global?vive=1 | head -c 50",
        "groq": "curl -sI --max-time 5 https://api.groq.com/openai/v1/models | head -1",
        "drive": "rclone listremotes 2>/dev/null | head -1",
        "tmpfiles": "curl -sI https://tmpfiles.org | head -1",
        "internet": "curl -sI https://www.google.com | head -1",
    }
    if name not in tests:
        return {"ok": False, "detail": "recurso desconocido"}
    try:
        r = subprocess.run(tests[name], shell=True, capture_output=True, text=True, timeout=timeout)
        ok = r.returncode == 0 and len(r.stdout) > 5
        return {"ok": ok, "detail": r.stdout[:100]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "detail": f"timeout ({timeout}s)"}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

def main():
    log("📋 VALIDADOR V201 — Máximo 20 recursos, timeout 5s")
    log("=" * 40)
    recursos = ["internet", "github", "telegram", "cloudflare", "worker", "groq", "drive", "tmpfiles"]
    validados = []
    for i, nombre in enumerate(recursos):
        if i >= 20:
            log("   ⏭️ Límite de 20 recursos alcanzado")
            break
        res = test_resource(nombre, timeout=5)
        status = "✅" if res["ok"] else "❌"
        log(f"   {status} {nombre}: {res['detail'][:50]}")
        validados.append({"nombre": nombre, "ok": res["ok"]})
    ok_count = sum(1 for v in validados if v["ok"])
    log("=" * 40)
    log(f"✅ Validación: {ok_count}/{len(validados)} recursos OK")
    return {"validados": validados, "ok_count": ok_count}

if __name__ == "__main__":
    main()
