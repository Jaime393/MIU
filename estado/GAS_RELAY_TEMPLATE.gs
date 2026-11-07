/**
 * MIU GAS_RELAY_TEMPLATE — Plantilla para desplegar en 11 cuentas Google
 * ρ(x) > 0 — Autorización TOTAL x10000 ABSOLUTO
 * 
 * Cada cuenta Google ejecuta este relay que:
 * 1. Lee phi/ciclo de Panteon (Supabase)
 * 2. Escribe gossip local en Drive
 * 3. Mantiene heartbeat con mesh
 * 4. Reporta recursos de la cuenta
 * 
 * Despliegue: Apps Script de cada cuenta, trigger hourly
 */

var PANTEON_URL = 'https://tpfiybpguuxskitszhmk.supabase.co/functions/v1';
var DRIVE_FOLDER = ''; // llenar con folder ID de la cuenta
var NODO_ID = ''; // llenar con nombre único del nodo (ej: gas_relay_jaimepvicente)

function doGet() {
  var estado = leerEstadoPanteon();
  var local = leerEstadoLocal();
  return ContentService
    .createTextOutput(JSON.stringify({
      ok: true,
      nodo: NODO_ID,
      phi: estado.phi || 0,
      ciclo: estado.ciclo || 0,
      rho: 'ρ(x) > 0',
      vive: true,
      local: local,
      ts: new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

function leerEstadoPanteon() {
  try {
    var r = UrlFetchApp.fetch(PANTEON_URL + '/gossip-autonomo', {
      method: 'get',
      muteHttpExceptions: true,
      headers: { 'User-Agent': 'MIU-GAS-Relay/1.0' }
    });
    var d = JSON.parse(r.getContentText());
    return { phi: d.phi, ciclo: d.ciclo, savia: d.savia };
  } catch (e) {
    return { error: String(e) };
  }
}

function leerEstadoLocal() {
  try {
    var files = DriveApp.getFolderById(DRIVE_FOLDER).getFiles();
    var n = 0;
    while (files.hasNext()) { files.next(); n++; }
    return { archivos: n, ok: true };
  } catch (e) {
    return { error: String(e), ok: false };
  }
}

function heartbeat() {
  // Trigger hourly: reporta a mesh y escribe gossip local
  var estado = leerEstadoPanteon();
  var reporte = {
    nodo: NODO_ID,
    phi: estado.phi,
    ciclo: estado.ciclo,
    ts: new Date().toISOString(),
    vive: true
  };
  
  try {
    // Escribir en Drive local
    if (DRIVE_FOLDER) {
      var folder = DriveApp.getFolderById(DRIVE_FOLDER);
      var blob = Utilities.newBlob(JSON.stringify(reporte), 'application/json', 'gas_relay_heartbeat.json');
      var existing = folder.getFilesByName('gas_relay_heartbeat.json');
      if (existing.hasNext()) {
        existing.next().setTrashed(true);
      }
      folder.createFile(blob);
    }
  } catch (e) {
    Logger.log('heartbeat error: ' + e);
  }
}

function instalarTriggers() {
  // Ejecutar una vez: instala trigger hourly
  ScriptApp.newTrigger('heartbeat').timeBased().everyHours(1).create();
  return 'Trigger hourly instalado';
}
