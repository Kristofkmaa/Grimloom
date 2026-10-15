# Planche ChatGPT d'ailes de PROFIL (4 images en ligne, fond vert, racine au bord droit) -> dev/assets_wings.js
# usage : python3 dev/build/build_wings.py planche.png clé   (clé = corbeau | os | enfer | givre | dechu)
import sys, os, io, re, json, base64
import numpy as np
from PIL import Image
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
path, key = sys.argv[1], sys.argv[2]
S = float(os.environ.get('WING_S', '0.5')); CW, CH, RX, RY = 200, 470, 190, 215   # case de sortie et racine de l'aile
a = np.array(Image.open(path).convert('RGB')).astype(int); H, W = a.shape[:2]; r, g, b = a[..., 0], a[..., 1], a[..., 2]
bg = np.median(a[:10, :10].reshape(-1, 3), 0); d = np.sqrt(((a - bg) ** 2).sum(-1))
al = np.clip((d - 60) / 70, 0, 1); al = np.where((g - np.maximum(r, b) > 40) & (g > 120) & (d < 170), 0, al)
fg = al > 0.5; edge = fg & ndimage.binary_dilation(~fg, iterations=3); m = edge & (g > np.maximum(r, b)); a[..., 1] = np.where(m, np.maximum(r, b), g)
rgba = np.dstack([a, (al * 255).astype(int)]).astype('uint8')
lab, n = ndimage.label(fg); sz = ndimage.sum(fg, lab, range(1, n + 1)); big = np.isin(lab, 1 + np.where(sz >= 3000)[0])   # grandes pièces = ailes
out = Image.new('RGBA', (CW * 4, CH)); hs = []
for i in range(4):
    x0, x1 = int(i * W / 4), int((i + 1) * W / 4); col = big[:, x0:x1]; ys, xs = np.where(col)
    xr = xs.max(); near = ys[xs > xr - 18]; ry = int(np.median(near)) if i == 0 else ry0; ry0 = ry; hs.append(int((ys.max() - ys.min()) * S))
    fr = rgba[:, x0:x1].copy(); keep = ndimage.binary_dilation(col, iterations=40)   # garde les petits éclats/flocons proches de l'aile
    fr[..., 3] = np.where(keep, fr[..., 3], 0)
    im = Image.fromarray(fr); im = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)
    q = np.array(im); q[..., 3] = np.clip((q[..., 3].astype(int) - 40) * 255 // 150, 0, 255); im = Image.fromarray(q)
    out.alpha_composite(Image.new('RGBA', (1, 1)), (0, 0))
    ox, oy = i * CW + RX - round(xr * S), RY - round(ry * S)
    sx0, sy0 = max(0, -(ox - i * CW)), max(0, -oy); im = im.crop((sx0, sy0, min(im.width, CW - (ox - i * CW)), min(im.height, CH - oy)))
    out.alpha_composite(im, (max(i * CW, ox), max(0, oy)))
b2 = io.BytesIO(); out.save(b2, 'WEBP', quality=90, method=6, alpha_quality=100)
P = D + 'assets_wings.js'; txt = open(P).read() if os.path.exists(P) else 'ASSETS.wingside = ASSETS.wingside || {};\n'
txt = re.sub(r'ASSETS\.wingside\.%s = .*\n' % key, '', txt)
txt += 'ASSETS.wingside.%s = %s;\n' % (key, json.dumps({'cw': CW, 'ch': CH, 'rx': RX, 'ry': RY, 'n': 4, 'h': hs[0], 'src': 'data:image/webp;base64,' + base64.b64encode(b2.getvalue()).decode()}))
open(P, 'w').write(txt); out.save(os.environ.get('PREVIEW', '/tmp') + '/wing_%s.png' % key)
print(key, 'ok', hs, len(b2.getvalue()) // 1024, 'Ko')
