// Simulador de equilibrio: node simulate.js
// Cada estrategia "correr p" elige Correr con probabilidad p; si no, alterna Saltar / Salto largo.
const J = require('./game.js');
function rng(seed) { let a = seed; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function estrategia(pc) {
  return (p, r) => {
    if (r() < pc) return 'correr';
    if (!J.disponibles(p).includes('largo')) return 'saltar';
    return r() < 0.5 ? 'largo' : 'saltar';
  };
}
function simular(pc, N = 2000) {
  let pruebas = 0, meta = 0, pts = 0, rondas = 0;
  const f = estrategia(pc);
  for (let g = 0; g < N; g++) {
    const r = rng(g + 1), s = J.nuevaPartida(1, r);
    for (;;) {
      const pr = s.prueba;
      for (;;) {
        J.empezarRonda(s);
        const el = s.jugadores.map((p) => (p.llegada || p.eliminado ? null : f(p, r)));
        if (J.resolverRonda(s, el).fin) break;
      }
      const p = s.jugadores[0];
      pruebas++; meta += p.llegada ? 1 : 0; pts += p.totales[pr]; rondas += s.ronda;
      if (s.fase === 'final') break;
      J.iniciarPrueba(s);
    }
  }
  return { meta: (100 * meta / pruebas).toFixed(0) + '%', puntos: (pts / pruebas).toFixed(1), rondas: (rondas / pruebas).toFixed(1) };
}
console.log('Configuración:', JSON.stringify(J.CFG));
for (const pc of [0, 0.2, 0.4, 0.6, 0.8, 1]) console.log('prob. correr', pc, simular(pc));
