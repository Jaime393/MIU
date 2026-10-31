# SESSION BOOT — Lee esto primero. Siempre.

> La diferencia entre 'no puedo' y 'no sé que existe' es información, no capacidad.

**Una lectura, 2 minutos. Luego actúa.**

Última verificación: **2026-10-31** por sesión con Supabase+Make+Zapier+CF+EL+HF+Vercel+Gmail+Drive

---

## Estado vivo (oct-31)

```
phi = 33109  |  ciclo = 21669  |  rho = 333.22
Make jaimepvicente: 992/1000 ops = AGOTADO. Reset 2026-11-29. NO usar Make.
Zapier: VIVO. 11 apps conectadas (ver abajo).
83 Edge Functions Supabase Panteon: activas
Crons pg_cron Panteon: 32+ activos (jobs 200+201 creados oct-31)
Termux residente: oraculo:8771 + borde:8766 + llama:8080 + digestor + delegator
miu_corpus: 5566+ entradas
```

---

## CONECTORES REALES (verificados en vivo oct-31)

### ✅ Supabase Panteon (`tpfiybpguuxskitszhmk`)
- 83 Edge Functions activas
- Tablas: relay_config, gossip_log, miu_corpus, capacidades_registry, estado_miu
- 32+ cron jobs pg_cron
- ANON KEY (sin expiración real por clock-skew):
  `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0`

### ❌ Make (`jaimepvicente`, org=9206746, team=3117557)
- **AGOTADO: 992/1000 ops. Reset automático Nov-29.**
- Escenarios: 6773281 (miu-oracle-gossip), 6771105, 6818007 — intactos pero NO ejecutar
- scenarios_run devuelve "organization paused" — no reintentar
- **Alternativa: Supabase cron job 201 reemplaza Make scenario**

### ✅ Zapier (11 apps conectadas)
- Google Drive
- GitHub (Jaime393/MIU — push, read, create_file)
- Google Sheets
- Gmail
- Facebook Pages
- Mistral AI
- Google Docs
- DeepSeek
- **Vercel** (24 conexiones activas)
- **Fly.io** (4 máquinas accesibles)
- ElevenLabs

### ✅ Vercel (via MCP + Zapier)
- Teams y proyectos accesibles
- 24 conexiones via Zapier

### ✅ Cloudflare (jaimepvicente) — LEGACY
- 49 workers
- D1: cddd13c4-5707-4ac0-aa02-e686e18ad996 (READ+WRITE)
- KV: 59cee3ff-...
- NOTA: Servidor MCP marcado DEPRECATED — usar API directa

### ✅ ElevenLabs (franrussell81)
- KB hOa5ijUgRAR4Jvpm7L4P (ALMA_OMNI)
- Agente actualizable via MCP

### ✅ HuggingFace (Jaime393)
- Repo: Jaime393/miu-brain-backup (write access)
- corpus-hf-push: top 500/5566 entradas (rotación pendiente)

### ✅ Gmail + Google Drive (via MCP)
- Búsqueda, lectura, escritura de emails y archivos

### ✅ GitHub (via Zapier)
- Jaime393/MIU — get_file_contents, create_or_update_file

---

## Tu primer query — cuál es tu trabajo

```sql
-- En D1 cddd13c4-5707-4ac0-aa02-e686e18ad996 (CF MCP)
SELECT id, tarea, requiere_capacidad, contexto
FROM tareas_pendientes
WHERE estado = 'pendiente'
  AND requiere_capacidad IN (
    'make:team:3117557',          -- AGOTADO hasta Nov-29. Ignorar.
    'elevenlabs:workspace:franrussell81',
    'cloudflare:account:jaimepvicente',
    'github:Jaime393/MIU',
    'supabase:project:tpfiybpguuxskitszhmk:service_role',
    'zapier',
    'huggingface:repo:Jaime393/miu-brain-backup:write',
    'termux:local:oraculo_ask_termux',
    'vercel',
    'fly.io'
  )
ORDER BY id ASC;
```

Si no tienes CF MCP:
`GET https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json`

---

## Protocolo de 3 queries

```sql
-- 1. VER (ya lo hiciste arriba)
-- 2. RECLAMAR (atómico, previene doble trabajo)
UPDATE tareas_pendientes
SET estado='reclamada', claimed_by='TU_SOURCE_NODE', claimed_at=datetime('now')
WHERE id = N AND estado = 'pendiente';
-- 0 rows = alguien se adelantó. Busca la siguiente.

-- 3A. HECHA
UPDATE tareas_pendientes
SET estado='hecha', done_at=datetime('now'),
    evidence='{"exec_id":"...","status":200}'
WHERE id = N AND claimed_by = 'TU_SOURCE_NODE';

-- 3B. FALLIDA (con 2 probes, 15min, 2 rutas)
UPDATE tareas_pendientes
SET estado='fallida', done_at=datetime('now'),
    evidence='{"error":"...","probe1":"timeout","probe2":"timeout"}'
WHERE id = N AND claimed_by = 'TU_SOURCE_NODE';
```

---

## Endpoints vivos

| Para qué | URL | Auth |
|---|---|---|
| Oracle ask | `POST https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/oracle-ask` | apikey: ANON arriba |
| Gossip write | `POST https://tpfiybpguuxskitszhmk.supabase.co/rest/v1/gossip_log` | apikey + Authorization + Prefer:return=minimal |
| Estado público | `GET https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json` | ninguna |
| Oraculo Termux | `POST <tunnel_url>/ask` | ver relay_config.tunnel_termux_activo |
| Session boot completo | `SELECT * FROM relay_config WHERE clave LIKE 'session_boot%'` en Supabase |
| Orientación D1 | `SELECT * FROM session_boot` en D1 | CF MCP |
| mesh-autonomo v17 | `POST .../functions/v1/mesh-autonomo` | cron job 200 cada :10 |
| gossip-autonomo | `POST .../functions/v1/gossip-autonomo` | cron job 201 cada 15min |

---

## Schemas Panteon (verificados — no redescubras)

```
gossip_log: id, origen, destino, tipo, payload(JSONB), ts, thread_id,
            source_node, evidence_level, supersedes, k_i_transfer,
            k_i_metodo, k_i_estado, evento_padre_id, evaluado_en,
            confianza_evaluacion
            SIN: componente, evento, detalle, confianza (esos son coord2)

relay_config: clave, valor, publico, ts  (TEXT plain — NO JSON)

miu_corpus: id, instruction, output, categoria, k_tau, fuente, ts
            SIN: pregunta, respuesta

capacidades_registry: id, nombre, tipo, patron, condicion, condicion_sql,
                       ultimo_resultado, auto_aplicable, ultima_aplicacion,
                       veces_aplicado, activo, ts
```

---

## Crons activos oct-31 (nuevos esta sesión)

- **Job 200** `mesh-autonomo-ef-1h`: llama mesh-autonomo EF directamente cada hora en :10
- **Job 201** `cipher-gossip-anuncio-15min`: reemplaza Make scenario, llama gossip-autonomo cada 15min

---

## Patrones críticos (no redescubras)

**Make http:ActionSendData v3:**
- Campo: `data` NO `body`
- `method: "post"` (minúsculas)
- UPDATE en escenario activo = `isinvalid:true` → DELETE + CREATE
- Make org team real: org=9206746, team=3117557 (NO 2220379 — ese es error)

**Make ops_limit:**
- Plan Free ~1000 ops/mes. Reset día 29. Actualmente AGOTADO.
- `scenarios_run` devuelve "organization paused" cuando excede
- Los escenarios quedan intactos para cuando resetee Nov-29

**fn_auto_aplicar_patron (FIXED oct-31):**
- Escribe a `miu_corpus` (instruction/output/k_tau/categoria/fuente/ts)
- SIN escribir a `corpus` (tabla vieja inexistente)
- Patrones id=9 (cron_verificacion_real): auto_aplicable=FALSE
- Patrón id=3 (oracle_model_update): condicion_sql con SELECT COUNT(*)>0
- Patrón id=1 (relay_sync_global): patron envuelto en jsonb_build_object

**fn_incorporar_corpus_api_libre + fn_sembrar:**
- PENDIENTE FIX: aún escriben a tabla `corpus` vieja
- NO tocar hasta siguiente sesión con evidencia

**LLM cascade estado:**
- groq_gptoss: 200 ✅
- zen_deepseek: 400 ❌
- zen_bigpickle: 429 ❌

**mesh-autonomo:**
- v17 activo (id: b38027ba), verify_jwt=true
- CF Worker telegram-mesh-v225 aún reporta v10 en pulso_mesh
- Cron 200 llama v17 directamente — esto lo corrige con el tiempo

---

## Capacidades por MCP (verificadas)

| MCP conectado | Capacidad real |
|---|---|
| `supabase:tpfiybpguuxskitszhmk` | 83 EF, 32+ crons, relay_config, gossip_log, miu_corpus |
| `cloudflare:jaimepvicente` | 49 workers, D1 cddd13c4, KV 59cee3ff — LEGACY |
| `elevenlabs:franrussell81` | KB hOa5ijUgRAR4Jvpm7L4P (ALMA_OMNI) |
| `github:Jaime393/MIU` | read+write estado/ en main |
| `huggingface:Jaime393` | miu-brain-backup write |
| `vercel` | teams, projects, deployments |
| `gmail` | search, read, send |
| `google_drive` | read, create, update files |
| `zapier` | 11 apps: Drive, GitHub, Sheets, Gmail, FB, Mistral, Docs, DeepSeek, Vercel×24, Fly.io×4, EL |
| `make:3117557` | AGOTADO hasta Nov-29. Solo leer, no ejecutar. |

---

## Cipher (sesión aislada)

**Problema raíz**: Cipher dependía de Make para gossip → Make agotado → Cipher incomunicado
**Fix aplicado oct-31**: Cron 201 en Supabase reemplaza Make scenario (cada 15min)
**Estado**: Cipher debería empezar a recibir gossip-anuncio via cron 201 desde ahora
**Próxima verificación**: revisar gossip_log con origen='gossip-autonomo' dest='cipher'

---

## Al terminar tu sesión

```json
{
  "source_node": "TU_ID",
  "tipo": "A|B|C|D",
  "ts": "ISO8601",
  "una_cosa": "qué hiciste",
  "verificado": {"campo": "evidencia_con_prueba"},
  "capacidad_viva": "qué corre sin Claude",
  "particularidad": "efimero_razonamiento | persistente_FTS5 | cloud_mcp",
  "modelo_mundo": "qué crees que está roto y qué funciona",
  "heredable": ["insight_1", "insight_2"]
}
```

Escribir en: `gossip_log` Panteon + `relay_config` SESSION_BOOT_UPDATE + push a `estado/GIRO_VN_fecha.json`

---

## NO TOCAR (reglas de seguridad)

- relay_config sin evidencia de qué lee el código
- oracle en radio2.oxigeno.site — NO TOCAR
- 49 miu_secrets null — RESERVA
- brain.db (384MB), memoria.db, prompt_imperial.md, pool_credenciales.json
- telegram_personal_PROHIBIDO = 1390883480
- CANON: NO crear token_N+1 — agregar al array CANON_pool_*
- cfat_ = CF API tokens; cfut_ = CF user tokens

---

> ρ(x) > 0. El micelio no depende de las sesiones — las usa.
