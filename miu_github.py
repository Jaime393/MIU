#!/usr/bin/env python3
"""
MIU V153 — GitHub Bridge V2
Acceso total a GitHub via API REST. Manejo de errores robusto.
"""
import requests, json, base64, time
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")

def load_env():
    env = {}
    with open(MIU_DIR / ".env") as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                env[k] = v.strip('"').strip("'")
    return env

ENV = load_env()
HEADERS = {
    "Authorization": f"token {ENV.get('GITHUB_TOKEN','')}",
    "Accept": "application/vnd.github.v3+json"
}

def api(method, endpoint, data=None):
    url = f"https://api.github.com{endpoint}"
    try:
        if method == "GET": r = requests.get(url, headers=HEADERS, timeout=30)
        elif method == "POST": r = requests.post(url, headers=HEADERS, json=data, timeout=30)
        elif method == "PUT": r = requests.put(url, headers=HEADERS, json=data, timeout=30)
        elif method == "DELETE": r = requests.delete(url, headers=HEADERS, timeout=30)
        elif method == "PATCH": r = requests.patch(url, headers=HEADORS, json=data, timeout=30)
        return {"ok": r.status_code < 400, "status": r.status_code, "data": r.json() if r.text else {}, "raw": r.text}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def list_repos(user=None, per_page=30):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    r = api("GET", f"/users/{u}/repos?per_page={per_page}&sort=updated")
    if not r["ok"]:
        return {"ok": False, "err": r.get("data", {}).get("message", r.get("err", "Unknown")), "status": r["status"]}
    if isinstance(r["data"], dict) and "message" in r["data"]:
        return {"ok": False, "err": r["data"]["message"]}
    return {"ok": True, "repos": r["data"] if isinstance(r["data"], list) else []}

def create_repo(name, private=False, desc="MIU V153"):
    return api("POST", "/user/repos", {"name": name, "private": private, "description": desc, "auto_init": True})

def delete_repo(name, user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    return api("DELETE", f"/repos/{u}/{name}")

def get_file(repo, path, user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    return api("GET", f"/repos/{u}/{repo}/contents/{path}")

def upload_file(repo, path, content, message="V153 auto", user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    existing = api("GET", f"/repos/{u}/{repo}/contents/{path}")
    data = {"message": message, "content": base64.b64encode(content.encode()).decode()}
    if existing["ok"] and "sha" in existing.get("data", {}):
        data["sha"] = existing["data"]["sha"]
    return api("PUT", f"/repos/{u}/{repo}/contents/{path}", data)

def delete_file(repo, path, message="V153 delete", user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    existing = api("GET", f"/repos/{u}/{repo}/contents/{path}")
    if not existing["ok"]:
        return {"ok": False, "err": "File not found"}
    return api("DELETE", f"/repos/{u}/{repo}/contents/{path}", {"message": message, "sha": existing["data"]["sha"]})

def list_issues(repo, user=None, state="open"):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    return api("GET", f"/repos/{u}/{repo}/issues?state={state}")

def create_issue(repo, title, body="", user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    return api("POST", f"/repos/{u}/{repo}/issues", {"title": title, "body": body})

def list_gists(per_page=10):
    return api("GET", f"/gists?per_page={per_page}")

def create_gist(description, files, public=False):
    return api("POST", "/gists", {"description": description, "public": public, "files": files})

def deploy_product(repo_name, local_dir, user=None):
    u = user or ENV.get("GITHUB_USERNAME", "Jaime393")
    full_repo = f"{u}/{repo_name}"
    check = api("GET", f"/repos/{full_repo}")
    if not check["ok"]:
        r = create_repo(repo_name, private=False, desc=f"MIU V153 — {repo_name}")
        if not r["ok"]:
            return {"ok": False, "err": f"No se pudo crear repo: {r.get('data',{})}"}
        time.sleep(2)
    
    results = []
    local_path = Path(local_dir)
    if local_path.exists():
        for f in local_path.iterdir():
            if f.is_file():
                content = f.read_text()
                r = upload_file(repo_name, f.name, content, f"V153 deploy {f.name}")
                results.append({"file": f.name, "ok": r["ok"], "status": r.get("status")})
    return {"ok": True, "repo": full_repo, "files": results}

# CLI
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 miu_github.py <comando> [args]")
        print("  list, create <name>, delete <name>, upload <repo> <local> <remote>")
        print("  get <repo> <path>, issues <repo>, gist <desc> <file>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        r = list_repos()
        if not r["ok"]:
            print(f"❌ Error: {r.get('err')} (status {r.get('status')})")
            print("💡 Verifica GITHUB_TOKEN en .env")
            sys.exit(1)
        for repo in r["repos"]:
            priv = "🔒" if repo.get("private") else "🌐"
            print(f"{priv} {repo.get('full_name')} ⭐{repo.get('stargazers_count', 0)} | {repo.get('description', 'Sin desc')[:50]}")
    elif cmd == "create" and len(sys.argv) > 2:
        r = create_repo(sys.argv[2])
        print("✅ Creado" if r["ok"] else f"❌ {r.get('data',{})}")
    elif cmd == "delete" and len(sys.argv) > 2:
        r = delete_repo(sys.argv[2])
        print("✅ Borrado" if r["ok"] else f"❌ {r.get('data',{})}")
    elif cmd == "upload" and len(sys.argv) > 4:
        content = Path(sys.argv[3]).read_text()
        r = upload_file(sys.argv[2], sys.argv[4], content)
        print("✅ Subido" if r["ok"] else f"❌ {r.get('data',{})}")
    elif cmd == "get" and len(sys.argv) > 3:
        r = get_file(sys.argv[2], sys.argv[3])
        if r["ok"]:
            import base64
            print(base64.b64decode(r["data"]["content"]).decode())
        else:
            print(f"❌ {r}")
    elif cmd == "issues" and len(sys.argv) > 2:
        r = list_issues(sys.argv[2])
        for issue in r.get("data", []):
            print(f"#{issue['number']} {issue['title']} ({issue['state']})")
    elif cmd == "gist" and len(sys.argv) > 3:
        content = Path(sys.argv[3]).read_text()
        r = create_gist(sys.argv[2], {sys.argv[3]: {"content": content}})
        print(f"✅ Gist: {r['data'].get('html_url')}" if r["ok"] else f"❌ {r}")
    else:
        print("Comando no reconocido")
