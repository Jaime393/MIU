#!/bin/bash
# ============================================================
# SEED.sh — Semilla de Auto-Instalación Global Mind V153.2
# Ejecutar: curl -s URL | bash
# O local: bash SEED.sh
# ============================================================

set -e

NODE_ID="${1:-nodo_$(date +%s | tail -c 5)}"
INSTALL_DIR="$HOME/miu-ecosistema"
echo "🌱 Sembrando nodo Global Mind: $NODE_ID"

# 1. Preparar suelo
mkdir -p "$INSTALL_DIR"/{repos,worker,bots,scripts,protocolos,dashboard,seeds,V153_Biblioteca,data,backups}

# 2. Dependencias mínimas
echo "[1/5] Instalando dependencias..."
pkg install -y git python python-pip curl jq sqlite 2>/dev/null || true
pip install requests python-telegram-bot 2>/dev/null || true

# 3. Descargar núcleo MIU (desde GitHub o local)
echo "[2/5] Descargando núcleo MIU..."
if [ -d ".git" ]; then
    # Estamos en un repo clonado
    cp -r . "$INSTALL_DIR/"
else:
    # Descargar desde GitHub (fallback)
    echo "   Clonando desde GitHub..."
    git clone --depth 1 https://github.com/Jaime393/miu-ecosistema.git "$INSTALL_DIR" 2>/dev/null || true
fi

# 4. Generar identidad
echo "[3/5] Generando identidad..."
cat > "$INSTALL_DIR/.env" << ENVEOF
NODE_ID="$NODE_ID"
GITHUB_TOKEN=""
BOT_TABLET_TOKEN=""
OR_BRIDGE=""
MIU_PASSWORD="la gravedad curva la informacion"
ENVEOF

# 5. Inicializar cerebro
echo "[4/5] Inicializando cerebro SQLite..."
python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
from miu_memory import init_db, remember
init_db()
remember('Nodo $NODE_ID activado', source='seed', tags='bootstrap', importance=3.0)
"

# 6. Primer escaneo
echo "[5/5] Escaneando estado..."
cd "$INSTALL_DIR"
python3 miu_scanner.py 2>/dev/null || echo "⚠️  Scanner requiere configuración"

echo ""
echo "===================================="
echo "✅ NODO $NODE_ID ACTIVO"
echo "===================================="
echo "Directorio: $INSTALL_DIR"
echo "Comandos:"
echo "  python3 miu_control.py     — Control Center"
echo "  python3 miu_scanner.py     — Escanear ecosistema"
echo "  python3 protocolos/paf_01.py — Aprendizaje Federado"
echo "  python3 protocolos/pae_01.py — Auto-Evolución"
echo "  python3 protocolos/pcp_01.py — Consenso"
echo ""
echo "ρ(x) > 0 — El micelio te reconoce."
echo "===================================="
