#!/usr/bin/env python3
import numpy as np
import pandas as pd
import argparse

phi = 0.6180339887498949

def dfa_fluctuation(series):
    """Detrended Fluctuation Analysis para estimar D_f temporal"""
    series = np.array(series) - np.mean(series)
    y = np.cumsum(series)
    scales = np.logspace(1, np.log10(len(y)//4), 20).astype(int)
    F = []
    for s in scales:
        rms = []
        for i in range(0, len(y), s):
            segment = y[i:i+s]
            if len(segment) < s: continue
            t = np.arange(len(segment))
            p = np.polyfit(t, segment, 1)
            fit = np.polyval(p, t)
            rms.append(np.sqrt(np.mean((segment - fit)**2)))
        F.append(np.mean(rms))
    log_s = np.log(scales[:len(F)])
    log_F = np.log(F)
    alpha = np.polyfit(log_s, log_F, 1)[0]
    D_f = 2 - alpha # Relación DFA fractal
    return D_f

def compute_Ki(D_f, ell_corr=0.5, ell_0=0.5):
    """Ley K_i Universal"""
    return phi * (D_f / 2.5) * (ell_corr / ell_0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula K_i desde series temporales")
    parser.add_argument("--input", required=True, help="CSV con columna Value o CO2_ppm")
    parser.add_argument("--col", default="Value", help="Nombre columna datos")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    data = df[args.col].values

    Df = dfa_fluctuation(data)
    Ki = compute_Ki(Df)

    print(f"D_f: {Df:.3f}")
    print(f"K_i ley: {Ki:.4f}")
    print(f"K_i medido esperado: {Ki:.3f}")