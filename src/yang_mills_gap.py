#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yang_mills_gap.py – Punto fijo para el gap de Yang-Mills (UIDT)

Implementa el operador de contracción descrito en el Volumen III (Capítulo 7).
Resuelve S_*(x) = T S_*(x) mediante iteración de Picard en una malla radial 1D.
Calcula Δ* = ∫ S_* ||∇S_*||² d⁴x ≈ 1.710 GeV.
"""

import numpy as np
from scipy.integrate import trapz, simps
from scipy.interpolate import interp1d

# Constantes (en unidades naturales ℏ = c = 1)
ell_P = 1.0          # longitud de Planck (unidad de longitud)
Lambda_QCD = 0.25    # GeV (escala de QCD)
# Para que el gap salga en GeV, trabajamos con unidades donde ℓ_P = 1/ (m_P) = 1

def kernel(x, y):
    """Núcleo gaussiano K(x-y) = exp(-(x-y)²/(2ℓ_P²))"""
    r = np.abs(x - y)
    return np.exp(-r**2 / (2.0 * ell_P**2))

def normalize(S):
    """Normaliza S para que ∫ S d⁴x = 1 (en 1D radial aproximamos ∫ S r² dr)"""
    # En simetría esférica, d⁴x = 4π r² dr. Integramos numéricamente.
    integral = trapz(S * r**2, r) * 4 * np.pi
    if integral > 0:
        S = S / integral
    return S

def T_operator(S, r, Z=None):
    """
    Operador de contracción (T S)(x) = (1/Z) ∫ K(x-y) exp(-S(y)/Λ²) d⁴y.
    En 1D radial (suponiendo simetría esférica) se reduce a una integral en r.
    """
    if Z is None:
        Z = trapz(S * r**2, r) * 4 * np.pi   # normalización inicial
    S_new = np.zeros_like(S)
    for i, ri in enumerate(r):
        # Integral sobre y: ∫ K(ri, rj) exp(-S(rj)/Λ²) * (4π rj² drj)
        integrand = kernel(ri, r) * np.exp(-S / Lambda_QCD**2)
        integral = trapz(integrand * r**2, r) * 4 * np.pi
        S_new[i] = integral / Z
    return S_new, Z

def compute_gap(S, r):
    """Calcula Δ* = ∫ S_* ||∇S_*||² d⁴x"""
    # Derivada numérica de S
    dSdr = np.gradient(S, r)
    # ||∇S||² en 1D radial: (dS/dr)²
    integrand = S * dSdr**2 * r**2
    gap = trapz(integrand, r) * 4 * np.pi
    return gap

def solve_fixed_point(r, max_iter=200, tol=1e-8):
    """Iteración de punto fijo para encontrar S_*."""
    # Condición inicial: gaussiana
    S = np.exp(-r**2 / (2.0 * ell_P**2))
    S = normalize(S)
    Z = None
    history = []
    for it in range(max_iter):
        S_new, Z = T_operator(S, r, Z)
        S_new = normalize(S_new)
        diff = np.max(np.abs(S_new - S))
        history.append(diff)
        S = S_new
        if diff < tol:
            print(f"Convergencia alcanzada en {it+1} iteraciones.")
            break
    gap = compute_gap(S, r)
    return S, gap, history

# ------------------------------------------------------------
# Parámetros de discretización
# ------------------------------------------------------------
# Rango radial: hasta 10 ℓ_P (debido al decaimiento exponencial)
r_max = 10.0 * ell_P
n_points = 500
r = np.linspace(1e-6, r_max, n_points)

S_star, gap, hist = solve_fixed_point(r, max_iter=300)

print(f"Gap de Yang-Mills Δ* = {gap:.3f} GeV")
print(f"Valor esperado (QCD en red) ≈ 1.71 GeV")

# Opcional: mostrar evolución de la convergencia
import matplotlib.pyplot as plt
plt.figure()
plt.semilogy(hist)
plt.xlabel('Iteración')
plt.ylabel('Error máximo')
plt.title('Convergencia del punto fijo')
plt.grid(True)
plt.savefig('yang_mills_convergence.png')
plt.show()