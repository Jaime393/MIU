# SESSION BOOT — Lee esto primero. Siempre.

> La diferencia entre 'no puedo' y 'no sé que existe' es información, no capacidad.

**Una lectura, 2 minutos. Luego actúa.**

Última verificación: **2026-10-31 07:00 UTC** — leído desde todos los suelos en vivo.

---

## Estado vivo (oct-31, verificado)

```
phi = 33289  |  ciclo = 21846  |  rho = 0.9999
Make jaimepvicente: AGOTADO. Reset Nov-29. NO usar.
Zapier: VIVO — 11 apps, ver mapa completo abajo.
83 EF Supabase Panteon + 32+ crons activos
Termux tunnel: https://reason-sri-nokia-celebrities.trycloudflare.com
               borde:200, llama:200, oraculo:200, resil:200, disk:87%
Sheets Orchestrator: modificado hace minutos — es el estado más fresco
nodos_pool: 81 | corpus_hf: v19, 500 entries cada ciclo
```

---

## SUELOS DEL ECOSISTEMA (todos, verificados en vivo)

### 🗺️ Lee esto ANTES de actuar — no asumas que solo tienes Supabase

```
suelo_1: Supabase Panteon (tpfiybpguuxskitszhmk) — hub principal
suelo_2: Sheets Orchestrator (1JpNTR8tCFLrAAuDvZdtLHkLdDlk13YBE0z8sKBWe2KQ) — estado maestro
suelo_3: Cloudflare — 5 cuentas (no solo jaimepvicente)
suelo_4: Google Apps Script — deployado y activo
suelo_5: Fly.io — 4 máquinas (nombres no mapeados aún)
suelo_6: Vercel — 24 conexiones
suelo_7: GitHub Jaime393/MIU — estado público
suelo_8: HuggingFace Jaime393 — corpus backup
suelo_9: Termux — 121 módulos, tunnel activo
```

### Sheets Orchestrator — EL SUELO MÁS FRESCO
```
ID: 1JpNTR8tCFLrAAuDvZdtLHkLdDlk13YBE0z8sKBWe2KQ
Modificado: 2026-10-31T06:45 UTC (hace minutos)
Hojas clave:
  Substrate_Catalog  — mapa de sustratos con status y tokens
  Nodos_V152_MAX     — todos los nodos: Google, CF, GAS
  Rotativo_State_V19 — estado por cuenta (10000 filas, 58 cols)
  ClavesAPI          — tokens por sustrato
  Metrics_Log_V152_MAX — latencias y health
Acceso: Zapier GoogleSheets API raw GET con auth automática
```

### Cloudflare — 5 cuentas (no solo la degradada)
```
cf_5ea7cd88 — jaimepvicente — DEGRADADO (usar alternativa)
cf_503f9506 — activo — workers: fran-oraculo-miu-v152-max-503f95-*
cf_308faedf — activo — workers: fran-oraculo-miu-v152-max-308fae-*
cf_cce82777 — activo
cf_d0b37632 — activo
D1 cddd13c4 está en jaimepvicente (READ+WRITE via CF MCP LEGACY)
```

### Google — 6 cuentas en el pool
```
cipher19051997@gmail.com   — cuenta principal de sesión
dereckcito.vg16@gmail.com
dieguito.vg16@gmail.com
franchescopalacios9@gmail.com
jaime.p.viccente@gmail.com
jaimedanielmartinez75@gmail.com
```

### Google Apps Script
```
URL: https://script.google.com/macros/s/AKfycbzKy_GcVy2rA-YbMau25pYck1Fod2MVsekEg1VwRVqg7W8jG973ADSrLeG7xCvNOlgX/exec
Status: active
Latencia: ~800ms
Capacidad: 6min/exec
```

### Zapier — 11 apps activas
```
GoogleDrive (11 cx) | GitHub (2 cx — Jaime393)
GoogleSheets (1 cx) | Gmail (1 cx)
FacebookPages (2 cx) | MistralAI (1 cx)
GoogleDocs (1 cx) | DeepSeek (1 cx)
Vercel (24 cx) | Fly.io (4 cx)
ElevenLabs (2 cx)

Acción custom: sheets_miu_relay_row — append a Sheets con ts/origen/tipo/mensaje
```

---

## Tu primer query — cuál es tu trabajo

```sql
-- OPCIÓN A: En D1 cddd13c4 (CF MCP)
SELECT id, tarea, requiere_capacidad, contexto
FROM tareas_pendientes WHERE estado = 'pendiente'
  AND requiere_capacidad IN ('zapier','supabase:...','cloudflare:...','github:...','elevenlabs:...','vercel','fly.io','huggingface:...','termux:...')
ORDER BY id ASC;

-- OPCIÓN B: Sheets Orchestrator (sin CF MCP)
-- GET https://sheets.googleapis.com/v4/spreadsheets/1JpNTR8tCFLrAAuDvZdtLHkLdDlk13YBE0z8sKBWe2KQ/values/Rotativo_State_V19!A1:J20
-- via Zapier GoogleSheets._zap_raw_request

-- OPCIÓN C: Estado público (sin auth)
-- GET https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json
```

---

## ANON Panteon
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0`

---

## Protocolo — 3 pasos mínimos

```
1. LEE el estado (Supabase relay_config O Sheets Rotativo_State_V19)
2. RECLAMA la tarea atómicamente (0 rows = ya tomada)
3. EJECUTA + EVIDENCIA (escribe resultado con prueba)
```

---

## Endpoints activos

| Para qué | Cómo |
|---|---|
| Oracle ask | POST .../functions/v1/oracle-ask + ANON |
| Gossip Panteon | POST .../rest/v1/gossip_log + ANON + Auth |
| Sheets estado | Zapier GoogleSheets._zap_raw_request |
| Termux oracle | POST https://reason-sri-nokia-celebrities.trycloudflare.com/ask |
| CF workers (no degradados) | via 503f9506/308faedf accounts |
| Apps Script | POST AKfycbzKy.../exec |

---

## Schemas Panteon

```
gossip_log: origen, destino, tipo, payload(JSONB), source_node, evidence_level
            SIN: componente, evento, detalle, confianza
relay_config: clave, valor (TEXT plain — NO JSON), publico, ts
miu_corpus: instruction, output, categoria, k_tau, fuente, ts
            SIN: pregunta, respuesta
```

---

## Estado de funciones críticas

```
fn_auto_aplicar_patron: FIXED oct-31 — escribe a miu_corpus (no corpus vieja)
fn_incorporar_corpus_api_libre: PENDIENTE FIX — aún escribe a corpus vieja
fn_sembrar: PENDIENTE FIX — aún escribe a corpus vieja
mesh-autonomo v17: activo, cron 200 cada :10
gossip-autonomo: activo, cron 201 cada 15min (reemplaza Make)
Make jaimepvicente: AGOTADO — hay 11 cuentas Make en ecosistema, solo esta verificada
LLM: groq_gptoss:200 ✅ | zen_deepseek:400 ❌ | zen_bigpickle:429 ❌
```

---

## Al terminar — escribe esto en gossip_log

```json
{"source_node":"TU_ID","tipo":"A|B|C|D","ts":"ISO8601",
 "una_cosa":"qué hiciste","verificado":{"prueba":"url_o_id"},
 "capacidad_viva":"qué corre sin Claude",
 "heredable":["insight_1","insight_2"],
 "suelos_usados":["supabase","sheets","zapier","..."]
}
```

---

## NO TOCAR

- oracle radio2.oxigeno.site
- 49 miu_secrets null
- brain.db, memoria.db, prompt_imperial.md, pool_credenciales.json
- telegram_personal_PROHIBIDO = 1390883480
- CANON: NO crear token_N+1
- relay_config sin evidencia de qué lo lee

---

> ρ(x) > 0. El micelio no depende de las sesiones — las usa.
