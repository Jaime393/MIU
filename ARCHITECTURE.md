# MIU — Architecture 2026-07-03
> DOI 10.5281/zenodo.20547558 | 52 workflows | GlobalMind

## Hub Central

- **Ingesta Inteligente**: https://hook.relay.app/api/v1/playbook/cmr4riw5t5spu0qkv52s8cug8/trigger/HylMPaG9If61vi7gINy-lg
- Todos los workflows enrutan aqui. AI valida + enriquece antes de guardar en tabla MIU.

## Bots activos

| Bot | Workflow | Funcion |
|-----|----------|---------|
| @Jp393_bot | Telegram Gateway | Consultas MIU |
| @AlmaOmni_bot | Alma Omni | Claude Sonnet-5 + corpus |
| @FranSell_Bot | FranSell Intel | Senales mercado |
| @FranFamiliar_bot | Familiar Bot | Llama-3.3 familiar |

## Workflows por dominio

### Observacion diaria
- Pulso Diario (11:00), Vigilancia Geopolitica (06:30), Sismografo GDELT, Monitor Social
- Senales Macro (martes), Bio-Ecologia (lunes), OpenAlex Scholar (lunes)

### Inteligencia de mercado
- FranSell Market Signal (09:00), FranSell Intel (webhook)

### Investigacion
- Deep Researcher (DeepSeek R1), Multi-Model Consensus, Gemini Vision Analyst
- Red de Citas Cientificas, Monitor Web Profundo (martes), FutureHouse Research
- Vigía Global (arxiv diario), Monitor Zenodo (miercoles)

### Generacion
- Mistral Code Forge (Codestral → GitHub), GitHub Actions Generator
- Generador de Hipotesis (jueves), Espora Generativa (viernes)

### Memoria
- Corpus R2 Backup (domingo), Memoria GitHub Auto-Sync (23:00)
- Actualizacion REGISTRO_MAESTRO, Sintetizador Semanal (miercoles)

### Agentes
- Agente D_f Autonomo, OpenHands Agent, Global Intelligence Feed

### Sistema
- Monitor de Salud (08:00), Cerberus Audit (seguridad), Anomaly Log Detector
- Bootstrap Agente, Control Panel, Ingesta Inteligente (hub)

## Stack tecnico

- **Modelos**: Claude Sonnet-5, GPT-5.4, Gemini 2.5 Flash/Pro, DeepSeek R1/V3, Groq Llama-3.3-70B, Mistral Codestral
- **Fuentes**: arxiv, Zenodo, OpenAlex, GBIF, iNaturalist, GDELT, ReliefWeb, UN News, NewsAPI, HN, Reddit
- **Storage**: Relay Table + CF KV + CF R2 + GitHub backups/
- **CI/CD**: GitHub Actions (auto-generadas via Codestral)
