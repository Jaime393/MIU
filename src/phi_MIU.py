#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
phi_MIU.py – Cálculo del funcional de conciencia integrada Φ_MIU.

Implementa la definición del Volumen III (Capítulo 1):
Φ_MIU = ∫[ρ ln(ρ/ρ_base) + ½ Tr(κ_F) + I_causal + α Σb_k + β c_1] dV

Dependencias: numpy, scipy (para homología persistente opcional).
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import laplacian
from scipy.linalg import eigh

# ------------------------------------------------------------
# 1. Funciones básicas para el campo ρ
# ------------------------------------------------------------

def compute_rho_from_activity(activity):
    """
    Estima la densidad informacional ρ a partir de actividad neuronal.
    activity: matriz de (tiempo, neuronas). Devuelve vector ρ normalizado.
    """
    rho = np.mean(activity, axis=0)
    rho = np.maximum(rho, 0)
    rho = rho / np.sum(rho)
    return rho

def compute_fisher_curvature(rho, coords, method='gradient'):
    """
    Calcula la curvatura de Fisher κ_F = ∇² ln ρ.
    method: 'gradient' (diferencias finitas) o 'laplacian' (matriz laplaciana).
    coords: coordenadas de los nodos (N, dim).
    """
    N = len(rho)
    if method == 'gradient' and coords is not None:
        # Estimación mediante gradiente en malla regular (simplificada)
        grad = np.gradient(np.log(rho + 1e-12))
        kappa = np.sum(np.gradient(grad), axis=0)
        return kappa
    else:
        # Usar la matriz laplaciana de un grafo de vecindad
        if coords is None:
            raise ValueError("Se necesitan coordenadas para el método laplaciano")
        # Construir grafo de vecindad basado en distancia euclídea
        dist = squareform(pdist(coords))
        sigma = np.median(dist[dist>0])   # escala típica
        W = np.exp(-dist**2 / (2*sigma**2))
        np.fill_diagonal(W, 0)
        L = laplacian(W, normed=False)
        # κ_F se aproxima por la traza del laplaciano aplicado a ln ρ
        ln_rho = np.log(rho + 1e-12)
        kappa = (L @ ln_rho) / (1 + 1e-12)
        return kappa

def compute_causal_info(activity, partition=None):
    """
    Estima I_causal como la información mutua mínima entre dos particiones.
    Por simplicidad, utiliza la información mutua entre dos mitades.
    """
    n_neurons = activity.shape[1]
    if partition is None:
        mid = n_neurons // 2
        part1 = slice(0, mid)
        part2 = slice(mid, n_neurons)
    else:
        part1, part2 = partition
    # Calcular información mutua entre las dos partes (suponiendo normalidad)
    # Método simplificado: correlación de Pearson
    corr = np.corrcoef(activity.mean(axis=0))[part1, part2]
    # Convertir a información mutua gaussiana: I = -0.5 log(1 - r²)
    # Tomamos el promedio de todas las combinaciones
    r_vals = corr.flatten()
    r_vals = r_vals[~np.isnan(r_vals)]
    if len(r_vals) == 0:
        return 0.0
    I = -0.5 * np.mean(np.log(1 - r_vals**2 + 1e-12))
    return max(I, 0.0)

def compute_betti(coords, radius=None):
    """
    Calcula los números de Betti b0, b1, b2 para un conjunto de puntos.
    Necesita la librería 'gudhi' o 'ripser'. Si no está instalada, devuelve valores dummy.
    """
    try:
        import gudhi
        rips = gudhi.RipsComplex(points=coords, max_edge_length=radius if radius else 1.0)
        simplex_tree = rips.create_simplex_tree(max_dimension=2)
        betti = simplex_tree.persistence()
        b0 = sum(1 for (dim, _) in betti if dim == 0)
        b1 = sum(1 for (dim, _) in betti if dim == 1)
        b2 = sum(1 for (dim, _) in betti if dim == 2)
        return b0, b1, b2
    except ImportError:
        # Fallback: estimación usando componentes conexas y ciclos simples
        # Este dummy no es riguroso; para fines ilustrativos.
        from scipy.sparse.csgraph import connected_components
        dist = squareform(pdist(coords))
        adj = (dist < 0.5).astype(int)
        n_components, _ = connected_components(adj, directed=False)
        b0 = n_components
        b1 = 0   # placeholder
        b2 = 0
        return b0, b1, b2

def compute_chern_class(xi_phase):
    """
    Estima la primera clase de Chern c₁(ξ) a partir de la fase Φ(x).
    xi_phase: matriz de fases (N,).
    c₁ ≈ (1/(2π)) ∮ dΦ = número de enrollamiento.
    """
    # Tomamos una aproximación simple: variación total de la fase dividida por 2π
    phase_diff = np.diff(xi_phase)
    total_variation = np.sum(np.abs(phase_diff))
    c1 = total_variation / (2 * np.pi)
    return c1

# ------------------------------------------------------------
# 2. Funcional Φ_MIU principal
# ------------------------------------------------------------

def compute_phi(activity, coords, rho_base=1e-3, alpha=0.1, beta=0.05):
    """
    Calcula Φ_MIU a partir de actividad neuronal y coordenadas de electrodos.
    activity : (n_tiempos, n_neuronas)
    coords   : (n_neuronas, dim) – coordenadas espaciales
    """
    rho = compute_rho_from_activity(activity)
    # Término informacional (divergencia KL)
    term_info = np.sum(rho * np.log(rho / (rho_base + 1e-12)))
    # Término geométrico (curvatura Fisher)
    kappa = compute_fisher_curvature(rho, coords)
    term_geom = 0.5 * np.mean(kappa)
    # Término causal
    I_causal = compute_causal_info(activity)
    # Términos topológicos
    b0, b1, b2 = compute_betti(coords)
    sum_betti = b0 + b1 + b2
    # Clase de Chern (necesita la fase ξ; aquí usamos una simulación)
    # En su lugar, simulamos una fase aleatoria para demo
    xi_phase = np.angle(np.fft.fft(activity.mean(axis=0)))
    c1 = compute_chern_class(xi_phase)
    term_top = alpha * sum_betti + beta * c1
    phi = term_info + term_geom + I_causal + term_top
    return phi

# ------------------------------------------------------------
# 3. Ejemplo de uso con datos simulados
# ------------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(42)
    # Simular 1000 instantes de tiempo, 20 neuronas
    T = 1000
    N = 20
    # Actividad coherente (oscilaciones gamma) para crear un estado consciente simulado
    t = np.linspace(0, 1, T)
    gamma = 40.0  # Hz
    signal = np.sin(2 * np.pi * gamma * t)[:, None]
    noise = 0.1 * np.random.randn(T, N)
    activity = signal + noise
    # Coordenadas aleatorias de las neuronas en 3D
    coords = np.random.rand(N, 3)
    phi_val = compute_phi(activity, coords)
    print(f"Φ_MIU (consciente simulado) = {phi_val:.4f}")
    # Ahora simular actividad incoherente (ruido puro)
    activity_incoh = np.random.randn(T, N)
    phi_val_incoh = compute_phi(activity_incoh, coords)
    print(f"Φ_MIU (incoherente) = {phi_val_incoh:.4f}")