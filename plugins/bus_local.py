#!/usr/bin/env python3
"""
MIU V∞+26 — BUS LOCAL CON ARCHIVOS (CORREGIDO)
Usa directorio local en lugar de /tmp para evitar problemas de permisos.
"""
import os, json, time, glob, hashlib
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
QUEUE_DIR = MIU_DIR / ".miu_queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

def enviar(mensaje, destino="broadcast"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    nombre = QUEUE_DIR / f"{timestamp}_{hashlib.md5(str(mensaje).encode()).hexdigest()[:8]}.msg"
    with open(nombre, "w") as f:
        json.dump({"mensaje": mensaje, "destino": destino, "timestamp": timestamp}, f)
    return True

def recibir(limpiar=True):
    mensajes = []
    for archivo in sorted(QUEUE_DIR.glob("*.msg")):
        try:
            with open(archivo, "r") as f:
                data = json.load(f)
                mensajes.append(data)
            if limpiar:
                archivo.unlink()
        except:
            pass
    return mensajes

def run(args=None):
    print("🔌 Bus local con archivos iniciado")
    enviar("Hola desde bus local", "test")
    mensajes = recibir()
    print(f"📨 Mensajes recibidos: {len(mensajes)}")
    return {"ok": True, "mensajes": mensajes}

if __name__ == "__main__":
    print(run())
