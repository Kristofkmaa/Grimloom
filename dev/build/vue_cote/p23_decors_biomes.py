# p23 : un décor par biome (ASSETS.biomeBg[1..6], dev/assets_biomes.js) à la place du cimetière recoloré ; bandes raccordées en boucle
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p23 decors biomes' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep(" if (!SBG.complete || !SBG.naturalWidth) { ctx.fillStyle = '#1a1028'; ctx.fillRect(0, top, BW, VH); return; }\n  const s2 = VH / SBG.naturalHeight, w = SBG.naturalWidth * s2, off = ((B.scroll * ZW) % w + w) % w; ctx.imageSmoothingEnabled = false;\n  for (let x = -off; x < BW; x += w) ctx.drawImage(SBG, Math.floor(x), top, Math.ceil(w) + 1, VH);\n  const bi = BIOMES.indexOf(biome()); if (bi > 0) {",
    "\n  const bi = BIOMES.indexOf(biome()), BI = BBG[bi] && BBG[bi].complete && BBG[bi].naturalWidth ? BBG[bi] : SBG; if (!BI.complete || !BI.naturalWidth) { ctx.fillStyle = '#1a1028'; ctx.fillRect(0, top, BW, VH); return; }\n  const s2 = VH / BI.naturalHeight, w = BI.naturalWidth * s2, off = ((B.scroll * ZW) % w + w) % w; ctx.imageSmoothingEnabled = BI !== SBG; ctx.imageSmoothingQuality = 'high';\n  for (let x = -off; x < BW; x += w) ctx.drawImage(BI, Math.floor(x), top, Math.ceil(w) + 1, VH);\n  if (bi > 0 && BI === SBG) {")
rep("function drawSideBg(VH) { const top = -OFFY;",
    "const BBG = {}; for (const k in (ASSETS.biomeBg || {})) { BBG[k] = new Image(); BBG[k].src = ASSETS.biomeBg[k]; } // p23 decors biomes\nfunction drawSideBg(VH) { const top = -OFFY;")
s = s.replace('<style id="sv">', '<style id="sv">/* p23 decors biomes */', 1)
open(P, 'w').write(s); print('p23 decors biomes ok')
