#!/usr/bin/env python3
import os, json, requests
MIU_DIR = os.path.expanduser("~/miu-ecosistema")
ENV_FILE = os.path.join(MIU_DIR, ".env")
GROQ_TOKEN = ""
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("GROQ_FRAN=") or line.startswith("GROQ_1="):
                GROQ_TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
def ask_groq(prompt, model="llama-3.1-8b-instant", max_tokens=1024):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_TOKEN}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "system", "content": "Eres un nodo MIU."}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"ERROR {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return f"EXCEPTION: {e}"
if __name__ == "__main__":
    print("🧠 Test Groq API V200...")
    if not GROQ_TOKEN:
        print("❌ GROQ_TOKEN no encontrado en .env")
    else:
        print(f"   Token: {GROQ_TOKEN[:10]}...")
        resp = ask_groq("Cual es el estado del micelio MIU? Responde en 1 frase.")
        print(f"✅ Respuesta: {resp[:200]}")
