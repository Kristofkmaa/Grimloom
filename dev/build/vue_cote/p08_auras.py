# patch v27 : auras vivantes des héros de profil (couche aura séparée par build_side.py --aura=…)
#  ondulation de bas en haut, respiration, halo qui vacille, éclat additif, particules propres à chaque aura
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v27' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

rep("const SIDEI = {}; for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; }",
r"""const SIDEI = {}, SIDEA = {}; for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; if (ASSETS.side[k].aura) { const a = new Image(); a.src = ASSETS.side[k].aura; SIDEA[k] = a; } }
// patch v27 : réglages des auras vivantes (couleur du halo, particules)
const AFX = {
  violet: { glow: '150,60,255', p: ['#c070ff', '#8a40ff', '#e0b8ff'], kind: 'soul', amp: 1 },
  feu: { glow: '255,110,30', p: ['#ffb040', '#ff6020', '#ffe080'], kind: 'ember', amp: 1.2 },
  glace: { glow: '120,200,255', p: ['#ffffff', '#c8ecff', '#8ad0ff'], kind: 'snow', amp: 0.7 },
  sang: { glow: '220,20,40', p: ['#ff3040', '#b01020', '#ff7080'], kind: 'drip', amp: 0.9 },
  sacre: { glow: '255,215,110', p: ['#fff0b0', '#ffd860', '#ffffff'], kind: 'dust', amp: 0.8 },
  foudre: { glow: '170,210,255', p: ['#ffffff', '#bfe8ff', '#fff6a0'], kind: 'spark', amp: 0.8 },
  vert: { glow: '90,255,140', p: ['#a0ffb0', '#50e080', '#e0ffe0'], kind: 'soul', amp: 1 } };
const AUC = document.createElement('canvas'), AUG = AUC.getContext('2d'), AUW = document.createElement('canvas'), AUWG = AUW.getContext('2d');
function drawAura(SA, key, f, row, x0, y0, sc, time, pass) { // x0,y0 : coin haut-gauche de la case à l'écran
  const im = SIDEA[key], F = AFX[SA.fx] || AFX.violet; if (!im || !im.complete) return;
  if (AUC.width !== SA.cw || AUC.height !== SA.ch) { AUC.width = SA.cw; AUC.height = SA.ch; }
  AUG.clearRect(0, 0, SA.cw, SA.ch); AUG.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, 0, 0, SA.cw, SA.ch);
  const br = 1 + 0.035 * Math.sin(time * 3.1), amp = 7 * F.amp;
  if (AUW.width !== SA.cw || AUW.height !== SA.ch) { AUW.width = SA.cw; AUW.height = SA.ch; }
  AUWG.clearRect(0, 0, SA.cw, SA.ch); // ondulation calculée en pixels de la planche (pas de raccords visibles), puis un seul dessin lissé
  for (let y = 0; y < SA.ch; y += 2) { const k = 1 - y / SA.ch, dx = Math.round(Math.sin(y * 0.05 - time * 7) * amp * (0.25 + k) + Math.sin(y * 0.13 + time * 11) * amp * 0.3 * k), lift = pass ? 0 : Math.round(Math.max(0, Math.sin(time * 2.2 + y * 0.02)) * 3 * k);
    AUWG.drawImage(AUC, 0, y, SA.cw, 2, dx, y - lift, SA.cw, 2); }
  ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  if (pass) { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.16 + 0.12 * Math.sin(time * 4.3); }
  else ctx.globalAlpha = 0.9 + 0.1 * Math.sin(time * 5.7);
  const cx = x0 + SA.ax * sc, fy = y0 + SA.foot * sc; ctx.drawImage(AUW, cx - SA.ax * sc * br, fy - SA.foot * sc * br, SA.cw * sc * br, SA.ch * sc * br);
  ctx.restore(); }
function auraLife(SA, time, dt) { // halo + particules autour du héros
  const F = AFX[SA.fx] || AFX.violet, h = B.hero; if (h.dead) return;
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(CX - 4, YF - 46, 74 + 6 * Math.sin(time * 2.7), `rgba(${F.glow},1)`, 0.2 + 0.08 * Math.sin(time * 3.9) + (Math.random() < 0.04 ? 0.08 : 0)); ctx.restore();
  const rate = { soul: 3, ember: 14, snow: 9, drip: 5, dust: 8, spark: 4 }[F.kind] || 5; if (Math.random() > dt * rate) return;
  const c = pick(F.p), x = CX + rand(-34, 30), y = YF - rand(6, 100);
  if (F.kind === 'soul') B.fx.push({ k: 'p', x, y, vx: rand(-6, 6), vy: rand(-26, -14), g: -4, c, t: 0, d: rand(1.2, 1.9), r: rand(1.6, 2.6) });
  else if (F.kind === 'ember') B.fx.push({ k: 'p', x, y: YF - rand(0, 70), vx: rand(-10, 6), vy: rand(-55, -30), g: -10, c, t: 0, d: rand(0.6, 1.1), r: rand(0.7, 1.4) });
  else if (F.kind === 'snow') B.fx.push({ k: 'p', x: x + rand(-10, 10), y: YF - rand(40, 120), vx: rand(-10, 4), vy: rand(10, 22), g: 0, c, t: 0, d: rand(1, 1.6), r: rand(0.7, 1.3) });
  else if (F.kind === 'drip') B.fx.push({ k: 'p', x, y, vx: rand(-3, 3), vy: rand(5, 20), g: 180, c, t: 0, d: rand(0.5, 0.8), r: rand(0.8, 1.4) });
  else if (F.kind === 'dust') B.fx.push({ k: 'p', x, y, vx: rand(-5, 5), vy: rand(-18, -8), g: -2, c, t: 0, d: rand(1.2, 2), r: rand(0.6, 1.2) });
  else { const pts = [[x, y]]; for (let i = 0; i < 4; i++) pts.push([pts[i][0] + rand(-9, 9), pts[i][1] + rand(4, 11)]); B.fx.push({ k: 'bolt', pts, t: 0, d: 0.13 }); } }""")

rep("    if (!im || !im.complete) return; ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, Math.round(CX - SA.ax * sc), Math.round(YF - SA.foot * sc + by), Math.round(SA.cw * sc), Math.round(SA.ch * sc)); ctx.restore(); return; }",
r"""    if (!im || !im.complete) return; const x0 = Math.round(CX - SA.ax * sc), y0 = Math.round(YF - SA.foot * sc + by), ka = curForm(), hasA = !!SIDEA[ka];
    if (hasA) { auraLife(SA, time, 1 / 60); drawAura(SA, ka, f, row, x0, y0, sc, time, 0); }
    ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, x0, y0, Math.round(SA.cw * sc), Math.round(SA.ch * sc)); ctx.restore();
    if (hasA) drawAura(SA, ka, f, row, x0, y0, sc, time, 1); return; }""")
s = s.replace('<style id="sv">', '<style id="sv">/* patch v27 */', 1)
open(P, 'w').write(s); print('patch v27 ok')
