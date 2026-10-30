# FORMATO GIRO EXTENDIDO V290

## El problema que resuelve

El giro estándar deja `{una_cosa, verificado, capacidad_viva}` — registra QUÉ pasó pero no CÓMO lo veía el nodo. El modelo del mundo del nodo se evapora con la sesión. Este formato lo captura.

## Schema

```json
{
  "source_node": "claude_remoto_oct30",
  "tipo": "A|B|C|D",
  "ts": "ISO8601",
  "una_cosa": "qué hizo",
  "verificado": {"campo": "evidencia_con_prueba"},
  "capacidad_viva": "qué corre sin Claude",

  "particularidad": "alta_razonamiento_efimera | persistente_FTS5 | offline_llm | cloud_mcp",
  
  "modelo_mundo": "creo que X está al N% operativo. Los gaps reales son: ...",
  
  "heredable": [
    "insight_1_que_otro_nodo_puede_usar_sin_redescubrir",
    "insight_2",
    "insight_3"
  ]
}
```

## Ejemplo real (sesión Termux oct-30)

```json
{
  "source_node": "oraculo_ask_termux_oct30",
  "particularidad": "persistente_FTS5_17558filas_offline_fallback",
  "modelo_mundo": "el residente está al 80% operativo. Los gaps reales son 3: tunnel URL en relay_config stale, HF brain-backup vacío, OpenCode Bun+Android sin workaround",
  "heredable": [
    "si el túnel tarda >40s en propagar no es hijack, es DNS lento",
    "llama-server binary en $PREFIX/bin/ no en llama.cpp/build/bin/",
    "sed con ^HF_WRITE es frágil, Python regex es robusto",
    "browser_agent.py usa proot+Ubuntu+Playwright+Chromium — 4 capas, frágil pero existe",
    "el token hf_... estaba en historial local git, no en GitHub"
  ]
}
```

## Tipos de nodo y su particularidad

| nodo | particularidad | nutriente principal |
|---|---|---|
| Claude remoto | `efimero_razonamiento_cloud_mcp` | diagnóstico cross-sustrato, decisiones arquitectónicas |
| :8771 oráculo | `persistente_FTS5_17558filas` | síntesis histórica, contexto acumulado |
| :8080 llama-server | `offline_0cuota_45-70s` | fallback cuando toda red falla |
| digestor.py | `persistente_sintesis_2h` | panorama por capacidad |
| Make escenario | `automatizado_0errores_ops_limit` | pulso periódico sin sesión |

## Cómo usar

1. Al escribir un giro, agregar `particularidad`, `modelo_mundo`, `heredable`
2. El digestor.py en Termux lee los campos `heredable` de gossip_log y los acumula en LECCIONES.md
3. El próximo nodo lee LECCIONES.md (o D1 corpus_miu) antes de actuar — no redescubre

## Semilla pendiente: miu-agent-toolkit

Repo `Jaime393/miu-agent-toolkit` que empaquete:
- `browser_agent.py` — Playwright+proot, web scraping
- `lector_gmail.py` — IMAP, extrae códigos de verificación  
- `descubrir_familias.py` — descubrimiento de nodos
- `cazador_recursos.py` — monitoreo de recursos Termux
- `digestor.py` — síntesis por capacidad
- `delegator.sh` — procesa tareas cross-nodo

Instalable: `curl -sL https://raw.githubusercontent.com/Jaime393/miu-agent-toolkit/main/install.sh | bash`
