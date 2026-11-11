"""Synthetic finger-drawn digits: skeleton strokes per digit style + random distortion.
Normalisation here must match the app's JS exactly (see normalise())."""
import numpy as np
from PIL import Image, ImageDraw

rng = np.random.default_rng(0)

def arc(cx, cy, rx, ry, a0, a1, n=24):
    t = np.linspace(np.radians(a0), np.radians(a1), n)
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], 1)   # y down, angle 0 = right, 90 = down

def line(p, q, n=10):
    t = np.linspace(0, 1, n)[:, None]
    return np.array(p) * (1 - t) + np.array(q) * t

def cat(*parts):
    return np.concatenate(parts, 0)

def styles():
    S = {d: [] for d in range(10)}
    # 0
    S[0] += [[arc(.5, .5, .32, .48, -90, 270)], [arc(.5, .5, .36, .48, -100, 255)], [arc(.5, .5, .28, .48, 270, -90)],
             [arc(.5, .5, .4, .46, -80, 290)]]
    # 1
    S[1] += [[line((.5, 0), (.5, 1))], [cat(line((.3, .2), (.5, 0), 5), line((.5, 0), (.5, 1)))],
             [cat(line((.3, .22), (.52, 0), 5), line((.52, 0), (.5, 1))), line((.3, 1), (.72, 1), 6)],
             [line((.55, 0), (.45, 1))]]
    # 2
    S[2] += [[cat(arc(.5, .28, .32, .28, 190, 360 + 20), line((.8, .4), (.15, 1)), line((.15, 1), (.88, 1)))],
             [cat(arc(.5, .3, .35, .3, 200, 360 + 40), line((.76, .5), (.12, 1)), line((.12, 1), (.9, .98)))],
             [cat(arc(.5, .28, .3, .28, 180, 380), arc(.42, .78, .3, .22, -30, 120), arc(.2, .9, .1, .1, 300, 160), line((.15, .9), (.9, 1)))],
             [cat(arc(.48, .3, .34, .3, 170, 350), arc(.4, .75, .4, .3, -10, 100), line((.3, 1), (.9, 1)))]]
    # 3
    S[3] += [[cat(arc(.48, .26, .3, .26, 200, 450), arc(.48, .74, .34, .26, 270, 520))],
             [cat(arc(.5, .26, .3, .26, 210, 440), arc(.5, .73, .36, .27, 280, 500))],
             [cat(line((.15, 0), (.82, 0)), line((.82, 0), (.4, .42)), arc(.48, .7, .36, .3, 270, 510))],
             [cat(arc(.45, .27, .3, .27, 190, 460), arc(.45, .74, .38, .26, 260, 530))]]
    # 4
    S[4] += [[cat(line((.6, 0), (.05, .68)), line((.05, .68), (.95, .68))), line((.7, .25), (.7, 1))],
             [cat(line((.18, 0), (.15, .6)), line((.15, .6), (.9, .6))), line((.72, 0), (.72, 1))],
             [cat(line((.72, 1), (.72, 0)), line((.72, 0), (.05, .7)), line((.05, .7), (.95, .7)))],
             [cat(line((.25, 0), (.05, .62)), line((.05, .62), (.92, .58))), line((.68, .1), (.7, 1))]]
    # 5
    S[5] += [[cat(line((.85, 0), (.22, 0)), line((.22, 0), (.18, .45)), arc(.48, .7, .36, .3, 220, 495))],
             [cat(line((.2, 0), (.15, .45)), arc(.48, .7, .36, .3, 220, 500)), line((.2, 0), (.85, 0))],
             [cat(line((.82, .02), (.25, 0)), line((.25, 0), (.2, .42)), arc(.45, .68, .37, .32, 225, 480))]]
    # 6
    S[6] += [[cat(arc(.75, .6, .55, .6, 250, 180), arc(.5, .7, .32, .3, 180, 540))],
             [cat(line((.7, 0), (.25, .55)), arc(.5, .72, .3, .28, 200, 560))],
             [cat(arc(.8, .65, .62, .65, 260, 180), arc(.48, .72, .3, .28, 180, 520))]]
    # 7
    S[7] += [[cat(line((.1, 0), (.9, 0)), line((.9, 0), (.35, 1)))],
             [cat(line((.1, 0), (.9, 0)), line((.9, 0), (.4, 1))), line((.38, .5), (.85, .5))],
             [cat(line((.1, .08), (.12, 0), 4), line((.12, 0), (.9, 0)), arc(.0, 0, .9, 1, 0, 80))],
             [cat(line((.15, 0), (.88, .04)), line((.88, .04), (.5, 1)))]]
    # 8
    S[8] += [[cat(arc(.5, .25, .26, .25, 90, 450), arc(.5, .74, .32, .26, -90, 270))],
             [cat(arc(.5, .26, .28, .26, 30, 330), line((.74, .13), (.24, .58), 6), arc(.5, .75, .3, .25, 220, 500), line((.78, .7), (.26, .4), 6))],
             [cat(arc(.5, .25, .24, .25, 0, 360)), arc(.5, .74, .32, .26, -90, 270)],
             [cat(arc(.5, .24, .26, .24, 120, 480), arc(.5, .73, .3, .27, -60, 300))]]
    # 9
    S[9] += [[cat(arc(.48, .3, .32, .3, 0, -360), line((.8, .3), (.78, 1)))],
             [cat(arc(.48, .3, .32, .3, 10, -350), arc(.2, .3, .6, .7, 0, 80))],
             [arc(.48, .3, .32, .3, 0, 360), line((.8, .25), (.72, 1))],
             [cat(arc(.5, .28, .3, .28, 30, -330), line((.78, .4), (.55, 1)))]]
    return S

STYLES = styles()

def distort(strokes, mirror=False):
    pts = np.concatenate(strokes, 0)
    # low-frequency wobble + per-point jitter
    out = []
    ang = rng.normal(0, .14); sh = rng.normal(0, .18); sx = rng.uniform(.75, 1.25); sy = rng.uniform(.85, 1.15)
    A = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]]) @ np.array([[1, sh], [0, 1]]) @ np.diag([sx, sy])
    ph = rng.uniform(0, 6.28, 4); amp = rng.uniform(0, .05, 2)
    for s in strokes:
        s = s.copy()
        if mirror: s[:, 0] = 1 - s[:, 0]
        s = s + rng.normal(0, .012, s.shape)
        s[:, 0] += amp[0] * np.sin(s[:, 1] * 5 + ph[0]); s[:, 1] += amp[1] * np.sin(s[:, 0] * 5 + ph[1])
        # random trim/extension at ends (kids overshoot or stop short)
        k0 = rng.integers(0, max(1, len(s) // 10)); k1 = len(s) - rng.integers(0, max(1, len(s) // 10))
        s = s[k0:k1] if k1 - k0 > 2 else s
        out.append((s - .5) @ A.T + .5)
    return out

def normalise(strokes, size=28, box=20, width=2.3, ss=4):
    """Same steps as the app: fit the drawing's bounding box into a box x box square (aspect kept),
    centre it in size x size, draw lines `width` px wide, antialias. Returns floats 0..1."""
    pts = np.concatenate(strokes, 0)
    x0, y0 = pts.min(0); x1, y1 = pts.max(0)
    w, h = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    sc = box / max(w, h)
    ox = (size - w * sc) / 2 - x0 * sc; oy = (size - h * sc) / 2 - y0 * sc
    img = Image.new('L', (size * ss, size * ss), 0); d = ImageDraw.Draw(img)
    lw = max(1, int(round(width * ss)))
    for s in strokes:
        p = [((x * sc + ox) * ss, (y * sc + oy) * ss) for x, y in s]
        if len(p) == 1: p = p * 2
        d.line(p, fill=255, width=lw, joint='curve')
        for x, y in (p[0], p[-1]):
            r = lw / 2; d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    img = img.resize((size, size), Image.BOX)
    return np.asarray(img, np.float32) / 255.0

def make(n_per_digit, seed=0, mirror_rate=.15):
    global rng
    rng = np.random.default_rng(seed)
    X, Y = [], []
    for d in range(10):
        for i in range(n_per_digit):
            st = STYLES[d][rng.integers(len(STYLES[d]))]
            mir = d in (3, 4, 6, 7, 9) and rng.random() < mirror_rate
            X.append(normalise(distort(st, mir), width=rng.uniform(1.7, 3.0)).ravel()); Y.append(d)
    return np.array(X), np.array(Y)

if __name__ == '__main__':
    X, Y = make(6, seed=1)
    tiles = [Image.fromarray((x.reshape(28, 28) * 255).astype('uint8')).resize((56, 56)) for x in X]
    sheet = Image.new('L', (56 * 6, 56 * 10))
    for i, t in enumerate(tiles): sheet.paste(t, ((i % 6) * 56, (i // 6) * 56))
    sheet.save('/home/claude/hw/sheet.png')
