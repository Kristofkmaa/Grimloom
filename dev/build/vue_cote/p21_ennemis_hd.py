# p21 : ennemis de profil HD (planches build_enemy_hd.py -> dev/assets_enemy.js, ASSETS.DEMHD) : remplacent les anciennes planches, dessinés lissés
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p21 ennemis hd' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

rep("for (const k in ASSETS.DEM) { const im = new Image();",
    "Object.assign(ASSETS.DEM, ASSETS.DEMHD || {}); // p21 ennemis hd\nfor (const k in ASSETS.DEM) { const im = new Image();")
rep("  ctx.save(); ctx.imageSmoothingEnabled = false; if (o.alpha !== undefined) ctx.globalAlpha = o.alpha;",
    "  ctx.save(); ctx.imageSmoothingEnabled = !!A.hd; ctx.imageSmoothingQuality = 'high'; if (o.alpha !== undefined) ctx.globalAlpha = o.alpha;")
rep("const R = A.anims.idle_S || A.anims.walk_S; g.save(); g.imageSmoothingEnabled = false;",
    "const R = A.anims.idle_S || A.anims.walk_S; g.save(); g.imageSmoothingEnabled = !!A.hd;")
rep("const R = A.anims.walk_S; g.imageSmoothingEnabled = false;", "const R = A.anims.walk_S; g.imageSmoothingEnabled = !!A.hd;")
s = s.replace('<style id="sv">', '<style id="sv">/* p21 ennemis hd */', 1)
open(P, 'w').write(s); print('p21 ennemis hd ok')
