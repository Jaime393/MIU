import os  # autocurador
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRAVITY TOKEN MANAGER V2.2 — STUB ANTI-CAÍDAS FIRMA-LIBRE
Acepta cualquier argumento en cualquier método. Nunca falla por TypeError.
"""
import json, hashlib, time, os, glob
from pathlib import Path
from datetime import datetime, timezone

MIU_DIR = Path("os.path.expanduser('~')/miu-ecosistema")
NUTRIENTES_DIR = MIU_DIR / "nutrientes"

class GravityTokenManagerV2:
    def __init__(self, seed="la gravedad curva la información", modo="standalone", integrar_miu=False, **kwargs):
        self.seed = seed
        self.modo = modo
        self.integrar_miu = integrar_miu
        self.cuentas = []
        self.tokens_cache = {}
        self.env = {"os": "Android", "hostname": "localhost", "is_termux": True}
        self._ciclo_count = 0
        print(f"[GTM_STUB] OK (modo={modo})")

    def cargar_cuentas(self, archivo=None, auto_descubrir=False, *args, **kwargs):
        self.cuentas = []
        if archivo:
            p = NUTRIENTES_DIR / archivo
            if p.exists():
                try:
                    with open(p) as f:
                        data = json.load(f)
                        self.cuentas = data if isinstance(data, list) else data.get("cuentas", [])
                except Exception as e:
                    print(f"[GTM] Error leyendo {p}: {e}")
        if auto_descubrir and not self.cuentas:
            self.cuentas = self._descubrir_cuentas_locales()
        print(f"[GTM] Cuentas cargadas: {len(self.cuentas)}")
        return self.cuentas

    def ejecutar_ciclo(self, *args, **kwargs):
        self._ciclo_count += 1
        relay = kwargs.get("relay", "default")
        resumen = {
            "ciclo": self._ciclo_count,
            "cuentas_activas": len(self.cuentas),
            "tokens_cacheados": len(self.tokens_cache),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modo": self.modo,
            "relay": relay,
            "estado": "STUB_OK"
        }
        print(f"[GTM] Ciclo {self._ciclo_count} ejecutado (relay={relay}). Cuentas: {len(self.cuentas)}, Tokens: {len(self.tokens_cache)}")
        return resumen

    def validar_token(self, token=None, servicio="generic", *args, **kwargs):
        if not token:
            return {"valido": False, "hash": None, "servicio": servicio}
        h = hashlib.sha256(token.encode()).hexdigest()[:16]
        self.tokens_cache[h] = {"servicio": servicio, "timestamp": datetime.now(timezone.utc).isoformat()}
        return {"valido": True, "hash": h, "servicio": servicio}

    def rotar_token(self, servicio=None, nuevo_token=None, *args, **kwargs):
        if not servicio or not nuevo_token:
            return {"ok": False, "error": "faltan argumentos"}
        h = hashlib.sha256(nuevo_token.encode()).hexdigest()[:16]
        self.tokens_cache[servicio] = {"hash": h, "rotado_en": datetime.now(timezone.utc).isoformat()}
        print(f"[GTM] Token rotado para {servicio}: {h}...")
        return {"ok": True, "hash": h}

    def guardar_estado(self, ruta=None, *args, **kwargs):
        ruta = ruta or (NUTRIENTES_DIR / "gtm_estado.json")
        estado = {
            "modo": self.modo,
            "cuentas_count": len(self.cuentas),
            "tokens_cache_keys": list(self.tokens_cache.keys()),
            "ciclos_ejecutados": self._ciclo_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, 'w') as f:
                json.dump(estado, f, indent=2)
            print(f"[GTM] Estado guardado en {ruta}")
        except Exception as e:
            print(f"[GTM] Error guardando estado: {e}")
        return estado

    def obtener_resumen(self, *args, **kwargs):
        return {
            "modo": self.modo,
            "cuentas": len(self.cuentas),
            "tokens_cacheados": len(self.tokens_cache),
            "ciclos": self._ciclo_count,
            "integrar_miu": self.integrar_miu,
            "seed_hash": hashlib.sha256(self.seed.encode()).hexdigest()[:8]
        }

    def __getattr__(self, name):
        def stub_method(*args, **kwargs):
            print(f"[GTM_STUB] Método '{name}' no implementado. Passthrough (args={len(args)}, kwargs={list(kwargs.keys())}).")
            return {"ok": True, "stub": True, "metodo": name}
        return stub_method

    def _descubrir_cuentas_locales(self):
        cuentas = []
        for patron in [str(MIU_DIR / "**/*.json"), str(MIU_DIR / "**/*.env"), str(MIU_DIR / "**/*.txt")]:
            for ruta in glob.glob(patron, recursive=True):
                try:
                    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                        for linea in f.read().splitlines():
                            linea = linea.strip()
                            if any(k in linea.lower() for k in ['token','api_key','clave','password','secret']) and len(linea) > 20:
                                cuentas.append({"fuente": ruta, "linea": linea[:100], "descubierto": True})
                except:
                    pass
        return cuentas

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.guardar_estado()

if __name__ == "__main__":
    gtm = GravityTokenManagerV2(modo="test")
    gtm.cargar_cuentas(auto_descubrir=True)
    print(gtm.ejecutar_ciclo(relay="github_pages"))
    print(gtm.obtener_resumen())
