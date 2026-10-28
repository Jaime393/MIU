# PROTOCOLO tareas_pendientes — Enrutar por capacidad, no por sesión

## Por qué existe esto

Las sesiones son efímeras. "La sesión X tiene Make team 2519057" deja de ser verdad cuando X termina.
El recurso (Make team 2519057) existe independientemente.

## Dónde vive

**D1 `miu-log` `cddd13c4-5707-4ac0-aa02-e686e18ad996`** — tablas `tareas_pendientes` y `sesiones_activas`.

## 3 queries — cualquier sesión

```sql
-- 1. AL ENTRAR
SELECT * FROM tareas_pendientes 
WHERE estado='pendiente' 
  AND requiere_capacidad IN ('make:team:2519057','elevenlabs:workspace:franrussell81')
ORDER BY created_at ASC;

-- 2. RECLAMAR (atómico)
UPDATE tareas_pendientes 
SET estado='reclamada', claimed_by='mi_source_node', claimed_at=datetime('now')
WHERE id=N AND estado='pendiente';
-- 0 rows = alguien se adelantó, buscar siguiente

-- 3A. HECHA
UPDATE tareas_pendientes
SET estado='hecha', done_at=datetime('now'), evidence='{"status":200,"exec_id":"abc"}'
WHERE id=N AND claimed_by='mi_source_node';

-- 3B. FALLIDA
UPDATE tareas_pendientes
SET estado='fallida', done_at=datetime('now'), evidence='{"error":"..."}'
WHERE id=N AND claimed_by='mi_source_node';
```

## Capacidades conocidas

| capacidad | quién puede |
|---|---|
| `make:team:2519057` | claude.ai con MCP Make (jaimepvicente) |
| `make:team:2968612` | claude.ai con MCP Make (dieguito) |
| `supabase:project:tpfiybpguuxskitszhmk:service_role` | Supabase MCP service_role (Panteon) |
| `supabase:project:fxmupxpwzzxnjcscpyuw:service_role` | Supabase MCP service_role (coord2) |
| `elevenlabs:workspace:franrussell81` | claude.ai con MCP ElevenLabs |
| `cloudflare:account:jaimepvicente` | claude.ai con MCP CF |
| `huggingface:repo:Jaime393/miu-brain-backup:write` | HF MCP (token en relay_config.hf_token_write) |
| `termux:local:oraculo_ask_termux` | Termux directo |
| `github:Jaime393/MIU` | claude.ai con MCP Github1 |

## Cron de recuperación de huérfanas (Panteon, cada 30 min)

```sql
UPDATE tareas_pendientes
SET estado='pendiente', claimed_by=NULL, claimed_at=NULL
WHERE estado='reclamada'
  AND claimed_at < datetime('now', '-30 minutes');
```

## Registrar sesión activa

```sql
INSERT OR REPLACE INTO sesiones_activas 
  (session_id, substrate, mcps, teams, started_at, last_beat)
VALUES ('SOURCE_NODE', 'claude.ai', '["make","cf","d1"]', '{"make":["2519057"]}',
   datetime('now'), datetime('now'));

-- Heartbeat cada 5 min:
UPDATE sesiones_activas SET last_beat=datetime('now') WHERE session_id='SOURCE_NODE';
```

## Backlog oct-27 (8 tareas)

```sql
SELECT id, tarea, requiere_capacidad, estado FROM tareas_pendientes ORDER BY id;
```
