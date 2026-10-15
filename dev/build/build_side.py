# Planche ChatGPT fond vert 4×3 (héros de PROFIL, regard vers la droite) -> sprite pour le combat de côté.
# Rangée 0 : marche (4) · rangée 1 : attaque/sort (4) · rangée 2 : touché (2) puis mort (2).
# usage : python3 dev/build/build_side.py planche.png clé [--keep-green]
#   --ws : planche aux images collées (grosses auras) ; --claim=rang,col,x0,y0,x1,y1 pour forcer une zone
#   --aura=violet|feu|glace|sang|sacre|foudre|vert : sépare l'aura du corps (couche animée en jeu)
#   --keep-green : n'enlève pas le reflet vert des bords (pour les auras vertes, ex. la Liche)
# Écrit/complète dev/assets_side.js (ASSETS.side[clé] = {src, cw, ch, foot, ax}).
import sys, os, io, re, json, base64
import numpy as np
from PIL import Image
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
path, key = sys.argv[1], sys.argv[2]; keepg = '--keep-green' in sys.argv
S = float(os.environ.get('SIDE_S', '0.6'))   # 320 px de haut -> ~144 px : affiché pixel pour pixel sur téléphone (écran ×2)
Q = S / 0.3; CW, CH, FOOT, AX = round(int(os.environ.get('SIDE_W', '190')) * Q), round(128 * Q), round(116 * Q), round(92 * Q)   # case, ligne des pieds, axe du corps
im = Image.open(path).convert('RGB'); a = np.array(im).astype(int); H, W = a.shape[:2]
bg = np.median(np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3), a[-8:, :8].reshape(-1, 3), a[-8:, -8:].reshape(-1, 3)]), 0)
d = np.sqrt(((a - bg) ** 2).sum(-1)); r, g, b = a[..., 0], a[..., 1], a[..., 2]
greenish = (g - np.maximum(r, b) > 40) & (g > 120)
al = np.clip((d - 60) / 70, 0, 1)
if not keepg: al = np.where(greenish & (d < 170), np.minimum(al, 0.0), al)
fg = al > 0.5
lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=3)); lab = lab * fg
objs = ndimage.find_objects(lab); sizes = ndimage.sum(fg, lab, range(1, n + 1))
if not keepg:  # retire le reflet vert sur les bords
    edge = fg & ndimage.binary_dilation(~fg, iterations=3); m = edge & (g > np.maximum(r, b))
    a[..., 1] = np.where(m, np.maximum(r, b), g)
rgba = np.dstack([a, (al * 255).astype(int)]).astype('uint8')
cells = {}
if '--ws' in sys.argv:  # images collées (grosses auras) : partage par bassins autour du corps de chaque image
    from skimage.segmentation import watershed
    dist = ndimage.distance_transform_edt(fg); mk = np.zeros(fg.shape, int)
    for ri in range(3):
        for ci in range(4):
            y0, y1_, x0_ = int(ri * H / 3), int((ri + 1) * H / 3), int(ci * W / 4)
            win = np.zeros_like(fg); win[y0 + 20:y1_ - 10, x0_ + 60:x0_ + 300] = True
            core = (dist > max(8, np.percentile(dist[win & fg], 80) if (win & fg).any() else 8)) & win
            lb, nn = ndimage.label(core)
            if nn: big = 1 + int(np.argmax(ndimage.sum(core, lb, range(1, nn + 1)))); mk[lb == big] = ri * 4 + ci + 1
    for a in sys.argv:  # --claim=rang,col,x0,y0,x1,y1 : zone (pixels de la planche) donnée d'office à une image (ex. épée tendue)
        if a.startswith('--claim='): r_, c_, X0, Y0, X1, Y1 = map(int, a[8:].split(',')); z = np.zeros_like(fg); z[Y0:Y1, X0:X1] = True; mk[z & fg] = r_ * 4 + c_ + 1
    seg = watershed(-dist, mk, mask=fg)
    for v in range(1, 13):
        part = seg == v
        if part.sum() > 400: cells[((v - 1) // 4, (v - 1) % 4)] = [part]
else:
    def cut(prof, at, lo, hi):  # meilleure coupure (colonne/ligne la plus vide) près d'une ligne de la grille
        w = prof[max(lo, at - 130):min(hi, at + 130)]; return max(lo, at - 130) + int(np.argmin(w))
    for i, sl in enumerate(objs):
        if sl is None or sizes[i] < 400: continue
        m = lab[sl] == i + 1; oy, ox0 = sl[0].start, sl[1].start
        # morceaux : on recoupe un objet qui déborde sur plusieurs cases (images collées)
        xs_cut = [ox0]; ys_cut = [oy]
        for k in range(1, 4):
            gx = int(k * W / 4)
            if ox0 + 40 < gx < sl[1].stop - 40 and (sl[1].stop - ox0) > 1.4 * W / 4: xs_cut.append(ox0 + cut(m.sum(0), gx - ox0, 0, m.shape[1]))
        for k in range(1, 3):
            gy = int(k * H / 3)
            if oy + 40 < gy < sl[0].stop - 40 and (sl[0].stop - oy) > 1.3 * H / 3: ys_cut.append(oy + cut(m.sum(1), gy - oy, 0, m.shape[0]))
        xs_cut.append(sl[1].stop); ys_cut.append(sl[0].stop)
        for a0, a1 in zip(ys_cut, ys_cut[1:]):
            for b0, b1 in zip(xs_cut, xs_cut[1:]):
                part = np.zeros_like(fg); part[a0:a1, b0:b1] = m[a0 - oy:a1 - oy, b0 - ox0:b1 - ox0]
                if part.sum() < 400: continue
                cy, cx = ndimage.center_of_mass(part)
                ri, ci = min(2, int(cy // (H / 3))), min(3, int(cx // (W / 4))); cells.setdefault((ri, ci), []).append(part)

out = Image.new('RGBA', (CW * 4, CH * 3))
for (ri, ci), ids in cells.items():
    msk = np.logical_or.reduce(ids); ys, xs = np.where(msk); y1 = ys.max()
    fr = rgba.copy(); fr[..., 3] = np.where(msk, fr[..., 3], 0)
    x0 = int(ci * W / 4); crop = Image.fromarray(fr).crop((x0 - 140, y1 - int(CH / S), x0 - 140 + int(CW / S), y1 + 1))
    sm = crop.resize((round(crop.width * S), round(crop.height * S)), Image.LANCZOS)
    arr = np.array(sm); arr[..., 3] = np.clip((arr[..., 3].astype(int) - 40) * 255 // 150, 0, 255); sm = Image.fromarray(arr)
    # le corps est vers x0+170 dans la case source -> AX dans la case de sortie
    ox = round(AX - (140 + 170) * S); sm = sm.crop((max(0, -ox), 0, min(sm.width, CW - ox), sm.height)); out.alpha_composite(sm, (ci * CW + max(0, ox), ri * CH + FOOT - sm.height))
AURA = {  # teinte (degrés), saturation mini, luminosité mini
    'violet': [(250, 330, 0.16, 0.07), (190, 250, 0.10, 0.10, 'fumée')], 'feu': [(8, 62, 0.55, 0.62), (0, 30, 0.55, 0.30, 'fumée')], 'glace': [(178, 222, 0.22, 0.55)],
    'sang': [(342, 360, 0.55, 0.32), (0, 14, 0.55, 0.32), (330, 360, 0.40, 0.14, 'fumée'), (0, 22, 0.40, 0.14, 'fumée')], 'sacre': [(36, 64, 0.40, 0.72), (30, 75, 0.12, 0.70, 'fumée'), (0, 360, -1, 0.90, 'fumée')],
    'foudre': [(40, 75, 0.25, 0.80), (178, 225, 0.18, 0.75), (0, 360, -1, 0.94)], 'vert': [(75, 165, 0.30, 0.30)]}
ap = next((x[7:] for x in sys.argv if x.startswith('--aura=')), None); aura_out = None
if ap:
    import colorsys
    A = np.array(out).astype(float) / 255; rr, gg, bb, aa = A[..., 0], A[..., 1], A[..., 2], A[..., 3]
    mx, mn = A[..., :3].max(-1), A[..., :3].min(-1); v = mx; sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0); dl = np.maximum(mx - mn, 1e-6)
    hue = np.where(mx == rr, ((gg - bb) / dl) % 6, np.where(mx == gg, (bb - rr) / dl + 2, (rr - gg) / dl + 4)) * 60
    cand = np.zeros(aa.shape, bool)
    dense = ndimage.uniform_filter((aa > 0.5).astype(float), size=11) > 0.82   # cœur plein du personnage
    for r_ in AURA[ap]:
        h0, h1, s0, v0 = r_[:4]; c_ = (hue >= h0) & (hue <= h1) & ((sat >= s0) if s0 >= 0 else (sat < 0.15)) & (v >= v0)
        if len(r_) > 4: c_ &= ~dense   # 'fumée' : seulement en bordure, jamais dans le cœur du corps
        cand |= c_
    cand &= aa > 0.05
    body0 = (aa > 0.5) & ~cand
    inner = ndimage.uniform_filter(body0.astype(float), size=7) > 0.6   # détail coloré au milieu du corps (épée, gemme) : reste dans le corps
    am = cand & ~inner; am = ndimage.binary_opening(am, iterations=1) | (am & ~ndimage.binary_erosion(aa > 0.05, iterations=2))
    o = np.array(out); au = o.copy(); au[..., 3] = np.where(am, o[..., 3], 0); o[..., 3] = np.where(am, 0, o[..., 3])
    out = Image.fromarray(o); aura_out = Image.fromarray(au)
    print('aura', ap, int(am.sum() * 100 / max(1, (aa > 0.5).sum())), '% des pixels')
b = io.BytesIO(); out.save(b, 'WEBP', quality=90, method=6, alpha_quality=100)
P = D + 'assets_side.js'; txt = open(P).read() if os.path.exists(P) else 'ASSETS.side = ASSETS.side || {};\n'
txt = re.sub(r'ASSETS\.side\.%s = .*\n' % key, '', txt)
meta = {'cw': CW, 'ch': CH, 'foot': FOOT, 'ax': AX, 'k': round(0.3 / S, 4), 'src': 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()}
if aura_out is not None: b2 = io.BytesIO(); aura_out.save(b2, 'WEBP', quality=88, method=6, alpha_quality=100); meta['fx'] = ap; meta['aura'] = 'data:image/webp;base64,' + base64.b64encode(b2.getvalue()).decode()
txt += 'ASSETS.side.%s = %s;\n' % (key, json.dumps(meta))
open(P, 'w').write(txt)
out.save(os.environ.get('PREVIEW', '/tmp') + '/side_%s.png' % key)
if aura_out is not None: aura_out.save(os.environ.get('PREVIEW', '/tmp') + '/aura_%s.png' % key)
print(key, 'ok', sorted(cells), len(b.getvalue()) // 1024, 'Ko')
