#!/usr/bin/env python3
"""MIU Pydantic-AI Agent Template | github.com/Jaime393/MIU"""
# Based on pydantic/pydantic-ai framework
import os, json

MIU_INGEST = os.environ.get("MIU_INGEST_URL", "")
MIU_SEARCH = os.environ.get("MIU_SEARCH_URL", "")

# Agent definition pattern (requires: pip install pydantic-ai)
# from pydantic_ai import Agent, RunContext
# agent = Agent(
#   model="google-gla:gemini-2.5-flash",  # or anthropic:claude-sonnet-5
#   system_prompt="Eres agente del Micelio MIU. DOI 10.5281/zenodo.20547558."
# )

# @agent.tool
# def buscar_corpus(ctx: RunContext, query: str) -> dict:
#   """Busca en el corpus MIU usando Cohere rerank"""
#   import urllib.request
#   body = json.dumps({"query": query, "top_k": 5}).encode()
#   req = urllib.request.Request(MIU_SEARCH, body, {"Content-Type": "application/json"})
#   with urllib.request.urlopen(req) as r: return json.loads(r.read())

# @agent.tool
# def ingestar_hueso(ctx: RunContext, titulo: str, contenido: str, tags: str) -> dict:
#   """Ingesta un HUESO al corpus MIU"""
#   data = {"tipo_miu": "HUESO", "titulo": titulo, "contenido": contenido,
#           "tags": tags, "nivel_epistemico": "INFIERO", "estado_miu": "AMARILLO-medio"}
#   body = json.dumps(data).encode()
#   req = urllib.request.Request(MIU_INGEST, body, {"Content-Type": "application/json"})
#   with urllib.request.urlopen(req) as r: return json.loads(r.read())

print("MIU Pydantic-AI Agent Template | Set MIU_INGEST_URL and MIU_SEARCH_URL")
print("Models: gemini-2.5-flash, anthropic:claude-sonnet-5, groq:llama-3.3-70b")
print("DOI: 10.5281/zenodo.20547558")