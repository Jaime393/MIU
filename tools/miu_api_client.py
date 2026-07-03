#!/usr/bin/env python3
"""MIU Universal API Client | github.com/Jaime393/MIU"""
import os, sys, json, urllib.request
INGEST_URL = os.environ.get("MIU_INGEST_URL", "")
SEARCH_URL = os.environ.get("MIU_SEARCH_URL", "")
BOT = os.environ.get("TELEGRAM_BOT_MIU", "")
CHAT = 1390883480
def ingest(tipo, titulo, contenido, tags="", nivel="INFIERO", estado="AMARILLO-medio"):
    d={"tipo_miu":tipo,"titulo":titulo,"contenido":contenido,"tags":tags,"nivel_epistemico":nivel,"estado_miu":estado}
    r=urllib.request.Request(INGEST_URL,json.dumps(d).encode(),{"Content-Type":"application/json"})
    with urllib.request.urlopen(r) as x: return json.loads(x.read())
def search(q, k=5):
    r=urllib.request.Request(SEARCH_URL,json.dumps({"query":q,"top_k":k}).encode(),{"Content-Type":"application/json"})
    with urllib.request.urlopen(r) as x: return json.loads(x.read())
def tg(msg):
    r=urllib.request.Request(f"https://api.telegram.org/bot{BOT}/sendMessage",
        json.dumps({"chat_id":CHAT,"text":msg,"parse_mode":"Markdown"}).encode(),
        {"Content-Type":"application/json"})
    with urllib.request.urlopen(r) as x: return json.loads(x.read())
if __name__=="__main__":
    c=sys.argv[1] if len(sys.argv)>1 else "help"
    if c=="ingest": print(json.dumps(ingest(*sys.argv[2:6]),indent=2))
    elif c=="search": print(json.dumps(search(" ".join(sys.argv[2:])),indent=2))
    elif c=="tg": tg(" ".join(sys.argv[2:]))
    else: print("Usage: miu_api_client.py [ingest|search|tg] args...")