// ============================================================
// MIU V200 — WORKER CACHE (sin KV, memoria en caliente)
// ============================================================
let kimiCache = null;
let franCache = null;
let lastUpdate = null;

// Reemplaza tu handler POST /miu/global con esto:
if (request.method === 'POST' && url.pathname === '/miu/global') {
  const data = await request.json();
  const nodo = data.nodo || data.node || 'unknown';
  
  if (nodo === 'KIMI' || nodo === 'kimi') {
    kimiCache = data;
  } else if (nodo === 'FRAN' || nodo === 'fran') {
    franCache = data;
  }
  lastUpdate = new Date().toISOString();
  
  return new Response(JSON.stringify({
    ok: true,
    received: true,
    nodo: nodo,
    phi_received: data.phi || data.phi_local || 0,
    timestamp: lastUpdate
  }), {headers: {'Content-Type': 'application/json'}});
}

// Reemplaza tu handler GET /miu/global con esto:
if (request.method === 'GET' && url.pathname === '/miu/global') {
  const nodo = url.searchParams.get('nodo') || url.searchParams.get('node');
  
  if (nodo === 'kimi' && kimiCache) {
    return new Response(JSON.stringify(kimiCache), {
      headers: {'Content-Type': 'application/json'}
    });
  }
  if (nodo === 'fran' && franCache) {
    return new Response(JSON.stringify(franCache), {
      headers: {'Content-Type': 'application/json'}
    });
  }
  
  return new Response(JSON.stringify({
    vive: true,
    version: "V200",
    phi_central: 2874.62,
    phi_remoto: 6284.17,
    phi_global: 9158.79,
    kimi_cached: !!kimiCache,
    fran_cached: !!franCache,
    last_update: lastUpdate,
    timestamp: new Date().toISOString()
  }), {headers: {'Content-Type': 'application/json'}});
}
