/**
 * MIU D_f Calculator — Power-Law Fitting Tool
 * github.com/Jaime393/MIU | DOI 10.5281/zenodo.20547558
 * REGLA: Solo D_f legitimo. K_i circular (corr=1.0 tautologica).
 */
function powerLawFit(xArr, yArr) {
  const logX = xArr.map(x => Math.log(Math.abs(x)));
  const logY = yArr.map(y => Math.log(Math.abs(y)));
  const n = logX.length;
  if (n < 3) return { error: 'Need at least 3 points', n };
  const mean = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
  const mx = mean(logX), my = mean(logY);
  let num = 0, den = 0;
  for (let i = 0; i < n; i++) { num += (logX[i]-mx)*(logY[i]-my); den += (logX[i]-mx)**2; }
  if (den === 0) return { error: 'Degenerate data', n };
  const alpha = num / den;
  const ic = my - alpha * mx;
  const pred = logX.map(x => alpha*x+ic);
  const ssTot = logY.reduce((a,y) => a+(y-my)**2, 0);
  const ssRes = logY.reduce((a,y,i) => a+(y-pred[i])**2, 0);
  const r2 = ssTot===0 ? 0 : 1-ssRes/ssTot;
  const df = Math.abs(alpha);
  const rango = df<1.2?'LINEAL':df<1.5?'FRACTAL-BAJO':df<1.8?'FRACTAL-MEDIO':df<2.0?'FRACTAL-ALTO':'HIPERESCALADO';
  return { alpha:+alpha.toFixed(6), r2:+r2.toFixed(4), dfValue:+df.toFixed(4), n, rango };
}
if (typeof module!=='undefined') module.exports={powerLawFit};