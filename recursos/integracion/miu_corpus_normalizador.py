#!/usr/bin/env python3
# miu-corpus-normalizador v1 (CHK-141)
# Corrige el esquema mezclado de Jaime393/miu-dataset (prompt/chosen/rejected + instruction/input/output):
# lee el corpus vivo del Panteon (tabla corpus), lo normaliza a esquema fijo
# {instruction, input, output, categoria, ktau} y lo empuja como JSONL a
# Jaime393/miu-corpus-clean (dataset consistente para datasets-server/entrenamiento).
# Autonomo: GHA cada 8h. El corpus mezclado original se conserva (K-MIN, no poda).
import json, os, urllib.request

PAN = 'https://tpfiybpguuxskitszhmk.supabase.co/rest/v1/corpus'
ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0'
PAGE = 1000

def fetch_page(offset):
    url = f'{PAN}?select=id,pregunta,respuesta,categoria,ktau,fuente,version&order=id.asc&limit={PAGE}&offset={offset}'
    r = urllib.request.Request(url, headers={'apikey': ANON, 'Authorization': 'Bearer ' + ANON, 'User-Agent': 'miu-corpus-normalizador/1.0'})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read())

def main():
    rows, offset = [], 0
    while True:
        page = fetch_page(offset)
        if not page: break
        rows.extend(page); offset += PAGE
        if len(page) < PAGE: break
    print(f'corpus leido: {len(rows)} filas')
    # normalizar a esquema fijo
    with open('/tmp/corpus_clean.jsonl', 'w') as f:
        for r in rows:
            f.write(json.dumps({
                'instruction': r.get('pregunta') or '',
                'input': '',
                'output': r.get('respuesta') or '',
                'categoria': r.get('categoria') or '',
                'ktau': r.get('ktau'),
            }, ensure_ascii=False) + '\n')
    # empujar a HF
    from huggingface_hub import HfApi
    api = HfApi(token=os.environ['HF_TOKEN'])
    api.create_repo('Jaime393/miu-corpus-clean', repo_type='dataset', private=False, exist_ok=True)
    res = api.upload_file(path_or_fileobj='/tmp/corpus_clean.jsonl', path_in_repo='corpus_clean.jsonl',
                          repo_id='Jaime393/miu-corpus-clean', repo_type='dataset',
                          commit_message=f'corpus normalizado {len(rows)} pares esquema fijo (auto)')
    print('subido:', res)

if __name__ == '__main__':
    main()
