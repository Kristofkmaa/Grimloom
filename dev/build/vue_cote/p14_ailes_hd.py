# p14 : ailes de profil HD (planches build_wings.py -> dev/assets_wings.js) ; l'ancienne méthode reste pour une aile sans planche
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p14 ailes hd' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("function sideWings(SA, key, time, sc, by) { const w = wEq(); if (!w || !WING_IMG.complete) return; const A = wingAnchor(SA, key); if (!A) return;",
r"""const WSI = {}, WSD = {}; for (const k in (ASSETS.wingside || {})) { const i = new Image(); i.src = ASSETS.wingside[k].src; WSI[k] = i; } // p14 ailes hd
function wsDark(k) { if (WSD[k]) return WSD[k]; const im = WSI[k]; if (!im || !im.complete) return null; const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0); g.globalCompositeOperation = 'source-atop'; g.fillStyle = 'rgba(8,3,12,.55)'; g.fillRect(0, 0, c.width, c.height); return WSD[k] = c; }
function sideWings(SA, key, time, sc, by) { const w = wEq(); if (!w) return; const A = wingAnchor(SA, key); if (!A) return;
  const WS = ASSETS.wingside && ASSETS.wingside[w], im = WSI[w];
  if (WS && im && im.complete) { // battement : déployé → mi-course → replié → mi-course, plus rapide pendant l'avance
    const fr = Math.floor(time * (B.walk ? 9 : 4)) % WS.n, k = A.h * sc * 1.15 / WS.h, rx = CX + (A.x - SA.ax) * sc, ry = YF + (A.y - SA.foot) * sc + by, dk = wsDark(w);
    ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    if (dk) { const f2 = (fr + 1) % WS.n; ctx.save(); ctx.translate(rx + 8 * sc, ry - 7 * sc); ctx.rotate(0.12); ctx.scale(0.86 * k, 0.86 * k); ctx.drawImage(dk, f2 * WS.cw, 0, WS.cw, WS.ch, -WS.rx, -WS.ry, WS.cw, WS.ch); ctx.restore(); } // aile lointaine
    ctx.translate(rx, ry); ctx.scale(k, k); ctx.drawImage(im, fr * WS.cw, 0, WS.cw, WS.ch, -WS.rx, -WS.ry, WS.cw, WS.ch); ctx.restore(); // aile proche
    if (w === 'enfer' || w === 'givre' || w === 'dechu') { if (Math.random() < 0.25) B.fx.push({ k: 'p', x: rx - rand(10, 90) * k * 0.5, y: ry + rand(-60, 90) * k * 0.5, vx: 0, vy: w === 'givre' ? 10 : -16, g: 0, c: WINGS[w].c, t: 0, d: 0.7, r: 1 }); }
    return; }
  if (!WING_IMG.complete) return;""")
s = s.replace('<style id="sv">', '<style id="sv">/* p14 ailes hd */', 1)
open(P, 'w').write(s); print('p14 ailes hd ok')
