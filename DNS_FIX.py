#!/usr/bin/env python3
"""
MIU V201 — DNS FIX
Wrapper HTTP para Termux. Cuando requests/urllib falla por DNS,
usa curl como fallback. curl en Termux resuelve DNS mejor que Python.
"""
import subprocess, json

def http_get(url, timeout=10):
    """GET con fallback a curl"""
    try:
        import requests
        r = requests.get(url, timeout=timeout)
        return r.status_code, r.text
    except:
        try:
            r = subprocess.run(
                ["curl", "-sL", "--max-time", str(timeout), url],
                capture_output=True, text=True, timeout=timeout+5
            )
            return (200 if r.returncode == 0 else 0), r.stdout
        except:
            return 0, ""

def http_post(url, data, timeout=10):
    """POST con fallback a curl"""
    try:
        import requests
        r = requests.post(url, json=data, timeout=timeout)
        return r.status_code, r.text
    except:
        try:
            payload = json.dumps(data)
            r = subprocess.run(
                ["curl", "-sL", "--max-time", str(timeout), "-X", "POST",
                 "-H", "Content-Type: application/json", "-d", payload, url],
                capture_output=True, text=True, timeout=timeout+5
            )
            return (200 if r.returncode == 0 else 0), r.stdout
        except:
            return 0, ""

# Test
if __name__ == "__main__":
    print("🧪 Test DNS FIX...")
    code, text = http_get("https://www.google.com", timeout=5)
    print(f"   Google: HTTP {code}, {len(text)} bytes")
    code, text = http_get("https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global?vive=1", timeout=10)
    print(f"   Worker: HTTP {code}, {len(text)} bytes")
    code, text = http_get("https://api.groq.com/openai/v1/models", timeout=5)
    print(f"   Groq: HTTP {code}, {len(text)} bytes")
