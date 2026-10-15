P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v7.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

# ---------- étape jouée : la frontière (S.c/S.s) ou l'étape de farm (S.fc/S.fs) ----------
rep("function stageIndex() { return (S.c - 1) * 10 + S.s; }",
    "const PC = () => S.farm && S.fc ? S.fc : S.c, PS = () => S.farm && S.fs ? S.fs : S.s; // chapitre / étape réellement jouée\nconst label = (c, s) => `${c}-${s}`;\nfunction stageIndex() { return (PC() - 1) * 10 + PS(); }")
rep("L = Math.max(1, Math.floor(stageIndex() * 0.9) + ri(-2, 2))", "L = Math.max(1, Math.floor(Math.max(stageIndex(), S.best - 1) * 0.9) + ri(-2, 2))")
rep("const biome = () => BIOMES[B.bi === undefined ? (S.c - 1) % BIOMES.length : B.bi];", "const biome = () => BIOMES[B.bi === undefined ? (PC() - 1) % BIOMES.length : B.bi];")
rep("const sceneFor = () => S.s === 10 && !S.farm ? 'arena' : 'corridor';", "const sceneFor = () => PS() === 10 && !S.farm ? 'arena' : 'corridor';")
rep("B.bi = (S.c - 1) % BIOMES.length; const sc = sceneFor(), prev = B.scene;", "B.bi = (PC() - 1) % BIOMES.length; const sc = sceneFor(), prev = B.scene;")
rep("const n = stageIndex(), boss = S.s === 10 && !S.farm, ch = S.c, pool", "const n = stageIndex(), boss = PS() === 10 && !S.farm, ch = PC(), pool")
rep("const count = boss ? 0 : 4 + Math.floor(S.s / 2) + Math.min(6, ch);", "const count = boss ? 0 : 4 + Math.floor(PS() / 2) + Math.min(6, ch);")
rep("const pool = POOL[Math.min(POOL.length - 1, S.c - 1)], st = enemyStats(w.n, false), from = Math.random();\n  let img = pick(pool); if (S.c >= 2", "const pool = POOL[Math.min(POOL.length - 1, PC() - 1)], st = enemyStats(w.n, false), from = Math.random();\n  let img = pick(pool); if (PC() >= 2")
rep("const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0;", "const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0; B.hero.reported = 0; B.dmg = []; B.waveDmg = 0;")

# ---------- fin de vague : en farm on boucle sur l'étape réussie ----------
rep("  if (S.farm) { toast('Vague nettoyée (entraînement)'); }", "  if (S.farm) { S.ham = Math.min(HAM_MAX + 50, S.ham + 1); }")
# ---------- plus de mort : repli vers la dernière étape réussie ----------
rep("""function heroDied() {
  if (B.wave && B.wave.boss) { S.farm = true; toast('Le boss est trop fort : entraîne-toi et forge !'); }
  else if (S.s > 1) S.s--;
  save(); B.pend = 0.3; B.pendFn = () => { B.fade = 1; B.scroll = 0; startWave(); };
}""", """function heroDied() { // on ne meurt pas : on se replie sur la dernière étape réussie et on farm
  let c = PC(), st = PS();
  if (st > 1) st--; else if (c > 1) { c--; st = 9; }
  if (st === 10) st = 9;
  S.farm = true; S.fc = c; S.fs = st;
  toast(`Repli sur ${label(c, st)} : forge et reviens défier ${label(S.c, S.s)}`);
  save(); B.pend = 0.2; B.pendFn = () => { B.fade = 1; B.scroll = 0; startWave(); };
}
function challenge() { // remonter soi-même à l'étape suivante
  if (B.walk || !S.farm) return; S.farm = false; save(); B.en = []; B.es = []; B.shots = []; B.wave = null; B.hero.dead = 0; beginWalk();
}""")
rep("if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0; }", "if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0; B.banner = { a: 'Repli !', b: 'Le héros recule pour reprendre des forces', t: 1.6 }; }")
rep("if (h.dead) { h.deadT += dt; if (h.deadT > 1.4 && !h.reported) { h.reported = 1; heroDied(); } }", "if (h.dead) { h.deadT += dt; if (h.deadT > 1.2 && !h.reported) { h.reported = 1; heroDied(); } }")
# pas d'animation de mort : il chancelle
rep("else if (h.dead) { anim = 'mort'; fr = Math.min(14, h.deadT * 12); }", "else if (h.dead) { anim = 'touche'; fr = Math.min(9, h.deadT * 14); }")
rep("if (B.hero.dead) { ctx.fillStyle = `rgba(80,0,10,${Math.min(0.5, B.hero.deadT * 0.4)})`; ctx.fillRect(0, 0, BW, BH); }", "if (B.hero.dead) { ctx.fillStyle = `rgba(0,0,0,${Math.min(0.55, B.hero.deadT * 0.5)})`; ctx.fillRect(0, -40, BW, BH + 80); }")

# ---------- dégâts infligés : nombres plus lisibles + DPS ----------
rep("num(sx(e.X, e.z), py(e.z) - 50 * sOf(e.z), fmt(dmg), crit ? '#ffd23a' : '#ffffff', crit ? 1.3 : 1);",
    "num(sx(e.X, e.z) + rand(-6, 6), py(e.z) - 50 * sOf(e.z), fmt(dmg) + (crit ? '!' : ''), crit ? '#ffd23a' : '#ffffff', crit ? 1.4 : 1); B.dmg.push([B.t, Math.min(dmg, e.hp + dmg)]); B.waveDmg += Math.min(dmg, e.hp + dmg);")
rep("ctx.font = (n.k > 1.1 ? 17 : 12) + 'px Lilita, sans-serif'", "ctx.font = (n.k > 1.1 ? 22 : 15) + 'px Lilita, sans-serif'")
rep("const B = { en: [],", "const B = { dmg: [], waveDmg: 0, en: [],")

# ---------- HUD de combat ----------
rep('''    <div id="stageBar">''', '''    <div id="combatHud"><div id="hpBox"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-8.5-5.3-8.5-11.2A4.8 4.8 0 0 1 12 6.6a4.8 4.8 0 0 1 8.5 3.2C20.5 15.7 12 21 12 21z"/></svg><div class="hpbar"><i id="hpFill"></i><span id="hpTxt"></span></div></div><div id="dpsBox"><small>Dégâts / s</small><b id="dps">0</b><small id="totDmg"></small></div></div>
    <button id="challengeBtn" type="button" hidden></button>
    <div id="stageBar">''')
rep("#stageBar{", """#combatHud{position:absolute;left:8px;right:8px;bottom:8px;display:flex;gap:8px;align-items:flex-end;z-index:3;pointer-events:none}
#hpBox{flex:1;display:flex;align-items:center;gap:6px;color:#ff5a72;font-size:18px;filter:drop-shadow(0 2px 2px #000)}
.hpbar{position:relative;flex:1;height:18px;border-radius:9px;background:#0b0508e0;border:1.5px solid #6a2a3a;overflow:hidden}
.hpbar i{position:absolute;left:0;top:0;bottom:0;width:100%;background:linear-gradient(#ff7a8a,#c0162e);transition:width .15s;border-radius:8px}
.hpbar span{position:absolute;inset:0;font:400 12px/16px var(--n);color:#fff;text-align:center;text-shadow:0 1px 2px #000;letter-spacing:.03em}
#dpsBox{display:flex;flex-direction:column;align-items:flex-end;padding:4px 10px;border-radius:12px;background:#0b0508d8;border:1.5px solid #6a3a48;min-width:92px}
#dpsBox small{font:800 9px var(--b);color:var(--dim);text-transform:uppercase;letter-spacing:.06em}
#dpsBox b{font:400 20px/1 var(--n);color:#ffd27a;text-shadow:0 2px 0 #000}
#challengeBtn{position:absolute;left:50%;transform:translateX(-50%);top:calc(122px + env(safe-area-inset-top));z-index:4;border:2px solid #ffd27a;border-radius:22px;padding:8px 18px;background:linear-gradient(#ec3a54,#8a1028);color:#fff;font:400 16px var(--n);letter-spacing:.03em;box-shadow:0 4px 0 #4a0614,0 0 18px #ff3a5a80;animation:pulse 1.6s infinite;display:flex;align-items:center;gap:8px;white-space:nowrap}
#challengeBtn[hidden]{display:none}
#challengeBtn small{font:800 11px var(--b);opacity:.85}
@keyframes pulse{50%{box-shadow:0 4px 0 #4a0614,0 0 28px #ff3a5ac0;transform:translateX(-50%) scale(1.04)}}
#stageBar{""")
# le bouton Boss du dock devient inutile : le bouton Défier est dans la scène
rep("$('bossBtn').style.display = S.farm ? '' : 'none';", "$('bossBtn').style.display = 'none'; $('challengeBtn').hidden = !S.farm || !!B.walk; $('challengeBtn').innerHTML = `${IC.sword} Défier ${label(S.c, S.s)}<small>${S.s === 10 ? 'Boss' : ''}</small>`;")
rep("$('bossBtn').onclick = () => { if (B.walk) return; S.farm = false; S.s = 10; save(); B.en = []; B.es = []; beginWalk(); };", "$('bossBtn').onclick = challenge; $('challengeBtn').onclick = challenge;")
# ruban et losanges
rep("$('stage').textContent = `CHAPITRE ${S.c}`; $('biomeN').textContent = S.farm ? biome().n + ' · entraînement' : biome().n;",
    "$('stage').textContent = S.farm ? `FARM ${label(PC(), PS())}` : `CHAPITRE ${S.c} · ${S.s}/10`; $('biomeN').textContent = S.farm ? `${biome().n} · prochaine : ${label(S.c, S.s)}` : biome().n;")
rep("$('pips').innerHTML = Array.from({ length: 10 }, (_, i) => `<i class=\"${i + 1 < S.s || (S.farm && i < 9) ? 'done' : ''} ${i + 1 === S.s && !S.farm ? 'cur' : ''} ${i === 9 ? 'boss' : ''}\"></i>`).join('');",
    "$('pips').innerHTML = Array.from({ length: 10 }, (_, i) => `<i class=\"${i + 1 < S.s ? 'done' : ''} ${i + 1 === S.s ? 'cur' : ''} ${i === 9 ? 'boss' : ''}\" style=\"${S.farm && i + 1 === S.s ? 'opacity:.55' : ''}\"></i>`).join('');")
# mise à jour HUD de combat chaque image
rep("function uiWave() {", """function uiCombat() {
  const h = B.hero, p = clamp(h.hp / Math.max(1, h.hpMax), 0, 1); $('hpFill').style.width = (p * 100).toFixed(1) + '%'; $('hpTxt').textContent = `${fmt(Math.ceil(h.hp))} / ${fmt(h.hpMax)}`;
  while (B.dmg.length && B.dmg[0][0] < B.t - 3) B.dmg.shift(); const span = Math.min(3, Math.max(1, B.t - (B.dmg[0] ? B.dmg[0][0] : B.t)));
  $('dps').textContent = fmt(B.dmg.reduce((a, d) => a + d[1], 0) / span); $('totDmg').textContent = `vague : ${fmt(B.waveDmg)}`;
}
function uiWave() {""")
rep("draw(clock); heroPortrait(clock); if (uiT <= 0) { uiT = 0.5; uiTop(); } uiWave();", "draw(clock); heroPortrait(clock); if (uiT <= 0) { uiT = 0.5; uiTop(); } uiWave(); uiCombat();")
# barre de vie sous le héros : plus de doublon, le HUD l'affiche
rep("  const w = 60; ctx.fillStyle = 'rgba(0,0,0,.7)'; ctx.fillRect(CX - w / 2 - 1, YF + 8, w + 2, 6); ctx.fillStyle = '#e0283c'; ctx.fillRect(CX - w / 2, YF + 9, w * clamp(h.hp / h.hpMax, 0, 1), 4);\n", "")
# admin : boutons de progression cohérents avec le farm
rep("cp: () => { S.c++; S.s = 1; S.farm = false; B.fade = 1; startWave(); }, cm: () => { S.c = Math.max(1, S.c - 1); S.s = 1; S.farm = false; B.fade = 1; startWave(); },",
    "cp: () => { S.c++; S.s = 1; S.farm = false; S.best = Math.max(S.best, stageIndex()); B.fade = 1; startWave(); }, cm: () => { S.c = Math.max(1, S.c - 1); S.s = 1; S.farm = false; B.fade = 1; startWave(); },")
rep("boss: () => { S.s = 10; S.farm = false; startWave(); },", "boss: () => { S.s = 10; S.farm = false; startWave(); }, fail: () => { B.god = false; B.hero.hp = 1; hurtHero(1e12); },")
rep('<button class="btn red" data-a="kill" type="button">Tuer la vague</button></div>', '<button class="btn red" data-a="kill" type="button">Tuer la vague</button><button class="btn full" data-a="fail" type="button">Simuler une défaite</button></div>')

open(P, 'w').write(s)
print('ok')
