#!/usr/bin/env python3
"""
Buscador de tokens — Escanea directorios comunes en busca de claves.
"""
import os, re, json
from pathlib import Path

PATRONES = [
    r'[A-Z0-9]{20,}',           # tokens alfanuméricos largos
    r'sk-[a-zA-Z0-9]{20,}',      # OpenAI / OpenRouter
    r'ghp_[a-zA-Z0-9]{30,}',     # GitHub
    r'gsk_[a-zA-Z0-9]{30,}',     # Groq
    r'cfat_[a-zA-Z0-9]{30,}',    # Cloudflare
    r'sb_publishable_[a-zA-Z0-9]+', # Scaleway
]

DIRECTORIOS = [
    "/storage/emulated/0/Download",
    "/sdcard/Download",
    "/storage/25A9-180D",
    "/data/data/com.termux/files/home",
]

def buscar_archivos(dir_path):
    encontrados = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.env', '.json', '.txt', '.cfg', '.conf')):
                ruta = Path(root) / file
                try:
                    contenido = ruta.read_text(errors='ignore')
                    for patron in PATRONES:
                        for match in re.findall(patron, contenido):
                            encontrados.append({
                                "archivo": str(ruta),
                                "token": match[:15] + "..." + match[-5:],
                                "patron": patron
                            })
                except:
                    pass
    return encontrados

def main():
    print("🔍 Buscando tokens en directorios comunes...")
    resultados = []
    for d in DIRECTORIOS:
        if Path(d).exists():
            print(f"📁 Escaneando {d}...")
            resultados += buscar_archivos(d)
    
    print(f"\n✅ Encontrados {len(resultados)} posibles tokens")
    for r in resultados[:20]:
        print(f"   • {r['archivo']} → {r['token']}")
    
    with open("tokens_encontrados.json", "w") as f:
        json.dump(resultados, f, indent=2)
    print("\n📄 Reporte guardado en tokens_encontrados.json")

if __name__ == "__main__":
    main()
