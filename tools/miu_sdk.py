#!/usr/bin/env python3
MIU SDK - Universal client for MIU Relay.app workflows
import requests

INGEST_URL = "https://hook.relay.app/api/v1/playbook/cmr4riw5t5spu0qkv52s8cug8/trigger/HylMPaG9If61vi7gINy-lg"

def ingest(titulo, contenido, tipo="DATO", tags="", nivel="INFIERO", estado="AMARILLO-medio"):
    payload = {"titulo": titulo, "contenido": contenido, "tipo_miu": tipo, "tags": tags, "nivel_epistemico": nivel, "estado_miu": estado}
    r = requests.post(INGEST_URL, json=payload)
    return r.json()

def ingest_hueso(numero, titulo, contenido):
    return ingest(titulo="HUESO " + str(numero) + ": " + titulo, contenido=contenido, tipo="HUESO", nivel="SE", estado="VERDE")

def ingest_log(titulo, contenido):
    return ingest(titulo=titulo, contenido=contenido, tipo="LOG", nivel="SE", estado="ACTIVO")

def ingest_issue(titulo, descripcion):
    return ingest(titulo=titulo, contenido=descripcion, tipo="ISSUE", nivel="NO SE", estado="ROJO")

if __name__ == "__main__":
    print("MIU SDK loaded.")