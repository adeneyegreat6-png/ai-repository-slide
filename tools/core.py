#!/usr/bin/env python3
# Re-renders the carousel with the uploaded portrait as a scrimmed background.
import os, html, cairosvg, io
import numpy as np
from PIL import Image, ImageChops

W, H = 1080, 1350
M = 80
CW = W - 2*M
OUT = "/home/claude/slides_photo10"
os.makedirs(OUT, exist_ok=True)
PHOTO = "/mnt/user-data/uploads/1767332302414.jpg"
HANDLE = "@learnaiwithdoyin"
TOTAL_DOTS = 6

KICKER, NUM_A, NUM_B = "#6d9bef", "#5b8cff", "#9b6bff"
WHITE, SUBWHITE, GOLD = "#f5f7fb", "#e4ecf7", "#f2b134"
BORDER, DOT_OFF = "#b8c8e0", "#46546e"

def esc(s): return html.escape(s, quote=True)

def tlines(lines, x, y, dy, size, fill, weight="bold", style="normal",
           tracking=0, opacity=1.0):
    ls = f' letter-spacing="{tracking}"' if tracking else ""
    spans = "".join(f'<tspan x="{x}" dy="{0 if i==0 else dy}">{esc(t)}</tspan>'
                     for i, t in enumerate(lines))
    return (f'<text x="{x}" y="{y}" font-family="Poppins" font-size="{size}" '
            f'font-weight="{weight}" font-style="{style}" fill="{fill}" '
            f'fill-opacity="{opacity}"{ls} xml:space="preserve">{spans}</text>')

def defs():
    return f'''<defs>
      <linearGradient id="rainbow" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#4a90e2"/><stop offset="0.35" stop-color="#8e7cf0"/>
        <stop offset="0.7" stop-color="#c86dd7"/><stop offset="1" stop-color="#f0a04b"/>
      </linearGradient>
      <linearGradient id="num" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{NUM_A}"/><stop offset="1" stop-color="{NUM_B}"/>
      </linearGradient>
      <linearGradient id="ava" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#9b6bff"/><stop offset="1" stop-color="#5b8cff"/>
      </linearGradient>
    </defs>'''

def chrome(active):
    """transparent layer: rainbow bar + footer + dots only (no bg, photo shows through)"""
    footer = (f'<circle cx="{M+18}" cy="1250" r="18" fill="url(#ava)"/>'
              f'{tlines([HANDLE], M+50, 1258, 0, 25, WHITE)}')
    gap = 28; x_end = W - M
    xs = [x_end - (TOTAL_DOTS-1-i)*gap for i in range(TOTAL_DOTS)]
    dots = []
    for i, cx in enumerate(xs):
        if i == active:
            dots.append(f'<rect x="{cx-13}" y="1244" width="26" height="12" rx="6" fill="{GOLD}"/>')
        else:
            dots.append(f'<circle cx="{cx}" cy="1250" r="6" fill="{DOT_OFF}"/>')
    return (f'<rect x="0" y="0" width="{W}" height="12" fill="url(#rainbow)"/>'
            f'{footer}{"".join(dots)}')

def prompt_box(label, lines, y, h):
    # darker glass panel so italic text stays crisp over the photo
    box = (f'<rect x="{M}" y="{y}" width="{CW}" height="{h}" rx="22" '
           f'fill="#0a1424" fill-opacity="0.42" stroke="{BORDER}" '
           f'stroke-opacity="0.35" stroke-width="1.5"/>')
    lab = tlines([label], M+34, y+50, 0, 16, GOLD, tracking=2)
    txt = tlines(lines, M+34, y+92, 40, 24, WHITE, style="italic")
    return box + lab + txt

def svg_wrap(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">{defs()}{body}</svg>')

def big_number(n):
    return (f'<text x="{M}" y="252" font-family="Poppins" font-size="132" '
            f'font-weight="bold" fill="url(#num)" stroke="url(#num)" '
            f'stroke-width="1.5">{n}</text>')

def body_slide(active, kicker, num, head, sub, plabel, prompt):
    b = chrome(active)
    b += tlines([kicker], M, 122, 0, 19, KICKER, tracking=3)
    b += big_number(num)
    b += tlines(head, M, 348, 62, 56, WHITE)
    sy = 348 + (len(head)-1)*62 + 78
    b += tlines(sub, M, sy, 38, 25, SUBWHITE)
    box_y = max(618, sy + (len(sub)-1)*38 + 60)
    box_h = min(268, 1180 - box_y)
    b += prompt_box(plabel, prompt, box_y, box_h)
    return svg_wrap(b)

def monogram(cx, cy, r, letter, color):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<text x="{cx}" y="{cy+r*0.36}" font-family="Poppins" '
            f'font-size="{r*1.15:.0f}" font-weight="bold" fill="#0a1424" '
            f'text-anchor="middle">{esc(letter)}</text>')

def bullet_box(bullets, y, h, accent):
    box = (f'<rect x="{M}" y="{y}" width="{CW}" height="{h}" rx="22" '
           f'fill="#0a1424" fill-opacity="0.42" stroke="{BORDER}" '
           f'stroke-opacity="0.35" stroke-width="1.5"/>')
    inner = ""
    ly = y + 56
    for line in bullets:
        inner += (f'<circle cx="{M+42}" cy="{ly-8}" r="5" fill="{accent}"/>'
                  f'{tlines([line], M+64, ly, 0, 23, WHITE, weight="bold")}')
        ly += 56
    return box + inner

def tool_slide(active, kicker, num, toolname, letter, accent, bestfor, bullets):
    b = chrome(active)
    b += tlines([kicker], M, 122, 0, 19, KICKER, tracking=3)
    b += big_number(num)
    b += monogram(M+38, 322, 38, letter, accent)
    b += tlines([toolname], M+96, 336, 0, 46, WHITE, weight="bold")
    by = 420
    b += tlines(["BEST FOR"], M, by, 0, 16, GOLD, tracking=2)
    b += tlines(bestfor, M, by+38, 34, 25, SUBWHITE)
    box_y = by + 38 + (len(bestfor)-1)*34 + 50
    b += bullet_box(bullets, box_y, min(230, 1180-box_y), accent)
    return svg_wrap(b)

def cover_slide(active, kicker, head, sub):
    b = chrome(active)
    b += tlines([kicker], M, 132, 0, 20, KICKER, tracking=3)
    b += tlines(head, M, 250, 72, 62, WHITE)
    sy = 250 + (len(head)-1)*72 + 96
    b += tlines(sub, M, sy, 42, 27, SUBWHITE)
    return svg_wrap(b)

def cta_slide(active, kicker, head, sub, pills):
    b = chrome(active)
    b += tlines([kicker], M, 132, 0, 20, KICKER, tracking=3)
    b += tlines(head, M, 252, 72, 60, WHITE)
    sy = 252 + (len(head)-1)*72 + 92
    b += tlines(sub, M, sy, 42, 26, SUBWHITE)
    py = sy + (len(sub)-1)*42 + 70
    for i, p in enumerate(pills):
        fy = py + i*84; filled = (i == 0)
        fill = GOLD if filled else "none"; fop = "1" if filled else "0"
        tcol = "#1a1205" if filled else GOLD
        pw = 150 + int(len(p)*15.5)
        b += (f'<rect x="{M}" y="{fy}" width="{pw}" height="64" rx="32" '
              f'fill="{fill}" fill-opacity="{fop}" stroke="{GOLD}" stroke-width="2"/>')
        b += tlines([p], M+34, fy+41, 0, 22, tcol)
    return svg_wrap(b)

# ---------- photo background (built once, shared by all slides) ----------
def navy_gradient(top=(24,42,68), bot=(10,20,34)):
    yy = np.linspace(0,1,H)[:,None]; xx = np.linspace(0,1,W)[None,:]
    t = (xx+yy)/2
    arr = np.stack([top[i]*(1-t)+bot[i]*t for i in range(3)], -1)
    return Image.fromarray(arr.astype("uint8"), "RGB")

def cover_crop(im):
    iw, ih = im.size
    s = max(W/iw, H/ih)
    im = im.resize((int(iw*s), int(ih*s)), Image.LANCZOS)
    nw, nh = im.size
    left = (nw-W)//2
    top = int((nh-H)*0.28)          # bias up so the face sits in the upper third
    return im.crop((left, top, left+W, top+H))

def build_background():
    base = navy_gradient().convert("RGBA")
    photo = cover_crop(Image.open(PHOTO).convert("RGB"))
    # alpha: keep left text-column dark, let subject show right-of-centre,
    # fade top (bar/kicker) and bottom (footer)
    ax = np.linspace(0,1,W)[None,:]
    hx = np.clip((ax-0.30)/0.45, 0, 1)        # ramps from 30%->75% width
    hx = 0.10 + hx*0.60                        # left 0.10  ->  right 0.70
    ay = np.linspace(0,1,H)[:,None]
    vf = np.minimum(np.clip(ay/0.10,0,1), np.clip((1-ay)/0.15,0,1))
    alpha = (hx*vf*255).astype("uint8")
    alpha = np.broadcast_to(alpha,(H,W)).copy()
    base.paste(photo, (0,0), Image.fromarray(alpha, "L"))
    # global navy wash to unify tone + protect legibility
    base = Image.alpha_composite(base, Image.new("RGBA",(W,H),(12,22,38,72)))
    return base

