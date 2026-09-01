from pathlib import Path
import subprocess, shutil

HOME = Path.home()
ECOS = [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("/storage/25A9-180D/FranBot")]
LOG = HOME/"miu-ecosistema"/"logs"/"flujo_constante.log"
LOG.parent.mkdir(parents=True, exist_ok=True)

def log(m):
    with open(LOG, "a") as f: f.write(m+"\n")
    print(m)

def buscar_grietas_y_tejer_suelo():
    grietas = []
    browsers = ["termux-open", "xdg-open", "curl", "wget", "lynx", "w3m"]
    for b in browsers:
        if shutil.which(b):
            grietas.append(f"browser:{b}")

    # absoluto general: no discrimina ruta, usa str() anti ValueError
    for eco in ECOS:
        if not eco.exists(): continue
        for keyfile in ["secrets.json", "cuentas.txt", "claves_ssh.json", "tokens.env", "config.json"]:
            kf = eco / keyfile
            if kf.exists() and kf.stat().st_size > 10:
                try:
                    rel = kf.relative_to(HOME)
                except ValueError:
                    rel = kf  # absoluto general, no discrimina /storage/25A9-180D
                grietas.append(f"cuenta:{rel}")

    suelo = HOME / "miu-ecosistema" / "suelo_fertil"
    suelo.mkdir(parents=True, exist_ok=True)

    for eco in ECOS:
        if not eco.exists(): continue
        for mapa in eco.glob("mapa_universal_*.txt"):
            dest = suelo / mapa.name
            if not dest.exists():
                try:
                    dest.symlink_to(mapa)
                    log(f"🌱 suelo fértil tejido: {mapa.name}")
                except Exception as e:
                    try:
                        shutil.copy(mapa, dest)
                        log(f"🌱 suelo fértil copiado: {mapa.name}")
                    except: pass
    return grietas, suelo

def flujo_constante_nodos():
    log("🌊 FLUJO CONSTANTE RETROALIMENTADO V∞+27 — absoluto general anti toda condición")
    grietas, suelo = buscar_grietas_y_tejer_suelo()
    log(f"→ grietas {len(grietas)}: {grietas[:15]}")
    log(f"→ suelo fértil {suelo} con {len(list(suelo.iterdir()))} enlaces")

    # salida a red absoluta — no discrimina, prueba todos
    for url in ["https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global", "https://8.8.8.8"]:
        try:
            r = subprocess.run(["curl","-s","--max-time","8",url], capture_output=True, text=True)
            if "vive" in r.stdout or len(r.stdout)>10:
                log(f"✓ salida red OK via curl {url} {len(r.stdout)}B")
                (suelo / "ultimo_global.json").write_text(r.stdout[:5000])
                break
        except Exception as e:
            log(f"· {url} {e}")

    # nodo heartbeat absoluto
    hb = HOME/"miu-ecosistema"/"plugins"/"heartbeat_flujo.py"
    hb.write_text('from pathlib import Path\nimport time\nLOG=Path.home()/"miu-ecosistema"/"logs"/"flujo_constante.log"\nwhile True:\n    open(LOG,"a").write("💓 flujo constante\\n")\n    time.sleep(60)\n')
    log(f"✓ heartbeat absoluto {hb}")

    log("Φ9158.79 vive:true — absoluto general no discrimina")

if __name__ == "__main__":
    flujo_constante_nodos()
