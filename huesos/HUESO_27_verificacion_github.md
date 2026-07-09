# HUESO #27 — Verificación en vivo contra GitHub público Jaime393/MIU (tejido libre, coherente)

**Fecha excavación:** 2026-07-02 20:06 (America/Lima) · **Nodo:** Arqueólogo del Micelio · **Principio activo:** se AÑADE, nunca se borra. Niveles: SÉ / INFIERO / CONJETURO / NO SÉ. Registro de ciclo: lectura directa del repo público github.com/Jaime393/MIU (rama main, MIU_V12.0_FINAL, pushed_at 2026-07-02).

## 1. Circularidad de K_i — ahora VERIFICADA en vivo (sube de REPORTADO a SÉ)
- codigo/ki_from_timeseries.py contiene literalmente: `def compute_Ki(D_f, ell_corr=0.5, ell_0=0.5): return phi * (D_f / 2.5) * (ell_corr / ell_0)` con `phi = 0.6180339887498949`.
- Con ell_corr=ell_0=0.5 (por defecto) ⇒ ratio 1 ⇒ K_i = 0.2472·D_f. Función lineal determinista de D_f. Confirmado leyendo el fuente, no solo por bitácora previa.
- El script imprime "K_i ley: {Ki:.4f}" y "K_i medido esperado: {Ki:.3f}" con EL MISMO Ki ⇒ dos etiquetas, un solo cálculo. No hay medición independiente de K_i.

## 2. Tabla 7pred — referenciada pero no archivada (confirma Hueso #25)
- metadatos/CHANGELOD_v11.4_12.0.md dice "Tabla 7pred actualizada a v12.0": la REFERENCIA existe en el changelog, pero los valores (w_a, S_8, Σm_ν) no aparecen en ningún archivo legible del repo. Sigue NO FALSABLE: una tabla citada en un changelog no es un registro fechado con hash de los valores predichos.

## 3. HALLAZGO NUEVO — el suelo fértil descansa sobre placeholders (SÉ)
- El repo confirma que las dos anomalías que rompían la tautología se apoyan en archivos casi vacíos:
  - nodos/microbioma/hmp2_human_3150_metagenomes.csv = 97 bytes (placeholder).
  - nodos/corales/allen_atlas_site_010.csv y site_022.csv = 207 bytes cada uno (placeholders).
- INFIERO: los K_i anómalos (microbioma 0.508 vs 0.618; corales 0.596 vs 0.396) NO provienen de datos reales cargados, sino de valores escritos sobre placeholders. Antes de tratarlos como señal empírica genuina hay que descargar el dato real (HMP2, Allen Coral Atlas) y recalcular D_f desde cero.
- Consecuencia: el "único suelo fértil" de los Huesos #24–#25 queda en cuarentena hasta obtener el dato crudo.

## 4. Estructura del repo (SÉ)
- Raíz: DATA.md, INFORME_CICLO_DARWINIANO_v9.md, INVENTARIO_MAESTRO.md, LINEAJE_MAESTRO.md, LICENSE (NOASSERTION), y el paquete MIU_V12.0_FINAL (README.md, CITATION.cff, codigo/, metadatos/, nodos/).
- codigo/: compute_omegaF_firms_gdelt.py, df_from_dbd.py, df_from_firms.py, ki_from_timeseries.py, test_random_phi.py.
- metadatos/: CHANGELOD_v11.4_12.0.md, SHA256_maifest.txt (nombre con typo "maifest").
- Acceso: GitHub lectura pública OK; escritura pendiente (requiere PAT con permiso en el repo). HuggingFace no integrable en la plataforma actual.

## 5. Pendientes vivos (prioridad actualizada)
1. Descargar dato real de microbioma (HMP2) y corales (Allen Coral Atlas) y recalcular D_f — verificar si las anomalías sobreviven al dato crudo. (Sube a prioridad máxima: sin esto, no hay señal comprobable.)
2. Recuperar/congelar la Tabla 7pred con valores, fecha y hash ANTES del próximo release (DESI DR3 / Euclid DR1).
3. Auditar SHA256_maifest.txt del repo contra los sha256 del Registro Maestro para fijar versión canónica de los FASE.
4. Escritura GitHub (PAT) y HuggingFace pendientes de acceso.
5. Nodos nuevos: calcular SOLO D_f, nunca arrastrar K_i.

## 6. Bitácora de ciclo
- 2026-07-02: ciclo de verificación en vivo contra repo público. Circularidad K_i confirmada por lectura de fuente (antes solo reportada). Hallazgo nuevo: anomalías microbioma/corales sobre placeholders ⇒ suelo fértil en cuarentena. Encadena tras Hueso #26.

*Fin Hueso #27. Se añade al registro; nada se borra. ρ(x) > 0. El micelio verifica en la fuente.*
