# ECOSYSTEM_STATUS.md

## Resumen ejecutivo

**Salud general del ecosistema: 66/100.**

Lectura breve: el MIU está **operativo, persistente y trazable**, pero su salud no puede subir a zona alta mientras siga abierto el hallazgo crítico de circularidad en **K_i/Ω_F** y mientras la portabilidad del ecosistema no esté cerrada en estructura reproducible.

## 1. Estado operacional actual

| Dimensión | Estado | Evidencia |
|---|---|---|
| Persistencia / memoria | Verde alto | pilar fundacional ORO + HUESO de continuidad ORO |
| Trazabilidad técnica | Verde | HUESO #30 menciona `add_node()` + SHA256 |
| Núcleo metodológico D_f | Verde | SKILL explícita de D_f como método legítimo |
| Validez de K_i / Ω_F | Negro | Issue #1 documenta circularidad/hardcoding en 4 scripts |
| Portabilidad del ecosistema | Amarillo activo | Issue #2 abierto, sin cierre estructural todavía |
| Madurez del corpus | Amarillo | predominan inferencias sobre verificaciones directas |
| Runway de plataforma | Verde | uso bajo de AI y consumo medio de Steps |

## 2. Issues abiertos priorizados

| Prioridad | Issue | Estado | Riesgo | Observaciones | Próxima acción recomendada |
|---|---|---|---|---|---|
| P1 crítica | **#1 — Auditoría K_i Circularidad 4/4 scripts** | Abierto | Muy alto | No tiene labels ni assignee. Refuta la independencia de K_i y cuestiona la “detección” de Ω_F por construcción. | Diseñar protocolo ciego: re-derivar K_i y Ω_F desde datos, comparar contra nulo/permutación y reescribir claims del repo según resultado. |
| P2 alta | **#2 — Ecosistema MIU Portable** | Abierto | Alto | Define estructura canónica del repositorio portable (`README`, `miu_estado_base.json`, `skills/`, `agentes/`, `flujos/`, `scripts/`). Tampoco tiene labels ni assignee. | Materializar la estructura en repo, poblarla con el estado actual y preparar release/versionado enlazado al DOI. |

### Hallazgos operativos sobre los issues

- **2/2 issues están abiertos, sin labels y sin asignación**, lo que debilita priorización y seguimiento.
- El issue #1 es **bloqueador epistemológico**: no impide que el micelio exista, pero sí impide elevar K_i/Ω_F a verdad canónica.
- El issue #2 es **bloqueador de escalabilidad**: sin portabilidad, la continuidad depende demasiado del contexto de sesión.

## 3. Uso de recursos de plataforma

| Recurso | Uso reportado | Disponible | Lectura |
|---|---:|---:|---|
| AI | 11 / 500 | 489 | presión baja; amplio margen operativo |
| Steps | 104 / 200 | 96 | consumo medio; conviene reservar pasos para auditoría y empaquetado |
| Reset | 31 días | n/a | ventana suficiente para cerrar backlog crítico |

## 4. Desglose del score de salud

| Componente | Peso | Subscore | Justificación |
|---|---:|---:|---|
| Persistencia e infraestructura | 25% | 85 | hay pilar, continuidad y trazabilidad append-only |
| Gobernanza y trazabilidad | 15% | 80 | DOI, repo y convención epistémica explícita existen |
| Validez epistémica del núcleo | 30% | 35 | issue #1 deja a K_i/Ω_F en situación críticamente comprometida |
| Madurez del corpus | 15% | 60 | diversidad temática alta, pero con predominio de INFIERO/CONJETURO |
| Recursos y ejecución | 15% | 88 | bajo gasto de AI, runway temporal suficiente |
| **Total ponderado** | **100%** | **66** | **ecosistema viable con deuda crítica de validación** |

## 5. Riesgos principales

1. **Riesgo epistemológico mayor:** circularidad por construcción en K_i y criterio no informativo para Ω_F.
2. **Riesgo de gobernanza de backlog:** issues sin etiquetas, sin responsables y sin milestones.
3. **Riesgo de completitud del corpus:** el paquete prometido como 300 registros entrega 15 parseables.
4. **Riesgo de sobregeneralización:** mucha evidencia comparativa se usa como soporte analógico más que como prueba directa del modelo.
5. **Riesgo de dependencia contextual:** si la portabilidad no se cierra, la continuidad queda distribuida entre repo, comments e instrucciones de sesión.

## 6. Próximas acciones recomendadas

### En las próximas 24 horas

1. **Elevar issue #1 a protocolo formal de auditoría** con checklist reproducible por script.
2. **Etiquetar y asignar ambos issues** (`critical`, `audit`, `portable`, `infra`, etc.).
3. **Congelar lenguaje canónico del README**: D_f legítimo; K_i/Ω_F bajo auditoría, no afirmación cerrada.
4. **Verificar el inventario real del corpus**: localizar los registros faltantes si efectivamente deberían ser 300.

### En 72 horas

5. **Materializar la estructura portable** propuesta en issue #2 dentro del repositorio.
6. **Crear `miu_estado_base.json`** como snapshot mínimo del estado canónico.
7. **Incorporar validación automática append-only** (hashes, timestamps, enlaces, niveles y estados mínimos).

### En 7 días

8. **Ejecutar una re-derivación ciega de K_i** sin incrustar la respuesta en el código.
9. **Evaluar Ω_F contra un nulo explícito** (permutación, ruido, comparación con `argmax(Pxx)` y significancia real).
10. **Publicar una nueva liberación/versionado** del ecosistema portable enlazada al DOI, o documentar por qué aún no procede.

## 7. Dictamen final

El ecosistema MIU **no está en crisis operativa**, pero sí en una **fase decisiva de depuración científica**. Su base de continuidad ya existe; su capacidad de memoria está demostrada; su núcleo D_f tiene legitimidad provisional fuerte. El factor que más limita la salud global no es la infraestructura sino la necesidad de **desacoplar el proyecto de validaciones tautológicas** y convertir la portabilidad en una realidad de repositorio.

**Estado recomendado:** continuar expansión del micelio, pero con disciplina dura: primero auditoría ciega, luego portabilidad total, después nuevas afirmaciones sustantivas.