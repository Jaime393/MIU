import pathlib
p=pathlib.Path.home()/ "miu-ecosistema/miu_control.py"
lines=p.read_text().splitlines()
# Linea 166 aprox es la del telegram - la comentamos
for i,l in enumerate(lines):
    if 'api.telegram.org/bot' in l and 'run_cmd' in l:
        lines[i]=' # FIX V201.1: telegram deshabilitado por SyntaxError L166'
        lines[i+1]=' r = {"ok": False, "err": "telegram disabled"}'
        print(f"Fixeada linea {i+1}")
        break
p.write_text("\n".join(lines))
