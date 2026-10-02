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

## 4. Reglas finales (las que implementa el PDF)

Reglamento completo en la primera página de
[`print/circus-charlie-imprimible.pdf`](print/circus-charlie-imprimible.pdf). Resumen:

- **Pista** de 20 casillas (0 = salida, 19 = meta), 3 corazones por jugador y prueba.
- **Ronda:** (1) baja el bonus 1 (empieza en 10); (2) todos eligen en secreto
  Correr / Saltar / Salto largo; (3) se voltea el obstáculo y se resuelve.
- **Vistazo:** una ficha por jugador y prueba para mirar en secreto la carta
  superior del mazo antes de elegir (es la forma de gestionar el azar).
- **Cansancio:** tras un Salto largo, esa carta no se puede jugar la ronda siguiente.
- **Caer:** -1 corazón y no avanzas. Con 0 corazones, eliminado de la prueba.
- **Mazo de 24 cartas por prueba:** 5 libres, 7 bajos, 5 largos, 4 con bolsa, 3 especiales.
- **Puntos:** llegar a meta = valor del bonus en ese momento (mín. 1) + 1 por
  corazón restante + 2 por cada bolsa. Gana quien más puntos sume en las 3 pruebas.
- **Pelota loca** (prueba 3): se tira un d6 (1-3 actúa como obstáculo bajo, 4-6 como largo).

Cambios respecto al borrador: se eliminan los multiplicadores y las fichas de
pelota (las sustituyen la carta *Pelota loca* y el d6) y todos empiezan cada
prueba con 3 vidas.

## 5. Componentes (contenido del PDF, 17 páginas A4)

| Páginas | Contenido |
|---|---|
| 1 | Reglamento |
| 2-4 | Tableros: Aros de fuego, Monos, Pelotas |
| 5 | 4 peones de Charlie recortables |
| 6 | Fichas (vidas, bolsas, vistazo, bonus) y hoja de puntuación |
| 7-15 | 72 cartas de obstáculo (3 mazos de 24, 63×88 mm) |
| 16-17 | 12 cartas de acción (3 por jugador) |

El PDF se regenera con `python3 print/generate.py` (requiere `reportlab`).

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

> Estado: fase 2 (PDF) hecha; falta la fase 3 (versión digital).
