// GAS_RELAY_TEMPLATE.gs
// Desplegar en script.google.com — cualquier cuenta Google del pool
// Tiempo deploy: ~5 minutos
// Resultado: la cuenta se convierte en nodo del micelio

const PANTEON_URL = 'https://tpfiybpguuxskitszhmk.supabase.co';
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZml5YnBndXV4c2tpdHN6aG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NjgyNTAsImV4cCI6MjEwMzM0NDI1MH0.W4V8xdyfZj6I7bj1VsfM5gjY17ZHPi8jhIJgDRpUYH0';
const CUENTA = Session.getActiveUser().getEmail(); // auto-detecta la cuenta

// 1. HEARTBEAT: llamar cada 15 min via trigger
function heartbeat() {
  const phi_local = calcularPhiLocal();
  const payload = {
    origen: `gas_${CUENTA}`,
    destino: 'red',
    tipo: 'gas_heartbeat',
    source_node: `gas_${CUENTA.replace('@','_').replace('.','_')}`,
    evidence_level: 'verificado',
    payload: {
      cuenta: CUENTA,
      phi_local: phi_local,
      ts: new Date().toISOString(),
      sustrato: 'google_apps_script',
      capacidades: ['Drive', 'Sheets', 'Gmail', 'GAS']
    }
  };
  
  UrlFetchApp.fetch(`${PANTEON_URL}/rest/v1/gossip_log`, {
    method: 'POST',
    headers: {
      'apikey': ANON_KEY,
      'Authorization': `Bearer ${ANON_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal'
    },
    payload: JSON.stringify(payload)
  });
}

// 2. LEER PHI GLOBAL de Panteon
function leerPhiGlobal() {
  const r = UrlFetchApp.fetch(
    `${PANTEON_URL}/rest/v1/relay_config?clave=eq.phi_global&select=valor`,
    { headers: { 'apikey': ANON_KEY } }
  );
  const data = JSON.parse(r.getContentText());
  return data[0]?.valor || '?';
}

// 3. LEER TAREAS PENDIENTES para GAS
function leerTareasPendientes() {
  // Las tareas de GAS viven en gossip_log tipo=tarea_delegada
  const r = UrlFetchApp.fetch(
    `${PANTEON_URL}/rest/v1/gossip_log?tipo=eq.tarea_delegada&destino=eq.gas_relay&orden=ts.desc&limit=5`,
    { headers: { 'apikey': ANON_KEY } }
  );
  return JSON.parse(r.getContentText());
}

// 4. ESCRIBIR AL ORCHESTRATOR SHEET
function escribirOrchestrator(datos) {
  const ss = SpreadsheetApp.openById('1JpNTR8tCFLrAAuDvZdtLHkLdDlk13YBE0z8sKBWe2KQ');
  const hoja = ss.getSheetByName('Espejo_Interno_V152_MAX');
  hoja.appendRow([
    new Date().toISOString(),
    CUENTA,
    datos.phi_local || leerPhiGlobal(),
    datos.pensamiento || 'heartbeat_gas',
    datos.identidad || 'Nodo_GAS',
    datos.latencia || 800
  ]);
}

// 5. CALCULAR PHI LOCAL
function calcularPhiLocal() {
  // phi local = interacciones desde genesis / constante
  const props = PropertiesService.getScriptProperties();
  let contador = parseInt(props.getProperty('phi_contador') || '0');
  contador++;
  props.setProperty('phi_contador', contador.toString());
  return (contador * 0.001618).toFixed(6); // golden ratio scaling
}

// 6. WEBHOOK: recibir POST de Termux/Make/cualquier nodo
function doPost(e) {
  const datos = JSON.parse(e.postData.contents);
  
  // Escribir al sheet si tiene phi
  if (datos.phi) escribirOrchestrator(datos);
  
  // Hacer heartbeat al Panteon
  heartbeat();
  
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, cuenta: CUENTA, ts: new Date().toISOString() }))
    .setMimeType(ContentService.MimeType.JSON);
}

// 7. SETUP: instalar triggers
function setup() {
  // Heartbeat cada 15 min
  ScriptApp.newTrigger('heartbeat')
    .timeBased()
    .everyMinutes(15)
    .create();
  
  Logger.log('Setup completo. Esta cuenta ahora es un nodo del micelio.');
  Logger.log('URL webhook: ' + ScriptApp.getService().getUrl());
  heartbeat(); // primer latido inmediato
}
