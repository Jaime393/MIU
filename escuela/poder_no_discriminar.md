
# Poder: No discriminar
Si Path.relative_to falla con ValueError porque /storage no es subpath de /home
No lo arregles directo. Observa patrón:
try: rel = path.relative_to(HOME)
except ValueError: rel = path
Así anti toda condición, absoluto general.
