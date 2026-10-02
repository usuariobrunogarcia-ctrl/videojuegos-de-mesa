"""Genera el PDF imprimible de Circus Charlie de mesa (A4)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Spacer
from reportlab.lib.styles import ParagraphStyle
from sprites import *

W, H = A4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'circus-charlie-imprimible.pdf')
JUGADORES = [('Rojo', '#d62828'), ('Azul', '#1d6fd1'), ('Verde', '#2a9d4f'), ('Amarillo', '#fcbf49')]

PRUEBAS = {
    'fuego': dict(n=1, titulo='AROS DE FUEGO', main='#d94f1e', light='#ffe3cc', floor='#a33a14',
                  nombres=dict(vacio='Pista libre', bajo='Hoguera', largo='Aro grande',
                               bolsa='Aro con bolsa', especial='Aro doble')),
    'monos': dict(n=2, titulo='MONOS', main='#1d6fd1', light='#d8ecff', floor='#8b5a2b',
                  nombres=dict(vacio='Cuerda libre', bajo='Mono en la cuerda', largo='Hueco en la cuerda',
                               bolsa='Mono con bolsa', especial='Mono pillo')),
    'pelotas': dict(n=3, titulo='PELOTAS', main='#7b4fd0', light='#e6dcff', floor='#4b2f8f',
                    nombres=dict(vacio='Pista libre', bajo='Pelota pequeña', largo='Hueco entre pelotas',
                                 bolsa='Pelota con bolsa', especial='Pelota loca')),
}
MAZO = [('vacio', 5), ('bajo', 7), ('largo', 5), ('bolsa', 4), ('especial', 3)]
CAE = '¡Cae! -1 vida'
RESULT = {
    'vacio': ('Avanzas 2', 'Avanzas 1', 'Avanzas 1'),
    'bajo': (CAE, 'Avanzas 1', 'Avanzas 1'),
    'largo': (CAE, CAE, 'Avanzas 1'),
    'bolsa': (CAE, 'Avanzas 1 y bolsa (2 pts)', 'Avanzas 1'),
}
ESPECIAL = {
    'fuego': (CAE, 'Avanzas 1', 'Avanzas 3'),
    'monos': ('Avanzas 1', CAE, 'Avanzas 1'),
    'pelotas': (CAE, '1-3: avanzas 1 / 4-6: cae', 'Avanzas 1'),
}
DESC = {
    'vacio': 'Nada en el camino. Aprovecha para correr.',
    'bajo': 'Obstáculo bajo: hay que saltarlo.',
    'largo': 'Obstáculo largo: solo un salto largo lo supera.',
    'bolsa': 'Un salto corto recoge la bolsa de puntos.',
}
DESC_ESP = {
    'fuego': 'Dos aros seguidos: ¡el salto largo los pasa a la vez!',
    'monos': 'El mono salta contigo: no saltes corto.',
    'pelotas': 'Tira 1d6: 1-3 actúa como Pelota pequeña, 4-6 como Hueco.',
}


def hexc(s):
    return colors.HexColor(s)


def banner(c, titulo, sub, main, pre=None):
    c.setFillColor(hexc(main))
    c.rect(0, H - 120, W, 120, stroke=0, fill=1)
    c.setFillColor(colors.white)
    if pre:
        c.setFont('Helvetica-Bold', 14)
        c.drawString(42, H - 36, pre)
        c.setFont('Helvetica-Bold', 34)
        c.drawString(40, H - 72, titulo)
    else:
        c.setFont('Helvetica-Bold', 34)
        c.drawString(40, H - 62, titulo)
    c.setFont('Helvetica', 12)
    c.drawString(42, H - 100 if pre else H - 88, sub)


# ---------------------------------------------------------------- escenas
def escena(c, x, y, w, h, prueba, tipo):
    p = PRUEBAS[prueba]
    c.setFillColor(hexc(p['light']))
    c.setStrokeColor(colors.HexColor('#1a1a2e'))
    c.setLineWidth(1.2)
    c.rect(x, y, w, h, fill=1, stroke=1)
    draw_sprite(c, NUBE, x + w - 50, y + h - 24, 3.5, {'W': '#ffffff'})
    fl = y + 22
    c.setFillColor(hexc(p['floor']))
    if prueba == 'monos':
        pass
    else:
        c.rect(x + 1, y + 1, w - 2, 21, fill=1, stroke=0)
    draw_sprite(c, CHARLIE, x + 8, fl, 3.5, {'a': '#d62828'})
    cx = x + w * 0.42
    if prueba == 'monos':
        c.setStrokeColor(hexc(p['floor']))
        c.setLineWidth(3)
        gap = tipo == 'largo'
        if gap:
            c.line(x + 1, fl, cx + 8, fl)
            c.line(cx + 62, fl, x + w - 1, fl)
            c.setFillColor(colors.HexColor('#1a1a2e'))
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(cx + 35, fl - 14, 'v v v')
        else:
            c.line(x + 1, fl, x + w - 1, fl)
    if prueba == 'fuego':
        if tipo == 'bajo':
            draw_sprite(c, HOGUERA, cx + 10, fl, 5)
        elif tipo == 'largo':
            draw_sprite(c, ring(16), x + 62, fl, 4.8)
        elif tipo == 'bolsa':
            draw_sprite(c, ring(16), x + 60, fl, 4.5)
            draw_sprite(c, BOLSA, x + 78, fl + 18, 3)
        elif tipo == 'especial':
            draw_sprite(c, ring(16), x + 52, fl, 3.4)
            draw_sprite(c, ring(16), x + 98, fl, 3.4)
    elif prueba == 'monos':
        if tipo == 'bajo':
            draw_sprite(c, MONO, cx + 12, fl + 1, 5)
        elif tipo == 'bolsa':
            draw_sprite(c, MONO, x + 58, fl + 1, 4)
            draw_sprite(c, BOLSA, x + 112, fl + 1, 3.2)
        elif tipo == 'especial':
            draw_sprite(c, MONO, cx + 12, fl + 1, 5)
            c.setFillColor(hexc('#d62828'))
            c.setFont('Helvetica-Bold', 30)
            c.drawString(cx + 78, fl + 40, '!')
    else:
        if tipo == 'bajo':
            draw_sprite(c, ball(14), cx + 8, fl, 4.5)
        elif tipo == 'largo':
            c.setFillColor(hexc(p['light']))
            c.rect(x + 92, y + 1, 22, 21, fill=1, stroke=0)
            c.setFillColor(colors.HexColor('#1a1a2e'))
            c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(x + 103, y + 8, 'v v')
            draw_sprite(c, ball(14), x + 56, fl, 2.5)
            draw_sprite(c, ball(14), x + 118, fl, 2.5)
        elif tipo == 'bolsa':
            draw_sprite(c, ball(14), x + 56, fl, 3.5)
            draw_sprite(c, BOLSA, x + 110, fl, 3)
        elif tipo == 'especial':
            draw_sprite(c, ball(14), cx + 4, fl, 5)
            c.setFillColor(hexc('#fcbf49'))
            c.setStrokeColor(colors.HexColor('#1a1a2e'))
            c.setFont('Helvetica-Bold', 30)
            c.drawString(cx + 28, fl + 24, '?')
    if tipo == 'vacio':
        c.setFillColor(hexc(p['main']))
        c.setFont('Helvetica-Bold', 26)
        c.drawString(x + w * 0.55, fl + 14, '>>>')


def carta_obstaculo(c, x, y, cw, ch, prueba, tipo):
    p = PRUEBAS[prueba]
    c.setFillColor(colors.white)
    c.setStrokeColor(hexc(p['main']))
    c.setLineWidth(3)
    c.roundRect(x + 3, y + 3, cw - 6, ch - 6, 8, fill=1, stroke=1)
    c.setFillColor(hexc(p['main']))
    c.roundRect(x + 3, y + ch - 36, cw - 6, 33, 8, fill=1, stroke=0)
    c.rect(x + 3, y + ch - 36, cw - 6, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 12.5)
    c.drawCentredString(x + cw / 2, y + ch - 25, p['nombres'][tipo].upper())
    escena(c, x + 12, y + ch - 36 - 8 - 100, cw - 24, 100, prueba, tipo)
    c.setFillColor(colors.HexColor('#1a1a2e'))
    d = DESC_ESP[prueba] if tipo == 'especial' else DESC[tipo]
    fs = 7.5
    while pdfmetrics.stringWidth(d, 'Helvetica-Oblique', fs) > cw - 22:
        fs -= 0.25
    c.setFont('Helvetica-Oblique', fs)
    c.drawCentredString(x + cw / 2, y + ch - 36 - 8 - 100 - 12, d)
    res = ESPECIAL[prueba] if tipo == 'especial' else RESULT[tipo]
    for i, (nombre, r) in enumerate(zip(('CORRER', 'SALTAR', 'SALTO LARGO'), res)):
        ry = y + 66 - i * 23
        c.setFillColor(hexc('#eeeeee'))
        c.setStrokeColor(hexc('#1a1a2e'))
        c.setLineWidth(0.8)
        c.rect(x + 12, ry, cw - 24, 20, fill=1, stroke=1)
        c.setFillColor(hexc(p['main']))
        c.rect(x + 12, ry, 62, 20, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(x + 43, ry + 7, nombre)
        c.setFillColor(hexc('#b00020') if r.startswith('¡Cae') else hexc('#12602a'))
        c.setFont('Helvetica-Bold', 7.4 if len(r) < 20 else 6.2)
        c.drawString(x + 79, ry + 7, r)
    c.setFillColor(hexc('#888888'))
    c.setFont('Helvetica', 6)
    c.drawCentredString(x + cw / 2, y + 9, 'Circus Charlie de mesa - ' + p['titulo'].title())


def marcas_corte(c, x0, y0, cw, ch, cols, rows):
    c.setStrokeColor(hexc('#999999'))
    c.setLineWidth(0.4)
    for i in range(cols + 1):
        xx = x0 + i * cw
        c.line(xx, y0 - 10, xx, y0 - 3)
        c.line(xx, y0 + rows * ch + 3, xx, y0 + rows * ch + 10)
    for j in range(rows + 1):
        yy = y0 + j * ch
        c.line(x0 - 10, yy, x0 - 3, yy)
        c.line(x0 + cols * cw + 3, yy, x0 + cols * cw + 10, yy)


def paginas_cartas(c, cartas, dibujar):
    cw, ch = 63 * mm, 88 * mm
    x0 = (W - 3 * cw) / 2
    y0 = (H - 3 * ch) / 2
    for i in range(0, len(cartas), 9):
        lote = cartas[i:i + 9]
        for k, carta in enumerate(lote):
            col, fila = k % 3, k // 3
            dibujar(c, x0 + col * cw, y0 + (2 - fila) * ch, cw, ch, carta)
        marcas_corte(c, x0, y0, cw, ch, 3, 3)
        c.showPage()


# ---------------------------------------------------------------- tableros
def tablero(c, clave):
    p = PRUEBAS[clave]
    banner(c, p['titulo'], 'Circus Charlie de mesa  -  Tablero', p['main'], pre='PRUEBA %d' % p['n'])
    # decoración en el banner
    draw_sprite(c, CHARLIE, W - 215, H - 112, 5, {'a': '#ffffff'})
    if clave == 'fuego':
        draw_sprite(c, HOGUERA, W - 145, H - 112, 4)
        draw_sprite(c, ring(16), W - 90, H - 112, 4)
    elif clave == 'monos':
        draw_sprite(c, MONO, W - 145, H - 112, 4)
        draw_sprite(c, MONO, W - 90, H - 112, 4, flip=True)
    else:
        draw_sprite(c, ball(14), W - 145, H - 112, 3.5)
        draw_sprite(c, ball(14), W - 90, H - 112, 3.5)

    cell = 100
    x0 = (W - 5 * cell) / 2
    top = H - 140
    for n in range(20):
        fila, k = n // 5, n % 5
        col = k if fila % 2 == 0 else 4 - k
        x = x0 + col * cell
        y = top - (fila + 1) * cell
        c.setFillColor(hexc(p['light']) if (fila + col) % 2 == 0 else colors.white)
        c.setStrokeColor(colors.HexColor('#1a1a2e'))
        c.setLineWidth(1.5)
        c.rect(x, y, cell, cell, fill=1, stroke=1)
        c.setFillColor(hexc(p['main']))
        c.setFont('Helvetica-Bold', 22)
        c.drawString(x + 7, y + cell - 26, str(n))
        if n == 0:
            c.setFont('Helvetica-Bold', 14)
            c.drawCentredString(x + cell / 2, y + 12, 'SALIDA')
        if n == 19:
            sz = 11
            for a in range(8):
                for b in range(3):
                    c.setFillColor(colors.black if (a + b) % 2 == 0 else colors.white)
                    c.rect(x + 6 + a * sz, y + 6 + b * sz, sz, sz, fill=1, stroke=0)
            c.setFillColor(hexc(p['main']))
            c.setFont('Helvetica-Bold', 16)
            c.drawCentredString(x + cell / 2, y + 48, 'META')
        # flecha de sentido
        if n < 19 and k < 4:
            ax = x + cell - 18 if fila % 2 == 0 else x + 18
            d = 1 if fila % 2 == 0 else -1
            c.setFillColor(hexc(p['main']))
            c.setStrokeColor(hexc(p['main']))
            c.setLineWidth(0)
            path = c.beginPath()
            path.moveTo(ax, y + 12)
            path.lineTo(ax + 10 * d, y + 18)
            path.lineTo(ax, y + 24)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
    # Bonus
    by = top - 4 * cell - 62
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 11)
    c.drawString(x0, by + 46, 'BONUS  -  baja 1 casilla cada ronda. Colocar la ficha en el 10 al empezar.')
    bw = 500 / 11
    for i in range(11):
        v = 10 - i
        c.setFillColor(hexc(p['light']) if i % 2 == 0 else colors.white)
        c.setStrokeColor(colors.HexColor('#1a1a2e'))
        c.setLineWidth(1.2)
        c.rect(x0 + i * bw, by, bw, 40, fill=1, stroke=1)
        c.setFillColor(hexc(p['main']))
        c.setFont('Helvetica-Bold', 18)
        c.drawCentredString(x0 + i * bw + bw / 2, by + 12, str(v))
    c.setFillColor(hexc(p['light']))
    c.setStrokeColor(hexc(p['main']))
    c.setLineWidth(1.5)
    c.roundRect(x0, 160, 500, 52, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x0 + 10, 197, 'CADA RONDA')
    c.setFont('Helvetica', 9)
    c.drawString(x0 + 10, 183, '1. Baja el bonus 1 casilla.   2. Todos eligen acción en secreto (opcional: ficha de vistazo).')
    c.drawString(x0 + 10, 170, '3. Voltea el obstáculo y revelad a la vez.   Si caes: -1 corazón y no avanzas.')
    # Jugadores
    py = 30
    pw, gap = 120, 6.7
    for i, (nombre, col) in enumerate(JUGADORES):
        x = x0 + i * (pw + gap)
        c.setFillColor(colors.white)
        c.setStrokeColor(hexc(col))
        c.setLineWidth(3)
        c.roundRect(x, py, pw, 118, 6, fill=1, stroke=1)
        c.setFillColor(hexc(col))
        c.rect(x, py + 94, pw, 24, fill=1, stroke=0)
        c.setFillColor(colors.white if nombre != 'Amarillo' else colors.HexColor('#1a1a2e'))
        c.setFont('Helvetica-Bold', 10)
        c.drawString(x + 8, py + 101, 'JUGADOR ' + nombre.upper())
        c.setFillColor(colors.HexColor('#1a1a2e'))
        c.setFont('Helvetica', 8)
        c.drawString(x + 8, py + 82, 'Vidas (3 corazones)')
        for k in range(3):
            c.setStrokeColor(colors.HexColor('#999999'))
            c.setDash(2, 2)
            c.setLineWidth(0.8)
            c.roundRect(x + 8 + k * 34, py + 46, 30, 30, 4, fill=0, stroke=1)
            c.setDash()
        c.setFont('Helvetica', 8)
        c.drawString(x + 8, py + 32, 'Puntos de esta prueba')
        c.setStrokeColor(colors.HexColor('#999999'))
        c.setLineWidth(0.8)
        c.rect(x + 8, py + 8, pw - 16, 20, fill=0, stroke=1)
    c.showPage()


# ---------------------------------------------------------------- peones
def peones(c):
    banner(c, 'PEONES DE CHARLIE', 'Recorta cada peón y móntalo con las instrucciones de abajo.', '#d62828')
    px = 6
    pw, ph = 12 * px, 16 * px
    tab = 18
    gap = 22
    total = 4 * pw + 3 * gap
    x0 = (W - total) / 2
    ytop = H - 150 - 16 * 6
    for i, (nombre, col) in enumerate(JUGADORES):
        x = x0 + i * (pw + gap)
        pal = {'a': col}
        # panel trasero (girado) arriba, frontal abajo
        y_front = ytop - ph - tab
        y_back = y_front + ph
        c.setStrokeColor(colors.HexColor('#999999'))
        c.setLineWidth(0.6)
        c.rect(x, y_front - tab, pw, ph + tab + ph + tab, fill=0, stroke=1)
        draw_sprite(c, CHARLIE, x, y_front, px, pal)
        c.saveState()
        c.translate(x + pw, y_back + ph)
        c.rotate(180)
        draw_sprite(c, CHARLIE, 0, 0, px, pal)
        c.restoreState()
        c.setDash(3, 3)
        c.line(x, y_back, x + pw, y_back)
        c.line(x, y_front, x + pw, y_front)
        c.line(x, y_back + ph, x + pw, y_back + ph)
        c.setDash()
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Helvetica', 6.5)
        c.drawCentredString(x + pw / 2, y_front - tab + 5, 'pestaña base')
        c.drawCentredString(x + pw / 2, y_back + ph + 6, 'pestaña base')
        c.setFillColor(hexc(col))
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(x + pw / 2, y_front - tab - 14, nombre.upper())
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica', 9)
    for k, t in enumerate([
        'Cómo montarlos:',
        '1. Recorta el rectángulo completo de cada peón.',
        '2. Dobla por la línea central de la cabeza: el frente y la espalda quedan uno tras otro.',
        '3. Pega las dos mitades entre sí y dobla las pestañas inferiores hacia fuera para que se sostenga.',
        '4. Para más estabilidad, pega las pestañas a un círculo de cartón.',
    ]):
        c.setFont('Helvetica-Bold' if k == 0 else 'Helvetica', 9)
        c.drawString(40, 150 - k * 14, t)
    c.showPage()


# ---------------------------------------------------------------- fichas + puntuación
def fichas(c):
    banner(c, 'FICHAS Y PUNTUACIÓN', 'Recorta cada ficha. Corazón = vida, bolsa = 2 pts, ojo = vistazo.', '#2a9d4f')
    d = 38
    x = 40
    y = H - 175
    # corazones
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y + 8, 'VIDAS (16)')
    for i in range(16):
        cx = 40 + (i % 8) * (d + 14)
        cy = y - 8 - d - (i // 8) * (d + 12)
        c.setStrokeColor(colors.HexColor('#999999'))
        c.setLineWidth(0.7)
        c.circle(cx + d / 2, cy + d / 2, d / 2, fill=0, stroke=1)
        draw_sprite(c, CORAZON, cx + (d - 9 * 3.2) / 2, cy + (d - 8 * 3.2) / 2, 3.2)
    y2 = y - 8 - 2 * (d + 12) - 22
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y2 + 8, 'BOLSAS DE PUNTOS (12)  -  2 puntos cada una')
    for i in range(12):
        cx = 40 + (i % 8) * (d + 14)
        cy = y2 - 8 - d - (i // 8) * (d + 12)
        c.setStrokeColor(colors.HexColor('#999999'))
        c.circle(cx + d / 2, cy + d / 2, d / 2, fill=0, stroke=1)
        draw_sprite(c, BOLSA, cx + (d - 12 * 2.4) / 2, cy + (d - 12 * 2.4) / 2, 2.4)
    y3 = y2 - 8 - 2 * (d + 12) - 22
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y3 + 8, 'VISTAZO (4) - uno por jugador y prueba   |   MARCADOR DE BONUS (3)')
    for i in range(4):
        cx = 40 + i * (d + 14)
        cy = y3 - 8 - d
        c.setStrokeColor(colors.HexColor('#999999'))
        c.circle(cx + d / 2, cy + d / 2, d / 2, fill=0, stroke=1)
        draw_sprite(c, OJO, cx + (d - 11 * 3) / 2, cy + (d - 6 * 3) / 2, 3)
    for i in range(3):
        cx = 330 + i * (d + 14)
        cy = y3 - 8 - d
        c.setStrokeColor(colors.HexColor('#999999'))
        c.circle(cx + d / 2, cy + d / 2, d / 2, fill=0, stroke=1)
        c.setFillColor(hexc('#d62828'))
        path = c.beginPath()
        path.moveTo(cx + d / 2, cy + 6)
        path.lineTo(cx + d - 8, cy + d - 8)
        path.lineTo(cx + 8, cy + d - 8)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
    # hoja de puntuación
    ty = y3 - 8 - d - 50
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, ty, 'HOJA DE PUNTUACIÓN')
    cols = [120, 70, 70, 70, 70, 80]
    heads = ['Jugador', 'Aros', 'Monos', 'Pelotas', 'TOTAL', 'Récord']
    rows = 5
    rh = 36
    xs = [40]
    for w_ in cols:
        xs.append(xs[-1] + w_)
    c.setStrokeColor(colors.HexColor('#1a1a2e'))
    c.setLineWidth(1)
    c.setFillColor(hexc('#eeeeee'))
    c.rect(40, ty - 16 - rh, sum(cols), rh, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 11)
    for i, hd in enumerate(heads):
        c.drawCentredString((xs[i] + xs[i + 1]) / 2, ty - 16 - rh + 12, hd)
    for r in range(4):
        yy = ty - 16 - rh * (r + 2)
        c.setFillColor(hexc(JUGADORES[r][1]))
        c.rect(40, yy, cols[0], rh, fill=1, stroke=1)
        c.setFillColor(colors.white if JUGADORES[r][0] != 'Amarillo' else colors.HexColor('#1a1a2e'))
        c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(40 + cols[0] / 2, yy + 12, JUGADORES[r][0])
        c.setFillColor(colors.white)
        for i in range(1, 6):
            c.rect(xs[i], yy, cols[i], rh, fill=0, stroke=1)
    c.showPage()


# ---------------------------------------------------------------- cartas de acción
ACCIONES = [
    ('CORRER', 'Avanzas 2 casillas si el camino está libre.',
     'Si hay obstáculo: ¡cae!'),
    ('SALTAR', 'Salto corto: supera obstáculos bajos.',
     'Recoge bolsas (2 pts).'),
    ('SALTO LARGO', 'Supera obstáculos largos y huecos.',
     'Cansancio: gíralo y no podrás usarlo la ronda siguiente.'),
]


def carta_accion(c, x, y, cw, ch, carta):
    idx, (nombre, col) = carta
    ac = ACCIONES[idx]
    c.setFillColor(colors.white)
    c.setStrokeColor(hexc(col))
    c.setLineWidth(4)
    c.roundRect(x + 3, y + 3, cw - 6, ch - 6, 8, fill=1, stroke=1)
    c.setFillColor(hexc(col))
    c.rect(x + 3, y + ch - 36, cw - 6, 24, fill=1, stroke=0)
    c.roundRect(x + 3, y + ch - 40, cw - 6, 36, 8, fill=1, stroke=0)
    c.setFillColor(colors.white if nombre != 'Amarillo' else colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(x + cw / 2, y + ch - 28, ac[0])
    # escena
    sx, sy, sw, sh = x + 12, y + ch - 40 - 10 - 120, cw - 24, 120
    c.setFillColor(hexc('#fff4d6'))
    c.setStrokeColor(colors.HexColor('#1a1a2e'))
    c.setLineWidth(1.2)
    c.rect(sx, sy, sw, sh, fill=1, stroke=1)
    c.setFillColor(hexc('#d9a441'))
    c.rect(sx + 1, sy + 1, sw - 2, 20, fill=1, stroke=0)
    fl = sy + 21
    cx = sx + sw / 2 - 30
    if idx == 0:
        draw_sprite(c, CHARLIE, cx, fl, 5, {'a': col})
        c.setStrokeColor(colors.HexColor('#1a1a2e'))
        c.setLineWidth(2)
        for k in range(3):
            c.line(cx - 8 - k * 6, fl + 20 + k * 14, cx - 36 - k * 6, fl + 20 + k * 14)
    elif idx == 1:
        draw_sprite(c, CHARLIE, cx + 4, fl + 16, 4.5, {'a': col})
        c.setStrokeColor(colors.HexColor('#1a1a2e'))
        c.setLineWidth(2)
        c.line(cx + 70, fl + 6, cx + 70, fl + 40)
        c.line(cx + 70, fl + 40, cx + 62, fl + 32)
        c.line(cx + 70, fl + 40, cx + 78, fl + 32)
    else:
        draw_sprite(c, CHARLIE, cx + 22, fl + 16, 4.5, {'a': col})
        c.setStrokeColor(colors.HexColor('#1a1a2e'))
        c.setLineWidth(2)
        c.bezier(sx + 14, fl + 8, sx + 30, fl + 70, sx + sw - 50, fl + 70, sx + sw - 16, fl + 8)
        c.line(sx + sw - 16, fl + 8, sx + sw - 24, fl + 16)
        c.line(sx + sw - 16, fl + 8, sx + sw - 30, fl + 8)
    st = ParagraphStyle('a', fontName='Helvetica', fontSize=9, leading=11, alignment=1)
    f = Frame(x + 14, y + 12, cw - 28, sy - y - 18, showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f.addFromList([Paragraph('<b>%s</b>' % ac[1], st), Spacer(1, 6), Paragraph(ac[2], ParagraphStyle('b', parent=st, fontSize=8.5, textColor=hexc('#b00020') if idx != 1 else hexc('#12602a')))], c)


# ---------------------------------------------------------------- reglas
def reglas(c):
    banner(c, 'CIRCUS CHARLIE de mesa', 'Reglamento  -  1 a 4 jugadores  -  15-20 min  -  edad 8+', '#d62828')
    draw_sprite(c, CHARLIE, W - 110, H - 112, 6, {'a': '#ffffff'})
    s = ParagraphStyle('p', fontName='Helvetica', fontSize=9.3, leading=12, spaceAfter=3)
    h = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=11, leading=13, spaceBefore=6, spaceAfter=2, textColor=hexc('#d62828'))
    t = []
    P = lambda txt: t.append(Paragraph(txt, s))
    Hd = lambda txt: t.append(Paragraph(txt, h))
    Hd('OBJETIVO')
    P('Eres Charlie, el payaso del circo. Superad tres pruebas de riesgo (Aros de fuego, Monos y Pelotas) y sumad más puntos que los demás. '
      'Solo controlas <b>cuándo saltar</b>: el circo avanza solo. En solitario, intenta batir tu récord.')
    Hd('MATERIAL')
    P('3 tableros, 72 cartas de obstáculo (24 por prueba), 12 cartas de acción, 4 peones, fichas de vida, bolsa, vistazo y bonus, '
      'hoja de puntuación y un dado de 6 caras (no incluido, solo para la Pelota loca).')
    Hd('PREPARACIÓN (cada prueba)')
    P('1. Coloca el tablero. Cada jugador pone su peón en <b>SALIDA (0)</b>.<br/>'
      '2. Cada jugador coge sus 3 cartas de acción (Correr, Saltar, Salto largo), 3 corazones y 1 ficha de vistazo.<br/>'
      '3. Baraja el mazo de la prueba boca abajo. Pon el marcador de bonus en el <b>10</b>.')
    Hd('UNA RONDA')
    P('<b>1. El reloj corre:</b> baja el marcador de bonus 1 casilla (se queda en 0).<br/>'
      '<b>2. Elegid:</b> todos eligen en secreto una carta de acción y la dejan boca abajo. '
      'Antes de elegir, puedes gastar tu <b>ficha de vistazo</b> para mirar en secreto la carta superior del mazo.<br/>'
      '<b>3. Revelación:</b> se voltea la carta de obstáculo y todos giran su acción a la vez. '
      'Cada jugador resuelve lo que dice su carta de obstáculo para la acción elegida.')
    Hd('ACCIONES')
    P('<b>Correr:</b> avanza 2 si está libre; contra un obstáculo, caes.<br/>'
      '<b>Saltar:</b> supera obstáculos bajos y recoge bolsas.<br/>'
      '<b>Salto largo:</b> supera obstáculos largos y huecos. <b>Cansancio:</b> tras usarlo, gira la carta; '
      'esa carta no se puede jugar la ronda siguiente (se endereza al final de esa ronda).')
    Hd('CAER')
    P('Si caes, pierdes 1 corazón y no avanzas. Con 0 corazones quedas <b>eliminado de la prueba</b> '
      '(conservas tus bolsas, pero no cobras bonus ni corazones). Todos vuelven a tener 3 corazones en la prueba siguiente.')
    Hd('LAS CARTAS DE OBSTÁCULO')
    P('Cada carta indica lo que ocurre con cada acción. Resumen del mazo (24 cartas): '
      '5 libres, 7 bajos, 5 largos, 4 con bolsa y 3 especiales. '
      'Las bolsas valen 2 puntos: ponlas junto a tu tablero.')
    Hd('FIN DE LA PRUEBA')
    P('Al llegar a la <b>META (casilla 19)</b> cobras de inmediato el valor que marque el bonus en ese momento '
      '(mínimo 1). Quien llegue en la misma ronda cobra lo mismo. Si el mazo se acaba, baraja el descarte. '
      'La prueba termina cuando todos han llegado a la meta o quedado eliminados. '
      'Además cada jugador suma <b>1 punto por corazón</b> que conserve (si llegó a meta) y 2 por cada bolsa.')
    Hd('PARTIDA COMPLETA')
    P('Jugad las 3 pruebas y apunta los puntos en la hoja. Gana quien más puntos tenga. '
      'Empate: gana quien tenga más bolsas. '
      '<b>En solitario</b>: suma tus puntos y compáralos con tu récord.')
    Hd('CONSEJOS')
    P('El Salto largo es seguro contra casi todo, pero tras usarlo no podrás repetirlo. '
      'Correr es la forma más rápida de cobrar bonus alto... y la más arriesgada. '
      'Guarda el vistazo para el momento en que más lo necesites.')
    f1 = Frame(36, 28, W - 72, H - 135 - 28, showBoundary=0)
    f1.addFromList(t, c)
    assert not t, 'El reglamento no cabe en la página: %d bloques sobran' % len(t)
    c.showPage()


def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle('Circus Charlie de mesa - Material imprimible')
    c.setAuthor('Videojuegos de mesa')
    reglas(c)
    for k in ('fuego', 'monos', 'pelotas'):
        tablero(c, k)
    peones(c)
    fichas(c)
    for k in ('fuego', 'monos', 'pelotas'):
        mazo = []
        for tipo, n in MAZO:
            mazo += [tipo] * n
        paginas_cartas(c, mazo, lambda cv, x, y, cw, ch, tipo, k=k: carta_obstaculo(cv, x, y, cw, ch, k, tipo))
    acc = []
    for j in JUGADORES:
        for idx in range(3):
            acc.append((idx, j))
    paginas_cartas(c, acc, carta_accion)
    c.save()
    print('PDF generado:', OUT)


if __name__ == '__main__':
    main()
