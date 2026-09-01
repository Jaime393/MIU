#!/usr/bin/env python3
# MIU_INTEGRACION_AUTENTICADOR_ORQUESTADOR_V24.py
# Conecta autenticador con orquestador V∞+24

import os, sys, json
from pathlib import Path

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
PLUGINS_DIR = MIU_DIR / "plugins"

def integrar():
    print("[INTEGRACION] V∞+24")
    
    # 1. Verificar orquestador
    orq_path = PLUGINS_DIR / "orquestador_integrado_v24.py"
    if not orq_path.exists():
        print("  X orquestador_integrado_v24.py no encontrado")
        return False
    print(f"  OK Orquestador: {orq_path}")
    
    # 2. Verificar autenticador
    auth_path = MIU_DIR / "autenticador_autonomo.py"
    if not auth_path.exists():
        print("  ! autenticador_autonomo.py no encontrado")
        print("  Generando stub...")
        with open(auth_path, "w") as f:
            f.write("class AutenticadorStub:\n"
                    "    def query_llm(self, p, s='openrouter'): return {'ok': False, 'error': 'stub'}\n"
                    "    def send_email(self, d, a, c): return {'ok': False}\n"
                    "    def send_telegram(self, d, m): return {'ok': False}\n"
                    "def obtener_autenticador(): return AutenticadorStub()\n")
        print("  OK Stub generado")
    
    # 3. Crear alias en .bashrc
    bashrc = Path("os.path.expanduser('~')/.bashrc")
    alias_line = "alias miu='cd ~/miu-ecosistema && python3 plugins/orquestador_integrado_v24.py --ciclo'\n"
    if bashrc.exists() and alias_line.strip() not in bashrc.read_text():
        with open(bashrc, "a") as f:
            f.write(alias_line)
        print("  OK Alias 'miu' anadido a .bashrc")
    
    print("\n[INTEGRACION] Completada.")
    print("  Uso: miu")
    print("  O: python3 plugins/orquestador_integrado_v24.py --status")
    return True

if __name__ == "__main__":
    integrar()
