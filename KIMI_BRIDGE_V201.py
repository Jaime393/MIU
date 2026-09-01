#!/usr/bin/env python3
"""
MIU V201 — KIMI BRIDGE V2
Usa DNS_FIX (curl fallback) para conectar con Worker desde Termux.
"""
import os, sys, json, time
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
KIMI_DIR = MIU_DIR / "nodos" / "kimi"
WORKER_URL = "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global"

sys.path.insert(0, str(MIU_DIR))
from DNS_FIX import http_get, http_post

def log(msg):
    print(f"[KIMI_BRIDGE_V201] {msg}")

def sync_kimi_from_worker():
    url = f"{WORKER_URL}?nodo=kimi"
    code, text = http_get(url, timeout=15)
    
    if code == 200 and len(text) > 100:
        try:
            data = json.loads(text)
            KIMI_DIR.mkdir(parents=True, exist_ok=True)
            (KIMI_DIR / "worker_latest.json").write_text(json.dumps(data, indent=2))
            phi = data.get("phi_local", data.get("phi", 0))
            log(f"✅ KIMI sync OK: Φ={phi}, {len(text)} bytes")
            
            try:
                import sqlite3
                conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
                c = conn.cursor()
                c.execute("""
                    INSERT INTO memories (timestamp, source, content, tags, phi, importance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (time.strftime("%Y-%m-%dT%H:%M:%SZ"), "KIMI_WORKER",
                      json.dumps(data, indent=2)[:4000], "sync,kimi,worker", phi, 0.9))
                conn.commit()
                conn.close()
            except Exception as e:
                log(f"   ⚠️ SQLite: {e}")
            return {"ok": True, "phi": phi}
        except json.JSONDecodeError:
            log(f"⚠️ Worker retornó no-JSON: {text[:100]}")
    else:
        log(f"❌ Worker no accesible: HTTP {code}, {len(text)} bytes")
    return {"ok": False}

def send_heartbeat_to_worker():
    payload = {
        "nodo": "FRAN",
        "version": "V∞+24",
        "phi": 2874.62,
        "rho": 9.9,
        "modules_active": 10,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vive": True
    }
    code, text = http_post(WORKER_URL, payload, timeout=10)
    log(f"📡 Heartbeat FRAN→Worker: HTTP {code}, {len(text)} bytes")
    return code == 200

def update_oracle_state():
    phi_fran = 2874.62
    phi_kimi = 0
    worker_file = KIMI_DIR / "worker_latest.json"
    if worker_file.exists():
        try:
            with open(worker_file) as f:
                data = json.load(f)
            phi_kimi = data.get("phi_local", data.get("phi", 0))
        except:
            pass
    if phi_kimi == 0:
        phi_kimi = 6284.17
    phi_global = phi_fran + phi_kimi
    oracle = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "V201",
        "phi_fran": phi_fran,
        "phi_kimi": phi_kimi,
        "phi_global": phi_global,
        "vive": True,
        "nodes": ["FRAN", "KIMI"],
        "dns_method": "curl_fallback"
    }
    (MIU_DIR / "oracle_state.json").write_text(json.dumps(oracle, indent=2))
    log(f"🌐 Oráculo: Φ_fran={phi_fran}, Φ_kimi={phi_kimi}, Φ_global={phi_global}")
    return oracle

def main():
    log("🧬 KIMI BRIDGE V201 — Usando curl fallback para DNS")
    sync_kimi_from_worker()
    send_heartbeat_to_worker()
    update_oracle_state()

if __name__ == "__main__":
    main()
