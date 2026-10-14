"""Carte Narthex — carte de visite 85 × 55 mm, 8 par feuille A4, traits de coupe.
Usage : python3 carte.py nnf04a30 [autre-clé ...]  → carte_<date>.pdf
Une clé par ligne d'arguments ; une seule clé = feuille entière de la même carte.
"""
import sys, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"))
URL = "pastek-stack.github.io/Narthex"
W, H = 85 * mm, 55 * mm
M = 7 * mm  # marge intérieure

def carte(c, x0, y0, key):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Mono", 7)
    c.drawString(x0 + M, y0 + H - M - 5, "N A R T H E X")
    c.setFont("Mono", 6.5)
    c.drawString(x0 + M, y0 + 24 * mm, "Clé")
    c.setFont("Mono", 15)
    c.drawString(x0 + M, y0 + 17 * mm, key)
    c.setFont("Mono", 5.5)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(x0 + M, y0 + M, URL)

def marks(c, x0, y0):
    c.setStrokeColorRGB(0.65, 0.65, 0.65); c.setLineWidth(0.2)
    L, g = 3 * mm, 1 * mm
    for x in (x0, x0 + W):
        for y in (y0, y0 + H):
            c.line(x, y - g - L if y == y0 else y + g, x, y - g if y == y0 else y + g + L)
            c.line(x - g - L if x == x0 else x + g, y, x - g if x == x0 else x + g + L, y)

def main(keys):
    out = f"carte_{datetime.date.today():%Y-%m-%d}.pdf"
    c = canvas.Canvas(out, pagesize=A4)
    pw, ph = A4
    cols, rows, gap = 2, 4, 8 * mm
    gx = (pw - cols * W - (cols - 1) * gap) / 2
    gy = (ph - rows * H - (rows - 1) * gap) / 2
    cells = [(gx + i * (W + gap), ph - gy - H - j * (H + gap)) for j in range(rows) for i in range(cols)]
    if len(keys) == 1:
        keys = keys * len(cells)
    n = 0
    for key in keys:
        if n == len(cells):
            c.showPage(); n = 0
        x0, y0 = cells[n]
        carte(c, x0, y0, key); marks(c, x0, y0)
        n += 1
    c.save()
    print(out)

if __name__ == "__main__":
    main(sys.argv[1:] or ["nnf04a30"])
