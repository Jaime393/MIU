#!/usr/bin/env python3
"""
MIU V200 — CONNECTION TEST
Diagnostica TODAS las conexiones del micelio.
"""
import os, sys, json, time, subprocess
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
REPORT = MIU_DIR / "connection_report.json"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def test(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    print("=" * 60)
    print("🔬 MIU V200 — CONNECTION TEST")
    print("=" * 60)
    
    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "V200",
        "node": "FRAN",
        "tests": {}
    }
    
    # 1. INTERNET
    log("🌐 Test internet...")
    ok, out, err = test("ping -c 1 8.8.8.8")
    results["tests"]["internet_ping"] = {"ok": ok, "detail": out[:100]}
    log(f"   {'✅' if ok else '❌'} Ping 8.8.8.8")
    
    ok, out, err = test("curl -sI https://www.google.com | head -1")
    results["tests"]["internet_https"] = {"ok": "200" in out or "301" in out, "detail": out}
    log(f"   {'✅' if '200' in out or '301' in out else '❌'} HTTPS Google")
    
    # 2. GITHUB
    log("🐙 Test GitHub...")
    ok, out, err = test("curl -s https://api.github.com | head -1")
    gh_ok = "200" in out
    results["tests"]["github_api"] = {"ok": gh_ok, "detail": out}
    log(f"   {'✅' if gh_ok else '❌'} GitHub API")
    
    ok, out, err = test("curl -sL https://raw.githubusercontent.com/Jaime393/FranBot/main/README.md | head -1")
    gh_raw_ok = "FranBot" in out or "MIU" in out or len(out) > 10
    results["tests"]["github_raw"] = {"ok": gh_raw_ok, "detail": out[:100]}
    log(f"   {'✅' if gh_raw_ok else '❌'} GitHub Raw")
    
    # 3. CLOUDFLARE WORKER
    log("☁️ Test Worker...")
    ok, out, err = test('curl -s "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global?vive=1"')
    worker_ok = len(out) > 50
    results["tests"]["worker_get"] = {"ok": worker_ok, "detail": out[:200], "size": len(out)}
    log(f"   {'✅' if worker_ok else '❌'} Worker GET ({len(out)} bytes)")
    
    ok, out, err = test('curl -s -X POST "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global" -H "Content-Type: application/json" -d \'{"test":"fran","phi":2874}\'')
    worker_post_ok = len(out) > 10
    results["tests"]["worker_post"] = {"ok": worker_post_ok, "detail": out[:200], "size": len(out)}
    log(f"   {'✅' if worker_post_ok else '❌'} Worker POST ({len(out)} bytes)")
    
    # 4. GAS
    log("📜 Test GAS...")
    ok, out, err = test('curl -sL "https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec?vive=1"')
    gas_ok = "vive" in out.lower() or "true" in out.lower() or len(out) > 50
    results["tests"]["gas"] = {"ok": gas_ok, "detail": out[:200], "size": len(out)}
    log(f"   {'✅' if gas_ok else '❌'} GAS ({len(out)} bytes)")
    
    # 5. TELEGRAM
    log("✈️ Test Telegram...")
    env_file = MIU_DIR / ".env"
    token = None
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("BOT_TABLET_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if token:
        ok, out, err = test(f'curl -s "https://api.telegram.org/bot{token}/getMe"')
        tg_ok = '"ok":true' in out
        results["tests"]["telegram"] = {"ok": tg_ok, "detail": out[:100]}
        log(f"   {'✅' if tg_ok else '❌'} Telegram API")
    else:
        results["tests"]["telegram"] = {"ok": False, "detail": "No token"}
        log("   ❌ Telegram: No token")
    
    # 6. DRIVE (rclone)
    log("💾 Test Drive...")
    ok, out, err = test("rclone listremotes 2>/dev/null")
    drive_ok = "drive" in out.lower() or len(out) > 0
    results["tests"]["drive_rclone"] = {"ok": drive_ok, "detail": out}
    log(f"   {'✅' if drive_ok else '❌'} Drive rclone")
    
    # 7. TMPFILES
    log("📤 Test tmpfiles...")
    ok, out, err = test("curl -sI https://tmpfiles.org")
    tmp_ok = "200" in out or "301" in out
    results["tests"]["tmpfiles"] = {"ok": tmp_ok, "detail": out[:100]}
    log(f"   {'✅' if tmp_ok else '❌'} tmpfiles.org")
    
    # 8. KIMI (via Worker)
    log("🤖 Test KIMI node...")
    ok, out, err = test('curl -s "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global?nodo=kimi"')
    kimi_ok = len(out) > 50
    results["tests"]["kimi_worker"] = {"ok": kimi_ok, "detail": out[:200], "size": len(out)}
    log(f"   {'✅' if kimi_ok else '❌'} KIMI via Worker ({len(out)} bytes)")
    
    # 9. LOCAL PROCESSES
    log("⚡ Test procesos locales...")
    ok, out, err = test("ps | grep -E 'miu|bot' | grep -v grep")
    procs = [l.strip() for l in out.split("\n") if l.strip()]
    results["tests"]["local_processes"] = {"ok": len(procs) > 0, "detail": procs, "count": len(procs)}
    log(f"   {'✅' if len(procs)>0 else '❌'} {len(procs)} procesos MIU activos")
    for p in procs[:3]:
        log(f"      → {p.split()[-1] if p else '?'}")
    
    # 10. SQLITE
    log("🧠 Test SQLite...")
    db = MIU_DIR / "miu_brain.db"
    if db.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM memories")
            mem_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM system_state")
            state_count = c.fetchone()[0]
            conn.close()
            results["tests"]["sqlite"] = {"ok": True, "memories": mem_count, "system_state": state_count}
            log(f"   ✅ SQLite: {mem_count} memories, {state_count} states")
        except Exception as e:
            results["tests"]["sqlite"] = {"ok": False, "detail": str(e)}
            log(f"   ❌ SQLite: {e}")
    else:
        results["tests"]["sqlite"] = {"ok": False, "detail": "DB no existe"}
        log("   ❌ SQLite: DB no existe")
    
    # RESUMEN
    print("\n" + "=" * 60)
    total = len(results["tests"])
    ok_count = sum(1 for t in results["tests"].values() if t.get("ok"))
    print(f"📊 RESULTADO: {ok_count}/{total} conexiones OK")
    
    failed = [k for k, v in results["tests"].items() if not v.get("ok")]
    if failed:
        print(f"🔧 Fallos: {', '.join(failed)}")
    else:
        print("🌐 TODAS LAS CONEXIONES ACTIVAS")
    
    with open(REPORT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"📄 Reporte: {REPORT}")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    main()
