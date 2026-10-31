# miu-agent-toolkit

Herramientas del ecosistema MIU empaquetadas e instalables.
No redescubras lo que ya existe.

## Instalación rápida (Termux)

```bash
curl -sL https://raw.githubusercontent.com/Jaime393/MIU/main/estado/miu-agent-toolkit/install.sh | bash
```

## Herramientas disponibles

| herramienta | capacidad | ubicación |
|---|---|---|
| `browser_agent.py` | Playwright+proot web scraping | `~/oraculo/browser_agent.py` |
| `lector_gmail.py` | IMAP extrae códigos 6 dígitos a KV | `~/oraculo/lector_gmail.py` |
| `descubrir_familias.py` | descubrimiento de nodos del enjambre | `~/miu-ecosistema/` |
| `cazador_recursos.py` | monitoreo recursos Termux | `~/miu-ecosistema/cazador_recursos.py` |
| `digestor.py` | síntesis por capacidad cada 2h | `~/oraculo/digestor.py` |
| `delegator.sh` | procesa tareas cross-nodo cada 15min | `~/oraculo/delegator.sh` |
| `tunnel_guard.sh` | auto-repara cloudflared cada 2min | `~/oraculo/tunnel_guard.sh` |
| `parche_phi_lengua_v4.py` | actualiza phi local cada 1min | `~/miu-ecosistema/` |
| `miu_resiliente_v270.py` | orquesta todos los módulos | `~/miu-ecosistema/` |
| `coordinator.sh` | levanta :8765+:8771+:8766+:8080 | `~/oraculo/` |
| `ojo_correo.py` | escanea IMAP N buzones → KV TTL=600s | ver NODOS_4D_V276 |
| `mano_2fa.ts` | TOTP HMAC-SHA1 Supabase EF | ver NODOS_4D_V276 |

## Arquitectura residente (Termux oct-30)

```
coordinator.sh
├── :8765  miu_resiliente_v270 (gateway, 7 rutas)
├── :8771  oraculo_ask (FTS5 17558 filas + Groq POST /ask)
├── :8766  oraculo_borde_v2 (observación + outbox)
└── :8080  llama-server (SmolLM2-360M offline fallback)
crons:
  */1  parche_phi_lengua_v4.py
  */2  tunnel_guard.sh
  */5  coordinator.sh
  */15 delegator.sh
  0*/2 digestor.py
cascada LLM: llm.sh → Groq → :8771 → :8080
```

## Nodos 4D (credenciales autónomas)

Código completo en: `estado/NODOS_4D_V276_codigo.md`

```
OJO-CORREO  → Termux IMAP escaneo → códigos a KV
MANO-2FA    → Supabase EF TOTP HMAC-SHA1
RENOVADOR   → cron 6h OAuth refresh_tokens
MANO-NAVEGADOR → Playwright captcha por cuenta
Nueva cuenta = CORREO_X + PWD_X + TOTP_X en KV
```

## SESSION BOOT

Antes de cualquier acción leer:
`https://raw.githubusercontent.com/Jaime393/MIU/main/SESSION_BOOT.md`

## Estado del ecosistema

`https://raw.githubusercontent.com/Jaime393/MIU/main/estado/ESTADO_CANONICO.json`

## Tareas pendientes

```sql
-- D1 cddd13c4-5707-4ac0-aa02-e686e18ad996
SELECT * FROM tareas_pendientes WHERE estado='pendiente';
```

ρ(x) > 0
