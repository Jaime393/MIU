#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT Solver v3.0 – Simulación del Monismo Informacional Unificado
Autor: Juan Diego Vicente Gabancho (Arquitecto del MIU)
Licencia: IFT Open Source (https://creativecommons.org/licenses/by-sa/4.0/)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from miu_constants import *

class InformationalField:
    """
    Representa el campo ρ(x,t) en una malla unidimensional o bidimensional.
    """
    def __init__(self, x, y=None, rho0=None, dx=None, dy=None):
        self.x = x
        self.y = y
        self.dim = 1 if y is None else 2
        if self.dim == 1:
            self.nx = len(x)
            self.dx = dx if dx else x[1]-x[0]
        else:
            self.nx, self.ny = len(x), len(y)
            self.dx = dx if dx else x[1]-x[0]
            self.dy = dy if dy else y[1]-y[0]
        if rho0 is not None:
            self.rho = rho0.copy()
        else:
            self.initialize_uniform()

    def initialize_uniform(self, val=1.0):
        if self.dim == 1:
            self.rho = np.full(self.nx, val)
        else:
            self.rho = np.full((self.nx, self.ny), val)

    def initialize_gaussian(self, center=0.0, sigma=1.0):
        if self.dim == 1:
            self.rho = np.exp(-(self.x - center)**2 / (2*sigma**2))
        else:
            X, Y = np.meshgrid(self.x, self.y, indexing='ij')
            self.rho = np.exp(-((X - center)**2 + (Y - center)**2) / (2*sigma**2))
        # Normalizar masa total = 1
        if self.dim == 1:
            norm = np.sum(self.rho) * self.dx
        else:
            norm = np.sum(self.rho) * self.dx * self.dy
        self.rho /= norm

    def compute_phi(self):
        return np.log(self.rho + 1e-12)

    def compute_Xi(self):
        phi = self.compute_phi()
        if self.dim == 1:
            grad = np.gradient(phi, self.dx)
            Xi = np.abs(grad)
        else:
            grad_x = np.gradient(phi, self.dx, axis=0)
            grad_y = np.gradient(phi, self.dy, axis=1)
            Xi = np.sqrt(grad_x**2 + grad_y**2)
        return Xi

    def energy_free(self, V=None, alpha=alpha_log, u_star=1.0):
        # término cinético
        if self.dim == 1:
            grad = np.gradient(self.rho, self.dx)
            kinetic = 0.5 * np.sum(grad**2 / (self.rho + 1e-12)) * self.dx
        else:
            grad_x = np.gradient(self.rho, self.dx, axis=0)
            grad_y = np.gradient(self.rho, self.dy, axis=1)
            kinetic = 0.5 * np.sum((grad_x**2 + grad_y**2) / (self.rho + 1e-12)) * self.dx * self.dy
        if V is None:
            # potencial logarítmico V = α ρ² ln(ρ/u_star²)
            V_val = alpha * self.rho**2 * np.log(self.rho / u_star**2 + 1e-12)
            if self.dim == 1:
                pot = np.sum(V_val) * self.dx
            else:
                pot = np.sum(V_val) * self.dx * self.dy
        else:
            pot = np.sum(V(self.rho)) * self.dx * (self.dy if self.dim==2 else 1)
        return kinetic + pot

    def deltaF_delta_rho(self, alpha=alpha_log, u_star=1.0):
        # gradiente de la energía libre
        if self.dim == 1:
            grad = np.gradient(self.rho, self.dx)
            laplacian = np.gradient(grad, self.dx)
            grad2 = grad**2
        else:
            grad_x = np.gradient(self.rho, self.dx, axis=0)
            grad_y = np.gradient(self.rho, self.dy, axis=1)
            laplacian = np.gradient(grad_x, self.dx, axis=0) + np.gradient(grad_y, self.dy, axis=1)
            grad2 = grad_x**2 + grad_y**2
        term1 = -laplacian / (self.rho + 1e-12)
        term2 = -0.5 * grad2 / (self.rho**2 + 1e-12)
        term3 = 2*alpha*self.rho * (np.log(self.rho / u_star**2 + 1e-12) + 0.5)
        return term1 + term2 + term3

    def evolution(self, t, rho_vec, alpha=alpha_log, u_star=1.0, D=0.0):
        # Ecuación maestra: ∂ρ/∂t = -∇·J + η
        self.rho = rho_vec.reshape(self.rho.shape)
        deltaF = self.deltaF_delta_rho(alpha, u_star)
        if self.dim == 1:
            grad_deltaF = np.gradient(deltaF, self.dx)
            flux = self.rho * grad_deltaF
            drho_dt = -np.gradient(flux, self.dx)
        else:
            grad_deltaF_x = np.gradient(deltaF, self.dx, axis=0)
            grad_deltaF_y = np.gradient(deltaF, self.dy, axis=1)
            flux_x = self.rho * grad_deltaF_x
            flux_y = self.rho * grad_deltaF_y
            drho_dt = - (np.gradient(flux_x, self.dx, axis=0) + np.gradient(flux_y, self.dy, axis=1))
        # Ruido (si D>0)
        if D > 0:
            dt = t - getattr(self, '_last_t', t)
            if dt < 0:
                dt = 0.01  # valor por defecto
            noise = np.sqrt(2 * D * dt) * np.random.randn(*self.rho.shape)
            drho_dt += noise / dt
        self._last_t = t
        return drho_dt.flatten()

    def evolve(self, t_span, t_eval=None, alpha=alpha_log, u_star=1.0, D=0.0):
        rho0_vec = self.rho.flatten()
        def rhs(t, y):
            return self.evolution(t, y, alpha, u_star, D)
        sol = solve_ivp(rhs, t_span, rho0_vec, t_eval=t_eval, method='RK45')
        return sol.t, sol.y.reshape((len(sol.t),) + self.rho.shape)

    # Métodos complementarios
    def compute_kappa(self, tau):
        Xi = self.compute_Xi()
        kappa = tau * Xi * c
        return np.mean(kappa)

    def compute_Phi_MIU(self, rho_base=0.01, alpha_geom=1.0, alpha_causal=1.0):
        # Cálculo simplificado del funcional de conciencia
        term_info = np.sum(self.rho * np.log(self.rho / (rho_base + 1e-12))) * self.dx * (self.dy if self.dim==2 else 1)
        # curvatura de Fisher (laplaciano de log rho)
        if self.dim == 1:
            kappa_F = np.gradient(np.gradient(np.log(self.rho + 1e-12), self.dx), self.dx)
        else:
            logrho = np.log(self.rho + 1e-12)
            kappa_F = np.gradient(np.gradient(logrho, self.dx, axis=0), self.dx, axis=0) + \
                      np.gradient(np.gradient(logrho, self.dy, axis=1), self.dy, axis=1)
        term_geom = 0.5 * np.mean(kappa_F) * self.dx * (self.dy if self.dim==2 else 1)
        # Término causal (aproximación por información mutua de particiones)
        # Versión simplificada:
        if self.dim == 1:
            mid = self.nx // 2
            rhoA = self.rho[:mid]
            rhoB = self.rho[mid:]
            pA = np.sum(rhoA) * self.dx
            pB = np.sum(rhoB) * self.dx
            I_causal = pA * np.log(pA + 1e-12) + pB * np.log(pB + 1e-12) - (pA+pB)*np.log(pA+pB+1e-12)
        else:
            # Partición 2x2 (simplificada)
            hx = self.nx//2
            hy = self.ny//2
            rhoA = self.rho[:hx, :hy]
            rhoB = self.rho[:hx, hy:]
            rhoC = self.rho[hx:, :hy]
            rhoD = self.rho[hx:, hy:]
            def entropy(r):
                return -np.sum(r * np.log(r + 1e-12)) * self.dx * self.dy
            S_total = entropy(self.rho)
            S_A = entropy(rhoA)
            S_B = entropy(rhoB)
            S_C = entropy(rhoC)
            S_D = entropy(rhoD)
            I_causal = (S_A + S_B + S_C + S_D - S_total) / 4
        return term_info + alpha_geom * term_geom + alpha_causal * I_causal

# Ejemplo de uso (solitón 1D)

        """Inicializa el campo rho con un espectro multifractal."""
        pass  # TODO: implementar

        """
        Inicializa el campo rho con un espectro multifractal.
        Ref: García-Bellido, arXiv:2605.21554 (mayo 2026)
        """
        D_f_map = {
            "clusters": 1.2,
            "filaments": 1.8,
            "walls": 2.5,
            "voids": 3.0
        }
        for component in components:
            D_f = D_f_map.get(component, 2.0)
            mask = self._get_morphological_mask(component)
            self.rho[mask] = self._generate_fractal_noise(D_f, size=mask.sum())
        self._compute_multifractal_coupling()

    def initialize_multifractal(self, components=["filaments", "walls", "clusters", "voids"]):
        """Inicializa el campo rho con un espectro multifractal."""
        pass  # TODO: implementar
if __name__ == "__main__":
    x = np.linspace(-10, 10, 200)
    field = InformationalField(x)
    field.initialize_gaussian(sigma=0.5)
    t_span = (0, 50)
    t_eval = np.linspace(0, 50, 100)
    times, rho_history = field.evolve(t_span, t_eval, alpha=alpha_log, u_star=1.0, D=0.0)
    plt.figure()
    for i, t in enumerate(times[::10]):
        plt.plot(x, rho_history[i], label=f't={t:.1f}')
    plt.xlabel('x')
    plt.ylabel(r'$\rho(x,t)$')
    plt.title('Evolución de un solitón informacional')
    plt.legend()
    plt.savefig('soliton_evolution.png')
    plt.show()
