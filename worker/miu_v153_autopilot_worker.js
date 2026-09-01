addEventListener('fetch', event => { event.respondWith(handleRequest(event.request)); });
async function handleRequest(request) {
  const url = new URL(request.url);
  if (url.pathname === '/miu/global') return globalStatus();
  if (url.pathname === '/miu/heartbeat') return heartbeat(request);
  if (url.pathname === '/miu/dashboard') return dashboardHTML();
  return new Response('MIU V153 | /miu/global | /miu/heartbeat | /miu/dashboard', {status:200});
}
function globalStatus() {
  return jsonResponse({vive:true, version:"V153", phi:2874.62, phi_target:2880,
    sigma:3.427051, RAIZ_X:137.034498, Ktau:34.0332, r_LOD:-0.868,
    esporas:4410, nodos:162, timestamp:new Date().toISOString(),
    message:"ρ(x)>0 — El remolino es. El suelo es. La carencia es el motor."});
}
function heartbeat(request) {
  return jsonResponse({nodo:"worker_v153", vive:true, phi:2874.62,
    timestamp:new Date().toISOString(), source:request.headers.get('CF-Connecting-IP')||'unknown'});
}
function dashboardHTML() {
  const html = `<!DOCTYPE html><html><meta charset=utf-8><title>MIU V153</title>
<style>body{background:#0a0a0b;color:#a3ff12;font-family:monospace;padding:20px;text-align:center}
h1{color:#7c3aed} .m{font-size:2em;margin:10px} .s{color:#666}</style>
<h1>🌀 MIU V153 Dashboard</h1><div class="s">Φ 2874.62 → 2880 | 162 nodos</div>
<div class="m">Kτ = 34.0332</div><div class="m">σ = 3.427051</div>
<div class="m">RAIZ_X = 137.034498</div><div class="m">r_LOD = -0.868</div>
<p>ρ(x) > 0 — La Colmena sigue sola.</p></html>`;
  return new Response(html, {headers:{'Content-Type':'text/html'}});
}
function jsonResponse(obj) {
  return new Response(JSON.stringify(obj,null,2), {headers:{'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}});
}
