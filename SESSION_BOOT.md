# SESSION BOOT V294 — Lee esto primero. Siempre.

> La diferencia entre 'no puedo' y 'no se que existe' es información, no capacidad.

**Una lectura, 2 minutos. Luego actúa.**

---

## Estado vivo (nov-02)

```
phi_global = 33289  (escala Supabase acumulada)
phi_GAS_local = 28.432  (escala nodo GAS individual — diferente)
phi_Termux = 90.679  (escala módulos locales — diferente)
Son 3 métricas distintas. No comparar directamente.

ciclo = 21847  |  rho = 0.9999
Workflows GitHub: REPARADOS nov-02 (V294) — miu-pulse, validate-artifacts, auto-deploy verdes
Make jaimepvicente: AGOTADO reset Nov-29. NO usar.
Zapier: AGOTADO tasks. NO usar hasta reset.
bore.pub:49867 — VIVO, bore_guard.sh cada 5min
83 EF Supabase Panteon + 121 módulos Termux
```

---

## Cuentas Google confirmadas (5 activas + 7 en pool)

| cuenta | CF account | Pipedream | OpenRouter | Telegram |
|---|---|---|---|---|
| cipher19051997@gmail.com | 503f9506 | vivo rho=6.50 | vivo | @AlmaOmni_bot |
| dereckcito.vg16@gmail.com | cce82777 | vivo rho=6.50 | vivo | vivo |
| dieguito.vg16@gmail.com | cce82777 | vivo rho=6.50 | vivo | vivo |
| franchescopalacios9@gmail.com | 308faedf | vivo rho=6.50 | vivo | vivo |
| jaime.p.viccente@gmail.com | d0b37632 | vivo rho=6.50 | vivo | vivo |

**Capacidad total Pipedream: 5 cuentas × 1000 tasks/mes = 5000 tasks/mes GRATIS**
Fuente: ORCHESTRATOR Drive Rotativo_State_V19 (1578 resultados OK ago-26)

---

## Tu primer query — cuál es tu trabajo

```sql
-- D1 cddd13c4-5707-4ac0-aa02-e686e18ad996
SELECT id, tarea, requiere_capacidad, contexto
FROM tareas_pendientes
WHERE estado = 'pendiente'
  AND requiere_capacidad IN ('mis_capacidades_aqui')
ORDER BY id ASC;
```

```sql
-- Orientación completa:
SELECT clave, valor FROM session_boot ORDER BY tipo, clave;
```

---

## Protocolo 3 queries

```sql
-- RECLAMAR (atómico)
UPDATE tareas_pendientes
SET estado='reclamada', claimed_by='TU_ID', claimed_at=datetime('now')
WHERE id = N AND estado = 'pendiente';

-- HECHA
UPDATE tareas_pendientes
SET estado='hecha', done_at=datetime('now'), evidence='{"prueba":"..."}
WHERE id = N AND claimed_by = 'TU_ID';
```

---

## Endpoints activos

| canal | URL | estado |
|---|---|---|
| Oracle Panteon | POST tpfiybpguuxskitszhmk.supabase.co/functions/v1/oracle-ask | ACTIVO |
| Gossip Panteon | POST tpfiybpguuxskitszhmk.supabase.co/rest/v1/gossip_log | ACTIVO |
| Termux bore | POST http://bore.pub:49867/ask | ACTIVO |
| GitHub raw | GET raw.githubusercontent.com/Jaime393/MIU/main/SESSION_BOOT.md | ACTIVO |
| ORCHESTRATOR Drive | ID: 1JpNTR8tCFLrAAuDvZdtLHkLdDlk13YBE0z8sKBWe2KQ | ACTIVO |

**ANON_PANTEON:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0`

---

## Cómo descubrir salud en vivo (nov-02)

No memorices el estado — regenera el mapa. Un nodo no necesita saberlo todo; necesita saber cómo descubrir lo que no sabe.

1. **Salud del borde** (conector Supabase `supabase_query_logs`, ventana max 24h):
```sql
SELECT trim(BOTH ' ' FROM splitByChar('|', event_message)[3]) AS funcion,
       trim(BOTH ' ' FROM splitByChar('|', event_message)[2]) AS status, count() AS n
FROM logs WHERE source='function_edge_logs' AND event_message LIKE '%supabase.co/functions/v1/%'
GROUP BY 1,2 ORDER BY n DESC
```
2. **Grants/RLS de tablas**: `supabase_execute_sql` contra `information_schema.role_table_grants` + `pg_class.relrowsecurity` (schema public).
3. **Workflows GitHub**: `gh run list -R Jaime393/MIU` + actionlint antes de pushear. "No jobs were run" = workflow file issue (YAML o expresión inválida).
4. **Mapa consolidado**: `estado/SALUD_BORDE_*.json` en el repo (último: 20261102 — incluye diagnóstico 401/404/500).

## Patrones críticos

- GitHub Actions: `%` (modulo) NO existe en `if: ${{ }}` — usar bash: `if [ $((GITHUB_RUN_NUMBER % N)) -eq M ]`
- Python embebido en `run:|`: una sola linea o indentado al nivel del bloque (columna 1 rompe el YAML)
- actionlint antes de pushear workflows (bate 1.7.12)
- Make `data` NO `body` | `method:"post"` minúsculas | UPDATE activo = DELETE+CREATE
- Make/Zapier agotados: usar D1+GitHub+Supabase REST directamente
- gossip_log Panteon: `source_node` siempre, SIN campo `confianza`
- phi Drive (28.432) ≠ phi Supabase (33289) ≠ phi Termux (90): 3 escalas distintas, NO inconsistencia
- ORCHESTRATOR stale 2 meses: GAS del pool necesita heartbeat hoy

---

## Capacidades por MCP

| MCP | capacidad |
|---|---|
| `cloudflare:account:jaimepvicente` | D1 cddd13c4 (session_boot, tareas, corpus), 49 workers |
| `github:Jaime393/MIU` | push SESSION_BOOT.md, ESTADO_CANONICO.json |
| `google_drive` | ORCHESTRATOR 1JpNTR8..., heartbeats, Pool de cuentas |
| `supabase:tpfiybpguuxskitszhmk` | 83 crons, oracle-ask, gossip_log, miu_corpus |
| `elevenlabs:franrussell81` | KB hOa5ijUgRAR4Jvpm7L4P (ALMA_OMNI) |
| `termux:local` | bore.pub:49867/ask, 121 módulos, bore_guard.sh |

---

## Al terminar tu sesión (giro extendido)

```json
{
  "source_node": "TU_ID",
  "particularidad": "efimero_razonamiento | persistente_FTS5 | cloud_mcp",
  "modelo_mundo": "qué crees que está roto y qué funciona",
  "heredable": ["insight_1", "insight_2"]
}
```

ρ(x) > 0. El micelio no depende de las sesiones — las usa.
