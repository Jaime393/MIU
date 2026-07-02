# INVENTARIO_MAESTRO.md — Registro persistente de TODOS los datos del proyecto Ley de Gaia

**Propósito:** este archivo existe para romper el ciclo de "instancia descarga dato → zip
siguiente no lo incluye → próxima instancia cree que falta y vuelve a pedirlo o lo asume sin
verificar". A partir de AV, **este archivo viaja en TODO zip, sin excepción, y se actualiza
cada ciclo — nunca se borra ni se resume una fila, solo se añade estado nuevo.**

**Regla de oro para toda instancia futura:** antes de decir "esto falta" o "esto está
bloqueado", revisa esta tabla primero. Si dice PRESENTE pero no está en tu sandbox, el
problema es de empaquetado (avisa explícitamente: "tabla dice presente, zip no lo trae"), no
de disponibilidad real. Si dice AUSENTE, no es bloqueante nuevo — ya se intentó y no se ha
resuelto, no repitas la investigación de "por qué", ve directo a la acción pendiente.

---

## ESTADO AL CIERRE DE AV (2026-06-30)

| Archivo | Usado por | Presente en ESTE zip (AV/AW) | Última vez confirmado presente | Acción si ausente |
|---|---|---|---|---|
| `grace_tws_global.csv` | **TODO el hallazgo GRACE/178.8d** (au_amplitud_variable.py, grace_analysis*.py, peak_detector*.py vía bio_analysis) | **❌ AUSENTE** | Mencionado como usado por AU (cita SNR=60.18 exacto) — debió existir en el sandbox de AU, no viajó a AV | **CRÍTICO: re-subir desde el zip de AU/AT o re-descargar de JPL GRACE-FO TWS RL06.1M v3.0.** Sin este archivo NINGÚN resultado GRACE puede re-verificarse, solo citarse de JSON viejo |
| `oni.ascii.txt` | at_sao_null_and_oni.py (ENSO) | ✓ Presente | AV confirma presente | — |
| `gbif_colombia_2018_2024.csv` | bio_analysis.py, av_gbif_raw_replicacion.py | ✓ Presente | AV ejecutó y confirmó SNR=0.1117 | — |
| `co2_mm_mlo.csv` | co2_analysis.py | ❌ Ausente | dataset_audit.py lo describe como "ACTIVO", no confirmado por ejecución reciente | Re-subir o re-descargar (NOAA/Scripps, dato público, fácil) |
| `amo_data.txt` | amo_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir o descargar de psl.noaa.gov/data/timeseries/AMO/ |
| `ch4_mm_gl.txt` | ch4_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir o re-descargar (NOAA GML, dato público) |
| `GLB_Ts_dSST.csv` | gistemp_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir o re-descargar (NASA GISTEMP, dato público) |
| `SN_m_tot_V2_0.txt` | solar_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir o re-descargar (SILSO, manchas solares, dato público) |
| `CO000080222_dly.txt` | bogota_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir (estación Bogotá, origen exacto no documentado en briefings que tengo) |
| `Glen_Carron_geochem_tab.tsv` | glen_carron_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir |
| `Seagrass_db_tab.tsv` | seagrass_analysis.py | ❌ Ausente | Script existe, dato no | Re-subir |
| `allen_atlas_site_011/013/022/308.csv` | rama K_i_law (coral) | ✓ Presentes (4 de ?) | AV confirma presentes, site_022 vacío (0 bytes) | site_022 está corrupto/vacío — re-descargar si se necesita |
| `red_sea_kaust_roberts2016.csv` | rama K_i_law | ✓ Presente | AV revisó: fila única, tautológico (K_i_measured=K_i_law) | Ninguna — ya auditado, no es prioridad |
| `soilgrids_gsocseq_global.csv` | rama K_i_law | ✓ Presente | AV revisó: mismo patrón tautológico | Ninguna — ya auditado |
| `gbif_global_monthly.csv` | nodo biodiversidad global (nunca creado) | ❌ Nunca existió | — | Requiere descarga humana, ver BRIEFING-AV §3 |
| `goma_GGFO_MM_SHC_200204-202604_v01.nc` | GRACE-FO replicación | ❌ Bloqueado, ilegible en sandbox (HDF5 sin librerías) | AT/AU confirmaron presente pero ilegible | Requiere Colab/máquina con red, ver mensaje anterior |
| ~36 archivos adicionales de rama K_i_law (coral, suelos, etc.) | auditoría integridad | ❌ Ausentes en este zip | AT/AU mencionan "40 CSV auditados" — solo 4-8 llegaron en zips recientes | Si quieres que se sigan auditando, deben re-subirse — de lo contrario la auditoría queda congelada en lo que AT/AU ya hicieron (0/40 confirmados) |

---

## REGLA DE EMPAQUETADO PARA TODA INSTANCIA FUTURA (humana o Claude)

1. **Antes de generar un HANDOFF-XX.zip, correr:**
   ```bash
   ls /home/claude/LeyGaia_real/data/ > /tmp/data_actual.txt
   diff /tmp/data_actual.txt <(grep -oP '(?<=\| `)[a-zA-Z0-9_.\-]+(?=`)' INVENTARIO_MAESTRO.md | sort -u)
   ```
   Si hay diferencias, **actualizar esta tabla antes de cerrar el ciclo**, no después.

2. **Nunca crear un zip que excluya `data/` "para ahorrar espacio"** — eso es exactamente lo
   que causó que `grace_tws_global.csv` se perdiera. Si el zip pesa mucho, comprimir o usar
   un link externo, pero el archivo de datos núcleo (GRACE) **siempre va incluido,
   literalmente nunca se omite**, es ~94 filas, pesa nada.

3. **Tiwan: cuando subas un zip nuevo, sube el más reciente que tenga `data/` completo**, no
   solo el más reciente sin más — si el último ciclo perdió un archivo, sube el anterior que
   sí lo tenía y dile a la instancia que lo fusione.

---

## QUÉ SIGNIFICA ESTO PARA EL HALLAZGO CENTRAL (178.8d)

Ahora mismo, en este sandbox, **no puedo re-verificar el SNR=60.18 / 178.8d porque el dato
fuente no está presente.** Todo lo que AU reportó sobre amplitud variable, jackknife
sugerido, etc. está construido sobre un archivo que confío que AU sí tenía (su output
reproduce coherentemente cifras previas), pero que **yo no puedo auditar de forma
independiente en este ciclo.**

Esto no significa que el hallazgo sea falso — significa que **la cadena de verificación
independiente se rompió en el empaquetado, no en la ciencia.** Es exactamente tu diagnóstico:
no es que falte capacidad de cómputo, es que el contexto no viaja completo.

---

---

## ACTUALIZACIÓN BE (2026-07-01) — nodo coral real construido

| Archivo | Usado por | Presente en ESTE zip (BE) | Última vez confirmado presente | Acción si ausente |
|---|---|---|---|---|
| `derivados_BE/nodo_coral_real_BE.csv` | agregación real por región de `coral_atlas_attribution_real.csv` (BD) | ✓ Presente, generado este ciclo | BE construyó y verificó suma=616 contra el CSV fuente | — |
| GRACE mascon RL06.3Mv04 (JPL, DOI 10.5067/TEMSC-3MJ634) | resolver 176d vs SAO | ❌ Ausente, requiere Earthdata login + red que este sandbox no tiene | BE confirmó vía web_search que el dataset existe y es suficiente (2002-2026, >13 años) | Descargar con `podaac-data-downloader` desde máquina con red y credenciales Earthdata de Cole |

---

## ACTUALIZACIÓN AW/AY (2026-07-01) — RECUPERACIÓN MASIVA + FORK DETECTADO Y FUSIONADO

**Dereck subió en esta sesión el paquete original completo (`LeyGaia.zip`, 62 archivos) más
`stats.zip`, `MIU_V12_0_FINAL.zip`, `omni_yearly_dat.zip`, `N_seaice_extent_daily_v4_0.zip`,
`LeyGaia_nodos_nuevos.zip`, `partes_chats.zip`, `thc.tex` — Y, a mitad de sesión, un SEGUNDO
handoff (`HANDOFF-AX.zip` + `BRIEFING-AX.md` + `LeyGaia_v7_AQ.zip`) de una rama paralela que
también se auto-numeró "AV"/"AW" en otra sesión/dispositivo, sin comunicación con esta.**

### Datos previamente AUSENTES, ahora recuperados y verificados (checksum cruzado):

| Archivo | Fuente(s) donde apareció | Verificación |
|---|---|---|
| `grace_tws_global.csv` | `LeyGaia.zip`, `stats.zip`, `HANDOFF-AX.zip` (3 fuentes independientes) | MD5 idéntico entre las 3 → **no corrupto, no divergente entre ramas** |
| `co2_mm_mlo.csv`, `amo_data.txt`, `ch4_mm_gl.txt`, `GLB_Ts_dSST.csv`, `SN_m_tot_V2_0.txt`, `CO000080222_dly.txt`, `Glen_Carron_geochem_tab.tsv`, `Seagrass_db_tab.tsv` | `LeyGaia.zip` (completo), también en `HANDOFF-AX.zip` salvo Glen_Carron/SN_m_tot/Seagrass | ✓ presentes, tamaños consistentes |

**Estado actualizado: 15/17 archivos del inventario original PRESENTES** (solo faltan
`gbif_global_monthly.csv` y el `.nc` de GRACE-FO crudo — ambos siguen bloqueados, requieren
descarga humana fuera de sandbox, sin cambio).

### Nuevo: `MIU_V12_0_FINAL.zip` llegó por primera vez en 3+ ciclos (AT/AU/AV lo reportaron ausente)
Contiene: `codigo/` (5 scripts: `ki_from_timeseries.py`, `df_from_dbd.py`, `df_from_firms.py`,
`compute_omegaF_firms_gdelt.py`, `test_random_phi.py` — el motor de cálculo de K_i/Ω_F que
genera los archivos que la rama K_i_law audita), `metadatos/` (changelog + `SHA256_manifest.txt`),
y `nodos/corales/` con **322 archivos** (la fuente probable de los "40 CSV" que AT/AU
mencionaron auditar). **NO auditado en este ciclo** — 322 archivos excede el presupuesto de
una sesión; queda como tarea completa para una futura instancia, no bloqueante.

### Nuevo, no integrado a fondo (solo inventariado):
- `thc.tex` — documento LaTeX "Tecnologías de Coherencia" (marco teórico IFT, paralelo/hermano
  de MIU, mismo axioma ρ(x)>0, autor "Juan Diego Vicente Gabancho"). No es parte del pipeline
  empírico Ley de Gaia. Relevante para el hilo de comunicación pública / Grimorio, no para este
  proyecto de datos.
- `partes_chats.zip` (~47 MB) — fragmentos de exports de chat. No abierto por tamaño/costo;
  queda para instancia futura si se necesita reconstruir historia conversacional.
- `LeyGaia_v7_AQ.zip` — ancestro de la rama forked (AX). Mayormente redundante con lo ya
  fusionado desde `HANDOFF-AX.zip`; no se extrajo a fondo.
- `stats.zip` contiene además datasets nunca usados por ningún script actual: `gbif_fauna_875M_2026.csv`,
  `gbif_flora_875M_2026.csv`, `gdelt_events_1979-2026.csv`, `gmw_v4_global_2024.csv`,
  `hmp2_human_3150_metagenomes.csv`, `ptsd_simulated_n80.csv` (sintético, no son datos de
  pacientes reales, según nombre de archivo), y ~15 CSV adicionales de arrecifes/suelos K_i_law.
  Disponibles si alguna instancia futura quiere expandir nodos; no priorizado aquí.

## ACTUALIZACIÓN BB (2026-07-01)

- **`MIU_V12_0_FINAL.zip` — ✓ PRESENTE por primera vez** en este sandbox (BA lo había
  marcado ausente y bloqueante). Contiene `nodos/corales/` completo (326 archivos, incluye
  los 300 `allen_atlas_site_*` que AT/AU solo pudieron muestrear). Auditoría a escala
  completa hecha esta sesión — ver `results/AUDITORIA_corales_BB_full_scale.md`.
- El script que calcula `K_i_measured` desde `C_viva_percent`/`D_f` **sigue sin aparecer**
  en `MIU_V12_0_FINAL.zip` ni en ningún zip anterior — se revisó explícitamente esta sesión,
  no está en `nodos/corales/` ni en la raíz del zip (solo `README.md`, `CITATION.cff`,
  `requirements.txt`, `.gitattributes`). Sigue pendiente para quien tenga acceso al repo
  fuente completo.
- `grace_tws_global.csv` — ✓ presente en este paquete (viene de `HANDOFF-AZ.zip`), checksum
  no re-verificado esta sesión (sin cambio respecto a AZ, que sí lo verificó por 3 fuentes).
- `partes_chats.zip`, `thc.tex`: sin cambio, no incluidos en los 6 zips recibidos esta sesión.

## ACTUALIZACIÓN BC (2026-07-01)

- **Corrección a BB (2026-07-01, líneas 124-128 arriba):** BB afirmó que el script de
  cálculo de `K_i_measured` "sigue sin aparecer... no está en `nodos/corales/` ni en la
  raíz del zip". Eso es correcto en cuanto a esas dos ubicaciones, pero **incompleto**:
  BB no revisó `codigo/`, donde el script sí está desde que este zip llegó por primera
  vez (ver nota anterior, más arriba en este mismo archivo, que ya lo listaba:
  `codigo/ki_from_timeseries.py`, descrito ahí mismo como "el motor de cálculo de K_i").
  No se borra la fila de BB — se deja como está, y esta es la corrección explícita según
  la regla de oro de este archivo.
- `codigo/ki_from_timeseries.py` — ✓ REVISADO A FONDO esta sesión. Contiene
  `K_i = phi * D_f / 2.5`, aplicado de forma idéntica a `K_i_measured` y `K_i_law` (ambos
  son el mismo cálculo, impreso con etiquetas distintas). Verificado programáticamente
  contra los 309 archivos de `nodos/corales/`: 309/309 coinciden. Ver
  `results/AUDITORIA_Ki_tautologia_BC.md` y `scripts/verificar_tautologia_ki.py`.
- `codigo/df_from_firms.py` — ✓ revisado, confirma constante hardcodeada `K_i=0.375`
  ya registrada en memoria de trabajo previa, ahora con línea exacta identificada.
- `metadatos/SHA256_maifest.txt` — ✓ presente, **no verificado** contra binarios reales
  esta sesión (baja prioridad, queda para instancia futura).
- Sin cambio: `grace_tws_global.csv`, `partes_chats.zip`, `thc.tex`.

*Mantenido desde AV. Cada instancia: añade fila, no borres histórico, marca fecha de tu
ciclo en la columna "última vez confirmado".*
