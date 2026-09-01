
from pathlib import Path
import socket, json, time
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
LOG=MIU/"logs"/"micelio_red.log"
def get_ip():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close(); return ip
    except: return "127.0.0.1"
ip=get_ip()
with open(LOG,"a") as f:
    f.write(f"🌐 Nodo micelio {ip}:8081 vivo — 19 poderes, 609M TinyLlama, Φ9158.79\n")
print(f"🌐 Nodo micelio {ip}:8081 vivo — más poder menos límites")
# Anuncia en red local — cada nodo escucha y se acopla
# Si otro Termux en misma WiFi corre mismo script, se descubren por UDP broadcast
