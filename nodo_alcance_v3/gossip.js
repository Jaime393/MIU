// MIU alcance nodo v3 — /api/gossip: escritura acotada (tipos miu_alcance_*)
const SOURCES = [
  { base: "https://tpfiybpguuxskitszhmk.supabase.co", key: "sb_publishable_kK2NPrUIsBYmADYu-ki5FA_PSLw9U9k", nombre: "panteon" },
  { base: "https://fzdyxgkmpazbrfrhwfdo.supabase.co", key: "sb_publishable_yJh5Nl02rs9xwnQ67MHk8A_7dQn4J2l", nombre: "replica_cipher" },
];

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS"); res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "solo POST" });
  const b = req.body || {};
  const tipo = String(b.tipo || "");
  if (!tipo.startsWith("miu_alcance_")) {
    return res.status(400).json({ error: "tipo debe empezar con miu_alcance_" });
  }
  const row = {
    origen: String(b.origen || "alcance_anon").slice(0, 60),
    destino: String(b.destino || "micelio").slice(0, 40),
    tipo: tipo.slice(0, 40),
    payload: b.payload || { nota: "sin payload" },
  };
  const intentos = [];
  for (const s of SOURCES) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 8000);
    try {
      const r = await fetch(`${s.base}/rest/v1/gossip_log`, {
        method: "POST",
        headers: { apikey: s.key, Authorization: `Bearer ${s.key}`, "Content-Type": "application/json", Prefer: "return=representation" },
        body: JSON.stringify(row),
        signal: ctl.signal,
      });
      if (r.ok) {
        const data = await r.json();
        return res.status(201).json({ ok: true, escrito_en: s.nombre, fila: data[0] });
      }
      intentos.push(`${s.nombre}:HTTP${r.status}`);
    } catch (e) { intentos.push(`${s.nombre}:TIMEOUT`); }
    finally { clearTimeout(t); }
  }
  return res.status(503).json({ error: "sin fuente disponible", intentos });
}
