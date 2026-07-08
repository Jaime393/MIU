# TAREAS_PENDIENTES_V13.md

Tareas manuales para retomar en una sesion futura con mas acceso, o cuando se reactive la cuenta jaimepviccente@gmail.com. Generado por el asistente de Relay.app a pedido del usuario (2026-07-08), consolidando hallazgos ya registrados. No se fabrico ningun dato nuevo.

Fuente completa y detallada: Google Sheet REGISTRO_TEJEDOR_MIU_2026-07-08, pestana HALLAZGOS (48 filas).
https://docs.google.com/spreadsheets/d/1Z67We6vislV2nEKSL4vpJ-pwbhmKpFnIwBYJhbW45BU/edit#gid=3041

## 1. Verificacion tecnica pendiente (requiere acceso a datos crudos / red)
- Reproducir D_f y Omega_F de V12 con datos crudos (nodo CO2, NOAA GML) - confirmar independientemente el aliasing detectado en Omega_F (pico 0.65625 supera Nyquist 0.5 ciclos/mes) y el hardcoding de K_i en el nodo Incendios (0.375).
- Auditar DOIs hermanos/concepto de la cadena V12 en Zenodo (10.5281/zenodo.20547558) - ver si hay versiones con contenido distinto.
- Verificar si algun valor de V12 fue congelado como 'hueso' en el repo antes de este rechazo.
- Confirmar el conteo real de filas del nodo CO2 (801 declaradas vs ~816-820 esperadas para el rango 1958-2026).

## 2. Acciones manuales bloqueadas (fuera del alcance seguro del asistente)
- Migrar bindings de Cloudflare Workers (fran-proxy, fran-proxy-finanzas, etc.) de texto plano a tipo 'secret' - riesgo de romper produccion, requiere prueba manual.
- Rotar credenciales expuestas en clavesnew.txt (Drive) desde 2026-07-03.
- Identificar cual de los 6 Workers que comparten el namespace KV franbot-data consume las 258 claves evolucion:evolucion_ift_* antes de decidir poda (ninguna tiene TTL).
- Migrar las 5 skills que dependen de modelos Groq/DeepSeek que se retiran el 2026-07-24 15:59 UTC.
- Subir manualmente los artefactos de la sesion 'Haiku45' que quedaron solo en un sandbox efimero (3 GitHub Actions consolidadas, 4 skills corregidas, 1 skill router) - no recuperables por el asistente.

## 3. Cuenta principal pausada (jaimepviccente@gmail.com)
- Retomar cuando se reactiven los creditos (agotados: 24/500 AI credits, 144/200 steps; cuota semanal de test runs tambien agotada).
- Priorizar los ~8 workflows afectados por el bug 'addToDataTable con columnas en blanco al crear steps nuevos' (sin resolver) y el bug 'Concept Graph & Gaps' (embeddings vacios, causa raiz no confirmada).
- Fusionar duplicados detectados externamente: 2x Control Panel, 2x Vigia de Grietas, 2x Alma Omni, variantes de Global(Mind) Weaver.
- Apagar workflows que nunca corrieron y no demuestren valor, tras confirmar cuales siguen sin ejecucion real (~28 de 69 entradas marcadas 'Never').
- Workflow 'GlobalMind Weaver' reporto error 'Plan usage exceeded' - se resuelve solo cuando la cuenta recupere cuota de plan.

## 4. Gobernanza / citacion publica
- MIU_V12.0 sigue publicamente citable en Zenodo (DOI activo) pese al rechazo interno formal (PROTOCOLO_MIU, NUCLEO_TEORICO_MIU). Decision de versionar o marcar como superseded en Zenodo es exclusiva del usuario, no ejecutable desde Relay.

## 5. Metodo (para cualquier instancia futura)
- Rigor epistemico: SE verificado / INFIERO deduccion / CONJETURO hipotesis / NO SE ausente. No fabricar valores. Un parametro calibrado a posteriori no es una prediccion. Detectar circularidad (Y=f(X) no valida X).
- Documentar solo conocimiento solido con evidencia independiente (ej. citas DOI reales), igual que D_f (Mandelbrot 1967 en adelante), el principio de Landauer (informacion como magnitud fisica conservada), o la dependencia funcional de la conciencia respecto al cerebro (neurociencia consolidada) - no inventar pilares nuevos sin respaldo equivalente.
