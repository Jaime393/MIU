import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
args = parser.parse_args()

df = pd.read_csv(args.input)
vals = df['value'].values # usa 'value' no 'DBD_g_cm3'
vals = vals[vals > 0]

# Box-counting para D_f
def box_count_2d(coords, box_sizes):
    counts = []
    for size in box_sizes:
        x_bins = np.floor(coords[:,0] / size).astype(int)
        y_bins = np.floor(coords[:,1] / size).astype(int)
        boxes = set(zip(x_bins, y_bins))
        counts.append(len(boxes))
    return counts

coords = df[['x','y']].values
box_sizes = np.logspace(0.5, 2.5, 10)
counts = box_count_2d(coords, box_sizes)

coeffs = np.polyfit(np.log(1/box_sizes), np.log(counts), 1)
D_f = coeffs[0]

print(f"Variable: FIRMS_FRP_MW")
print(f"Puntos: {len(vals)}")
print(f"FRP min/max: {vals.min():.1f} / {vals.max():.1f} MW")
print(f"D_f fractal incendios: {D_f:.3f}")
print(f"K_i recomendado: 0.375")

out = pd.DataFrame({
    'Variable': ['FIRMS_FRP_MW'],
    'D_f': [D_f],
    'K_i': [0.375],
    'Source': ['FIRMS Raster TIF'],
    'DOI_URL': ['NASA FIRMS 2025']
})
out.to_csv('nodos/clima/firms_df_Ki.csv', index=False)
print("Guardado: nodos/clima/firms_df_Ki.csv")