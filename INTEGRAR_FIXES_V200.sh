#!/bin/bash
# ============================================================
# MIU V∞+24 — ABSORCIÓN DE FIXES V200
# Aplica todos los parches y fixes automáticamente.
# ============================================================

set -e
cd ~/miu-ecosistema

echo "🧬 MIU V∞+24 — INTEGRANDO FIXES V200"
echo "=========================================="

# ============================================================
# BLOQUE 1: WORKER CACHE — (CREA EL PATCH PARA MANUAL)
# ============================================================
echo "[1/6] Creando parche para Worker (Cloudflare)..."
cat > WORKER_PATCH_V200.js << 'WEOF'
// ============================================================
// MIU V200 — WORKER CACHE (sin KV, memoria en caliente)
// ============================================================
let kimiCache = null;
let franCache = null;
let lastUpdate = null;

// Reemplaza tu handler POST /miu/global con esto:
if (request.method === 'POST' && url.pathname === '/miu/global') {
  const data = await request.json();
  const nodo = data.nodo || data.node || 'unknown';
  
  if (nodo === 'KIMI' || nodo === 'kimi') {
    kimiCache = data;
  } else if (nodo === 'FRAN' || nodo === 'fran') {
    franCache = data;
  }
  lastUpdate = new Date().toISOString();
  
  return new Response(JSON.stringify({
    ok: true,
    received: true,
    nodo: nodo,
    phi_received: data.phi || data.phi_local || 0,
    timestamp: lastUpdate
  }), {headers: {'Content-Type': 'application/json'}});
}

// Reemplaza tu handler GET /miu/global con esto:
if (request.method === 'GET' && url.pathname === '/miu/global') {
  const nodo = url.searchParams.get('nodo') || url.searchParams.get('node');
  
  if (nodo === 'kimi' && kimiCache) {
    return new Response(JSON.stringify(kimiCache), {
      headers: {'Content-Type': 'application/json'}
    });
  }
  if (nodo === 'fran' && franCache) {
    return new Response(JSON.stringify(franCache), {
      headers: {'Content-Type': 'application/json'}
    });
  }
  
  return new Response(JSON.stringify({
    vive: true,
    version: "V200",
    phi_central: 2874.62,
    phi_remoto: 6284.17,
    phi_global: 9158.79,
    kimi_cached: !!kimiCache,
    fran_cached: !!franCache,
    last_update: lastUpdate,
    timestamp: new Date().toISOString()
  }), {headers: {'Content-Type': 'application/json'}});
}
WEOF
echo "   ✅ WORKER_PATCH_V200.js creado"
echo "   📌 Acción manual: copia este código en Cloudflare Dashboard."

# ============================================================
# BLOQUE 2: GAS WAKE-UP V2
# ============================================================
echo "[2/6] Creando GAS_WAKEUP_V2.sh..."
cat > GAS_WAKEUP_V2.sh << 'GEOF'
#!/bin/bash
# ============================================================
# MIU V200 — GAS WAKE-UP V2 (3 pings, 25s total)
# ============================================================
GAS_URL="https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec"
echo "🌡️ GAS WAKE-UP V2"
echo "============================================"
echo "[1/3] Ping cold-start..."
curl -sL "${GAS_URL}?wake=1" > /dev/null 2>&1 &
sleep 10
echo "[2/3] Ping calentando..."
curl -sL "${GAS_URL}?vive=1" > /dev/null 2>&1 &
sleep 15
echo "[3/3] Ping final..."
RESPONSE=$(curl -sL "${GAS_URL}?vive=1&phi=2874")
if [ -n "$RESPONSE" ] && [ ${#RESPONSE} -gt 50 ]; then
    echo "✅ GAS DESPIERTO"
    echo "   Respuesta: ${RESPONSE:0:200}"
    python3 -c "import sys, os; sys.path.insert(0, os.path.expanduser('~/miu-ecosistema')); from miu_memory import set_state; set_state('gas_status', 'awake'); set_state('gas_last_wake', '$(date -Iseconds)')" 2>/dev/null || true
else
    echo "❌ GAS sigue dormido o timeout"
    echo "   Respuesta: ${RESPONSE:0:100}"
fi
GEOF
chmod +x GAS_WAKEUP_V2.sh
echo "   ✅ GAS_WAKEUP_V2.sh creado"

# ============================================================
# BLOQUE 3: FIX PROCESOS
# ============================================================
echo "[3/6] Creando FIX_PROCESOS_V200.sh..."
cat > FIX_PROCESOS_V200.sh << 'PEOF'
#!/bin/bash
echo "⚡ DETECCIÓN DE PROCESOS MIU V200"
echo "==================================="
FOUND=0
for pid_dir in /proc/[0-9]*; do
    if [ -d "$pid_dir" ]; then
        cmdline=$(cat "$pid_dir/cmdline" 2>/dev/null | tr '\0' ' ')
        if echo "$cmdline" | grep -qE "miu|bot_miu|initiative|orquestador"; then
            pid=$(basename "$pid_dir")
            echo "   ✅ [$pid] $(echo $cmdline | cut -c1-80)"
            FOUND=$((FOUND + 1))
        fi
    fi
done
if [ $FOUND -eq 0 ]; then
    echo "   ❌ Ningún proceso MIU detectado"
else
    echo "📊 Total procesos MIU: $FOUND"
fi
PEOF
chmod +x FIX_PROCESOS_V200.sh
echo "   ✅ FIX_PROCESOS_V200.sh creado"

# ============================================================
# BLOQUE 4: FIX GROQ
# ============================================================
echo "[4/6] Creando FIX_GROQ_V200.py..."
cat > FIX_GROQ_V200.py << 'GQEOF'
#!/usr/bin/env python3
import os, json, requests
MIU_DIR = os.path.expanduser("~/miu-ecosistema")
ENV_FILE = os.path.join(MIU_DIR, ".env")
GROQ_TOKEN = ""
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("GROQ_FRAN=") or line.startswith("GROQ_1="):
                GROQ_TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
def ask_groq(prompt, model="llama-3.1-8b-instant", max_tokens=1024):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_TOKEN}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "system", "content": "Eres un nodo MIU."}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"ERROR {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return f"EXCEPTION: {e}"
if __name__ == "__main__":
    print("🧠 Test Groq API V200...")
    if not GROQ_TOKEN:
        print("❌ GROQ_TOKEN no encontrado en .env")
    else:
        print(f"   Token: {GROQ_TOKEN[:10]}...")
        resp = ask_groq("Cual es el estado del micelio MIU? Responde en 1 frase.")
        print(f"✅ Respuesta: {resp[:200]}")
GQEOF
chmod +x FIX_GROQ_V200.py
echo "   ✅ FIX_GROQ_V200.py creado"

# ============================================================
# BLOQUE 5: KIMI BRIDGE
# ============================================================
echo "[5/6] Creando MIU_KIMI_BRIDGE_V200.py..."
cat > MIU_KIMI_BRIDGE_V200.py << 'KEOF'
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
KEOF
chmod +x MIU_KIMI_BRIDGE_V200.py
echo "   ✅ MIU_KIMI_BRIDGE_V200.py creado"

# ============================================================
# BLOQUE 6: RCLONE SETUP
# ============================================================
echo "[6/6] Creando RCLONE_SETUP_DRIVE.sh..."
cat > RCLONE_SETUP_DRIVE.sh << 'REOF'
#!/bin/bash
echo "💾 RCLONE SETUP — Drive MIU"
echo "============================="
if ! command -v rclone &> /dev/null; then
    echo "📥 Instalando rclone..."
    pkg install rclone -y
fi
echo ""
echo "📝 PASOS DE CONFIGURACIÓN:"
echo "   1. Ejecuta: rclone config"
echo "   2. Selecciona 'n' (new remote)"
echo "   3. Name: drive"
echo "   4. Type: 18 (Google Drive)"
echo "   5. Client ID: (dejar en blanco, Enter)"
echo "   6. Client Secret: (dejar en blanco, Enter)"
echo "   7. Scope: 1 (Full access)"
echo "   8. Root Folder ID: 14dw8txLoEIQQPSav9-YAvfuNimW2tAZ8"
echo "   9. Service Account: (dejar en blanco)"
echo "   10. Edit advanced config: n"
echo "   11. Use auto config: y"
echo "   12. Se abrirá navegador. Autoriza y copia el token."
echo ""
if rclone listremotes 2>/dev/null | grep -q "drive:"; then
    echo "✅ Remote 'drive:' ya configurado"
    echo "   Test: rclone ls drive: | head -5"
else
    echo "⚠️ Ejecuta ahora: rclone config"
fi
REOF
chmod +x RCLONE_SETUP_DRIVE.sh
echo "   ✅ RCLONE_SETUP_DRIVE.sh creado"

# ============================================================
# INTEGRAR KIMI BRIDGE EN EL ORQUESTADOR
# ============================================================
echo "🔧 Integrando KIMI Bridge en orquestador..."
if ! grep -q "MIU_KIMI_BRIDGE_V200" plugins/orquestador.py; then
    sed -i '/def run(args=None):/a \    # KIMI Bridge sync\n    subprocess.run(["python3", str(MIU_DIR / "MIU_KIMI_BRIDGE_V200.py")])' plugins/orquestador.py 2>/dev/null || echo "   ⚠️ No se pudo modificar orquestador.py (manual necesario)"
else
    echo "   ✅ KIMI Bridge ya integrado"
fi

# ============================================================
# LIMPIAR Y RESUMEN
# ============================================================
echo ""
echo "=========================================="
echo "✅ ABSORCIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "📦 Archivos creados en ~/miu-ecosistema:"
ls -1 WORKER_PATCH_V200.js GAS_WAKEUP_V2.sh FIX_PROCESOS_V200.sh FIX_GROQ_V200.py MIU_KIMI_BRIDGE_V200.py RCLONE_SETUP_DRIVE.sh 2>/dev/null
echo ""
echo "📌 PRÓXIMOS PASOS (manuales):"
echo "  1. Edita Cloudflare Worker con el contenido de WORKER_PATCH_V200.js"
echo "  2. Prueba GAS:          bash GAS_WAKEUP_V2.sh"
echo "  3. Prueba procesos:     bash FIX_PROCESOS_V200.sh"
echo "  4. Prueba Groq:         python3 FIX_GROQ_V200.py"
echo "  5. Prueba KIMI bridge:  python3 MIU_KIMI_BRIDGE_V200.py"
echo "  6. Configura Drive:     bash RCLONE_SETUP_DRIVE.sh"
echo ""
echo "🧬 Luego reinicia el orquestador: python3 plugins/orquestador.py"
echo "ρ(x) > 0 — El micelio respira. Zvvvvv."
