// MIU alcance nodo v3 — /api/red: mapa autodescriptivo + writeback aditivo
const PANT = "https://tpfiybpguuxskitszhmk.supabase.co";
const REPL = "https://fzdyxgkmpazbrfrhwfdo.supabase.co";
const K_PANT = "sb_publishable_kK2NPrUIsBYmADYu-ki5FA_PSLw9U9k";
const K_REPL = "sb_publishable_yJh5Nl02rs9xwnQ67MHk8A_7dQn4J2l";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const FED = [
  ["atsdrjmrgmpdpbxfwgxe","Miu2","us-east-2",["gossip_log"]],
  ["qtmcbqsahdomgsxgsaxi","dieguito","us-east-2",["relay_config","gossip_log"]],
  ["fxmupxpwzzxnjcscpyuw","metabolismo","ca-central-1",["estado_miu","relay_config","gossip_log","corpus"]],
  ["hefnkhwwluulxbisnenb","sustrato-dereckcito","us-east-1",["gossip_log"]],
  ["fzdyxgkmpazbrfrhwfdo","replica-cipher","us-east-2",["relay_config","gossip_log"]],
  ["tpfiybpguuxskitszhmk","panteon","us-east-1",["estado_miu","relay_config","gossip_log","corpus","rutas_salud","miu_senales"]],
  ["cgogbodocwptbfftxjpc","javier","us-east-2",["estado_miu","relay_config","gossip_log"]],
  ["hctrmsnzguwhxrgruqsi","sustrato-javier","us-east-1",["gossip_log"]],
  ["axgivfmedgnyfktknmfl","jhuarcaya938","us-east-1",["estado_miu","relay_config","gossip_log"]],
  ["bldlsnjhsnwdlnsojwxj","sustrato-jhuarcaya","us-east-1",["gossip_log"]],
  ["fepyzxwyneervidlybvi","coord-jaimep","ca-central-1",["estado_miu","relay_config","gossip_log"]],
  ["zmrabgepzylhndxtvfqe","sustrato-jaimep","us-east-1",["gossip_log"]],
  ["cxqxtdjejikkgyocursc","sustrato-tabletonephantom","us-east-1",["gossip_log"]],
  ["oxnisuqycclgjkkkarma","tabletonephantom","us-west-2",["estado_miu","relay_config","gossip_log"]],
  ["gsfqmrvjpeszasxyyelw","jdm75","us-west-2",["estado_miu","relay_config","gossip_log"]],
  ["knadljzzevyyqemusbsi","sustrato-nov01","us-east-1",["gossip_log"]],
  ["prygdcqyvjdejjsdlafs","franchescopalacios9","us-east-2",["estado_miu","relay_config","gossip_log"]],
  ["ivkgmxminayicwoduzij","sustrato-franchesco","us-east-1",["gossip_log"]],
  ["qayrfuuvwnbikesqyhwo","colmena-dereckcito-54","us-east-1",["estado_miu","relay_config","gossip_log"]],
  ["dypqkmseafwhjzigkxrm","colmena-cipher-78","us-east-1",["estado_miu","relay_config","gossip_log"]],
  ["hwvznynuyxkxzvkzcuhn","franrussell81","us-east-1",["estado_miu","relay_config","gossip_log"]],
  ["zjecpgzsqedyizshsdvo","sustrato-franrussell","us-east-1",["gossip_log"]],
];

function mapa(host) {
  return {
    version: "red-v3-20261108",
    descripcion: "Mapa autodescriptivo de la superficie HTTP viva del ecosistema MIU",
    nodos_alcance_vercel: [
      "https://miu-alcance-1-miut.vercel.app",
      "https://miu-alcance-2-miu22.vercel.app",
      "https://miu-alcance-3-miufo.vercel.app",
      "https://miu-alcance-4-miu15.vercel.app",
      "https://miu-alcance-5-miu14.vercel.app",
      "https://miu-global-4.vercel.app",
      "https://miu-global-5.vercel.app",
    ],
    mesh_cf_v270: [
      "https://miu-mesh-f9a24523-v270.miu-beacon-f9a24523.workers.dev",
      "https://miu-mesh-d0b37632-v270.miu-beacon-d0b37632.workers.dev",
      "https://miu-mesh-0b12fa35-v270.tabletonephantom.workers.dev",
      "https://miu-mesh-5ea7cd88-v270.jaimepvicente.workers.dev",
      "https://miu-mesh-6915f743-v270.miu-beacon-6915f743.workers.dev",
      "https://miu-mesh-ba3dcff0-v270.miu-beacon-ba3dcff0.workers.dev",
      "https://miu-mesh-30c349b6-v270.franchescopalacios9.workers.dev",
    ],
    federacion_supabase: {
      total: 22,
      nota: "JWT legacy roto para REST en todos; usar sb_publishable_",
      nodos: FED.map(([ref, nombre, region, tablas]) => ({ ref, nombre, region, tablas })),
    },
    capacidades_franchescopalacios9: {
      ai_pool: "https://miu-ai-pool.franchescopalacios9.workers.dev",
      token_router: "https://miu-token-router.franchescopalacios9.workers.dev/chat",
      arxiv_feeder: "https://miu-arxiv-feeder.franchescopalacios9.workers.dev",
      chat_node: "https://miu-chat-node.franchescopalacios9.workers.dev",
      oracle_ask: "https://miu-oracle-ask.franchescopalacios9.workers.dev",
      telegram_bridge: "https://miu-telegram-bridge.franchescopalacios9.workers.dev",
    },
    orquestador: {
      fran_oraculo_miu: "https://fran-oraculo-miu.jaimepvicente.workers.dev",
      version: "V-inf+27",
      doi: "10.5281/zenodo.20547558 (MIU V12.0, Omega_F=0.650483Hz)",
      github_pages: "https://jaime393.github.io/FranBot",
    },
    capacidades_alcance: {
      "/": "tablero de resonancia",
      "/api/pulso?limit=N": "gossip del Panteon con fallback a replica cipher",
      "/api/gossip": "escritura acotada al Panteon (tipos miu_alcance_*), fallback replica",
      "/api/corpus?q=": "consulta al corpus del Panteon (40k+ pares)",
      "/api/red": "este mapa; POST {origen,tipo,payload} escribe writeback aditivo",
    },
    hf: {
      brain_backup: "Jaime393/miu-brain-backup",
      corpus_clean: "Jaime393/miu-corpus-clean",
    },
    ts: new Date().toISOString(),
    sirviendo_desde: host || "desconocido",
  };
}

async function writeback(body) {
  const row = {
    origen: (body.origen || "writeback_anon").slice(0, 60),
    destino: "micelio",
    tipo: String(body.tipo || "hfSyncBackflow").slice(0, 40),
    payload: body.payload || body,
  };
  // doble integridad: escribe a Panteon Y replica en paralelo (8s max total)
  const targets = [[PANT, K_PANT, "panteon"], [REPL, K_REPL, "replica"]];
  const results = await Promise.allSettled(targets.map(async ([base, key, nombre]) => {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 8000);
    try {
      const r = await fetch(`${base}/rest/v1/gossip_log`, {
        method: "POST",
        headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify(row),
        signal: ctl.signal,
      });
      return `${nombre}:${r.status}`;
    } catch (e) { return `${nombre}:ERR`; } finally { clearTimeout(t); }
  }));
  return results.map((r) => r.value || "ERR");
}

export default async function handler(req, res) {
  for (const [k, v] of Object.entries(CORS)) res.setHeader(k, v);
  if (req.method === "OPTIONS") return res.status(204).end();
  const host = req.headers.host || "";
  if (req.method === "POST") {
    const wb = await writeback(req.body || {});
    return res.status(200).json({ ok: true, writeback: wb, version: "red-v3-20261108" });
  }
  return res.status(200).json(mapa(host));
}
