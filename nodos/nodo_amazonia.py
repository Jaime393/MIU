"""
NODO BIOFÍSICO #25 — AMAZONIA (DETER/INPE)
===========================================
Calcula la dimensionalidad fractal (D_f) de las alertas de deforestación
en tiempo real usando la API pública de INPE/DETER (TerraBrasilis).

Métrica MIU: K_i = φ⁻¹ · (D_f / 2.5) · (ℓ_corr / ℓ_0)
Umbral de colapso: K_i < 0.3

Fuente: https://terrabrasilis.dpi.inpe.br/api/v1/deforestation/deter
"""

import requests
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
import math

# Constantes MIU
PHI_INV = 0.6180339887498948  # φ⁻¹
L0 = 1.0  # escala de referencia (km)

class NodoAmazonia:
    """Calcula K_i para el bioma amazónico usando datos DETER/INPE."""

    def __init__(self, cache_dir="cache_amazonia"):
        self.base_url = "https://terrabrasilis.dpi.inpe.br/api/v1/deforestation/deter"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def fetch_alerts(self, days=30, uf=None):
        """Descarga alertas recientes de deforestación."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
        }
        if uf:
            params["uf"] = uf

        cache_file = self.cache_dir / f"alerts_{start_date.date()}_{end_date.date()}.json"

        if cache_file.exists():
            print(f"[Nodo Amazonia] Usando caché: {cache_file}")
            return json.loads(cache_file.read_text())

        print(f"[Nodo Amazonia] Descargando alertas {start_date.date()} → {end_date.date()}...")
        try:
            resp = requests.get(f"{self.base_url}/alerts", params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            cache_file.write_text(json.dumps(data))
            print(f"[Nodo Amazonia] {len(data)} alertas descargadas.")
            return data
        except Exception as e:
            print(f"[Nodo Amazonia] Error API: {e}")
            return []

    def box_counting_dimension(self, points, box_sizes=None):
        """
        Calcula D_f mediante box-counting sobre coordenadas de alertas.

        Args:
            points: array (N, 2) de (lat, lon)
            box_sizes: lista de tamaños de caja en grados

        Returns:
            D_f: dimensionalidad fractal estimada
            r2: R² del ajuste lineal
        """
        if len(points) < 10:
            return None, 0.0

        if box_sizes is None:
            # Escalas logarítmicas: desde 0.01° hasta 10°
            box_sizes = np.logspace(-2, 1, 20)

        lats = np.array([p[0] for p in points])
        lons = np.array([p[1] for p in points])

        lat_range = lats.max() - lats.min()
        lon_range = lons.max() - lons.min()

        counts = []
        for bs in box_sizes:
            if bs > max(lat_range, lon_range) * 2:
                continue
            lat_bins = max(1, int(lat_range / bs))
            lon_bins = max(1, int(lon_range / bs))

            # Contar cajas ocupadas
            lat_idx = np.floor((lats - lats.min()) / bs).astype(int)
            lon_idx = np.floor((lons - lons.min()) / bs).astype(int)

            # Limitar índices
            lat_idx = np.clip(lat_idx, 0, lat_bins - 1)
            lon_idx = np.clip(lon_idx, 0, lon_bins - 1)

            boxes = set(zip(lat_idx, lon_idx))
            counts.append(len(boxes))

        if len(counts) < 4:
            return None, 0.0

        # Regresión lineal: log(N) = -D_f * log(ε) + C
        valid_sizes = [bs for bs in box_sizes[:len(counts)]]
        log_eps = np.log(1.0 / np.array(valid_sizes))
        log_N = np.log(np.array(counts))

        coeffs = np.polyfit(log_eps, log_N, 1)
        D_f = coeffs[0]

        # R²
        predicted = np.polyval(coeffs, log_eps)
        ss_res = np.sum((log_N - predicted) ** 2)
        ss_tot = np.sum((log_N - np.mean(log_N)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return D_f, r2

    def calcular_K_i(self, days=30):
        """Calcula K_i para la Amazonia usando datos recientes."""
        alerts = self.fetch_alerts(days=days)

        if not alerts:
            return {"K_i": None, "D_f": None, "status": "SIN_DATOS"}

        # Extraer coordenadas (centroides de geometrías o lat/lon si disponible)
        points = []
        total_area_km2 = 0
        municipios = set()

        for alert in alerts:
            # Intentar extraer coordenadas
            lat = alert.get("lat") or alert.get("latitude")
            lon = alert.get("lon") or alert.get("longitude")

            if lat and lon:
                points.append((float(lat), float(lon)))
            elif "geometry" in alert:
                # Si hay geometría, usar el centroide aproximado
                try:
                    geom = alert["geometry"]
                    if "coordinates" in geom:
                        coords = geom["coordinates"]
                        if isinstance(coords[0], list):
                            # Polígono: calcular centroide
                            flat = []
                            for ring in coords:
                                flat.extend(ring)
                            lats = [c[1] for c in flat]
                            lons = [c[0] for c in flat]
                            points.append((np.mean(lats), np.mean(lons)))
                except:
                    pass

            area = alert.get("area_km2") or alert.get("area_ha", 0) / 100
            total_area_km2 += float(area) if area else 0

            mun = alert.get("municipio") or alert.get("municipality")
            if mun:
                municipios.add(mun)

        if len(points) < 10:
            return {
                "K_i": None, "D_f": None,
                "total_area_km2": total_area_km2,
                "n_alertas": len(alerts),
                "n_municipios": len(municipios),
                "status": "POCOS_DATOS",
                "mensaje": f"Solo {len(points)} puntos con coordenadas. Se necesitan ≥10."
            }

        D_f, r2 = self.box_counting_dimension(points)

        if D_f is None:
            return {
                "K_i": None, "D_f": None,
                "total_area_km2": total_area_km2,
                "n_alertas": len(alerts),
                "status": "ERROR_CALCULO"
            }

        # Calcular longitud de correlación como radio del cluster
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        centroid = (np.mean(lats), np.mean(lons))
        distances = [math.sqrt((p[0]-centroid[0])**2 + (p[1]-centroid[1])**2) for p in points]
        l_corr = np.std(distances) * 2  # 2σ como escala de correlación (en grados)
        l_corr_km = l_corr * 111.32  # convertir grados a km (aproximado)

        # K_i = φ⁻¹ · (D_f / 2.5) · (ℓ_corr / ℓ_0)
        K_i = PHI_INV * (D_f / 2.5) * (l_corr_km / L0)

        # Determinar banda
        if K_i >= 0.88: banda = "ORO"
        elif K_i >= 0.75: banda = "VERDE"
        elif K_i >= 0.60: banda = "AMARILLO"
        elif K_i >= 0.40: banda = "ROJO"
        else: banda = "NEGRO — COLAPSO ECOLÓGICO INMINENTE"

        resultado = {
            "K_i": round(K_i, 4),
            "banda": banda,
            "D_f": round(D_f, 4),
            "r2_box_counting": round(r2, 4),
            "l_corr_km": round(l_corr_km, 2),
            "total_area_km2": round(total_area_km2, 2),
            "n_alertas": len(alerts),
            "n_municipios": len(municipios),
            "periodo_dias": days,
            "status": "OK",
            "timestamp": datetime.now().isoformat()
        }

        return resultado

# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================
if __name__ == "__main__":
    nodo = NodoAmazonia()

    # Calcular K_i para últimos 30, 90 y 365 días
    for periodo in [30, 90]:
        print(f"
{'='*60}")
        print(f"Calculando K_i Amazonia — período: {periodo} días")
        print(f"{'='*60}")
        resultado = nodo.calcular_K_i(days=periodo)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

        if resultado["status"] == "OK":
            print(f"
🌳 K_i Amazonia = {resultado['K_i']} ({resultado['banda']})")
            print(f"   D_f = {resultado['D_f']} (R² = {resultado['r2_box_counting']})")
            if resultado["K_i"] < 0.3:
                print("   ⚠️  ALERTA: COLAPSO ECOLÓGICO INMINENTE")
