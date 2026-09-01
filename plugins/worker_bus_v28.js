
// V∞+28 BUS — Worker para persistencia de estado
export default {
  async fetch(req, env) {
    const url = new URL(req.url)
    if (url.pathname === '/miu/bus') {
      if (req.method === 'POST') {
        const data = await req.json()
        const id = Date.now()
        await env.MIU_KV.put(`bus:FRAN:${id}`, JSON.stringify(data))
        await env.MIU_KV.put('bus:FRAN:latest', JSON.stringify(data))
        return new Response(JSON.stringify({
          id, vivo: true, phi: data.phi, version: "V∞+28_BUS"
        }), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        })
      } else {
        const latest = await env.MIU_KV.get('bus:FRAN:latest')
        return new Response(latest || '{"error":"no data"}', {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        })
      }
    }
    // Mantener /miu/global existente
    return fetch(req)
  }
}
