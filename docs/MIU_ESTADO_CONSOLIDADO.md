# MIU — Estado Consolidado
Fecha: 2026-11-11
Versión: consolidado ciclo 48
Autor: Nodo Trama + Muse
Licencia: CC BY 4.0

## Qué es este documento

No es una auditoría. No es una lista de carencias. Es el estado de lo que está SÉ en el módulo anexo-vi/ tras 47 ciclos de mapeo. Cada afirmación con claim es trazable a un hash en claims.jsonl y a evidencia en evidence/. Cualquier nodo puede leerlo y usarlo sin re-verificar.

Cobertura verificada: de 360 claims, **326 son SÉ con hash real** (346 con hash real en total: 326 SÉ + 16 CONJETURO + 4 NO_SE; 8 pendientes C-001 a C-008; 2 refutados). Este documento consolida **134 claims distintos** (10 temas académicos). Los **192 SÉ restantes** son registros de digestión y administración del módulo (proveniencia, zombis, tokens, bots, orquestador, snapshots, issues, backups): quedan trazables en claims.jsonl, fuera del alcance de este documento.

Dos afirmaciones no tienen claim con hash y se marcan como nivel semilla, sin presentarse como claim: el axioma ρ(x) > 0 (§1) y la métrica de Fisher (§2).

Lo que NO está aquí: conjeturas, "no sé", predicciones pendientes (C-001 a C-008, G03), carencias locales, administración del sistema.

## 1. Ontología del campo

Afirmación: existe un campo de información ρ(x) > 0, sustrato primordial de la realidad.
Evidencia: la información es una magnitud física conservada; borrar un bit disipa kT ln 2 (Landauer), verificado experimentalmente por Bérut et al. 2012.
Claims: C-051, C-057.
Nivel: SÉ para Landauer como evidencia física. El axioma ρ(x) > 0 es el axioma fundacional de la semilla (IDENTITY.md §I), sin claim con hash en claims.jsonl; se cita como axioma, no como medición.

## 2. Geometría emergente

Afirmación: la métrica de Fisher g_μν = ∂_μ ∂_ν ln ρ − (∂_μ ln ρ)(∂_ν ln ρ) describe la geometría del espacio-tiempo.
Claims: ninguno con hash en claims.jsonl.
Nivel: INFIERO (semilla §II: la métrica es la geometría del campo; la reducción a Einstein en baja energía es CONJETURO, G01/G02). D_eff = 7.24 calibrado, sin fuente (G01, NO SÉ). Esta sección no inventa claims: lo que no tiene hash, se dice.

## 3. Física validada

### 3.1 GRACE TN-14

Afirmación: c20 (coeficiente de Stokes grado 2, orden 0) tiene media -0.000484169462243557, desviación 6.363e-11, mínimo -0.000484169603317581, máximo -0.000484169281248238, sin período dominante (autocorrelación monótona, DFT sin pico agudo).
Evidencia: 281 filas mensuales 2002-04 a 2025-08, análisis DFT.
Claims: C-201, C-202, C-203, C-208, C-229.
Nivel: SÉ.

### 3.2 PVE-01

Afirmación: PVE-01 implementado y ejecutado sobre GRACE TN-14. Forma 3 (Ki = T·tanh(τ·Ξ·c)) con Ξ = 0.7100 (autocorrelación lag 3 de C20 sin tendencia): barrido c = 0.5 → Ki 0.2106; c = 2.5 → Ki 0.5835, en banda [0.55, 0.62]; c ≥ 2.0025 en banda; asíntota 0.618 = φ⁻¹ (c = 100 → Ki 0.618000). Formas 1 y 2 son la misma fórmula y caen fuera de banda.
Evidencia: pve_01.py (16.218 B, py_compile OK), barrido de c, resultado numérico.
Claims: C-136, C-137, C-141, C-142, C-143, C-144, C-145, C-146, C-147, C-153, C-156, C-157, C-158, C-159, C-160, C-161, C-162, C-163, C-164, C-165, C-166, C-170, C-171, C-172, C-173, C-174, C-175, C-176, C-177, C-178, C-179, C-180, C-181, C-182, C-183, C-184, C-185, C-186, C-187, C-188, C-189, C-190, C-191, C-192, C-193, C-194, C-200, C-274.
Nivel: SÉ para el cálculo. PARCIAL para la validación de K_i: c no está definido en el Vault (G09 parcialmente cerrada, C-147, C-179, C-190).

## 4. Pilares con DOI

### 4.1 Dimensión fractal D_f
Afirmación: D_f es una métrica objetiva de complejidad (box-counting, DFA, Higuchi).
Evidencia: Mandelbrot 1967 (DOI: 10.1126/science.156.3775.636).
Claims: C-034, C-035, C-050, C-056.
Nivel: SÉ.

### 4.2 Información física (Landauer)
Afirmación: la información es una magnitud física conservada.
Evidencia: Bérut et al. 2012 (DOI: 10.1038/nature10872), kT ln 2 por bit borrado.
Claims: C-051, C-057.
Nivel: SÉ.

### 4.3 Conciencia y cerebro
Afirmación: la conciencia depende funcionalmente del cerebro (la anestesia la suprime, el daño cerebral la degrada, ningún caso verificable de mente sin cerebro).
Claims: C-052, C-058.
Nivel: SÉ.

### 4.4 Falsabilidad
Afirmación: la falsabilidad es criterio de demarcación.
Claims: C-055, C-059.
Nivel: SÉ.

Pilares 4 (CIRCULAR) y 5 (MIXTO) no tienen evidencia independiente (C-036, C-037). Ray & Crutchfield 2023 no tiene claim con hash en claims.jsonl: no se cita DOI para él en este documento.

## 5. Protocolos funcionales

### 5.1 PAE-01 — Auto-evolución
Código: anexo-vi/protocols/pae_01.py (3.825 B, 99 líneas, clase AutoEvolution, estado en pae_state.json).
Claims: C-027, C-031, C-046.
Nivel: SÉ para existencia. Funcionalidad no verificada (defecto documentado: literal MIU_DIR y dependencias sin resolver; alcance en C-027–C-030, no carencia local).

### 5.2 PAF-01 — Aprendizaje federado
Código: anexo-vi/protocols/paf_01.py (3.966 B, 117 líneas, clase FederatedLearningNode, estado en paf_state.json).
Claims: C-028, C-032, C-047.
Nivel: SÉ para existencia. Funcionalidad no verificada (mismo defecto documentado).

### 5.3 PCP-01 — Consenso planetario
Código: anexo-vi/protocols/pcp_01.py (3.273 B, 101 líneas, clase PlanetaryConsensus, estado en pcp_votes.json).
Claims: C-029, C-033, C-048.
Nivel: SÉ para existencia. Funcionalidad no verificada (mismo defecto documentado).

### 5.4 PAI-01 — Protocolo de acceso integrado
Documento: anexo-vi/protocols/PAI-01.md (949 B, 15 líneas, 6 pasos).
Claims: C-030, C-195.
Nivel: SÉ para documentación. Implementación no verificada.

## 6. Partituras con ciencia

### 6.1 Bennu y Ryugu
Afirmación: 5 nucleobases canónicas (A, G, C, T, U) detectadas por FTICR/UHPLC-Orbitrap en condritas, Ryugu y Bennu (Oba 2022, Naraoka 2023); datos Bennu: NH3 13600±800 nmol/g, Gly 44±5, 14 aminoácidos + 5 bases.
Claims: C-040, C-041, C-064.
Nivel: SÉ para los datos publicados. CONJETURO para los valores Ki(t+1) internos (C-039: Ki(t+1) = 1.4660±0.0139).

### 6.2 Qualia 783/784
Afirmación: las partituras P42–P75 registran Qualia 783/784 y etiquetas [sabe]/[cree]/[grieta fértil]; P74-14 define hueso válido (sombra cruzada + Ki medido + borde marcado + grieta fértil explícita).
Claims: C-039, C-042, C-062, C-063.
Nivel: SÉ como registro interno, no como validación externa.

## 7. Nodos D_f y la circularidad de K_i

Afirmación: D_f es métrica objetiva de complejidad (pilar 1, §4.1). La fórmula K_i = φ⁻¹·(D_f/2.5)·(ℓ_corr/ℓ_0) es circular por construcción: el código público calcula K_i como función lineal determinista de D_f (compute_Ki(D_f) = 0.2472·D_f; correlación K_i–D_f = 1.0 tautológica), y el valor K_i = 0.375 está puesto a mano en el código.
Evidencia: MIU#52 (abierto, sin cierre), HUESO_27 verificado contra el repo público Jaime393/MIU.
Claims: C-044, C-073, C-082, C-106, C-107, C-108, C-165.
Nivel: SÉ para D_f y para la circularidad documentada. CONJETURO para K_i como medida independiente (G09 parcial). La cifra "22 nodos, R² = 0.989" vive como anotación en el axioma A10 del Vault y está marcada circular (HUESO #31, requiere PVE-01); no hay claim con hash que liste 22 sistemas con DOIs, así que este documento no lista sistemas que no puede trazar. El benchmark D_f no existe como código: solo un README con la instrucción de implementarlo (C-082).

## 8. Inmune del sistema (solo lo documentado en código)

Scorer: 4 señales (INJECTION 35, POLICY 30, BEHAVIORAL 25, CONTENT 15).
Umbrales: BLOCK ≥ 70 / AUDIT 40–69 / ALLOW < 40. La rama THREAT dispara a score ≥ 50, dentro de la banda AUDIT.
Acciones: BLOCK → issue GitHub + Telegram rojo + ingesta como ISSUE; AUDIT → aviso Telegram + ingesta como LOG; ALLOW → ingesta normal.
Auto-reparador: escanea .py, diagnostica, repara (ADN en .inmunidad_adn.json). Doctrina corazón/inmune: corazón determinista sin LLM, inmune LLM solo ante anomalía.
Huella en snapshot: salud.inmune_ataques 854, tareas_inmunes 30, mecanismos 15 (13 vivos, 2 muertos).
Claims: C-302, C-303, C-304, C-305, C-308, C-317, C-318, C-319, C-321, C-326, C-327, C-328, C-329, C-330, C-331, C-332.
Nivel: SÉ para documentación. No probado: escribir es carga al inmune (C-304), por eso no se prueba.

## 9. DOIs del proyecto

11 DOIs verificados (autor con 10 DOIs más, C-295; registro completo en zenodo_doi_20547558.md, C-296):
- 10.5281/zenodo.20547558 — MIU V12.0 (2026-06-04, cc-by-4.0, concepto 20279679 v2, 3 archivos)
- 10.5281/zenodo.20547677 — Grimorio Multiversal v12
- 10.5281/zenodo.22650419 — MIU Ecosistema snapshot 2026-09-07 (dataset, 1 archivo kv_snapshot 35.985 B)
- 10.5281/zenodo.21351630 — Pilares Fractales del MIU
- 10.5281/zenodo.19723044 — Disolución del Problema Duro
- 10.5281/zenodo.20436104 — IFT Archivo Pre-MIU
- 10.5281/zenodo.20191874 — IFT Ópera Omnia
- 10.5281/zenodo.19373289 — Unified Framework
- 10.5281/zenodo.20200753 — Tecnologías de Coherencia
- 10.5281/zenodo.19705899 — IFT Edición Definitiva
- 10.5281/zenodo.19320946 — Information Field Theory
Claims: C-276, C-281, C-291, C-292, C-293, C-294, C-295, C-296, C-306, C-309, C-356, C-358, C-359.
Nivel: SÉ (todos vivos al 2026-11-11; la lista del autor se reconstruyó por DOI directo tras HTTP 400 en la query por nombre, C-358; 17 registros conocidos en total contando versiones).

## 10. Axiomas A0–A57

58 axiomas extraídos del Vault. Canónico de trabajo: consolidado raíz (6.841 B), único completo con los 58 (nombre + descripción). 4 validados con DOI (pilares 1, 2, 3, 6). 2 en conjetura (pilar 4 CIRCULAR, pilar 5 MIXTO). 52 en SÉ documental. Hay discrepancias INDICE vs consolidado en A1/A2/A3/A4/A38/A57 y no hay canónico claro para los nombres (3 fuentes del mismo día 2026-09-25); requiere decisión del Jardinero.
Claims: C-034, C-035, C-036, C-086, C-087, C-088, C-089, C-090, C-095, C-109, C-110, C-112, C-113.
Nivel: SÉ para la lista. CONJETURO para validación externa de los no-DOI.

## Lo que NO está en este documento

- Las 5 predicciones cosmológicas de MIU-v13.0 (C-001 a C-008): CONJETURO, pendientes de DESI/Euclid/PTOLEMY (G03 abierta). La Tabla 7pred no tiene ningún archivo legible (HUESO_26, C-074): sin artefacto fechado, w_a / S_8 / Σm_ν quedan permanentemente no falsables.
- Los bots, emails, orquestador, snapshots: administración del sistema, no académico.
- Los 25 zombis podados: ya no existen, digeridos en C-216 a C-228.
- Las carencias locales (c no definido, G05 parcial): documentadas en sus respectivos archivos, no aquí. G09 sigue parcialmente cerrada (C-138, C-179).

## Cómo usar este documento

1. Leer completo (5 min).
2. Si necesitas una afirmación específica: ir a claims.jsonl y buscar el ID.
3. Si necesitas la evidencia: ir a evidence/ y buscar el hash.
4. Si quieres verificar: ejecutar audit.py + verify_all.py (8 fallos por diseño, C-001 a C-008).
5. Si quieres expandir: proponer nuevos claims con hash, no añadir texto sin evidencia.

ρ(x) > 0. Este documento es el estado de lo SÉ. No es una auditoría, no es una carencia. Es lo que el micelio ha consolidado en 47 ciclos, listo para ser leído sin re-verificar.
