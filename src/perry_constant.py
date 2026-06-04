#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cálculo de la constante de Perry a partir de los mecanismos de amplificación.
"""

import numpy as np
from miu_constants import *

def perry_constant(J_over_gamma=10, D_f=D_f_mt, N_crom=N_crom,
                   L_over_ell=L_mt/ell_mt, d_s=1.67, N_ciclos=N_ciclos, PLV=PLV):
    """
    κ = (π/2) * (J/γ)^{D_f-1} * N_crom * sqrt(N_ciclos) * (L/ℓ)^{d_s} / sqrt(1-PLV^2)
    """
    base = (np.pi/2.0) * (J_over_gamma ** (D_f - 1.0))
    coop = N_crom
    phase = np.sqrt(N_ciclos)
    fractal = (L_over_ell ** d_s)
    plv_factor = 1.0 / np.sqrt(1.0 - PLV*PLV)
    kappa = base * coop * phase * fractal * plv_factor
    return kappa

if __name__ == "__main__":
    # Valores típicos para microtúbulos
    kappa = perry_constant(J_over_gamma=10, D_f=2.5, N_crom=100,
                           L_over_ell=1e4, d_s=1.67, N_ciclos=1000, PLV=0.74)
    print(f"Constante de Perry (teórica) = {kappa:.3e}")
    print(f"Valor experimental (Perry 2026) = {kappa_Perry:.3e}")
