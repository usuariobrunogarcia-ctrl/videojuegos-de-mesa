# Circus Charlie — Plan de diseño

> Estado: **decisiones tomadas, plan listo para pasar a PDF**.
>
> Decisiones: 1 o más jugadores · mucho azar · 3 pruebas (aros de fuego, monos, pelotas) · estilo pixel art.

## 1. El "latido" del videojuego

Circus Charlie (Konami, 1984) es una carrera de obstáculos en la que el
jugador **solo controla el momento del salto**. Lo que lo hace tenso:

1. **Pantalla que avanza sola**: no decides si avanzar, decides cuándo saltar.
2. **Reloj de bonus**: los puntos del bonus bajan constantemente; ir rápido
   paga, pero arriesga.
3. **Obstáculos que castigan el mal timing**: fuego, huecos, monos, pelotas.
4. **Saltos de riesgo**: coger una bolsa de puntos o un aro de fuego da más
   puntos, pero exige saltar en el momento exacto.
5. **Varias pruebas de circo** con una mecánica distinta cada una.
6. **Vidas y meta**: llegar a la plataforma final, o perder una vida.

## 2. Idea central de la traducción

**Pantalla que scrollea → mazo de obstáculos que se revela.**
Cada ronda se voltea una carta del mazo de la prueba: esa carta es lo que
"entra por la derecha de la pantalla".

**Reflejos → decisión simultánea y secreta.**
Todos eligen a la vez y en secreto una acción (Correr / Saltar / Salto largo).
Se revelan juntos. Sustituye al botón de salto: el "timing" se convierte en
anticipar qué viene en la fila de cartas visibles.

**Reloj → ficha en un marcador de bonus** que baja cada ronda.

## 3. Estructura de la partida

- **Jugadores:** 1 o más (1–4). Con 1 jugador intentas batir tu récord de puntos; con 2+ gana quien más puntos sume.
- **Azar:** alto. El mazo se baraja siempre y los obstáculos son impredecibles; la habilidad está en gestionar el riesgo, no en memorizar.
- **Duración:** 15–20 min (3 pruebas) o una prueba suelta en 5–8 min.
- **Una partida = una secuencia de pruebas.** Cada prueba tiene su propio
  mazo, tablero y regla especial.

### Pruebas (3)

| Prueba | Mecánica original | Traducción de mesa |
|---|---|---|
| **1. Aros de fuego** | Saltar aros de fuego y hogueras sobre un león | Pista de casillas. Cartas: aro, hoguera, aro+bolsa de puntos. Saltar un aro con bolsa da bonus extra |
| **2. Monos** | Avanzar por la cuerda floja saltando monos | Pista estrecha: fallar un salto = caída (pierdes vida). Los monos salen al azar, en carriles alto o bajo |
| **3. Pelotas** | Saltar de pelota en pelota | Fichas de pelota de distinta velocidad (dado); hay que "aterrizar" en una al saltar |

Cada prueba se puede jugar suelta o encadenada en el orden 1 → 2 → 3.

## 4. Reglas base (primera propuesta)

**Preparación:** cada jugador tiene un peón de Charlie, 3 vidas y un mazo de
acción propio (3 cartas: Correr, Saltar, Salto largo). Se baraja el mazo de la
prueba y se revelan las **3 próximas cartas** (visibles = lo que viene).

**Una ronda:**
1. Se avanza el marcador de bonus 1 punto hacia abajo.
2. Todos eligen en secreto una carta de acción y las revelan a la vez.
3. Se resuelve la carta de obstáculo actual contra cada jugador:
   - **Correr:** avanza 2 casillas. Falla si hay obstáculo.
   - **Saltar:** esquiva obstáculo corto. Avanza 1.
   - **Salto largo:** esquiva obstáculo largo/hueco. Avanza 1; no se puede
     usar dos rondas seguidas (cansancio).
4. Quien falla pierde una vida y no avanza.
5. Se voltea la siguiente carta de obstáculo.

**Fin de prueba:** el primero en llegar a la meta se lleva el bonus que quede
en el marcador; el resto cobra la mitad. Se suman puntos de bolsas y combos.

**Fin de partida:** tras la última prueba, gana quien tenga más puntos (en solitario, compara con tu récord). Sin
vidas = eliminado de esa prueba (vuelve en la siguiente con 1 vida).

## 5. Componentes (lista inicial para el PDF)

- 3 tableros de prueba (pista de casillas, una hoja A4 por prueba), en pixel art.
- Peones de Charlie en cartón (4 colores) con peana.
- Mazo de obstáculos por prueba (≈ 24 cartas c/u, con repetidos para el azar).
- 1 dado (d6) para velocidad de pelotas y eventos.
- Mazo de acciones (3 cartas × 4 jugadores).
- Marcador de bonus + ficha.
- Fichas de vida, de bolsas de puntos y de multiplicador.
- Hoja de reglas de 1 página.

Todo en A4 monocromo-friendly, para imprimir en casa y recortar.

## 6. Versión digital (fase 3)

Web simple (HTML + JS, sin dependencias) que implementa las mismas reglas con
cartas y tablero visuales. Sirve para **probar y equilibrar** antes de imprimir:
simular cientos de partidas y ver si ganar siempre es del que corre o del que
salta.

## 7. Decisiones tomadas

1. **Jugadores:** 1 o más.
2. **Azar:** alto.
3. **Pruebas:** aros de fuego, monos y pelotas.
4. **Estilo gráfico:** pixel art (paleta limitada, sprites de 16×16 ampliados).
5. **Idioma:** español.

## 8. Siguientes pasos

1. ✅ Plan ajustado con tus decisiones.
2. Genero el PDF de piezas imprimibles (`print/`).
3. Construyo la versión digital jugable (`digital/`).
