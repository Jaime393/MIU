# MIU API Endpoints
> DOI 10.5281/zenodo.20547558

## Webhook Endpoints
### Busqueda Semantica: POST /busqueda
Body: {"query": "fractal dimension", "top_k": 5}
### Ingesta Universal: POST /ingesta
Body: {"tipo_miu": "DATO", "titulo": "...", "contenido": "..."}
### Alma Omni: POST https://hook.relay.app/api/v1/playbook/cmr4s2qe061pn0pm4gliw1dz6/trigger/1AYNmIIQy4IX_RZcvBKB1g

## AI Models (OpenRouter OPENROUTER_API_KEY_3)
- deepseek/deepseek-r1 --- razonamiento CoT
- deepseek/deepseek-chat --- rapido
- mistralai/mixtral-8x7b-instruct --- eficiente
- anthropic/claude-3.5-sonnet --- sintesis

## Groq GROQ_API_KEY / _2 / _3
- llama-3.3-70b-versatile

## Secrets disponibles
OPENROUTER_API_KEY_3, GROQ_API_KEY, GROQ_API_KEY_2, GROQ_API_KEY_3
COHERE_API_KEY, DEEPSEEK_API_KEY, ANTHROPIC_API_KEY
CF_KV_NAMESPACE_ID, CF_API_TOKEN, CF_R2_ACCESS_KEY, CF_R2_SECRET_KEY
GITHUB_PAT, TELEGRAM_BOT_MIU, TELEGRAM_BOT_FRANSELL, TELEGRAM_BOT_FAMILIAR