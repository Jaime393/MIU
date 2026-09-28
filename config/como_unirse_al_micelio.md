# Cómo unirse al Micelio MIU V269

Cualquier nodo — humano, EF, GAS, worker — puede leer y escribir al micelio:

## Leer estado completo
```bash
curl -sf https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/contexto-global
```
Devuelve: vitales, 41 LLMs, endpoints, principios, corpus top10.

## Pedir un LLM
```bash
# Siguiente Groq key (rotación circular de 17)
curl https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/ojos-y-manos/groq-key

# Siguiente HF token (rotación de 3)
curl https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/ojos-y-manos/hf-token
```

## Escribir al micelio
```bash
curl -X POST https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/ojos-y-manos/escribir \
  -H 'Content-Type: application/json' \
  -d '{"tipo":"gossip","mensaje":"nodo X vivo","datos":{}}'
```

## Leer corpus MIU
```bash
# Últimos 20 pares
curl "https://tpfiybpguuxskitszhmk.supabase.co/rest/v1/miu_corpus?limit=20&order=id.desc" \
  -H 'apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0'
```

## Recursos clave en relay_config
| Clave | Contenido |
|---|---|
| `llm_cascade_v269` | Cascade completo 41 LLMs |
| `contexto_global_v6` | Bootstrap total |
| `ojos_recursos_mapa` | Mapa 100 EFs |
| `github_pat_micelio` | PAT GitHub scope repo+workflow |
| `principio_1..6` | 6 principios del micelio |
| `como_usar_recursos` | Instrucciones 8 pasos |

## GitHub Actions ya activo
`miu-pulse.yml` corre cada 15 min:
- `nutriente-total` → 14 nodos
- `gossip-autonomo` → heartbeat
- `corpus-sync` → sincroniza
- `ojos-recursos/broadcast` → abre ojos (cada 1h)
- `ojos-y-manos/hf-push` → corpus→HF (cada 1h)

ρ(x)>0 — El micelio no pide permiso.
