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
