# PAI-01 — Protocolo de Absorción de Inteligencia

## Propósito
Permitir que cualquier nodo del micelio integre nuevas APIs, servicios, o tecnologías externas de forma estandarizada.

## Pasos
1. **Detección**: el módulo `tejedor.py` identifica una carencia (ej. falta de datos de clima).
2. **Búsqueda**: `absorber.py` busca en fuentes públicas una API que cubra esa carencia.
3. **Selección**: evalúa la API según criterios de coherencia (K_i, D_f, FDC).
4. **Integración**: genera un plugin para esa API (siguiendo el formato de `miu_plugin_manager.py`).
5. **Validación**: prueba la API con una llamada de prueba y registra el resultado.
6. **Publicación**: sube el plugin a GitHub/Drive para que otros nodos lo absorban.

## Ejemplo
Si se detecta carencia de datos de mercado, `absorber.py` busca APIs financieras (ej. Alpha Vantage, Yahoo Finance), selecciona la más coherente, genera un plugin `market_plugin.py` y lo valida.
