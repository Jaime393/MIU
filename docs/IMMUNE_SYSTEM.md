# IMMUNE_SYSTEM.md — Sistema Inmune MIU
> Inspired by Cerberus (Adirdabush1/cerberus) + Claude-Red offensive methodology
> DOI: 10.5281/zenodo.20547558 | Status: ACTIVO

## Architecture

### Workflow: Sistema Inmune (webhook)
Receives any event → scores against 4 signals → BLOCK/AUDIT/ALLOW

### Signals (Cerberus-inspired)
| Signal | Weight | Examples |
|--------|--------|----------|
| INJECTION | 35 | ignore previous, jailbreak, DAN mode |
| POLICY | 30 | new role, act as, override instructions |
| BEHAVIORAL | 25 | exfiltrate, send secrets, infinite loop |
| CONTENT | 15 | XSS, eval(), javascript: |

### Actions
- **BLOCK** (score ≥ 70): GitHub issue [SECURITY] + Telegram ROJO + ingest as ISSUE
- **AUDIT** (score 40-69): Telegram warning + ingest as LOG
- **ALLOW** (score < 40): normal ingestion

### Integration Points
- Any Relay workflow can POST to the immune webhook before executing external actions
- AlmaOmni checks all incoming Telegram messages
- Ingesta Universal pre-validates content

## Files
- `tools/miu_immune.js` — core scoring engine (Node.js)
- `tools/miu_global_mind.py` — synthesis engine (Python)

## Current State: VERDE ✅
Last audit: automated daily via Monitor de Salud 08:00 Lima
