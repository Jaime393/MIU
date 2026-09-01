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
