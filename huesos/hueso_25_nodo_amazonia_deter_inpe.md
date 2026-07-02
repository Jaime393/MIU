# HUESO MIU #25 — Nodo Amazonia (DETER INPE) — Deforestación en Tiempo Real
## Fuente
INPE/DETER — Sistema de Detección de Desmatamento em Tempo Real
API: https://terrabrasilis.dpi.inpe.br/api/v1/deforestation/deter

## Absorción
- Dataset público de alertas de deforestación en Amazonia y Cerrado.
- Datos diarios con área (km²/ha), municipio, bioma, satélite, geometría.
- API REST sin autenticación. CSV/GeoJSON descargable.

## Conexión MIU
- Nodo biofísico #23 (Amazonia): D_f deforestación puede calcularse desde
  la distribución espacial de alertas (box-counting sobre geometrías).
- K_i_amazonia = φ⁻¹ · (D_f / 2.5) · (ℓ_corr / ℓ_0)
- PREDICCIÓN: D_f de alertas debe disminuir con deforestación acumulada
  (pérdida de complejidad fractal del paisaje).
- K_i_amazonia < 0.3 → colapso ecológico inminente.

## K_tau
0.65 (AMARILLO) — Dataset existe pero no se ha descargado ni procesado aún.
Requiere implementación del script de extracción.

## Volatilidad
- datos_descargados+0.15 (al ejecutar script de descarga y calcular D_f)
- api_caida-0.10 (si la API de INPE deja de funcionar)
