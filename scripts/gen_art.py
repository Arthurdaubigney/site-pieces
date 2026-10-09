#!/usr/bin/env python3
"""Génère les illustrations vectorielles originales du site (pièces stylisées).
Aucune photo tierce : toutes les images sont créées ici, donc libres de droits.
Usage : python3 scripts/gen_art.py"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')

INK, INK2 = '#161b22', '#2a313b'
GOLD_DK = '#5e4513'

DEFS = '''<defs>
<linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbfaf6"/><stop offset=".45" stop-color="#d4cfc2"/><stop offset="1" stop-color="#8f8979"/></linearGradient>
<linearGradient id="silverEdge" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e5da"/><stop offset="1" stop-color="#6f6a5c"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0d99b"/><stop offset=".5" stop-color="#c29c4d"/><stop offset="1" stop-color="#8a6a2b"/></linearGradient>
<linearGradient id="goldEdge" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd493"/><stop offset="1" stop-color="#7a5c22"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".38" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient>
<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#c9a965" stop-opacity=".45"/><stop offset="1" stop-color="#c9a965" stop-opacity="0"/></radialGradient>
</defs>'''

EMBLEMS = {
 'crown': '<path d="M80 98 L83 70 L92 82 L100 64 L108 82 L117 70 L120 98 Z"/><rect x="80" y="98" width="40" height="6" rx="2"/>',
 'cross': '<rect x="94" y="62" width="12" height="46" rx="2"/><rect x="80" y="76" width="40" height="12" rx="2"/>',
 'towers': '<rect x="78" y="76" width="12" height="30"/><rect x="94" y="66" width="12" height="40"/><rect x="110" y="76" width="12" height="30"/><path d="M78 76l6-8 6 8zM94 66l6-9 6 9zM110 76l6-8 6 8z"/>',
 'sprig': '<path d="M100 108 V66" stroke="%s" stroke-width="3" fill="none"/>' % GOLD_DK + ''.join(
    '<ellipse cx="%.1f" cy="%.1f" rx="5" ry="11" transform="rotate(%d %.1f %.1f)"/>' % (100+s*12, y, s*50, 100+s*12, y) for s, y in ((-1, 90), (1, 90), (-1, 74), (1, 74))) + '<ellipse cx="100" cy="64" rx="5" ry="11"/>',
 'flower': ''.join('<ellipse cx="100" cy="76" rx="6" ry="14" transform="rotate(%d 100 90)"/>' % a for a in range(0, 360, 60)) + '<circle cx="100" cy="90" r="5" fill="#f0d99b"/>',
 'book': '<path d="M78 70 L98 76 V106 L78 100 Z"/><path d="M122 70 L102 76 V106 L122 100 Z"/>',
 'atom': '<g stroke="%s" stroke-width="3" fill="none"><path d="M100 90 L100 66 M100 90 L79 102 M100 90 L121 102 M100 66 L79 102 M100 66 L121 102 M79 102 L121 102"/></g>' % GOLD_DK + ''.join('<circle cx="%d" cy="%d" r="7"/>' % p for p in ((100, 90), (100, 66), (79, 102), (121, 102))),
 'eagle': '<path d="M100 64 L107 76 L136 66 L122 92 L132 104 L108 100 L100 112 L92 100 L68 104 L78 92 L64 66 L93 76 Z"/>',
 'face': '<path d="M100 62c-14 0-22 10-22 22 0 10 5 14 6 22l4 8h24l4-8c1-8 6-12 6-22 0-12-8-22-22-22z"/>',
}

def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5
        rr = r if i % 2 == 0 else r*0.42
        pts.append('%.1f,%.1f' % (cx+rr*math.cos(a), cy+rr*math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (' '.join(pts), fill)

def coin(top='', bottom='', value='2', emblem=None, variant=None, gold_ring=False, stars=True, uid='c'):
    """Retourne un <g> 200x200 (centre 100,100)."""
    ring_fill, disc_fill = ('url(#gold)', 'url(#silver)') if gold_ring else ('url(#silver)', 'url(#gold)')
    edge = 'url(#goldEdge)' if gold_ring else 'url(#silverEdge)'
    txt_ring = '#6e5a22' if gold_ring else '#6b6657'
    txt_disc = GOLD_DK if not gold_ring else '#5d5a50'
    emb = ''
    if emblem:
        emb = '<g fill="%s">%s</g>' % (txt_disc, EMBLEMS[emblem])
    val_y, val_size = (127, 34) if emblem else (122, 76)
    def val(dx=0, dy=0, fill=txt_disc, op=1):
        return '<text x="%s" y="%s" font-family="Georgia,\'Times New Roman\',serif" font-weight="700" font-size="%d" text-anchor="middle" fill="%s" opacity="%s">%s</text>' % (100+dx, val_y+dy, val_size, fill, op, value)
    center = ''
    if variant == 'double':
        center = '<g>' + val(5, 4, '#2a2210', .35) + emb.replace('<g ', '<g transform="translate(5 4)" opacity=".35" ', 1) + '</g>'
    center += '<g>' + val(-1, -1, '#fff6d8', .55) + val() + emb + '</g>'
    if variant == 'rot130':
        center = '<g transform="rotate(130 100 100)">' + center + '</g>'
    if variant == 'flip':
        center = '<g transform="rotate(180 100 100)">' + center + '</g>'
    ring_txt = ''
    if top:
        ring_txt += '<path id="%st" d="M24 100 A76 76 0 0 1 176 100" fill="none"/><text font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="11" letter-spacing="2.6" fill="%s"><textPath href="#%st" startOffset="50%%" text-anchor="middle">%s</textPath></text>' % (uid, txt_ring, uid, top)
    if bottom:
        ring_txt += '<path id="%sb" d="M15 100 A85 85 0 0 0 185 100" fill="none"/><text font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="11" letter-spacing="2.6" fill="%s"><textPath href="#%sb" startOffset="50%%" text-anchor="middle">%s</textPath></text>' % (uid, txt_ring, uid, bottom)
    st = ''
    if stars and not (top or bottom):
        for i in range(12):
            a = i*math.pi/6
            st += star(100+80*math.cos(a), 100+80*math.sin(a), 5.6, txt_ring)
    elif stars:
        st = star(26, 100, 4.2, txt_ring) + star(174, 100, 4.2, txt_ring)
    return ('<g>'
      '<circle cx="100" cy="100" r="98" fill="%s"/>'
      '<circle cx="100" cy="100" r="97" fill="none" stroke="#fff" stroke-opacity=".38" stroke-width="3.2" stroke-dasharray="1.1 1.9"/>'
      '<circle cx="100" cy="100" r="94" fill="%s"/>'
      '<circle cx="100" cy="100" r="66" fill="#000" fill-opacity=".14"/>'
      '<circle cx="100" cy="100" r="64.5" fill="%s"/>'
      '<circle cx="100" cy="100" r="58" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.2"/>'
      '%s%s%s'
      '<circle cx="100" cy="100" r="98" fill="url(#sheen)"/>'
      '<circle cx="100" cy="100" r="98" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="1"/>'
      '</g>') % (edge, ring_fill, disc_fill, ring_txt, st, center)

def place(g, x, y, size, rot=0, shadow=True):
    s = size/200.0
    sh = '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="url(#shadow)"/>' % (x+size*.54, y+size*.98, size*.46, size*.07) if shadow else ''
    return sh + '<g transform="translate(%.1f %.1f) rotate(%s %.1f %.1f) scale(%.4f)">%s</g>' % (x, y, rot, size/2, size/2, s, g)

def loupe(x, y, size, rot=0):
    s = size/100.0
    return ('<g transform="translate(%.1f %.1f) rotate(%s 50 50) scale(%.3f)">'
      '<path d="M66 66 L94 94" stroke="%s" stroke-width="11" stroke-linecap="round"/>'
      '<path d="M66 66 L94 94" stroke="#a6823c" stroke-width="5" stroke-linecap="round"/>'
      '<circle cx="42" cy="42" r="34" fill="#fff" fill-opacity=".14" stroke="#a6823c" stroke-width="7"/>'
      '<circle cx="42" cy="42" r="34" fill="none" stroke="%s" stroke-width="2" stroke-opacity=".5"/>'
      '<path d="M22 36 A22 22 0 0 1 36 22" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-opacity=".85"/></g>'
      ) % (x, y, rot, s, INK, INK)

def svg(w, h, body, bg=None, title=''):
    b = ''
    if bg == 'ink':
        b = '<rect width="%d" height="%d" fill="url(#bgink)"/>' % (w, h)
    elif bg == 'paper':
        b = '<rect width="%d" height="%d" fill="url(#bgpaper)"/>' % (w, h)
    extra = ('<linearGradient id="bgink" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#232a35"/><stop offset="1" stop-color="#0f1318"/></linearGradient>'
             '<linearGradient id="bgpaper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f1e6"/><stop offset="1" stop-color="#e9dfc8"/></linearGradient>')
    d = DEFS.replace('</defs>', extra + '</defs>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img"><title>%s</title>%s%s%s</svg>' % (w, h, title, d, b, body)

def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)

def glow(cx, cy, r):
    return '<circle cx="%d" cy="%d" r="%d" fill="url(#glow)"/>' % (cx, cy, r)

# ---------- Hero ----------
body = glow(820, 360, 520)
body += place(coin(top='EURO', bottom='COLLECTION', value='2', uid='h1', stars=True), 120, 330, 330, -14)
body += place(coin(value='2', emblem='flower', uid='h2', stars=True, gold_ring=False), 360, 430, 280, 10)
body += place(coin(value='1', gold_ring=True, uid='h3'), 150, 40, 230, 8)
body += place(coin(top='RARE', bottom='MONACO', value='2', emblem='crown', uid='h4'), 560, 120, 560, 6)
write('hero.svg', svg(1200, 900, body, 'ink', 'Pièces de 2 euros stylisées'))

# ---------- Types ----------
# Pièces fautées
body = glow(320, 300, 300) + place(coin(top='2 EURO', bottom='2 EURO', value='2', variant='double', uid='f1'), 40, 60, 480, -6) + loupe(310, 280, 260, 0)
write('faute.svg', svg(560, 560, body, 'ink', 'Pièce de 2 euros avec double frappe observée à la loupe'))
# Monaco
body = place(coin(top='MONACO', bottom='2007', value='2', emblem='crown', uid='m1'), 20, 60, 500, 0)
write('monaco.svg', svg(560, 640, body, None, 'Pièce de 2 euros de Monaco stylisée'))
# Vatican & San Marino
body = place(coin(top='VATICANO', bottom='2005', value='2', emblem='cross', uid='v1'), 20, 130, 330, -8) + place(coin(top='SAN MARINO', bottom='2004', value='2', emblem='towers', uid='v2'), 250, 20, 300, 10)
write('collection.svg', svg(640, 520, body, 'paper', 'Pièces de 2 euros du Vatican et de Saint-Marin stylisées'))
# Commémoratives
body = place(coin(top='COMMÉMORATIVE', bottom='ÉDITION LIMITÉE', value='2', emblem='book', uid='c1'), 60, 60, 480, 0)
write('commemorative.svg', svg(600, 600, body, 'paper', 'Pièce commémorative de 2 euros stylisée'))
# Coffret BU / BE
case = '<rect x="30" y="140" width="740" height="360" rx="26" fill="#0f1318"/><rect x="46" y="156" width="708" height="328" rx="18" fill="url(#bgink)"/>'
for i, (cx, tp) in enumerate(((180, 'BU'), (400, 'BE'), (620, 'BU'))):
    case += '<circle cx="%d" cy="320" r="112" fill="#0b0e12"/><circle cx="%d" cy="320" r="106" fill="#161b22" stroke="#000" stroke-opacity=".5" stroke-width="3"/>' % (cx, cx)
    case += place(coin(top='EURO', bottom=tp, value='2', uid='k%d' % i, emblem=('flower', 'sprig', 'book')[i]), cx-98, 222, 196, 0, shadow=False)
case += '<text x="400" y="545" font-family="Georgia,serif" font-size="26" fill="#c9a965" text-anchor="middle" letter-spacing="6">COFFRET OFFICIEL</text>'
write('coffret.svg', svg(800, 600, case, 'paper', 'Coffret de pièces de 2 euros BU et BE stylisé'))
# Expertise
body = glow(330, 270, 300) + place(coin(top='EXPERTISE', bottom='NUMISMATIQUE', value='2', emblem='flower', uid='e1'), 90, 80, 360, -6) + loupe(310, 220, 330, 0)
write('expertise.svg', svg(800, 600, body, 'paper', 'Pièce de 2 euros examinée à la loupe'))
# Confidentialité
lock = ('<g transform="translate(250 90)"><path d="M70 130 V90 a60 60 0 0 1 120 0 V130" fill="none" stroke="#a6823c" stroke-width="22" stroke-linecap="round"/>'
        '<rect x="30" y="120" width="200" height="170" rx="26" fill="url(#bgink)"/><rect x="30" y="120" width="200" height="170" rx="26" fill="none" stroke="#c9a965" stroke-opacity=".5" stroke-width="3"/>'
        '<circle cx="130" cy="188" r="20" fill="#c9a965"/><rect x="122" y="196" width="16" height="46" rx="6" fill="#c9a965"/></g>')
body = glow(400, 280, 330) + place(coin(value='2', uid='p1'), 40, 330, 150, -10) + place(coin(value='2', emblem='sprig', uid='p2'), 600, 340, 140, 12) + lock
write('confidentialite.svg', svg(800, 520, body, 'paper', 'Cadenas protégeant des pièces de 2 euros'))

# ---------- Bandeau commémoratives (6 pièces) ----------
coins = [
 ('c-monaco-grace-kelly', dict(top='MONACO', bottom='2007', emblem='crown')),
 ('c-vatican-sede-vacante', dict(top='VATICANO', bottom='2005', emblem='cross')),
 ('c-saint-marin', dict(top='SAN MARINO', bottom='2004', emblem='towers')),
 ('c-finlande', dict(top='SUOMI FINLAND', bottom='2004', emblem='sprig')),
 ('c-andorre', dict(top='ANDORRA', bottom='2020', emblem='flower')),
 ('c-france-rome', dict(top='RÉPUBLIQUE FRANÇAISE', bottom='2007', emblem='book')),
]
for n, kw in coins:
    write(n + '.svg', svg(220, 220, place(coin(value='2', uid='b', **kw), 10, 8, 200, 0, shadow=False), None, n))

# ---------- Erreurs ----------
write('e-belgique-atomium.svg', svg(220, 220, place(coin(top='BELGIQUE', bottom='2006', value='2', emblem='atom', variant='rot130', uid='x1'), 10, 8, 200, 0, shadow=False), None, 'rotation de matrice 130°'))
write('e-italie-double.svg', svg(220, 220, place(coin(top='ITALIA', bottom='2002', value='1', variant='double', gold_ring=True, uid='x2'), 10, 8, 200, 0, shadow=False), None, 'double frappe'))
write('e-allemagne-revers.svg', svg(220, 220, place(coin(top='DEUTSCHLAND', bottom='2004', value='1', emblem='eagle', variant='flip', gold_ring=True, uid='x3'), 10, 8, 200, 0, shadow=False), None, 'revers renversé 180°'))

# ---------- Image de partage (rendue en PNG via un navigateur) ----------
body = glow(900, 300, 480) + place(coin(top='EURO', bottom='RARE', value='2', emblem='crown', uid='o1'), 640, 90, 440, 8) + place(coin(value='2', uid='o2'), 520, 330, 230, -10)
body += '<text x="70" y="250" font-family="Georgia,serif" font-size="78" fill="#fff">Euro<tspan fill="#c9a965" font-style="italic">Rare</tspan></text>'
body += '<text x="70" y="330" font-family="Arial,sans-serif" font-size="34" fill="#d8d3c6">Estimation gratuite de</text><text x="70" y="378" font-family="Arial,sans-serif" font-size="34" fill="#d8d3c6">vos pièces de 2 € rares</text>'
write('og.svg', svg(1200, 630, body, 'ink', 'EuroRare'))
print('ok')
