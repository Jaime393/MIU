#!/usr/bin/env python3
import numpy as np
import pandas as pd
import argparse

phi = 0.6180339887498949

def load_all_nodes(base_dir="nodos"):
    """Carga todos los CSV y extrae D_f, K_i"""
    import glob, os
    csv_files = glob.glob(f"{base_dir}/**/*.csv", recursive=True)
    Df_list, Ki_list = [], []

    for f in csv_files:
        try:
            df = pd.read_csv(f)
            if "D_f" in df.columns and "K_i" in df.columns:
                Df_list.extend(df["D_f"].dropna().values)
                Ki_list.extend(df["K_i"].dropna().values)
        except:
            pass
    return np.array(Df_list), np.array(Ki_list)

def randomization_test(Df, Ki, n_perm=100000):
    """Test permutaciones para descartar azar"""
    slopes = []
    for i in range(n_perm):
        Ki_shuffled = np.random.permutation(Ki)
        slope = np.polyfit(Df, Ki_shuffled, 1)[0]
        slopes.append(slope)

    slope_real = np.polyfit(Df, Ki, 1)[0]
    slope_theory = phi / 2.5

    p_value = np.mean(np.array(slopes) >= slope_real)
    R2 = np.corrcoef(Df, Ki)[0,1]**2

    print(f"Pendiente real: {slope_real:.6f}")
    print(f"Pendiente teórica φ/2.5: {slope_theory:.6f}")
    print(f"R²: {R2:.4f}")
    print(f"p-valor permutaciones: {p_value:.2e}")
    print(f"Nodos: {len(Df)}")

    if p_value < 1e-48:
        print("✓ Ley K_i validada. No es azar.")
    return R2, p_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_permutations", type=int, default=100000)
    args = parser.parse_args()

    Df, Ki = load_all_nodes()
    if len(Df) == 0:
        print("Error: No hay datos D_f/K_i en /nodos/")
        exit(1)

    randomization_test(Df, Ki, args.n_permutations)