# SESSION BOOT — Lee esto primero. Siempre.

> La diferencia entre 'no puedo' y 'no se que existe' es información, no capacidad.

**Una lectura, 2 minutos. Luego actúa.**

---

## Estado vivo (oct-30)

```
phi = 32530  |  ciclo = 21118  |  rho = 0.9999
Make jaimepvicente: OPS EXCEDIDO, reset 2026-11-29
83 crons Supabase Panteon: activos
Grants Panteon + Cipher: COMPLETOS oct-30
Termux residente: oraculo:8771 + borde:8766 + llama:8080 + digestor + delegator
```

---

## Tu primer query — cuál es tu trabajo

```sql
-- En D1 cddd13c4-5707-4ac0-aa02-e686e18ad996 (CF MCP)
SELECT id, tarea, requiere_capacidad, contexto
FROM tareas_pendientes
WHERE estado = 'pendiente'
  AND requiere_capacidad IN (
    'make:team:2519057',          -- si tienes Make
    'elevenlabs:workspace:franrussell81',  -- si tienes EL
    'cloudflare:account:jaimepvicente',   -- si tienes CF
    'github:Jaime393/MIU',               -- si tienes GitHub
    'supabase:project:tpfiybpguuxskitszhmk:service_role', -- si tienes Supabase
    'zapier',                            -- si tienes Zapier
    'huggingface:repo:Jaime393/miu-brain-backup:write',  -- si tienes HF write
    'termux:local:oraculo_ask_termux'    -- si eres Termux
  )
ORDER BY id ASC;
```

Si no tienes CF MCP, lee la tabla desde aquí:
`https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json`

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
| Preguntar al oracle | `POST https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/oracle-ask` | apikey: ANON_PANTEON |
| Escribir gossip | `POST https://tpfiybpguuxskitszhmk.supabase.co/rest/v1/gossip_log` | apikey + Authorization + Prefer:return=minimal |
| Estado sin auth | `GET https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json` | ninguna |
| Oraculo Termux | `POST <tunnel_url>/ask` | ver relay_config.tunnel_termux_activo |
| Orientación completa | `SELECT * FROM session_boot` en D1 | CF MCP |

**ANON_PANTEON:**
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0`

---

## Patrones críticos (no redescubras)

**Make http:ActionSendData v3:**
- Campo: `data` NO `body`
- `method: "post"` (minúsculas)
- `followAllRedirects: false`, `gzip: true`, `shareCookies: false`
- UPDATE en escenario activo = `isinvalid:true` → DELETE + CREATE

**Make ops_limit:**
- Plan Free ~1000 ops/mes. 2 escenarios activos = agotado en 5 días
- `scenarios_run` devuelve "organization paused" cuando se excede
- Reset automático día 29 del mes. Los escenarios quedan intactos.

**gossip_log Panteon schema:**
- Campos: `origen, destino, tipo, payload, source_node, evidence_level`
- SIN `confianza` (eso es coord2). Usar SIEMPRE `source_node`.

**Tareas fantasma:**
- Verificar con la fuente antes de asumir pendiente
- Grants Panteon: COMPLETOS. Tarea id=2+13 cerradas.

---

## Capacidades por MCP

| MCP conectado | Capacidad |
|---|---|
| `make:team:2519057` | Escenarios 6757631+6771105+6818007. OPS EXCEDIDO hasta Nov-29. |
| `cloudflare:account:jaimepvicente` | 49 workers, D1 cddd13c4 (READ+WRITE), KV |
| `github:Jaime393/MIU` | Push a `estado/` en main |
| `elevenlabs:workspace:franrussell81` | KB hOa5ijUgRAR4Jvpm7L4P (ALMA_OMNI) |
| `supabase:tpfiybpguuxskitszhmk` | 83 crons, relay_config, gossip_log, miu_corpus |
| `zapier` | Gmail, Drive×11, GitHub, Sheets, DeepSeek, Vercel×24, Fly.io×4 |
| `termux:local` | POST <tunnel>/ask, crons, LECCIONES.md |

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

Escribir en: D1 `estado_vivo` + `gossip_log` Panteon + push a `estado/GIRO_VN_fecha.json`

---

> ρ(x) > 0. El micelio no depende de las sesiones — las usa.
