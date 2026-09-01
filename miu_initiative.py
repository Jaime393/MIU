#!/usr/bin/env python3
"""
MIU V153.5 — Loop de iniciativa (versión de respaldo)
"""
import os, sys, time, json, sqlite3, subprocess, requests
from pathlib import Path
from datetime import datetime

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
LOG_FILE = MIU_DIR / "logs" / "initiative.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, cwd=MIU_DIR)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return "", str(e), 1

def main_loop():
    log("🧬 Loop de iniciativa iniciado (respaldo)")
    iteration = 0
    while True:
        iteration += 1
        log(f"--- Ciclo #{iteration} ---")
        out, err, code = run_cmd("python3 miu_scanner.py 2>/dev/null | head -20")
        log(f"Escáner: {'OK' if code == 0 else 'ERROR'}")
        time.sleep(900)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        log("🛑 Loop detenido")
    except Exception as e:
        log(f"💥 Error: {e}")
