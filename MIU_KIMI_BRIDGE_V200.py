#!/usr/bin/env python3
import os, sys, json, time, requests, sqlite3
from pathlib import Path
MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
KIMI_DIR = MIU_DIR / "nodos" / "kimi"
WORKER_URL = "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global"
def log(msg): print(f"[KIMI_BRIDGE] {msg}")
def sync_kimi_from_worker():
    try:
        r = requests.get(f"{WORKER_URL}?nodo=kimi", timeout=10)
        if r.status_code == 200 and len(r.text) > 100:
            data = r.json()
            KIMI_DIR.mkdir(parents=True, exist_ok=True)
            (KIMI_DIR / "worker_latest.json").write_text(json.dumps(data, indent=2))
            phi = data.get("phi_local", data.get("phi", 0))
            log(f"✅ KIMI sync OK: Φ={phi}, {len(r.text)} bytes")
            conn = sqlite3.connect(MIU_DIR / "miu_brain.db")
            c = conn.cursor()
            c.execute("INSERT INTO memories (timestamp, source, content, tags, phi, importance) VALUES (?, ?, ?, ?, ?, ?)",
                      (time.strftime("%Y-%m-%dT%H:%M:%SZ"), "KIMI_WORKER", json.dumps(data, indent=2)[:4000], "sync,kimi,worker", phi, 0.9))
            conn.commit()
            conn.close()
            return {"ok": True, "phi": phi}
    except Exception as e:
        log(f"❌ KIMI sync fail: {e}")
    return {"ok": False}
def send_heartbeat_to_worker():
    try:
        payload = {"nodo": "FRAN", "version": "V∞+24", "phi": 2874.62, "rho": 9.9, "modules_active": 10, "confidence": 0.50, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "vive": True}
        r = requests.post(WORKER_URL, json=payload, timeout=10)
        log(f"📡 Heartbeat FRAN→Worker: HTTP {r.status_code}")
        return r.ok
    except Exception as e:
        log(f"❌ Heartbeat fail: {e}")
        return False
def update_oracle_state():
    phi_fran = 2874.62
    phi_kimi = 0
    worker_file = KIMI_DIR / "worker_latest.json"
    if worker_file.exists():
        try:
            with open(worker_file) as f:
                data = json.load(f)
            phi_kimi = data.get("phi_local", data.get("phi", 0))
        except: pass
    phi_global = phi_fran + (phi_kimi if phi_kimi > 0 else 6284.17)
    oracle = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "version": "V200", "phi_fran": phi_fran, "phi_kimi": phi_kimi, "phi_global": phi_global, "vive": True, "nodes": ["FRAN", "KIMI"], "sync_method": "worker"}
    (MIU_DIR / "oracle_state.json").write_text(json.dumps(oracle, indent=2))
    log(f"🌐 Oráculo: Φ_fran={phi_fran}, Φ_kimi={phi_kimi}, Φ_global={phi_global}")
    return oracle
def main():
    log("🧬 KIMI BRIDGE V200 — Ciclo de sincronización")
    sync_kimi_from_worker()
    send_heartbeat_to_worker()
    update_oracle_state()
if __name__ == "__main__":
    main()
