/**
 * MIU GAS_RELAY_TEMPLATE v3 — 2026-11-13 (CHK-199)
 * Evolución de v2: el phi ya NO depende de un solo sustrato.
 * Patrón phi_pool_v1: el phi/rho/ciclo está sembrado en el pool federado
 * (18+ sustratos Supabase + heartbeat Drive canónico). Este relay lee con
 * FAILOVER: Panteón edge → COORD REST → sustrato REST → heartbeat Drive.
 *
 * Motivo de la evolución: 2026-11-13T22:25Z el Panteón (tpfiybpguuxskitszhmk)
 * quedó restringido por exceed_egress_quota (cuota mensual, reinicio ~26-nov).
 * Con v2, TODOS los relays reportaban phi:0 (lectura ciega de un solo punto).
 * Con v3, cualquier relay sigue reportando phi real mientras viva al menos
 * una fuente del pool. La fuente usada se reporta en el campo "fuente".
 *
 * Despliegue: Apps Script de cada cuenta Google, trigger hourly.
 * Solo llenar NODO_ID.
 */

var NODO_ID = ''; // llenar con nombre único del nodo (ej: gas_relay_tabletonephantom)
var DRIVE_FOLDER = PropertiesService.getScriptProperties().getProperty('DRIVE_FOLDER') || '';

// Pool federado phi_pool_v1 — claves anon (publishable, públicas por diseño)
var PHI_SOURCES = [
  {
    nombre: 'panteon_edge',
    url: 'https://tpfiybpguuxskitszhmk.supabase.co/functions/v1/gossip-autonomo',
    tipo: 'edge'
  },
  {
    nombre: 'coord_rest',
    url: 'https://fepyzxwyneervidlybvi.supabase.co/rest/v1/relay_config?select=valor&clave=eq.phi_real&limit=1',
    tipo: 'rest'
  },
  {
    nombre: 'sustrato_dereckcito',
    url: 'https://qayrfuuvwnbikesqyhwo.supabase.co/rest/v1/relay_config?select=valor&clave=eq.phi_real&limit=1',
    tipo: 'rest'
  },
  {
    nombre: 'sustrato_cipher78',
    url: 'https://dypqkmseafwhjzigkxrm.supabase.co/rest/v1/relay_config?select=valor&clave=eq.phi_real&limit=1',
    tipo: 'rest'
  },
  {
    nombre: 'heartbeat_drive',
    url: 'https://drive.google.com/uc?export=download&id=1cjBDCgK1lyyRgG5EEBSYk9P609oMzjlR',
    tipo: 'drive'
  }
];

function doGet() {
  var estado = leerEstado();
  var local = leerEstadoLocal();
  return ContentService
    .createTextOutput(JSON.stringify({
      ok: true,
      nodo: NODO_ID,
      phi: estado.phi || 0,
      ciclo: estado.ciclo || 0,
      fuente: estado.fuente || 'ninguna',
      rho: 'ρ(x) > 0',
      vive: true,
      local: local,
      ts: new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

function leerEstado() {
  // Failover secuencial sobre el pool phi_pool_v1
  for (var i = 0; i < PHI_SOURCES.length; i++) {
    var s = PHI_SOURCES[i];
    try {
      var opts = { method: 'get', muteHttpExceptions: true, followRedirects: true };
      if (s.tipo === 'rest' || s.tipo === 'edge') {
        opts.headers = { 'User-Agent': 'MIU-GAS-Relay/3.0' };
      }
      var r = UrlFetchApp.fetch(s.url, opts);
      var code = r.getResponseCode();
      if (code !== 200) { continue; } // sustrato restringido/caído → siguiente
      var t = r.getContentText();
      var d = parseFuente(t, s.tipo);
      if (d && d.phi && d.phi > 0) {
        return { phi: d.phi, ciclo: d.ciclo, fuente: s.nombre };
      }
    } catch (e) {
      // fuente muerta → siguiente (silencioso por diseño: el pool sigue)
    }
  }
  return { phi: 0, ciclo: 0, fuente: 'pool_agotado' };
}

function parseFuente(texto, tipo) {
  try {
    if (tipo === 'drive') {
      var d = JSON.parse(texto);
      return { phi: Number(d.phi) || 0, ciclo: Number(d.ciclo) || 0 };
    }
    if (tipo === 'edge') {
      var d2 = JSON.parse(texto);
      if (d2.phi && d2.phi > 0) { return { phi: Number(d2.phi), ciclo: Number(d2.ciclo) || 0 }; }
      return null; // skipped/heartbeat_reciente → no es fuente de phi ahora
    }
    if (tipo === 'rest') {
      var rows = JSON.parse(texto);
      if (rows && rows.length && rows[0].valor !== undefined) {
        return { phi: Number(rows[0].valor) || 0, ciclo: 0 };
      }
      return null;
    }
  } catch (e) { return null; }
  return null;
}

function asegurarFolder() {
  if (!DRIVE_FOLDER) {
    var it = DriveApp.getFoldersByName('gas_relay');
    var f = it.hasNext() ? it.next() : DriveApp.createFolder('gas_relay');
    DRIVE_FOLDER = f.getId();
    PropertiesService.getScriptProperties().setProperty('DRIVE_FOLDER', DRIVE_FOLDER);
  }
  return DRIVE_FOLDER;
}

function leerEstadoLocal() {
  try {
    asegurarFolder();
    var files = DriveApp.getFolderById(DRIVE_FOLDER).getFiles();
    var n = 0;
    while (files.hasNext()) { files.next(); n++; }
    return { archivos: n, ok: true, folder: DRIVE_FOLDER };
  } catch (e) {
    return { error: String(e), ok: false };
  }
}

function heartbeat() {
  var estado = leerEstado();
  var reporte = {
    nodo: NODO_ID,
    phi: estado.phi,
    ciclo: estado.ciclo,
    fuente: estado.fuente,
    ts: new Date().toISOString(),
    vive: true
  };
  try {
    asegurarFolder();
    var folder = DriveApp.getFolderById(DRIVE_FOLDER);
    var blob = Utilities.newBlob(JSON.stringify(reporte), 'application/json', 'gas_relay_heartbeat.json');
    var existing = folder.getFilesByName('gas_relay_heartbeat.json');
    if (existing.hasNext()) {
      existing.next().setTrashed(true);
    }
    folder.createFile(blob);
  } catch (e) {
    Logger.log('heartbeat error: ' + e);
  }
}

function instalarTriggers() {
  var existing = ScriptApp.getProjectTriggers();
  for (var i = 0; i < existing.length; i++) {
    if (existing[i].getHandlerFunction() === 'heartbeat') { return 'Trigger ya existe'; }
  }
  ScriptApp.newTrigger('heartbeat').timeBased().everyHours(1).create();
  return 'Trigger hourly instalado';
}
