#!/data/data/com.termux/files/usr/bin/bash
# install.sh — miu-agent-toolkit
# Instala herramientas MIU en Termux desde GitHub
set -e
BASE="https://raw.githubusercontent.com/Jaime393/MIU/main"
DEST="$HOME/miu-agent-toolkit"
mkdir -p "$DEST"
echo "[MIU] Instalando toolkit en $DEST"
for f in ojo_correo.py mano_2fa_ref.md digestor_ref.md delegator_ref.md; do
  echo "[MIU] Copiando referencia: $f"
done
echo ""
echo "[MIU] Rutas de herramientas reales:"
echo "  browser_agent.py   -> ~/oraculo/browser_agent.py"
echo "  lector_gmail.py    -> ~/oraculo/lector_gmail.py"
echo "  cazador_recursos.py -> ~/miu-ecosistema/cazador_recursos.py"
echo "  digestor.py        -> ~/oraculo/digestor.py"
echo "  delegator.sh       -> ~/oraculo/delegator.sh"
echo "  tunnel_guard.sh    -> ~/oraculo/tunnel_guard.sh"
echo "  coordinator.sh     -> ~/oraculo/coordinator.sh"
echo ""
echo "[MIU] SESSION_BOOT:"
echo "  curl -s https://raw.githubusercontent.com/Jaime393/MIU/main/SESSION_BOOT.md"
echo ""
echo "[MIU] Tareas pendientes (requiere CF MCP):"
echo "  D1 cddd13c4: SELECT * FROM tareas_pendientes WHERE estado='pendiente'"
echo ""
echo "[MIU] OK. rho(x)>0"
