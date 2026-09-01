#!/bin/bash
# Chat de control — escribe ideas y el sistema las ejecuta
cd ~/miu-ecosistema
echo "🧠 CHAT DE CONTROL — Escribe una idea y presiona Enter"
echo "   Ejemplos: 'escanea', 'github', 'conversa', 'repara', 'guerra', 'absorbe'"
echo "   Escribe 'salir' para cerrar"
echo ""

while true; do
    read -p "💡 Tú: " idea
    if [[ "$idea" == "salir" ]]; then
        break
    fi
    echo "$idea" >> logs/chat_active.log
    echo "📤 Idea enviada al micelio. Espera un momento..."
    python3 plugins/escucha_ideas.py
    echo ""
done
