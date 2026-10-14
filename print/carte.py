"""Carte Narthex — format DL (99 × 210 mm), 3 par feuille A4, traits de coupe.
Usage : python3 carte.py nnf04a30 [autre-clé ...]  → carte_<date>.pdf
"""
import sys, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"))
URL = "pastek-stack.github.io/Narthex"
W, H = 210 * mm, 99 * mm  # carte DL, à l'italienne

def carte(c, x0, y0, key):
    # tout en noir pur, pas de filet, pas de fond
    c.setFillColorRGB(0, 0, 0)
    # mot, haut gauche
    c.setFont("Mono", 9)
    c.drawString(x0 + 14 * mm, y0 + H - 16 * mm, "N A R T H E X")
    # clé, centre optique
    c.setFont("Mono", 9)
    c.drawString(x0 + 14 * mm, y0 + 44 * mm, "Clé")
    c.setFont("Mono", 22)
    c.drawString(x0 + 14 * mm, y0 + 32 * mm, key)
    # url, bas gauche, discret
    c.setFont("Mono", 7.5)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawString(x0 + 14 * mm, y0 + 12 * mm, URL)

def marks(c, x0, y0):
    c.setStrokeColorRGB(0.6, 0.6, 0.6); c.setLineWidth(0.25)
    L = 4 * mm
    for (x, y) in [(x0, y0), (x0 + W, y0), (x0, y0 + H), (x0 + W, y0 + H)]:
        c.line(x - L - 1 * mm, y, x - 1 * mm, y) if x == x0 else c.line(x + 1 * mm, y, x + L + 1 * mm, y)
        c.line(x, y - L - 1 * mm, x, y - 1 * mm) if y == y0 else c.line(x, y + 1 * mm, x, y + L + 1 * mm)

def main(keys):
    out = f"carte_{datetime.date.today():%Y-%m-%d}.pdf"
    c = canvas.Canvas(out, pagesize=A4)
    pw, ph = A4
    x0 = (pw - W) / 2
    slots = [ph - 10 * mm - H - i * (H + 0) for i in range(3)]
    i = 0
    for key in keys:
        if i == 3:
            c.showPage(); i = 0
        y0 = slots[i]
        carte(c, x0, y0, key); marks(c, x0, y0)
        i += 1
    c.save()
    print(out)

if __name__ == "__main__":
    main(sys.argv[1:] or ["nnf04a30"])
