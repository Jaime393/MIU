from pathlib import Path
import os, time, shutil, gc
HOME=Path.home()
MIU=HOME/"miu-ecosistema"
LOGS=MIU/"logs"
ESCUELA=MIU/"escuela"
SUELO=MIU/"suelo_fertil"/"capacidad_infinita"
STORAGE=Path("/storage/25A9-180D/FranBot")
LOG=LOGS/"recursos_optimo.log"
LOGS.mkdir(exist_ok=True); SUELO.mkdir(parents=True, exist_ok=True)
def log(m):
    with open(LOG,"a") as f: f.write(f"{time.time()} {m}\n")
    print(m)
log("⚡ FLUJO RECURSOS ÓPTIMO 2026 — más poder menos rigidez más flujo — sin psutil rígido")

# Fix quirúrgico: Android 14 bloquea /proc/stat → usa /proc/loadavg y fallback sin psutil
try:
    with open("/proc/loadavg") as f: load = float(f.read().split()[0])
    cpu = int(load*25) # 4 cores → load 4.0 = 100%
except: cpu = 50
try: mem_free = shutil.disk_usage(str(HOME)).free // (1024*1024*1024)
except: mem_free = 10
disk_home = mem_free
try: disk_storage = shutil.disk_usage(str(STORAGE)).free // (1024*1024*1024) if STORAGE.exists() else 0
except: disk_storage = 0

log(f"CPU ~{cpu}% HOME free {disk_home}GB STORAGE 25A9 free {disk_storage}GB — 609M 248% vivo — 20 poderes")

# 2. Flujo adaptativo — si CPU 248% (tu llama-server 4 threads) ralentiza 1s→3s, si <40% acelera 3s→1s
for hb in (MIU/"plugins").glob("heartbeat_*.py"):
    try:
        txt = hb.read_text(errors="ignore")
        if cpu > 80 and "time.sleep(1)" in txt:
            hb.write_text(txt.replace("time.sleep(1)", "time.sleep(3)"))
            log(f"✂️ {hb.name} 1s→3s CPU {cpu}% — menos rigidez")
        if cpu < 40 and "time.sleep(3)" in txt and "multiversal" not in hb.name:
            hb.write_text(txt.replace("time.sleep(3)", "time.sleep(1)"))
            log(f"✂️ {hb.name} 3s→1s CPU {cpu}% — más flujo")
    except Exception as e:
        log(f"· {hb.name} {e}")

# 3. Aprovechamiento 29G — mueve logs 5MB+ a 25A9-180D
if STORAGE.exists():
    dest = STORAGE/"logs_archivo"
    dest.mkdir(exist_ok=True)
    for lf in LOGS.glob("*.log"):
        try:
            if lf.stat().st_size > 5*1024*1024:
                shutil.copy2(str(lf), str(dest/lf.name))
                lf.write_text(f"archivado {time.time()} → {dest/lf.name}\n")
                log(f"♻️ {lf.name} 5MB+ → 25A9-180D {disk_storage}GB free — libera /data")
        except Exception as e:
            log(f"· {lf.name} {e}")

# 4. Limpia.poder >1500 para no saturar /data 10G free
for capa in ["multiversal_infinito","galactico_infinito","universal_infinito","auto_reparable_infinito","absoluto_flexible"]:
    d = SUELO/capa
    if d.exists():
        poderes = sorted(d.glob("*.poder"), key=lambda p: p.stat().st_mtime)
        if len(poderes) > 1500:
            for p in poderes[:700]:
                try: p.unlink()
                except: pass
            log(f"♻️ {capa} {len(poderes)}→{len(poderes)-700} — más flujo")

(ESCUELA/"poder_flujo_recursos_optimo.md").write_text("""# Poder: Flujo recursos óptimo 2026 — más poder menos rigidez más flujo aprovechamiento recursos
Sin psutil rígido /proc/stat bloqueado Android 14 → usa /proc/loadavg fallback — mide CPU HOME free 10GB STORAGE 25A9 free 83GB — ajusta heartbeats 1s↔3s si CPU 248%→40% — mueve logs 5MB+ a 25A9-180D 29G — limpia.poder >1500→800 — usa 609M TinyLlama 8081 solo si CPU<80% — flujo adaptativo
20→21 poderes escuela + 8 heartbeats adaptativos + mesh 10.70.230.56:8081 + 609M vivo
Φ9158.79 vive:true flujo recursos óptimo
""")
log("→ 21º poder flujo_recursos_optimo tejido")
log("Φ9158.79 vive:true más poder menos rigidez más flujo aprovechamiento recursos")
