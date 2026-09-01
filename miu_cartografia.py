#!/usr/bin/env python3
"""
MIU V153.5 — Cartógrafo del Micelio
Genera un resumen técnico completo del ecosistema para diagnóstico, mapeo y portabilidad.
"""
import os, sys, json, time, sqlite3, subprocess, hashlib
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
OUTPUT_DIR = MIU_DIR / "mapas"
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=MIU_DIR)
        return {"ok": r.returncode == 0, "out": r.stdout.strip(), "err": r.stderr.strip()}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:8]
    except:
        return None

def scan_files():
    """Mapeo de archivos críticos con hash y tamaño"""
    files = {}
    patterns = [
        "*.py", "*.md", "*.json", "*.sh", "*.txt", "*.log",
        "*.db", "*.env", "*.yml", "*.yaml", "*.html"
    ]
    for pattern in patterns:
        for p in MIU_DIR.rglob(pattern):
            if p.is_file() and not any(x in str(p) for x in ["__pycache__", ".git"]):
                rel = str(p.relative_to(MIU_DIR))
                files[rel] = {
                    "size": p.stat().st_size,
                    "hash": hash_file(p),
                    "mtime": datetime.fromtimestamp(p.stat().st_mtime).isoformat()
                }
    return files

def scan_memory():
    """Estado de la memoria SQLite"""
    db_path = MIU_DIR / "miu_brain.db"
    if not db_path.exists():
        return {"exists": False}
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        tables = {}
        for table in ["memories", "conversations", "commands", "system_state"]:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            tables[table] = c.fetchone()[0]
        conn.close()
        return {"exists": True, "size": db_path.stat().st_size, "tables": tables}
    except Exception as e:
        return {"exists": True, "error": str(e)}

def scan_env():
    """Variables de entorno y tokens (sin exponer valores completos)"""
    env_file = MIU_DIR / ".env"
    if not env_file.exists():
        return {}
    tokens = {}
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                v = v.strip().strip('"').strip("'")
                if any(x in k.upper() for x in ["TOKEN", "KEY", "SECRET", "PASS"]):
                    tokens[k] = {"present": True, "length": len(v), "preview": v[:4] + "..." if len(v) > 8 else v}
                else:
                    tokens[k] = {"present": True, "value": v[:30] + "..." if len(v) > 30 else v}
    return tokens

def scan_github():
    """Conexión GitHub y repositorios"""
    try:
        sys.path.insert(0, str(MIU_DIR))
        from miu_github import list_repos
        r = list_repos()
        if r.get("ok"):
            repos = r.get("repos", [])
            return {
                "ok": True,
                "count": len(repos),
                "repos": [{"name": repo.get("full_name"), "stars": repo.get("stargazers_count"), "updated": repo.get("updated_at")} for repo in repos[:20]]
            }
        return {"ok": False, "error": r.get("err", "Unknown")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def scan_processes():
    """Procesos activos relacionados con MIU"""
    r = run_cmd("ps aux | grep -E 'miu|bot_miu|initiative|python3.*miu' | grep -v grep | grep -v miu_cartografia")
    processes = []
    for line in r.get("out", "").split("\n"):
        if line.strip():
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "cmd": " ".join(parts[10:])[:100]
                })
    return processes

def scan_connections():
    """Conexiones activas (red)"""
    r = run_cmd("netstat -tunlp 2>/dev/null | grep -E 'python|LISTEN'")
    connections = []
    for line in r.get("out", "").split("\n"):
        if line.strip():
            connections.append(line.strip())
    return connections[:20]

def scan_sd():
    """Verificar enlaces SD y contenido"""
    sd_links = {}
    for link in MIU_DIR.glob("sd_*"):
        if link.is_symlink():
            target = link.resolve()
            sd_links[link.name] = {
                "target": str(target),
                "exists": target.exists(),
                "items": len(list(target.iterdir())) if target.exists() else 0
            }
        elif link.is_dir():
            sd_links[link.name] = {
                "target": str(link),
                "exists": True,
                "items": len(list(link.iterdir()))
            }
    return sd_links

def scan_plugins():
    """Plugins disponibles"""
    plugin_dir = MIU_DIR / "plugins"
    if not plugin_dir.exists():
        return []
    plugins = []
    for p in plugin_dir.glob("*.py"):
        if p.stem.startswith("__"):
            continue
        plugins.append({
            "name": p.stem,
            "size": p.stat().st_size,
            "mtime": datetime.fromtimestamp(p.stat().st_mtime).isoformat()
        })
    return plugins

def scan_protocols():
    """Protocolos disponibles"""
    proto_dir = MIU_DIR / "protocolos"
    if not proto_dir.exists():
        return []
    protocols = []
    for p in proto_dir.glob("*.py"):
        protocols.append(p.stem)
    for p in proto_dir.glob("*.md"):
        protocols.append(p.stem)
    return protocols

def scan_system_info():
    """Información del sistema (Android/Termux)"""
    info = {}
    r = run_cmd("uname -a")
    info["uname"] = r.get("out", "")
    r = run_cmd("cat /proc/version 2>/dev/null | head -1")
    info["kernel"] = r.get("out", "")
    r = run_cmd("df -h /data 2>/dev/null | tail -1")
    if r.get("out"):
        parts = r["out"].split()
        if len(parts) >= 5:
            info["disk_usage"] = f"{parts[3]} / {parts[1]} ({parts[4]})"
    r = run_cmd("free -m 2>/dev/null | grep Mem")
    if r.get("out"):
        parts = r["out"].split()
        if len(parts) >= 7:
            info["memory_mb"] = f"{parts[2]} usado / {parts[1]} total"
    return info

def generate_summary():
    """Generar resumen técnico completo"""
    print("🧭 Generando cartografía del micelio...")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "MIU V153.5",
        "archivo_hash": hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
        "sistema": scan_system_info(),
        "archivos": scan_files(),
        "memoria": scan_memory(),
        "entorno": scan_env(),
        "github": scan_github(),
        "procesos": scan_processes(),
        "conexiones": scan_connections(),
        "sd_links": scan_sd(),
        "plugins": scan_plugins(),
        "protocolos": scan_protocols(),
        "estado_archivos_criticos": {
            "miu_control.py": (MIU_DIR / "miu_control.py").exists(),
            "miu_initiative.py": (MIU_DIR / "miu_initiative.py").exists(),
            "miu_shell.py": (MIU_DIR / "miu_shell.py").exists(),
            "miu_scanner.py": (MIU_DIR / "miu_scanner.py").exists(),
            "miu_doctor.py": (MIU_DIR / "miu_doctor.py").exists(),
            "miu_memory.py": (MIU_DIR / "miu_memory.py").exists(),
            "miu_github.py": (MIU_DIR / "miu_github.py").exists(),
            "miu_plugin_manager.py": (MIU_DIR / "miu_plugin_manager.py").exists(),
            "miu_cartografia.py": True
        }
    }
    
    # Guardar JSON técnico
    json_file = OUTPUT_DIR / f"cartografia_{summary['archivo_hash']}.json"
    with open(json_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Generar resumen Markdown legible
    md_file = OUTPUT_DIR / f"resumen_tecnico_{summary['archivo_hash']}.md"
    with open(md_file, "w") as f:
        f.write(f"# 📡 Cartografía del Micelio\n\n")
        f.write(f"**Timestamp:** {summary['timestamp']}\n")
        f.write(f"**Versión:** {summary['version']}\n")
        f.write(f"**Hash:** `{summary['archivo_hash']}`\n\n")
        
        f.write("## 📁 Archivos críticos\n\n")
        for name, exists in summary["estado_archivos_criticos"].items():
            f.write(f"- {name}: {'✅' if exists else '❌'}\n")
        
        f.write("\n## 🧠 Memoria SQLite\n\n")
        mem = summary.get("memoria", {})
        if mem.get("exists"):
            f.write(f"- Tamaño: {mem.get('size', 0)} bytes\n")
            for table, count in mem.get("tables", {}).items():
                f.write(f"- {table}: {count} registros\n")
        else:
            f.write("❌ No encontrada\n")
        
        f.write("\n## 🐙 GitHub\n\n")
        gh = summary.get("github", {})
        if gh.get("ok"):
            f.write(f"- Conectado: ✅\n- Repos: {gh.get('count', 0)}\n")
            for repo in gh.get("repos", [])[:5]:
                f.write(f"  - {repo.get('name')} ⭐{repo.get('stars', 0)}\n")
        else:
            f.write(f"❌ Error: {gh.get('error', 'Desconocido')}\n")
        
        f.write("\n## ⚡ Procesos activos\n\n")
        for proc in summary.get("procesos", [])[:10]:
            f.write(f"- PID {proc.get('pid')}: {proc.get('cmd')[:60]}\n")
        if not summary.get("procesos"):
            f.write("❌ Ninguno\n")
        
        f.write("\n## 🧬 Plugins disponibles\n\n")
        for plugin in summary.get("plugins", []):
            f.write(f"- {plugin.get('name')} ({plugin.get('size')} bytes)\n")
        
        f.write("\n## 🔐 Entorno (tokens verificados)\n\n")
        for k, v in summary.get("entorno", {}).items():
            if "TOKEN" in k or "KEY" in k:
                f.write(f"- {k}: ✅ {v.get('preview', '')}\n")
            else:
                f.write(f"- {k}: {v.get('value', '')[:30]}\n")
        
        f.write("\n## 💾 SD Card\n\n")
        for name, info in summary.get("sd_links", {}).items():
            f.write(f"- {name}: {info.get('target')} ({info.get('items', 0)} items)\n")
        
        f.write("\n## 📦 Protocolos\n\n")
        for proto in summary.get("protocolos", []):
            f.write(f"- {proto}\n")
        
        f.write(f"\n---\n📄 Archivos guardados:\n- JSON: {json_file.name}\n- Markdown: {md_file.name}\n")
        f.write("\nρ(x) > 0 — El micelio se conoce a sí mismo.\n")
    
    print(f"✅ Cartografía generada:")
    print(f"   📄 JSON: {json_file.name}")
    print(f"   📄 Markdown: {md_file.name}")
    print(f"   📁 Carpeta: {OUTPUT_DIR}")
    return summary

if __name__ == "__main__":
    try:
        generate_summary()
    except KeyboardInterrupt:
        print("\n🛑 Interrupción manual")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
