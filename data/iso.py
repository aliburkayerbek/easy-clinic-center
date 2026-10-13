"""Generate the isometric 'How it works' SVG for the Easy Clinic Center catalogue."""
import math, pathlib

C30, S30 = math.cos(math.radians(30)), 0.5
OX, OY = 500, 150

NAVY = "#24507A"
CYAN = "#3DD5E6"
CYAN_D = "#22AFC4"
AQUA = "#1EE6CF"
GREEN = "#8DC63F"
GREEN_D = "#6FA52B"


def P(x, y, z=0):
    return (OX + (x - y) * C30, OY + (x + y) * S30 - z)


def pts(*ps):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in ps)


def poly(ps, fill, stroke="none", sw=0, extra=""):
    return f'<polygon points="{pts(*ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def box(x, y, z, w, d, h, top, left, right, stroke="none", sw=0, extra=""):
    out = []
    # face at y+d (spans x) -> left-front
    out.append(poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], left, stroke, sw, extra))
    # face at x+w (spans y) -> right-front
    out.append(poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], right, stroke, sw, extra))
    out.append(poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], top, stroke, sw, extra))
    return "\n".join(out)


def win_left(x, y, z, w, d, h, u, v, ww, wh, fill):
    """window on the y+d face; u along x, v along z"""
    yy = y + d
    return poly([P(x + u, yy, z + v), P(x + u + ww, yy, z + v), P(x + u + ww, yy, z + v + wh), P(x + u, yy, z + v + wh)], fill)


def win_right(x, y, z, w, d, h, u, v, ww, wh, fill):
    xx = x + w
    return poly([P(xx, y + u, z + v), P(xx, y + u + ww, z + v), P(xx, y + u + ww, z + v + wh), P(xx, y + u, z + v + wh)], fill)


def platform(x, y, accent_l, accent_r, size=210):
    return box(x, y, 0, size, size, 26, "#FFFFFF", accent_l, accent_r, "#D5EEF2", 1)


def road(a, b, axis):
    """flat iso strip between platform centres along an axis on z=0"""
    (x1, y1), (x2, y2) = a, b
    W = 26
    if axis == "x":
        ps = [P(x1, y1 - W, 1), P(x2, y2 - W, 1), P(x2, y2 + W, 1), P(x1, y1 + W, 1)]
    else:
        ps = [P(x1 - W, y1, 1), P(x2 - W, y2, 1), P(x2 + W, y2, 1), P(x1 + W, y1, 1)]
    s = poly(ps, "#E6F8FA", "#BFEAF0", 1)
    (sx, sy), (ex, ey) = P(x1, y1, 1), P(x2, y2, 1)
    s += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{CYAN_D}" stroke-width="3" stroke-dasharray="9 8" stroke-linecap="round"/>'
    # chevron arrow at 60% along
    t = 0.62
    mx, my = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
    if axis == "x":
        a1, tip, a2 = P(mx - 14, my - 14, 1), P(mx + 6, my, 1), P(mx - 14, my + 14, 1)
    else:
        a1, tip, a2 = P(mx - 14, my - 14, 1), P(mx, my + 6, 1), P(mx + 14, my - 14, 1)
    s += f'<polyline points="{pts(a1, tip, a2)}" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    return s


S = 210  # platform size
H = 26   # platform height
POS = {
    "s1": (0, 0),
    "s2": (330, 0),
    "s3": (330, 330),
    "a": (660, 330),
    "b": (330, 660),
}


def centre(k):
    x, y = POS[k]
    return (x + S / 2, y + S / 2)


parts = []

# --- roads (drawn first, under platforms) ---
parts.append(road(centre("s1"), centre("s2"), "x"))
parts.append(road(centre("s2"), centre("s3"), "y"))
parts.append(road(centre("s3"), centre("a"), "x"))
parts.append(road(centre("s3"), centre("b"), "y"))

# --- platforms (back to front by x+y) ---
order = sorted(POS, key=lambda k: sum(POS[k]))
plat_colors = {
    "s1": (CYAN, CYAN_D), "s2": (CYAN, CYAN_D), "s3": (CYAN, CYAN_D),
    "a": (AQUA, "#14C2AE"), "b": (GREEN, GREEN_D),
}


def obj_s1(x, y):
    """Application from the UK: stack of documents + envelope"""
    z = H
    o = []
    for i in range(3):
        o.append(box(x + 45 + i * 6, y + 55 - i * 6, z + i * 7, 95, 120, 5, "#FFFFFF", "#E3EEF3", "#C9DDE6", "#B9CFDA", 0.8))
    # lines on top sheet
    tz = z + 3 * 7
    bx, by = x + 57, y + 43
    for j in range(5):
        a, b = P(bx + 12, by + 18 + j * 18, tz), P(bx + 70 - (j % 2) * 18, by + 18 + j * 18, tz)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#9FC3D3" stroke-width="2.4" stroke-linecap="round"/>')
    # envelope standing
    o.append(box(x + 130, y + 40, z, 10, 70, 52, "#FFFFFF", "#F2FBFC", "#DDF2F6", NAVY, 1.2))
    a, m, b = P(x + 140, y + 40, z + 52), P(x + 140, y + 75, z + 26), P(x + 140, y + 110, z + 52)
    o.append(f'<polyline points="{pts(a, m, b)}" fill="none" stroke="{NAVY}" stroke-width="1.6"/>')
    return "\n".join(o)


def obj_s2(x, y):
    """Detailing the medical case: laptop with heartbeat"""
    z = H
    o = []
    o.append(box(x + 50, y + 60, z, 120, 95, 7, "#F4F8FA", "#C9D7DF", "#AFC2CD"))
    # screen standing at back (y = y+60 .. +66)
    sx, sy = x + 50, y + 54
    o.append(box(sx, sy, z, 120, 6, 88, "#E9EEF1", NAVY, "#1B3E60"))
    # screen inner on front face (y+60 face)
    yy = sy + 6
    o.append(poly([P(sx + 8, yy, z + 10), P(sx + 112, yy, z + 10), P(sx + 112, yy, z + 80), P(sx + 8, yy, z + 80)], "#EFFFFC"))
    hb = [(14, 45), (36, 45), (44, 30), (52, 66), (60, 22), (68, 45), (106, 45)]
    o.append(f'<polyline points="{pts(*[P(sx + u, yy, z + v) for u, v in hb])}" fill="none" stroke="{CYAN_D}" stroke-width="3" stroke-linejoin="round"/>')
    # keyboard hint
    for j in range(3):
        a, b = P(x + 62, y + 80 + j * 18, z + 7), P(x + 158, y + 80 + j * 18, z + 7)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#AFC2CD" stroke-width="2" stroke-dasharray="6 4"/>')
    # stethoscope-ish plus badge
    o.append(box(x + 150, y + 150, z, 36, 36, 36, "#FFFFFF", GREEN, GREEN_D))
    cx, cy = x + 168, y + 168
    for (u1, v1, u2, v2) in [(-10, -3, 10, 3), (-3, -10, 3, 10)]:
        o.append(poly([P(cx + u1, cy + v1, z + 36), P(cx + u2, cy + v1, z + 36), P(cx + u2, cy + v2, z + 36), P(cx + u1, cy + v2, z + 36)], GREEN_D))
    return "\n".join(o)


def building(x, y, z, w, d, h, rows, cols_l, cols_r, cross=False):
    o = [box(x, y, z, w, d, h, "#FFFFFF", "#DCEFF4", "#B5DAE4", "#C7E3EA", 0.8)]
    for r in range(rows):
        v = 12 + r * ((h - 20) / rows)
        for c in range(cols_l):
            u = 8 + c * ((w - 16) / cols_l)
            o.append(win_left(x, y, z, w, d, h, u, v, (w - 16) / cols_l - 6, 9, "#5C8DB3"))
        for c in range(cols_r):
            u = 8 + c * ((d - 16) / cols_r)
            o.append(win_right(x, y, z, w, d, h, u, v, (d - 16) / cols_r - 6, 9, "#3E6E96"))
    if cross:
        cx, cy, tz = x + w / 2, y + d / 2, z + h
        for (u1, v1, u2, v2) in [(-14, -4, 14, 4), (-4, -14, 4, 14)]:
            o.append(poly([P(cx + u1, cy + v1, tz), P(cx + u2, cy + v1, tz), P(cx + u2, cy + v2, tz), P(cx + u1, cy + v2, tz)], "#E2465A"))
    return "\n".join(o)


def obj_s3(x, y):
    """Hospital-based quotes: three hospital buildings + price tag"""
    z = H
    o = []
    o.append(building(x + 20, y + 25, z, 60, 60, 80, 4, 2, 2))
    o.append(building(x + 105, y + 20, z, 80, 70, 125, 6, 3, 2, cross=True))
    o.append(building(x + 30, y + 115, z, 70, 70, 55, 3, 2, 2))
    # quote card standing
    o.append(box(x + 130, y + 120, z, 8, 70, 60, "#FFFFFF", "#FFFFFF", "#EAF6F8", NAVY, 1.2))
    for j in range(3):
        a, b = P(x + 138, y + 132, z + 44 - j * 13), P(x + 138, y + 178 - j * 10, z + 44 - j * 13)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{CYAN_D}" stroke-width="2.4" stroke-linecap="round"/>')
    return "\n".join(o)


def obj_a(x, y):
    """All-inclusive: plane tail, hotel, car, medical box"""
    z = H
    o = []
    # hotel
    o.append(building(x + 20, y + 20, z, 70, 55, 95, 5, 2, 2))
    # medical box
    o.append(box(x + 115, y + 25, z, 60, 60, 45, "#FFFFFF", GREEN, GREEN_D))
    cx, cy, tz = x + 145, y + 55, z + 45
    for (u1, v1, u2, v2) in [(-16, -5, 16, 5), (-5, -16, 5, 16)]:
        o.append(poly([P(cx + u1, cy + v1, tz), P(cx + u2, cy + v1, tz), P(cx + u2, cy + v2, tz), P(cx + u1, cy + v2, tz)], GREEN_D))
    # suitcase
    o.append(box(x + 25, y + 115, z, 55, 28, 60, "#FFD27A", "#F2A93B", "#D98E22"))
    hx, hy = x + 52, y + 129
    a, b, c, d = P(hx - 12, hy, z + 60), P(hx - 12, hy, z + 72), P(hx + 12, hy, z + 72), P(hx + 12, hy, z + 60)
    o.append(f'<polyline points="{pts(a, b, c, d)}" fill="none" stroke="#9A5E12" stroke-width="3" stroke-linejoin="round"/>')
    # car (transfer)
    o.append(box(x + 105, y + 120, z + 6, 85, 45, 22, "#FFFFFF", NAVY, "#1B3E60"))
    o.append(box(x + 122, y + 125, z + 28, 48, 36, 18, "#EAF6F8", "#9FD9E4", "#7CC6D4"))
    for wx in (x + 120, x + 172):
        cxw, cyw = P(wx, y + 165, z + 6)
        o.append(f'<ellipse cx="{cxw:.1f}" cy="{cyw:.1f}" rx="8" ry="9" fill="#1A2B3B"/>')
    return "\n".join(o)
    # plane (unused)
    px, py, pz = x + 140, y - 10, z + 150
    body = [P(px - 60, py, pz), P(px + 40, py, pz), P(px + 55, py + 4, pz + 2), P(px + 40, py + 8, pz + 4), P(px - 60, py + 8, pz + 4)]
    o.append(poly(body, "#FFFFFF", NAVY, 1.4))
    wing = [P(px - 5, py - 40, pz + 2), P(px + 10, py - 40, pz + 2), P(px + 5, py + 48, pz + 2), P(px - 10, py + 48, pz + 2)]
    o.append(poly(wing, CYAN, NAVY, 1.2))
    tail = [P(px - 60, py, pz + 4), P(px - 48, py, pz + 4), P(px - 56, py + 4, pz + 26), P(px - 64, py + 4, pz + 26)]
    o.append(poly(tail, CYAN_D, NAVY, 1.2))
    return "\n".join(o)


def obj_b(x, y):
    """Treatment only: medical box solid, extras as dashed 'optional' ghosts"""
    z = H
    o = []
    ghost = 'stroke-dasharray="5 4" fill-opacity="0.15"'
    o.append(box(x + 20, y + 25, z, 55, 28, 55, "#9FB6C7", "#9FB6C7", "#9FB6C7", "#7E97AA", 1.4, ghost))
    o.append(box(x + 25, y + 110, z, 60, 50, 80, "#9FB6C7", "#9FB6C7", "#9FB6C7", "#7E97AA", 1.4, ghost))
    o.append(box(x + 105, y + 60, z, 80, 80, 70, "#FFFFFF", GREEN, GREEN_D))
    cx, cy, tz = x + 145, y + 100, z + 70
    for (u1, v1, u2, v2) in [(-22, -7, 22, 7), (-7, -22, 7, 22)]:
        o.append(poly([P(cx + u1, cy + v1, tz), P(cx + u2, cy + v1, tz), P(cx + u2, cy + v2, tz), P(cx + u1, cy + v2, tz)], GREEN_D))
    # stethoscope line on left face
    yy = y + 140
    curve = [P(x + 120, yy, z + 55), P(x + 132, yy, z + 25), P(x + 150, yy, z + 18), P(x + 168, yy, z + 25), P(x + 172, yy, z + 50)]
    o.append(f'<polyline points="{pts(*curve)}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>')
    return "\n".join(o)


OBJ = {"s1": obj_s1, "s2": obj_s2, "s3": obj_s3, "a": obj_a, "b": obj_b}

for k in order:
    x, y = POS[k]
    l, r = plat_colors[k]
    parts.append(platform(x, y, l, r, S))
    parts.append(OBJ[k](x, y))


# --- floating number badges above each platform ---
def badge(k, label, color):
    x, y = POS[k]
    bx, by = P(x + S / 2, y + S / 2, H)
    tx, ty = P(x, y + S, H)  # left corner of platform
    return ""


# --- labels (2D cards) ---
def label(cx, cy, num, title, lines, color, anchor="start", w=250):
    x = cx if anchor == "start" else cx - w
    h = 34 + 19 * len(lines) + 30
    s = f'<g><rect x="{x}" y="{cy}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="#D3EEF2" stroke-width="1.5"/>'
    s += f'<rect x="{x}" y="{cy}" width="6" height="{h}" rx="3" fill="{color}"/>'
    s += f'<circle cx="{x + 34}" cy="{cy + 32}" r="17" fill="{color}"/>'
    s += f'<text x="{x + 34}" y="{cy + 38.5}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="17" fill="#FFFFFF">{num}</text>'
    s += f'<text x="{x + 60}" y="{cy + 38}" font-family="Inter" font-weight="700" font-size="17" fill="{NAVY}">{title}</text>'
    for i, ln in enumerate(lines):
        s += f'<text x="{x + 20}" y="{cy + 72 + i * 19}" font-family="Inter" font-size="14" fill="#4F6475">{ln}</text>'
    return s + "</g>"


def leader(p1, p2, color):
    return f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{color}" stroke-width="1.6" stroke-dasharray="3 4"/><circle cx="{p2[0]:.1f}" cy="{p2[1]:.1f}" r="4" fill="{color}"/>'


import sys
LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
NOLABEL = LANG == "none"
if NOLABEL: LANG = "en"
TXT = {
 "en": dict(
   t1="Apply from the UK", l1=["Send us your request online,", "by phone or WhatsApp."],
   t2="Detail your case", l2=["Reports, imaging and history", "reviewed by our medical team."],
   t3="Hospital-based quotes", l3=["Offers from our partner", "hospitals across Türkiye."],
   tb="OPTION B", nb="Treatment Only", lb=["Treatment price only. Flights, hotel", "and transfers stay optional add-ons."],
   ta="OPTION A", na="All-Inclusive Package", la=["Treatment + flights + accommodation", "+ airport & hospital transfers."],
   fork="TWO-STAGE QUOTE"),
 "tr": dict(
   t1="İngiltere'den başvuru", l1=["Talebinizi online, telefonla", "veya WhatsApp ile iletin."],
   t2="Vaka detaylandırılır", l2=["Raporlar, görüntüler ve geçmiş", "tıbbi ekibimizce incelenir."],
   t3="Hastane bazlı teklif", l3=["Türkiye'deki partner", "hastanelerimizden teklifler."],
   tb="SEÇENEK B", nb="Sadece Tedavi", lb=["Yalnızca tedavi fiyatı. Uçak, otel ve", "transfer opsiyonel olarak eklenir."],
   ta="SEÇENEK A", na="Her Şey Dahil Paket", la=["Tedavi + uçak bileti + konaklama", "+ havalimanı ve hastane transferi."],
   fork="İKİ AŞAMALI TEKLİF"),
}[LANG]

labels = []
# S1: left of top platform
p = P(0, S / 2, H)
labels.append(leader((p[0] - 60, p[1] - 70), (p[0] + 20, p[1] - 30), CYAN_D))
labels.append(label(p[0] - 60, p[1] - 160, "1", TXT["t1"], TXT["l1"], CYAN_D, "end", 285))
# S2: right
p = P(330 + S, S / 2, H)
labels.append(leader((p[0] - 10, p[1] - 150), (p[0] - 40, p[1] - 60), CYAN_D))
labels.append(label(p[0] - 80, p[1] - 265, "2", TXT["t2"], TXT["l2"], CYAN_D, "start", 285))
# S3: left
p = P(330, 330 + S / 2, H)
labels.append(leader((p[0] - 50, p[1] - 40), (p[0] + 25, p[1] - 10), CYAN_D))
labels.append(label(p[0] - 50, p[1] - 115, "3", TXT["t3"], TXT["l3"], CYAN_D, "end", 285))

def option_card(x, y, w, tag, title, lines, color):
    h = 58 + 20 * len(lines) + 16
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>'
    s += f'<rect x="{x + 18}" y="{y - 14}" width="{len(tag) * 9.6 + 26}" height="28" rx="14" fill="{color}"/>'
    s += f'<text x="{x + 31}" y="{y + 5}" font-family="Inter" font-weight="700" font-size="13" letter-spacing="1.5" fill="#FFFFFF">{tag}</text>'
    s += f'<text x="{x + 22}" y="{y + 44}" font-family="Inter" font-weight="700" font-size="19" fill="{NAVY}">{title}</text>'
    for i, ln in enumerate(lines):
        s += f'<text x="{x + 22}" y="{y + 74 + i * 20}" font-family="Inter" font-size="14" fill="#4F6475">{ln}</text>'
    return s


labels.append(option_card(10, 885, 400, TXT["tb"], TXT["nb"], TXT["lb"], GREEN_D))
labels.append(option_card(590, 885, 400, TXT["ta"], TXT["na"], TXT["la"], "#14B8A4"))
# fork caption
fx, fy = P(330 + S / 2, 330 + S / 2, H)
labels.append(f'<text x="{fx:.1f}" y="{fy + 175:.1f}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="13" letter-spacing="2" fill="{CYAN_D}">{TXT["fork"]}</text>')

parts_l = "" if NOLABEL else "\n".join(labels)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -40 1140 1060" width="100%">
<defs>
  <radialGradient id="glow" cx="50%" cy="55%" r="60%">
    <stop offset="0%" stop-color="#E9FBFC"/><stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
</defs>
<ellipse cx="500" cy="560" rx="560" ry="420" fill="url(#glow)"/>
{"".join(parts)}
{parts_l}
</svg>'''

open(pathlib.Path(__file__).resolve().parent / "_build" / ("iso_none.svg" if NOLABEL else f"iso_{LANG}.svg"), "w").write(svg)
print("ok", len(svg))
