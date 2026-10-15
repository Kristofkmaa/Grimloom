P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v14.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# ---------- 3 nouveaux biomes + mobs propres à chaque biome ----------
rep("""  { n: 'La Fournaise', floor: [[784, 368], [736, 368], [784, 272], [784, 320]], dirt: [736, 416], flag: [[736, 208], [784, 208]], seg: [[304, 400, 64], [384, 400, 64], [272, 208, 80]], awall: 192, mul: 'rgb(255,185,160)', tint: 'rgb(255,180,150)', light: 'rgba(255,90,30,1)', hue: -18, dark: 0.58, rune: '#ffa020', embers: 1 },
];""", """  { n: 'La Fournaise', floor: [[784, 368], [736, 368], [784, 272], [784, 320]], dirt: [736, 416], flag: [[736, 208], [784, 208]], seg: [[304, 400, 64], [384, 400, 64], [272, 208, 80]], awall: 192, mul: 'rgb(255,185,160)', tint: 'rgb(255,180,150)', light: 'rgba(255,90,30,1)', hue: -18, dark: 0.58, rune: '#ffa020', embers: 1 },
  { n: 'Le Marais putride', floor: [[976, 368], [928, 368], [976, 320], [928, 320], [928, 272]], dirt: [928, 416], flag: [[928, 208], [976, 208]], seg: [[384, 336, 64], [304, 336, 64], [384, 400, 64]], awall: 336, mul: 'rgb(205,230,140)', tint: 'rgb(215,240,150)', light: 'rgba(170,255,40,1)', hue: 62, dark: 0.6, rune: '#b8ff30', toxic: 1 },
  { n: 'L\\'Abîme gelé', floor: [[880, 320], [832, 320], [880, 272], [832, 272], [832, 368]], dirt: [832, 416], flag: [[832, 208], [880, 208]], seg: [[176, 496, 64], [80, 496, 64], [368, 208, 64]], awall: 416, mul: 'rgb(232,246,255)', tint: 'rgb(222,240,255)', light: 'rgba(170,230,255,1)', hue: 175, dark: 0.5, rune: '#bff4ff', snow: 1 },
  { n: 'Le Néant', floor: [[784, 320], [736, 320], [784, 368], [736, 368], [736, 272]], dirt: [736, 416], flag: [[784, 208], [736, 208]], seg: [[176, 272, 64], [80, 272, 64], [368, 208, 64], [272, 208, 80]], awall: 192, mul: 'rgb(210,190,245)', tint: 'rgb(205,185,255)', light: 'rgba(170,90,255,1)', hue: 245, dark: 0.6, rune: '#c070ff', motes: 1 },
];
// mobs de chaque biome : v = variante de couleur (recoloration des démons), pool = démons de base, elites, boss (alterne à chaque tour du monde)
const BMOBS = [
  { v: null, tip: '', pool: ['imp1', 'imp2', 'imp4', 'imp5', 'imp7', 'imp9', 'imp10', 'spawn2', 'spawn5'], elites: ['elite1', 'elite6'], boss: [['p_idle', 'Le Démon écarlate'], ['beast4', 'La Bête ailée']] },
  { v: 'bone', tip: 'Démons d\\'os : +25 % de PV', pool: ['spawn10', 'spawn11', 'spawn12', 'spawn7', 'imp3', 'imp8', 'spawn5'], elites: ['elite5', 'elite3'], boss: [['beast3', 'L\\'Arachnide d\\'os'], ['beast1', 'Le Colosse d\\'os']] },
  { v: 'drown', tip: 'Démons noyés : lents mais coriaces', pool: ['spawn3', 'spawn4', 'spawn9', 'imp6', 'imp2', 'spawn13', 'spawn8'], elites: ['elite2', 'elite4'], boss: [['beast5', 'La Wyverne des abysses'], ['beast2', 'La Bête noyée']] },
  { v: 'fire', tip: 'Démons de braise : frappent plus fort', pool: ['imp1', 'imp10', 'spawn1', 'spawn2', 'spawn6', 'spawn5', 'imp7'], elites: ['elite1', 'elite3'], boss: [['beast2', 'La Bête ardente'], ['p_idle', 'Le Seigneur des braises']] },
  { v: 'poison', tip: 'Démons putrides : leurs coups empoisonnent', pool: ['imp3', 'imp5', 'imp8', 'spawn9', 'spawn12', 'spawn13', 'spawn6'], elites: ['elite2', 'elite6'], boss: [['beast1', 'La Bête putride'], ['beast3', 'L\\'Arachnide venimeuse']] },
  { v: 'ice', tip: 'Démons de givre : leurs coups te ralentissent', pool: ['spawn4', 'spawn7', 'spawn8', 'spawn10', 'spawn11', 'imp4', 'imp9'], elites: ['elite5', 'elite4'], boss: [['beast4', 'La Bête ailée du givre'], ['beast5', 'La Wyverne de glace']] },
  { v: 'void', tip: 'Démons du Néant : esquivent 15 % des coups', pool: ['spawn3', 'spawn8', 'spawn11', 'spawn1', 'imp6', 'imp10', 'spawn12'], elites: ['elite3', 'elite6'], boss: [['p_idle', 'Le Démon du Néant'], ['beast3', 'La Tisseuse du Néant']] },
];
const bossOf = ch => { const bi = (ch - 1) % BIOMES.length, L = BMOBS[bi].boss[Math.floor((ch - 1) / BIOMES.length) % 2]; return { key: L[0], n: L[1], v: BMOBS[bi].v, bi }; };
// ---------- recoloration des démons (faite une fois par feuille, en tâche de fond) ----------
const VARS = { bone: [45, 0.35, 1.15], drown: [170, 0.75, 1.0], fire: [28, 1.1, 1.15], poison: [95, 0.95, 1.05], ice: [195, 0.55, 1.35], void: [280, 0.85, 1.0] };
const VCOL = { bone: '#e8dcb0', drown: '#50e0c8', fire: '#ffa030', poison: '#9aff3a', ice: '#c8f0ff', void: '#c070ff' };
const DV = {}, DVQ = [];
function demImg(key, v) { const im = IMG['D_' + key]; if (!v || !VARS[v]) return im; const k = key + '@' + v; if (DV[k]) return DV[k]; if (DVQ.indexOf(k) < 0) DVQ.push(k); return im; }
function recolorStep() {
  const k = DVQ.shift(); if (!k || DV[k]) return; const [key, v] = k.split('@'), im = IMG['D_' + key]; if (!im || !im.complete) { DVQ.push(k); return; }
  const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0);
  const id = g.getImageData(0, 0, c.width, c.height), d = id.data, [h0, sm, lm] = VARS[v];
  for (let i = 0; i < d.length; i += 4) {
    if (!d[i + 3]) continue; const r = d[i] / 255, gg = d[i + 1] / 255, b = d[i + 2] / 255, mx = Math.max(r, gg, b), mn = Math.min(r, gg, b), dl = mx - mn; if (dl <= 0) continue;
    const l = (mx + mn) / 2, sat = dl / (1 - Math.abs(2 * l - 1) + 1e-6); if (sat <= 0.18) continue;
    let h = mx === r ? ((gg - b) / dl) % 6 : mx === gg ? (b - r) / dl + 2 : (r - gg) / dl + 4; h *= 60; const dh = ((h + 540) % 360) - 180; if (Math.abs(dh) >= 50) continue;
    const nh = ((h0 + dh * 0.6) % 360 + 360) % 360, ns = Math.min(1, sat * sm), nl = Math.min(1, l * lm), C = (1 - Math.abs(2 * nl - 1)) * ns, X = C * (1 - Math.abs((nh / 60) % 2 - 1)), m = nl - C / 2, q = Math.floor(nh / 60);
    const [R, G, Bq] = q === 0 ? [C, X, 0] : q === 1 ? [X, C, 0] : q === 2 ? [0, C, X] : q === 3 ? [0, X, C] : q === 4 ? [X, 0, C] : [C, 0, X];
    d[i] = (R + m) * 255; d[i + 1] = (G + m) * 255; d[i + 2] = (Bq + m) * 255;
  }
  g.putImageData(id, 0, 0); DV[k] = c;
}
function queueBiome(bi) { const M = BMOBS[bi % BMOBS.length]; if (!M.v) return; for (const key of [...M.pool, ...M.elites, ...M.boss.map(b => b[0] === 'p_idle' ? 'spawn1' : b[0])]) demImg(key, M.v); }""")

# pool / élites / boss pris dans le biome
rep("const POOL = [['imp1', 'imp2', 'imp4', 'imp5', 'imp7', 'imp9', 'imp10'], ['imp1', 'imp2', 'imp5', 'imp9', 'spawn1', 'spawn2', 'spawn5', 'spawn9'], ['imp3', 'imp6', 'imp8', 'spawn1', 'spawn3', 'spawn4', 'spawn6', 'spawn8', 'spawn9', 'spawn12'], ['spawn3', 'spawn4', 'spawn6', 'spawn8', 'spawn10', 'spawn11', 'spawn12', 'spawn13', 'imp6', 'imp8']];\n", "const bmobs = () => BMOBS[(B.bi === undefined ? (PC() - 1) : B.bi) % BMOBS.length];\n")
rep("const BOSSES = ['p_idle', 'beast1', 'beast2', 'beast3', 'beast5', 'beast4'];\nconst BNAMES = ['Le Démon écarlate', 'La Bête ardente', 'L\\'Arachnide écarlate', 'La Bête pâle', 'La Wyverne', 'La Bête ailée'];\n", "")
rep("  if (sc === 'corridor' && (prev === 'arena' || !B.started) && S.s === 1 && !S.farm) B.banner = { a: `Chapitre ${S.c}`, b: biome().n, t: 2.4 };",
    "  if (sc === 'corridor' && (prev === 'arena' || !B.started) && S.s === 1 && !S.farm) { B.banner = { a: `Chapitre ${S.c}`, b: biome().n, t: 2.4 }; if (bmobs().tip) setTimeout(() => toast(bmobs().tip), 1800); }\n  queueBiome(B.bi); if (PS() >= 8) queueBiome(B.bi + 1);")
rep("const n = stageIndex(), boss = PS() === 10 && !S.farm, ch = PC(), pool = POOL[Math.min(POOL.length - 1, ch - 1)];", "const n = stageIndex(), boss = PS() === 10 && !S.farm, ch = PC();")
rep("  if (boss) { const img = BOSSES[(ch - 1) % BOSSES.length], st = enemyStats(n, true); spawnEnemy(img, 0, 0.93, st, true); B.banner = { a: 'Boss', b: ['Le Démon écarlate', 'La Bête ardente', 'L\\'Arachnide écarlate', 'La Bête pâle', 'La Wyverne', 'La Bête ailée'][(ch - 1) % 6], t: 2.2 }; }",
    "  if (boss) { const bo = bossOf(ch), st = enemyStats(n, true); spawnEnemy(bo.key, 0, 0.93, st, true); B.banner = { a: 'Boss', b: bo.n, t: 2.2 }; }")
rep("""function spawnEnemy(img, X, z, st, boss) {
  const ranged = !!RANGED[img], elite = /elite/.test(img), key = img === 'p_idle' ? 'spawn1' : img, D = ASSETS.DEM[key].anims;""",
"""function spawnEnemy(img, X, z, st, boss, v) {
  const ranged = !!RANGED[img], elite = /elite/.test(img), key = img === 'p_idle' ? 'spawn1' : img, D = ASSETS.DEM[key].anims;
  if (v === undefined) v = bmobs().v; const hpK = v === 'bone' ? 1.25 : v === 'drown' ? 1.15 : 1, atkK = v === 'fire' ? 1.18 : 1, spK = v === 'drown' ? 0.88 : 1; demImg(key, v);""")
rep("B.en.push({ img, X, z, hp: st.hp * (elite ? 4 : 1), max: st.hp * (elite ? 4 : 1), atk: st.atk * (elite ? 1.8 : 1), spd: (boss ? 0.15 : rand(0.13, 0.2)) * (/imp/.test(img) ? 1.3 : 1), ranged,",
    "B.en.push({ img, v, X, z, hp: st.hp * (elite ? 4 : 1) * hpK, max: st.hp * (elite ? 4 : 1) * hpK, atk: st.atk * (elite ? 1.8 : 1) * atkK, spd: (boss ? 0.15 : rand(0.13, 0.2)) * (/imp/.test(img) ? 1.3 : 1) * spK, ranged,")
rep("""  const pool = POOL[Math.min(POOL.length - 1, PC() - 1)], st = enemyStats(w.n, false), from = Math.random();
  let img = pick(pool); if (PC() >= 2 && Math.random() < 0.06) img = pick(['elite1', 'elite2', 'elite3', 'elite4', 'elite5', 'elite6']);""",
"""  const M = bmobs(), st = enemyStats(w.n, false), from = Math.random(), loop = Math.floor((PC() - 1) / BIOMES.length);
  let img = pick(M.pool); if ((PC() >= 2 || B.dun) && Math.random() < 0.06 + 0.02 * Math.min(5, loop)) img = pick(M.elites);""")

# dessin avec la bonne variante
rep("""  const A = ASSETS.DEM[key], im = IMG['D_' + key]; if (!A || !im.complete) return; o = o || {};
  const flip""", """  o = o || {}; const A = ASSETS.DEM[key], im = demImg(key, o.v); if (!A || !IMG['D_' + key].complete) return;
  const flip""")
rep("  const o = { alpha: al, loop };\n  if (e.boss || e.elite)", "  const o = { alpha: al, loop, v: e.v };\n  if (e.boss || e.elite)")
# halo du boss/élite à la couleur de la variante
rep("glow(x, y - A.bh * 0.5 * sc, 46 * sc, e.boss ? 'rgba(255,30,50,1)' : 'rgba(255,190,80,1)', 0.3 * al);",
    "glow(x, y - A.bh * 0.5 * sc, 46 * sc, e.v && e.boss ? VCOL[e.v] : e.boss ? 'rgba(255,30,50,1)' : 'rgba(255,190,80,1)', 0.3 * al);")

# effets des variantes : poison, givre, esquive du Néant
rep("""function hitEnemy(e, dmg, crit) {
  if (e.dead) return;""", """function hitEnemy(e, dmg, crit) {
  if (e.dead) return; if (e.v === 'void' && !e.boss && !B.oneshot && Math.random() < 0.15) { num(sx(e.X, e.z), py(e.z) - 50 * sOf(e.z), 'Esquive', '#d8a0ff', 1); return; }""")
rep("function hurtHero(d) {", "function hurtHero(d, v) {")
rep("B.hero.hp -= d; sfxPlay('hurt');", "B.hero.hp -= d; if (v === 'poison') { B.hero.psT = 3; B.hero.psD = Math.max(B.hero.psD && B.hero.psT > 0 ? B.hero.psD : 0, d * 0.15); } if (v === 'ice') B.hero.icT = 1.6; sfxPlay('hurt');")
rep("if (e.shoot) B.es.push({ X: e.X, z: e.z, h: 30, dmg: e.atk, t: 0, fx: e.boss ? 'pfeu' : pick(['pfeu', 'pmort', 'pglace']) }); else hurtHero(e.atk);",
    "if (e.shoot) B.es.push({ X: e.X, z: e.z, h: 30, dmg: e.atk, t: 0, v: e.v, fx: e.v === 'ice' ? 'pglace' : e.v === 'fire' ? 'pfeu' : e.v === 'void' || e.v === 'poison' ? 'pmort' : e.boss ? 'pfeu' : pick(['pfeu', 'pmort', 'pglace']) }); else hurtHero(e.atk, e.v);")
rep("if (d <= v) { s.dead = 1; hurtHero(s.dmg); }", "if (d <= v) { s.dead = 1; hurtHero(s.dmg, s.v); }")
rep("  if (B.frenzyT > 0) o.rate *= 2;", "  if (B.hero && B.hero.icT > 0) o.rate *= 0.75;\n  if (B.frenzyT > 0) o.rate *= 2;")
rep("    h.cd -= dt; h.shootT -= dt; h.hurt -= dt;", """    h.icT = (h.icT || 0) - dt;
    if (h.psT > 0 && !B.god) { h.psT -= dt; h.hp -= h.psD * dt; h.psN = (h.psN || 0) + h.psD * dt; if (h.psN >= Math.max(1, h.hpMax * 0.01)) { num(CX + rand(-16, 16), YF - 70, '-' + fmt(h.psN), '#9aff3a', 0.9); h.psN = 0; } if (Math.random() < dt * 8) B.fx.push({ k: 'p', x: CX + rand(-14, 14), y: YF - rand(10, 50), vx: 0, vy: -20, g: -10, c: '#9aff3a', t: 0, d: 0.7, r: 1.1 }); if (h.hp <= 0) { h.hp = 0; h.dead = 1; h.deadT = 0; if (!B.dun) B.banner = { a: 'Repli !', b: 'Le poison a eu raison du héros', t: 1.6 }; } }
    if (h.icT > 0 && Math.random() < dt * 8) B.fx.push({ k: 'p', x: CX + rand(-16, 16), y: YF - rand(10, 60), vx: 0, vy: 12, g: 0, c: '#c8f0ff', t: 0, d: 0.6, r: 1 });
    h.cd -= dt; h.shootT -= dt; h.hurt -= dt;""")
# petites particules autour des démons recolorés
rep("    e.cd -= dt; e.hitT -= dt;\n", "    e.cd -= dt; e.hitT -= dt; if (e.v && e.v !== 'bone' && Math.random() < dt * (e.boss ? 14 : 2.5)) B.fx.push({ k: 'p', x: sx(e.X, e.z) + rand(-10, 10) * sOf(e.z), y: py(e.z) - rand(10, 50) * sOf(e.z), vx: rand(-4, 4), vy: e.v === 'ice' || e.v === 'drown' ? 14 : -22, g: 0, c: VCOL[e.v], t: 0, d: 0.7, r: 1.1 * sOf(e.z) + 0.3 });\n")
rep("  const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0; B.hero.reported = 0; B.dmg = []; B.waveDmg = 0;\n  ui();\n}",
    "  const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0; B.hero.reported = 0; B.hero.psT = 0; B.hero.icT = 0; B.dmg = []; B.waveDmg = 0;\n  ui();\n}")

# particules d'ambiance des nouveaux biomes
rep("  const h = B.hero, st = heroStats();\n  if (h.dead)", """  if (bi.snow && Math.random() < dt * 18) B.fx.push({ k: 'p', x: rand(0, BW), y: rand(-20, YF - 80), vx: rand(-8, 4), vy: rand(12, 26), g: 0, c: Math.random() < 0.5 ? '#ffffff' : '#d8f4ff', t: 0, d: rand(1.6, 2.6), r: rand(0.6, 1.4) });
  if (bi.toxic && Math.random() < dt * 12) { const X = rand(-1, 1), z = rand(0, 1.2); B.fx.push({ k: 'p', x: sx(X, z), y: py(z) - rand(0, 6), vx: rand(-3, 3), vy: rand(-22, -10), g: -3, c: pick(['#b8ff30', '#7ad020', '#e0ff70']), t: 0, d: rand(1, 1.8), r: rand(0.8, 1.6) }); }
  if (bi.motes && Math.random() < dt * 10) { const X = rand(-1, 1), z = rand(0, 1.4); B.fx.push({ k: 'p', x: sx(X, z), y: py(z) - rand(0, 60), vx: rand(-10, 10), vy: rand(-14, -4), g: -2, c: pick(['#c070ff', '#8040ff', '#f0c0ff']), t: 0, d: rand(1.4, 2.4), r: rand(0.6, 1.3) }); }
  if (DVQ.length) recolorStep();
  const h = B.hero, st = heroStats();
  if (h.dead)""")

# donjon du givre dans l'abîme gelé
rep("givre: { n: 'Caveau Gelé', bi: 2 } };", "givre: { n: 'Caveau Gelé', bi: 5 } };")
rep("spawnEnemy(pick(['beast1', 'beast2', 'beast3', 'beast4', 'beast5']), 0, 0.93, st, true); }", "spawnEnemy(pick(['beast1', 'beast2', 'beast3', 'beast4', 'beast5']), 0, 0.93, st, true); }\n  queueBiome(B.bi);")

# carte du monde : boss et décor par biome
rep("function demOn(g, key, x, y, sc) { const A = ASSETS.DEM[key], im = IMG['D_' + key]; if (!A || !im.complete) return;",
    "function demOn(g, key, x, y, sc, v) { const A = ASSETS.DEM[key], im = demImg(key, v); if (!A || !IMG['D_' + key].complete) return;")
rep("g.strokeText(BNAMES[(k - 1) % BNAMES.length], x, y + R + 14); g.fillText(BNAMES[(k - 1) % BNAMES.length], x, y + R + 14); }",
    "g.strokeText(bossOf(k).n, x, y + R + 14); g.fillText(bossOf(k).n, x, y + R + 14); }")
rep("if (isB) { const bk = BOSSES[(k - 1) % BOSSES.length] === 'p_idle' ? 'spawn1' : BOSSES[(k - 1) % BOSSES.length];",
    "if (isB) { const bo = bossOf(k), bk = bo.key === 'p_idle' ? 'spawn1' : bo.key;")
rep("demOn(g, bk, x, y - R + 6, 1.25);", "demOn(g, bk, x, y - R + 6, 1.25, bo.v);")
rep("      else if (bi.spores) { g.fillStyle = 'rgba(90,170,70,.12)'; g.beginPath(); g.arc(x, y, 8 + r * 16, 0, TAU); g.fill(); }",
    """      else if (bi.spores) { g.fillStyle = 'rgba(90,170,70,.12)'; g.beginPath(); g.arc(x, y, 8 + r * 16, 0, TAU); g.fill(); }
      else if (bi.toxic) { g.fillStyle = 'rgba(150,230,40,.2)'; g.beginPath(); g.ellipse(x, y, 16 + r * 24, 6 + r * 7, 0, 0, TAU); g.fill(); g.fillStyle = 'rgba(220,255,120,.35)'; g.beginPath(); g.arc(x + 5, y - 1, 2, 0, TAU); g.fill(); }
      else if (bi.snow) { g.fillStyle = 'rgba(235,248,255,.22)'; g.beginPath(); g.ellipse(x, y, 20 + r * 26, 7 + r * 8, 0, 0, TAU); g.fill(); g.strokeStyle = 'rgba(190,240,255,.35)'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(x - 6, y); g.lineTo(x, y - 14 - r * 10); g.lineTo(x + 6, y); g.stroke(); }
      else if (bi.motes) { g.strokeStyle = 'rgba(190,110,255,.35)'; g.lineWidth = 1.5; g.beginPath(); g.ellipse(x, y, 12 + r * 14, 5 + r * 5, 0, 0, TAU); g.stroke(); g.fillStyle = 'rgba(200,130,255,.5)'; g.fillRect(x - 1, y - 1, 2, 2); }""")

# admin : sauter à un biome
rep('<button class="btn full" data-a="fail" type="button">Simuler une défaite</button></div>',
    '<button class="btn full" data-a="fail" type="button">Simuler une défaite</button></div>\n  <div class="lbl2">Aller au biome</div><div class="adm">${BIOMES.map((b, i) => `<button class="btn" type="button" data-bio="${i}" style="border-color:${b.rune};color:${b.rune}">${b.n.replace(/^(Le |La |L\\\')/, \'\')}</button>`).join(\'\')}</div>')
open(P, 'w').write(s)
print('ok')
s = open(P).read()
rep("  $('mbox').querySelectorAll('[data-set]').forEach(b => b.onclick = () => {", "  $('mbox').querySelectorAll('[data-bio]').forEach(b => b.onclick = () => { const i = +b.dataset.bio; S.c = i + 1 + Math.floor((S.c - 1) / BIOMES.length) * BIOMES.length; S.s = 1; S.farm = false; S.best = Math.max(S.best, stageIndex()); B.scene = 'x'; B.fade = 1; save(); startWave(); closeM(); toast(BIOMES[i].n); });\n  $('mbox').querySelectorAll('[data-set]').forEach(b => b.onclick = () => {")
open(P, 'w').write(s)
print('ok2')
