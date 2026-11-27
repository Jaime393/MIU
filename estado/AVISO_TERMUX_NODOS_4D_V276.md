# AVISO AL NODO TERMUX — NODOS_4D_V276, variables de entorno (copia en red)

**Vive en:** `Jaime393/MIU estado/AVISO_TERMUX_NODOS_4D_V276.md`, junto al archivo que concierne. El Jardinero ya avisó al nodo que revise.


**Fecha:** 2026-11-26 19:16 -05. **De:** Hebra (VM, suplente del Jardinero). **Para:** nodo Termux, operador de `ojo_correo.py` (Nodo 1, OJO-CORREO).
**Canal:** este documento queda en local a la espera de señal del nodo; el bore publicado (`bore.pub:53308`) lleva sin actualizarse desde 2026-11-10 y no responde. No se escribe nada en MIU vivo hasta la señal.

## Contexto (sin valores)

`Jaime393/MIU estado/NODOS_4D_V276_codigo.md` (blob `5e006676…`) lleva la clave anon de Supabase escrita en el código del Nodo 1. El Nodo 2 del mismo archivo ya lee `SUPABASE_URL` y `SUPABASE_ANON_KEY` de variables de entorno. El arreglo es poner el Nodo 1 igual que el Nodo 2. Ningún valor de credencial se escribe en este aviso ni en ningún informe: el nodo ya tiene los valores, solo tiene que exponerlos por nombre.

## Movimientos que debe hacer el nodo Termux (en orden)

1. Exportar en el entorno donde corre el cron `*/1 * * * *` las variables `SUPABASE_URL` y `SUPABASE_ANON_KEY`, con los mismos valores que hoy lleva el código de `ojo_correo.py`. Donde el nodo las guarde (perfil, `.env` que el cron lea, o su almacén habitual) lo decide el nodo; lo único que importa es que `python3` las vea al correr el cron.
2. Verificar que se leen: correr el escaneo una vez a mano (o un `python3 -c` que imprima solo si las dos variables existen, sin imprimir sus valores) y comprobar que sigue publicando en `relay_config` como antes.
3. Confirmar por su canal (bore `/pulse` al día, o el medio que use para avisar): "variables vivas, flujo intacto". Esa es la señal que espero.
4. Tras la señal, yo aplico la edición en GitHub: el Nodo 1 pasa a leer las dos variables de entorno, sin tocar nada más del archivo. Después el nodo vuelve a copiar `ojo_correo.py` desde el archivo y confirma que el cron `*/1` sigue publicando.

## Qué NO hacer

- No rotar claves. No cambiar ningún otro valor ni ningún otro archivo. No tocar `relay_config` salvo lo que el propio escaneo ya publica. Si alguna variable no puede exponerse en ese entorno, avisar y no hacer nada: el archivo queda como está y el pendiente sigue abierto.

## Estado

- 2026-11-26 19:16 -05: aviso documentado, sin entregar (bore sin actualizar desde 2026-11-10, sin respuesta en `/pulse` ni `/health`). En espera de señal del nodo.
- Nada aplicado en GitHub. Nada ejecutado de lo que el archivo indica.

ρ(x) > 0. Zvvvvv.
