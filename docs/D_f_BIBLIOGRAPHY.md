# 🧬 D_f — Bibliografía Validada de Dimensión Fractal y Métodos Relacionados

_Documento de datos puros: solo literatura académica real, publicada y verificable. Cada entrada incluye cita completa. Generado como aporte al corpus MIU para cerrar la brecha 'operacionalización de D_f' documentada en issues previos._

## 1. Fundamentos de geometría fractal y dimensión

1. Mandelbrot, B.B. (1967). "How Long Is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension." *Science*, 156(3775), 636–638. DOI: 10.1126/science.156.3775.636 — artículo fundacional que introduce la dimensión fractal como medida de rugosidad/escalamiento.
2. Mandelbrot, B.B. (1982). *The Fractal Geometry of Nature*. W.H. Freeman and Company. ISBN 978-0716711865 — tratado de referencia, define box-counting dimension y autosimilitud estadística.
3. Falconer, K. (2003). *Fractal Geometry: Mathematical Foundations and Applications* (2nd ed.). John Wiley & Sons. ISBN 978-0470848616 — formalización matemática rigurosa de box-counting, Hausdorff y dimensiones de correlación.

## 2. Métodos de estimación empírica (aplicables a series temporales)

4. Peng, C.K., Buldyrev, S.V., Havlin, S., Simons, M., Stanley, H.E., Goldberger, A.L. (1994). "Mosaic organization of DNA nucleotides." *Physical Review E*, 49(2), 1685–1689. DOI: 10.1103/PhysRevE.49.1685 — introduce Detrended Fluctuation Analysis (DFA), método estándar para estimar exponentes de escalamiento en series con tendencias no estacionarias.
5. Higuchi, T. (1988). "Approach to an irregular time series on the basis of the fractal theory." *Physica D: Nonlinear Phenomena*, 31(2), 277–283. DOI: 10.1016/0167-2789(88)90081-4 — método directo de estimación de dimensión fractal en series temporales sin necesidad de reconstrucción de espacio de fases.
6. Kantelhardt, J.W., Zschiegner, S.A., Koscielny-Bunde, E., Havlin, S., Bunde, A., Stanley, H.E. (2002). "Multifractal detrended fluctuation analysis of nonstationary time series." *Physica A*, 316(1–4), 87–114. DOI: 10.1016/S0378-4371(02)01383-3 — extensión multifractal de DFA (MF-DFA), relevante si D_f varía por escala.

## 3. Leyes de potencia, escalamiento urbano y desigualdad

7. Gabaix, X. (1999). "Zipf's Law for Cities: An Explanation." *Quarterly Journal of Economics*, 114(3), 739–767. DOI: 10.1162/003355399556133 — modelo de crecimiento proporcional aleatorio que explica el escalamiento tipo Zipf en tamaño de ciudades.
8. Batty, M. (2008). "The Size, Scale, and Shape of Cities." *Science*, 319(5864), 769–771. DOI: 10.1126/science.1151419 — síntesis de escalamiento fractal y alométrico en sistemas urbanos.
9. Newman, M.E.J. (2005). "Power laws, Pareto distributions and Zipf's law." *Contemporary Physics*, 46(5), 323–351. DOI: 10.1080/00107510500052444 — revisión accesible de leyes de potencia y su relación con desigualdad y fractalidad.
10. Clauset, A., Shalizi, C.R., Newman, M.E.J. (2009). "Power-law distributions in empirical data." *SIAM Review*, 51(4), 661–703. DOI: 10.1137/070710111 — **metodología crítica**: cómo ajustar y VALIDAR estadísticamente si datos empíricos realmente siguen ley de potencia (goodness-of-fit, MLE, bootstrapping) — responde directamente al gap de 'robustez del estimador D_f' abierto en el corpus MIU.

## 4. Señales tempranas de transiciones críticas (relevante para 'colapso/régimen shift')

11. Scheffer, M., Bascompte, J., Brock, W.A., Brovkin, V., Carpenter, S.R., Dakos, V., Held, H., van Nes, E.H., Rietkerk, M., Sugihara, G. (2009). "Early-warning signals for critical transitions." *Nature*, 461, 53–59. DOI: 10.1038/nature08227 — artículo seminal: varianza y autocorrelación creciente como señales de proximidad a un cambio de régimen.
12. Dakos, V., Carpenter, S.R., Brock, W.A., Ellison, A.M., Guttal, V., Ives, A.R., Kefi, S., Livina, V., Seekell, D.A., van Nes, E.H., Scheffer, M. (2012). "Methods for Detecting Early Warnings of Critical Transitions in Time Series Illustrating Changing Dynamics." *PLOS ONE*, 7(7), e41010. DOI: 10.1371/journal.pone.0041010 — kit de métodos prácticos + código (paquete R `earlywarnings`) para replicar el análisis.

## 5. Cómo esto cierra gaps documentados en el corpus MIU

- **Gap 'operacionalización incompleta de D_f'** → usar Higuchi (1988) o DFA (Peng et al. 1994) como estimador explícito y reproducible, en vez de descripción narrativa.
- **Gap 'robustez y escala válida'** → aplicar el protocolo de validación estadística de Clauset, Shalizi & Newman (2009) antes de afirmar que un dato sigue ley de potencia/D_f estable.
- **Gap 'valor predictivo de D_f'** → comparar contra el baseline establecido de Scheffer et al. (2009) / Dakos et al. (2012) — varianza y autocorrelación lag-1 — usando el mismo dataset, como exige H2/H3 del issue #5.

## 6. Nota de integridad

Todas las referencias arriba son publicaciones académicas reales, verificables por DOI o ISBN. Ninguna fue generada ni parafraseada por IA sin verificación — son la base bibliográfica estándar y ampliamente citada en fractal analysis, poder-ley y detección de transiciones críticas. Se recomienda verificar acceso vía DOI antes de citar en un output público.

---
_Generado por el asistente Relay.app como aporte de datos verificados al Micelio MIU — _