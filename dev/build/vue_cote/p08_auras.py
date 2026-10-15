# p08 : auras vivantes des héros de profil (couche aura séparée par build_side.py --aura=…)
#  le dessin reste intact : scintillement de la lumière, flammèches qui s'échappent des bords de l'aura,
#  halo + lumière au sol (+ cercle runique et contour pulsé pour les formes ultimes), embrasement à chaque attaque
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p08 auras' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

rep("const SIDEI = {}; for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; }",
r"""const SIDEI = {}, SIDEA = {}; for (const k in (ASSETS.side || {})) { const i = new Image(); i.src = ASSETS.side[k].src; SIDEI[k] = i; if (ASSETS.side[k].aura) { const a = new Image(); a.src = ASSETS.side[k].aura; SIDEA[k] = a; } }
// p08 auras : réglages par type (couleur de la lumière, couleurs et forme des flammèches)
const AFX = {
  violet: { glow: '150,60,255', p: ['#c070ff', '#8a40ff', '#e0b8ff', '#5a2090'], kind: 'soul', rate: 16 },
  feu: { glow: '255,110,30', p: ['#ffb040', '#ff6020', '#ffe080', '#ff3010'], kind: 'flame', rate: 28 },
  glace: { glow: '120,200,255', p: ['#ffffff', '#c8ecff', '#8ad0ff'], kind: 'shard', rate: 16 },
  sang: { glow: '220,20,40', p: ['#ff3040', '#b01020', '#ff7080'], kind: 'drop', rate: 12 },
  sacre: { glow: '255,215,110', p: ['#fff0b0', '#ffd860', '#ffffff'], kind: 'dust', rate: 18 },
  foudre: { glow: '170,210,255', p: ['#ffffff', '#bfe8ff', '#fff6a0'], kind: 'spark', rate: 10 },
  vert: { glow: '90,255,140', p: ['#a0ffb0', '#50e080', '#e0ffe0'], kind: 'soul', rate: 16 } };
const AUC = document.createElement('canvas'), AUG = AUC.getContext('2d', { willReadFrequently: true }), AUPTS = {};
const flick = (t, k) => 0.55 + 0.25 * Math.sin(t * 7.3 + k) + 0.15 * Math.sin(t * 13.1 + k * 2) + 0.05 * Math.sin(t * 29 + k * 3); // scintillement irrégulier
function auraCell(SA, key, f, row) { // la case de l'aura dans AUC + liste de ses pixels (points de départ des flammèches)
  const im = SIDEA[key]; if (!im || !im.complete) return null;
  if (AUC.width !== SA.cw || AUC.height !== SA.ch) { AUC.width = SA.cw; AUC.height = SA.ch; }
  AUG.clearRect(0, 0, SA.cw, SA.ch); AUG.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, 0, 0, SA.cw, SA.ch);
  const ck = key + ':' + row + ':' + f; if (!AUPTS[ck]) { const d = AUG.getImageData(0, 0, SA.cw, SA.ch).data, L = [];
    for (let y = 0; y < SA.ch; y += 2) for (let x = 0; x < SA.cw; x += 2) { const i = (y * SA.cw + x) * 4; if (d[i + 3] > 160 && d[i] + d[i + 1] + d[i + 2] > 180) L.push([x, y, `rgb(${d[i]},${d[i + 1]},${d[i + 2]})`]); }
    AUPTS[ck] = L; }
  return AUPTS[ck]; }
function wisp(F, x, y, c, big) { const k = F.kind, b = big ? 1.5 : 1;
  const o = { k: 'w', kind: k, x, y, c, t: 0, ph: rand(0, 6), s: rand(0.8, 1.3) * b };
  if (k === 'flame') Object.assign(o, { vx: rand(-8, 8), vy: rand(-48, -28) * b, d: rand(0.35, 0.6) });
  else if (k === 'soul') Object.assign(o, { vx: rand(-10, 10), vy: rand(-30, -16) * b, d: rand(0.8, 1.3) });
  else if (k === 'shard') Object.assign(o, { vx: rand(-14, 14), vy: rand(-18, 4) * b, d: rand(0.5, 0.9), rot: rand(0, 6) });
  else if (k === 'drop') Object.assign(o, { vx: rand(-4, 4), vy: rand(0, 12), g: 220, d: rand(0.5, 0.8) });
  else if (k === 'dust') Object.assign(o, { vx: rand(-8, 8), vy: rand(-26, -10) * b, d: rand(0.7, 1.2) });
  else Object.assign(o, { vx: 0, vy: 0, d: 0.12 });
  B.fx.push(o); }
function drawWisp(o) { const p = o.t / o.d, a = Math.max(0, 1 - p), s = o.s; ctx.save(); ctx.translate(Math.round(o.x + Math.sin(o.t * 9 + o.ph) * 2 * (o.kind === 'flame' || o.kind === 'soul' ? 1 : 0)), Math.round(o.y)); ctx.fillStyle = o.c;
  if (o.kind === 'flame') { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a; const h = (6 + 4 * (1 - p)) * s, w = (3 - 1.6 * p) * s; ctx.beginPath(); ctx.moveTo(0, -h); ctx.quadraticCurveTo(w, -h * 0.25, 0, 0); ctx.quadraticCurveTo(-w, -h * 0.25, 0, -h); ctx.fill(); }
  else if (o.kind === 'soul') { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a * 0.9; const r = 2.6 * s; ctx.beginPath(); ctx.arc(0, 0, r, Math.PI, 0); ctx.lineTo(r, r * 1.6); ctx.lineTo(r * 0.3, r); ctx.lineTo(-r * 0.3, r * 1.7); ctx.lineTo(-r, r); ctx.closePath(); ctx.fill(); ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = '#1a0628'; ctx.globalAlpha = a; ctx.fillRect(-r * 0.6, -r * 0.2, r * 0.45, r * 0.5); ctx.fillRect(r * 0.15, -r * 0.2, r * 0.45, r * 0.5); }
  else if (o.kind === 'shard') { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a; ctx.rotate((o.rot || 0) + o.t * 4); const r = 2.6 * s * (1 - p * 0.4); ctx.beginPath(); ctx.moveTo(0, -r * 1.6); ctx.lineTo(r * 0.6, 0); ctx.lineTo(0, r * 1.6); ctx.lineTo(-r * 0.6, 0); ctx.fill(); }
  else if (o.kind === 'drop') { ctx.globalAlpha = a; ctx.beginPath(); ctx.ellipse(0, 0, 1.3 * s, 2.2 * s, 0, 0, TAU); ctx.fill(); }
  else if (o.kind === 'dust') { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a; const r = 1.2 * s; ctx.fillRect(-r / 2, -r / 2, r, r); if (Math.sin(o.t * 14 + o.ph) > 0.6) { ctx.globalAlpha = a * 0.7; ctx.fillRect(-r * 2, -0.4, r * 4, 0.8); ctx.fillRect(-0.4, -r * 2, 0.8, r * 4); } }
  else { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a; ctx.strokeStyle = o.c; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(0, 0); let x = 0, y = 0; for (let i = 0; i < 4; i++) { x += rand(-5, 5); y += rand(3, 7); ctx.lineTo(x, y); } ctx.stroke(); }
  ctx.restore(); }
const HSIL = document.createElement('canvas'), HSG = HSIL.getContext('2d');
function auraBack(SA, key, f, row, x0, y0, sc, time) { // derrière le héros : halo, lumière au sol, cercle runique (ultimes), aura qui scintille
  const F = AFX[SA.fx] || AFX.violet, h = B.hero, ult = (EVO[key] || {}).st === 3, hit = Math.max(0, 1 - (B.t - (h.shotAt || -9)) / 0.35), fl = flick(time, 0);
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  glow(CX - 4, YF - 48, 70 + 8 * fl + 30 * hit, `rgba(${F.glow},1)`, 0.12 + 0.12 * fl + 0.3 * hit);
  ctx.save(); ctx.translate(CX - 2, YF + 2); ctx.scale(1, 0.26); glow(0, 0, 62 + 10 * fl, `rgba(${F.glow},1)`, 0.25 + 0.15 * fl + 0.3 * hit);
  if (ult) { ctx.rotate(time * 0.6); ctx.strokeStyle = `rgba(${F.glow},${0.45 + 0.2 * fl})`; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.arc(0, 0, 50, 0, TAU); ctx.stroke(); ctx.setLineDash([7, 9]); ctx.beginPath(); ctx.arc(0, 0, 41, 0, TAU); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = `rgba(${F.glow},${0.6 + 0.3 * fl})`; for (let i = 0; i < 8; i++) { const a = i * TAU / 8; ctx.fillRect(Math.cos(a) * 50 - 2.5, Math.sin(a) * 50 - 2.5, 5, 5); } }
  ctx.restore(); ctx.restore();
  if (!auraCell(SA, key, f, row)) return; ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.globalAlpha = 0.78 + 0.22 * fl; ctx.drawImage(AUC, x0, y0, SA.cw * sc, SA.ch * sc); ctx.restore(); }
function auraFront(SA, key, f, row, x0, y0, sc, time, dt) { // devant : lueur de l'aura, contour pulsé (ultimes), flammèches, embrasement à l'attaque
  const F = AFX[SA.fx] || AFX.violet, h = B.hero, ult = (EVO[key] || {}).st === 3, hit = Math.max(0, 1 - (B.t - (h.shotAt || -9)) / 0.35), fl = flick(time, 1.7);
  if (ult) { const im = SIDEI[key]; if (HSIL.width !== SA.cw || HSIL.height !== SA.ch) { HSIL.width = SA.cw; HSIL.height = SA.ch; }
    const sx0 = f * SA.cw, sy0 = row * SA.ch, o2 = Math.max(2, Math.round(1.6 / sc)); HSG.clearRect(0, 0, SA.cw, SA.ch); HSG.globalCompositeOperation = 'source-over'; // liseré : silhouette décalée moins la silhouette
    for (const [dx, dy] of [[-o2, 0], [o2, 0], [0, -o2], [0, o2]]) HSG.drawImage(im, sx0, sy0, SA.cw, SA.ch, dx, dy, SA.cw, SA.ch);
    HSG.globalCompositeOperation = 'destination-out'; HSG.drawImage(im, sx0, sy0, SA.cw, SA.ch, 0, 0, SA.cw, SA.ch); HSG.drawImage(AUC, 0, 0);
    HSG.globalCompositeOperation = 'source-in'; HSG.fillStyle = `rgb(${F.glow})`; HSG.fillRect(0, 0, SA.cw, SA.ch);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = Math.min(1, (0.45 + 0.4 * (0.5 + 0.5 * Math.sin(time * 3.2))) * (1 + hit)); ctx.imageSmoothingEnabled = true; ctx.drawImage(HSIL, x0, y0, SA.cw * sc, SA.ch * sc); ctx.restore(); }
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.06 + 0.12 * fl + 0.35 * hit; ctx.imageSmoothingEnabled = true; ctx.drawImage(AUC, x0, y0, SA.cw * sc, SA.ch * sc); ctx.restore();
  if (h.dead) return; const L = AUPTS[key + ':' + row + ':' + f]; if (!L || !L.length) return;
  let n = F.rate * dt * (B.walk ? 1.6 : 1); if (hit > 0.9 && !h.burst) { n += 12; h.burst = 1; } if (hit < 0.5) h.burst = 0;
  for (; n > 0; n--) { if (n < 1 && Math.random() > n) break; const q = L[Math.floor(Math.random() * L.length)];
    wisp(F, x0 + q[0] * sc, y0 + q[1] * sc, Math.random() < 0.5 ? q[2] : pick(F.p), hit > 0.9); } }""")

rep("  for (const f of B.fx) { f.t += dt; if (f.k === 'p') { f.x += f.vx * dt; f.y += f.vy * dt; f.vy += (f.g === undefined ? 260 : f.g) * dt; } }",
    "  for (const f of B.fx) { f.t += dt; if (f.k === 'p' || f.k === 'w') { f.x += f.vx * dt; f.y += f.vy * dt; f.vy += (f.g === undefined ? (f.k === 'w' ? 0 : 260) : f.g) * dt; } }")
rep("    if (f.k === 'g') { const A = ASSETS['fx_' + f.sh];", "    if (f.k === 'w') { drawWisp(f); continue; }\n    if (f.k === 'g') { const A = ASSETS['fx_' + f.sh];")
rep("    if (!im || !im.complete) return; ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, Math.round(CX - SA.ax * sc), Math.round(YF - SA.foot * sc + by), Math.round(SA.cw * sc), Math.round(SA.ch * sc)); ctx.restore(); return; }",
r"""    if (!im || !im.complete) return; const x0 = Math.round(CX - SA.ax * sc), y0 = Math.round(YF - SA.foot * sc + by), ka = curForm(), hasA = !!SIDEA[ka];
    if (hasA) auraBack(SA, ka, f, row, x0, y0, sc, time);
    ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im, f * SA.cw, row * SA.ch, SA.cw, SA.ch, x0, y0, Math.round(SA.cw * sc), Math.round(SA.ch * sc)); ctx.restore();
    if (hasA) { const now = performance.now(), dt2 = Math.min(0.05, (now - (B.auT || now)) / 1000); B.auT = now; auraFront(SA, ka, f, row, x0, y0, sc, time, dt2); } return; }""")
s = s.replace('<style id="sv">', '<style id="sv">/* p08 auras */', 1)
open(P, 'w').write(s); print('p08 auras ok')
