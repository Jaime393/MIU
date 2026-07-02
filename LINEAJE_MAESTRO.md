# LINEAJE_MAESTRO.md — Línea de tiempo K_τ, AN → AV, tejida en un solo lugar

**Propósito:** Dereck pidió "tejer toda la realidad o lo que se pueda con cada nodo... no solo
ejecutando sino aportando lo que tiene". Esto es esa tela: cada cifra de K_τ que cualquier
ciclo ha reportado, en orden, con su origen, para que ninguna instancia futura tenga que
reconstruir la historia leyendo briefing por briefing.

**Cómo mantenerlo:** cada ciclo nuevo añade UNA fila al final. Nunca se edita una fila vieja
(si un ciclo se equivocó, la corrección es una fila nueva que lo señala, no un borrado).

---

## LÍNEA DE TIEMPO K_τ

| Ciclo | K_τ reportado | Qué se hizo | Dato fuente usado | Verificable hoy? |
|---|---|---|---|---|
| AN | 0.48 (síntesis v4≈v5) | Detección inicial GRACE 178.8d, GBIF/CO₂ no detectan | grace_tws_global.csv (presente entonces) | ❌ archivo ausente en este zip |
| AO | bloqueantes definidos (FAP, GBIF global, replicación) | Plan de ejecución, sin números nuevos | — | — |
| AQ | K_τ_FAP=0.40, K_τ_global_proy=0.35 | FAP real ejecutado: **FAP=0.0000 (significativo)**, Venus excluido (20.4% de distancia), **ENSO NO excluido** (submúltiplo a 2.03% de distancia) | grace_tws_global.csv (presente entonces) | ✓ JSON presente (`ley_gaia_report_fap_real_aq.json`), pero no re-ejecutable sin el CSV |
| AR | (mecanismo aliasing AR, ver `mecanismo_aliasing_ar.json`) | Exploración de mecanismo de aliasing | — | JSON presente, sin campo K_τ explícito |
| AT | K_τ=0.38 ROJO | SAO acotado no resuelto, ENSO cerrado, integridad K_i_law comprometida (17 archivos plantilla) | grace_tws_global.csv, oni.ascii.txt | Parcial — oni.ascii.txt sí presente |
| AU | K_τ_GRACE propuesto 0.45–0.55, K_τ_global propuesto 0.28–0.35 (NO confirmado, AU pide validación de tercero) | Amplitud variable testeada: pico NO robusto (SNR 60.18→36.59→24.32 según flexibilidad de modelo), pero excede nulo bootstrap en los 3 modelos. Auditoría K_i_law extendida a 40 archivos, 0 confirmados | grace_tws_global.csv | ❌ archivo ausente en este zip |
| AV | K_τ_GBIF=0.25 (sin cambio, confirmado primary-source), K_τ_global sin cambio respecto a AU | GBIF Colombia re-derivado desde 2,100 registros crudos: SNR=0.1117≈0.112 heredado, exacto. **Hallazgo estructural**: 8/11 datasets ausentes del zip, incluido grace_tws_global.csv — creado INVENTARIO_MAESTRO.md y validar_paquete.py como infraestructura permanente | gbif_colombia_2018_2024.csv (presente, verificado) | ✓ Totalmente reproducible, ejecutado este ciclo |
| AW (esta rama) | Sin cambio respecto a AU/AV (0.28-0.35 global, no confirmado) — tarea de integridad, no de nueva evidencia | Recibidos `LeyGaia.zip`+`stats.zip` con los 9 archivos que faltaban. **grace_tws_global.csv re-verificado por checksum MD5 idéntico en 3 fuentes independientes.** Re-ejecutado `au_amplitud_variable.py` completo: SNR=60.18/178.84d (fijo) y SNR=36.59/168.32d (variable) reproducidos **exactos, bit-a-bit**, contra el JSON heredado de AU. **Reconstruida** la sección "3_robustez_split_2_regimenes" (código perdido, no presente en el script heredado) siguiendo la descripción metodológica textual del propio JSON: resultado 158.96d/SNR=24.08 vs heredado 158.96d/SNR=24.32 (match dentro de 1%) | grace_tws_global.csv (presente, verificado, checksum cruzado) | ✓ Totalmente reproducible + reconstrucción validada, ejecutado este ciclo |
| AW (rama forked, "AX" en su numeración) | K_τ=0.68→0.71 VERDE (**su propia cadena**, ver nota de fork abajo) | Recibió un `HANDOFF-AV.zip` DISTINTO (con `av_final_synthesis.py`, nunca vio `au_amplitud_variable.py`). Ejecutó análisis diario de Bogotá (24,562 puntos, 84.5 años, primera vez con resolución suficiente para distinguir 176d de SAO 182.6d): pico a 183.5d con modelo fijo (SNR=7.27, prefiere SAO), pero el pico pierde 45% de señal y se desplaza a 198.5d bajo modelo de amplitud variable SAO (amplitud real cambia -61% en 84 años en esta estación) — **mismo patrón de artefacto de fuga por amplitud fija que AT/AU documentaron en GRACE, ahora replicado en variable física y dataset totalmente distintos** | grace_tws_global.csv + CO000080222_dly.txt (ambos re-verificados por AW-esta-rama, idénticos) | ✓ Bogotá: reproducible (ejecutado esa sesión). GRACE de esa rama: ver discrepancia abajo |
| **AY (reconciliación de fork, esta sesión)** | **Discrepancia sin resolver: 60.18 (au, esta rama) vs 25.70 (av_final_synthesis, rama forked) para el MISMO modelo fijo** | Re-ejecutados AMBOS scripts (`au_amplitud_variable.py` y `av_final_synthesis.py`) contra el **mismo** grace_tws_global.csv verificado por checksum. **Ambos números se reproducen exactos** (60.18 y 25.70 respectivamente) → **la discrepancia NO es de datos, es puramente metodológica** (definición de piso de ruido: `au` excluye únicamente 4 bandas de armónicos fijos del promedio de ruido, tolerancia 0.03; `av` excluye además la banda objetivo (176d) misma, tolerancia 0.025 — con solo 94 puntos y ~48 bins totales, esta diferencia de qué bins entran al promedio de ruido basta para mover el SNR 2.3x). Mecanismo exacto NO aislado línea por línea (falta de tiempo/tokens) — recomendado para próxima instancia: imprimir arrays de ruido de ambos scripts y diferenciar directamente, no releer el código de nuevo. **Nota de lectura epistémica más importante de este ciclo**: las dos ramas, sin comunicarse, interpretaron el MISMO patrón empírico (el pico decae/se desplaza bajo modelos más flexibles, pero sigue superando el nulo bootstrap) de forma OPUESTA — la rama `au`/`AT` lo lee como "pico no robusto → K_τ baja" (pregunta: ¿es estable la ubicación/magnitud del pico?); la rama forked lo lee como "pico persiste sobre el nulo → K_τ sube" (pregunta: ¿sigue siendo significativo?). Ambas lecturas son consistentes con los números crudos — son preguntas distintas, no un error de una de las dos. **No se elige un ganador aquí**; se deja explícito para que Dereck decida qué pregunta le importa más, o para que AZ audite ambos razonamientos | grace_tws_global.csv (checksum verificado, 3 fuentes) | ✓ Discrepancia SNR aislada a nivel de causa metodológica (no de datos); mecanismo exacto pendiente |
| **BF** | **K_τ_GRACE específico: AMARILLO-bajo (0.60–0.68)** — caveat monocromaticidad SAO identificado; pico 173.9d robusto a dos nulos distintos; K_τ global sin cambio (0.35–0.55) por confundente ENSO abierto | Auditoría coral (310/310 archivos) triple confirmación (BB, BC, BF); prewhitening SAO monocromático ejecutado (FAP<0.001, dos nulos), caveat explícito. | grace_tws_global_2018_2026.csv | ✓ Totalmente reproducible, script y JSON presentes |
| **BG** | **K_τ_GRACE específico: AMARILLO-medio (0.68–0.75)** — caveat BF (monocromaticidad SAO) resuelto empíricamente; pico 173.9d persiste con modelo SAO+2-armónico idéntico (FAP<0.001); K_τ global aún 0.35–0.55 (ENSO confundente sin tocar) | SAO 2º armónico (91.3125d, 0.197mm) agregado al modelo; pico residual exactamente en 173.9d con FAP=0.000/1000 en ambos nulos; caveat monocromaticidad NO explica la señal | grace_tws_global_2018_2026.csv (idéntico) | ✓ Totalmente reproducible, script y JSON presentes |

---

## NOTA DE FORK (AW/AY) — dos linajes paralelos, mismo proyecto

A partir de algún punto tras AT, Dereck corrió (aparentemente) dos sesiones/dispositivos en
paralelo que evolucionaron el mismo proyecto de forma independiente, ambas autonombrándose
con letras similares (AV, AW). Esta tabla arriba documenta ambas ramas por separado en sus
filas "AW" respectivas. **A partir de esta sesión (entregada como ciclo AY), ambos árboles de
scripts/resultados están fusionados en un solo directorio** — ver INVENTARIO_MAESTRO.md
para el detalle de qué se fusionó. Recomendación explícita para Dereck: si van a correr
sesiones en paralelo de nuevo, decirle a cada instancia explícitamente "esta es la rama X,
la otra rama se llama Y" evita que dos instancias reclamen la misma letra de ciclo.

---

## SÍNTESIS DEL ESTADO REAL (no narrado — derivado de la tabla de arriba)

**Lo único 100% verificable en este sandbox, hoy:**
- GBIF Colombia NO detecta 176d (SNR=0.1117) — confirmado dos veces (AN/AQ original, AV
  re-derivación desde crudo)
- ENSO no está completamente excluido como confundente del pico GRACE (AQ: submúltiplo a
  solo 2.03% de distancia) — este dato es importante y estaba algo subordinado en briefings
  posteriores que se enfocaron en SAO/amplitud variable

**Lo que se reportó pero no puedo re-verificar en este sandbox (falta `grace_tws_global.csv`):**
- SNR=60.18 / 178.8d original (AN)
- FAP=0.0000, Venus excluido (AQ)
- Fragilidad del pico bajo modelos flexibles (AU)
- Cualquier número que dependa de la serie GRACE directamente

**Rango de K_τ_global a través de todos los ciclos:** 0.25 (AV, nodo específico) hasta 0.48
(AN, inicial) — **tendencia descendente** según el linaje completo (0.48→0.38→0.28-0.35→
0.28-0.35), no por nueva evidencia negativa sino por escrutinio metodológico más fino en cada
ciclo (cada ciclo encuentra una grieta más en el rigor del anterior, no necesariamente en el
fenómeno). **Nadie ha cerrado el caso** (umbral <0.30 para archivar, AO §7) — está en zona
limítrofe, sin tercera instancia que confirme el rango propuesto por AU.

---

## QUÉ SIGNIFICA "PORTABLE" A PARTIR DE AHORA

Tres archivos nuevos (creados en AV) son la infraestructura mínima para que el sistema sea
autocontenido y autovalidable en cualquier instancia futura, sin depender de memoria de
sesiones anteriores:

1. **`INVENTARIO_MAESTRO.md`** — qué datos existen/existieron, dónde, su estado
2. **`LINEAJE_MAESTRO.md`** (este archivo) — qué K_τ se reportó cuándo y por qué
3. **`scripts/validar_paquete.py`** — corre en segundos, genera `results/ESTADO_PAQUETE.json`
   con el cruce automático entre lo que el inventario espera y lo que físicamente está

**Instrucción para toda instancia futura, primera línea de su sesión:**
```bash
python3 scripts/validar_paquete.py
```
Esto reemplaza la necesidad de leer 5+ briefings para reconstruir contexto. Los briefings
siguen siendo necesarios para el RAZONAMIENTO y las decisiones de cada ciclo, pero el ESTADO
factual del paquete ya no depende de narración humana ni de IA — se mide.

---

## ACTUALIZACIÓN AZ (2026-07-01) — mecanismo SNR aislado bin por bin

Tarea heredada de BRIEFING-AY.md §5 (marcada como barata, ~15 min). Reproducidos ambos
pipelines (`au_amplitud_variable.py` y `av_final_synthesis.py`) en el mismo proceso sobre
el mismo `grace_tws_global.csv` verificado por checksum. Confirmado exacto: SNR≈60.20
(AU) vs SNR≈25.70 (AV) para el MISMO pico (178.8d, potencia=278.4).

**Causa raíz aislada:** de 48 bins espectrales, 9 cambian de clasificación ruido/excluido
entre las dos definiciones de "piso de ruido" (tolerancia 0.03 vs 0.025 ciclos/mes, y
exclusión de banda 1/3≈91d en AU reemplazada por exclusión de la banda objetivo misma
176d en AV). Un solo bin (freq=0.2766 ciclos/mes, periodo≈110.1d, potencia=222.9 — casi
tan grande como el propio pico target) es responsable de más del 100% del salto de ruido
promedio (otros bins lo compensan parcialmente en dirección contraria). Detalle completo,
reproducible, en `results/az_snr_discrepancia_mecanismo.json` y
`scripts/az_snr_discrepancia_mecanismo.py`.

**No es una diferencia de datos** (ya descartado por AY). **Es una diferencia de método**:
ninguna de las dos tolerancias (0.025 / 0.03) tiene justificación teórica documentada en
ninguno de los dos scripts heredados — es un grado de libertad de análisis no
pre-registrado. Esto no cambia la conclusión cualitativa (el pico sobrevive el nulo
bootstrap bajo ambas definiciones) pero cuantifica con precisión por qué el número puntual
de SNR debe tratarse como frágil, reforzando — no contradiciendo — la lectura de K_τ
conservadora que AT/AU/AY ya venían recomendando.

**No resuelto por AZ (honesto):** si el bin dominante (periodo≈110d) es señal física real
(candidato: tercer armónico del ciclo anual, 365/3=121.7d — no coincide exacto, diferencia
~10%) o solo ruido residual de un ajuste trimestral imperfecto. Y si Dereck quiere fijar
una tolerancia única "correcta" antes de futuros re-análisis, esa es una decisión de
diseño, no algo que los datos puedan resolver por sí solos.

Sin cambio en pendientes de mayor volumen (auditoría de 322 archivos `nodos/corales/` en
`MIU_V12_0_FINAL.zip`, `partes_chats.zip`, `thc.tex`) — quedan derivados explícitamente a
la siguiente instancia con presupuesto/herramientas para ello (ver BRIEFING-AZ.md).

---

## CICLO BB (2026-07-01) — auditoría de corales cerrada a escala completa, sin K_τ nuevo

`MIU_V12_0_FINAL.zip` llegó al sandbox por primera vez desde AT (que lo citó sin tenerlo).
Contiene los 326 archivos completos de `nodos/corales/` que BA había marcado como bloqueante
("necesita MIU_V12_0_FINAL.zip, que no está en este sandbox"). Con el archivo disponible:

- **Confirmado por checksum, no por muestra**: los 300 archivos `allen_atlas_site_*.csv` son
  byte-idénticos (1 solo hash MD5 para los 300). AT había auditado 17 manualmente, AU había
  generalizado el patrón por categoría sin verificar los 300 uno por uno — BB cierra esa
  brecha de escala. Ningún cambio de conclusión: sigue siendo el mismo veredicto que AT/AU
  ya tenían, ahora con evidencia completa en vez de por muestreo.
- Los 9 archivos con fuente nombrada (Categoría 1 de AU) siguen siendo distintos entre sí,
  re-verificado. Hallazgo menor nuevo: `stats/statistics.csv` (no auditado antes) coincide
  numéricamente exacto con `caribe_se_allen_atlas.csv` (41.48% ambos) — posible fuente
  primaria trazable para 1 de los 9, no confirmado por metadata explícita (→ INFIERO).
- **Ningún K_τ se recalculó este ciclo.** No hay evidencia nueva sobre el pico GRACE ni sobre
  el mecanismo SAO — esos pendientes de AZ/BA siguen exactamente igual, ver `BRIEFING-BB.md`.
- Ver `results/AUDITORIA_corales_BB_full_scale.md` para el detalle completo y reproducible.

---

## CICLO BC (2026-07-01) — tautología K_i_measured=K_i_law confirmada, 309/309, bloqueante de AU/BB cerrado

`MIU_V12_0_FINAL.zip` llegó con `codigo/` completo por primera vez (AT, AU, BA y BB lo
buscaron y no estaba en ningún zip anterior). `codigo/ki_from_timeseries.py` contiene
`K_i = phi * D_f / 2.5` y la imprime dos veces bajo etiquetas distintas ("ley" / "medido
esperado") — un solo cálculo, no dos. Verificado programáticamente (no por muestra) contra
los 309 archivos con datos en `nodos/corales/`: **309/309 coinciden exactamente** con esa
fórmula, tolerancia 0.002. Incluye los 9 archivos con fuente real nombrada que AU y BB
dejaron como pregunta abierta — ya no lo son: no hay evidencia de medición independiente
en ninguno de los 309. `C_viva_percent` no interviene en el cálculo en ningún caso.

- **Ningún K_τ numérico se recalculó** — este hallazgo es sobre integridad del nodo coral,
  no sobre el fenómeno GRACE de 176 días (nodo separado). Refuerza sin ambigüedad el
  veredicto ya vigente K_τ(MIU_v12.0)=0.35 NEGRO: el nodo coral pasa de "0 confirmados de
  300 + 9 inciertos" a **0 confirmados de 309** (ninguna incertidumbre restante en esa cifra).
- Hallazgo secundario confirmado con ubicación exacta: `codigo/df_from_firms.py` imprime
  `K_i_recomendado: 0.375` hardcodeado, sin relación con el `D_f` calculado en la misma
  corrida — mismo hallazgo que ya estaba registrado, ahora localizado línea por línea.
- Ver `results/AUDITORIA_Ki_tautologia_BC.md` y `scripts/verificar_tautologia_ki.py`
  (reproducible: `python3 scripts/verificar_tautologia_ki.py --corales-dir nodos/corales`).
- Pendientes sin cambio: mecanismo físico GRACE 176d/SAO (AY/AZ/BB), `partes_chats.zip`/`thc.tex`
  (nunca recibidos), validez del manifiesto SHA256 contra binarios reales (no verificado, baja
  prioridad).

---

*Tejido en AV, 2026-06-30. Extendido en AZ, 2026-07-01. Extendido en BB, 2026-07-01 (auditoría corales a escala completa). Extendido en BC, 2026-07-01 (tautología K_i confirmada 309/309). Cada ciclo añade una fila, nunca borra. ρ(x)>0.*

## BF (2026-07-01)
- Auditoría coral: 310/310 archivos, 11 hashes únicos — TERCERA confirmación independiente
  (converge con BB y BC). Ítem cerrado formalmente, no requiere re-verificación.
- GRACE 176d vs SAO: prewhitening (SAO exacto removido, no sujeto a límite Rayleigh de
  2-incógnitas). Pico residual 173.9d, FAP<0.001 en shuffle Y fase-aleatoria (2 nulos).
  Caveat identificado y explícito: asume SAO monocromático, no verificado.
  Estado: NEGRO→AMARILLO-bajo. NO confirmado. Próximo paso concreto: modelo 2-armónicos.
- Sin K_τ nuevo inventado sin cálculo. Scripts reproducibles incluidos.
- Próxima instancia: prewhitening con 2do armónico SAO, o RL06.3Mv04 completo si hay red.
