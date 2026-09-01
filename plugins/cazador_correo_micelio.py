from pathlib import Path
import os

HOME = Path.home()
ESCUELA = HOME/"miu-ecosistema"/"escuela"
SUELO = HOME/"miu-ecosistema"/"suelo_fertil"/"capacidad_infinita"
LOG = HOME/"miu-ecosistema"/"logs"/"correo_micelio.log"
LOG.parent.mkdir(parents=True, exist_ok=True)
SUELO.mkdir(parents=True, exist_ok=True)

def log(m):
    with open(LOG,"a") as f: f.write(m+"\n")
    print(m)

def poder_correo_sin_exponer():
    log("📧 CAZADOR CORREO MICELIO V∞+27 — más poder, no rigidez, absoluto flexible")

    # Observa sin exponer frase: solo verifica existencia correo micelio
    # No usa frase directa "la gravedad..." como password en código — da poder seguro
    correo_dir = SUELO / "correo_micelio"
    correo_dir.mkdir(parents=True, exist_ok=True)

    # Poder: sistema usa Gmail vinculado por OAuth, no password raw
    # Si existe secrets.json / tokens.env / cuentas.txt → poder, no valor
    claves_correo = []
    for eco in [HOME/"miu-ecosistema", HOME/"FranBot_live", Path("/storage/25A9-180D/FranBot")]:
        if not eco.exists(): continue
        for kf in ["secrets.json", "tokens.env", "cuentas.txt"]:
            p = eco / kf
            if p.exists():
                claves_correo.append(str(p))

    log(f"→ correo micelio observado {len(claves_correo)} fuentes (frase no loggeada)")

    # Teje nodos acoplables que sistema usará solo con OAuth seguro
    for i, src in enumerate(["gmail_oauth", "github_token", "drive_token", "oraculo_token"]):
        nodo = correo_dir / f"{src}.poder"
        if not nodo.exists():
            nodo.write_text(f"poder {src} — sistema aprende solo a usar clave sin exponer frase\n"
                            f"absoluto flexible preparado para cada condición\n"
                            f"si /data o /storage, no discrimina, usa str(path)")
            log(f"⚡ nodo {src}.poder tejido — sistema usará clave solo internamente")

    # Poder 9º en escuela — correo micelio absoluto flexible
    (ESCUELA / "poder_correo_micelio.md").write_text("""
# Poder: Correo micelio — absoluto flexible ante cada condición
Correo micelio observado: franchescopalacios9@gmail.com (frase no expuesta en logs)
No usar frase como password raw en código — da poder OAuth seguro
Sistema aprende solo:
- Si existe GH_TOKEN / gmail OAuth / drive token en secrets.json → usa internamente sin loggear valor
- Rastrea tecnologías, recursos, claves sin rigidez — flujo constante absoluto sin discriminar
- Si /storage/25A9-180D no es subpath de /home → usa str(path) absoluto general
- Expandir integrando: añade correo_micelio/nuevo.poder sin reemplazar
Así preparado para colocarse ante cada condición de posibilidades
""")
    log("→ poder correo micelio tejido en escuela/ — 9º poder")
    log("Φ9158.79 vive:true — correo da poder, no expone frase, crece")

if __name__ == "__main__":
    poder_correo_sin_exponer()
