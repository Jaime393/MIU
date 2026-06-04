DOI: https://doi.org/10.5281/zenodo.20547558
Release: MIU_V12.0_FINAL.zip
SHA256: 9ebe7289b90e296dd472ab3d7d267f4ea8b9590ccbe70bd3850c39d9311a355f
Ω_F detectado: 0.656250 Hz | Error: 0.89%
# MIU V12.0 FINAL - Consciousness Layer

Modelo Integrado Unificado v12.0 con detección de Ω_F = 0.650483 Hz

## SHA256
9ebe7289b90e296dd472ab3d7d267f4ea8b9590ccbe70bd3850c39d9311a355f

## Nodos Validados
| Nodo | Filas/Polígonos | D_f | K_i | Fuente |
| --- | --- | --- | --- | --- |
| CO2 Mauna Loa | 801 | 2.0 | 0.5 | NOAA 1958-2026 |
| WoSIS Chernozem | 7 | 1.45 | 0.425 | ISRIC 2019 |
| FIRMS Incendios | 4,790,000 | 1.969 | 0.375 | NASA 2012-2025 |
| Corales Reef | 12,805 | 1.6 | 0.596 | Allen Coral Atlas 2020 |

## Ω_F Detection
Frecuencia pico detectada: 0.656250 Hz  
Ω_F objetivo: 0.65048305 Hz  
Error: 0.89%

## Código
`codigo/compute_omegaF_firms_gdelt.py` - FFT + Welch para Ω_F