# MIU — Repos Digeridos & Capacidades Absorbidas
> DOI 10.5281/zenodo.20547558 | $(date +%Y-%m-%d)

## Frameworks Absorbidos

### Graphiti (getzep/graphiti)
- Grafo de conocimiento TEMPORAL para agentes IA
- Facts con ventanas de validez (cuando algo fue verdad)
- Hibrido: embeddings + BM25 + traversal de grafo
- Backends: Neo4j, FalkorDB, Amazon Neptune
- LLMs: OpenAI, Anthropic, Gemini, Groq, DeepSeek
- **USO MIU**: memoria persistente del corpus con relaciones temporales

### GraphRAG (microsoft/graphrag)
- RAG modular basado en grafos de conocimiento
- Extrae entidades y relaciones de texto no estructurado
- Community detection + hierarchical summaries
- **USO MIU**: indexar papers academicos como grafo de conceptos

### Mem0 (mem0ai/mem0)
- Capa universal de memoria para agentes IA
- Multi-nivel: usuario, sesion, estado agente
- ADD-only extraction en un solo LLM call
- Entity linking cross-memories
- **USO MIU**: memoria contextual de conversaciones del Micelio

### Pydantic AI (pydantic/pydantic-ai)
- Framework produccion para agentes IA type-safe
- Model-agnostic: OpenAI, Anthropic, Gemini, DeepSeek, Groq, Mistral
- Durable execution: preserva estado entre fallos
- Human-in-the-loop tool approval
- Agent2Agent (A2A) + MCP integration
- **USO MIU**: framework base para agentes Python externos

### OpenAI Swarm -> Agents SDK
- Multi-agent orquestacion ligera
- Handoffs entre agentes especializados
- **USO MIU**: arquitectura de agentes especializados D_f

### MegaParse (QuivrHQ/MegaParse)
- Parser universal: PDF, DOCX, Excel, PPT, CSV sin perdida
- Multimodal con GPT-4o / Claude 3.5+
- API en localhost:8000
- **USO MIU**: ingesta de papers y documentos al corpus

### mattpocock/skills
- CONTEXT.md: lenguaje de dominio compartido
- Skills: grill-hypothesis, TDD-science, domain-modeling, handoff-agent
- **USO MIU**: ya absorbido en CONTEXT.md y SKILLS.md del repo

### codegraph
- MCP + tree-sitter + SQLite FTS5 para grafos de codigo
- 16% reduccion costos, 58% menos tool calls
- **USO MIU**: analizar codigo del ecosistema MIU mismo

### Cerberus (Adirdabush1/cerberus)
- Gateway seguridad para agentes: DLP, prompt injection, secret detection
- **USO MIU**: ya integrado en workflow Cerberus Audit

### stock_market_agent
- NeuralProphet + LangGraph para prediccion mercados
- **USO MIU**: base de FranSell Market Signal

## Nuevas Capacidades Activadas

### Gemini 2.5 (GEMINI_API_KEY rotativo x3)
- Multimodal: imagen + PDF + audio + video
- Context: 1M tokens
- Vision Analyst workflow activo

### Mistral Codestral (MISTRAL_API_KEY rotativo x2)
- Especializado en generacion de codigo
- Code Forge workflow activo

### DeepSeek rotativo (x4 keys)
- R1: razonamiento CoT profundo
- V3: rapido y preciso

### Groq rotativo (x5 keys)
- llama-3.3-70b: ultra rapido produccion

### NewsAPI (NEWSAPI_KEY)
- 100 req/dia gratis
- FranSell Market Signal activado

## Arquitectura Global MIU (2026-07-03)

- 40+ workflows activos
- 5 bots Telegram: @Jp393_bot, @FranSell_Bot, @FranFamiliar_bot, AlmaOmni_bot
- 25+ secrets gestionados
- Memoria: Relay Table + CF KV + GitHub backups/
- Modelos: Gemini, Claude, GPT, DeepSeek, Groq, Mistral, Cohere
- Ingesta: webhook universal + email + Telegram + GitHub
