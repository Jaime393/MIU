#!/usr/bin/env python3
"""
MIU V153.4 — Plugin Manager
Carga, lista y ejecuta plugins dinámicamente sin reiniciar.
"""
import os, sys, importlib.util, json, inspect
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
PLUGIN_DIR = MIU_DIR / "plugins"

def ensure_dir():
    PLUGIN_DIR.mkdir(exist_ok=True)
    (PLUGIN_DIR / "__init__.py").touch(exist_ok=True)

def list_plugins():
    ensure_dir()
    plugins = []
    for p in PLUGIN_DIR.glob("*.py"):
        if p.stem.startswith("__"):
            continue
        plugins.append({
            "name": p.stem,
            "size": p.stat().st_size,
            "path": str(p.relative_to(MIU_DIR))
        })
    return plugins

def load_plugin(name):
    ensure_dir()
    path = PLUGIN_DIR / f"{name}.py"
    if not path.exists():
        return None, f"Plugin '{name}' no encontrado."
    
    spec = importlib.util.spec_from_file_location(f"miu_plugin_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, None

def run_plugin(name, args=None):
    mod, err = load_plugin(name)
    if err:
        return {"ok": False, "err": err}
    
    # Buscar función principal
    func = None
    for fname in ["run", "main", "execute", f"{name}_run"]:
        if hasattr(mod, fname):
            func = getattr(mod, fname)
            break
    
    if not func:
        return {"ok": False, "err": "Plugin no tiene función run/main/execute"}
    
    try:
        if args:
            result = func(args)
        else:
            result = func()
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def create_plugin(name, code):
    ensure_dir()
    path = PLUGIN_DIR / f"{name}.py"
    with open(path, "w") as f:
        f.write(code)
    return {"ok": True, "path": str(path)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📦 MIU Plugin Manager")
        print("Uso: python3 miu_plugin_manager.py <comando> [args]")
        print("")
        print("Comandos:")
        print("  list                          — Listar plugins")
        print("  run <nombre> [args...]        — Ejecutar plugin")
        print("  create <nombre>               — Crear desde stdin")
        print("  info <nombre>                 — Info del plugin")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        plugins = list_plugins()
        print(f"📦 {len(plugins)} plugins encontrados:")
        for p in plugins:
            print(f"   • {p['name']} ({p['size']} bytes)")
    
    elif cmd == "run" and len(sys.argv) >= 3:
        name = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else None
        r = run_plugin(name, args)
        if r["ok"]:
            print(f"✅ Resultado:\\n{r['result']}")
        else:
            print(f"❌ {r['err']}")
    
    elif cmd == "create" and len(sys.argv) >= 3:
        name = sys.argv[2]
        print("Pega el código del plugin (Ctrl+D para terminar):")
        code = sys.stdin.read()
        r = create_plugin(name, code)
        if r["ok"]:
            print(f"✅ Plugin '{name}' creado en {r['path']}")
    
    elif cmd == "info" and len(sys.argv) >= 3:
        mod, err = load_plugin(sys.argv[2])
        if err:
            print(f"❌ {err}")
        else:
            funcs = [n for n in dir(mod) if not n.startswith("_")]
            print(f"📄 {sys.argv[2]}.py")
            print(f"   Funciones: {', '.join(funcs)}")
    
    else:
        print("Comando no reconocido. Usa 'list', 'run', 'create', 'info'.")
