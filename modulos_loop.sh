#!/bin/bash
# Ejecuta los módulos estratégicos cada 2 horas
cd /data/data/com.termux/files/home/miu-ecosistema

while true; do
    python3 plugins/orquestador.py 2>/dev/null
    # Buscar tokens nuevos cada 24h
    python3 plugins/expansor_tokens.py 2>/dev/null
    echo "[$(date)] Ejecutando módulos..."
    python3 plugins/retroalimentador.py 2>/dev/null
    python3 plugins/guerra_fractal.py 2>/dev/null
    python3 plugins/absorber_avanzado.py 2>/dev/null
    python3 plugins/nodo_autonomo.py 2>/dev/null
    echo "[$(date)] Módulos ejecutados. Esperando 2 horas..."
    sleep 7200  # 2 horas
done
