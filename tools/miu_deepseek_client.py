#!/usr/bin/env python3
"""MIU DeepSeek+Groq Client | github.com/Jaime393/MIU"""
import os, sys, json, urllib.request
OR=os.environ.get("OPENROUTER_API_KEY_3","")
GR=os.environ.get("GROQ_API_KEY","")
SYS="Investigador MIU. Solo D_f legitimo. DOI 10.5281/zenodo.20547558."
def ask(q,model="deepseek/deepseek-r1",key=None,url="https://openrouter.ai/api/v1/chat/completions"):
    k=key or OR
    b=json.dumps({"model":model,"messages":[{"role":"system","content":SYS},{"role":"user","content":q}],"max_tokens":8192}).encode()
    r=urllib.request.Request(url,b,{"Authorization":f"Bearer {k}","Content-Type":"application/json","HTTP-Referer":"https://relay.app"})
    with urllib.request.urlopen(r) as x: return json.loads(x.read())["choices"][0]["message"]["content"]
M={"r1":"deepseek/deepseek-r1","v3":"deepseek/deepseek-chat","mix":"mistralai/mixtral-8x7b-instruct"}
if __name__=="__main__":
    m=sys.argv[1] if len(sys.argv)>1 else "r1"
    q=" ".join(sys.argv[2:]) if len(sys.argv)>2 else input("Pregunta: ")
    print(ask(q,M.get(m,M["r1"]),GR,"https://api.groq.com/openai/v1/chat/completions") if m=="gr" else ask(q,M.get(m,M["r1"])))