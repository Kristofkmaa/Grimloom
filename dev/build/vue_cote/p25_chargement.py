# p25 : chargement à la demande des grosses images (monstres, héros, ailes, décors) : l'image ne se télécharge
#  que la première fois que le jeu en a besoin (premier test .complete / .naturalWidth). Avec build_pwa (images en fichiers a/…),
#  le jeu s'ouvre vite et ne télécharge que ce qui sert.
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p25 chargement' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
LAZY = r"""const IMC = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'complete').get, IMN = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'naturalWidth').get; // p25 chargement
function lazyImg(url) { const im = new Image(); let go = false; const st = () => { if (!go) { go = true; im.src = url; } };
  Object.defineProperty(im, 'complete', { get() { st(); return IMC.call(im); } }); Object.defineProperty(im, 'naturalWidth', { get() { st(); return IMN.call(im); } }); im.load = st; return im; }
"""
rep("for (const k in ASSETS.DEM) { const im = new Image(); im.src = ASSETS.DEM[k].src; IMG['D_' + k] = im; }",
    LAZY + "for (const k in ASSETS.DEM) IMG['D_' + k] = lazyImg(ASSETS.DEM[k].src);")
rep("for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; if (ASSETS.side[k].aura) { const a = new Image(); a.src = ASSETS.side[k].aura; SIDEA[k] = a; } }",
    "for (const k in (ASSETS.side || {})) { SIDEI[k] = lazyImg(ASSETS.side[k].src); if (ASSETS.side[k].aura) SIDEA[k] = lazyImg(ASSETS.side[k].aura); }")
rep("for (const k in (ASSETS.biomeBg || {})) { BBG[k] = new Image(); BBG[k].src = ASSETS.biomeBg[k]; }", "for (const k in (ASSETS.biomeBg || {})) BBG[k] = lazyImg(ASSETS.biomeBg[k]);")
rep("const RBG = new Image(); if (ASSETS.raidBg) RBG.src = ASSETS.raidBg.src;", "const RBG = ASSETS.raidBg ? lazyImg(ASSETS.raidBg.src) : new Image();")
rep("for (const k in (ASSETS.wingside || {})) { const i = new Image(); i.src = ASSETS.wingside[k].src; WSI[k] = i; }", "for (const k in (ASSETS.wingside || {})) WSI[k] = lazyImg(ASSETS.wingside[k].src);")
rep("for (const k in ASSETS) if (ASSETS[k].src) {", "for (const k in ASSETS) if (ASSETS[k].src && k !== 'raidBg') {")
# démarrage : on n'attend plus toutes les images (au plus 2,5 s), et jamais celles chargées à la demande
rep("const ready = () => Object.values(IMG).every(i => i.complete);", "const BOOT0 = Date.now(), ready = () => Date.now() - BOOT0 > 2500 || Object.values(IMG).every(i => i.load || i.complete);")
# monstres d'un biome : chargés dès qu'on y entre (et ceux du biome suivant en avance)
rep("function queueBiome(bi) { const M = BMOBS[bi % BMOBS.length];",
    "function warmBiome(bi) { const M = BMOBS[bi % BMOBS.length]; for (const key of [...M.pool, ...M.elites, ...M.boss.map(b => b[0] === 'p_idle' ? 'spawn1' : b[0])]) { const im = IMG['D_' + key]; if (im && im.load) im.load(); } const g = BBG[bi % BMOBS.length]; if (g && g.load) g.load(); }\nfunction queueBiome(bi) { warmBiome(bi); warmBiome(bi + 1); const M = BMOBS[bi % BMOBS.length];")
s = s.replace('<style id="sv">', '<style id="sv">/* p25 chargement */', 1)
open(P, 'w').write(s); print('p25 chargement ok')
