#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_ift_solver.py – Pruebas unitarias para el IFT Solver y funciones asociadas.

Ejecutar: pytest test_ift_solver.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from src.ift_solver import InformationalField   # asumiendo que ift_solver.py está en src/
from src.phi_MIU import compute_phi, compute_rho_from_activity

# ------------------------------------------------------------
# Tests para ift_solver.py (clase InformationalField)
# ------------------------------------------------------------

def test_initialization():
    x = np.linspace(-10, 10, 100)
    field = InformationalField(x)
    assert field.x is x
    assert field.dx == x[1] - x[0]
    assert field.rho is None

def test_gaussian_initialization():
    x = np.linspace(-10, 10, 200)
    field = InformationalField(x)
    field.initialize_gaussian(sigma=0.5)
    assert field.rho is not None
    # La masa total debe ser 1 (normalización)
    total_mass = np.sum(field.rho) * field.dx
    assert np.isclose(total_mass, 1.0, atol=1e-6)

def test_deltaF_delta_rho():
    x = np.linspace(-5, 5, 50)
    field = InformationalField(x)
    field.initialize_gaussian(sigma=1.0)
    df = field.deltaF_delta_rho(alpha=0.1, u_star=1.0)
    assert len(df) == len(x)
    assert not np.any(np.isnan(df))

def test_evolution_conserves_mass():
    x = np.linspace(-10, 10, 200)
    field = InformationalField(x)
    field.initialize_gaussian(sigma=1.0)
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 20)
    times, rho_history = field.evolve(t_span, t_eval, alpha=0.1, u_star=1.0)
    # Verificar que la masa se conserva
    mass_initial = np.sum(field.rho) * field.dx
    for i in range(len(times)):
        mass = np.sum(rho_history[i]) * field.dx
        assert np.isclose(mass, mass_initial, atol=1e-6)

# ------------------------------------------------------------
# Tests para phi_MIU.py
# ------------------------------------------------------------

def test_phi_computation():
    np.random.seed(42)
    T, N = 500, 10
    activity = np.random.randn(T, N)
    coords = np.random.rand(N, 3)
    phi = compute_phi(activity, coords)
    assert isinstance(phi, float)
    assert phi >= 0.0   # debería ser no negativo

def test_rho_from_activity():
    T, N = 100, 5
    activity = np.random.randn(T, N)
    rho = compute_rho_from_activity(activity)
    assert rho.shape == (N,)
    assert np.isclose(np.sum(rho), 1.0)

# ------------------------------------------------------------
# Para ejecutar las pruebas manualmente (no necesario con pytest)
# ------------------------------------------------------------
if __name__ == "__main__":
    pytest.main([__file__])