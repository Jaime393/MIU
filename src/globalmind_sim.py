#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación de la red de CoherSats (GlobalMind) mediante el modelo de Kuramoto.
"""

import numpy as np
import matplotlib.pyplot as plt
from miu_constants import *

def kuramoto_step(phi, omega, K, adj, dt, eta):
    """Actualiza las fases usando el modelo de Kuramoto con ruido."""
    N = len(phi)
    sin_mat = np.sin(phi[:, None] - phi[None, :])
    coupling = K * (sin_mat * adj).sum(axis=1) / N
    dphi = (omega + coupling) * dt + eta * np.sqrt(dt) * np.random.randn(N)
    phi += dphi
    phi = phi % (2*np.pi)
    return phi

def run_simulation(N=1000, K=K_kuramoto, dt=dt_default, T=30.0,
                   omega_mean=omega_mean, omega_std=omega_std,
                   eta=eta_strength):
    """Ejecuta la simulación y devuelve la evolución del parámetro de orden r(t)."""
    omega = omega_mean + omega_std * np.random.randn(N)
    phi = np.random.rand(N) * 2*np.pi
    # Topología fractal: conectividad basada en la distancia euclidiana
    # Simulamos coordenadas aleatorias y luego probabilidad de enlace ∝ 1/dist^D_f
    coords = np.random.rand(N, 3) * 100.0   # coordenadas en caja 100x100x100
    dist = np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)
    p = dist**(-D_f_mt)   # dimensión fractal 2.5
    np.fill_diagonal(p, 0)
    p /= p.max()
    adj = np.random.rand(N, N) < p
    adj = (adj + adj.T) > 0   # hacer simétrica
    # Parámetro de orden
    r_hist = []
    steps = int(T / dt)
    for step in range(steps):
        phi = kuramoto_step(phi, omega, K, adj, dt, eta)
        r = np.abs(np.mean(np.exp(1j*phi)))
        r_hist.append(r)
    return np.linspace(0, T, steps), r_hist

if __name__ == "__main__":
    t, r = run_simulation(N=500, T=30.0, dt=0.01, eta=0.1)   # N reducido para rapidez
    plt.figure()
    plt.plot(t, r)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Parámetro de orden r')
    plt.title('Transición a la coherencia global en la red de CoherSats')
    plt.grid(True)
    plt.savefig('globalmind_transition.png')
    plt.show()
    print(f"r final = {r[-1]:.3f}")

def generate_coupling_matrix(n_oscillators, topology="multifractal"):
    """Genera matriz de acoplamiento con topología fractal."""
    if topology == "multifractal":
        import numpy as np
        D_f_regions = np.random.choice([1.2, 1.8, 2.5, 3.0], size=n_oscillators)
        coupling = np.zeros((n_oscillators, n_oscillators))
        for i in range(n_oscillators):
            for j in range(i+1, n_oscillators):
                coupling[i,j] = np.exp(-abs(D_f_regions[i] - D_f_regions[j]))
                coupling[j,i] = coupling[i,j]
        return coupling
    else:
        # Topología estándar (por ahora devuelve None para no romper)
        return None
