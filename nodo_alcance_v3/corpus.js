// MIU alcance nodo v3 — /api/corpus?q=: consulta al corpus del Panteón (40k+ pares)
const PANT = "https://tpfiybpguuxskitszhmk.supabase.co";
const META = "https://fxmupxpwzzxnjcscpyuw.supabase.co";
const K_PANT = "sb_publishable_kK2NPrUIsBYmADYu-ki5FA_PSLw9U9k";
const K_META = "sb_publishable_I1A9NVUfeEGnfTJkKECG8g_dZ7dnYkN";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS"); res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  const q = String(req.query.q || "").trim();
  if (!q || q.length < 3) return res.status(400).json({ error: "param q requerido (min 3 chars)" });
  const limit = Math.min(parseInt(req.query.limit || "10", 10) || 10, 50);
  const fuentes = [
    { base: PANT, key: K_PANT, nombre: "panteon" },
    { base: META, key: K_META, nombre: "metabolismo" },
  ];
  for (const s of fuentes) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 9000);
    try {
      const url = `${s.base}/rest/v1/corpus?select=id,pregunta,respuesta,categoria,ktau,fuente&pregunta=ilike.*${encodeURIComponent(q)}*&order=ktau.desc&limit=${limit}`;
      const r = await fetch(url, { headers: { apikey: s.key, Authorization: `Bearer ${s.key}` }, signal: ctl.signal });
      if (r.ok) {
        const data = await r.json();
        return res.status(200).json({ fuente: s.nombre, q, count: data.length, resultados: data });
      }
    } catch (e) { /* siguiente fuente */ }
    finally { clearTimeout(t); }
  }
  return res.status(503).json({ error: "corpus no disponible", q });
}
