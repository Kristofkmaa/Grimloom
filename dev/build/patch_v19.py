# patch v19 : Sorcier de profil (8 formes) dans le combat de côté. Les planches sont dans assets_side.js (build_side.py).
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v19' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const sideHero = () => S.cls === 'knight' && S.form === 'ecuyer';",
    "// patch v19 : héros de profil = Écuyer, ou toute forme présente dans ASSETS.side (planches build_side.py)\nconst SIDEI = {}; for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; }\nconst sideHero = () => (S.cls === 'knight' && S.form === 'ecuyer') || !!(ASSETS.side && ASSETS.side[curForm()]);")
rep("function drawSideHero(time, anim) { const h = B.hero, C = 109, sc = 0.7; let im = SHI, row = 2, f = Math.floor(time * 2.5) % 2 ? 2 : 0;",
    """function drawSideHero(time, anim) { const h = B.hero, SA = ASSETS.side && ASSETS.side[curForm()];
  if (SA) { const im = SIDEI[curForm()], sc = 0.69 * (SA.k || 1); let row = 1, f = 0, by = 0; // rangées : marche · sort · touché (2) + mort (2)
    if (h.dead) { row = 2; f = h.deadT < 0.3 ? 2 : 3; } else if (anim === 'course') { row = 0; f = Math.floor(time * 10) % 4; }
    else if (anim === 'tir') { f = clamp(Math.floor((1 - Math.max(0, h.shootT) / 0.3) * 4), 0, 3); } else if (anim === 'touche') { row = 2; f = 0; } else by = Math.round(Math.sin(time * 2.6) * 1.2);
    const w = wEq(); if (w && WING_IMG.complete && !h.dead) { const fw = [0, 1, 2, 3, 2, 1][Math.floor(time * (B.walk ? 9 : 5)) % 6], ws = 0.5; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(CX - 8, YF - 70); ctx.drawImage(WING_IMG, fw * 168, WINGS[w].row * 168, 168, 168, -84 * ws, -48 * ws, 168 * ws, 168 * ws); ctx.restore(); }
    if (!im || !im.complete) return; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, Math.round(CX - SA.ax * sc), Math.round(YF - SA.foot * sc + by), Math.round(SA.cw * sc), Math.round(SA.ch * sc)); ctx.restore(); return; }
  const C = 109, sc = 0.7; let im = SHI, row = 2, f = Math.floor(time * 2.5) % 2 ? 2 : 0;""")
open(P, 'w').write(s); print('patch v19 ok')
