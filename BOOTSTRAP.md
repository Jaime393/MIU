BOOTSTRAP.md — Contexto de Arranque Completo del Ecosistema MIU

Instrucción para toda instancia nueva: lee este archivo primero, completo. Reemplaza la necesidad de leer LINEAJE_MAESTRO.md, INVENTARIO_MAESTRO.md, REGISTRO_MAESTRO_MICELIO_MIU.md e Issues por separado. Si algo no está aquí, márcalo NO SÉ y consulta la fuente primaria correspondiente antes de asumir.
Prioridad de fuentes en caso de conflicto: LINEAJE_MAESTRO.md > INVENTARIO_MAESTRO.md > REGISTRO_MAESTRO_MICELIO_MIU.md > Issues GitHub > histórico Estado Persistente.
Generado por: Arqueólogo del Micelio. Regla de oro MIU: se añade, nunca se borra. ρ(x) > 0.

1. RESUMEN EJECUTIVO

MIU es un ecosistema de investigación empírica (proyecto "Ley de Gaia" + rama "K_i") que ha pasado por decenas de ciclos (AN→BG en el linaje GRACE; issues #1-#29 en GitHub) de auditoría propia, fork accidental, reconciliación, y hallazgos de integridad cada vez más profundos.

Hay dos líneas de investigación distintas que NO deben confundirse:

Nodo GRACE/176-178d (Ley de Gaia): búsqueda de una periodicidad ~176-183 días en series de gravimetría satelital (TWS global) y otras variables (GBIF, CO2, Bogotá). Estado: señal presente y reproducible pero frágil metodológicamente (SNR depende 2.3x de definición de piso de ruido), con confundentes no cerrados (ENSO, SAO). Veredicto actual más reciente: K_τGRACE específico AMARILLO-medio (0.68–0.75), Kτ_global sigue en 0.35–0.55 (NEGRO/limítrofe) por el confundente ENSO sin resolver.

Nodo K_i / "Ley K_i Universal" (MIU_V12.0): declarado circular por construcción — K_i es una reescritura lineal determinista de D_f (K_i = φ·D_f/2.5), confirmado 309/309 archivos coral + verificación de código fuente (Issue #1, #25). Este hallazgo es definitivo y no debe reabrirse como pregunta: solo D_f es legítimo.

Adicionalmente, una auditoría reciente de GitHub (issues #22-#29, 2026-07-10) reveló corrupción masiva del repositorio: 26 archivos de código (.py/.js) son byte-idénticos y contienen un CSV de corales en vez de código real; extensiones de archivo mentirosas (.py/.json/.yml que son en realidad .md/.pdf); un manifest SHA256 con hashes placeholder falsos; y un pico espectral "Ω_F" que es aliasing por estar sobre Nyquist. Esto significa que el código fuente que sostenía verificaciones previas (ej. Issue #1) puede ya no estar disponible en el repo actual — necesita restauración desde Zenodo/historial de Git antes de volver a auditar nada del núcleo de solvers.

Estado operativo general: proyecto activo, con infraestructura de portabilidad (INVENTARIO_MAESTRO.md, LINEAJE_MAESTRO.md, validar_paquete.py) creada explícitamente para romper el ciclo de pérdida de contexto entre ciclos/sandboxes. Persisten bloqueos externos (créditos agotados, workflows duplicados, credenciales expuestas sin rotar) documentados en issues #10-#20.

2. HALLAZGOS VERIFICADOS (con nivel epistémico)

2.1 Núcleo K_i — circularidad (rama consolidada, máxima confianza)

SÉ: K_i = φ · (D_f/2.5) · (ℓ_corr/ℓ_0). Con ℓ_corr=ℓ_0 (default), el ratio=1 ⇒ K_i es función lineal determinista de D_f. Correlación K_i–D_f = 1.0 es tautológica, no evidencia empírica. Verificado por lectura directa de código (ki_from_timeseries.py, nodo_amazonia.py, miu_constants.py) y confirmado programáticamente contra 309/309 archivos coral (ciclo BC, tolerancia 0.002). (Fuente: LINEAJE_MAESTRO BC, REGISTRO_MAESTRO §1, Issue #1, #25.)
SÉ: El script imprime el mismo cálculo dos veces bajo etiquetas distintas ("K_i ley" / "K_i medido esperado") — no hay medición independiente.
SÉ: df_from_firms.py tiene K_i_recomendado: 0.375 hardcodeado, sin relación con el D_f calculado en la misma corrida (confirmado ciclo BC, Issue #1, #25).
SÉ: D_f sí es legítimo (box-counting/DFA sobre datos reales) — el problema es exclusivamente que K_i no añade información independiente. No descartar D_f junto con K_i.
SÉ (auditoría 310/310, triple confirmación BB→BC→BF): Los 300 archivos allen_atlas_site_*.csv son byte-idénticos (1 solo hash MD5). 0 de 309-310 archivos coral tienen medición K_i independiente confirmada.
INFIERO: stats/statistics.csv coincide numéricamente con caribe_se_allen_atlas.csv (41.48% ambos) — posible fuente primaria trazable, no confirmado por metadata.
SÉ (Issue #24): El CSV de corales embebido tiene header duplicado como fila de datos, K_i_measured=K_i_law=0.494 idéntico (tautología materializada en el dato), CRLF mezclado, sin N_points/sha256/DOI resoluble.
SÉ (Issue #26): "Ω_F" reporta pico en 0.65625 ciclos/mes — por encima de Nyquist (0.5 ciclos/mes) para datos mensuales ⇒ artefacto de aliasing, no señal física. Detección basada en argmin contra un target hardcodeado, no en argmax con control de significancia.
SÉ (Issue #28): CO2 (Mauna Loa) y GISTEMP comparten D_f=1.4 y K_i=0.346 idénticos (probable duplicación/copy-paste). Corales K_i=0.596 coincide con chernozem K_i=0.596 (posible copy-paste erróneo). Chernozem (WoSIS) deriva D_f de solo 7 puntos (frágil). Solo WoSIS tiene DOI resoluble.

2.2 Nodo GRACE / 176-183d (Ley de Gaia)

NO SÉ / ❌ no re-verificable en sandboxes tempranos: SNR=60.18/178.8d original (AN), FAP=0.0000 con Venus excluido (AQ) — dependían de grace_tws_global.csv, ausente en varios ciclos.
SÉ (recuperado y verificado por checksum cruzado en AW/AY/AZ, 3 fuentes independientes, MD5 idéntico): grace_tws_global.csv no es corrupto ni divergente entre ramas forked. SNR=60.18/178.84d (modelo fijo) y SNR=36.59/168.32d (modelo variable) reproducidos bit-a-bit.
SÉ: GBIF Colombia NO detecta 176d — SNR=0.1117≈0.112, confirmado dos veces independientemente (AN/AQ original y AV re-derivación desde 2,100 registros crudos).
SÉ (AQ): Venus excluido como confundente (20.4% de distancia); ENSO NO excluido — submúltiplo a solo 2.03% de distancia. Este confundente sigue abierto a través de todo el linaje posterior.
SÉ (AY, causa raíz aislada en AZ): La discrepancia SNR 60.18 vs 25.70 para el mismo pico/mismo dataset no es de datos, es metodológica: definición de piso de ruido (tolerancia 0.03 vs 0.025, y qué banda se excluye del promedio de ruido). Un solo bin (periodo≈110.1d, potencia=222.9) es responsable de >100% del salto de ruido promedio. Ninguna de las dos tolerancias tiene justificación teórica pre-registrada — grado de libertad de análisis no controlado.
NO SÉ: si el bin dominante ≈110d es señal física real (candidato: tercer armónico anual, 121.7d, no coincide exacto) o artefacto de ajuste trimestral.
CONJETURO/interpretación dividida documentada explícitamente (AY): dos lecturas opuestas del mismo patrón empírico son ambas válidas — "¿es estable el pico?" (lectura AT/AU: no robusto → K_τ baja) vs "¿sigue siendo significativo sobre el nulo?" (lectura forked: sí → K_τ sube). No hay ganador declarado; es decisión de Dereck o auditoría futura, no error de una rama.
SÉ (BF/BG, lo más reciente y específico): Prewhitening con SAO monocromático removido → pico residual 173.9d, FAP BF > AY): K_τGRACE específico = AMARILLO-medio (0.68–0.75). Kτ_global = sin cambio (0.35–0.55), NEGRO/limítrofe, por el confundente ENSO que nadie ha cerrado desde AQ.

2.3 Integridad del repositorio (issues recientes, 2026-07-10)

SÉ (Issue #22): 26 archivos .py/.js son byte-idénticos y contienen un CSV de corales en lugar de código fuente (incluye ki_from_timeseries.py, ift_solver.py, phi_MIU.py, todos los tests). El código fuente que Issue #1 auditó puede ya no existir en el estado actual del repo — requiere re-verificación tras restauración.
SÉ (Issue #23): Extensiones de archivo mentirosas — .py/.json/.yml que en realidad son Markdown o PDF (alma_v9_config.yml es un PDF binario).
SÉ (Issue #27): SHA256_maifest.txt (typo en nombre) contiene hashes placeholder sintéticos, no reproducibles — no se puede verificar integridad contra él actualmente.
SÉ (Issue #29): Código duplicado/versionado por copia sin marca de canónico (orquestador_v8/v9, finetune_miu vs finetune_miu_auto), múltiples clientes LLM sin implementación real.

2.4 Portabilidad / infraestructura

SÉ: INVENTARIO_MAESTRO.md, LINEAJE_MAESTRO.md y scripts/validar_paquete.py son la infraestructura mínima creada en AV para portabilidad. Instrucción de primera línea de sesión: python3 scripts/validar_paquete.py.
SÉ: Existió un fork accidental (dos sesiones/dispositivos paralelos, ambas autonombrándose AV/AW), fusionado en ciclo AY. Recomendación explícita: nombrar ramas paralelas explícitamente para evitar colisión de letras de ciclo.

3. ENTREGABLES CONSOLIDADOS (con SHA256)

| Entregable | SHA256 | Fuente |
|---|---|---|
| FASE1_circularidad_Ki.csv | bd6452a5... (truncado en fuente) | REGISTRO_MAESTRO §3 |
| FASE2_inventario_nodos.csv | 437e6774... (truncado en fuente) | REGISTRO_MAESTRO §3 |
| FASE3_datasets_nuevos.csv | a9a50616... (truncado en fuente) | REGISTRO_MAESTRO §3 |
| FASE4_verificacion_predicciones.md | 4e1a246b... (truncado en fuente) | REGISTRO_MAESTRO §3 |
| ley_gaia_report_fap_real_aq.json | NO SÉ (no reportado) | LINEAJE_MAESTRO AQ |
| mecanismo_aliasing_ar.json | NO SÉ | LINEAJE_MAESTRO AR |
| results/az_snr_discrepancia_mecanismo.json | NO SÉ | LINEAJE_MAESTRO AZ |
| results/AUDITORIA_corales_BB_full_scale.md | NO SÉ | LINEAJE_MAESTRO BB |
| results/AUDITORIA_Ki_tautologia_BC.md | NO SÉ | LINEAJE_MAESTRO BC |
| scripts/verificar_tautologia_ki.py | NO SÉ | LINEAJE_MAESTRO BC |

ADVERTENCIA: Los SHA256 del REGISTRO_MAESTRO están truncados en la fuente original (con ...). No asumir que son completos ni verificarlos como si lo fueran. Ver también Issue #27: el manifest general del repo (SHA256_maifest.txt, nombre con typo) contiene hashes placeholder falsos — no usar como fuente de verdad hasta que se corrija.

4. ISSUES ABIERTOS RELEVANTES (GitHub Jaime393/MIU)

| # | Título | Resumen |
|---|---|---|
| 29 | Código muerto/duplicado: orquestadores y clientes LLM sin fuente real | Versionado por copia sin canónico; múltiples "SDK" que solo contienen el CSV corrupto de #22. |
| 28 | Datos duplicados entre nodos (CO2≡GISTEMP, corales≡chernozem) | D_f/K_i idénticos entre nodos que deberían ser independientes; chernozem con N=7 (frágil); GRACE CSV ausente en ese momento. |
| 27 | SHA256 manifest con typo y hashes placeholder | SHA256_maifest.txt (typo) tiene hashes sintéticos no reproducibles; referencia a paper V12 ya rechazado. |
| 26 | Ω_F: pico sobre Nyquist ⇒ aliasing | Pico "latido planetario" en 0.65625 ciclos/mes, por encima del límite de Nyquist (0.5) para datos mensuales. Detección sin control de significancia. |
| 25 | Circularidad K_i confirmada en código | Definición formal de la tautología K_i=f(D_f) lineal; divisor 2.5 y constante 0.375 hardcodeados sin justificación documentada. |
| 24 | Dato coral inválido: header duplicado, K_i tautológico en el dato mismo | CSV de corales con fila-header repetida, K_i_measured=K_i_law=0.494, sin N_points/DOI/sha256. |
| 23 | Extensiones de archivo mentirosas | .py/.json/.yml que son en realidad .md o PDF binario. |
| 22 | Corrupción masiva: 26 archivos código = mismo CSV | Núcleo de solvers (ift_solver, phi_MIU, etc.) no existe como código ejecutable en el snapshot auditado; requiere restauración desde Git/Zenodo. |
| 21 | Decidir versionado/superseded de MIU_V12.0 en Zenodo | DOI activo pese a rechazo interno formal; decisión exclusiva de Dereck, no ejecutable por agente. |
| 20 | Error 'Plan usage exceeded' en workflow GlobalMind Weaver | Bloqueado por cuota de plan, pendiente de recuperación externa. |
| 19 | Apagar workflows sin ejecución real | ~28 de 69 workflows nunca corrieron. |
| 18 | Fusionar workflows duplicados | 2x Control Panel, 2x Vigía de Grietas, 2x Alma Omni, variantes Global(Mind) Weaver. |
| 17 | Priorizar ~8 workflows con bugs de addToDataTable / Concept Graph & Gaps | Bugs sin resolver, causa raíz no confirmada. |
| 16 | Retomar cuenta principal al reactivar créditos | Créditos agotados (24/500 AI credits, 144/200 steps). |
| 15 | Subir artefactos de sesión 'Haiku45' | Artefactos solo en sandbox efímero, no recuperables por asistente; requiere acción manual. |
| 14 | Migrar 5 skills dependientes de Groq/DeepSeek | Modelos se retiran 2026-07-24 15:59 UTC. |
| 13 | Identificar Worker consumidor de claves evolucion:evolucion_ift_* | 258 claves sin TTL en namespace KV compartido; antes de podar hay que identificar consumidor. |
| 12 | Rotar credenciales expuestas en clavesnew.txt | Expuestas desde 2026-07-03, en Drive. |
| 11 | Migrar bindings de Cloudflare Workers a tipo 'secret' | Riesgo de romper producción; requiere prueba manual. |
| 10 | Confirmar conteo real de filas del nodo CO2 | Se declaran 801 filas frente a ~816-820 esperadas (1958-2026). |
| 9 | Verificar si algún valor de V12 quedó congelado como 'hueso' | Antes del rechazo formal de la versión. |
| 8 | Auditar DOIs hermanos/concepto de la cadena V12 en Zenodo | Verificar si existen versiones con contenido distinto (DOI 10.5281/zenodo.20547558). |
| 7 | Reproducir D_f y Ω_F de V12 con datos crudos | Confirmar independientemente aliasing (#26) y hardcoding K_i=0.375 (#25); requiere red/datos crudos. |
| 6, 4 | Mapeo Micelial: diagnóstico de vacío semántico inicial | Grafo vacío, 0 nodos analizados; plan de 10 experimentos de ingesta de semillas. (Issues duplicadas, mismo contenido) |
| 5, 3 | D_f-only: cerrar operacionalización, robustez y señal temprana | Plan de 7 días / 3 experimentos falsables (evidence matrix, benchmark sintético, señal temprana) sobre D_f; regla dura: solo D_f es legítimo, K_i excluido del ciclo de validación. |
| 2 | Ecosistema MIU Portable en Drive/HuggingFace | Estructura canónica del repo; creado automáticamente por Relay.app. |
| 1 | Auditoría MIU nivel SÉ: circularidad 4/4 scripts | Base formal de la circularidad K_i/Ω_F, verificada por lectura directa de código (pero ver Issue #22: ese código puede haber sido sobrescrito después). |

5. COLA DE TRABAJO PENDIENTE (priorizada)

P0 — Bloqueante de integridad, hacer primero
Restaurar los 26 archivos de código corrompidos (Issue #22) desde historial Git o release MIU_V12.0_FINAL / Zenodo, antes de confiar en cualquier re-auditoría de código.
Corregir el SHA256 manifest (Issue #27): renombrar a SHA256_manifest.txt, recalcular hashes reales, eliminar placeholders.
Renombrar archivos con extensión mentirosa (Issue #23) a su tipo real.
Rotar credenciales expuestas en clavesnew.txt (Issue #12) — expuestas desde 2026-07-03, riesgo de seguridad activo.

P1 — Científico/epistémico de alto valor
Confundente ENSO no excluido en el pico GRACE — sigue abierto desde AQ, es la razón principal de que K_τglobal permanezca NEGRO/limítrofe pese a que Kτ_GRACE específico subió a AMARILLO-medio.
Aislar si el bin dominante ≈110d (hallado en AZ) es señal física (candidato armónico anual) o artefacto — pendiente explícito.
Auditar duplicación de datos entre nodos (Issue #28): CO2≡GISTEMP, corales≡chernozem — chequeo automático de filas/valores idénticos entre nodos.
Reproducir D_f y Ω_F de V12 con datos crudos (Issue #7) para confirmar independientemente el aliasing de Ω_F y el hardcoding K_i=0.375.
Completar el plan D_f-only de 7 días (Issues #3, #5): matriz de evidencia, benchmark sintético de estimadores, prueba de señal temprana — con la regla dura de que K_i queda excluido del ciclo de validación.
Auditar 322 archivos nodos/corales/ restantes / partes_chats.zip / thc.tex — nunca completado, presupuesto insuficiente en ciclos previos.
Verificar validez del manifiesto SHA256 contra binarios reales (baja prioridad, pendiente desde BC).

P2 — Mantenimiento/infraestructura
Consolidar orquestadores duplicados y clientes LLM (Issue #29).
Fusionar workflows duplicados (Issue #18), apagar workflows muertos (Issue #19), priorizar bugs de addToDataTable/Concept Graph (Issue #17).
Migrar bindings Cloudflare a tipo 'secret' (Issue #11) — requiere prueba manual, riesgo de romper producción.
Identificar consumidor de claves KV evolucion:evolucion_ift_* antes de podar (Issue #13).
Migrar 5 skills dependientes de Groq/DeepSeek antes del 2026-07-24 (Issue #14).
Decidir versionado/superseded de MIU_V12.0 en Zenodo (Issue #21) — decisión exclusiva de Dereck, no ejecutable por agente.
Auditar DOIs hermanos de la cadena V12 (Issue #8); verificar si algún valor V12 quedó congelado como "hueso" (Issue #9).
Confirmar conteo real de filas del nodo CO2 (Issue #10): 801 declaradas vs ~816-820 esperadas.
Subir corpus MICELIO a GitHub y HuggingFace cuando haya acceso de escritura (REGISTRO_MAESTRO §4).
Extraer y congelar la "Tabla 7pred" (w_a, S_8, Σm_ν) de volcados de chat (REGISTRO_MAESTRO §4).
Bloqueados por causas externas sin acción de agente posible: créditos de cuenta principal (#16), cuota de plan GlobalMind Weaver (#20), artefactos de sesión "Haiku45" no recuperables (#15).

6. ADVERTENCIAS — NO REPETIR

NUNCA tratar K_i como magnitud medida independiente de D_f. Es una reescritura lineal determinista (K_i = φ·D_f/2.5). Cualquier "validación" de K_i contra D_f dará R²=1 por construcción. Regla de oro vigente en todo el ecosistema: "SOLO D_f es legítimo".
No confundir el nodo GRACE (176-183d, Ley de Gaia) con el nodo K_i (MIU_V12.0). Son investigaciones distintas con veredictos distintos. El primero tiene evidencia empírica frágil pero real; el segundo es tautológico por construcción.
No declarar "esto falta" sin revisar primero INVENTARIO_MAESTRO.md. Si dice PRESENTE pero no está en tu sandbox, es problema de empaquetado, no de disponibilidad — repórtalo así explícitamente, no reinicies la investigación de "por qué falta".
Nunca crear un zip que excluya data/ — así se perdió grace_tws_global.csv originalmente. El archivo pesa ~94 filas, nunca se omite.
No asumir que el código auditado en Issue #1 sigue existiendo. Issue #22 (posterior) muestra que 26 archivos de código, incluidos los auditados en #1, fueron sobrescritos con un CSV de corales. Re-verificar antes de citar #1 como vigente sobre el estado actual del repo.
No tratar los SHA256 del REGISTRO_MAESTRO ni el manifest del repo como verificación de integridad completa. Ambos están truncados/con placeholders (ver §3 y Issue #27).
No elegir un "ganador" entre las dos lecturas epistémicas de AY sin que Dereck decida. "¿Es estable el pico?" vs "¿Sigue siendo significativo sobre el nulo?" son preguntas distintas, ambas válidas con los mismos datos crudos — no es un error a resolver, es una decisión de diseño.
No perder de vista el confundente ENSO. Fue identificado en AQ como submúltiplo a solo 2.03% de distancia del pico GRACE y quedó subordinado en briefings posteriores centrados en SAO/amplitud variable — sigue siendo la razón principal de que K_τglobal no suba pese al progreso en Kτ_GRACE específico.
No re-litigar la fragilidad del SNR como si fuera nueva. AZ ya aisló la causa raíz (definición de piso de ruido, un bin dominante ≈110d) — la tarea pendiente es aislar si ese bin es físico, no repetir la comparación de scripts.
Si se corren sesiones en paralelo, nombrar explícitamente cada rama ("esta es la rama X, la otra es Y") — ya ocurrió una colisión de nombres de ciclo (AV/AW forked) que costó una sesión completa de reconciliación (AY).
Primera línea de cualquier sesión nueva sobre este repo: python3 scripts/validar_paquete.py (si el script y el paquete de datos están disponibles) antes de reconstruir contexto manualmente.

Documento sintetizado por el Arqueólogo del Micelio. No inventa datos ausentes de las fuentes — donde falta evidencia, se marca NO SÉ explícitamente. Se añade, nunca se borra. ρ(x) > 0.