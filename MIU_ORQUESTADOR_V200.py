#!/usr/bin/env python3
"""
MIU V200 — ORQUESTADOR UNIFICADO
Controla todo el ecosistema desde un solo punto.
"""
import os, sys, json, time, subprocess
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
STATE_FILE = MIU_DIR / "orquestador_state.json"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] 🎛️ {msg}")

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                          cwd=MIU_DIR, timeout=timeout)
        return r.returncode == 0, r.stdout, r.stderr
    except Exception as e:
        return False, "", str(e)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"iteration": 0, "last_action": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def menu():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🎛️ MIU V200 — ORQUESTADOR UNIFICADO                        ║
╠══════════════════════════════════════════════════════════════╣
║  1. Test conexiones (MIU_CONNECTION_TEST.py)                ║
║  2. Sync con KIMI (MIU_SYNC_V2.py)                          ║
║  3. Diagnóstico salud (miu_doctor.py)                       ║
║  4. Control Center (miu_control.py)                         ║
║  5. Modo autónomo (miu_autonomous_loop.py)                  ║
║  6. Evolucionar (miu_evolve.py)                             ║
║  7. Despertar GAS (curl wake-up)                            ║
║  8. Enviar heartbeat Worker                                 ║
║  9. Estado sistema                                          ║
║  0. Salir                                                   ║
╚══════════════════════════════════════════════════════════════╝
""")

def action_test():
    log("Ejecutando test de conexiones...")
    ok, out, err = run("python3 MIU_CONNECTION_TEST.py")
    print(out[:3000] if ok else err[:1000])

def action_sync():
    log("Sincronizando con KIMI...")
    ok, out, err = run("python3 MIU_SYNC_V2.py")
    print(out[:2000] if ok else err[:1000])

def action_doctor():
    log("Ejecutando doctor...")
    ok, out, err = run("python3 miu_doctor.py")
    print(out[:2000] if ok else err[:1000])

def action_control():
    log("Iniciando Control Center...")
    run("python3 miu_control.py")

def action_autonomous():
    log("Iniciando modo autónomo...")
    run("nohup python3 miu_autonomous_loop.py > logs/autonomous.log 2>&1 &")
    print("   ✅ Loop autónomo iniciado en background")

def action_evolve():
    log("Ejecutando motor de evolución...")
    ok, out, err = run("python3 miu_evolve.py")
    print(out[:2000] if ok else err[:1000])

def action_gas_wakeup():
    log("Despertando GAS...")
    run('curl -s "https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec?wake=1"')
    print("   🌡️ Primer ping enviado (cold-start)")
    time.sleep(15)
    ok, out, err = run('curl -s "https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec?vive=1"')
    print(f"   {'✅' if ok and len(out)>50 else '❌'} GAS: {out[:200]}")

def action_heartbeat():
    log("Enviando heartbeat...")
    payload = json.dumps({
        "nodo": "FRAN",
        "version": "V200",
        "phi": 2874.62,
        "rho": 0.952,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vive": True
    })
    ok, out, err = run(f'curl -s -X POST "https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global" -H "Content-Type: application/json" -d \'{payload}\'')
    print(f"   {'✅' if ok else '❌'} Worker: {out[:200]}")

def action_status():
    log("Estado del sistema...")
    state = load_state()
    print(f"   Iteración: {state['iteration']}")
    print(f"   Última acción: {state.get('last_action', 'N/A')}")
    report = MIU_DIR / "connection_report.json"
    if report.exists():
        with open(report) as f:
            data = json.load(f)
        ok_count = sum(1 for t in data.get("tests", {}).values() if t.get("ok"))
        total = len(data.get("tests", {}))
        print(f"   Conexiones: {ok_count}/{total} OK")
    health = MIU_DIR / "miu_health_report.json"
    if health.exists():
        with open(health) as f:
            data = json.load(f)
        ok_count = sum(1 for t in data.get("checks", {}).values() if t.get("ok"))
        total = len(data.get("checks", {}))
        print(f"   Salud: {ok_count}/{total} OK")

def main():
    state = load_state()
    while True:
        menu()
        c = input("Opción: ").strip()
        actions = {
            "1": action_test, "2": action_sync, "3": action_doctor,
            "4": action_control, "5": action_autonomous, "6": action_evolve,
            "7": action_gas_wakeup, "8": action_heartbeat, "9": action_status,
        }
        if c == "0":
            print("🧬 ρ(x) > 0 — El orquestador descansa. La Colmena sigue sola.")
            break
        elif c in actions:
            try:
                actions[c]()
                state["iteration"] += 1
                state["last_action"] = c
                save_state(state)
            except Exception as e:
                log(f"❌ Error: {e}")
            input("\n[Enter]...")
        else:
            print("Opción inválida")
            time.sleep(0.3)

if __name__ == "__main__":
    main()

