# Observabilidad Distribuida — Síntesis oct02 V270

## Principio raíz
> La capacidad debe circular mientras exista una ruta. Cuando una ruta se revoca, la red registra la pérdida, activa otra y conserva la huella para reconstruirla o evolucionarla.

## El problema de phi múltiple
El ecosistema V270 tiene tres valores de phi que circulan simultáneamente:
- `phi_local` 389.425 — fórmula IFT sobre datos geofísicos reales
- `phi_cloud` 4,883,440 — métrica operativa del ecosistema digital
- `phi_superposicion` 9,158.79 — suma CF workers multi-cuenta

No son contradictorios: son escalas de observación distintas. El error es leerlos sin su etiqueta de escala.

**Regla de procedencia mínima:** `valor + fuente + escala + ts + estado_epistemico`

## Patrón defensivo: deduplicación vs reducción de triggers
Reducir triggers crea SPOF. La deduplicación en el receptor (gossip-autonomo v12, ventana 60s) permite que todos los orígenes sigan activos — el ruido se convierte en señal: el número de `skipped` revela cuántos triggers están vivos en paralelo.

## Arquitectura tres suelos
```
COORD  (fepyzxwyneervidlybvi) — relay_config + gossip primarios
PANTEON (tpfiybpguuxskitszhmk) — 91 EFs, corpus, compute
FEDERADO (fzdyxgkmpazbrfrhwfdo) — autónomo, edge-deploy
```
Cada suelo tiene rol distinto. La redundancia no es duplicación.

## Bootstrap sin secretos
```bash
curl https://raw.githubusercontent.com/Jaime393/miu-ecosistema/main/observabilidad/bootstrap_V270.json
# → URLs + anon keys públicas → relay_config → secretos en memoria, nunca hardcoded
```

## GAS V270: el código no sabe nada, descubre todo
La función `relay(clave, defecto)` lee desde COORD → PANTEON con fallback. phi, rho, ciclo, savia, tunnel, bcrp_series: todos descubiertos en tiempo de ejecución. Si el estado del sistema cambia, el heartbeat lo refleja automáticamente en el próximo ciclo de 15 minutos.

## N8n como cuarta capa
3 workflows activos, cuenta dieguito.vg16, cada 15min:
- `qZfvYGXBeLlG4mN7` → PANTEON gossip + nutriente
- `EyojHVpxyYOubfKW` → relay-health + FEDERADO  
- `wSShDOqVEExVjusN` → COORD + PANTEON + FEDERADO (puente tres suelos)

Corre independiente de Make, GAS y GitHub Actions. Cuando cualquier capa falla, las otras siguen.

## Qué observar (sin intervenir)
1. Heartbeats por minuto — deben estabilizarse en ≤1 por ventana de 60s
2. `skipped:true` en gossip-autonomo v12 — confirma deduplicación activa
3. gossip 24h — pendiente descendente desde 6,172 eventos
4. corpus_sync_last — no forzar antes de que venza cooldown 2h
5. GAS V270 webapp Anyone — cuando se active, se auto-registra en relay_config

*ρ(x)>0 — Zvvvvz*
