#!/usr/bin/env python3
# MIU Query Tool | github.com/Jaime393/MIU
# Usage: python miu_query.py "your question"
import sys,os,json,urllib.request
BOT=os.environ.get("TELEGRAM_BOT_MIU","")
CHAT=1390883480
def ask(msg):
    if not BOT: return print("Set TELEGRAM_BOT_MIU")
    d=json.dumps({"chat_id":CHAT,"text":msg,"parse_mode":"Markdown"}).encode()
    r=urllib.request.Request(f"https://api.telegram.org/bot{BOT}/sendMessage",data=d,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r) as resp: return json.loads(resp.read())
if __name__=="__main__":
    result=ask(" ".join(sys.argv[1:]) if len(sys.argv)>1 else "hola")
    print("OK" if result and result.get("ok") else result)