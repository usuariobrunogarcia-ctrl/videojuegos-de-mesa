# Videojuegos de mesa

Convertir videojuegos clásicos en juegos de mesa que replican la experiencia
original **sin pantalla ni electrónica**: el propio tablero, las cartas y los
dados hacen el trabajo de la máquina.

## Flujo de trabajo por juego

Cada juego vive en `games/<nombre>/` y pasa por tres fases, en este orden:

1. **Planificación** (`PLAN.md`): qué hace especial al videojuego, cómo se
   traduce a mecánicas físicas, componentes y reglas. Se aprueba antes de seguir.
2. **Piezas imprimibles** (`print/`): PDF con tablero, cartas y fichas listos
   para imprimir y recortar.
3. **Versión digital jugable** (`digital/`): una versión web para probar y
   equilibrar las reglas.

## Principio de diseño

No copiamos las reglas del videojuego: copiamos su **sensación**. La CPU se
sustituye por reglas automáticas y deterministas (mazos, patrones, dados).

## Juegos

| Juego | Planificación | PDF imprimible | Versión digital |
|---|---|---|---|
| [Circus Charlie](games/circus-charlie/PLAN.md) | ✅ Aprobado | ⏳ | ⏳ |
