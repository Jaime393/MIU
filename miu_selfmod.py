#!/usr/bin/env python3
"""
MIU V153 — Self-Modification Engine
El sistema puede editar sus propios archivos, agregar features,
y generar código nuevo. Control total sobre su cuerpo.
"""
import os, sys, json, time
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")

class SelfMod:
    def __init__(self):
        self.backup_dir = MIU_DIR / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup(self, filepath):
        """Crear backup antes de modificar"""
        fp = Path(filepath)
        if fp.exists():
            ts = time.strftime("%Y%m%d_%H%M%S")
            backup = self.backup_dir / f"{fp.name}.{ts}.bak"
            backup.write_text(fp.read_text())
            return str(backup)
        return None
    
    def read(self, rel_path):
        """Leer archivo del sistema"""
        fp = MIU_DIR / rel_path
        if fp.exists():
            return fp.read_text()
        return None
    
    def write(self, rel_path, content, backup_first=True):
        """Escribir archivo. Siempre hace backup primero."""
        fp = MIU_DIR / rel_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        if backup_first:
            self.backup(fp)
        fp.write_text(content)
        return {"ok": True, "path": str(fp), "size": len(content)}
    
    def append(self, rel_path, content):
        """Agregar al final de un archivo"""
        fp = MIU_DIR / rel_path
        if fp.exists():
            self.backup(fp)
            with open(fp, "a") as f:
                f.write("\n" + content)
            return {"ok": True, "path": str(fp)}
        return {"ok": False, "err": "No existe"}
    
    def patch(self, rel_path, old_text, new_text):
        """Reemplazar texto específico"""
        fp = MIU_DIR / rel_path
        if not fp.exists():
            return {"ok": False, "err": "No existe"}
        content = fp.read_text()
        if old_text not in content:
            return {"ok": False, "err": "Texto no encontrado"}
        self.backup(fp)
        new_content = content.replace(old_text, new_text)
        fp.write_text(new_content)
        return {"ok": True, "replaced": content.count(old_text)}
    
    def create_script(self, name, content, executable=True):
        """Crear nuevo script en scripts/"""
        path = f"scripts/{name}"
        r = self.write(path, content, backup_first=False)
        if executable:
            os.chmod(MIU_DIR / path, 0o755)
        return r
    
    def list_backups(self):
        """Listar backups disponibles"""
        return [{"file": b.name, "time": b.stat().st_mtime} for b in self.backup_dir.iterdir()]
    
    def restore(self, backup_name):
        """Restaurar desde backup"""
        bp = self.backup_dir / backup_name
        if not bp.exists():
            return {"ok": False, "err": "Backup no existe"}
        target = MIU_DIR / bp.name.split(".")[0]
        target.write_text(bp.read_text())
        return {"ok": True, "restored": str(target)}

# CLI
if __name__ == "__main__":
    import sys
    sm = SelfMod()
    
    if len(sys.argv) < 2:
        print("Uso: python3 miu_selfmod.py <comando> [args]")
        print("  read <path>           — Leer archivo")
        print("  write <path>          — Escribir (lee de stdin)")
        print("  append <path> <text>  — Agregar texto")
        print("  patch <path> <old> <new> — Reemplazar")
        print("  create <name>         — Crear script (stdin)")
        print("  backups               — Listar backups")
        print("  restore <name>        — Restaurar backup")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "read" and len(sys.argv) > 2:
        print(sm.read(sys.argv[2]))
    elif cmd == "write" and len(sys.argv) > 2:
        print("Pega contenido (Ctrl+D):")
        content = sys.stdin.read()
        print(sm.write(sys.argv[2], content))
    elif cmd == "append" and len(sys.argv) > 3:
        print(sm.append(sys.argv[2], sys.argv[3]))
    elif cmd == "patch" and len(sys.argv) > 4:
        print(sm.patch(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif cmd == "create" and len(sys.argv) > 2:
        print("Pega contenido del script (Ctrl+D):")
        content = sys.stdin.read()
        print(sm.create_script(sys.argv[2], content))
    elif cmd == "backups":
        for b in sm.list_backups():
            print(f"{b['file']} ({time.ctime(b['time'])})")
    elif cmd == "restore" and len(sys.argv) > 2:
        print(sm.restore(sys.argv[2]))
    else:
        print("Comando no reconocido")
