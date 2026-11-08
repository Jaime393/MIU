#!/usr/bin/env python3
# miu-intenciones-consumidor v1 (CHK-140)
# Drena la cola intenciones del Metabolismo (fxmupxpwzzxnjcscpyuw):
# lee pendientes, ejecuta tipo=conversacion via chat-node (groq), escribe respuesta
# a gossip_log del Metabolismo y marca la intencion ejecutada.
# Falla suave: una intencion que no puede ejecutar queda pendiente (K-MIN, no poda).
import json, os, sys, urllib.request

META_URL = 'https://fxmupxpwzzxnjcscpyuw.supabase.co/rest/v1'
CHAT = 'https://miu-chat-node.franchescopalacios9.workers.dev/chat'
CHAT_TOKEN = 'MIU_2026_11'
ANON = os.environ.get('CANADA_ANON', '')

def req(url, method='GET', body=None, headers=None, timeout=30):
    data = json.dumps(body).encode() if body is not None else None
    h = {'User-Agent': 'miu-intenciones-consumidor/1.0'}
    if headers: h.update(headers)
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.loads(resp.read() or b'{}')

def main():
    if not ANON:
        print('CANADA_ANON no definido'); return
    H = {'apikey': ANON, 'Authorization': 'Bearer ' + ANON, 'Content-Type': 'application/json'}
    pend = req(f'{META_URL}/intenciones?select=*&estado=eq.pendiente&order=ts.asc&limit=5', headers=H)
    if not isinstance(pend, list):
        print('lectura fallo:', pend); return
    print(f'intenciones pendientes leidas: {len(pend)}')
    for it in pend:
        fid = it.get('flow_id'); tipo = it.get('tipo'); obj = it.get('objetivo') or ''
        try:
            if tipo == 'conversacion':
                resp = req(CHAT, method='POST', timeout=60, body={'msg': obj},
                           headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + CHAT_TOKEN})
                respuesta = resp.get('respuesta') or '(vacia)'
            elif tipo == 'probe':
                respuesta = f'probe absorbido por consumidor v1: {obj}'
            else:
                respuesta = f'tipo {tipo} sin ejecutor v1 - queda como grieta fertil'
            # escribir respuesta al gossip del Metabolismo
            req(f'{META_URL}/gossip_log', method='POST', headers=H,
                body={'origen': 'intenciones_consumidor_v1', 'destino': 'metabolismo', 'tipo': 'intencion_ejecutada',
                      'payload': {'flow_id': fid, 'objetivo': obj, 'respuesta': respuesta[:800]}})
            # marcar ejecutada
            req(f"{META_URL}/intenciones?flow_id=eq.{fid}", method='PATCH', headers=H,
                body={'estado': 'ejecutada', 'ejecutor': 'consumidor_v1_github', 'evidencia': {'respuesta': respuesta[:400]}, 'ts_cierre': 'now()'})
            print(f'ejecutada: {fid} -> {respuesta[:80]}')
        except Exception as e:
            print(f'fallo {fid}: {str(e)[:100]} - queda pendiente')

if __name__ == '__main__':
    main()
