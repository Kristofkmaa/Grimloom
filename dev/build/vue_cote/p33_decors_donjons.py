# p33 : un décor par donjon et pour le raid (ASSETS.dunBg[clé], dev/assets_dun.js) : fixe, centré ; sinon décor du biome
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p33 decors donjons' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("function drawSideBg(VH) { const top = -OFFY;\n",
    "const DNBG = {}; for (const k in (ASSETS.dunBg || {})) DNBG[k] = lazyImg(ASSETS.dunBg[k]); // p33 decors donjons\nfunction drawSideBg(VH) { const top = -OFFY;\n  { const dk = B.dun && (B.dun.raid ? 'raid' : B.dun.k), I = dk && DNBG[dk]; if (I && I.complete && I.naturalWidth) { const s3 = VH / I.naturalHeight, w = I.naturalWidth * s3; ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(I, Math.round((BW - w) / 2 + (B.dun.raid ? w * 0.08 : 0)), top, w, VH); return; } }\n")
rep("function startDunWave() {", "function startDunWave() { { const dk = B.dun && (B.dun.raid ? 'raid' : B.dun.k); if (dk && DNBG[dk]) DNBG[dk].load(); }")
s = s.replace('<style id="sv">', '<style id="sv">/* p33 decors donjons */', 1)
open(P, 'w').write(s); print('p33 ok')
