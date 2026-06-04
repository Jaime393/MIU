#!/usr/bin/env python3
import numpy as np
import pandas as pd
import argparse

def box_counting_3d(dbd_array, scales=[1,2,4,8,16,32]):
    """Box-counting 3D para DBD WoSIS. dbd_array en g/cm3"""
    N = []
    for s in scales:
        # Binariza: suelo vs poro usando umbral DBD media
        threshold = np.mean(dbd_array)
        binary = (dbd_array > threshold).astype(int)
        # Cuenta cajas ocupadas
        shape = binary.shape
        n_boxes = 0
        for i in range(0, shape[0], s):
            for j in range(0, shape[1], s):
                for k in range(0, shape[2], s):
                    if np.any(binary[i:i+s, j:j+s, k:k+s]):
                        n_boxes += 1
        N.append(n_boxes)
    log_s = np.log(1/np.array(scales))
    log_N = np.log(N)
    D_f = -np.polyfit(log_s, log_N, 1)[0]
    return D_f

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula D_f desde CSV WoSIS DBD")
    parser.add_argument("--input", required=True, help="CSV WoSIS con columna DBD_g_cm3")
    parser.add_argument("--output", default="D_f_result.txt")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    dbd = df["DBD_g_cm3"].values
    # Simula 3D apilando valores si solo hay 1D
    if len(dbd) < 1000:
        dbd_3d = np.tile(dbd, (10,10,10))
    else:
        dbd_3d = dbd.reshape(-1,10,10)

    Df = box_counting_3d(dbd_3d)
    print(f"D_f calculado: {Df:.3f}")

    with open(args.output, 'w') as f:
        f.write(f"D_f = {Df:.4f}\n")
    print(f"Guardado en {args.output}")