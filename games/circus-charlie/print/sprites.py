"""Sprites en pixel art (cuadrículas de caracteres) y utilidades de dibujo."""
import math

PAL = {
    'K': '#1a1a2e', 'W': '#ffffff', 'R': '#d62828', 'O': '#f77f00',
    'Y': '#fcbf49', 'G': '#2a9d4f', 'B': '#1d6fd1', 'N': '#8b5a2b',
    'S': '#f2c29b', 'T': '#e0b04c', 'D': '#555566', 'L': '#c9c9d4',
    'V': '#7b4fd0', 'C': '#5ec8e5', 'H': '#ff8fab',
}

CHARLIE = [
    ".....WW.....",
    "....aaaa....",
    "...aaaaaa...",
    "..KKKKKKKK..",
    "...SSSSSS...",
    "...SKSSKS...",
    "...SSRRSS...",
    "....SSSS....",
    "..aaaaaaaa..",
    ".SaaaWWaaaS.",
    ".SaaaWWaaaS.",
    "..aaaaaaaa..",
    "...aa..aa...",
    "...aa..aa...",
    "..KKK..KKK..",
    "..KKK..KKK..",
]

HOGUERA = [
    ".....Y......",
    "....YOY.....",
    "...YOROY....",
    "..YORRROY...",
    "..OORRRROO..",
    ".OORRYYRROO.",
    ".OORYYYYROO.",
    "..KKKKKKKK..",
    "..KDDDDDDK..",
    "...KDDDDK...",
    "...KDDDDK...",
    "..KKKKKKKK..",
]

BOLSA = [
    "....K..K....",
    ".....KK.....",
    "....KRRK....",
    "...KTTTTK...",
    "..KTTTKTTK..",
    ".KTTTKKKTTK.",
    ".KTTTKTTTTK.",
    ".KTTTTKKTTK.",
    ".KTTTTTKTTK.",
    ".KTTKKKKTTK.",
    "..KTTTKTTK..",
    "...KKKKKK...",
]

MONO = [
    "..NNN..NNN..",
    ".NNNNNNNNNN.",
    ".NNSSSSSSNN.",
    "NNNSKSSKSNNN",
    ".NNSSSSSSNN.",
    "..NSSRRSSN..",
    "...NSSSSN...",
    "..NNNNNNNN..",
    ".NNNNNNNNNN.",
    "NN.NNNNNN.NN",
    "NN.NNNNNN.NN",
    "...NN..NN...",
    "...NN..NN...",
    "..KK....KK..",
]

CORAZON = [
    ".KK...KK.",
    "KRRK.KRRK",
    "KRWRKRRRK",
    "KRRRRRRRK",
    ".KRRRRRK.",
    "..KRRRK..",
    "...KRK...",
    "....K....",
]

OJO = [
    "...KKKKK...",
    ".KKWWWWWKK.",
    "KWWWBBBWWWK",
    "KWWBBKBBWWK",
    ".KKWBBBWKK.",
    "...KKKKK...",
]

NUBE = [
    "...WWW......",
    "..WWWWW.WW..",
    ".WWWWWWWWWW.",
    "WWWWWWWWWWWW",
]


def ring(n=16):
    g = []
    c = (n - 1) / 2
    for y in range(n):
        row = ''
        for x in range(n):
            d = math.hypot(x - c, y - c)
            if d > c + 0.2:
                row += '.'
            elif d >= c - 1.0:
                row += 'R'
            elif d >= c - 2.0:
                row += 'O'
            elif d >= c - 3.0:
                row += 'Y'
            else:
                row += '.'
        g.append(row)
    return g


def ball(n=14):
    g = []
    c = (n - 1) / 2
    for y in range(n):
        row = ''
        for x in range(n):
            d = math.hypot(x - c, y - c)
            if d > c + 0.2:
                row += '.'
            elif d >= c - 1.0:
                row += 'K'
            else:
                row += 'R' if ((x + y) // 3) % 2 == 0 else 'W'
        g.append(row)
    return g


def sprite_size(grid):
    return max(len(r) for r in grid), len(grid)


def draw_sprite(c, grid, x, y, px, pal=None, flip=False):
    """Dibuja el sprite con esquina inferior izquierda en (x, y)."""
    palette = dict(PAL)
    if pal:
        palette.update(pal)
    w, h = sprite_size(grid)
    for r, row in enumerate(grid):
        row = row.ljust(w, '.')
        if flip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch == '.':
                continue
            col = palette[ch]
            c.setFillColor(col)
            c.setStrokeColor(col)
            c.setLineWidth(0.25)
            c.rect(x + i * px, y + (h - 1 - r) * px, px, px, stroke=1, fill=1)
    return w * px, h * px
