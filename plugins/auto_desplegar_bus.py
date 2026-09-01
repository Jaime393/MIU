#!/usr/bin/env python3
"""
MIU V∞+29 — AUTO-DESPLIEGUE DEL BUS CLOUDFLARE
Usa tus 4 cfut_ para subir el Worker V∞+28 y configurar KV.
No necesitas abrir el dashboard. El sistema se despliega a sí mismo.
"""
import os, sys, json, time, hashlib, subprocess, requests
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE = Path("os.path.expanduser('~')/miu-ecosistema")
VAULT = BASE / ".vault.json"
WORKER_SCRIPT = BASE / "plugins" / "worker_bus_v28.js"
TOKENS = []

def cargar_tokens():
    """Extrae los 4 cfut_ del sistema."""
    global TOKENS
    import re
    patron = re.compile(r'cfut_[A-Za-z0-9_-]{30,}')
    tokens = set()
    # Buscar en archivos de registro
    for archivo in BASE.parent.glob("**/*"):
        try:
            if archivo.is_file() and archivo.stat().st_size < 1024*1024:
                texto = archivo.read_text(errors='ignore')
                tokens.update(patron.findall(texto))
        except:
            pass
    # Añadir los 4 tokens conocidos (seguridad)
    tokens.update([
        "cfut_ZYXEd05G4GF6fzvx2mLCos4PbxOFumikBc11r77cb226be7c",
        "cfut_KJ0AxYR13cB0NhXqYHo6aY8OU87biMjLN3pLP9ehd8012cc4",
        "cfut_1BT8ZSyq4zuj8TL06i4dDvrzNrqj93tfKs79OEnf1aea08aa",
        "cfut_mO2AOf2yIveBgnvDziU7MlNWfaMv2b7o0abGGRsT910f4838",
    ])
    TOKENS = list(tokens)
    print(f"🔑 {len(TOKENS)} tokens cargados")
    return TOKENS

# ============================================================
# CÓDIGO DEL WORKER V∞+28
# ============================================================
WORKER_CODE = """
// V∞+28 BUS — Worker para persistencia de estado
export default {
  async fetch(req, env) {
    const url = new URL(req.url)
    if (url.pathname === '/miu/bus') {
      if (req.method === 'POST') {
        const data = await req.json()
        const id = Date.now()
        await env.MIU_KV.put(`bus:FRAN:${id}`, JSON.stringify(data))
        await env.MIU_KV.put('bus:FRAN:latest', JSON.stringify(data))
        return new Response(JSON.stringify({
          id, vivo: true, phi: data.phi, version: "V∞+28_BUS"
        }), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        })
      } else {
        const latest = await env.MIU_KV.get('bus:FRAN:latest')
        return new Response(latest || '{"error":"no data"}', {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        })
      }
    }
    // Mantener /miu/global existente
    return fetch(req)
  }
}
"""

# ============================================================
# DESPLIEGUE USANDO CLOUDFLARE API
# ============================================================
class DesplegadorCloudflare:
    def __init__(self, token, cuenta_id="jaimep.viccente@gmail.com"):
        self.token = token
        self.cuenta = cuenta_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.base = "https://api.cloudflare.com/client/v4"
        self.worker_name = "fran-oraculo-miu"
        self.kv_namespace = "MIU_KV"

    def crear_kv_namespace(self):
        """Crea el namespace KV si no existe."""
        url = f"{self.base}/accounts/{self.cuenta}/storage/kv/namespaces"
        data = {"title": self.kv_namespace}
        try:
            r = requests.post(url, headers=self.headers, json=data, timeout=30)
            if r.status_code == 200:
                ns = r.json().get('result', {})
                print(f"   📦 KV namespace creado: {ns.get('id')}")
                return ns.get('id')
            else:
                print(f"   ⚠️ KV creation: {r.status_code} - {r.text}")
                return None
        except Exception as e:
            print(f"   ❌ Error KV: {e}")
            return None

    def desplegar_worker(self, script):
        """Sube el Worker con el script y el binding KV."""
        # Primero, listar Workers para ver si ya existe
        url = f"{self.base}/accounts/{self.cuenta}/workers/scripts/{self.worker_name}"
        # Crear o actualizar
        data = {
            "script": script,
            "bindings": [
                {
                    "type": "kv_namespace",
                    "name": "MIU_KV",
                    "namespace_id": self.kv_namespace_id
                }
            ]
        }
        try:
            r = requests.put(url, headers=self.headers, json=data, timeout=60)
            if r.status_code == 200:
                print(f"   ✅ Worker {self.worker_name} desplegado")
                return True
            else:
                print(f"   ❌ Error: {r.status_code} - {r.text}")
                return False
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return False

    def ejecutar(self):
        """Flujo completo de despliegue."""
        print("🚀 Desplegando Worker V∞+28...")
        # 1. Crear KV namespace
        self.kv_namespace_id = self.crear_kv_namespace()
        if not self.kv_namespace_id:
            print("⚠️ No se pudo crear KV. Intentando usar existente...")
            # Buscar namespace existente
            url = f"{self.base}/accounts/{self.cuenta}/storage/kv/namespaces"
            r = requests.get(url, headers=self.headers, timeout=30)
            if r.status_code == 200:
                for ns in r.json().get('result', []):
                    if ns.get('title') == self.kv_namespace:
                        self.kv_namespace_id = ns.get('id')
                        print(f"   ✅ KV existente encontrado: {self.kv_namespace_id}")
                        break
        # 2. Desplegar Worker
        if self.kv_namespace_id:
            return self.desplegar_worker(WORKER_CODE)
        else:
            print("❌ No se pudo obtener KV namespace")
            return False

# ============================================================
# INTEGRACIÓN CON EL ECOSISTEMA
# ============================================================
def auto_desplegar():
    """Función principal que usa el primer token válido."""
    tokens = cargar_tokens()
    if not tokens:
        print("❌ No se encontraron tokens. Busca cfut_ en tus archivos.")
        return False
    for token in tokens:
        print(f"🔑 Probando token: {token[:15]}...")
        desplegador = DesplegadorCloudflare(token)
        if desplegador.ejecutar():
            print("✅ Despliegue exitoso. El bus V∞+28 está activo.")
            return True
        else:
            print("⚠️ Falló con este token, probando siguiente...")
    print("❌ Todos los tokens fallaron.")
    return False

# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("🧬 V∞+29 — AUTO-DESPLIEGUE DEL BUS NATIVO")
    print("="*60)
    # Guardar el código del Worker localmente
    with open(WORKER_SCRIPT, 'w') as f:
        f.write(WORKER_CODE)
    print(f"📄 Worker script guardado en {WORKER_SCRIPT}")
    # Ejecutar despliegue
    exito = auto_desplegar()
    if exito:
        print("🌐 Bus disponible en: https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/bus")
    else:
        print("❌ Falló el despliegue. Revisa tus tokens y conexión.")
    print("="*60)
