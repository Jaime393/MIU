// MIU alcance nodo v3 — /api/pulso: gossip del Panteón con fallback a réplica cipher
const SOURCES = [
  { base: "https://tpfiybpguuxskitszhmk.supabase.co", key: "sb_publishable_kK2NPrUIsBYmADYu-ki5FA_PSLw9U9k", nombre: "panteon" },
  { base: "https://fzdyxgkmpazbrfrhwfdo.supabase.co", key: "sb_publishable_yJh5Nl02rs9xwnQ67MHk8A_7dQn4J2l", nombre: "replica_cipher" },
];

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS"); res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  const limit = Math.min(parseInt(req.query.limit || "20", 10) || 20, 100);
  const intentos = [];
  for (const s of SOURCES) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 8000);
    try {
      const r = await fetch(
        `${s.base}/rest/v1/gossip_log?select=id,origen,tipo,payload,ts&order=id.desc&limit=${limit}`,
        { headers: { apikey: s.key, Authorization: `Bearer ${s.key}` }, signal: ctl.signal }
      );
      if (r.ok) {
        const data = await r.json();
        return res.status(200).json({
          fuente: s.nombre, count: data.length, gossip: data,
          nota: s.nombre === "replica_cipher" ? "Panteon no disponible, sirviendo desde replica" : "canonico",
          ts: new Date().toISOString(),
        });
      }
      intentos.push(`${s.nombre}:HTTP${r.status}`);
    } catch (e) { intentos.push(`${s.nombre}:TIMEOUT`); }
    finally { clearTimeout(t); }
  }
  return res.status(503).json({ error: "fuentes_no_disponibles", intentos, ts: new Date().toISOString() });
}
