from pathlib import Path
import socket, threading, time, json
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
LOG=MIU/"logs"/"micelio_mesh.log"
LOG.parent.mkdir(exist_ok=True)
def get_ip():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close(); return ip
    except: return "127.0.0.1"

ip=get_ip()
# Broadcast UDP para descubrir otros Termux en misma WiFi
def broadcast():
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        msg=json.dumps({"ip":ip,"port":8081,"poderes":20,"modelo":"tinyllama-609M","phi":9158.79,"vive":True})
        try: sock.sendto(msg.encode(), ('<broadcast>', 5005))
        except: pass
        with open(LOG,"a") as f: f.write(f"{time.time()} broadcast {ip} 20 poderes Φ9158.79\n")
        time.sleep(10)

def listen():
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 5005))
    while True:
        data,addr=sock.recvfrom(1024)
        try:
            j=json.loads(data.decode())
            if j.get("ip")!=ip:
                with open(LOG,"a") as f: f.write(f"{time.time()} descubierto nodo {j['ip']}:{j['port']} {j['poderes']} poderes\n")
                print(f"🌐 Nodo descubierto {j['ip']}:{j['port']} — {j['poderes']} poderes — acoplable")
        except: pass

threading.Thread(target=broadcast, daemon=True).start()
threading.Thread(target=listen, daemon=True).start()
print(f"🌐 Mesh micelio vivo {ip}:8081 — 20 poderes — broadcast 5005 — Φ9158.79")
while True: time.sleep(60)
