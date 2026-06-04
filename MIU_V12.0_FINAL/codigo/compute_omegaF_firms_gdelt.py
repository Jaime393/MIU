#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.signal import welch
import sys

OmegaF = 0.65048305

def detect_fs(df):
    """Detecta frecuencia muestreo: mensual=12, anual=1"""
    cols = df.columns.str.lower().tolist()

    # Si hay columna Month/Mes → mensual
    if 'month' in cols or 'mes' in cols:
        return 12.0

    # Si solo hay Year y >100 filas → asume mensual CO2
    if 'year' in cols and len(df) > 100:
        return 12.0

    # Si años van de 1 en 1 → anual
    if 'year' in cols:
        years = df['Year'].values
        if len(years) > 1 and np.median(np.diff(years)) == 1:
            return 1.0

    return 1.0

def detect_column(df):
    cols = df.columns.str.lower().tolist()
    for name in ["fire_count", "count", "value", "bright_ti4", "frp", "confidence"]:
        if name in cols:
            return df.columns[cols.index(name)]
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            return col
    raise ValueError("No hay columna numérica")

def compute_fft_peak(csv_file):
    df = pd.read_csv(csv_file)
    col = detect_column(df)
    fs = detect_fs(df)
    print(f"Usando columna: '{col}' | fs={fs} muestras/año")

    data = df[col].values
    data = data - np.mean(data)

    n = len(data)
    if n < 8:
        print(f"Error: Solo {n} datos. Necesitas mínimo 8.")
        return None

    nperseg = min(256, n//2, n-1)
    f, Pxx = welch(data, fs=fs, nperseg=nperseg, noverlap=nperseg//2)

    idx = np.argmin(np.abs(f - OmegaF))
    peak_freq = f[idx]
    peak_power = Pxx[idx]

    print(f"Archivo: {csv_file}")
    print(f"Datos usados: {n} puntos")
    print(f"Frecuencia pico: {peak_freq:.6f} Hz")
    print(f"Ω_F objetivo: {OmegaF:.8f} Hz")
    print(f"Diferencia: {abs(peak_freq - OmegaF):.6f} Hz")
    print(f"Potencia pico: {peak_power:.4f}")

    if abs(peak_freq - OmegaF) < 0.05:
        print("✓ Latido planetario Ω_F detectado")
    else:
        print("× Ω_F no detectado. Revisa fs o datos.")

    return peak_freq

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python compute_omegaF_firms_gdelt.py archivo.csv")
        exit(1)
    compute_fft_peak(sys.argv[1])