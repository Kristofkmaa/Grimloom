P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v2.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

def cut(a_mark, b_mark, new, b_incl=True):
    global s
    a = s.index(a_mark); b = s.index(b_mark, a) + (len(b_mark) if b_incl else 0)
    s = s[:a] + new + s[b:]

# ---------- biomes, scènes, sol défilant ----------
cut("function buildFloor()", "  FLOOR = c;\n}\n", r'''// ================= biomes =================
// Chaque chapitre = un biome : tuiles de sol, murs, couleur de lumière et de flamme. Le chapitre 5 reprend le premier, etc.
const BIOMES = [
  { n: 'Les Catacombes', floor: [[736, 320], [784, 320], [736, 368], [784, 368], [736, 272]], dirt: [736, 416], flag: [[736, 208], [784, 208]], seg: [[80, 272, 64], [176, 272, 64], [272, 208, 80], [368, 208, 64]], awall: 192, mul: 'rgb(255,250,245)', tint: 'rgb(255,205,205)', light: 'rgba(255,140,50,1)', hue: 0, dark: 0.62, rune: '#ff3040' },
  { n: 'L\'Ossuaire moussu', floor: [[928, 368], [976, 368], [928, 320], [976, 320], [928, 272]], dirt: [928, 416], flag: [[928, 208], [976, 208]], seg: [[304, 336, 64], [384, 336, 64], [304, 400, 64], [384, 400, 64]], awall: 336, mul: 'rgb(220,240,205)', tint: 'rgb(215,245,200)', light: 'rgba(150,255,100,1)', hue: 80, dark: 0.64, rune: '#7aff5a', spores: 1 },
  { n: 'La Crypte noyée', floor: [[832, 320], [880, 320], [832, 272], [880, 272], [832, 368]], dirt: [832, 416], flag: [[832, 208], [880, 208]], seg: [[80, 496, 64], [176, 496, 64], [368, 208, 64]], awall: 416, mul: 'rgb(195,215,255)', tint: 'rgb(190,215,255)', light: 'rgba(90,170,255,1)', hue: 190, dark: 0.66, rune: '#5ab0ff', drip: 1 },
  { n: 'La Fournaise', floor: [[784, 368], [736, 368], [784, 272], [784, 320]], dirt: [736, 416], flag: [[736, 208], [784, 208]], seg: [[304, 400, 64], [384, 400, 64], [272, 208, 80]], awall: 192, mul: 'rgb(255,185,160)', tint: 'rgb(255,180,150)', light: 'rgba(255,90,30,1)', hue: -18, dark: 0.58, rune: '#ffa020', embers: 1 },
];
const SEG = 1.4; // longueur d'un tronçon de couloir : on avance exactement de ça entre deux vagues
const biome = () => BIOMES[(S.c - 1) % BIOMES.length];
const sceneFor = () => S.s === 10 && !S.farm ? 'arena' : 'corridor';
const TEXC = {};
function sceneTex(scene, bi) {
  const key = scene + BIOMES.indexOf(bi); if (TEXC[key]) return TEXC[key];
  const tex = document.createElement('canvas'); tex.width = tex.height = 512; const tg = tex.getContext('2d'); tg.imageSmoothingEnabled = false;
  let seed = 7 + BIOMES.indexOf(bi) * 31; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  if (scene === 'arena') {
    for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) { const f = bi.flag[(x + y) & 1]; tg.drawImage(IMG.tiles, f[0], f[1], 32, 32, x * 32, y * 32, 32, 32); }
    // cercle d'invocation peint au sol (devient une ellipse une fois projeté)
    const cx = 256, cy = 150; tg.save(); tg.translate(cx, cy); tg.scale(1, 1.55); tg.strokeStyle = bi.rune; tg.globalAlpha = 0.55; tg.lineWidth = 4;
    for (const r of [92, 74]) { tg.beginPath(); tg.arc(0, 0, r, 0, TAU); tg.stroke(); }
    tg.lineWidth = 3; tg.beginPath(); for (let i = 0; i <= 5; i++) { const a = -Math.PI / 2 + i * TAU * 2 / 5; tg[i ? 'lineTo' : 'moveTo'](Math.cos(a) * 74, Math.sin(a) * 74); } tg.stroke();
    tg.fillStyle = bi.rune; for (let i = 0; i < 12; i++) { const a = i * TAU / 12; tg.fillRect(Math.cos(a) * 83 - 2, Math.sin(a) * 83 - 2, 4, 4); }
    tg.restore();
  } else {
    for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) { const f = bi.floor[rnd() < 0.6 ? 0 : Math.floor(rnd() * bi.floor.length)]; tg.drawImage(IMG.tiles, f[0], f[1], 32, 32, x * 32, y * 32, 32, 32); }
    for (let i = 0; i < 6; i++) { tg.globalAlpha = 0.7; tg.drawImage(IMG.tiles, bi.dirt[0], bi.dirt[1], 64, 64, Math.floor(rnd() * 7) * 64 + 32, Math.floor(rnd() * 8) * 64, 64, 64); } tg.globalAlpha = 1;
  }
  let wt;
  if (scene === 'arena') { wt = document.createElement('canvas'); wt.width = 408; wt.height = 78; const wg = wt.getContext('2d'); for (let i = 0; i < 2; i++) wg.drawImage(IMG.tiles, 58, bi.awall, 204, 78, i * 204, 0, 204, 78); }
  else { const list = [...bi.seg, ...bi.seg]; wt = document.createElement('canvas'); wt.width = list.reduce((a, q) => a + q[2] + 16, 0); wt.height = 48; const wg = wt.getContext('2d'); let x = 0; for (const q of list) { wg.drawImage(IMG.tiles, ...TL.pillar, x, 0, 16, 48); wg.drawImage(IMG.tiles, q[0], q[1], q[2], 48, x + 16, 0, q[2], 48); x += q[2] + 16; } }
  return TEXC[key] = { tex, wt };
}
const FC = document.createElement('canvas'); FC.width = BW * 2; FC.height = BH * 2;
let FKEY = '';
function renderFloor(scene, bi, scroll) { // sol et murs projetés, avec défilement quand le héros avance
  const key = scene + BIOMES.indexOf(bi) + ':' + scroll.toFixed(3); if (key === FKEY) return; FKEY = key;
  const { tex, wt } = sceneTex(scene, bi), g = FC.getContext('2d'); g.setTransform(2, 0, 0, 2, 0, 0); g.imageSmoothingEnabled = false; g.globalCompositeOperation = 'source-over';
  g.fillStyle = '#060304'; g.fillRect(0, 0, BW, BH);
  for (let y = YH; y < BH; y++) { const q = (y - YH) / (YF - YH), s = S1 + q * (1 - S1), z = (1 / s - 1) / K, hw = HW * s; const X0 = -CX / hw, X1 = (BW - CX) / hw; const u0 = 256 + X0 * 128, u1 = 256 + X1 * 128, v = (((z + scroll) * 300) % 512 + 512) % 512;
    if (u0 >= 0 && u1 <= 512) g.drawImage(tex, u0, v, u1 - u0, 1, 0, y, BW, 1); else g.drawImage(tex, 0, v, 512, 1, CX + (-256 / 128) * hw, y, 512 / 128 * hw, 1);
    const lx = sx(-1, z), rx = sx(1, z); g.fillStyle = '#060304'; if (lx > 0) g.fillRect(0, y, lx, 1); if (rx < BW) g.fillRect(rx, y, BW - rx, 1); }
  for (let x = 0; x < BW; x++) { const hw = Math.abs(x - CX), s = hw / HW; if (s < S1 || s > 1.25) continue; const z = (1 / s - 1) / K, base = py(z), top = base - WALLH * s, u = (((z + scroll) * 220) % wt.width + wt.width) % wt.width;
    g.drawImage(wt, u, 0, 1, wt.height, x, top, 1, base - top); g.fillStyle = `rgba(0,0,0,${0.25 + (1 - s) * 0.5})`; g.fillRect(x, top, 1, base - top); }
  const bl = sx(-1, 1), br = sx(1, 1), bh = WALLH * S1;
  if (scene === 'arena') { // salle close : mur du fond et grande porte du boss
    const w = 204 * (bh / 78); for (let x = bl - w * 0.3; x < br; x += w) g.drawImage(IMG.tiles, 58, bi.awall, 204, 78, x, YH - bh, w, bh);
    g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(bl, YH - bh, br - bl, bh);
    const gh = bh * 1.02, gw = gh * 64 / 105; g.drawImage(IMG.tiles, 880, 0, 64, 105, CX - gw / 2, YH - gh, gw, gh);
  } else { // couloir sans fin : les portes latérales défilent avec les murs
    for (let k = -1; k < 2; k++) { const dz = 0.55 - scroll + Math.round(scroll / SEG) * SEG + k * SEG; if (dz < 0.12 || dz > 0.98) continue;
      for (const side of [-1, 1]) { const z0 = dz + 0.07, z1 = dz - 0.07, x0 = sx(side, z0), x1 = sx(side, z1), b0 = py(z0), b1 = py(z1), h0 = WALLH * sOf(z0) * 0.7, h1 = WALLH * sOf(z1) * 0.7; g.fillStyle = '#020102'; g.beginPath(); g.moveTo(x0, b0); g.lineTo(x0, b0 - h0); g.lineTo(x1, b1 - h1); g.lineTo(x1, b1); g.fill(); } }
  }
  g.globalCompositeOperation = 'multiply'; g.fillStyle = bi.mul; g.fillRect(0, 0, BW, BH); g.globalCompositeOperation = 'source-over';
  const gr = g.createLinearGradient(0, YH - 70, 0, YH + (scene === 'arena' ? 90 : 150)); gr.addColorStop(0, 'rgba(0,0,0,.95)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, BW, YH + 150);
  FLOOR = FC;
}
''')

cut("const DECO = [", "\n", r'''// décor : position monde (wz) dans un tronçon, il défile quand on avance
const DECO_C = [{ k: 'torch', X: -0.96, wz: 0.3 }, { k: 'torch', X: 0.96, wz: 0.3 }, { k: 'torch', X: -0.96, wz: 1.0 }, { k: 'torch', X: 0.96, wz: 1.0 }, { k: 'brazier', X: -0.78, wz: 0.82 }, { k: 'brazier', X: 0.78, wz: 1.22 }, { k: 'urn', X: -0.88, wz: 0.15, v: 0 }, { k: 'urn', X: 0.9, wz: 0.75, v: 2 }, { k: 'urn', X: -0.9, wz: 1.12, v: 1 }, { k: 'post', X: 0.86, wz: 0.05, v: 1 }, { k: 'skull', X: -0.4, wz: 0.85 }, { k: 'skull', X: 0.5, wz: 0.4 }, { k: 'skull', X: 0.2, wz: 1.3 }];
const DECO_A = [{ k: 'brazier', X: -0.3, z: 0.97 }, { k: 'brazier', X: 0.3, z: 0.97 }, { k: 'brazier', X: -0.84, z: 0.62 }, { k: 'brazier', X: 0.84, z: 0.62 }, { k: 'pillar', X: -0.93, z: 0.9 }, { k: 'pillar', X: 0.93, z: 0.9 }, { k: 'pillar', X: -0.93, z: 0.32 }, { k: 'pillar', X: 0.93, z: 0.32 }, { k: 'torch', X: -0.97, z: 0.08 }, { k: 'torch', X: 0.97, z: 0.08 }, { k: 'skull', X: -0.55, z: 0.2 }, { k: 'skull', X: 0.6, z: 0.75 }, { k: 'urn', X: -0.8, z: 0.05, v: 2 }];
for (let i = 0; i < 6; i++) { const a = i * TAU / 6 + 0.5; DECO_A.push({ k: 'candle', X: Math.cos(a) * 0.5, z: 0.5 + Math.sin(a) * 0.17 }); }
let DECO = DECO_C;
function placeDeco() { DECO = B.scene === 'arena' ? DECO_A : DECO_C; if (DECO === DECO_C) for (const d of DECO) d.z = ((d.wz - B.scroll + 0.15) % SEG + SEG) % SEG - 0.15; }
''')

rep("const B = { en: [], shots: [], es: [], fx: [], nums: [], hero: { hp: 1, hpMax: 1, cd: 0, shootT: 0, hurt: 0, dead: 0 }, wave: null, t: 0, shake: 0, banner: null };",
    "const B = { en: [], shots: [], es: [], fx: [], nums: [], hero: { hp: 1, hpMax: 1, cd: 0, shootT: 0, hurt: 0, dead: 0 }, wave: null, t: 0, shake: 0, banner: null, scene: 'corridor', scroll: 0, walk: null, fade: 1, pend: 0, pendFn: null };")

# ---------- enchaînement : vague -> marche -> vague / arène / nouveau biome ----------
rep("""function startWave() {
  const n = stageIndex(),""", """function startWave() {
  const sc = sceneFor(), prev = B.scene; if (sc !== prev) { B.scene = sc; B.scroll = 0; B.fade = 1; }
  if (sc === 'corridor' && (prev === 'arena' || !B.started) && S.s === 1 && !S.farm) B.banner = { a: `Chapitre ${S.c}`, b: biome().n, t: 2.4 };
  B.started = 1; placeDeco();
  const n = stageIndex(),""")
rep("spawnEnemy(img, 0, 0.82, st, true);", "spawnEnemy(img, 0, 0.93, st, true);")
rep("S.best = Math.max(S.best, stageIndex()); save(); setTimeout(startWave, 900);", "S.best = Math.max(S.best, stageIndex()); save(); B.pend = 0.9; B.pendFn = beginWalk;")
rep("save(); setTimeout(startWave, 1200);", "save(); B.pend = 0.3; B.pendFn = () => { B.fade = 1; B.scroll = 0; startWave(); };")
rep("// ================= effets =================", """function beginWalk() { // le héros avance vers le fond : couloir suivant, ou porte de l'arène
  const change = sceneFor() !== B.scene;
  B.walk = { t: 0, dur: change ? 2.0 : 1.5, d0: B.scroll, dist: SEG, change };
  B.wave = null; uiWave();
}
// ================= effets =================""")

rep("""  B.t += dt; B.shake = Math.max(0, B.shake - dt * 30); if (B.banner) { B.banner.t -= dt; if (B.banner.t <= 0) B.banner = null; }""",
"""  B.t += dt; B.shake = Math.max(0, B.shake - dt * 30); if (B.banner) { B.banner.t -= dt; if (B.banner.t <= 0) B.banner = null; }
  if (B.pend > 0) { B.pend -= dt; if (B.pend <= 0 && B.pendFn) { const f = B.pendFn; B.pendFn = null; f(); } }
  if (B.walk) {
    const w = B.walk; w.t += dt; const q = Math.min(1, w.t / w.dur), e = q < 0.5 ? 2 * q * q : 1 - Math.pow(-2 * q + 2, 2) / 2, ns = w.d0 + w.dist * e, ds = ns - B.scroll; B.scroll = ns;
    for (const en of B.en) en.z -= ds; // les cadavres restent au sol
    if (w.change) B.fade = clamp((w.t - (w.dur - 0.6)) / 0.6, 0, 1);
    if (q >= 1) { B.walk = null; B.scroll = w.change ? 0 : Math.round(B.scroll / SEG) * SEG % (SEG * 1000); startWave(); }
  } else if (B.fade > 0) B.fade = Math.max(0, B.fade - dt * 1.5);
  if (B.scene === 'corridor') placeDeco();
  const bi = biome();
  if ((bi.embers || bi.spores || bi.drip) && Math.random() < dt * (bi.drip ? 6 : 10)) { const X = rand(-1, 1), z = rand(0, 1); B.fx.push(bi.drip ? { k: 'p', x: sx(X, z), y: py(z) - WALLH * sOf(z) * rand(0.5, 1), vx: 0, vy: 30, g: 300, c: '#9ad0ff', t: 0, d: 0.6, r: 0.8 } : { k: 'p', x: sx(X, z), y: py(z) - rand(0, 30), vx: rand(-8, 8), vy: rand(-30, -12), g: bi.embers ? -8 : -2, c: bi.embers ? pick(['#ffb040', '#ff6020', '#ffe080']) : pick(['#b0ff80', '#70d060']), t: 0, d: rand(1.2, 2.2), r: rand(0.6, 1.2) }); }""")
rep("f.vy += 260 * dt;", "f.vy += (f.g === undefined ? 260 : f.g) * dt;")
# pas de tir ni de spawn pendant la marche
rep("    if (h.cd <= 0 && B.en.some(", "    if (!B.walk && h.cd <= 0 && B.en.some(")

# ---------- dessin ----------
rep("  if (!FLOOR) { if (IMG.tiles.complete) buildFloor(); else return; }", "  if (!IMG.tiles.complete) return; renderFloor(B.scene, biome(), B.scroll);")
rep("  for (const d of DECO) L.push({ z: d.z, f: () => drawDeco(d, time) });", "  for (const d of DECO) if (d.z > -0.12 && d.z < 1.06) L.push({ z: d.z, f: () => drawDeco(d, time) });\n  if (B.scene === 'arena') { ctx.globalCompositeOperation = 'lighter'; glow(CX, py(0.5), 110, biome().light, 0.12 + Math.sin(time * 2.5) * 0.05); ctx.globalCompositeOperation = 'source-over'; }")
rep("  if (B.hero.dead) { ctx.fillStyle = `rgba(80,0,10,${Math.min(0.5, B.hero.deadT * 0.4)})`; ctx.fillRect(0, 0, BW, BH); }\n}",
    "  if (B.hero.dead) { ctx.fillStyle = `rgba(80,0,10,${Math.min(0.5, B.hero.deadT * 0.4)})`; ctx.fillRect(0, 0, BW, BH); }\n  if (B.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${B.fade})`; ctx.fillRect(-10, -60, BW + 20, BH + 120); }\n}")
# le bandeau passe par-dessus le fondu
a = s.index("  if (B.banner) { const a = Math.min(1, B.banner.t * 2);"); b = s.index("\n", a)
banner = s[a:b]; s = s[:a] + s[b + 1:]
rep("  if (B.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${B.fade})`; ctx.fillRect(-10, -60, BW + 20, BH + 120); }\n}", "  if (B.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${B.fade})`; ctx.fillRect(-10, -60, BW + 20, BH + 120); }\n" + banner + "\n}")

# lumière teintée par biome
rep("g.fillStyle = 'rgba(10,2,8,.62)';", "g.fillStyle = `rgba(10,2,8,${biome().dark})`;")
rep("for (const d of DECO) if (d.k === 'brazier' || d.k === 'torch') hole(", "for (const d of DECO) if ((d.k === 'brazier' || d.k === 'torch' || d.k === 'candle') && d.z > -0.12 && d.z < 1.06) hole(")
rep("ctx.fillStyle = 'rgb(255,205,205)'; ctx.fillRect(0, 0, BW, BH);", "ctx.fillStyle = biome().tint; ctx.fillRect(0, 0, BW, BH);")

# flammes à la couleur du biome + nouveaux décors
rep("function drawDeco(d, time) {\n  const x = sx(d.X, d.z), y = py(d.z), s = sOf(d.z) * 2.2;",
    "function drawDeco(d, time) {\n  const x = sx(d.X, d.z), y = py(d.z), s = sOf(d.z) * 2.2, bi = biome(); if (bi.hue) ctx.filter = `hue-rotate(${bi.hue}deg) saturate(1.3)`;\n  if (d.k === 'pillar') { ctx.drawImage(IMG.tiles, ...TL.pillar, x - 8 * s, y - 64 * s, 16 * s, 64 * s); ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.fillRect(x - 8 * s, y - 64 * s, 16 * s, 64 * s); }\n  else if (d.k === 'candle') { const A = ASSETS.anim.list.candleA, f = Math.floor(time * 8 + d.X * 7) % A.n; ctx.drawImage(IMG.anim, A.x + f * 16, 0, 16, 16, x - 5 * s, y - 11 * s, 10 * s, 10 * s); ctx.globalCompositeOperation = 'lighter'; glow(x, y - 8 * s, 14 * s, bi.light, 0.5); ctx.globalCompositeOperation = 'source-over'; }\n  else")
rep("  else if (d.k === 'skull') {", "  else if (d.k === 'skull') { ctx.filter = 'none';")
s = s.replace("'rgba(255,140,50,1)', 0.6", "bi.light, 0.6")
a = s.index("function drawDeco(d, time) {"); b = s.index("\n}\n", a)
s = s[:b] + "\n  ctx.filter = 'none';" + s[b:]

# héros qui court pendant la marche
rep("if (h.dead) { anim = 'mort'; fr = Math.min(14, h.deadT * 12); }", "if (B.walk) { anim = 'course'; fr = time * 16; } else if (h.dead) { anim = 'mort'; fr = Math.min(14, h.deadT * 12); }")

# barre de vague pendant la marche
rep("const w = B.wave; if (!w) return;", "const w = B.wave; if (!w) { $('waveTxt').textContent = sceneFor() === 'arena' ? 'Vers l\\'arène du boss…' : B.scene === 'arena' ? 'Vers un nouveau biome…' : 'En avant…'; $('waveBar').style.width = '0%'; $('waveBox').classList.remove('boss'); return; }")

open(P, 'w').write(s)
print('ok')
s = open(P).read()
rep("if (B.wave.boss) { S.farm = true;", "if (B.wave && B.wave.boss) { S.farm = true;")
rep("const st = heroStats(); if (B.hero.dead) return;", "const st = heroStats(); if (B.hero.dead || B.walk) return;")
rep("$('bossBtn').onclick = () => { S.farm = false; S.s = 10; save(); startWave(); };", "$('bossBtn').onclick = () => { if (B.walk) return; S.farm = false; S.s = 10; save(); B.en = []; B.es = []; beginWalk(); };")
open(P, 'w').write(s)
print('ok2')
