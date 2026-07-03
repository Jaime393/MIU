# 🌿 MIU — Blueprint de Construcción (Portable)

_Documento masticado para reconstruir el ecosistema MIU en OTRA cuenta/workspace de Relay.app desde cero, sin necesidad de leer cada workflow original. Generado por el asistente Relay.app.

## ⚠️ Límite técnico real
Los workspaces de Relay.app son islas: workflows, conexiones y secrets NO se heredan ni se comparten entre cuentas. Esta guía es para RECREAR manualmente los workflows más valiosos en la cuenta nueva — no es una migración automática.

## 0. Qué preparar antes de construir
1. Conectar integraciones: Google Drive, Gmail, GitHub (nuevo PAT o el mismo repo si compartes acceso), y opcionalmente Google Sheets.
2. Crear estos workspace secrets (nombre → qué va adentro, valores están en Drive: `claves.txt` y el zip `claves antiguas`):
   - `COHERE_API_KEY` — Cohere embeddings/rerank
   - `GEMINI_API_KEY` — Google Gemini
   - `MISTRAL_API_KEY` — Mistral/Codestral
   - `DEEPSEEK_API_KEY` — DeepSeek R1/V3
   - `GROQ_API_KEY` — Groq (Llama)
   - `OPENROUTER_API_KEY` — OpenRouter (multi-modelo)
   - `ANTHROPIC_API_KEY` — Claude directo (opcional, Relay ya da modelos Claude sin key)
   - `GITHUB_PAT` — Personal Access Token con scope repo+workflow, para commits y workflow_dispatch
   - `TELEGRAM_BOT_<NOMBRE>` — token de cada bot de @BotFather
   - `NEWSAPI_KEY` — newsapi.org (gratis, 100 req/día)
   - `CF_API_TOKEN`, `CF_KV_NAMESPACE_ID`, `CF_R2_ACCESS_KEY`, `CF_R2_SECRET_KEY` — Cloudflare KV/R2 (opcional, memoria persistente)
   - `HF_TOKEN` — HuggingFace, si se quiere pipeline de datasets/modelos
3. Crear la tabla central 'Estado Persistente MIU' con columnas: Tipo (enum: HUESO,NODO,DATO,ISSUE,SKILL,LOG,BOOTSTRAP), Título (texto), Contenido (markdown), Fuente URL (uri), Nivel Epistémico (enum: SÉ,INFIERO,CONJETURO,NO SÉ,N/A), Estado MIU (enum: NEGRO,ROJO,AMARILLO-bajo,AMARILLO-medio,VERDE,ORO,ACTIVO,PENDIENTE), SHA256 (texto), Tags (texto). O usar la tabla YA COMPARTIDA `table:cmr4g2bhl18sr0qm53kndb32c` si esta cuenta tiene acceso a ella — en ese caso NO crear una nueva, apuntar los workflows ahí directamente.
4. Crear un repo GitHub propio (o pedir acceso de escritura a `Jaime393/MIU`).

## 1. Patrón central: 'Hub de Ingesta'
Construir PRIMERO este workflow — todos los demás lo alimentan.
- Trigger: Webhook (builtin.webhook)
- Recibe JSON: {tipo_miu, titulo, contenido, tags, nivel_epistemico, estado_miu, fuente_url?}
- Step: 'Add record to table' → tabla MIU → mapea cada campo del body a la columna correspondiente
- Guardar la URL del webhook generada — se usa en TODOS los demás workflows como destino de `http.request` POST para ingestar datos. Esto evita el bug de plataforma donde 'Add record to table' a veces no expone columnas al crearlo por API — el hub se configura UNA vez desde la UI y ya queda.

## 2. Workflows prioritarios a recrear (orden recomendado)

### A. 🕸️ Concept Graph & Gaps (mensual)
Propósito: lee corpus → Cohere embeddings → matriz similitud coseno → detecta pares relacionados + nodos aislados (gaps) → issue GitHub + Telegram.
Pasos: (1) Find records en tabla (list, ~100) (2) Custom code: arma arrays `texts` e `ids` desde Título+Contenido de cada registro (3) HTTP POST a `https://api.cohere.com/v2/embed` body `{model:'embed-multilingual-v3.0', texts, input_type:'clustering', embedding_types:['float']}` header `Authorization: Bearer {secrets.COHERE_API_KEY}` (4) Custom code: dot product coseno entre todos los pares, top 10 similares + aislados (score bajo) (5) AI prompt (object mode): recibe pares+aislados, devuelve clusters, gaps críticos, experimentos, issue_title, issue_body, telegram_msg (6) GitHub create issue (7) HTTP POST al hub de ingesta (8) Telegram sendMessage SIN parse_mode (9) Email opcional.
⚠️ BUG CONOCIDO no resuelto en la cuenta original: el paso (2) a veces devuelve arrays vacíos — verificar que el campo se llama exactamente 'Título' (con tilde) y que el objeto de cada record realmente trae ese campo poblado antes de mapear.

### B. 🏋️ Self-Evolution Loop (semanal, domingo)
Propósito: analiza crecimiento del corpus → detecta gaps → issue GitHub → dispara Action de sync HF.
Pasos: (1) Get workspace usage (créditos/steps) (2) Find records tabla (list ~50) (3) AI prompt object 'hard' tier, adjunta los records como attachment, prompt pide: 3 gaps epistémicos, 3 experimentos falsificables, modelos HF recomendados, issue_title/body, evaluación crecimiento, telegram_msg (4) Custom code trivial: `return {body:{ref:'main'}}` (el nombre de branch, NO agregar 'inputs' extra salvo que el .yml del repo los declare) (5) GitHub create issue (6) HTTP POST dispatch a `.../actions/workflows/<nombre>.yml/dispatches` con ese body (7) HTTP POST hub ingesta (8) Telegram sin parse_mode (9) Email.

### C. 🧬 GGUF Build Pipeline (semanal, sábado)
Propósito: genera script de fine-tuning con Codestral → commit a GitHub → dispara evaluación.
Pasos: (1) Find records tabla, cuenta total (2) Custom code: cuenta por Tipo (3) HTTP POST a `https://api.mistral.ai/v1/chat/completions` model `codestral-latest`, pide script Python unsloth completo (4) Custom code: base64 encode del script (5) HTTP GET al mismo path del archivo en GitHub para obtener el `sha` actual SI YA EXISTE (6) Custom code: arma body `{message, content, committer}` y solo agrega `sha` si el GET anterior lo devolvió (evita error 'sha wasnt supplied' al sobrescribir) (7) HTTP PUT commit a GitHub contents API (8) HTTP POST dispatch a Action de evaluación, body `{ref:'main', inputs:{...}}` SOLO con los inputs que el .yml realmente declara (9) Telegram + hub ingesta + email.

### D. 👁️ Gemini Vision Analyst (manual, bajo demanda) — VERIFICADO FUNCIONANDO end-to-end
Trigger manual con campos: descripcion, tipo (enum IMAGEN/PDF/DRIVE/URL/TEXTO), url_fuente, contexto.
Pasos: (1) HTTP POST a `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={secrets.GEMINI_API_KEY}` con prompt combinando los 4 campos del trigger (2) AI prompt object (easy tier) que estructura la respuesta de Gemini en campos MIU: tags, titulo, tipo_miu, contenido, estado_miu, nivel_epistemico, resumen_telegram (3) GitHub create issue (4) HTTP POST hub ingesta (5) Telegram (6) Email.

### E. 🛡️ Sistema Inmune / Cerberus Audit (webhook, seguridad)
Propósito: gateway que evalúa eventos/tool-calls entrantes en señales (Policy, Behavioral, Content, Injection) → ALLOW/AUDIT/BLOCK.
Pasos: (1) Webhook trigger recibe evento (2) AI prompt object: evalúa las 4 señales, produce score 0-100 y veredicto (3) Paths: si score≥50 → issue GitHub + Estado MIU=ROJO + Telegram alerta; si no → ingesta normal + Telegram ALLOW.

### F. 📚 Corpus Consolidator / Weekly Digest (síntesis)
Propósito: lee corpus completo + issues abiertos → AI genera README.md / CORPUS_SUMMARY.md vivos → commit a GitHub.
Pasos: (1) Find records tabla (list, tantos como haya — NO asumir 300, usar el conteo real) (2) Find issues GitHub (3) AI prompt object: genera 2-3 documentos markdown con secciones fijas (4) Custom code: base64 de cada doc (5) HTTP PUT commit cada uno a GitHub (repetir patrón GET-sha si el archivo ya existe) (6) Telegram sin parse_mode + Email.

## 3. Reglas anti-bugs (aprendidas con errores reales)
1. **Telegram**: NUNCA usar `parse_mode: Markdown` con texto generado por IA — el texto suele traer asteriscos/guiones bajos sin escapar y Telegram devuelve 400. Enviar texto plano.
2. **GitHub PUT contents (crear o actualizar archivo)**: si el archivo YA EXISTE, la API exige el campo `sha` del archivo actual — hacer GET previo a la misma URL y pasar `payload.sha` condicionalmente en el PUT.
3. **GitHub Actions dispatch (workflow_dispatch)**: el body requiere `ref` (branch, normalmente 'main'). Si se agrega `inputs`, deben coincidir EXACTAMENTE con los inputs declarados en el `.yml` del Action — de lo contrario 422 'Unexpected inputs provided'.
4. **'Add record to table' (addToDataTable) creado por API/asistente**: puede aparecer sin columnas mapeables (bug de plataforma reportado). Workaround confiable: usar el patrón de Hub de Ingesta (sección 1) — un único webhook con ese step configurado UNA vez desde la UI, y todos los demás workflows le hacen POST via `http.request`.
5. **No asumir volumen de datos fijo** ('300 registros', etc.) en prompts — usar siempre el conteo real devuelto por el step de lectura.
6. **Custom code sandbox**: no soporta `require`/imports de Node — solo lodash (`_`), Buffer, atob/btoa, TextEncoder/Decoder, crypto.subtle, crypto.randomUUID. Para Python u otros lenguajes, generar el CÓDIGO como texto (vía AI) y commitearlo a GitHub — no se ejecuta dentro de Relay.

## 4. Filosofía de datos (llevar a la nueva cuenta)
- Regla epistémica: solo D_f (dimensión fractal, box-counting/DFA) se trata como métrica legítima y falsificable. K_i se documentó como tautología circular — no usar como soporte de validación.
- Niveles epistémicos: SÉ (validado) > INFIERO (evidencia indirecta) > CONJETURO (hipótesis) > NO SÉ.
- Estado MIU (semáforo de madurez): NEGRO(auditoría pendiente) → ROJO(riesgo) → AMARILLO-bajo/medio → VERDE(validado) → ORO(fundacional).

## 5. Qué NO recrear
Evitar volver a construir automatizaciones especulativas de 'consciencia', 'autonomía general' o 'entrenamiento de modelos conscientes' — no son capacidades reales de esta plataforma ni de los modelos de IA subyacentes. Lo real y valioso es: ingesta de datos, síntesis con IA, detección de anomalías/gaps, y notificación — todo lo demás es narrativa, no funcionalidad.

---
_Generado por el asistente Relay.app — commiteado en docs/BLUEPRINT.md del repo compartido._