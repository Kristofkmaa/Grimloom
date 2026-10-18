# Repère la selle image par image sur chaque planche de monture (dev/assets_mount.js) : suivi d'un motif autour de la selle
#  de l'image d'attente, avec rotation (cabrage). Écrit A.seats = [rangée][image] = [x, y] (pixels de la case).
import re, json, base64, io, sys, os
import numpy as np
from PIL import Image
from skimage.feature import match_template
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
SEAT = { 'chopper': [92, 100], 'cercueil': [126, 112], 'coq': [115, 90], 'escargot': [130, 108], 'destrier_rouge': [104, 88], 'destrier_os': [112, 90] }
P = D + 'assets_mount.js'; t = open(P).read()
for k, (qx, qy) in SEAT.items():
    mo = re.search(r'(ASSETS\.MOUNT\.%s = )(\{.*\});' % k, t); A = json.loads(mo.group(2))
    im = np.array(Image.open(io.BytesIO(base64.b64decode(A['src'].split(',')[1]))).convert('RGBA')).astype(float)
    cw, ch = A['cw'], A['ch']; cell = lambda r, f: im[r * ch:(r + 1) * ch, f * cw:(f + 1) * cw]
    def lum(c): return (c[..., :3].mean(-1) * (c[..., 3] / 255))
    ref = lum(cell(1, 0)); h = 18; w = 26
    tpl0 = ref[qy - h:qy + h, qx - w:qx + w]
    seats = []
    for r in range(3):
        row = []
        for f in range(4):
            tgt = lum(cell(r, f)); best = (-2, qx, qy)
            for ang in ([0] if r < 2 else range(-45, 31, 5)):
                tp = ndimage.rotate(tpl0, ang, reshape=False, order=1) if ang else tpl0
                R = 50 if r == 2 else 22; x0, y0 = max(0, qx - w - R), max(0, qy - h - R)
                sub = tgt[y0:qy + h + R, x0:qx + w + R]; res = match_template(sub, tp); y, x = np.unravel_index(np.argmax(res), res.shape); x += x0; y += y0
                # préférence pour un déplacement raisonnable
                v = res[y - y0, x - x0] - 0.002 * np.hypot(x + w - qx, y + h - qy)
                if v > best[0]: best = (v, x + w, y + h)
            row.append([int(best[1]), int(best[2])])
        seats.append(row)
    FIX = {'destrier_os': {(0, 2): [119, 104], (0, 3): [119, 104]}, 'destrier_rouge': {(2, 1): [125, 76]}, 'chopper': {(2, 1): [90, 100]}, 'escargot': {(2, 3): [120, 108]}, 'coq': {(2, 0): [110, 92], (2, 2): [118, 90], (2, 3): [112, 92]}}
    for (r, f), v in FIX.get(k, {}).items(): seats[r][f] = v
    A['seats'] = seats; print(k, seats)
    pv = os.environ.get('PREVIEW')
    if pv:
        from PIL import ImageDraw
        o = Image.fromarray(im.astype('uint8')); bg = Image.new('RGBA', o.size, (40, 30, 40, 255)); bg.alpha_composite(o); dr = ImageDraw.Draw(bg)
        for r in range(3):
            for f in range(4): x, y = seats[r][f]; dr.ellipse([f * cw + x - 4, r * ch + y - 4, f * cw + x + 4, r * ch + y + 4], fill=(0, 255, 0, 255))
        bg.save(pv + '/seat_' + k + '.png')
    t = t.replace(mo.group(0), mo.group(1) + json.dumps(A) + ';')
open(P, 'w').write(t)
