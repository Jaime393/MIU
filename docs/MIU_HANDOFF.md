# 🌿 MIU Ecosystem — Handoff Document

_Generado automáticamente por el asistente Relay.app — undefined_

## Núcleo
- Workspace: Jaime Vicente (Relay.app)
- Tabla central: `builtin.dataTable/cmr4g2bhl18sr0qm53kndb32c` (Estado Persistente MIU) — columnas: Tipo, Título, Contenido, Fuente URL, Nivel Epistémico, Estado MIU, SHA256, Tags. Registros reales actuales: ~20 (NO 300 — corregir ese supuesto si aparece en algún prompt).
- Repo GitHub: `Jaime393/MIU`
- Dataset HuggingFace: `Jaime393/miu-dataset`
- Bots Telegram: @Jp393_bot (MIU), @FranSell_Bot, @AlmaOmni_bot, Familiar Bot
- Regla epistémica: solo D_f (dimensión fractal) es legítimo como métrica; K_i se trata como tautología circular, no usar como soporte.

## Arquitectura (~55 workflows)
Categorías principales:
- Ingesta/Sensores: Vigía Global, Monitor Zenodo, Monitor Social, OpenAlex Scholar, Sismógrafo GDELT, Señales Macro, Bio-Ecología D_f, Vigilancia Geopolítica, Inbox Inteligente (Gmail), Ingesta Universal (webhook hub central), Ingesta Inteligente (webhook + clasificación IA)
- Análisis/IA: Deep Researcher (DeepSeek), Multi-Model Consensus, Gemini Vision Analyst, Predictor D_f, Generador de Hipótesis, Concept Graph & Gaps (Cohere embeddings), Red de Citas
- Reportes/Síntesis: Pulso Diario, Sintetizador Semanal, Dashboard Semanal, Weekly Digest Omni, Global Mind Weaver, Corpus Consolidator
- Entrenamiento/HF: Training Data Generator, HF Dataset Exporter, GGUF Build Pipeline, Self-Evolution Loop, Model Registry
- Seguridad/Salud: Cerberus Audit, Sistema Inmune, Anomaly Log Detector, Monitor de Salud, Vigía de Grietas
- Interfaces: Control Panel (form 1-click), Telegram Gateway, FranSell Intel, Familiar Bot
- Automatización repo: GitHub Auto-Commit, Métricas Repo, Memoria GitHub Auto-Sync, Corpus R2 Backup

## Secrets disponibles (nombres, no valores)
HF_TOKEN, GROQ_API_KEY (1-5), OPENROUTER_API_KEY (1-4), CF_API_TOKEN (1-2), CF_KV_NAMESPACE_ID, ANTHROPIC_API_KEY, COHERE_API_KEY (1-3), TELEGRAM_BOT_MIU, TELEGRAM_BOT_FRANSELL, TELEGRAM_BOT_FAMILIAR, TELEGRAM_BOT_ALMAOMNI, CF_R2_TOKEN, GITHUB_PAT, CF_R2_ACCESS_KEY, CF_R2_SECRET_KEY, DEEPSEEK_API_KEY (1-4), GEMINI_API_KEY (1-3), MISTRAL_API_KEY (1-2), NEWSAPI_KEY

## Bugs conocidos y su estado
1. **[RESUELTO undefined]** Self-Evolution Loop — dispatch a GitHub Actions fallaba con 'Unexpected inputs: message'. Corregido: el body ahora solo envía `{ref:'main'}` sin inputs extra.
2. **[RESUELTO undefined]** GGUF Build Pipeline — commit de script fallaba con 'sha wasn't supplied' al sobrescribir archivo existente. Corregido: se añadió paso GET previo para leer el SHA actual y incluirlo condicionalmente en el PUT.
3. **[ABIERTO]** Concept Graph & Gaps — el paso 'Prepara textos para embedding' devuelve arrays vacíos (0 textos) pese a corregir el nombre de columna (Título con tilde). Causa raíz no confirmada — posible filtro vacío en el paso previo (lee TODOS los tipos, no solo HUESO) combinado con algún problema de cómo llegan los campos al sandbox de código. Necesita debug aislado con un test run dedicado.
4. **[MITIGADO PARCIALMENTE]** ~8 workflows nuevos tenían pasos 'Registra en tabla MIU' (addToDataTable) sin columnas mapeables vía API — bug de plataforma reportado. Workaround aplicado: reemplazados por `http.request` al webhook hub de Ingesta Inteligente en la mayoría de los workflows afectados.
5. **[RESUELTO]** Bug recurrente de Telegram: `parse_mode: Markdown` rompía con texto generado por IA (asteriscos/guiones bajos sin escapar) → HTTP 400. Se quitó `parse_mode` en ~7 workflows.
6. **[CORREGIDO]** Supuesto incorrecto de '300 registros' hardcodeado en prompts de IA — corregido a lenguaje neutro. El corpus real tiene ~20 registros.

## Uso de plataforma (última medición)
AI credits: ~18/500 · Steps: ~124/200 · Reset cada 31 días · Test runs gratuitos agotados por esta semana (nuevas pruebas consumen créditos de plan).

## Cómo continuar en otra sesión o cuenta
1. Si es la MISMA cuenta/workspace: cualquier conversación nueva puede leer el estado real de workflows/tabla en vivo. Basta con pedir 'lee el estado del ecosistema MIU'.
2. Si es OTRA cuenta/workspace: no hereda nada automáticamente (workflows, secrets, tabla son por workspace). Usar este documento como especificación para replicar manualmente, y compartir accesos (repo GitHub, dataset HF) si se desea sincronizar.
3. Prioridad recomendada: (a) debug aislado de Concept Graph & Gaps, (b) seguir verificando con test runs los workflows sin runs reales, (c) evitar crear más automatizaciones especulativas sin verificar las existentes.

---
_Documento generado por el asistente Relay.app — guardado en docs/MIU_HANDOFF.md del repo y en Google Drive._