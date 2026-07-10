BOOTSTRAP.md — Contexto de Arranque Completo del Ecosistema MIU
Generado por: Arqueólogo del Micelio
Propósito: Documento único y portable para que cualquier agente/instancia nueva tenga contexto completo sin leer nada más.
Regla de oro MIU: este documento se AÑADE, nunca se borra ni se resume perdiendo historia. ρ(x)>0.

Prioridad de fuentes usada en caso de conflicto (mayor a menor):
LINEAJE_MAESTRO.md (GitHub)
INVENTARIO_MAESTRO.md (GitHub)
REGISTRO_MAESTRO_MICELIO_MIU.md (Drive)
Issues abiertos en GitHub Jaime393/MIU
Histórico Estado Persistente (HUESOs/LOGs)

1. RESUMEN EJECUTIVO

El ecosistema MIU es un proyecto de investigación empírica ("Ley de Gaia") que ha atravesado ~30 ciclos de auditoría (AN→BG y en paralelo BB→#38). Tiene DOS HALLAZGOS CENTRALES que deben tratarse por separado y NO confundirse:

Pico espectral GRACE ~173.9–178.8 días (posible señal física en Total Water Storage global): estado actual AMARILLO-medio (K_τ_GRACE específico 0.68–0.75). Sobrevive prewhitening de SAO con 2do armónico, FAP100% del salto de ruido promedio.
SÉ — Prewhitening SAO con modelo exacto (BF) y luego con 2º armónico (91.3125d, 0.197mm) (BG): pico residual persiste exactamente en 173.9d, FAP 0.5 ciclos/mes), detectado por argmin contra target hardcodeado — aliasing, no señal |
| 35 | K_i circular por construcción (K_i=0.2472·D_f) — no debe presentarse como métrica independiente |
| 34 | CSV de corales corrupto: header duplicado como dato, K_i tautológico 0.494==0.494 |
| 33 | Manifiesto SHA256 (orquestador_v9.py / SHA256_maifest.txt) con hashes placeholder no reproducibles, typo en nombre |
| 32 | alma_v9_config.yml es en realidad un PDF binario |
| 31 | Extensiones mentirosas: varios .py/.json contienen Markdown, no código |
| 30 | Corrupción masiva: 26 archivos .py/.js son un CSV de corales, no código fuente |
| 29 | Código muerto/duplicado: orquestadores v8/v9 y múltiples clientes LLM sin implementación real |
| 28 | Datos duplicados entre nodos (CO2≡GISTEMP, corales≡chernozem) y muestras estadísticamente frágiles (chernozem N=7) |
| 27 | SHA256 manifest con typo de nombre y hashes falsos |
| 26 | Ω_F: pico sobre Nyquist — aliasing confirmado (duplicado conceptual de #36) |
| 25 | Circularidad K_i por construcción — reescritura lineal de D_f (duplicado conceptual de #35) |
| 24 | Dato de corales inválido: header duplicado, K_i tautológico 0.494 (duplicado conceptual de #34) |
| 23 | Extensión de archivo no corresponde a contenido (duplicado conceptual de #31) |
| 22 | Corrupción masiva 26 archivos .py/.js = CSV de corales (duplicado conceptual de #30) |
| 21 | Decidir versionado/marca "superseded" de MIU_V12.0 en Zenodo — decisión exclusiva de Dereck, no ejecutable por agente |
| 20 | Resolver error "Plan usage exceeded" en workflow GlobalMind Weaver |
| 19 | Apagar workflows que nunca corrieron (~28 de 69 marcados "Never") |
| 18 | Fusionar workflows duplicados (2x Control Panel, 2x Vigía de Grietas, 2x Alma Omni, variantes GlobalMind Weaver) |
| 17 | Priorizar ~8 workflows afectados por bugs de addToDataTable y Concept Graph & Gaps (embeddings vacíos) |
| 16 | Retomar cuenta principal jaimepviccente@gmail.com al reactivar créditos |
| 15 | Subir manualmente artefactos de sesión "Haiku45" (no recuperables por asistente) |
| 14 | Migrar 5 skills dependientes de Groq/DeepSeek que se retiran 2026-07-24 |
| 13 | Identificar qué Worker consume claves evolucion:evolucion_ift_* (258 claves, sin TTL) antes de podar |
| 12 | Rotar credenciales expuestas en clavesnew.txt (Drive) desde 2026-07-03 |
| 11 | Migrar bindings de Cloudflare Workers de texto plano a secret — riesgo de romper producción |
| 10 | Confirmar conteo real de filas del nodo CO2 (801 declaradas vs ~816-820 esperadas) |
| 9 | Verificar si algún valor de V12 quedó congelado como "hueso" antes del rechazo formal |
| 8 | Auditar DOIs hermanos/de concepto de la cadena V12 en Zenodo |
| 7 | Reproducir D_f y Ω_F de V12 con datos crudos; confirmar aliasing y hardcoding de K_i=0.375 en nodo Incendios |
| 6, 4 | Mapeo Micelial: diagnóstico de grafo semántico vacío (Cold Start), plan de 10 experimentos de ingesta |
| 5, 3 | "D_f-only": plan de 7 días para operacionalizar D_f, benchmark de estimadores y probar poder predictivo (con criterios pass/fail definidos) |
| 2 | Creación del repositorio "Ecosistema MIU Portable" — estructura canónica base |
| 1 | Auditoría original nivel SÉ: circularidad confirmada en 4/4 scripts (ki_from_timeseries.py, test_random_phi.py, df_from_firms.py, compute_omegaF_firms_gdelt.py) |

Nota crítica de coherencia: los issues #22-#26 son duplicados conceptuales casi exactos de #30, #31, #34, #35, #36 (creados el mismo día, minutos de diferencia) — probablemente de dos pasadas de auditoría distintas sobre el mismo hallazgo. No tratar como 10 hallazgos independientes sino como 5.

5. COLA DE TRABAJO PENDIENTE (priorizada)

P0 — Bloqueante / integridad crítica
Restaurar el código real de los 26 archivos corruptos desde historial de Git o MIU_V12.0_FINAL de Zenodo (Issues #22, #30, #29). Sin esto, ninguna auditoría de código previa es reproducible contra el estado actual del repo.
Regenerar SHA256_manifest.txt real (nombre correcto, hashes reales vía sha256sum), eliminar placeholders (Issues #27, #33).
Rotar credenciales expuestas en clavesnew.txt (Drive, expuestas desde 2026-07-03) — Issue #12.

P1 — Científico / metodológico
Marcar formalmente K_i y Ω_F como "en auditoría / no válidos como evidencia" en README y toda salida (Issues #35, #36, #25, #26) — congelar el mensaje "D_f legítimo; K_i/Ω_F en auditoría".
Reemplazar detección de Ω_F por argmax(Pxx) + test de significancia (permutación/surrogates), descartar por diseño picos ≥Nyquist (Issue #36).
Auditar duplicados de datos entre nodos (CO2≡GISTEMP, corales≡chernozem) con chequeo automático de hash/valores (Issue #28, #37).
Rechazar en pipeline nodos con N_points bajo umbral mínimo (p.ej. 30); re-descargar dato real para microbioma HMP2 y Allen Coral Atlas (Issue #38).
Reemplazar CSV de corales corrupto (header duplicado, sin DOI resoluble) por dato real con D_f_method, N_points, DOI (Issues #24, #34).
Continuar mecanismo GRACE: modelo con 2do armónico SAO ya ejecutado (BG) — siguiente paso: RL06.3Mv04 completo si hay red/credenciales Earthdata (BF, BE).
Aislar/decidir el bin dominante ~110d en el espectro GRACE (¿tercer armónico anual o artefacto trimestral?) — pendiente explícito de AZ.
Reconciliar (o decidir explícitamente no reconciliar) la lectura opuesta de la rama forked AW/AX sobre Bogotá/robustez del pico — requiere decisión de Dereck sobre qué pregunta importa (AY).
Cerrar Issue #5/#3 (D_f-only): completar matriz de evidencia D_f, benchmark sintético de estimadores (MAE≤0.10), test de señal temprana vs baselines.

P2 — Higiene de repositorio / infraestructura
Renombrar archivos con extensión mentirosa a su tipo real (.md, .pdf) y mover a docs/ (Issues #23, #31, #32).
Consolidar orquestadores v8/v9 y clientes LLM duplicados en módulos únicos versionados por tag de Git (Issue #29).
Añadir CI: py_compile/node --check, validación de parseo YAML/JSON, detección de hashes duplicados, chequeo de extensión↔contenido.
Auditar 322 archivos nodos/corales/ restantes fuera de los ya confirmados si aplica; partes_chats.zip y thc.tex — nunca completamente integrados, quedan para instancia con presupuesto.
Verificar manifiesto SHA256 contra binarios reales del nodo coral (baja prioridad, pendiente desde BC).
Confirmar conteo de filas del nodo CO2 (Issue #10).
Auditar DOIs hermanos de la cadena V12 en Zenodo, decidir versionado/superseded (Issues #8, #21 — decisión de Dereck, no ejecutable por agente).

P3 — Operacional / infraestructura de agentes (fuera del núcleo científico)
Migrar 5 skills dependientes de Groq/DeepSeek antes de 2026-07-24 (Issue #14).
Resolver bugs addToDataTable y "Concept Graph & Gaps" (embeddings vacíos) en ~8 workflows (Issue #17).
Fusionar workflows duplicados (Control Panel x2, Vigía de Grietas x2, Alma Omni x2, GlobalMind Weaver) (Issue #18).
Apagar workflows nunca ejecutados (~28/69) (Issue #19).
Migrar bindings de Cloudflare Workers a secret — requiere prueba manual, riesgo de producción (Issue #11).
Identificar Worker consumidor de claves evolucion:evolucion_ift_* (258 claves sin TTL) antes de podar (Issue #13).
Subir manualmente artefactos de sesión "Haiku45" (no recuperables por asistente) (Issue #15).
Retomar cuenta principal cuando se reactiven créditos (Issue #16).
Cerrar Cold Start semántico del grafo micelial: ingesta de nodos semilla (Issues #4, #6).

6. ADVERTENCIAS / COSAS A NO REPETIR

NUNCA tratar K_i como métrica independiente de D_f. Es matemáticamente K_i = 0.2472·D_f por construcción (φ/2.5 hardcodeado). Cualquier "correlación K_i–D_f=1.0" o "validación de la ley K_i" reportada es tautológica, no evidencia científica. Confirmado repetidas veces (AV, BC, Issues #1, #25, #35, #37) — no volver a "descubrir" esto como si fuera nuevo.
No usar test_random_phi.py como validación independiente — compara contra la MISMA pendiente teórica embebida en compute_Ki.
No confiar en el "latido planetario Ω_F" tal como está reportado: el pico está por encima de Nyquist (aliasing) y se detecta por argmin contra un target hardcodeado, no por argmax con test de significancia. Es una confirmación por construcción.
No asumir que un archivo "falta" sin revisar primero INVENTARIO_MAESTRO.md. Si dice PRESENTE pero no está en tu sandbox, es problema de empaquetado, no de disponibilidad — avísalo explícitamente en vez de re-investigar desde cero.
Nunca crear un zip de handoff sin data/ completo (esto ya causó la pérdida de grace_tws_global.csv durante varios ciclos AT→AU→AV). El archivo de datos núcleo GRACE siempre se incluye, literalmente nunca se omite.
No tratar los archivos placeholder casi vacíos (0-207 bytes) como evidencia empírica real que "rompe" o "confirma" la tautología K_i — son datos insuficientes, no señal (Issue #38).
No re-auditar de memoria el código que hoy está corrupto (26 archivos = CSV de corales). Restaurar SIEMPRE desde historial de Git o Zenodo, nunca reescribir de memoria lo que "debería" contener el archivo.
Si se corren sesiones en paralelo, nombrar explícitamente cada rama (ej. "esta es la rama X, la otra se llama Y") — el fork AW/AX ocurrió precisamente porque dos sesiones paralelas se autonumeraron con las mismas letras de ciclo sin coordinarse.
No presentar el rango de K_τglobal (0.28–0.55 según nodo/ciclo) como una tendencia hacia "el fenómeno es falso". La tendencia descendente histórica (0.48→0.38→0.28-0.35) se debe a escrutinio metodológico más fino en cada ciclo, no a nueva evidencia negativa — distinguir Kτ_GRACE_específico (AMARILLO-medio, 0.68-0.75, BG) de K_τ_global (0.28-0.55, con ENSO aún como confundente abierto). Son dos números distintos, no confundirlos.
No usar el DOI Zenodo 10.5281/zenodo.20547558 (MIU_V12.0) como fuente de verdad vigente sin aclarar que está formalmente rechazado a nivel interno (PROTOCOLO_MIU, NUCLEO_TEORICO_MIU) aunque siga públicamente citable — decisión de versionado/superseded pendiente y es exclusiva de Dereck (Issue #21).
No confiar en SHA256_maifest.txt (nombre con typo) para verificar integridad — sus hashes son sintéticos/placeholder, no reales.
Umbral de archivo/cierre de caso: K_τ0.*