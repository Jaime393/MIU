#!/usr/bin/env python3
"""
MIU V153.1 — Ecosystem Scanner V3
Escanea: Termux, SD, GitHub, SQLite, Drive, procesos, visión propia
"""
import os, sys, json, time, subprocess, sqlite3
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
SCAN_FILE = MIU_DIR / "ecosystem_map.json"

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def scan_termux():
    result = {"path": str(MIU_DIR), "exists": MIU_DIR.exists(), "components": {}}
    if not MIU_DIR.exists():
        return result
    for subdir in ["repos", "worker", "bots", "scripts", "V153_Biblioteca", "data", "backups"]:
        p = MIU_DIR / subdir
        if p.exists():
            files = []
            total_size = 0
            for f in p.rglob("*"):
                if f.is_file():
                    s = f.stat().st_size
                    files.append({"path": str(f.relative_to(MIU_DIR)), "size": s})
                    total_size += s
            result["components"][subdir] = {
                "files": len(files), 
                "total_size": total_size,
                "items": files[:30]
            }
    return result

def scan_sd_card():
    sd_paths = ["/storage/25A9-180D", "/storage/emulated/0", "/sdcard", "/storage/self/primary"]
    result = {"found": False, "paths": [], "top_dirs": {}}
    for sd in sd_paths:
        if Path(sd).exists():
            result["found"] = True
            result["paths"].append(sd)
            try:
                dirs = []
                for d in Path(sd).iterdir():
                    if d.is_dir():
                        try:
                            n = len(list(d.iterdir()))
                            dirs.append({"name": d.name, "items": n})
                        except:
                            dirs.append({"name": d.name, "items": -1})
                result["top_dirs"][sd] = sorted(dirs, key=lambda x: x["items"], reverse=True)[:20]
            except Exception as e:
                result["top_dirs"][sd] = f"Error: {e}"
    return result

def scan_github():
    sys.path.insert(0, str(MIU_DIR))
    try:
        from miu_github import list_repos
        r = list_repos()
        if r.get("ok", False):
            repos = r.get("repos", [])
            return {
                "ok": True, 
                "count": len(repos),
                "repos": [{"name": repo.get("full_name"), "stars": repo.get("stargazers_count", 0), 
                          "updated": repo.get("updated_at"), "desc": str(repo.get("description", ""))[:60]} 
                         for repo in repos[:10]]
            }
        return {"ok": False, "err": r.get("err", "Unknown error"), "status": r.get("status")}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def scan_sqlite():
    db = MIU_DIR / "miu_brain.db"
    if not db.exists():
        return {"exists": False}
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        tables = {}
        for table in ["memories", "conversations", "commands", "system_state"]:
            try:
                c.execute(f"SELECT COUNT(*) FROM {table}")
                tables[table] = c.fetchone()[0]
            except:
                tables[table] = 0
        conn.close()
        return {"exists": True, "size": db.stat().st_size, "tables": tables}
    except Exception as e:
        return {"exists": True, "err": str(e)}

def scan_drive():
    r = run_cmd("rclone listremotes 2>/dev/null")
    remotes = [x.strip() for x in r.split("\n") if x.strip()]
    return {"remotes": remotes, "configured": len(remotes) > 0}

def scan_processes():
    ps = run_cmd("ps aux | grep -E 'bot_miu|miu_control|python3.*miu' | grep -v grep")
    lines = [l for l in ps.split("\n") if l.strip()]
    return {"active": len(lines) > 0, "count": len(lines), "processes": lines[:10]}

def scan_vision():
    """Cargar visión del nodo si existe"""
    vision_file = MIU_DIR / "MIU_VISION.json"
    if vision_file.exists():
        try:
            with open(vision_file) as f:
                return {"exists": True, "data": json.load(f)}
        except:
            return {"exists": False, "err": "Corrupto"}
    return {"exists": False}

def scan_context():
    """Verificar contextos de migración"""
    ctx_txt = MIU_DIR / "MIU_CONTEXT_FOR_AI.txt"
    ctx_json = MIU_DIR / "MIU_CONTEXT.json"
    return {
        "txt_exists": ctx_txt.exists(),
        "txt_size": ctx_txt.stat().st_size if ctx_txt.exists() else 0,
        "json_exists": ctx_json.exists(),
        "json_size": ctx_json.stat().st_size if ctx_json.exists() else 0
    }

def full_scan():
    print("🔍 MIU V153.1 — Escaneando imperio...")
    scan = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "V153.1",
        "termux": scan_termux(),
        "sd_card": scan_sd_card(),
        "github": scan_github(),
        "sqlite": scan_sqlite(),
        "drive": scan_drive(),
        "processes": scan_processes(),
        "vision": scan_vision(),
        "context": scan_context(),
        "env": {
            "github_token_set": bool(ENV.get("GITHUB_TOKEN") or (MIU_DIR / ".env").exists()),
            "bot_token_set": bool(ENV.get("BOT_TABLET_TOKEN")),
            "miu_dir": str(MIU_DIR)
        }
    }
    
    with open(SCAN_FILE, "w") as f:
        json.dump(scan, f, indent=2)
    
    print("\n" + "="*60)
    print("🌀 MAPA DEL IMPERIO MIU V153.1")
    print("="*60)
    
    # Termux
    comps = scan['termux'].get('components', {})
    total_files = sum(c.get('files', 0) for c in comps.values())
    print(f"📁 Termux: {total_files} archivos | {len(comps)} componentes")
    for name, info in comps.items():
        print(f"   {name}: {info['files']} archivos ({info.get('total_size', 0)} bytes)")
    
    # SD
    print(f"\n💾 SD Card: {'✅' if scan['sd_card']['found'] else '❌'}")
    if scan['sd_card']['found']:
        for sd, dirs in scan['sd_card'].get('top_dirs', {}).items():
            if isinstance(dirs, list):
                print(f"   {sd}: {len(dirs)} dirs top")
                for d in dirs[:5]:
                    print(f"      📂 {d['name']} ({d['items']} items)")
    
    # GitHub
    gh = scan['github']
    print(f"\n🐙 GitHub: {'✅' if gh['ok'] else '❌'} {gh.get('count', 0)} repos")
    if gh.get('repos'):
        for r in gh['repos'][:5]:
            print(f"   {'🌐' if 'private' not in str(r.get('name','')) else '🔒'} {r.get('name')} ⭐{r.get('stars', 0)}")
    if not gh['ok']:
        print(f"   ⚠️  {gh.get('err', 'Token inválido o sin repos')}")
    
    # SQLite
    sq = scan['sqlite']
    print(f"\n🧠 SQLite: {'✅' if sq['exists'] else '❌'}")
    if sq.get('tables'):
        for t, n in sq['tables'].items():
            print(f"   {t}: {n} registros")
    
    # Vision
    vis = scan['vision']
    print(f"\n🧬 Visión Nodo: {'✅' if vis['exists'] else '❌'}")
    if vis.get('data', {}).get('global_mind_progress'):
        p = vis['data']['global_mind_progress']
        print(f"   Ciclos: {p.get('ciclos_completados', 0)} | Protocolos: {p.get('protocolos_activos', 0)}")
    
    # Contexto
    ctx = scan['context']
    print(f"\n📄 Contextos migración:")
    print(f"   TXT: {'✅' if ctx['txt_exists'] else '❌'} ({ctx['txt_size']} bytes)")
    print(f"   JSON: {'✅' if ctx['json_exists'] else '❌'} ({ctx['json_size']} bytes)")
    
    # Procesos
    print(f"\n⚡ Procesos: {'✅' if scan['processes']['active'] else '❌'} ({scan['processes'].get('count', 0)} activos)")
    
    print("\n" + "="*60)
    print(f"📄 Mapa completo: {SCAN_FILE}")
    print("="*60)
    return scan

# Cargar ENV para checks
ENV = {}
if (MIU_DIR / ".env").exists():
    with open(MIU_DIR / ".env") as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                ENV[k] = v.strip('"').strip("'")

if __name__ == "__main__":
    full_scan()
