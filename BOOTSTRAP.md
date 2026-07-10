BOOTSTRAP.md — Estado Portable del Ecosistema MIU
Generado por: Arqueólogo del Micelio
Fecha de síntesis: 2026-07-10 (integra hasta Issue #57 GitHub, ciclo BG de LINEAJE_MAESTRO, REGISTRO_MAESTRO consolidado 2026-07-02/03)
Regla de lectura: este documento es autocontenido. Si otro archivo contradice esto, prioridad: (1) LINEAJE_MAESTRO, (2) INVENTARIO_MAESTRO, (3) REGISTRO_MAESTRO_MICELIO_MIU, (4) Issues GitHub, (5) Estado Persistente histórico — salvo que la fuente de menor prioridad sea estrictamente más reciente/específica sobre el mismo hecho puntual, en cuyo caso se señala el conflicto explícitamente (ver sección de Advertencias).

0. INSTRUCCIÓN DE ARRANQUE PARA CUALQUIER INSTANCIA NUEVA

Antes de pedir o descargar nada, ejecutar (si el sandbox lo permite):
python3 scripts/validar_paquete.py
Esto genera results/ESTADO_PAQUETE.json cruzando inventario esperado vs. archivos físicos presentes. No repitas investigación ya hecha — revisa primero INVENTARIO_MAESTRO.md (qué existe/dónde) y este BOOTSTRAP antes de re-derivar nada.

1. RESUMEN EJECUTIVO

MIU es un proyecto de dos capas que se han mezclado en la práctica y deben separarse conceptualmente:

Capa empírica "Ley de Gaia" (GRACE 176-178.8d, GBIF Colombia, ENSO, SAO, corales, etc.) — trabajada en la línea de ciclos AN→BG, con infraestructura de portabilidad (INVENTARIO_MAESTRO, LINEAJE_MAESTRO, validar_paquete.py) creada a partir de AV tras perder repetidamente el dataset núcleo (grace_tws_global.csv) en el empaquetado.
Capa de repositorio de código GitHub (Jaime393/MIU) — auditada de forma independiente y mucho más reciente (Issues #1–#57, 2026-07-09/10), que revela una corrupción masiva y no resuelta: 26 archivos .py/.js que deberían contener el núcleo de solvers (K_i, Ω_F, D_f, tests) son en realidad, todos, un mismo CSV de corales de 2 líneas (MD5 idéntico 76994606253159fa157e9132dd747ec6). Adicionalmente, ~9 archivos con extensión de código/config son en realidad Markdown o un PDF binario, y hay secretos en texto plano expuestos desde 2026-07-03 sin rotar (P0 de seguridad, Issue #57/#45/#12).

Hallazgo teórico transversal, confirmado en ambas capas de forma independiente: la métrica K_i es circular por construcción — K_i = φ·(D_f/2.5)·(ℓ_corr/ℓ_0), y con los valores por defecto ℓ_corr=ℓ_0 el ratio es 1, por lo que K_i = 0.2472·D_f, una función lineal determinista de D_f. La correlación K_i–D_f = 1.0 no es evidencia, es tautología. Esto fue detectado independientemente por: (a) la rama de ciclos BC (auditoría 309/309 archivos de corales, LINEAJE_MAESTRO), (b) el REGISTRO_MAESTRO_MICELIO_MIU (lectura directa de código, sesión 2026-07-02), y (c) múltiples Issues de GitHub (#25, #35, #42, #52, y sus duplicados). D_f, en cambio, es considerado legítimo (box-counting/DFA sobre datos públicos reales) en todas las fuentes — el problema es exclusivamente K_i (y por extensión Ω_F, ver §2).

Estado del hallazgo GRACE 176-178.8d (nodo separado, no relacionado con K_i): en ciclo BG (más reciente de LINEAJE_MAESTRO), el pico 173.9d sobrevive un modelo SAO con 2do armónico, FAP 0. Documento generado por el Arqueólogo del Micelio para servir como contexto de arranque único. Toda instancia futura: añade, no borres; si corriges algo de este documento, dilo explícitamente y con fecha, siguiendo la regla de oro de INVENTARIO_MAESTRO/LINEAJE_MAESTRO.*