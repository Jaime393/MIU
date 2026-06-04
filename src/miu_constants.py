# miu_constants.py - Constantes físicas y del MIU
# Unidades SI (excepto cuando se indique)

import numpy as np

# Constantes fundamentales (CODATA 2025)
c = 2.99792458e8          # velocidad de la luz (m/s)
hbar = 1.054571817e-34    # constante reducida de Planck (J·s)
G = 6.67430e-11           # constante gravitacional (m³/kg·s²)
k_B = 1.380649e-23        # constante de Boltzmann (J/K)

# Unidades de Planck
ell_P = np.sqrt(hbar * G / c**3)   # longitud de Planck (m)
m_P = np.sqrt(hbar * c / G)        # masa de Planck (kg)
t_P = ell_P / c                    # tiempo de Planck (s)

# Constantes del MIU (dominio biológico-cerebral)
K_universal_bio = 1.0e-5   # s/m (producto τ·Ξ en sistemas biológicos cuánticos)
kappa_Perry = 5.1e5        # constante de Perry adimensional (microtúbulos)
Phi_c = 0.7                 # umbral de conciencia (adimensional)
kappa_min = 5e5            # coherencia mínima para conciencia (adimensional)

# Potencial logarítmico
alpha_log = 0.12            # coeficiente α (ajustado a DESI DR2)
u_star = 1.0                # escala de referencia (u_*)

# Parámetros de microtúbulos (para constante de Perry)

# ============================================================
# Espectro multifractal de la red cósmica
# Ref: García-Bellido, arXiv:2605.21554 (mayo 2026)
# ============================================================
D_f_cumulos = 1.2
D_f_filamentos = 1.8
D_f_paredes = 2.5
D_f_vacios = 3.0

# Dimensión fractal efectiva de microtúbulos (promedio)
D_f_mt = 2.5

# ============================================================
# Parámetros de energía oscura actualizados
# Ref: DESI DR2 + DES-Dovekie + Pantheon+, mayo 2026
# ============================================================
w0_DE = -0.803
wa_DE = -0.72
sigma_DE = 3.2
sigma_DE_min = 2.3
epsilon1_DE = 0.25
epsilon2_DE = -0.13
z_cruce1 = 0.5
z_cruce2 = None

# ============================================================
# Tensión de Hubble (H0DN, abril 2026)
# ============================================================
H0_local = 73.50
H0_CMB = 67.4
sigma_H0 = 6.0

# Nota autocrítica (v2.1):
# - D_f único refutado -> espectro multifractal.
# - Segundo cruce fantasma eliminado.
# - Firma f1 nunca confirmada por ET.
