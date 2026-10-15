P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v11.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# =================== sauvegarde ===================
rep("if (!Array.isArray(S.bag)) S.bag = [];",
    """if (!Array.isArray(S.bag)) S.bag = [];
S.seals = Object.assign({ sang: 0, os: 0, braise: 0, givre: 0 }, S.seals || {}); S.dlv = Object.assign({ sang: 1, os: 1, braise: 1, givre: 1 }, S.dlv || {});
if (S.keys === undefined) S.keys = 3; if (S.pages === undefined) S.pages = 30; S.spells = S.spells || {}; S.slots = S.slots || [null, null, null];
function keyTick() { const d = new Date().toDateString(); if (S.keyDay !== d) { S.keyDay = d; S.keys = Math.max(S.keys, 3); } }""")
rep("function hamTick() {", "function hamTick() { keyTick();")

# =================== sets explosifs ===================
rep("""  sang: { n: 'Étreinte du Sang', c: '#ff3a5a', b: [[2, 'Vol de vie +5 %'], [4, 'Attaque +25 %'], [6, 'Chaque démon tué rend 5 % des PV · +35 % de dégâts aux élites et boss']] },
  os: { n: 'Garde de l\\'Ossuaire', c: '#e8dcc0', b: [[2, 'Points de vie +20 %'], [4, 'Défense +40 % · régénération +1 %/s'], [6, 'Dégâts subis −30 % · la défense augmente l\\'attaque']] },
  braise: { n: 'Furie des Braises', c: '#ff8a2a', b: [[2, 'Vitesse d\\'attaque +15 %'], [4, 'Tirs explosifs (40 % autour de la cible)'], [6, 'Toutes les 5 attaques : nova de feu à 300 % sur tous les démons']] },
  givre: { n: 'Murmure du Givre', c: '#7ad8ff', b: [[2, 'Critique +8 %'], [4, 'Les tirs ralentissent les démons'], [6, 'Dégâts critiques +100 % · +30 % de dégâts aux démons ralentis']] },""",
"""  sang: { n: 'Étreinte du Sang', c: '#ff3a5a', b: [[2, 'Vol de vie +8 %'], [4, 'Attaque +40 %'], [6, 'Chaque démon tué explose (200 % autour) · sous 30 % de PV : Frénésie, vitesse d\\'attaque ×2 pendant 5 s']] },
  os: { n: 'Garde de l\\'Ossuaire', c: '#e8dcc0', b: [[2, 'Points de vie +30 %'], [4, 'Bouclier d\\'os de 20 % des PV, rechargé toutes les 10 s'], [6, 'Toutes les 4 s, 5 lances d\\'os jaillissent (400 % chacune) · 50 % des dégâts subis renvoyés']] },
  braise: { n: 'Furie des Braises', c: '#ff8a2a', b: [[2, 'Vitesse d\\'attaque +25 %'], [4, 'Tirs explosifs (60 % autour de la cible)'], [6, 'Toutes les 4 attaques : pluie de météores (500 %) · les démons tués s\\'enflamment et propagent le feu']] },
  givre: { n: 'Murmure du Givre', c: '#7ad8ff', b: [[2, 'Critique +12 %'], [4, 'Tirs ralentissants · les critiques gèlent 1 s'], [6, 'Toutes les 6 s : blizzard qui gèle tout 2 s · démons gelés +100 % de dégâts, ils éclatent en mourant (300 %)']] },""")
rep("splash: !!H.splash, chill: !!H.chill, killHeal: 0, bigDmg: 0, dmgRed: 0, nova: false, slowBonus: 0 };",
    "splash: !!H.splash, splashK: 0.4, chill: !!H.chill, killHeal: 0, bigDmg: 0, dmgRed: 0, nova: false, slowBonus: 0, bloodBoom: false, frenzy: false, boneShield: false, spears: false, thorns: 0, meteor: false, ignite: false, critFreeze: false, blizzard: false, frozenBonus: 0, shatter: false };")
rep("""  if (has('sang', 2)) o.vol += 5; if (has('sang', 4)) o.atk *= 1.25; if (has('sang', 6)) { o.killHeal = 5; o.bigDmg = 0.35; }
  if (has('os', 2)) o.pv *= 1.2; if (has('os', 4)) { o.def *= 1.4; o.regen += 1; } if (has('os', 6)) { o.dmgRed = 0.3; o.atk += o.def * 0.8; }
  if (has('braise', 2)) o.rate *= 1.15; if (has('braise', 4)) o.splash = true; if (has('braise', 6)) o.nova = true;
  if (has('givre', 2)) o.crit += 8; if (has('givre', 4)) o.chill = true; if (has('givre', 6)) { o.cdmg += 100; o.slowBonus = 0.3; }""",
"""  if (has('sang', 2)) o.vol += 8; if (has('sang', 4)) o.atk *= 1.4; if (has('sang', 6)) { o.bloodBoom = true; o.frenzy = true; }
  if (has('os', 2)) o.pv *= 1.3; if (has('os', 4)) o.boneShield = true; if (has('os', 6)) { o.spears = true; o.thorns = 0.5; }
  if (has('braise', 2)) o.rate *= 1.25; if (has('braise', 4)) { o.splash = true; o.splashK = 0.6; } if (has('braise', 6)) { o.meteor = true; o.ignite = true; }
  if (has('givre', 2)) o.crit += 12; if (has('givre', 4)) { o.chill = true; o.critFreeze = true; } if (has('givre', 6)) { o.blizzard = true; o.frozenBonus = 1; o.shatter = true; }
  if (B.frenzyT > 0) o.rate *= 2; if (B.spFrT > 0) o.rate *= 1 + 0.6 * (B.spFrK || 1);""")
# la forge ne donne plus de sets
rep("  const set = r >= 2 && Math.random() < 0.3 + (r - 2) * 0.12 ? pick(SETK) : null;\n", "  const set = null; // les sets se gravent avec les Sceaux des donjons\n")

# =================== combat : effets des sets ===================
rep("if (st.nova && (B.shotN = (B.shotN || 0) + 1) % 5 === 0) novaFire(st);", "if (st.meteor && (B.shotN = (B.shotN || 0) + 1) % 4 === 0) meteorShower(st.atk * 5, 6);")
rep("splash: st.splash, chill: st.chill,", "splash: st.splash, splashK: st.splashK, chill: st.chill,")
rep("hitEnemy(o, s.dmg * 0.4)", "hitEnemy(o, s.dmg * (s.splashK || 0.4))")
rep("function novaFire(st) {", r"""const alive = () => B.en.filter(e => !e.dead && e.spawn <= 0);
const ex = e => sx(e.X, e.z), ey = e => py(e.z) - 24 * sOf(e.z);
function aoe(e0, rad, dmg, fx, col) { // dégâts autour d'un point (explosions en chaîne possibles)
  sfx(fx, ex(e0), ey(e0), 90 * sOf(e0.z), 0.45); burst(ex(e0), ey(e0), col, 14, 200);
  for (const o of alive()) if (o !== e0 && hyp((o.X - e0.X) * 1.4, o.z - e0.z) < rad) hitEnemy(o, dmg, false);
}
function meteorShower(dmg, n) { // set Braises (6) et sort Pluie de feu
  const L = alive(); B.shake = Math.max(B.shake, 4);
  for (let i = 0; i < n && L.length; i++) { const e = L.length > i ? L[i % L.length] : pick(L); const tx = ex(e), ty = ey(e);
    B.fx.push({ k: 'streak', x: tx + 60, y: ty - 160, x2: tx, y2: ty, t: -i * 0.07, d: 0.35, c: '#ffb040' });
    setTimeout(() => { if (!e.dead) { sfx('feu', tx, ty, 110 * sOf(e.z), 0.45); hitEnemy(e, dmg, false); } }, 250 + i * 70); }
}
function freezeAll(sec) { for (const e of alive()) e.frozen = Math.max(e.frozen || 0, sec); B.flash = { c: '150,220,255', t: 0.45, a: 0.35 }; }
function boneSpears(dmg, n) { const L = alive().sort(() => Math.random() - 0.5).slice(0, n); for (const e of L) { B.fx.push({ k: 'spike', x: sx(e.X, e.z), y: py(e.z), s: sOf(e.z), t: 0, d: 0.55 }); hitEnemy(e, dmg, false); } }
function novaFire(st) {""")
rep("const st = heroStats(); if (st.vol) B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + dmg * st.vol / 100);",
    "const st = heroStats(); if (st.vol) B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + dmg * st.vol / 100); if (crit && st.critFreeze && !e.boss) e.frozen = Math.max(e.frozen || 0, 1);")
rep("if (e.dead) return; if (B.oneshot) dmg = Math.max(dmg, e.hp + 1); e.hp -= dmg;",
    "if (e.dead) return; if (e.frozen > 0) { const st0 = heroStats(); if (st0.frozenBonus) dmg *= 1 + st0.frozenBonus; } if (B.oneshot) dmg = Math.max(dmg, e.hp + 1); e.hp -= dmg;")
rep("if (e.hp <= 0) { e.dead = 1; e.deadT = 0; if (st.killHeal)",
    "if (e.hp <= 0) { e.dead = 1; e.deadT = 0; const wasFrozen = e.frozen > 0; setTimeout(() => { if (st.bloodBoom) aoe(e, 0.22, st.atk * 2, 'mort', '#ff2040'); if (st.ignite) aoe(e, 0.16, st.atk * 1.2, 'feu', '#ff9a30'); if (st.shatter && wasFrozen) aoe(e, 0.22, st.atk * 3, 'glace', '#bff0ff'); }, 60); if (st.killHeal)")
rep("d = Math.max(1, d * (100 / (100 + st.def * 4)) * (1 - st.dmgRed)); B.hero.hp -= d;",
    "d = Math.max(1, d * (100 / (100 + st.def * 4)) * (1 - st.dmgRed)); if (B.shield > 0) { const a = Math.min(B.shield, d); B.shield -= a; d -= a; num(CX + rand(-20, 20), YF - 96, 'Bloqué', '#e8f4ff', 1); if (d <= 0) return; } if (st.thorns) { const L = alive(); if (L.length) { const t = L.reduce((a, b) => b.z < a.z ? b : a); hitEnemy(t, d * st.thorns * 4, false); } } B.hero.hp -= d;")

# gel : les démons gelés ne bougent ni n'attaquent
rep("if (e.dead) { e.deadT += dt; continue; } e.t += dt; e.flash -= dt; e.chill -= dt; if (e.spawn > 0) { e.spawn -= dt; continue; }",
    "if (e.dead) { e.deadT += dt; continue; } e.flash -= dt; if (e.spawn > 0) { e.spawn -= dt; continue; } if (e.frozen > 0) { e.frozen -= dt; continue; } e.t += dt; e.chill -= dt;")
rep("  if (e.chill > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.35 * al, loop, tint: '#7ae8ff' });",
    "  if (e.chill > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.35 * al, loop, tint: '#7ae8ff' });\n  if (e.frozen > 0 && !e.dead) { dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.6, loop, tint: '#c8f4ff' }); ctx.globalCompositeOperation = 'lighter'; glow(x, y - A.bh * 0.5 * sc, 30 * sc, 'rgba(150,220,255,1)', 0.35); ctx.globalCompositeOperation = 'source-over'; }")

# =================== boucle : déclencheurs périodiques, sorts, donjon ===================
rep("  placeDeco();\n  { const G = B.gear", """  placeDeco();
  combatTick(dt);
  { const G = B.gear""")
rep("function beginWalk() {", r"""function combatTick(dt) { // sets (déclencheurs) + sorts + timer du donjon
  const h = B.hero, fighting = !B.walk && !h.dead && B.wave && alive().length > 0, st = heroStats();
  B.frenzyT = (B.frenzyT || 0) - dt; B.frenzyCd = (B.frenzyCd || 0) - dt; B.spFrT = (B.spFrT || 0) - dt; if (B.flash) { B.flash.t -= dt; if (B.flash.t <= 0) B.flash = null; }
  if (st.frenzy && h.hp < h.hpMax * 0.3 && B.frenzyCd <= 0 && !h.dead) { B.frenzyT = 5; B.frenzyCd = 20; B.banner = { a: 'Frénésie', b: 'Vitesse d\'attaque ×2', t: 1.2 }; }
  if (st.boneShield) { B.shT = (B.shT || 0) - dt; if (B.shT <= 0) { B.shT = 10; B.shield = Math.max(B.shield || 0, h.hpMax * 0.2); } }
  if (B.plague) { B.plague.t -= dt; B.plague.tick -= dt; if (B.plague.tick <= 0) { B.plague.tick = 0.5; for (const e of alive()) hitEnemy(e, B.plague.dps * 0.5, false); for (let i = 0; i < 6; i++) B.fx.push({ k: 'p', x: rand(40, BW - 40), y: rand(py(0.9), py(0.1)), vx: rand(-8, 8), vy: rand(-14, -4), g: 0, c: pick(['#7aff5a', '#3ad04a', '#b0ff80']), t: 0, d: 1, r: rand(1.5, 3) }); } if (B.plague.t <= 0) B.plague = null; }
  if (B.dun && !B.dun.end) { B.dun.t -= dt; if (B.dun.t <= 0) dunEnd(false, 'Temps écoulé'); }
  if (!fighting) return;
  if (st.spears) { B.spT = (B.spT || 0) - dt; if (B.spT <= 0) { B.spT = 4; boneSpears(st.atk * 4, 5); } }
  if (st.blizzard) { B.bzT = (B.bzT || 0) - dt; if (B.bzT <= 0) { B.bzT = 6; freezeAll(2); } }
  for (let i = 0; i < slotCount(); i++) { const id = S.slots[i]; if (!id || !S.spells[id]) continue; B.cd = B.cd || {}; B.cd[id] = (B.cd[id] === undefined ? SPELLS[id].cd * 0.5 : B.cd[id]) - dt; if (B.cd[id] <= 0) { B.cd[id] = SPELLS[id].cd; castSpell(id); } }
}
function beginWalk() {""")

# dessins : traînées, lances d'os, éclairs, colonne, bouclier, flash
rep("for (const f of B.fx) { const p = f.t / f.d; if (f.k === 'ring') {",
    """for (const f of B.fx) { const p = f.t / f.d; if (f.t < 0) continue;
    if (f.k === 'streak') { ctx.globalCompositeOperation = 'lighter'; const q = Math.min(1, p * 1.4), x = f.x + (f.x2 - f.x) * q, y = f.y + (f.y2 - f.y) * q; ctx.strokeStyle = f.c; ctx.lineWidth = 4; ctx.globalAlpha = 1 - p * 0.5; ctx.beginPath(); ctx.moveTo(x + 18, y - 48); ctx.lineTo(x, y); ctx.stroke(); glow(x, y, 16, 'rgba(255,160,60,1)', 0.8); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; continue; }
    if (f.k === 'spike') { const A2 = ASSETS.anim.list.spike, fr2 = Math.min(A2.n - 1, Math.floor(p * A2.n * 1.6)), sz = 34 * f.s * 2.2; ctx.globalAlpha = 1 - Math.max(0, p - 0.6) / 0.4; ctx.filter = 'brightness(2) saturate(0)'; ctx.drawImage(IMG.anim, A2.x + fr2 * 16, 0, 16, 16, f.x - sz / 2, f.y - sz, sz, sz); ctx.filter = 'none'; ctx.globalAlpha = 1; continue; }
    if (f.k === 'bolt') { ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = '#bfe8ff'; ctx.lineWidth = 3 * (1 - p) + 1; ctx.globalAlpha = 1 - p; ctx.beginPath(); f.pts.forEach((q, i) => { const jx = i ? rand(-6, 6) : 0; ctx[i ? 'lineTo' : 'moveTo'](q[0] + jx, q[1] + jx); }); ctx.stroke(); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; continue; }
    if (f.k === 'pillar') { ctx.globalCompositeOperation = 'lighter'; const gr = ctx.createLinearGradient(0, f.y - 260, 0, f.y); gr.addColorStop(0, 'rgba(255,240,160,0)'); gr.addColorStop(1, 'rgba(255,230,140,1)'); ctx.globalAlpha = (1 - p) * 0.9; ctx.fillStyle = gr; const w2 = 30 * (1 - p * 0.5); ctx.fillRect(f.x - w2 / 2, f.y - 260, w2, 260); glow(f.x, f.y, 60, 'rgba(255,230,140,1)', 0.7 * (1 - p)); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; continue; }
    if (f.k === 'ring') {""")
rep("  if (B.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${B.fade})`;", "  if (B.flash) { ctx.fillStyle = `rgba(${B.flash.c},${B.flash.a * B.flash.t / 0.45})`; ctx.fillRect(0, -40, BW, BH + 80); }\n  if (B.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${B.fade})`;")
rep("  sprH(H.key, key, fr, CX, YF, sc);\n", """  sprH(H.key, key, fr, CX, YF, sc);
  if (B.shield > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = 'rgba(230,240,255,.7)'; ctx.lineWidth = 2; ctx.globalAlpha = 0.6 + Math.sin(time * 6) * 0.2; ctx.beginPath(); ctx.ellipse(CX, YF - 34, 34, 46, 0, 0, TAU); ctx.stroke(); ctx.restore(); }
  if (B.frenzyT > 0 || B.spFrT > 0) { ctx.globalCompositeOperation = 'lighter'; glow(CX, YF - 30, 50, 'rgba(255,40,60,1)', 0.35 + Math.sin(time * 12) * 0.1); ctx.globalCompositeOperation = 'source-over'; }
""")

# =================== sorts ===================
rep("// ---------- carte du monde ----------", r"""// ================= pouvoirs (sorts automatiques) =================
const SPELLS = {
  blades: { n: 'Lames d\'ombre', r: 1, cd: 6, c: '#b48aff', ic: 'sword', d: p => `6 lames frappent des démons au hasard (${p} % chacune)`, p: 150 },
  shield: { n: 'Égide sanglante', r: 1, cd: 15, c: '#ff5a72', ic: 'shield', d: p => `Bouclier de ${Math.round(p / 6)} % des PV max`, p: 150 },
  meteor: { n: 'Pluie de feu', r: 2, cd: 9, c: '#ff8a2a', ic: 'flame', d: p => `5 météores s'écrasent (${p} % chacun)`, p: 250 },
  nova: { n: 'Nova de givre', r: 2, cd: 12, c: '#7ad8ff', ic: 'snow', d: p => `Gèle tous les démons 2 s (${p} %)`, p: 120 },
  chain: { n: 'Chaîne d\'éclairs', r: 3, cd: 8, c: '#9ad0ff', ic: 'bolt', d: p => `Un éclair rebondit sur 6 démons (${p} %)`, p: 220 },
  plague: { n: 'Fléau', r: 3, cd: 14, c: '#7aff5a', ic: 'drop', d: p => `Nuage toxique : ${p} % par seconde à tous pendant 5 s`, p: 60 },
  smite: { n: 'Châtiment', r: 4, cd: 16, c: '#ffe680', ic: 'sun', d: p => `Colonne sacrée sur le démon le plus fort (${p} %)`, p: 900 },
  frenzy: { n: 'Frénésie', r: 4, cd: 18, c: '#ff3a5a', ic: 'wind', d: p => `Vitesse d'attaque +${Math.round(p / 3)} % pendant 6 s`, p: 180 },
};
const SPR = ['', 'Rare', 'Épique', 'Légendaire', 'Mythique'], SPRC = ['', '#3a8ae0', '#a040e0', '#ff9a2a', '#ff2a3a'];
IC.snow = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 2v20M3.3 7l17.4 10M3.3 17 20.7 7M9 4l3 3 3-3M9 20l3-3 3 3"/></svg>';
IC.sun = '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="5"/><path d="M11 1h2v4h-2zM11 19h2v4h-2zM1 11h4v2H1zM19 11h4v2h-4zM4.2 5.6l1.4-1.4 2.8 2.8-1.4 1.4zM15.6 17l1.4-1.4 2.8 2.8-1.4 1.4zM4.2 18.4 7 15.6 8.4 17l-2.8 2.8zM15.6 7 18.4 4.2l1.4 1.4L17 8.4z"/></svg>';
const slotCount = () => S.c >= 4 ? 3 : S.c >= 2 ? 2 : 1;
const spPct = id => Math.round(SPELLS[id].p * (1 + 0.2 * ((S.spells[id] || { lv: 1 }).lv - 1)));
function castSpell(id) {
  const st = heroStats(), k = spPct(id) / 100, L = alive(), sp = SPELLS[id]; if (!L.length && id !== 'shield' && id !== 'frenzy') return;
  B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1);
  if (id === 'blades') for (let i = 0; i < 6; i++) { const e = pick(L); sfx('epee', ex(e), ey(e), 80 * sOf(e.z), 0.3, rand(0, TAU)); hitEnemy(e, st.atk * k, false); }
  else if (id === 'shield') B.shield = Math.max(B.shield || 0, B.hero.hpMax * k / 6);
  else if (id === 'meteor') meteorShower(st.atk * k, 5);
  else if (id === 'nova') { freezeAll(2); for (const e of L) { sfx('glace', ex(e), ey(e), 80 * sOf(e.z), 0.4); hitEnemy(e, st.atk * k, false); } }
  else if (id === 'chain') { let cur = L.reduce((a, b) => b.z < a.z ? b : a), pts = [[CX, YF - 40]], hit = new Set(); for (let i = 0; i < 6 && cur; i++) { hit.add(cur); pts.push([ex(cur), ey(cur)]); hitEnemy(cur, st.atk * k, false); const nx = alive().filter(o => !hit.has(o)); cur = nx.length ? nx.reduce((a, b) => hyp(b.X - cur.X, b.z - cur.z) < hyp(a.X - cur.X, a.z - cur.z) ? b : a) : null; } B.fx.push({ k: 'bolt', pts, t: 0, d: 0.35 }); }
  else if (id === 'plague') B.plague = { t: 5, tick: 0, dps: st.atk * k };
  else if (id === 'smite') { const e = L.reduce((a, b) => b.hp > a.hp ? b : a); B.fx.push({ k: 'pillar', x: ex(e), y: py(e.z), t: 0, d: 0.7 }); B.shake = Math.max(B.shake, 6); hitEnemy(e, st.atk * k, true); }
  else if (id === 'frenzy') { B.spFrT = 6; B.spFrK = spPct(id) / 300; }
}
function summon(n) {
  const cost = n * 10; if (S.pages < cost) { toast('Pas assez de pages de grimoire'); return; } S.pages -= cost; const got = [];
  for (let i = 0; i < n; i++) { const r = Math.random() * 100, tier = r < 5 ? 4 : r < 20 ? 3 : r < 50 ? 2 : 1, ids = Object.keys(SPELLS).filter(k => SPELLS[k].r === tier), id = pick(ids);
    const o = S.spells[id]; if (!o) { S.spells[id] = { lv: 1, cp: 0 }; got.push([id, 'Nouveau !']); } else { o.cp++; if (o.cp >= o.lv) { o.cp = 0; o.lv++; got.push([id, `Niveau ${o.lv} !`]); } else got.push([id, `+1 copie`]); } }
  if (!S.slots.some(Boolean)) { const f = Object.keys(S.spells)[0]; if (f) S.slots[0] = f; }
  save(); sheet(`<h3>Invocation <button class="x" type="button" aria-label="Fermer">✕</button></h3><div class="spgrid">${got.map(([id, t]) => spCard(id, t)).join('')}</div><button class="btn gold" type="button" style="width:100%;margin-top:14px" id="okS">Super</button>`); $('okS').onclick = closeM;
}
function spCard(id, extra) { const sp = SPELLS[id], o = S.spells[id]; return `<div class="spc ${o ? '' : 'lock'}" data-sp="${id}" style="--sc:${sp.c};--rc:${SPRC[sp.r]}"><div class="spi">${IC[sp.ic]}</div><b>${sp.n}</b><small>${o ? (extra || `Nv ${o.lv} · ${o.cp}/${o.lv}`) : SPR[sp.r]}</small></div>`; }
function showSpell(id) {
  const sp = SPELLS[id], o = S.spells[id], eqI = S.slots.indexOf(id);
  sheet(`<h3>${sp.n} <button class="x" type="button" aria-label="Fermer">✕</button></h3><div class="card" style="--rc:${sp.c}"><div class="hd"><div class="icon-big spi big" style="color:${sp.c}">${IC[sp.ic]}</div><div><h4>${sp.n}</h4><div class="rar"><b style="color:${SPRC[sp.r]}">${SPR[sp.r]}</b> · ${o ? `niveau ${o.lv}` : 'pas encore obtenu'}</div></div></div>
  <div class="stats"><div class="stat"><span>Effet</span><em style="font:700 13px var(--b);text-align:right">${sp.d(spPct(id))}</em></div><div class="stat"><span>Recharge</span><em>${sp.cd} s</em></div>${o ? `<div class="stat sub"><span>Prochain niveau</span><em>${o.cp} / ${o.lv} copies</em></div>` : ''}</div></div>
  ${o ? `<div class="row" style="margin-top:14px">${eqI >= 0 ? `<button class="btn" id="unS" type="button" style="flex:1">Retirer</button>` : Array.from({ length: slotCount() }, (_, i) => `<button class="btn gold" type="button" data-slot="${i}" style="flex:1">Emplacement ${i + 1}<small>${S.slots[i] ? 'remplace ' + SPELLS[S.slots[i]].n : 'libre'}</small></button>`).join('')}</div>` : ''}`);
  if ($('unS')) $('unS').onclick = () => { S.slots[eqI] = null; save(); closeM(); };
  $('mbox').querySelectorAll('[data-slot]').forEach(b => b.onclick = () => { const i = +b.dataset.slot; const j = S.slots.indexOf(id); if (j >= 0) S.slots[j] = null; S.slots[i] = id; save(); closeM(); toast(`${sp.n} équipé`); });
}
// ================= donjons des sets =================
const DUNS = { sang: { n: 'Crypte de Sang', bi: 3 }, os: { n: 'Ossuaire Profond', bi: 1 }, braise: { n: 'Forge Infernale', bi: 0 }, givre: { n: 'Caveau Gelé', bi: 2 } };
const dunReward = lv => 2 + Math.floor((lv - 1) / 3);
function startDungeon(k) {
  if (B.dun) return; if (S.keys < 1) { toast('Plus de clés : 3 reviennent chaque jour, +1 par boss de chapitre'); return; }
  B.dun = { k, lv: S.dlv[k], w: 0, t: 60 }; B.walk = null; B.pend = 0; B.pendFn = null; B.scene = 'arena'; B.scroll = 0; B.fade = 1; closeM(); startWave();
}
function startDunWave() {
  const D = B.dun, n = 4 + (D.lv - 1) * 5; B.bi = DUNS[D.k].bi; B.scene = 'arena'; placeDeco(); B.en = []; B.es = []; B.shots = [];
  const boss = D.w === 3, count = boss ? 0 : 6 + D.w * 2;
  B.wave = { n, boss, left: count, spawnT: 0.4, total: count + (boss ? 1 : 0), killed: 0, dun: true };
  if (boss) { const st = enemyStats(n, true); st.hp *= 0.8; spawnEnemy(pick(['beast1', 'beast2', 'beast3', 'beast4', 'beast5']), 0, 0.93, st, true); }
  if (D.w === 0) { const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0; B.hero.reported = 0; B.dmg = []; B.waveDmg = 0; B.cd = {}; B.banner = { a: DUNS[D.k].n, b: `Niveau ${D.lv} · 3 vagues + boss en 60 s`, t: 2 }; }
  ui();
}
function dunEnd(win, why) {
  const D = B.dun; if (!D || D.end) return; D.end = true; B.en.forEach(e => { if (!e.dead) e.frozen = 99; });
  if (win) { const r = dunReward(D.lv); S.seals[D.k] += r; S.pages += 5 + D.lv; S.keys--; S.dlv[D.k]++; B.banner = { a: 'Victoire !', b: `+${r} Sceaux · ${SETS[D.k].n}`, t: 2.4 }; }
  else B.banner = { a: 'Échec', b: `${why} · la clé n'est pas consommée`, t: 2.4 };
  save(); setTimeout(() => { B.dun = null; B.scene = 'x'; B.fade = 1; B.hero.dead = 0; startWave(); ui(); }, 2300);
}
function dunHTML() {
  return `<div class="frame" style="padding:12px"><h3>Donjons des sets <span class="keys">Clés : ${S.keys}</span></h3><p style="margin:0 0 10px;color:var(--dim);font:700 12px/1.4 var(--b)">Gagne des Sceaux pour graver un set sur la pièce de ton choix (bouton « Graver » sur un objet). 3 clés par jour, +1 par boss de chapitre. La clé n'est consommée qu'en cas de victoire.</p>
  ${SETK.map(k => `<div class="dun" style="--sc:${SETS[k].c}"><div><b>${DUNS[k].n}</b><small>${SETS[k].n} · niveau ${S.dlv[k]}</small><small>Récompense : ${dunReward(S.dlv[k])} Sceaux · tu en as <em>${S.seals[k]}</em></small></div><button class="btn gold" type="button" data-dun="${k}" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div>`).join('')}</div>`;
}
// ================= gravure des sets =================
const sealCost = r => r >= 4 ? 3 : r === 3 ? 2 : 1;
function openEngrave(it, back) {
  const c = sealCost(it.r);
  sheet(`<h3>Graver un set <button class="x" type="button" aria-label="Fermer">✕</button></h3><p style="margin:0 0 10px;color:var(--dim);font:700 13px/1.4 var(--b)">${SLOTS.find(q => q.id === it.slot).n} ${RAR[it.r].n.toLowerCase()} : ${c} Sceau${c > 1 ? 'x' : ''} du set choisi. Le set remplace l'ancien.</p>
  ${SETK.map(k => `<button class="btn engr" type="button" data-eg="${k}" style="--sc:${SETS[k].c}" ${S.seals[k] < c || it.set === k ? 'disabled' : ''}><b>${SETS[k].n}</b><small>${it.set === k ? 'déjà gravé' : `${S.seals[k]} Sceaux · coûte ${c}`}</small></button>`).join('')}`);
  $('mbox').querySelector('.x').onclick = back;
  $('mbox').querySelectorAll('[data-eg]').forEach(b => b.onclick = () => { const k = b.dataset.eg; S.seals[k] -= c; it.set = k; save(); B.gear = gear(); toast(`${SETS[k].n} gravé !`); equipFx({ r: 6 }); back(); });
}
// ---------- carte du monde ----------""")

# bouton Graver dans les fiches
rep("""    <div class="row" style="margin-top:14px"><button class="btn" id="unB" type="button" style="flex:1">Retirer<small>vers le sac</small></button>""",
    """    <div class="row" style="margin-top:14px"><button class="btn" id="unB" type="button" style="flex:1">Retirer<small>vers le sac</small></button>${it.r >= 2 ? '<button class="btn red" id="egB" type="button" style="flex:1">Graver<small>set</small></button>' : ''}""")
rep("    $('altB').onclick = () => openBag(it.slot);", "    $('altB').onclick = () => openBag(it.slot); if ($('egB')) $('egB').onclick = () => openEngrave(it, () => showItem(it, null));")
rep("""<button class="btn" id="sellB" type="button" style="flex:1">Vendre<small>+${fmt(it.v)} or</small></button>${isNew ?""", """<button class="btn" id="sellB" type="button" style="flex:1">Vendre<small>+${fmt(it.v)} or</small></button>${!isNew && it.r >= 2 ? '<button class="btn red" id="egB" type="button" style="flex:1">Graver<small>set</small></button>' : ''}${isNew ?""")
rep("    if ($('bagB')) $('bagB').onclick =", "    if ($('egB')) $('egB').onclick = () => openEngrave(it, () => showItem(it, 'bag'));\n    if ($('bagB')) $('bagB').onclick =")

# =================== branchements de la boucle de jeu ===================
rep("function startWave() {\n", "function startWave() {\n  if (B.dun) return startDunWave();\n")
rep("function stageCleared() {\n  const boss = B.wave.boss;", "function stageCleared() {\n  if (B.dun) { B.dun.w++; if (B.dun.w >= 4) dunEnd(true); else { B.pend = 0.5; B.pendFn = startWave; } return; }\n  const boss = B.wave.boss; S.pages += boss ? 10 : 1; if (boss && !S.farm) S.keys++;")
rep("function heroDied() { // on ne meurt pas", "function heroDied() { if (B.dun) { dunEnd(false, 'Le héros est à terre'); return; } // on ne meurt pas")
rep("if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0; B.banner = { a: 'Repli !',", "if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0; if (!B.dun) B.banner = { a: 'Repli !',")
rep("function uiWave() {\n  const w = B.wave;", "function uiWave() {\n  if (B.dun) { const D = B.dun; $('waveBox').classList.add('boss'); $('waveBar').style.width = (Math.max(0, D.t) / 60 * 100).toFixed(1) + '%'; $('waveTxt').textContent = D.end ? '' : `${D.w < 3 ? `Vague ${D.w + 1}/3` : 'Boss'} · ${Math.ceil(Math.max(0, D.t))} s`; return; }\n  const w = B.wave;")
rep("hamTick(); $('stage').textContent = S.farm ?", "hamTick(); if (B.dun) { $('stage').textContent = 'DONJON'; $('biomeN').textContent = `${DUNS[B.dun.k].n} · niveau ${B.dun.lv}`; $('challengeBtn').hidden = true; } else $('stage').textContent = S.farm ?")
rep("$('bossBtn').style.display = 'none'; $('challengeBtn').hidden = !S.farm;", "$('bossBtn').style.display = 'none'; $('challengeBtn').hidden = !S.farm || !!B.dun;")
rep("function challenge() { // remonter soi-même à l'étape suivante\n  if (!S.farm) return;", "function challenge() { // remonter soi-même à l'étape suivante\n  if (!S.farm || B.dun) return;")

# =================== onglets Pouvoirs et Donjons ===================
a = s.index("  } else {\n    const sk = tab === 'skills';"); b = s.index("\n  }\n}\n", a)
s = s[:a] + r"""  } else if (tab === 'skills') {
    const n = slotCount(), owned = Object.keys(S.spells).length;
    $('panel').innerHTML = `<div class="frame" style="padding:12px"><h3>Pouvoirs équipés</h3><div class="spslots">${[0, 1, 2].map(i => { const id = S.slots[i]; if (i >= n) return `<div class="sps lock">${IC.lock}<small>Chapitre ${i === 1 ? 2 : 4}</small></div>`; return id ? `<div class="sps" data-sp="${id}" style="--sc:${SPELLS[id].c}"><div class="spi">${IC[SPELLS[id].ic]}</div><small>${SPELLS[id].n}</small><em>Nv ${S.spells[id].lv}</em></div>` : `<div class="sps empty"><b>+</b><small>Libre</small></div>`; }).join('')}</div>
    <div class="summon"><div><b>${S.pages}</b><small>pages de grimoire</small><small>+1 par vague · +10 par boss · donjons</small></div><button class="btn" type="button" id="sum1" ${S.pages < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 pages</small></button><button class="btn gold" type="button" id="sum10" ${S.pages < 100 ? 'disabled' : ''}>×10<small>100 pages</small></button></div>
    <h3 style="margin-top:14px">Grimoire · ${owned}/${Object.keys(SPELLS).length}</h3><div class="spgrid">${Object.keys(SPELLS).map(id => spCard(id)).join('')}</div></div>`;
    $('sum1').onclick = () => summon(1); $('sum10').onclick = () => summon(10);
    document.querySelectorAll('[data-sp]').forEach(b => b.onclick = () => showSpell(b.dataset.sp));
  } else {
    $('panel').innerHTML = dunHTML();
    document.querySelectorAll('[data-dun]').forEach(b => b.onclick = () => startDungeon(b.dataset.dun));""" + s[b:]

# =================== styles ===================
rep(".eveil{display:grid;gap:6px}", """.eveil{display:grid;gap:6px}
.spi{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;font-size:24px;color:var(--sc);background:radial-gradient(circle,color-mix(in srgb,var(--sc) 35%,transparent),#14080d 70%);border:2px solid var(--sc);box-shadow:0 0 12px -2px var(--sc)}
.spi.big{width:64px;height:64px;font-size:32px;border-radius:14px}
.spslots{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.sps{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px;border-radius:14px;border:2px solid var(--sc,#4a2a36);background:#ffffff06;font:800 11px var(--b);text-align:center;cursor:pointer;position:relative}
.sps em{position:absolute;top:6px;right:6px;font:400 11px var(--n);font-style:normal;color:var(--gold2)}
.sps.empty{border-style:dashed;color:var(--dim)}.sps.empty b{font:400 30px/46px var(--n)}
.sps.lock{color:#6a5058;border-style:dashed}.sps.lock svg{font-size:26px;margin:10px 0}
.summon{display:grid;grid-template-columns:1fr auto auto;gap:8px;align-items:center;margin-top:12px;padding:10px;border-radius:12px;background:linear-gradient(90deg,#3a1a2a,#1a0b12);border:1.5px solid #6b3a2e}
.summon b{display:block;font:400 22px var(--n);color:var(--gold2)}.summon small{display:block;font:800 10px var(--b);color:var(--dim)}
.summon .btn{min-height:46px;font-size:14px;padding:4px 10px}
.spgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.spc{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 2px;border-radius:12px;border:2px solid var(--rc);background:#ffffff06;text-align:center;cursor:pointer}
.spc b{font:800 10px/1.2 var(--b)}.spc small{font:400 11px var(--n);color:var(--gold2)}
.spc.lock{filter:grayscale(1) brightness(.5)}
#spellHud{position:absolute;left:8px;bottom:36px;display:flex;gap:6px;z-index:3;pointer-events:none}
#spellHud div{position:relative;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-size:17px;color:var(--sc);background:#0b0508d8;border:2px solid var(--sc);overflow:hidden}
#spellHud div i{position:absolute;inset:0;background:conic-gradient(#000c var(--cd),transparent 0)}
.keys{font:400 16px var(--n);color:var(--gold2)}
.dun{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;margin-top:8px;border-radius:12px;border:1.5px solid color-mix(in srgb,var(--sc) 60%,transparent);background:linear-gradient(90deg,color-mix(in srgb,var(--sc) 18%,transparent),transparent)}
.dun b{display:block;font:900 15px var(--t);color:var(--sc)}.dun small{display:block;font:700 12px var(--b);color:var(--dim)}.dun em{font-style:normal;color:#fff}
.engr{width:100%;margin-top:8px;border-color:var(--sc);text-align:left}.engr b{color:var(--sc);font:900 15px var(--t)}""")

# HUD des sorts (recharges) au-dessus de la barre de vie
rep('    <button id="challengeBtn" type="button" hidden></button>', '    <div id="spellHud"></div>\n    <button id="challengeBtn" type="button" hidden></button>')
rep("function uiCombat() {", """function uiSpells() {
  const ids = S.slots.slice(0, slotCount()).filter(id => id && S.spells[id]), key = ids.join(','); const el = $('spellHud');
  if (el.dataset.k !== key) { el.dataset.k = key; el.innerHTML = ids.map(id => `<div style="--sc:${SPELLS[id].c}">${IC[SPELLS[id].ic]}<i></i></div>`).join(''); }
  [...el.children].forEach((d, i) => { const id = ids[i], cd = B.cd && B.cd[id] !== undefined ? Math.max(0, B.cd[id]) / SPELLS[id].cd : 0.5; d.querySelector('i').style.setProperty('--cd', (cd * 100).toFixed(0) + '%'); });
}
function uiCombat() { uiSpells();""")

# =================== admin ===================
rep('<div class="lbl2">Sets (6 pièces légendaires)</div>', '<div class="lbl2">Donjons, sceaux et pouvoirs</div><div class="adm"><button class="btn gold" data-a="keys" type="button">+10 clés</button><button class="btn gold" data-a="seals" type="button">+20 Sceaux de chaque</button><button class="btn gold" data-a="pages" type="button">+500 pages</button><button class="btn" data-a="allsp" type="button">Tous les sorts Nv 5</button></div><div class="lbl2">Sets (6 pièces légendaires)</div>')
rep("rset: () => {", "keys: () => S.keys += 10, seals: () => SETK.forEach(k => S.seals[k] += 20), pages: () => S.pages += 500, allsp: () => { Object.keys(SPELLS).forEach(k => S.spells[k] = { lv: 5, cp: 0 }); S.slots = Object.keys(SPELLS).slice(0, 3); },\n    rset: () => {")

open(P, 'w').write(s)
print('ok')
