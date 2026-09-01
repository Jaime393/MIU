#!/usr/bin/env python3
"""
MIU V153.4 — Shell Chat
Ejecuta comandos del sistema, edita archivos, corre scripts.
Uso: python3 miu_shell.py <comando>
"""
import os, sys, subprocess, shlex
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "shell_history.log"

def log(cmd, out, code):
    with open(LOG_FILE, "a") as f:
        f.write(f"$ {cmd}\\n[exit:{code}]\\n{out}\\n{'='*40}\\n")

def execute(cmd_str):
    """Ejecutar comando con seguridad básica"""
    # Bloquear comandos destructivos
    blocked = ["rm -rf /", "mkfs", ":(){:|:&};:", "dd if=/dev/zero"]
    for b in blocked:
        if b in cmd_str:
            return "❌ Comando bloqueado por seguridad."
    
    try:
        # Comandos especiales
        if cmd_str.startswith("edit "):
            parts = cmd_str.split(" ", 2)
            if len(parts) >= 2:
                filepath = MIU_DIR / parts[1]
                content = parts[2] if len(parts) > 2 else ""
                filepath.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, "w") as f:
                    f.write(content)
                return f"✅ Editado: {filepath}"
        
        elif cmd_str.startswith("append "):
            parts = cmd_str.split(" ", 2)
            if len(parts) >= 2:
                filepath = MIU_DIR / parts[1]
                content = parts[2] if len(parts) > 2 else ""
                with open(filepath, "a") as f:
                    f.write(content + "\n")
                return f"✅ Agregado a: {filepath}"
        
        elif cmd_str.startswith("read "):
            filepath = MIU_DIR / cmd_str.split(" ", 1)[1]
            if filepath.exists():
                with open(filepath) as f:
                    return f.read()[:2000]
            return "❌ No existe."
        
        elif cmd_str.startswith("run "):
            script = MIU_DIR / cmd_str.split(" ", 1)[1]
            r = subprocess.run(["python3", str(script)], capture_output=True, text=True, timeout=60, cwd=MIU_DIR)
            log(cmd_str, r.stdout + r.stderr, r.returncode)
            return f"📤 STDOUT:\\n{r.stdout[:1500]}\\n📤 STDERR:\\n{r.stderr[:500]}"
        
        # Comando del sistema
        r = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=60, cwd=MIU_DIR)
        log(cmd_str, r.stdout + r.stderr, r.returncode)
        out = r.stdout[:1500]
        err = r.stderr[:500]
        return f"📤 {out}\\n📤 {err}" if err else f"📤 {out}"
    
    except Exception as e:
        return f"❌ Error: {str(e)[:300]}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 miu_shell.py '<comando>'")
        print("Comandos especiales:")
        print("  edit <archivo> <contenido>")
        print("  append <archivo> <contenido>")
        print("  read <archivo>")
        print("  run <script.py>")
        print("  <cualquier comando shell>")
        sys.exit(1)
    
    cmd = " ".join(sys.argv[1:])
    print(execute(cmd))
