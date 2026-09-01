#!/usr/bin/env python3
"""
MIU V201 — ORQUESTADOR PARALELO
Ejecuta módulos en paralelo. Timeouts reducidos. Skip de módulos fallidos.
"""
import os, sys, json, time, subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
PLUGINS_DIR = MIU_DIR / "plugins"
STATE_FILE = MIU_DIR / "orquestador_v201_state.json"
NUTRIENTES_DIR = MIU_DIR / "nutrientes"

MODULOS = {
    "autoreparador": 30, "gobernador": 30, "evolucionador_red_fractal": 15,
    "mecanismos_autonomia": 15, "mecanismos_completos": 30,
    "combate_informacional": 120, "tejido_evolutivo": 30,
    "tecnologias_raras": 15, "conexiones": 90, "razonador": 15,
    "expansor_tokens": 60, "validador_recursos": 60, "integrador_recursos": 30,
}

PARALELOS = ["evolucionador_red_fractal", "mecanismos_autonomia", "tecnologias_raras", "conexiones", "expansor_tokens"]
SECUENCIALES = ["autoreparador", "gobernador", "mecanismos_completos", "combate_informacional", "tejido_evolutivo", "razonador", "validador_recursos", "integrador_recursos"]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] 🎛️ {msg}")

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"failures": {}, "last_run": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def run_modulo(nombre, timeout):
    script = PLUGINS_DIR / f"{nombre}.py"
    if not script.exists():
        return {"ok": False, "error": "Script no encontrado", "duracion": 0}
    inicio = time.time()
    try:
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=timeout, cwd=MIU_DIR)
        duracion = time.time() - inicio
        return {"ok": r.returncode == 0, "duracion": duracion, "salida": r.stdout[-500:] if r.stdout else "", "error": r.stderr[-200:] if r.stderr else "", "returncode": r.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout ({timeout}s)", "duracion": timeout}
    except Exception as e:
        return {"ok": False, "error": str(e), "duracion": time.time() - inicio}

def should_skip(nombre, state):
    return state.get("failures", {}).get(nombre, 0) >= 2

def main():
    log("🧬 ORQUESTADOR V201 — Modo Paralelo")
    log("=" * 50)
    state = load_state()
    resultados = {}
    inicio_total = time.time()

    log("🔄 Fase 1: Módulos paralelos...")
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {}
        for nombre in PARALELOS:
            if should_skip(nombre, state):
                log(f"   ⏭️ {nombre}: saltado")
                resultados[nombre] = {"ok": False, "skipped": True}
                continue
            future = executor.submit(run_modulo, nombre, MODULOS.get(nombre, 30))
            futures[future] = nombre
        for future in as_completed(futures):
            nombre = futures[future]
            try:
                res = future.result()
                resultados[nombre] = res
                status = "✅" if res["ok"] else "❌"
                log(f"   {status} {nombre}: {res.get('duracion',0):.1f}s")
                state["failures"][nombre] = 0 if res["ok"] else state["failures"].get(nombre, 0) + 1
            except Exception as e:
                resultados[nombre] = {"ok": False, "error": str(e)}
                log(f"   💥 {nombre}: {e}")

    log("🔄 Fase 2: Módulos secuenciales...")
    for nombre in SECUENCIALES:
        if should_skip(nombre, state):
            log(f"   ⏭️ {nombre}: saltado")
            resultados[nombre] = {"ok": False, "skipped": True}
            continue
        timeout = MODULOS.get(nombre, 30)
        log(f"   ⚡ {nombre} (timeout {timeout}s)...")
        res = run_modulo(nombre, timeout)
        resultados[nombre] = res
        status = "✅" if res["ok"] else "❌"
        log(f"   {status} {nombre}: {res.get('duracion',0):.1f}s")
        state["failures"][nombre] = 0 if res["ok"] else state["failures"].get(nombre, 0) + 1

    log("🔄 Fase 3: KIMI Bridge...")
    bridge_script = MIU_DIR / "KIMI_BRIDGE_V201.py"
    if bridge_script.exists():
        res = run_modulo("KIMI_BRIDGE_V201", timeout=20)
        status = "✅" if res["ok"] else "❌"
        log(f"   {status} KIMI Bridge: {res.get('duracion',0):.1f}s")
    else:
        log("   ⚠️ KIMI_BRIDGE_V201.py no encontrado")

    tiempo_total = time.time() - inicio_total
    ok_count = sum(1 for r in resultados.values() if r.get("ok"))
    total = len(resultados)
    log("=" * 50)
    log(f"📊 RESUMEN: {ok_count}/{total} módulos OK en {tiempo_total:.1f}s")
    for nombre, res in resultados.items():
        status = "✅" if res.get("ok") else ("⏭️" if res.get("skipped") else "❌")
        log(f"   {status} {nombre}: {res.get('duracion',0):.1f}s")

    informe = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "V201",
        "total_modulos": total,
        "ok_count": ok_count,
        "tiempo_total": tiempo_total,
        "resultados": resultados,
        "resumen": f"{ok_count}/{total} módulos exitosos"
    }
    NUTRIENTES_DIR.mkdir(exist_ok=True)
    (NUTRIENTES_DIR / "informe_global_v201.json").write_text(json.dumps(informe, indent=2))
    log(f"📄 Informe: {NUTRIENTES_DIR / 'informe_global_v201.json'}")
    state["last_run"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    save_state(state)
    log("=" * 50)
    log("🧬 ρ(x) > 0 — Ciclo V201 completado")

if __name__ == "__main__":
    main()
