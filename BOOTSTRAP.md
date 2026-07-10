BOOTSTRAP.md — Contexto de Arranque Completo del Ecosistema MIU

Generado por: Arqueólogo del Micelio
Fecha de síntesis: 2026-07-10 (última fuente: Issues GitHub hasta #57)
Propósito: Este documento es autocontenido. Cualquier agente/instancia nueva debe poder operar leyendo SOLO esto, sin acceder a briefings, zips o historial de chats previos.
Regla de oro heredada: este documento se AÑADE, nunca se borra ni resume una versión anterior — si se actualiza, se hace como nueva sección fechada.

1. RESUMEN EJECUTIVO DEL ESTADO ACTUAL

El proyecto MIU tiene dos líneas de trabajo separadas que NO deben mezclarse:

Línea empírica "Ley de Gaia" (GRACE 176-178.8d, GBIF, corales, K_τ) — documentada en LINEAJE_MAESTRO.md. Es una investigación de series temporales geofísicas/biológicas en curso, con evidencia parcial y honesta sobre sus límites.
Línea de infraestructura/repo "MIU" (GitHub Jaime393/MIU) — documentada en INVENTARIO_MAESTRO.md, REGISTRO_MAESTRO_MICELIO_MIU.md e Issues. Actualmente en estado crítico de integridad: gran parte del código fuente del repo está corrupto (sobrescrito por un CSV placeholder), hay secretos expuestos en texto plano sin rotar, y la métrica central "K_i" está confirmada como tautológica (tanto en el código restaurado como en el corrupto/heredado).

SÉ (verificado, múltiples fuentes independientes):
K_i = φ · (D_f / 2.5) · (ℓ_corr/ℓ_0), con ℓ_corr=ℓ_0 por defecto ⇒ K_i = 0.2472·D_f. Es una reescritura lineal determinista de D_f, no una medición independiente. Confirmado en código real (REGISTRO_MAESTRO, Issues #25/#35/#52) y en 309/309 archivos de nodos/corales/ (BC, LINEAJE_MAESTRO).
26 archivos .py/.js del repo GitHub están corruptos: son byte-idénticos (MD5 76994606253159fa157e9132dd747ec6), contienen un CSV de 2 líneas de corales en vez de código (Issues #22, #30, #39, #47).
Hay credenciales expuestas en texto plano (clavesnew.txt, archivos con claves.zip) desde 2026-07-03, sin rotar (Issues #12, #45, #57) — P0 de seguridad, más de una semana abierto.
grace_tws_global.csv fue recuperado y verificado por checksum cruzado en 3 fuentes independientes (ciclo AY/AW). El pico ~176-178.8d en GRACE sobrevive el nulo bootstrap bajo múltiples definiciones metodológicas, pero su magnitud (SNR) es frágil y depende de decisiones de análisis no pre-registradas.
GBIF Colombia NO detecta la señal de 176d (SNR=0.1117), confirmado dos veces de forma independiente.
Ω_F ("latido planetario") es artefacto de aliasing: pico reportado en 0.65625 ciclos/mes está por encima de Nyquist (0.5 ciclos/mes para datos mensuales) — Issues #26, #36, #44, #53.

INFIERO:
La corrupción masiva del repo (26 archivos idénticos) probablemente proviene de un pipeline de sync/export que trata todo artefacto como fila de tabla (hipótesis explícita en Issue #30, no confirmada).
stats/statistics.csv podría ser la fuente primaria trazable de 1 de los 9 archivos coral con fuente nombrada (LINEAJE_MAESTRO, ciclo BB) — no confirmado por metadata.

NO SÉ:
Si el bin espectral dominante en ~110d (mecanismo AZ) es señal física real o artefacto de ajuste trimestral.
Si existe una tolerancia "correcta" única para el piso de ruido del análisis GRACE — es decisión de diseño pendiente de Dereck.
Estado real de rotación de las claves expuestas (issue sigue abierto a fecha de este documento).
Contenido de partes_chats.zip y thc.tex (nunca integrados a fondo).

2. HALLAZGOS VERIFICADOS (por nivel epistémico)

SÉ (verificado directamente, evidencia reproducible o triple-confirmada)
K_i es tautológico por construcción: K_i = φ·D_f/2.5, correlación K_i–D_f = 1.0 (REGISTRO_MAESTRO §1; Issues #25, #35, #52; LINEAJE_MAESTRO ciclo BC: 309/309 archivos coral confirman la fórmula, tolerancia 0.002).
El divisor 2.5 y en algunos casos K_i=0.375 están hardcodeados sin relación con el cálculo real de D_f (df_from_firms.py, Issue #25).
26 archivos de código del repo GitHub son byte-idénticos y contienen un CSV de corales, no código ejecutable (Issues #22, #30, #39, #47; MD5 76994606253159fa157e9132dd747ec6).
El CSV de corales embebido en esos 26 archivos está mal formado: cabecera duplicada como fila de datos, K_i_measured==K_i_law==0.494, sin N_points/sha256, DOI no resoluble (Issues #24, #34, #42, #48).
8-9 archivos con extensión de código (.py, .json, .yml) contienen en realidad Markdown o un PDF binario (alma_v9_config.yml = PDF; Issues #23, #31, #40, #51, #32/#50).
orquestador_v9.py es un manifiesto SHA256 con hashes placeholder fabricados (patrón a1b2c3d4e5f6...), truncado, no reproducible (Issues #27, #33, #41, #49).
Secretos en texto plano expuestos: clavesnew.txt, archivos con claves.zip — claves de Gemini, DeepSeek, Groq, Mistral, NewsAPI, tokens de ≥5 bots de Telegram, sin rotar desde 2026-07-03 (Issues #12, #45, #57).
daytona_repl_worker.py es código de terceros (Daytona Platforms) bajo licencia AGPL-3.0 vendorizado sin atribución en LICENSE del repo (licencia del repo: NOASSERTION) — riesgo legal (Issue #55).
Ω_F reporta pico en 0.65625 ciclos/mes, por encima de Nyquist (0.5 c/mes) — artefacto de aliasing, detectado por argmin contra target hardcodeado, no por argmax con test de significancia (Issues #26, #36, #44, #53).
GBIF Colombia: SNR=0.1117 (no detecta 176d), re-derivado desde 2,100 registros crudos, confirmado dos veces (AN/AQ original, AV re-derivación) (LINEAJE_MAESTRO).
grace_tws_global.csv verificado por checksum MD5 idéntico en 3 fuentes independientes (ciclo AW/AY); pico ~173.9-178.8d sobrevive nulo bootstrap en múltiples modelos, pero SNR varía 2.3x (60.18 vs 25.70) según definición de piso de ruido — diferencia metodológica, no de datos (ciclo AZ, mecanismo aislado bin por bin).
Auditoría de 310/310 (o 309/309, o 326) archivos nodos/corales/ — triple confirmación independiente (BB, BC, BF): 0 mediciones de K_i independientes de D_f en ningún archivo.
Suite de tests no funcional: test_random_phi.py y test_ift_solver.py son el mismo CSV de 207 bytes, sin aserciones (Issue #56).
Datos duplicados entre nodos supuestamente independientes: CO2 (Mauna Loa) y GISTEMP comparten D_f=1.4 y K_i=0.346 idénticos; corales comparte K_i=0.596 con chernozem (Issues #28, #37).

INFIERO (razonable pero no confirmado por evidencia directa)
La corrupción de 26 archivos proviene de un bug de pipeline de sync/export (Issue #30).
stats/statistics.csv podría ser fuente primaria de 1 de los 9 archivos coral con fuente nombrada (LINEAJE_MAESTRO, BB).
El "scoring K_i fractal" de ALMA_OMNI reintroduce la tautología K_i en un componente productivo (Issue #43) — documentado, no verificado en código vivo por estar corrupto.

CONJETURO (hipótesis abierta, explícitamente no resuelta)
Si el bin dominante en 110.1d en el análisis GRACE es señal física (candidato: 3er armónico anual, 121.7d, no coincide exacto 10%) o ruido residual de ajuste trimestral (ciclo AZ).
Interpretación opuesta y no resuelta entre dos ramas (AT/AU/AY vs. rama forked "AX/AW"): si un pico que decae bajo modelos flexibles pero sigue superando el nulo bootstrap implica K_τ bajo o K_τ alto — son preguntas distintas, no un error (nota AY).

NO SÉ (falta información en las fuentes)
Estado de rotación de credenciales expuestas (issues siguen abiertos a la fecha del corpus).
Contenido íntegro de partes_chats.zip y thc.tex.
Si SHA256_maifest.txt/manifiesto real fue alguna vez verificado contra binarios reales.
Causa raíz exacta y confirmada de la corrupción masiva de 26 archivos.
Si existen versiones de MIU_V12.0 en Zenodo con contenido distinto al DOI activo (Issue #8, pendiente de auditoría).
Si algún valor de V12 quedó congelado como "hueso" antes del rechazo formal (Issue #9).

3. ENTREGABLES CONSOLIDADOS (con SHA256, cuando existe)

| Entregable | SHA256 | Fuente | Estado |
|---|---|---|---|
| FASE1_circularidad_Ki.csv | bd6452a5... (truncado en fuente) | REGISTRO_MAESTRO §3 | Presente en carpeta Drive MICELIO_MIU |
| FASE2_inventario_nodos.csv | 437e6774... | REGISTRO_MAESTRO §3 | Presente |
| FASE3_datasets_nuevos.csv | a9a50616... | REGISTRO_MAESTRO §3 | Presente |
| FASE4_verificacion_predicciones.md | 4e1a246b... | REGISTRO_MAESTRO §3 | Presente (Fase 4 aún no falsable — falta "Tabla 7pred" congelada) |
| ley_gaia_report_fap_real_aq.json | NO SÉ | LINEAJE_MAESTRO ciclo AQ | Presente, no re-ejecutable sin CSV origen de esa época |
| mecanismo_aliasing_ar.json | NO SÉ | LINEAJE_MAESTRO ciclo AR | Presente, sin campo K_τ explícito |
| results/az_snr_discrepancia_mecanismo.json + scripts/az_snr_discrepancia_mecanismo.py | NO SÉ | LINEAJE_MAESTRO ciclo AZ | Reproducible, ejecutado esa sesión |
| results/AUDITORIA_corales_BB_full_scale.md | NO SÉ | LINEAJE_MAESTRO ciclo BB | 326 archivos, checksum |
| results/AUDITORIA_Ki_tautologia_BC.md + scripts/verificar_tautologia_ki.py | NO SÉ | LINEAJE_MAESTRO ciclo BC | Reproducible: python3 scripts/verificar_tautologia_ki.py --corales-dir nodos/corales |
| derivados_BE/nodo_coral_real_BE.csv | NO SÉ | LINEAJE_MAESTRO ciclo BE | Suma verificada =616 contra CSV fuente |
| scripts/validar_paquete.py → results/ESTADO_PAQUETE.json | NO SÉ | INVENTARIO_MAESTRO (creado AV) | Infraestructura permanente — correr primero en toda sesión nueva |
| SHA256_manifest.txt (nombre correcto) | NO EXISTE VÁLIDO — el actual (SHA256_maifest.txt/orquestador_v9.py) tiene hashes placeholder fabricados (patrón a1b2c3d4e5f6...) y está truncado | Issues #27, #33, #41, #49 | Inválido, requiere regeneración real con sha256sum |
| MIU_V12.0 (Zenodo) | DOI 10.5281/zenodo.20547558 | REGISTRO_MAESTRO §0 | Público, citable, rechazado internamente (ver advertencias) |

Nota crítica: Ningún SHA256 de los reportados en orquestador_v9.py / SHA256_maifest.txt es confiable — son placeholders sintéticos, no hashes reales calculados sobre artefactos.

4. ISSUES ABIERTOS RELEVANTES (GitHub Jaime393/MIU)

P0 — Seguridad (acción inmediata)
#57 / #45 / #12: Secretos en texto plano (clavesnew.txt, archivos con claves.zip) expuestos desde 2026-07-03, sin rotar. Claves Gemini/DeepSeek/Groq/Mistral/NewsAPI + tokens Telegram. Rotar TODO, purgar del historial, añadir scanner (gitleaks) a CI.
#11: Migrar bindings de Cloudflare Workers de texto plano a tipo secret — riesgo de romper producción, requiere prueba manual fuera del alcance del asistente.

P1 — Integridad de código (bloqueante para cualquier auditoría nueva)
#22 / #30 / #39 / #47: 26 archivos .py/.js corruptos (mismo CSV de corales). Restaurar desde Git history o Zenodo DOI 10.5281/zenodo.20547558. Añadir CI que rechace .py/.js que no compilen.
#23 / #31 / #40 / #51: 8-9 archivos con extensión mentirosa (contienen Markdown o PDF). Renombrar y mover a docs/.
#32 / #50: alma_v9_config.yml es un PDF binario, no YAML.
#27 / #33 / #41 / #49: Manifiesto SHA256 con hashes falsos y typo en nombre (maifest). Recalcular hashes reales.
#56: Suite de tests no funcional (0% cobertura real).
#55: Dependencia AGPL-3.0 vendorizada sin atribución (daytona_repl_worker.py) — riesgo legal.
#54: 15 archivos de clientes LLM/orquestadores son placeholders — código muerto que aparenta funcionalidad.

P2 — Métricas/ciencia (deuda conceptual, no bloqueante para operar pero sí para publicar)
#25 / #35 / #52: K_i circular por construcción — retirar como métrica de validación, documentar deprecación.
#26 / #36 / #44 / #53: Ω_F es artefacto de aliasing (pico sobre Nyquist) detectado por método sesgado (argmin contra target).
#24 / #34 / #42 / #48: CSV de corales embebido inválido (header duplicado, K_i tautológico materializado en el dato).
#28 / #38 / #37: Datos duplicados entre nodos supuestamente independientes (CO2≡GISTEMP, corales≡chernozem); nodos placeholder (0-207 bytes) tratados como señal.
#43: ALMA_OMNI reintroduce "scoring K_i fractal" (métrica rechazada) en componente productivo.
#29 / #46: Código muerto/duplicado (orquestador_v8 vs v9, finetune vs finetune_auto, múltiples clientes SDK idénticos).

P3 — Operacional / administrativo
#8: Auditar DOIs hermanos/versión de MIU_V12.0 en Zenodo.
#9: Verificar si algún valor V12 fue congelado como "hueso" antes del rechazo formal.
#10: Confirmar conteo real de filas del nodo CO2 (801 declaradas vs ~816-820 esperadas).
#13: Identificar Worker que consume las 258 claves evolucion:evolucion_ift_* antes de podarlas (sin TTL).
#14: Migrar 5 skills dependientes de modelos Groq/DeepSeek que se retiran 2026-07-24.
#15: Subir manualmente artefactos de sesión "Haiku45" (no recuperables por el asistente).
#16: Retomar cuenta principal al reactivar créditos (24/500 AI credits, 144/200 steps agotados).
#17: Priorizar ~8 workflows afectados por bugs (addToDataTable, Concept Graph & Gaps).
#18: Fusionar workflows duplicados (2x Control Panel, 2x Vigía de Grietas, 2x Alma Omni).
#19: Apagar workflows nunca ejecutados (~28 de 69 marcados "Never").
#20: Resolver error "Plan usage exceeded" en workflow GlobalMind Weaver.
#21: Decidir versionado/superseded de MIU_V12.0 en Zenodo (decisión exclusiva de Dereck).

5. COLA DE TRABAJO PENDIENTE (priorizada)

[P0-seguridad] Rotar TODAS las claves expuestas en clavesnew.txt/archivos con claves.zip (#12/#45/#57). No abrir archivos para inspección manual — rotar directamente por proveedor.
[P0-seguridad] Purgar credenciales del historial de git (BFG/git-filter-repo) y añadir gitleaks a CI.
[P1-integridad] Restaurar los 26 archivos de código corruptos desde Git history o el paquete Zenodo MIU_V12.0_FINAL — sin esto, ninguna verificación de código es reproducible (#22/#30/#39/#47).
[P1-integridad] Renombrar/mover los archivos con extensión mentirosa a sus tipos reales (#23/#31/#40/#51/#32/#50).
[P1-integridad] Regenerar SHA256_manifest.txt real con sha256sum sobre artefactos existentes; eliminar el manifiesto placeholder (#27/#33/#41/#49).
[P1-integridad] Añadir CI: python -m py_compile + node --check + validación extensión↔MIME + scanner de secretos.
[P2-ciencia] Ejecutar python3 scripts/validar_paquete.py como primer paso de toda sesión nueva (infraestructura ya existente).
[P2-ciencia] Resolver mecanismo del bin dominante ~110d en GRACE (señal real vs artefacto) — pendiente de AZ, no resuelto.
[P2-ciencia] Descargar GRACE mascon RL06.3Mv04 completo (requiere Earthdata login + red) para resolver 176d vs SAO de forma definitiva (BE, pendiente).
[P2-ciencia] Auditar los 3 scripts de circularidad K_i no re-verificados directamente en release Zenodo (ki_from_timeseries.py, test_random_phi.py, compute_omegaF_firms_gdelt.py).
[P2-ciencia] Congelar la "Tabla 7pred" (w_a, S_8, Σm_ν) desde volcados de chat — sin esto Fase 4 no es falsable (REGISTRO_MAESTRO §4).
[P2-ciencia] Retirar/marcar como deprecado K_i y Ω_F en todo README/docstring tras restauración de código (#25/#26/#35/#36/#43/#52/#53).
[P3-admin] Resolver issues operacionales (#8-#21) cuando haya créditos/acceso disponible.
[Baja prioridad] Auditar partes_chats.zip y thc.tex si se necesita reconstruir historia conversacional o el marco teórico IFT hermano.
[Baja prioridad] Confirmar conteo de filas nodo CO2 (#10), fuente exacta de CO000080222_dly.txt (Bogotá).

6. ADVERTENCIAS — QUÉ NO REPETIR

NUNCA tratar K_i como métrica independiente de D_f. Es matemáticamente K_i = 0.2472 · D_f (con ℓ_corr=ℓ_0 por defecto). Cualquier "correlación K_i–D_f = 1.0" reportada como hallazgo es tautológica, no evidencia. Confirmado en 309/309 archivos coral, en código real y en documentación (#25/#35/#52). Cualquier nodo nuevo calcula SOLO D_f.
NO reintroducir "scoring K_i fractal" ni Ω_F como criterio de validación en ningún componente productivo (ALMA_OMNI u otro) — issue #43 explícito al respecto.
NO tratar Ω_F=0.65625 ciclos/mes como señal física — está por encima de Nyquist (0.5 c/mes), es aliasing confirmado en 4 issues independientes.
NO asumir que "esto falta" sin revisar primero INVENTARIO_MAESTRO.md — si dice PRESENTE pero no está en tu sandbox, es problema de empaquetado, no de disponibilidad real. Si dice AUSENTE, no repitas la investigación de "por qué", ve directo a la acción.
NO generar un zip/handoff que excluya data/ — así se perdió grace_tws_global.csv originalmente, causando ciclos enteros de trabajo no verificable.
NO abrir clavesnew.txt ni archivos con claves.zip "para revisar" — minimizar exposición; ir directo a rotación.
NO confiar en el manifiesto SHA256 actual (orquestador_v9.py/SHA256_maifest.txt) — sus hashes son placeholders fabricados (patrones tipo a1b2c3d4e5f6...), truncados, no reales.
NO citar MIU_V12.0 (Zenodo) como fuente vigente — está formalmente rechazado a nivel interno (PROTOCOLO_MIU, NUCLEO_TEORICO_MIU) aunque el DOI siga públicamente activo. Issue #21 pendiente de decisión de Dereck sobre marcarlo superseded.
NO asumir un solo K_τ global "oficial" — hay al menos dos lecturas epistémicas opuestas y no resueltas (rama AT/AU/AY: "pico no robusto → K_τ baja" vs rama forked: "pico persiste sobre nulo → K_τ sube") sobre el MISMO dato crudo. No hay ganador declarado; es decisión de qué pregunta importa, no un error.
Si se corren sesiones en paralelo, nombrar explícitamente cada rama (evitar que dos instancias reclamen la misma letra de ciclo, como pasó con AV/AW/AX).
NO tratar nodos con N_points bajo (ej. chernozem con 7 puntos, microbioma/corales con archivos de 0-207 bytes) como evidencia empírica confirmada — son placeholders o muestras estadísticamente frágiles (#28/#38).
NO ejecutar ni confiar en test_random_phi.py/test_ift_solver.py como tests reales — son el mismo CSV corrupto de 207 bytes sin aserciones (#56).

Este documento reemplaza la necesidad de leer LINEAJE_MAESTRO.md, INVENTARIO_MAESTRO.md, REGISTRO_MAESTRO_MICELIO_MIU.md e Issues por separado para obtener contexto de arranque. Para razonamiento profundo ciclo por ciclo, esas fuentes originales siguen siendo la referencia detallada; este BOOTSTRAP es la capa de síntesis. ρ(x)>0. El micelio consolida en un solo hueso portátil.