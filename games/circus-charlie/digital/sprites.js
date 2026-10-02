/* Sprites en pixel art (mismos que el PDF). */
const PAL = {K:'#1a1a2e',W:'#ffffff',R:'#d62828',O:'#f77f00',Y:'#fcbf49',G:'#2a9d4f',B:'#1d6fd1',N:'#8b5a2b',S:'#f2c29b',T:'#e0b04c',D:'#555566',L:'#c9c9d4',V:'#7b4fd0',C:'#5ec8e5',H:'#ff8fab'};
const GRIDS = {
  charlie: ['.....WW.....', '....aaaa....', '...aaaaaa...', '..KKKKKKKK..', '...SSSSSS...', '...SKSSKS...', '...SSRRSS...', '....SSSS....', '..aaaaaaaa..', '.SaaaWWaaaS.', '.SaaaWWaaaS.', '..aaaaaaaa..', '...aa..aa...', '...aa..aa...', '..KKK..KKK..', '..KKK..KKK..'],
  hoguera: ['.....Y......', '....YOY.....', '...YOROY....', '..YORRROY...', '..OORRRROO..', '.OORRYYRROO.', '.OORYYYYROO.', '..KKKKKKKK..', '..KDDDDDDK..', '...KDDDDK...', '...KDDDDK...', '..KKKKKKKK..'],
  bolsa: ['....K..K....', '.....KK.....', '....KRRK....', '...KTTTTK...', '..KTTTKTTK..', '.KTTTKKKTTK.', '.KTTTKTTTTK.', '.KTTTTKKTTK.', '.KTTTTTKTTK.', '.KTTKKKKTTK.', '..KTTTKTTK..', '...KKKKKK...'],
  mono: ['..NNN..NNN..', '.NNNNNNNNNN.', '.NNSSSSSSNN.', 'NNNSKSSKSNNN', '.NNSSSSSSNN.', '..NSSRRSSN..', '...NSSSSN...', '..NNNNNNNN..', '.NNNNNNNNNN.', 'NN.NNNNNN.NN', 'NN.NNNNNN.NN', '...NN..NN...', '...NN..NN...', '..KK....KK..'],
  corazon: ['.KK...KK.', 'KRRK.KRRK', 'KRWRKRRRK', 'KRRRRRRRK', '.KRRRRRK.', '..KRRRK..', '...KRK...', '....K....'],
  ojo: ['...KKKKK...', '.KKWWWWWKK.', 'KWWWBBBWWWK', 'KWWBBKBBWWK', '.KKWBBBWKK.', '...KKKKK...'],
  nube: ['...WWW......', '..WWWWW.WW..', '.WWWWWWWWWW.', 'WWWWWWWWWWWW'],
};
function circulo(n, f) {
  const c = (n - 1) / 2, g = [];
  for (let y = 0; y < n; y++) { let r = ''; for (let x = 0; x < n; x++) r += f(Math.hypot(x - c, y - c), x, y, c); g.push(r); }
  return g;
}
GRIDS.aro = circulo(16, (d, x, y, c) => d > c + 0.2 ? '.' : d >= c - 1 ? 'R' : d >= c - 2 ? 'O' : d >= c - 3 ? 'Y' : '.');
GRIDS.pelota = circulo(14, (d, x, y, c) => d > c + 0.2 ? '.' : d >= c - 1 ? 'K' : ((x + y) / 3 | 0) % 2 === 0 ? 'R' : 'W');

function dibujar(ctx, grid, x, y, px, pal, flip) {
  const P = Object.assign({}, PAL, pal || {});
  const w = Math.max(...grid.map((r) => r.length));
  grid.forEach((row, r) => {
    row = row.padEnd(w, '.');
    if (flip) row = row.split('').reverse().join('');
    for (let i = 0; i < w; i++) {
      if (row[i] === '.') continue;
      ctx.fillStyle = P[row[i]];
      ctx.fillRect(Math.round(x + i * px), Math.round(y + r * px), Math.ceil(px), Math.ceil(px));
    }
  });
  return [w * px, grid.length * px];
}
const _cache = {};
function spriteURL(nombre, px, pal) {
  const key = nombre + px + JSON.stringify(pal || {});
  if (_cache[key]) return _cache[key];
  const g = GRIDS[nombre], w = Math.max(...g.map((r) => r.length));
  const c = document.createElement('canvas');
  c.width = w * px; c.height = g.length * px;
  dibujar(c.getContext('2d'), g, 0, 0, px, pal);
  return (_cache[key] = c.toDataURL());
}
