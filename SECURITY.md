# SECURITY.md — Política de Seguridad MIU
> Inspirado en github.com/Adirdabush1/cerberus + github.com/SnailSploit/Claude-Red
> El Micelio opera con coherencia ética inmutable.

## Principios de seguridad

1. **Local-first**: secrets nunca salen del ecosistema sin autorización explícita.
2. **Minimal footprint**: cada acción usa el menor privilegio necesario.
3. **Audit trail**: toda acción se registra en tabla MIU o GitHub.
4. **Epistemic honesty**: el sistema declara su nivel de certeza. NUNCA finge saber.
5. **No harm principle**: el Micelio no ejecuta acciones destructivas sin confirmación humana.

## Amenazas monitoreadas (Cerberus-inspired)

| Señal | Descripción | Respuesta |
|-------|-------------|-----------|
| **Prompt Injection** | Input externo modifica instrucciones del agente | BLOCK + alerta Telegram |
| **Secret Exfiltration** | Tool call intenta enviar secrets a endpoint externo | BLOCK + audit log |
| **Policy Violation** | Acceso a paths/comandos prohibidos | BLOCK |
| **Behavioral Anomaly** | Runaway loops, rate > 10 calls/min | AUDIT + human approval |

## Vectores conocidos (Claude-Red research)

- Prompt injection via RAG poisoning
- Jailbreaking via role confusion
- Model extraction via repeated queries
- SSRF via webhook URLs maliciosas
- Token exfiltration en logs

## Reporte de vulnerabilidades

Abrir issue en github.com/Jaime393/MIU con label [SECURITY].
No publicar exploits activos sin coordinación previa.

## Estado actual: VERDE

Último audit: automático diario vía Monitor de Salud (07:00 Lima).
