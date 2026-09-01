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
