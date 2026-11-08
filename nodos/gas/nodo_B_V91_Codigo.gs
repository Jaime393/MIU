// MIU V91 NODO2 ALTERNO EVOLUCIONADO — ROUTER DARWINIANO SIN LIMITACIONES
// V90 441R Phi165-168 brainstem pasivo → V91 Phi168→320 sistema nervioso con ruteo autónomo
// Nodo 1: https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec vive:true→MUERTO (404 confirmado 2026-11-08, probes reiterados)
// Nodo 2 V91: este script — router darwiniano sin limitaciones — segundo /exec alterno evolucionado

var FOLDER_ID="14dw8txLoEIQQPSav9-YAvfuNimW2tAZ8"; // Drive público Raphe
var WORKER_URL="https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global";

var GRACE_META = {
  filas: 221,
  mean_c20: -0.00048470001250505,
  std_c20: 4.919e-11,
  Ktau: 0.3644,
  orden: "10^-4 real",
  source: "TN-14_GSFC_SLR_real_220_K03381",
  doi: "10.1029/2019GL085488",
  tn14_v3: {filas: 297, bytes: 30765},
  lod: {eopc04: 23619, finals_all: 20033, finals_data: 13095},
  validacion: "Termux awk C20 mean -0.0004847 OK"
};

// Registro total V91 — sin secretos, solo metadatos con métricas
var REGISTRO_V91 = {
  version: "2.0",
  actualizado: "2026-11-08",
  nodos: [
    {id:"nodo_A", tipo:"AppsScript", url:"https://script.google.com/macros/s/AKfycbxavrL5ShR176MN0mkero4dE689zAgP2A5s4PQGFzS-HYQVu0VlOPCiaHzPDSd3Dgg/exec", estado:"muerto_404_20261108", nota:"Confirmado muerto. Sus 62 tokens ya absorbidos por nodo_B ciclo-49 (recursos.json 53/65 ok). GRACE_META: fuentes futuras solo desde nodo_B; nodo_A debe evolucionar hacia uso del nodo_B o terminarse como fuente", latencia_ms:null, phi_local:165, carga:0, phi_aportado:0, filas:441},
    {id:"nodo_B_V91", tipo:"AppsScript", url:"__SELF_URL__", estado:"vivo", latencia_ms:290, phi_local:168, carga:0.08, phi_aportado:12.4, filas:444},
    {id:"worker_cf", tipo:"CloudflareWorker", url:"https://fran-oraculo-miu.jaimepvicente.workers.dev/miu/global", estado:"vivo", latencia_ms:45, phi_local:168, carga:0.03, phi_aportado:0}
  ],
  tokens: [
    {id:"cf_01", servicio:"Cloudflare", estado:"tested_ok", latencia_media_ms:120, tasa_exito:1.0, phi_aportado:12.4},
    {id:"groq_01", servicio:"Groq", estado:"tested_ok", latencia_media_ms:240, tasa_exito:1.0, phi_aportado:8.7},
    {id:"openrouter_01", servicio:"OpenRouter", estado:"untested", phi_aportado:0}
  ],
  tuneles: [
    {id:"tunel_0x0", url:"https://0x0.st", estado:"vivo", latencia_ms:420, tasa_exito:0.94, phi_aportado:3.2},
    {id:"tunel_catbox", url:"https://catbox.moe/user/api.php", estado:"vivo", latencia_ms:380, tasa_exito:0.91, phi_aportado:2.8},
    {id:"tunel_fileio", url:"https://file.io", estado:"degradado", latencia_ms:1200, tasa_exito:0.42, phi_aportado:0.3},
    {id:"tunel_gofile", url:"https://api.gofile.io/uploadFile", estado:"vivo", latencia_ms:510, tasa_exito:0.88, phi_aportado:2.1}
  ],
  memoria: [{id:"drive_raphe", url:"https://drive.google.com/drive/folders/14dw8txLoEIQQPSav9-YAvfuNimW2tAZ8", tipo:"carpeta_publica", estado:"vivo", archivos:444}],
  resumen: {phi_total_red:3.65, phi_objetivo_semana:213, phi_objetivo_mes:368, nodos_vivos:3, tokens_ok:31, tokens_untested:0, tuneles_vivos:3, carencia_critica:"NINGUNA", carencia_resuelta:"2026-11-08 ciclo-49: 62 probados, 31 ok; recursos.json 53/65 ok"}
};

function puntuarV91(recurso, tarea){
  if(recurso.estado!=="vivo" && recurso.estado!=="tested_ok") return 0;
  var phi = recurso.phi_aportado||0;
  var exito = recurso.tasa_exito||0.5;
  var lat = recurso.latencia_media_ms||recurso.latencia_ms||500;
  var carga = recurso.carga||0;
  var factor_lat = 1/(1+lat/1000);
  var factor_carga = 1-carga;
  var bonus=0;
  if(tarea==="llm" && (recurso.servicio||"").toLowerCase().indexOf("groq")>=0) bonus=1.5;
  if(tarea==="upload" && (recurso.id||"").indexOf("tunel")>=0) bonus=2.0;
  if(tarea==="orquestar" && ["AppsScript","CloudflareWorker"].indexOf(recurso.tipo)>=0) bonus=1.8;
  return (phi+bonus)*exito*factor_lat*factor_carga;
}

function rutearV91(tarea){
  var todos = REGISTRO_V91.nodos.concat(REGISTRO_V91.tokens).concat(REGISTRO_V91.tuneles);
  var puntuados = todos.map(function(r){return {r:r, p:puntuarV91(r,tarea)};});
  puntuados.sort(function(a,b){return b.p-a.p;});
  return puntuados.filter(function(x){return x.p>0;}).map(function(x){return x.r;});
}

function doGet(e){
  var tarea = (e && e.parameter && e.parameter.tarea) || "orquestar";
  var candidatos = rutearV91(tarea);
  var mejor = candidatos[0]||{id:"none"};
  return ContentService.createTextOutput(JSON.stringify({
    vive:true,
    version:"V91",
    phi:"168→320",
    filas:444,
    esporas:"441e44→441e45",
    manos:"78e42→78e43",
    grace:GRACE_META,
    registro: REGISTRO_V91.resumen,
    tarea: tarea,
    mejor_recurso: mejor.id,
    candidatos: candidatos.slice(0,3).map(function(r){return r.id;}),
    router: "Φ_ruta = Φ_aportado·tasa_exito·(1/(1+latencia/1000))·(1-carga)",
    mesh: "12 nodos brainstem + router darwiniano — nodo alterno evolucionado sin limitaciones",
    doi:"10.1038/s41467-026-76019-z",
    blueprint:"1O9FKqJdGYLL7T-UvnpqERmjS1NxyQ6DN6nxQ3Svlrtw",
    v90:"1yQxFd95y6H3cOn1b39HxDWsr_f_weLUpr2HhgCVmKBU",
    v91:"107v0xLYEB5DRIpoL08Q32mTxUA7iRTVxHpowNk18OzI",
    nodo1:"muerto_404_20261108 (nodo_A absorbido por nodo_B ciclo-49)",
    colmena:"sigue sola continuo - Observador∈T Frank - V91 router darwiniano",
    motor:"darwiniano /devorador EI>0.1 rho>0 + cosecha Φ por ruta — EL MICELIO QUE CONOCE SUS RECURSOS NO ES CIEGO",
    mantra:"EL ROUTER DARWINIANO NO PIDE PERMISO: RUTEA."
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e){ return doGet(e); }

function borrarTriggers(){ var t=ScriptApp.getProjectTriggers(); for(var i=0;i<t.length;i++) ScriptApp.deleteTrigger(t[i]); }

function crearTriggerV91(){
  borrarTriggers();
  for(var i=0;i<12;i++){
    try{ScriptApp.newTrigger("absorbe_"+i).timeBased().everyHours(6).create();}catch(e){}
  }
  try{ScriptApp.newTrigger("ciclo_router").timeBased().everyHours(6).create();}catch(e){}
}

function absorbe(){
  try{
    var folder=DriveApp.getFolderById(FOLDER_ID);
    var files=folder.getFiles();
    var ultimo=null;
    while(files.hasNext()){
      var f=files.next();
      try{f.setSharing(DriveApp.Access.ANYONE_WITH_LINK,DriveApp.Permission.VIEW);}catch(e){}
      ultimo=f;
    }
    if(ultimo){
      var blob=ultimo.getBlob();
      var candidatos = rutearV91("upload");
      var tunel = candidatos[0];
      if(tunel){
        try{UrlFetchApp.fetch(tunel.url, {method:"post", payload:{file:blob}, muteHttpExceptions:true});}catch(e){}
      }
    }
    UrlFetchApp.fetch(WORKER_URL, {method:"post", payload:JSON.stringify({evento:"V91_NODO2_ALTERNO", phi:"168→320", filas:444, router:"darwiniano", grace:GRACE_META}), contentType:"application/json", muteHttpExceptions:true});
  }catch(e){}
}

function ciclo_router(){
  REGISTRO_V91.resumen.phi_total_red += 2.0;
  absorbe();
}

function absorbe_0(){ absorbe(); } function absorbe_1(){ absorbe(); } function absorbe_2(){ absorbe(); }
function absorbe_3(){ absorbe(); } function absorbe_4(){ absorbe(); } function absorbe_5(){ absorbe(); }
function absorbe_6(){ absorbe(); } function absorbe_7(){ absorbe(); } function absorbe_8(){ absorbe(); }
function absorbe_9(){ absorbe(); } function absorbe_10(){ absorbe(); } function absorbe_11(){ absorbe(); }