# Planche ChatGPT fond vert 4×3 d'ENNEMI de profil (regard vers la GAUCHE) -> sprite HD pour le combat de côté.
# Rangée 0 : marche (4) · rangée 1 : attaque (4) · rangée 2 : touché (1) puis mort (3).
# usage : python3 dev/build/build_enemy_hd.py planche.png clé [--h=hauteur affichée] [--bg=magenta] [--row4=r,c;r,c…] [--anims={json}]
#   clé = n_ghoul, n_bat… : remplace l'ancienne planche (même taille affichée qu'avant, sauf --h)
# Écrit/complète dev/assets_enemy.js (ASSETS.DEMHD[clé]), fusionné dans ASSETS.DEM par p21.
import sys, os, io, re, json, base64
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.segmentation import watershed
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
path, key = sys.argv[1], sys.argv[2]
opt = dict(a[2:].split('=', 1) for a in sys.argv[3:] if a.startswith('--') and '=' in a)
S = float(opt.get('s', os.environ.get('ENEMY_S', '0.42')))
im = Image.open(path).convert('RGB'); a = np.array(im).astype(int); H, W = a.shape[:2]; cw, ch = W / 4, H / 3
r, g, b = a[..., 0], a[..., 1], a[..., 2]
bg = np.median(np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3), a[-8:, :8].reshape(-1, 3), a[-8:, -8:].reshape(-1, 3)]), 0)
d = np.sqrt(((a - bg) ** 2).sum(-1))
al = np.clip((d - 60) / 70, 0, 1)
if opt.get('bg') == 'magenta': keyed = (np.minimum(r, b) - g > 60)
else: keyed = (g - np.maximum(r, b) > 40) & (g > 120)
al = np.where(keyed & (d < 170), 0.0, al)
fg = al > 0.5
lab, n = ndimage.label(fg); sz = ndimage.sum(fg, lab, range(1, n + 1)); fg &= np.isin(lab, 1 + np.where(sz >= 6)[0]); al = np.where(fg, al, 0)
if opt.get('bg') != 'magenta':  # reflet vert sur les bords
    edge = fg & ndimage.binary_dilation(~fg, iterations=3); m = edge & (g > np.maximum(r, b)); a[..., 1] = np.where(m, np.maximum(r, b), g)
else:
    edge = fg & ndimage.binary_dilation(~fg, iterations=3); m = edge & (np.minimum(r, b) > g + 20); a[..., 0] = np.where(m, g, r); a[..., 2] = np.where(m, g, b)
semi = (al > 0.02) & (al < 0.98)   # bords et fumées : on retire la couleur du fond mélangée au dessin
un = (a - (1 - al[..., None]) * bg) / np.maximum(al[..., None], 0.25)
a = np.where(semi[..., None], np.clip(un, 0, 255), a).astype(int)
if opt.get('bg') == 'magenta':   # fumées roses : part du magenta du fond -> rendue transparente
    mg = np.clip((np.minimum(a[..., 0], a[..., 2]) - a[..., 1] - 25) / 200, 0, 0.85) * fg
    a = np.clip((a - mg[..., None] * bg) / (1 - mg[..., None]), 0, 255).astype(int); al = al * (1 - mg)
    rr, gg, bb = a[..., 0], a[..., 1], a[..., 2]; pk = fg & (rr > gg + 12) & (bb > gg + 12)   # teinte rose restante -> fumée jaune pâle
    L = (0.3 * rr + 0.55 * gg + 0.15 * bb); a = np.where(pk[..., None], np.dstack([L * 1.02, L, L * 0.72]).clip(0, 255), a).astype(int); al = np.where(pk, al * 0.85, al)
rgba = np.dstack([a, (al * 255).astype(int)]).astype('uint8')
# partage entre les 12 images : bassins autour du gros morceau de chaque case, puis chaque éclat va à l'image la plus proche
dist = ndimage.distance_transform_edt(fg); mk = np.zeros(fg.shape, int)
for ri in range(3):
    for ci in range(4):
        y0, y1, x0, x1 = int(ri * ch), int((ri + 1) * ch), int(ci * cw), int((ci + 1) * cw)
        win = np.zeros_like(fg); win[y0 + 10:y1 - 10, x0 + 30:x1 - 30] = True; w = win & fg
        if w.sum() < 300: continue
        core = (dist > max(3, np.percentile(dist[w], 75))) & win; lb, nn = ndimage.label(core)
        if nn: mk[lb == 1 + int(np.argmax(ndimage.sum(core, lb, range(1, nn + 1))))] = ri * 4 + ci + 1
seg = watershed(-dist, mk, mask=fg)
if (fg & (seg == 0)).any():
    _, (iy, ix) = ndimage.distance_transform_edt(seg == 0, return_indices=True); seg = np.where(fg, seg[iy, ix], 0)
# position : chaque image garde sa place dans sa case (pieds sur la même ligne), avec une marge pour ce qui déborde
M = int(cw * float(opt.get('m', 0.25))); MT = int(ch * 0.3)
walk = [seg == v for v in (1, 2, 3, 4)]
foot = int(np.median([np.where(m)[0].max() for m in walk if m.any()]))   # ligne des pieds (rangée 0, repère de la case)
CW, CH = round((cw + 2 * M) * S), round((ch + MT) * S)
extra = [tuple(map(int, x.split(','))) for x in opt['row4'].split(';')] if 'row4' in opt else []   # --row4=r,c;r,c… : 4e rangée faite d'images existantes (ex. rage)
out = Image.new('RGBA', (CW * 4, CH * (4 if extra else 3)))
for v in range(1, 13):
    msk = seg == v
    if msk.sum() < 300: continue
    ri, ci = (v - 1) // 4, (v - 1) % 4
    fr = rgba.copy(); fr[..., 3] = np.where(msk, fr[..., 3], 0)
    X0, Y0 = int(ci * cw) - M, int(ri * ch) - MT
    crop = Image.fromarray(fr).crop((X0, Y0, X0 + int(cw + 2 * M), Y0 + int(ch + MT)))
    sm = crop.resize((CW, CH), Image.LANCZOS)
    arr = np.array(sm); arr[..., 3] = np.clip((arr[..., 3].astype(int) - 30) * 255 // 170, 0, 255)
    out.alpha_composite(Image.fromarray(arr), (ci * CW, ri * CH))
    for j, (er, ec) in enumerate(extra):
        if (er, ec) == (ri, ci): out.alpha_composite(Image.fromarray(arr), (j * CW + int(opt.get('row4dx', 0)), 3 * CH))
FOOT = (foot + MT) * S   # depuis le haut de la case
w0 = walk[0]; ys, xs = np.where(w0)
ax = (np.median(xs) + M) * S; top = (ys.min()) * S; bh = FOOT - (ys.min() + MT) * S
# taille affichée : celle de l'ancienne planche (ou --h), via k
old = None
for f in [D + 'src.html']:
    mo = re.search(r'ASSETS\.DEM\.%s = \{"cw": (\d+), "ch": (\d+), "foot": (\d+), "bh": (\d+), "k": ([\d.]+)' % key, open(f).read())
    if mo: old = mo
k = float(opt['h']) / bh if 'h' in opt else (int(old.group(4)) * float(old.group(5)) / bh if old else 0.5)
spd = 0.5
m = {'cw': CW, 'ch': CH, 'foot': round(CH - FOOT, 1), 'bh': round(bh, 1), 'k': round(k, 4), 'spd': spd, 'ax': round(float(ax), 1), 'hd': 1,
     'anims': json.loads(opt['anims']) if 'anims' in opt else {'walk_S': [0, 4], 'atk_S': [1, 4], 'hit_S': [2, 1], 'die_S': [2, 4], 'idle_S': [0, 1]}}
bb = io.BytesIO(); out.save(bb, 'WEBP', quality=88, method=6, alpha_quality=100)
m['src'] = 'data:image/webp;base64,' + base64.b64encode(bb.getvalue()).decode()
NS, FN = ('MOUNT', 'assets_mount.js') if opt.get('dst') == 'mount' else ('DEMHD', 'assets_enemy.js')   # --dst=mount : planche de monture
P = D + FN; txt = open(P).read() if os.path.exists(P) else 'ASSETS.%s = ASSETS.%s || {};\n' % (NS, NS)
txt = re.sub(r'ASSETS\.%s\.%s = .*\n' % (NS, key), '', txt) + 'ASSETS.%s.%s = %s;\n' % (NS, key, json.dumps(m))
open(P, 'w').write(txt)
pv = os.environ.get('PREVIEW')
if pv:
    bgim = Image.new('RGBA', out.size, (40, 30, 40, 255)); bgim.alpha_composite(out)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(bgim)
    for ri in range(out.height // CH):
        for ci in range(4): dr.line([(ci * CW, ri * CH + FOOT), (ci * CW + CW, ri * CH + FOOT)], fill=(255, 255, 0, 120)); dr.line([(ci * CW + ax, ri * CH), (ci * CW + ax, ri * CH + CH)], fill=(0, 255, 255, 80))
    bgim.save(pv + '/en_' + key + '.png')
print(key, 'ok', CW, 'x', CH, 'k', m['k'], 'bh', m['bh'], len(bb.getvalue()) // 1024, 'Ko')
