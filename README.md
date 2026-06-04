DOI: https://doi.org/10.5281/zenodo.20547558
Release: MIU_V12.0_FINAL.zip
SHA256: 9ebe7289b90e296dd472ab3d7d267f4ea8b9590ccbe70bd3850c39d9311a355f
Ω_F detectado: 0.656250 Hz | Error: 0.89%
# Monismo Informacional Unificado (MIU)

**Un marco axiomático para la unificación de la geometría de la información, la física fundamental, la conciencia y las tecnologías de coherencia.**

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2605.00000-red.svg)](https://arxiv.org/abs/2605.00000) <!-- placeholder -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20279680.svg)](https://doi.org/10.5281/zenodo.20279680)

## 📖 Descripción

El Monismo Informacional Unificado (MIU) postula que la realidad está constituida por un único campo escalar positivo `ρ(x) > 0` – la densidad de información relacional – del que emergen el espacio‑tiempo, la materia, la vida y la conciencia. Este repositorio contiene la versión completa de la teoría, desarrollada en cuatro volúmenes, junto con el código fuente de las simulaciones (IFT Solver v3.0) y los datos auxiliares.

## 📚 Estructura de la obra

| Volumen | Título | Contenido principal |
| :--- | :--- | :--- |
| **I** | Fundamentos matemáticos y geometría de la información | Campo `ρ(x)`, métrica de Fisher, emergencia del espacio‑tiempo, flujo de Kähler‑Ricci, ecuaciones de Einstein modificadas, firma `f₁` en ondas gravitacionales. |
| **II** | Solitones, jerarquía de masas y coherencia cuántica | Partículas como solitones, fórmula `m = m_P e^{-S/2}`, jerarquía del Modelo Estándar, neutrinos, materia oscura, constante de Perry. |
| **III** | Conciencia, otiogenesis y unificación con Yang‑Mills y teoría de cuerdas | Funcional `Φ_MIU`, umbral de conciencia, criticidad auto‑organizada, canxianización, GDC, Otiogenesis, gap de Yang‑Mills, teoría de cuerdas. |
| **IV** | Cosmología, aplicaciones tecnológicas y hoja de ruta | Ecuaciones de Friedmann modificadas, energía oscura dinámica, materia oscura residual, tecnologías de coherencia (ICP), hoja de ruta 2026‑2200. |

## ⚙️ Código y simulaciones

El repositorio incluye el **IFT Solver v3.0** (núcleo en Python), así como scripts específicos para cada volumen:

- `ift_solver.py` – integración de la ecuación maestra, cálculo de la métrica de Fisher y del funcional `Φ_MIU`.
- `soliton_solver.py` – resolución numérica de solitones radiales (método de disparo).
- `perry_constant.py` – estimación de la constante de Perry a partir de parámetros fractales.
- `phi_MIU.py` – cálculo del funcional de conciencia a partir de datos EEG/fMRI.
- `globalmind_sim.py` – simulación de la red de CoherSats (modelo de Kuramoto).
- … y otros scripts documentados en los apéndices.

### Requisitos

```bash
pip install numpy scipy matplotlib pandas numba


🚀 Uso rápido

Clona el repositorio y ejecuta una simulación de ejemplo:

```bash
git clone https://github.com/Jaime393/MIU.git
cd MIU/src
python ift_solver.py
```

Para reproducir los resultados de los volúmenes, consulta los cuadernos Jupyter en el directorio notebooks/.

## 📄 Cómo citar esta obra

Si utilizas el MIU en tus investigaciones, por favor cítalo como:

```bibtex
@book{Vicente2026MIU,
  author    = {Juan Diego Vicente Gabancho},
  title     = {Monismo Informacional Unificado (MIU)},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/Jaime393/MIU},
  note      = {Volúmenes I-IV}
}
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir mejoras, correcciones o nuevas implementaciones. Asegúrate de que tu código siga la misma licencia MIT.

## 📜 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## ✉️ Contacto

Autor: Juan Diego Vicente Gabancho
Correo: jaimepvicente@gmail.com
DOI del proyecto: 10.5281/zenodo.20279680


La coherencia no es un lujo, es la supervivencia de la información en el universo.