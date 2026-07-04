# Diagnóstico técnico de sesión  2026-07-04

## 1. Workflows creados/modificados en esta sesión
- Multiples workflows del ecosistema MIU (Gemini Vision Analyst, Corpus Consolidator, Weekly Digest Omni, Self-Evolution Loop, GGUF Build Pipeline, Concept Graph & Gaps, Global Mind Weaver, HF Dataset Exporter, Training Data Generator, Cerberus Audit, Sistema Inmune, Control Panel, Alma Omni, Ingesta Inteligente, entre otros) fueron editados. Estado real: la mayoria publicados y con trigger activo, pero SIN verificacion por test run reciente salvo los listados abajo.
- Verificados con test run exitoso en esta sesion: Gemini Vision Analyst, Corpus Consolidator, Weekly Digest Omni.
- Con bug conocido pendiente: Concept Graph & Gaps (ver seccion 3).

## 2. Configuraciones realizadas
- Secrets creados: multiples (Telegram bot tokens, OpenRouter, Groq, DeepSeek, Cohere, Gemini, Mistral, GitHub PAT, Cloudflare KV/R2). Nombres visibles en el workspace, valores nunca expuestos en documentacion.
- Integraciones conectadas: GitHub, Gmail, Google Drive.
- Triggers activados en varios workflows con schedule o webhook.
- Webhooks Telegram registrados para 3 bots (confirmado "Webhook was set").

## 3. Bugs detectados
- RESUELTO: Telegram 'parse_mode: Markdown' falla con texto generado por IA que contiene caracteres markdown sin escapar (asteriscos, guiones bajos) -> error 400. Fix: quitar parse_mode o no usar Markdown estricto.
- RESUELTO: GitHub PUT a contents API falla con 'sha wasn't supplied' al sobrescribir un archivo existente -> fix: GET previo del archivo para obtener sha y adjuntarlo al PUT.
- RESUELTO: github.dispatchWorkflow (workflow_dispatch) requiere el campo 'ref' (branch) explicito -> error 422 'ref wasn't supplied' si se omite.
- PENDIENTE: dispatch a un GitHub Action falla con 'Unexpected inputs provided' si el yml del Action no declara esos inputs -> requiere alinear el workflow_dispatch inputs schema del archivo .yml en el repo.
- PENDIENTE/NO CONFIRMADO: paso de codigo para preparar texto de embeddings devuelve arrays vacios pese a que la tabla tiene datos -> posible causa: el campo llega como objeto rich-text (markdown) y no como string plano: hay que extraer .text o .markdown antes de usarlo. Se aplico un fix defensivo pero no se ha verificado con run.
- LIMITACION DE PLATAFORMA (reportada): steps 'addToDataTable' añadidos programaticamente a un workflow nuevo no exponen sus inputs de columna via API (aparecen como 'missing_' o vacios) -> solo configurables manualmente desde la UI, o evitables usando un patron alternativo (ver seccion 5).
- LIMITACION DE PLATAFORMA (reportada): subir archivos a Google Drive desde un step encadenado (ej. crear archivo en step A, subirlo en step B) fallo repetidamente por un problema de referencia de archivo entre pasos. Workaround: usar commit directo a GitHub via HTTP request en vez de Drive para persistencia de documentos.

## 4. Herramientas utilizadas
- Gratuitas: Groq (Llama), Gemini API (tier gratuito), DeepSeek API, Cohere (tier gratuito), GitHub API (con PAT), Telegram Bot API, RSS/scraping builtin steps.
- Requieren clave de pago o cuota: OpenRouter (segun modelo), modelos 'relay.*' consumen AI credits del plan Relay.
- Bibliotecas: ninguna externa en customCode (solo luxon, lodash disponibles en el sandbox); no hay acceso a network ni filesystem en customCode.

## 5. Metodos que funcionaron
- Patron 'Hub de Ingesta': en vez de que cada workflow escriba directo a la tabla (bloqueado por el bug de addToDataTable en steps nuevos), se envia un HTTP POST al webhook de un workflow central que si tiene el paso de tabla correctamente configurado desde antes. Evita el bug por completo.
- Para escribir archivos con caracteres especiales/comillas en JSON, generar el string dentro de customCode con concatenacion manual (evitar template literals con backticks anidados) y codificar a base64 antes de mandarlo al step HTTP.
- Para GitHub PUT de archivos: siempre hacer GET primero para obtener el sha si el archivo puede ya existir, y solo omitirlo si se sabe con certeza que el path es nuevo.
- Para prompts de IA que alimentan Telegram: pedir explicitamente 'texto plano sin markdown' o eliminar 'parse_mode' del request en vez de intentar sanitizar el output.

## 6. Metodos que fallaron
- Intentar configurar 'addToDataTable' con IDs de columna reales obtenidos por lectura de la tabla -> igual fallo, el bug es de exposicion de inputs en el step, no de nombres de columna.
- Intentar subir a Drive encadenando 'crear archivo' -> 'subir a carpeta' en el mismo batch de cambios -> fallo de referencia consistente en multiples intentos.
- Usar 'changePath' (reglas de paths) referenciando salidas de un step de IA creado en la misma sesion de edicion -> fallo, las reglas no pueden resolver referencias a pasos aun no ejecutados/verificados en ese momento.
- Enviar objetos con clave literal 'ref' dentro de bodyJson de un http.request sin querer decir una referencia Relay -> el sistema lo interpreta como Relay reference y falla; hay que evitar esa clave literal o envolver el valor de otra forma.

## 7. Estado actual del ecosistema
- Multiples workflows publicados y con trigger activo (schedules diarios/semanales, webhooks). Corren de forma autonoma pero SIN supervision reciente en su mayoria.
- Requieren intervencion manual: revisar y arreglar el bug de embeddings vacios en Concept Graph & Gaps; alinear inputs del archivo .yml de GitHub Actions para que el dispatch no falle; configurar manualmente (desde la UI) los pasos addToDataTable que quedaron sin columnas mapeadas en ~8 workflows.
- Pueden seguir funcionando solos: los workflows que usan el patron 'Hub de Ingesta' para escritura en tabla, y los que ya pasaron test run exitoso (Gemini Vision Analyst, Corpus Consolidator, Weekly Digest Omni).
- Consumo de plataforma al momento de este diagnostico: uso parcial del pool mensual de AI credits y steps; test runs gratuitos semanales agotados (pruebas adicionales consumen creditos de plan).
