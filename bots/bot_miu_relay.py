#!/usr/bin/env python3
"""
MIU V153 — Bot Relay V3
Control total: shell + GitHub + productos + memoria
"""
import os, sys, json, time, requests, subprocess, sqlite3
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
sys.path.insert(0, str(MIU_DIR))
from miu_memory import remember, recall, log_conversation, log_command, set_state, get_state

ENV = {}
with open(MIU_DIR / ".env") as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            ENV[k] = v.strip('"').strip("'")

TOKEN = ENV.get("BOT_TABLET_TOKEN", "")
OR_KEY = ENV.get("OR_JAIME", "")
CLAUDE_KEY = ENV.get("CLAUDE_DIEGO", "")
GROQ_KEY = ENV.get("GROQ_FRAN", "")

MIU_PROMPT = "Eres nodo MIU. ρ(x)>0. Kτ=34.0332 σ=3.427051 RAIZ_X=137.034498. Sin evidencia, sin dios. Fin."

def log(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}")
    with open(MIU_DIR / "bot.log", "a") as f:
        f.write(f"[{t}] {msg}\n")

def call_or(msg, model="meta-llama/llama-4-maverick"):
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role":"system","content":MIU_PROMPT},{"role":"user","content":msg}]},
            timeout=60)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ {str(e)[:200]}"

def call_claude(msg):
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": CLAUDE_KEY, "Content-Type": "application/json", "anthropic-version": "2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":4096,"system":MIU_PROMPT,"messages":[{"role":"user","content":msg}]},
            timeout=60)
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"❌ {str(e)[:200]}"

def call_groq(msg):
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model":"llama-4-scout-17b-16e-instruct","messages":[{"role":"system","content":MIU_PROMPT},{"role":"user","content":msg}]},
            timeout=60)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ {str(e)[:200]}"

def exec_shell(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=MIU_DIR, timeout=30)
        log_command(cmd, result.stdout[:500], "ok" if result.returncode == 0 else "fail", source="telegram")
        return f"🌀 CMD\\n📤 {result.stdout[:1500]}\\n📤 {result.stderr[:500]}"[:4000]
    except Exception as e:
        return f"❌ {str(e)[:300]}"

def exec_github(cmd):
    """Ejecutar comandos GitHub via miu_github.py"""
    try:
        result = subprocess.run(f"python3 {MIU_DIR}/miu_github.py {cmd}",
            shell=True, capture_output=True, text=True, cwd=MIU_DIR, timeout=30)
        return f"🐙 GITHUB\\n📤 {result.stdout[:1500]}\\n📤 {result.stderr[:500]}"[:4000]
    except Exception as e:
        return f"❌ {str(e)[:300]}"

def main():
    if not TOKEN:
        print("❌ Sin token"); sys.exit(1)
    try:
        from telegram import Update
        from telegram.ext import Application, MessageHandler, filters, ContextTypes
    except ImportError:
        print("❌ pip install python-telegram-bot"); sys.exit(1)

    log("🤖 Bot MIU Relay V3 iniciando...")
    app = Application.builder().token(TOKEN).build()

    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message.text
        user = update.message.from_user.username or "anon"
        log(f"[{user}] {msg[:100]}")

        # IA
        if msg.startswith("/meta"): reply = call_or(msg[5:])
        elif msg.startswith("/claude"): reply = call_claude(msg[7:])
        elif msg.startswith("/groq"): reply = call_groq(msg[5:])
        elif msg.startswith("/miu"): reply = call_or(msg[4:])
        
        # Sistema
        elif msg.startswith("/shell "): reply = exec_shell(msg[7:])
        elif msg.startswith("/miucmd "): reply = exec_shell(msg[8:])
        elif msg.startswith("/products"):
            reply = ""
            for name, path in [
                ("gossip", "repos/miu-v153-gossip/global-mind-gossip-phi4.py"),
                ("memoria", "repos/miu-v153-memoria/memoria-fractal-phi4.py"),
                ("arte", "repos/miu-v153-arte/arte-phi4-generador.py"),
                ("lod", "repos/miu-v153-lod/lod-c20-predictor.py")
            ]:
                r = subprocess.run(f"python3 {MIU_DIR/path}", shell=True, capture_output=True, text=True, timeout=30)
                reply += f"\\n{'✅' if r.returncode==0 else '❌'} {name}"
        elif msg.startswith("/status"):
            from miu_memory import get_stats
            s = get_stats()
            reply = f"🌀 MIU V3\\nΦ:2874.62 Kτ:34.0332\\nMem:{s['memories']} Chat:{s['conversations']}\\nBot:running"
        
        # GitHub
        elif msg.startswith("/gh "): reply = exec_github(msg[4:])
        elif msg.startswith("/gh-list"): reply = exec_github("list")
        elif msg.startswith("/gh-create "): reply = exec_github(f"create {msg[11:]}")
        elif msg.startswith("/gh-push"):
            reply = exec_github("push")  # Custom or use shell
        elif msg.startswith("/gh-issues "): reply = exec_github(f"issues {msg[11:]}")
        
        # Memoria
        elif msg.startswith("/remember "):
            remember(msg[10:], source=user, tags="telegram")
            reply = "🧠 Recordado"
        elif msg.startswith("/recall"):
            rows = recall(limit=5)
            reply = "\\n".join([f"[{r[1][:16]}] {r[3][:60]}..." for r in rows]) or "Vacío"
        
        # Ayuda
        else:
            reply = """🌀 MIU V153 COMANDOS:
🧠 IA: /meta /claude /groq /miu
⚡ SYS: /shell <cmd> /products /status
🐙 GITHUB: /gh-list /gh-create <name> /gh-issues <repo> /gh <args>
🧠 MEM: /remember <text> /recall
📄 Ej: /gh-create miu-v154-test"""

        log_conversation(user, msg, reply[:100], model="relay")
        await update.message.reply_text(reply[:4000])

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    log("✅ Bot V3 escuchando")
    set_state("bot_status", "running")
    app.run_polling()

if __name__ == "__main__":
    main()
