# p13 : ailes vues de profil, accrochées au dos du héros (une aile proche + l'aile lointaine assombrie derrière)
#  les planches d'ailes sont de face : on prend la demi-aile gauche (qui part vers l'arrière) et son reflet pour l'aile lointaine
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p13 ailes profil' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
OLD = "    const w = wEq(); if (w && WING_IMG.complete && !h.dead) { const fw = [0, 1, 2, 3, 2, 1][Math.floor(time * (B.walk ? 9 : 5)) % 6], ws = 0.62; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(CX - 10, YF - 88); ctx.drawImage(WING_IMG, fw * 168, WINGS[w].row * 168, 168, 168, -84 * ws, -48 * ws, 168 * ws, 168 * ws); ctx.restore(); }\n    if (!im || !im.complete) return;"
rep(OLD, "    if (!im || !im.complete) return;")
rep("    if (hasA) auraBack(SA, ka, f, row, x0, y0, sc, time);\n", "    if (hasA) auraBack(SA, ka, f, row, x0, y0, sc, time);\n    if (!h.dead) sideWings(SA, ka, time, sc, by); // p13 ailes profil\n")
rep("function drawSideHero(time, anim) {", r"""// p13 : point d'accroche des ailes (omoplate) mesuré une fois par forme sur l'image d'attente
const WANC = {}, WDARK = { c: null };
function wingAnchor(SA, key) { if (WANC[key]) return WANC[key]; const im = SIDEI[key]; if (!im || !im.complete) return null;
  const c = document.createElement('canvas'); c.width = SA.cw; c.height = SA.ch; const g = c.getContext('2d'); g.drawImage(im, 0, SA.ch, SA.cw, SA.ch, 0, 0, SA.cw, SA.ch);
  const d = g.getImageData(0, 0, SA.cw, SA.ch).data, op = (x, y) => d[(y * SA.cw + x) * 4 + 3] > 120; let top = SA.foot;
  for (let y = 0; y < SA.foot; y++) { let n = 0; for (let x = Math.max(0, SA.ax - 18); x < Math.min(SA.cw, SA.ax + 18); x++) if (op(x, y)) n++; if (n >= 4) { top = y; break; } }
  const hgt = SA.foot - top, sy = Math.round(top + hgt * 0.22); let back = SA.ax; // dos : bord gauche du corps à hauteur des épaules (on ignore la cape flottante)
  for (let x = SA.ax; x > SA.ax - hgt * 0.35; x--) { if (!op(x, sy)) break; back = x; }
  return WANC[key] = { x: back + hgt * 0.06, y: sy, h: hgt }; }
function wingDark() { if (WDARK.c || !WING_IMG.complete) return WDARK.c; const c = document.createElement('canvas'); c.width = WING_IMG.width; c.height = WING_IMG.height; const g = c.getContext('2d'); g.drawImage(WING_IMG, 0, 0);
  g.globalCompositeOperation = 'source-atop'; g.fillStyle = 'rgba(10,4,14,.5)'; g.fillRect(0, 0, c.width, c.height); return WDARK.c = c; }
function sideWings(SA, key, time, sc, by) { const w = wEq(); if (!w || !WING_IMG.complete) return; const A = wingAnchor(SA, key); if (!A) return;
  const fw = [0, 1, 2, 3, 2, 1][Math.floor(time * (B.walk ? 10 : 4.5)) % 6], row = WINGS[w].row, ws = A.h * sc * 1.1 / 105; // ~ la hauteur du héros
  const rx = CX + (A.x - SA.ax) * sc, ry = YF + (A.y - SA.foot) * sc + by, RX = 83, RY = 58; // racine de l'aile dans la planche
  ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  const dk = wingDark(); if (dk) { ctx.save(); ctx.translate(rx + 7 * sc, ry - 6 * sc); ctx.rotate(0.62); ctx.scale(-0.8 * ws, 0.86 * ws); // aile lointaine : moitié droite retournée, plus petite et sombre
    ctx.drawImage(dk, fw * 168 + 84, row * 168, 84, 168, -(168 - 84 - RX), -RY, 84, 168); ctx.restore(); }
  ctx.translate(rx, ry); ctx.rotate(0.42); ctx.scale(ws, ws); ctx.drawImage(WING_IMG, fw * 168, row * 168, 84, 168, -RX, -RY, 84, 168); ctx.restore(); // aile proche
  if (w === 'enfer' || w === 'givre' || w === 'dechu') { if (Math.random() < 0.25) B.fx.push({ k: 'p', x: rx - rand(5, 60) * ws, y: ry + rand(-20, 50) * ws, vx: 0, vy: w === 'givre' ? 10 : -16, g: 0, c: WINGS[w].c, t: 0, d: 0.7, r: 1 }); } }
function drawSideHero(time, anim) {""")
s = s.replace('<style id="sv">', '<style id="sv">/* p13 ailes profil */', 1)
open(P, 'w').write(s); print('p13 ailes profil ok')
