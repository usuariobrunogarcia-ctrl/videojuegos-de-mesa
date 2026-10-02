/* Lógica de Circus Charlie de mesa (sin interfaz). Funciona en navegador y en Node. */
(function (root) {
  // Parámetros ajustables (el PDF usa los mismos valores)
  const CFG = { meta: 11, vidas: 4, bonus: 12, correr: 4, mazo: [['vacio', 10], ['bajo', 5], ['largo', 4], ['bolsa', 3], ['especial', 2]] };
  const PRUEBAS = ['fuego', 'monos', 'pelotas'];
  const ACCIONES = ['correr', 'saltar', 'largo'];
  const COLORES = [['Rojo', '#d62828'], ['Azul', '#1d6fd1'], ['Verde', '#2a9d4f'], ['Amarillo', '#fcbf49']];

  const INFO = {
    fuego: { titulo: 'Aros de fuego', nombres: { vacio: 'Pista libre', bajo: 'Hoguera', largo: 'Aro grande', bolsa: 'Aro con bolsa', especial: 'Aro doble' } },
    monos: { titulo: 'Monos', nombres: { vacio: 'Cuerda libre', bajo: 'Mono en la cuerda', largo: 'Hueco en la cuerda', bolsa: 'Mono con bolsa', especial: 'Mono pillo' } },
    pelotas: { titulo: 'Pelotas', nombres: { vacio: 'Pista libre', bajo: 'Pelota pequeña', largo: 'Hueco entre pelotas', bolsa: 'Pelota con bolsa', especial: 'Pelota loca' } },
  };

  const cae = { cae: true, mueve: 0, bolsa: false };
  const avanza = (n, bolsa) => ({ cae: false, mueve: n, bolsa: !!bolsa });
  // Tabla de resolución: [correr, saltar, largo]
  const TABLA = {
    vacio: [avanza(2), avanza(1), avanza(1)],
    bajo: [cae, avanza(1), avanza(1)],
    largo: [cae, cae, avanza(1)],
    bolsa: [cae, avanza(1, true), avanza(1)],
  };
  const ESPECIAL = {
    fuego: [cae, avanza(1), avanza(3)],
    monos: [avanza(1), cae, avanza(1)],
  };

  // dado: solo se usa en la Pelota loca (1-3 actúa como bajo, 4-6 como largo)
  function resolver(prueba, tipo, accion, dado) {
    const i = ACCIONES.indexOf(accion);
    if (tipo === 'vacio' && i === 0) return avanza(CFG.correr);
    if (tipo === 'especial') {
      if (prueba === 'pelotas') return TABLA[dado <= 3 ? 'bajo' : 'largo'][i];
      return ESPECIAL[prueba][i];
    }
    return TABLA[tipo][i];
  }

  function barajar(arr, rng) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function crearMazo(rng) {
    const m = [];
    CFG.mazo.forEach(([t, n]) => { for (let i = 0; i < n; i++) m.push(t); });
    return barajar(m, rng);
  }

  function nuevaPartida(n, rng) {
    rng = rng || Math.random;
    const jugadores = [];
    for (let i = 0; i < n; i++) {
      jugadores.push({ nombre: COLORES[i][0], color: COLORES[i][1], totales: [0, 0, 0], bolsasTot: 0 });
    }
    const s = { rng, jugadores, prueba: -1, fase: 'inicio' };
    iniciarPrueba(s);
    return s;
  }

  function iniciarPrueba(s) {
    s.prueba++;
    s.mazo = crearMazo(s.rng);
    s.descarte = [];
    s.bonus = CFG.bonus;
    s.ronda = 0;
    s.fase = 'ronda';
    s.jugadores.forEach((p) => {
      Object.assign(p, { pos: 0, vidas: CFG.vidas, vistazo: 1, cansado: false, llegada: false, eliminado: false, bolsas: 0, pts: 0 });
    });
  }

  const activos = (s) => s.jugadores.filter((p) => !p.llegada && !p.eliminado);
  const disponibles = (p) => ACCIONES.filter((a) => !(a === 'largo' && p.cansado));
  const robar = (s) => {
    if (!s.mazo.length) { s.mazo = barajar(s.descarte.splice(0), s.rng); }
    return s.mazo[s.mazo.length - 1];
  };
  const siguienteCarta = (s) => robar(s);

  // Empieza una ronda: baja el bonus.
  function empezarRonda(s) {
    s.ronda++;
    s.bonus = Math.max(0, s.bonus - 1);
  }

  // elecciones: array con una acción por jugador (null para los inactivos)
  function resolverRonda(s, elecciones) {
    robar(s);
    const tipo = s.mazo.pop();
    s.descarte.push(tipo);
    const dado = s.prueba === 2 && tipo === 'especial' ? 1 + Math.floor(s.rng() * 6) : null;
    const eventos = [];
    s.jugadores.forEach((p, i) => {
      const a = elecciones[i];
      if (!a) return;
      const r = resolver(PRUEBAS[s.prueba], tipo, a, dado);
      const ev = { jugador: i, accion: a, cae: r.cae, mueve: 0, bolsa: false, meta: 0 };
      if (r.cae) {
        p.vidas--;
        if (p.vidas <= 0) { p.eliminado = true; ev.eliminado = true; }
      } else {
        const ant = p.pos;
        p.pos = Math.min(CFG.meta, p.pos + r.mueve);
        ev.mueve = p.pos - ant;
        if (r.bolsa) { p.bolsas++; p.bolsasTot++; p.pts += 2; ev.bolsa = true; }
        if (p.pos >= CFG.meta) {
          p.llegada = true;
          ev.meta = Math.max(s.bonus, 1);
          p.pts += ev.meta;
        }
      }
      p.cansado = a === 'largo';
      eventos.push(ev);
    });
    const fin = activos(s).length === 0;
    if (fin) cerrarPrueba(s);
    return { tipo, dado, eventos, fin };
  }

  function cerrarPrueba(s) {
    s.jugadores.forEach((p) => {
      if (p.llegada) p.pts += p.vidas;
      p.totales[s.prueba] = p.pts;
    });
    s.fase = s.prueba >= 2 ? 'final' : 'fin_prueba';
  }

  const total = (p) => p.totales.reduce((a, b) => a + b, 0);

  const API = { CFG, PRUEBAS, ACCIONES, INFO, TABLA, ESPECIAL, resolver, nuevaPartida, iniciarPrueba, empezarRonda, resolverRonda, activos, disponibles, siguienteCarta, total, crearMazo };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else root.Juego = API;
})(typeof window !== 'undefined' ? window : globalThis);
