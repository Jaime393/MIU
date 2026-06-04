#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver de solitones informacionales en 3D con simetría esférica.
Resuelve la ecuación de Klein-Gordon no lineal con potencial logarítmico.
Método de disparo (shooting).
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
from miu_constants import *

def rhs(r, y, alpha, u_star):
    """
    Sistema de primer orden:
    y[0] = u
    y[1] = du/dr
    """
    u, up = y
    if r < 1e-12:
        return [up, 0.0]  # evitar singularidad
    dupdr = -2.0/r * up - 2.0*alpha*u*(1.0 + np.log(u*u/(u_star*u_star) + 1e-12))
    return [up, dupdr]

def shoot(u0, r_max=20.0, n_points=1000, alpha=alpha_log, u_star=1.0):
    """Integra desde r=0 hasta r_max con condición inicial u(0)=u0, u'(0)=0."""
    r_span = (1e-6, r_max)
    r_eval = np.linspace(1e-6, r_max, n_points)
    sol = solve_ivp(rhs, r_span, [u0, 0.0], t_eval=r_eval, args=(alpha, u_star),
                    method='RK45', rtol=1e-8, atol=1e-10)
    if not sol.success:
        return np.inf
    return sol.y[0, -1]  # valor en r_max

def find_u0(alpha=alpha_log, u_star=1.0, bracket=(0.1, 1.0), r_max=20.0):
    """Encuentra u(0) tal que u(r_max) sea aproximadamente cero."""
    def f(u0):
        return shoot(u0, r_max=r_max, alpha=alpha, u_star=u_star)
    sol = root_scalar(f, bracket=bracket, method='brentq', xtol=1e-8)
    return sol.root

def solve_soliton(alpha=alpha_log, u_star=1.0, r_max=20.0, n_points=1000):
    u0 = find_u0(alpha, u_star, bracket=(0.1, 1.0), r_max=r_max)
    r = np.linspace(1e-6, r_max, n_points)
    sol = solve_ivp(rhs, (1e-6, r_max), [u0, 0.0], t_eval=r,
                    args=(alpha, u_star), method='RK45', rtol=1e-8, atol=1e-10)
    return sol.t, sol.y[0]

def compute_entropy(u, r):
    """Calcula la entropía de Shannon S = -∫ ρ ln ρ dV, con ρ = u^2."""
    dr = r[1] - r[0]
    rho = u**2
    integrand = r**2 * rho * np.log(rho + 1e-12)
    S = -4.0 * np.pi * np.trapz(integrand, dx=dr)
    return S

def compute_mass(u, r, alpha=alpha_log, u_star=1.0):
    """Calcula la masa del solitón a partir de la densidad de energía."""
    dr = r[1] - r[0]
    du = np.gradient(u, dr)
    V = alpha * u**2 * np.log(u**2/(u_star**2) + 1e-12)
    energy_density = 0.5 * du**2 + V
    integrand = r**2 * energy_density
    m = 4.0 * np.pi * np.trapz(integrand, dx=dr)
    # Convertir a GeV (1 J = 6.242e9 GeV)
    m_GeV = m * 6.242e9
    return m_GeV

if __name__ == "__main__":
    print("Resolviendo solitón con potencial logarítmico...")
    r, u = solve_soliton(alpha=alpha_log, u_star=1.0, r_max=20.0, n_points=1000)
    S = compute_entropy(u, r)
    m_GeV = compute_mass(u, r, alpha=alpha_log, u_star=1.0)
    print(f"Entropía S = {S:.2f} nats")
    print(f"Masa predicha (sin ajuste) = {m_GeV:.3e} GeV")
    print(f"Masa del electrón (referencia) = {0.511e-3} GeV")
    plt.figure()
    plt.plot(r, u)
    plt.xlabel('r (unidades arbitrarias)')
    plt.ylabel('u(r)')
    plt.title('Perfil del solitón')
    plt.grid(True)
    plt.savefig('soliton_profile.png')
    plt.show()
