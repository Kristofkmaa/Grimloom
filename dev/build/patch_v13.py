P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v15.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:110])
    s = s.replace(old, new)

# =================== sauvegarde ===================
rep("function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { } }",
    "function save() { if (window.__noSave) return; S.lastSeen = Date.now(); try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { } }")
rep("S.hero = 'chevalier';", """S.hero = 'chevalier';
S.st = Object.assign({ equip: 0, stage: 0, forgeLv: 0, boss: 0, dun: 0, summon: 0, upg: 0, comp: 0, fused: 0, bestR: -1 }, S.st || {});
if (S.q === undefined) { S.q = 0; S.qStart = 0; } S.auto = Object.assign({ on: false, keep: 3, equip: true }, S.auto || {});
if (S.lvl === undefined) { S.lvl = 1; S.xp = 0; S.tp = 0; } S.tal = Object.assign({ force: 0, vit: 0, prec: 0, brut: 0, cel: 0, avar: 0 }, S.tal || {});
S.ach = S.ach || {}; if (S.pet === undefined) S.pet = null; if (S.snd === undefined) S.snd = true; if (S.loginStreak === undefined) S.loginStreak = 0;""")

# =================== stats : talents, succès, familiers ===================
rep("  o.crit = Math.min(75, o.crit); return o;", """  const T = S.tal, A = achBonus(), PT = S.pet;
  o.atk *= (1 + 0.03 * T.force + A.atk / 100) * (PT === 'braise' ? 1.06 : 1); o.pv *= 1 + 0.04 * T.vit + A.pv / 100; o.crit += 0.5 * T.prec; o.cdmg += 5 * T.brut + (PT === 'griffe' ? 10 : 0); o.rate *= 1 + 0.02 * T.cel; if (PT === 'sangsue') o.vol += 2;
  o.crit = Math.min(75, o.crit); return o;""")
rep("const g = Math.round(3 * Math.pow(1.11, B.wave.n) * (", "const g = Math.round(goldMul() * 3 * Math.pow(1.11, B.wave.n) * (")

# =================== compteurs ===================
rep("function equipItem(it) { const cur = S.eq[it.slot];", "function equipItem(it) { S.st.equip++; const cur = S.eq[it.slot];")
rep("if (cur && S.bag.length >= BAG_MAX && isNew) { S.gold += cur.v; S.eq[it.slot] = it; }", "if (cur && S.bag.length >= BAG_MAX && isNew) { S.gold += cur.v; S.eq[it.slot] = it; S.st.equip++; }")
rep("function upForge() { const c = forgeCost(); if (S.gold < c) return; S.gold -= c; S.forge++;", "function upForge() { const c = forgeCost(); if (S.gold < c) return; S.gold -= c; S.forge++; S.st.forgeLv++;")
rep("S.comps[id].lv++;", "S.comps[id].lv++; S.st.comp++;")
rep("S.pages -= cost; const got = [];", "S.pages -= cost; S.st.summon += n; const got = [];")
rep("S.keys--; S.dlv[D.k]++;", "S.keys--; S.dlv[D.k]++; S.st.dun++;")
rep("const boss = B.wave.boss; S.pages += boss ? 10 : 1; if (boss && !S.farm) S.keys++;", "const boss = B.wave.boss; S.pages += boss ? 10 : 1; if (boss && !S.farm) { S.keys++; S.st.boss++; sfxPlay('roar'); } S.st.stage++;")
rep("S.ham--; S.forged++; const it = makeItem(); save();", "S.ham--; S.forged++; const it = makeItem(); S.st.bestR = Math.max(S.st.bestR, it.r); sfxPlay('forge'); save();")
# XP par démon tué
rep("S.gold += g; S.kills++;", "S.gold += g; S.kills++; gainXP(1 + B.wave.n * 0.25); sfxPlay('kill');")
rep("num(sx(e.X, e.z) + rand(-6, 6), py(e.z) - 50 * sOf(e.z), fmt(dmg) + (crit ? '!' : '')", "sfxPlay(crit ? 'crit' : 'hit'); num(sx(e.X, e.z) + rand(-6, 6), py(e.z) - 50 * sOf(e.z), fmt(dmg) + (crit ? '!' : '')")

# =================== boss : phases + attaque annoncée ===================
rep("  if (!fighting) return;\n", """  if (!fighting) return;
  for (const e of B.en) if (e.boss && !e.dead && e.spawn <= 0) {
    if (!e.enraged && e.hp < e.max * 0.5) { e.enraged = 1; e.spd *= 1.5; e.atk *= 1.3; B.banner = { a: 'Enragé !', b: 'Le boss entre dans une fureur sanglante', t: 1.6 }; B.shake = 8; sfxPlay('roar'); }
    e.slamT = (e.slamT === undefined ? 5 : e.slamT) - dt; if (e.slamT <= 0 && !B.warn) { e.slamT = e.enraged ? 5 : 8; B.warn = { t: 1.1, d: 1.1, dmg: e.atk * 2.2 }; }
  }
  if (B.warn) { B.warn.t -= dt; if (B.warn.t <= 0) { const d = B.warn.dmg; B.warn = null; B.shake = 10; sfxPlay('slam'); for (let i = 0; i < 20; i++) burst(CX + rand(-40, 40), YF - rand(0, 10), '#ff3040', 1, 160); hurtHero(d); } }
""")
rep("e.cd = (e.boss ? 1.0 : rand(0.8, 1.3)) + e.aDur;", "e.cd = (e.boss ? (e.enraged ? 0.55 : 1.0) : rand(0.8, 1.3)) + e.aDur;")
rep("  if (e.flash > 0) dem(e.key", "  if (e.enraged && !e.dead) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.28 + Math.sin(time * 10) * 0.1, loop, tint: '#ff1030' });\n  if (e.flash > 0) dem(e.key")
rep("  if (B.flash) { ctx.fillStyle = `rgba(${B.flash.c},", """  if (B.warn) { const p = 1 - B.warn.t / B.warn.d; ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = `rgba(255,30,50,${0.15 + p * 0.35})`; ctx.beginPath(); ctx.ellipse(CX, YF - 2, 70 * p + 10, (70 * p + 10) * 0.32, 0, 0, TAU); ctx.fill(); ctx.strokeStyle = 'rgba(255,90,100,.9)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(CX, YF - 2, 80, 26, 0, 0, TAU); ctx.stroke(); ctx.restore(); }
  if (B.flash) { ctx.fillStyle = `rgba(${B.flash.c},""")
# familier qui flotte près du héros
rep("  L.push({ z: -0.02, f: () => { drawComp(0, time); drawComp(1, time); } });", "  L.push({ z: -0.02, f: () => { drawComp(0, time); drawComp(1, time); } });\n  if (S.pet && PETS[S.pet]) L.push({ z: 0.05, f: () => { const P0 = PETS[S.pet], bob = Math.sin(time * 3) * 4; dem(P0.dem, B.walk ? 'walk' : 'walk', 'S', time * (B.walk ? 14 : 6), CX + 46, YF - 74 + bob, 0.85, {}); ctx.globalCompositeOperation = 'lighter'; glow(CX + 46, YF - 92 + bob, 22, P0.c, 0.35); ctx.globalCompositeOperation = 'source-over'; } });")

# =================== nouveaux systèmes ===================
rep("// ================= pouvoirs (sorts automatiques) =================", r"""// ================= son (synthétisé, sans fichier) =================
let AC = null, MUS = null; const lastSfx = {};
function audioInit() { if (AC || !S.snd) return; try { AC = new (window.AudioContext || window.webkitAudioContext)(); music(true); } catch (e) { } }
function tone(f, d, type, vol, slide, at) { const t = AC.currentTime + (at || 0), o = AC.createOscillator(), g = AC.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (slide) o.frequency.exponentialRampToValueAtTime(slide, t + d); g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0008, t + d); o.connect(g).connect(AC.destination); o.start(t); o.stop(t + d + 0.02); }
function noise(d, vol, freq, at) { const t = AC.currentTime + (at || 0), n = AC.sampleRate * d, b = AC.createBuffer(1, n, AC.sampleRate), a = b.getChannelData(0); for (let i = 0; i < n; i++) a[i] = (Math.random() * 2 - 1) * (1 - i / n); const src = AC.createBufferSource(), f = AC.createBiquadFilter(), g = AC.createGain(); src.buffer = b; f.type = 'lowpass'; f.frequency.value = freq; g.gain.value = vol; src.connect(f).connect(g).connect(AC.destination); src.start(t); }
function sfxPlay(k) {
  if (!AC || !S.snd) return; const now = performance.now(), gap = { hit: 45, crit: 80, kill: 60 }[k] || 0; if (gap && now - (lastSfx[k] || 0) < gap) return; lastSfx[k] = now;
  try {
    if (k === 'hit') noise(0.06, 0.12, 1800);
    else if (k === 'crit') { noise(0.09, 0.18, 3200); tone(900, 0.08, 'square', 0.04, 500); }
    else if (k === 'kill') { tone(160, 0.14, 'sine', 0.18, 60); noise(0.1, 0.1, 600); }
    else if (k === 'forge') { tone(1320, 0.5, 'triangle', 0.1); tone(1980, 0.35, 'sine', 0.06); noise(0.05, 0.25, 5000); }
    else if (k === 'roar') { noise(0.9, 0.35, 400); tone(90, 0.9, 'sawtooth', 0.12, 45); }
    else if (k === 'slam') { tone(70, 0.5, 'sine', 0.4, 35); noise(0.4, 0.4, 300); }
    else if (k === 'door') { tone(110, 1.2, 'sawtooth', 0.08, 70); noise(1.2, 0.08, 500); }
    else if (k === 'level') [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.25, 'triangle', 0.1, 0, i * 0.09));
    else if (k === 'reward') [784, 988, 1175].forEach((f, i) => tone(f, 0.2, 'sine', 0.1, 0, i * 0.07));
    else if (k === 'spell') { tone(400, 0.3, 'sine', 0.08, 1200); noise(0.2, 0.08, 2500); }
  } catch (e) { }
}
function music(on) { // nappe sombre : deux basses désaccordées + vent
  if (!AC) return; if (!on) { if (MUS) { MUS.forEach(n => { try { n.stop(); } catch (e) { } }); MUS = null; } return; } if (MUS) return;
  const out = AC.createGain(); out.gain.value = 0.05; out.connect(AC.destination); MUS = [];
  for (const f of [55, 55.4, 82.4]) { const o = AC.createOscillator(); o.type = 'sine'; o.frequency.value = f; o.connect(out); o.start(); MUS.push(o); }
  const n = AC.sampleRate * 4, b = AC.createBuffer(1, n, AC.sampleRate), a = b.getChannelData(0); for (let i = 0; i < n; i++) a[i] = Math.random() * 2 - 1;
  const src = AC.createBufferSource(); src.buffer = b; src.loop = true; const f = AC.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 400; f.Q.value = 0.7; const lfo = AC.createOscillator(), lg = AC.createGain(); lfo.frequency.value = 0.07; lg.gain.value = 250; lfo.connect(lg).connect(f.frequency); const wg = AC.createGain(); wg.gain.value = 0.35; src.connect(f).connect(wg).connect(out); src.start(); lfo.start(); MUS.push(src, lfo);
}
addEventListener('pointerdown', audioInit, { once: false });

// ================= niveau du héros et talents =================
const xpNeed = l => Math.round(20 * Math.pow(1.22, l - 1));
function gainXP(x) { S.xp += x; while (S.xp >= xpNeed(S.lvl)) { S.xp -= xpNeed(S.lvl); S.lvl++; S.tp++; toast(`Niveau ${S.lvl} ! +1 point de talent`); sfxPlay('level'); } }
const TALENTS = { force: ['Force', 'Attaque +3 %', 'sword'], vit: ['Vitalité', 'Points de vie +4 %', 'heart'], prec: ['Précision', 'Critique +0,5 %', 'star'], brut: ['Brutalité', 'Dégâts critiques +5 %', 'star'], cel: ['Célérité', 'Vitesse d\'attaque +2 %', 'wind'], avar: ['Avarice', 'Or gagné +5 %', 'drop'] };
const TAL_MAX = 25;

// ================= familiers =================
const PETS = { ombre: { n: 'Ombre', dem: 'imp7', unlock: 2, d: 'Or gagné +8 %', c: 'rgba(160,120,255,1)' }, braise: { n: 'Braisillon', dem: 'imp5', unlock: 3, d: 'Attaque +6 %', c: 'rgba(255,120,40,1)' }, griffe: { n: 'Griffe', dem: 'imp9', unlock: 5, d: 'Dégâts critiques +10 %', c: 'rgba(255,220,90,1)' }, sangsue: { n: 'Sangsue', dem: 'imp1', unlock: 7, d: 'Vol de vie +2 %', c: 'rgba(255,40,70,1)' } };
const goldMul = () => (1 + 0.05 * S.tal.avar + achBonus().gold / 100) * (S.pet === 'ombre' ? 1.08 : 1);

// ================= succès =================
const ACH = [
  ['k1', 'Boucher novice', 'Tuer 100 démons', () => S.kills >= 100, { atk: 1 }], ['k2', 'Fléau des démons', 'Tuer 1 000 démons', () => S.kills >= 1000, { atk: 2 }], ['k3', 'Exterminateur', 'Tuer 10 000 démons', () => S.kills >= 10000, { atk: 3 }],
  ['f1', 'Apprenti forgeron', 'Forger 50 objets', () => S.forged >= 50, { pv: 1 }], ['f2', 'Maître forgeron', 'Forger 500 objets', () => S.forged >= 500, { pv: 3 }],
  ['b1', 'Tueur de boss', 'Vaincre un boss', () => S.st.boss >= 1, { atk: 1 }], ['b2', 'Chasseur de démons majeurs', 'Vaincre 5 boss', () => S.st.boss >= 5, { pv: 2 }],
  ['c3', 'Explorateur des abysses', 'Atteindre le chapitre 3', () => S.c >= 3, { gold: 5 }], ['c6', 'Seigneur des profondeurs', 'Atteindre le chapitre 6', () => S.c >= 6, { gold: 10 }],
  ['r3', 'Éclat violet', 'Obtenir un objet Épique', () => S.st.bestR >= 3, { atk: 1 }], ['r4', 'Lueur dorée', 'Obtenir un objet Légendaire', () => S.st.bestR >= 4, { pv: 2 }], ['r6', 'Élu divin', 'Obtenir un objet Divin', () => S.st.bestR >= 6, { atk: 5 }],
  ['d5', 'Pilleur de cryptes', 'Réussir 5 donjons', () => S.st.dun >= 5, { gold: 5 }], ['s30', 'Grimoire ouvert', 'Invoquer 30 pouvoirs', () => S.st.summon >= 30, { atk: 2 }], ['cp', 'Chef de troupe', 'Monter un compagnon niveau 10', () => Object.values(S.comps).some(c => c.lv >= 10), { pv: 2 }],
];
function achBonus() { const o = { atk: 0, pv: 0, gold: 0 }; for (const a of ACH) if (S.ach[a[0]]) for (const k in a[4]) o[k] += a[4][k]; return o; }
function achTick() { for (const a of ACH) if (!S.ach[a[0]] && a[3]()) { S.ach[a[0]] = 1; toast(`Succès : ${a[1]} !`); sfxPlay('reward'); save(); } }
const title = () => { const got = ACH.filter(a => S.ach[a[0]]); return got.length ? got[got.length - 1][1] : 'Recrue des cryptes'; };

// ================= quêtes infinies =================
const QT = [
  ['forge', n => `Forger ${n} objets`, 10], ['kill', n => `Tuer ${n} démons`, 60], ['equip', n => `Équiper ${n} objets`, 3], ['stage', n => `Terminer ${n} vagues`, 5],
  ['forgeLv', n => `Améliorer la forge ${n} fois`, 1], ['upgrade', n => `Améliorer ${n} objets`, 3], ['summon', n => `Invoquer ${n} pouvoirs`, 5], ['boss', n => `Vaincre ${n} boss`, 1],
  ['comp', n => `Monter des compagnons de ${n} niveaux`, 2], ['dun', n => `Réussir ${n} donjons`, 1],
];
const qCount = k => ({ forge: S.forged, kill: S.kills, equip: S.st.equip, stage: S.st.stage, forgeLv: S.st.forgeLv, upgrade: S.st.upg, summon: S.st.summon, boss: S.st.boss, comp: S.st.comp, dun: S.st.dun })[k];
function quest() { const t = QT[S.q % QT.length], round = Math.floor(S.q / QT.length), n = Math.max(1, Math.round(t[2] * (1 + round * 0.6))); return { k: t[0], txt: t[1](n), n, cur: Math.min(n, qCount(t[0]) - S.qStart) }; }
function qReward() { const r = S.q % 4; return r === 0 ? { ham: 15 + Math.floor(S.q / 4) * 2 } : r === 1 ? { gold: Math.round(200 * Math.pow(1.12, stageIndex())) } : r === 2 ? { pages: 10 + Math.floor(S.q / 8) * 2 } : (S.q % 8 === 3 ? { keys: 1 } : { ham: 25 }); }
const rewTxt = r => Object.entries(r).map(([k, v]) => `+${fmt(v)} ${{ ham: 'marteaux', gold: 'or', pages: 'pages', keys: v > 1 ? 'clés' : 'clé' }[k]}`).join(' · ');
function giveRew(r) { if (r.ham) S.ham += r.ham; if (r.gold) S.gold += r.gold; if (r.pages) S.pages += r.pages; if (r.keys) S.keys += r.keys; if (r.seals) SETK.forEach(k => S.seals[k] += r.seals); }
function claimQuest() { const q = quest(); if (q.cur < q.n) return; const r = qReward(); giveRew(r); toast(`Quête accomplie : ${rewTxt(r)}`); sfxPlay('reward'); S.q++; S.qStart = qCount(QT[S.q % QT.length][0]); save(); uiTop(); }
function uiQuest() { const q = quest(), done = q.cur >= q.n, el = $('questBar'); el.classList.toggle('done', done); $('qTxt').textContent = q.txt; $('qProg').textContent = `${fmt(q.cur)}/${fmt(q.n)}`; $('qFill').style.width = (q.cur / q.n * 100).toFixed(1) + '%'; $('qRew').textContent = done ? 'Récupérer !' : rewTxt(qReward()); }

// ================= auto-forge =================
let autoT = 0;
function autoForgeTick(dt) {
  if (!S.auto.on || S.ham <= 0 || !$('modal').hidden) return; autoT -= dt; if (autoT > 0) return; autoT = 0.45;
  S.ham--; S.forged++; const it = makeItem(), cur = S.eq[it.slot]; S.st.bestR = Math.max(S.st.bestR, it.r);
  if (S.auto.equip && (!cur || itemPower(it) > itemPower(cur))) { if (cur && (cur.set || cur.r >= S.auto.keep) && S.bag.length < BAG_MAX) S.bag.push(cur); else if (cur) S.gold += cur.v; S.eq[it.slot] = it; S.st.equip++; equipFx(it); num(CX, YF - 120, `${SLOTS.find(q => q.id === it.slot).n} équipé`, RAR[it.r].c, 1); B.gear = gear(); const st = heroStats(); B.hero.hpMax = st.pv; }
  else if (it.r >= S.auto.keep && S.bag.length < BAG_MAX) { S.bag.push(it); num(CX, YF - 120, `${RAR[it.r].n} gardé`, RAR[it.r].c, 1); }
  else S.gold += it.v;
  if (S.ham <= 0) { S.auto.on = false; toast('Auto-forge en pause : plus de marteaux'); }
  save(); if (tab === 'forge' && Math.random() < 0.5) ui(); else uiTop();
}

// ================= amélioration et fusion d'objets =================
const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r]);
function upgradeItem(it) { const c = upCost(it); if (S.gold < c) return false; S.gold -= c; const k = SCALE(it.L + 1) / SCALE(it.L); it.main = it.main.map(([st, v]) => [st, round2(FLAT[st] ? v * k : v * 1.04)]); it.subs = it.subs.map(([st, v]) => [st, round2(FLAT[st] ? v * k : v * 1.02)]); it.L++; it.v = Math.round(it.v * 1.1); S.st.upg++; sfxPlay('forge'); save(); return true; }
function autoFuse() {
  let made = 0; for (const sl of SLOTS) for (let r = 0; r < 6; r++) { let g; while ((g = S.bag.filter(x => x.slot === sl.id && x.r === r && !x.set)).length >= 3) { const three = g.slice(0, 3), L = Math.max(...three.map(x => x.L)); S.bag = S.bag.filter(x => !three.includes(x)); const it = makeItem(r + 1, sl); while (it.L < L) upgradeItemFree(it); S.bag.push(it); made++; S.st.fused++; S.st.bestR = Math.max(S.st.bestR, it.r); } }
  return made;
}
function upgradeItemFree(it) { const k = SCALE(it.L + 1) / SCALE(it.L); it.main = it.main.map(([st, v]) => [st, round2(FLAT[st] ? v * k : v * 1.04)]); it.subs = it.subs.map(([st, v]) => [st, round2(FLAT[st] ? v * k : v * 1.02)]); it.L++; }

// ================= gains hors ligne + connexion quotidienne =================
const LOGIN = [{ ham: 20 }, { gold: 1 }, { pages: 20 }, { keys: 2 }, { ham: 40 }, { gold: 3 }, { pages: 50, seals: 2 }];
function welcome(ham0) {
  const q = []; const away = S.lastSeen ? (Date.now() - S.lastSeen) / 1000 : 0;
  if (away > 120) { const sec = Math.min(away, 8 * 3600), n = stageIndex(), gps = 3 * Math.pow(1.11, n) * 0.5 * goldMul(), r = { gold: Math.round(gps * sec), pages: Math.floor(sec / 300) }, ham = S.ham - ham0, xp = sec * 0.4 * (1 + n * 0.25); q.push(() => offlineSheet(sec, r, ham, xp)); }
  const d = new Date().toDateString(); if (S.loginDay !== d) q.push(() => loginSheet(d));
  const next = () => { const f = q.shift(); if (f) f(next); }; WQ = next; next();
}
let WQ = null;
function offlineSheet(sec, r, ham, xp) {
  const h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60);
  sheet(`<h3>Pendant ton absence <button class="x" type="button" aria-label="Fermer">✕</button></h3><p style="margin:0 0 12px;color:var(--dim);font:700 13px/1.4 var(--b)">Le Chevalier a continué de farmer pendant ${h ? h + ' h ' : ''}${m} min${sec >= 8 * 3600 ? ' (maximum 8 h)' : ''}.</p>
  <div class="list"><div>${IC.star}<span>Or<b>+${fmt(r.gold)}</b></span></div><div>${IC.flame}<span>Pages<b>+${fmt(r.pages)}</b></span></div><div>${IC.sword}<span>Marteaux<b>+${fmt(Math.max(0, ham))}</b></span></div><div>${IC.heart}<span>Expérience<b>+${fmt(xp)}</b></span></div></div>
  <button class="btn gold" type="button" id="offB" style="width:100%;margin-top:14px">Récupérer</button>`);
  const go = () => { giveRew(r); gainXP(xp); sfxPlay('reward'); save(); $('modal').hidden = true; ui(); if (WQ) WQ(); };
  $('offB').onclick = go; $('mbox').querySelector('.x').onclick = go;
}
function loginSheet(d) {
  const day = S.loginStreak % 7, rw = LOGIN.map(r => r.gold ? Object.assign({}, r, { gold: Math.round(r.gold * 500 * Math.pow(1.12, stageIndex())) }) : r);
  sheet(`<h3>Récompense du jour <button class="x" type="button" aria-label="Fermer">✕</button></h3><div class="login">${rw.map((r, i) => `<div class="${i < day ? 'got' : i === day ? 'now' : ''}"><small>Jour ${i + 1}</small><b>${rewTxt(r).replace(/ · /g, '<br>')}</b>${i < day ? '<em>✓</em>' : ''}</div>`).join('')}</div>
  <button class="btn gold" type="button" id="logB" style="width:100%;margin-top:14px">Récupérer le jour ${day + 1}</button>`);
  const go = () => { giveRew(rw[day]); S.loginDay = d; S.loginStreak++; sfxPlay('reward'); save(); $('modal').hidden = true; ui(); if (WQ) WQ(); };
  $('logB').onclick = go; $('mbox').querySelector('.x').onclick = go;
}

// ================= pouvoirs (sorts automatiques) =================""")
rep("  B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1);", "  B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1); sfxPlay('spell');")
rep("if (B.walk.boss) { B.gate", "if (B.walk.boss) { B.gate", 0) if False else None
rep("if (w.t > 2.35 && !w.creak) { w.creak = 1; B.shake = 5; }", "if (w.t > 2.35 && !w.creak) { w.creak = 1; B.shake = 5; sfxPlay('door'); }")

# =================== interface ===================
# barre de quête sous le combat
rep('  <div id="botBar"><div id="spellHud"></div>', '  <button id="questBar" type="button"><i id="qFill"></i><span class="qi">📜</span><span class="qt"><b id="qTxt"></b><small id="qRew"></small></span><em id="qProg"></em></button>\n  <div id="botBar"><div id="spellHud"></div>')
rep("#botBar{flex:none;display:flex;", """#questBar{flex:none;position:relative;display:flex;align-items:center;gap:8px;padding:5px 12px;border:0;border-top:1.5px solid #4a2532;background:#160a10;color:var(--txt);text-align:left;overflow:hidden}
#questBar #qFill{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,#4a2a14,#6a3a14);transition:width .3s}
#questBar > *{position:relative}
#questBar .qi{font-size:16px}
#questBar .qt{flex:1;min-width:0;display:flex;flex-direction:column}
#questBar b{font:800 12.5px var(--b);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#questBar small{font:800 10px var(--b);color:var(--gold)}
#questBar em{font:400 14px var(--n);font-style:normal;color:var(--gold2)}
#questBar.done{animation:qpulse 1.2s infinite}#questBar.done #qFill{background:linear-gradient(90deg,#8a5a14,#c88a1a)}#questBar.done small{color:#fff}
@keyframes qpulse{50%{filter:brightness(1.35)}}
.login{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.login div{position:relative;padding:8px 4px;border-radius:10px;text-align:center;background:#ffffff06;border:1.5px solid #ffffff14}
.login small{display:block;font:800 10px var(--b);color:var(--dim)}.login b{font:400 12px/1.3 var(--n);color:var(--gold2)}
.login .now{border-color:var(--gold);box-shadow:0 0 12px -3px var(--gold)}.login .got{opacity:.5}.login em{position:absolute;top:2px;right:6px;font-style:normal;color:#5ae07a}
.tal{display:grid;grid-template-columns:1fr auto;gap:6px 10px;align-items:center;padding:8px 10px;border-radius:10px;background:#ffffff06;border:1px solid #ffffff10;margin-top:6px}
.tal b{font:800 13px var(--b)}.tal small{display:block;font:700 11px var(--b);color:var(--dim)}.tal .bar{grid-column:1/-1;height:5px;border-radius:3px;background:#ffffff10;overflow:hidden}.tal .bar i{display:block;height:100%;background:linear-gradient(90deg,#c88a1a,#ffe39a)}
.tal .btn{min-height:36px;padding:2px 12px;font-size:14px}
.xpbar{height:10px;border-radius:5px;background:#ffffff10;overflow:hidden;margin:6px 0 2px}.xpbar i{display:block;height:100%;background:linear-gradient(90deg,#5a3aa8,#a07aff)}
.pets{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.pet{display:flex;align-items:center;gap:8px;padding:8px;border-radius:12px;border:1.5px solid #ffffff14;background:#ffffff06;cursor:pointer}
.pet.on{border-color:var(--gold);box-shadow:0 0 12px -4px var(--gold)}.pet.lock{filter:grayscale(1) brightness(.5)}
.pet canvas{width:48px;height:48px;image-rendering:pixelated}.pet b{display:block;font:900 13px var(--t);color:var(--gold2)}.pet small{display:block;font:700 11px var(--b);color:var(--dim)}
.achs{display:grid;gap:5px}.ach{display:flex;justify-content:space-between;gap:8px;padding:7px 10px;border-radius:9px;background:#ffffff05;border:1px solid #ffffff0c;font:700 12px var(--b);color:#7a6068}
.ach b{color:#9a8088}.ach.on{color:var(--txt);border-color:#c88a1a66;background:linear-gradient(90deg,#3a2410,transparent)}.ach.on b{color:var(--gold2)}.ach em{font-style:normal;color:#5ae07a;white-space:nowrap}
.autobox{margin-top:14px;padding:10px;border-radius:12px;background:#ffffff06;border:1.5px solid #6b3a2e}
#forgeBtn .autob{position:absolute;top:4px;right:8px;font:400 11px var(--n);padding:1px 7px;border-radius:8px;background:#3a1404;color:#ffd27a}
#botBar{flex:none;display:flex;""")
rep('$("questBar")', '$("questBar")', 0) if False else None
rep("$('forgeBtn').onclick = forge;", "$('forgeBtn').onclick = forge; $('questBar').onclick = claimQuest;")
rep("draw(clock); heroPortrait(clock); if (uiT <= 0) { uiT = 0.5; uiTop(); } uiWave(); uiCombat();", "draw(clock); heroPortrait(clock); if (uiT <= 0) { uiT = 0.5; uiTop(); achTick(); } uiWave(); uiCombat(); uiQuest(); autoForgeTick(dt);")
# badge AUTO sur le bouton forger
rep("$('flv').textContent = S.forge;", "$('flv').textContent = S.forge; { let ab = $('forgeBtn').querySelector('.autob'); if (S.auto.on && !ab) { ab = document.createElement('span'); ab.className = 'autob'; ab.textContent = 'AUTO'; $('forgeBtn').appendChild(ab); } else if (!S.auto.on && ab) ab.remove(); }")
# réglages auto-forge dans la fiche de la forge
rep("  $('upB').onclick = () => { upForge(); showForge(); };\n}", """  $('mbox').insertAdjacentHTML('beforeend', `<div class="autobox"><h3 style="margin-bottom:6px">Auto-forge</h3><p style="margin:0 0 8px;color:var(--dim);font:700 12px/1.4 var(--b)">Forge toute seule tant qu'il reste des marteaux. Équipe ce qui est meilleur, garde la rareté choisie, vend le reste.</p>
  <div class="lbl2">Garder dans le sac à partir de</div><div class="seg">${[2, 3, 4, 5].map(r => `<button type="button" data-keep="${r}" class="${S.auto.keep === r ? 'on' : ''}" style="color:${S.auto.keep === r ? '#fff' : RAR[r].c}">${RAR[r].n}</button>`).join('')}</div>
  <div class="row"><button class="btn ${S.auto.equip ? 'gold' : ''}" type="button" id="aEq" style="flex:1">Équiper le meilleur<small>${S.auto.equip ? 'oui' : 'non'}</small></button><button class="btn ${S.auto.on ? 'red' : 'gold'}" type="button" id="aOn" style="flex:1.2">${S.auto.on ? 'Arrêter' : 'Lancer'}<small>${S.ham} marteaux</small></button></div></div>`);
  $('mbox').querySelectorAll('[data-keep]').forEach(b => b.onclick = () => { S.auto.keep = +b.dataset.keep; save(); showForge(); });
  $('aEq').onclick = () => { S.auto.equip = !S.auto.equip; save(); showForge(); };
  $('aOn').onclick = () => { S.auto.on = !S.auto.on; save(); closeM(); toast(S.auto.on ? 'Auto-forge lancée' : 'Auto-forge arrêtée'); };
  $('upB').onclick = () => { upForge(); showForge(); };
}""")
# améliorer un objet + fusion
rep("""    <div class="row" style="margin-top:14px"><button class="btn" id="unB" type="button" style="flex:1">Retirer<small>vers le sac</small></button>""",
    """    <button class="btn gold" id="upI" type="button" style="width:100%;margin-top:12px" ${S.gold < upCost(it) ? 'disabled' : ''}>Améliorer au niveau ${it.L + 1}<small>${fmt(upCost(it))} or · tu as ${fmt(S.gold)}</small></button>
    <div class="row" style="margin-top:10px"><button class="btn" id="unB" type="button" style="flex:1">Retirer<small>vers le sac</small></button>""")
rep("    $('altB').onclick = () => openBag(it.slot);", "    $('upI').onclick = () => { if (upgradeItem(it)) { B.gear = gear(); showItem(it, null); } };\n    $('altB').onclick = () => openBag(it.slot);")
rep("""  <button class="btn" id="sellW" type="button" style="width:100%;margin-top:12px" ${worse.length ? '' : 'disabled'}>""", """  <button class="btn gold" id="fuseB" type="button" style="width:100%;margin-top:12px">Fusion auto<small>3 objets identiques (emplacement + rareté) → 1 de rareté supérieure</small></button>
  <button class="btn" id="sellW" type="button" style="width:100%;margin-top:8px" ${worse.length ? '' : 'disabled'}>""")
rep("  $('sellW').onclick = () => {", "  $('fuseB').onclick = () => { const n = autoFuse(); save(); openBag(); toast(n ? `${n} fusion${n > 1 ? 's' : ''} réussie${n > 1 ? 's' : ''} !` : 'Rien à fusionner (il faut 3 objets du même emplacement et de même rareté)'); if (n) sfxPlay('forge'); };\n  $('sellW').onclick = () => {")
# bouton son
rep('      <button id="mapBtn"', '      <button id="sndBtn" type="button" aria-label="Son"></button>\n      <button id="mapBtn"')
rep("#mapBtn{", "#sndBtn{width:32px;height:32px;border-radius:50%;border:1.5px solid #5a3040;background:linear-gradient(#2a1520,#12080d);color:var(--gold);display:grid;place-items:center;font-size:15px;padding:0}\n#mapBtn{")
rep("$('forgeBtn').onclick = forge;", "$('forgeBtn').onclick = forge; const sndIcon = () => $('sndBtn').innerHTML = S.snd ? '<svg class=\"i\" viewBox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M4 9h4l5-4v14l-5-4H4zM16 8.5a5 5 0 0 1 0 7l-1.4-1.4a3 3 0 0 0 0-4.2zM18.8 5.7a9 9 0 0 1 0 12.6l-1.4-1.4a7 7 0 0 0 0-9.8z\"/></svg>' : '<svg class=\"i\" viewBox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M4 9h4l5-4v14l-5-4H4zM16 9.4l1.4-1.4 2.1 2.1 2.1-2.1 1.4 1.4-2.1 2.1 2.1 2.1-1.4 1.4-2.1-2.1-2.1 2.1-1.4-1.4 2.1-2.1z\"/></svg>'; sndIcon(); $('sndBtn').onclick = () => { S.snd = !S.snd; save(); sndIcon(); if (S.snd) { audioInit(); music(true); } else music(false); };")

# onglet Héros : niveau, talents, familiers, succès
rep("""    ${Object.keys(setCounts()).length ? `<h3 style="margin-top:16px">Sets</h3>""", """    <h3 style="margin-top:16px">Niveau ${S.lvl} <span style="font:800 12px var(--b);color:var(--dim)">${S.tp} point${S.tp > 1 ? 's' : ''} de talent</span></h3><div class="xpbar"><i style="width:${(S.xp / xpNeed(S.lvl) * 100).toFixed(1)}%"></i></div><small style="font:700 11px var(--b);color:var(--dim)">${fmt(S.xp)} / ${fmt(xpNeed(S.lvl))} XP · titre : <b style="color:var(--gold2)">${title()}</b></small>
    ${Object.entries(TALENTS).map(([k, [n, d, ic]]) => `<div class="tal"><div><b>${IC[ic]} ${n} <span style="color:var(--gold2)">${S.tal[k]}/${TAL_MAX}</span></b><small>${d} par point</small></div><button class="btn gold" type="button" data-tal="${k}" ${S.tp < 1 || S.tal[k] >= TAL_MAX ? 'disabled' : ''}>+1</button><div class="bar"><i style="width:${S.tal[k] / TAL_MAX * 100}%"></i></div></div>`).join('')}
    <h3 style="margin-top:16px">Familier</h3><div class="pets">${Object.entries(PETS).map(([k, P0]) => { const open = S.c >= P0.unlock; return `<div class="pet ${S.pet === k ? 'on' : ''} ${open ? '' : 'lock'}" data-pet="${open ? k : ''}"><canvas data-pd="${P0.dem}" width="48" height="48"></canvas><div><b>${P0.n}</b><small>${open ? P0.d : 'Chapitre ' + P0.unlock}</small></div></div>`; }).join('')}</div>
    <h3 style="margin-top:16px">Succès · ${ACH.filter(a => S.ach[a[0]]).length}/${ACH.length}</h3><div class="achs">${ACH.map(a => `<div class="ach ${S.ach[a[0]] ? 'on' : ''}"><span><b>${a[1]}</b><br>${a[2]}</span><em>${Object.entries(a[4]).map(([k, v]) => `+${v} % ${{ atk: 'attaque', pv: 'PV', gold: 'or' }[k]}`).join('')}</em></div>`).join('')}</div>
    ${Object.keys(setCounts()).length ? `<h3 style="margin-top:16px">Sets</h3>""")
rep("    document.querySelectorAll('[data-rc]').forEach(", """    document.querySelectorAll('[data-tal]').forEach(b => b.onclick = () => { const k = b.dataset.tal; if (S.tp < 1 || S.tal[k] >= TAL_MAX) return; S.tp--; S.tal[k]++; save(); const st = heroStats(); B.hero.hpMax = st.pv; ui(); });
    document.querySelectorAll('[data-pet]').forEach(b => b.onclick = () => { const k = b.dataset.pet; if (!k) return; S.pet = S.pet === k ? null : k; save(); ui(); });
    document.querySelectorAll('[data-pd]').forEach(c => { const g = c.getContext('2d'), key = c.dataset.pd, A = ASSETS.DEM[key], im = IMG['D_' + key]; const R = A.anims.walk_S; g.imageSmoothingEnabled = false; const sc = 40 / Math.max(A.cw, A.ch) * 1.4; g.drawImage(im, 0, R[0] * A.ch, A.cw, A.ch, 24 - A.ax * sc, 46 - (A.ch - A.foot) * sc, A.cw * sc, A.ch * sc); });
    document.querySelectorAll('[data-rc]').forEach(""")

# démarrage : hors ligne + connexion du jour
rep("(function boot() { if (!ready()) return setTimeout(boot, 50); fit(); hamTick(); startWave(); ui(); requestAnimationFrame(frame); })();",
    "(function boot() { if (!ready()) return setTimeout(boot, 50); fit(); const ham0 = S.ham; hamTick(); startWave(); ui(); requestAnimationFrame(frame); setTimeout(() => welcome(ham0), 400); setTimeout(fit, 60); })();")
# admin
rep('<button class="btn" data-a="allcp" type="button">Tous les compagnons Nv 10</button>', '<button class="btn" data-a="allcp" type="button">Tous les compagnons Nv 10</button><button class="btn" data-a="lvl" type="button">+10 niveaux</button><button class="btn" data-a="qdone" type="button">Finir la quête</button><button class="btn" data-a="away" type="button">Simuler 3 h d\\\'absence</button><button class="btn" data-a="newday" type="button">Simuler un nouveau jour</button>')
rep("allcp: () => {", "lvl: () => { for (let i = 0; i < 10; i++) gainXP(xpNeed(S.lvl)); }, qdone: () => { const q = quest(); S.qStart -= q.n; }, away: () => { window.__noSave = true; S.lastSeen = Date.now() - 3 * 3600e3; try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { } location.reload(); return 'sheet'; }, newday: () => { S.loginDay = ''; welcome(S.ham); return 'sheet'; },\n    allcp: () => {")

open(P, 'w').write(s)
print('ok')
