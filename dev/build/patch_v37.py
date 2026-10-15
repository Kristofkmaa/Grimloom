P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v37.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
WB64 = open('/home/claude/grimloom/wingart/wings.b64').read()

# ============ données : ailes, plumes, raid, clés rechargeables ============
rep("function keyTick() { const d = new Date().toDateString(); if (S.keyDay !== d) { S.keyDay = d; S.keys = Math.max(S.keys, 3); } }",
r"""const KEY_MAX = 3, KEY_MS = 2 * 3600 * 1000; // clés des donjons de sets : comme les tickets
function keyTick() { const now = Date.now(); if (!S.keyT) S.keyT = now; if (S.keys >= KEY_MAX) { S.keyT = now; return; } const g = Math.floor((now - S.keyT) / KEY_MS); if (g > 0) { S.keys = Math.min(KEY_MAX, S.keys + g); S.keyT = S.keys >= KEY_MAX ? now : S.keyT + g * KEY_MS; } }
const keyLeft = () => S.keys >= KEY_MAX ? 0 : KEY_MS - (Date.now() - S.keyT);
// ================= ailes =================
const WINGS = {
  corbeau: { n: 'Ailes du Corbeau', row: 0, c: '#a070ff', st: r => `Critique +${(1.5 * r).toFixed(1)} %`, sp: r => `Toutes les 6 s, une nuée de corbeaux frappe 3 démons (${120 + 15 * r} % de l'attaque)` },
  os: { n: 'Ailes d\'Ossature', row: 1, c: '#e8dcb0', st: r => `Points de vie +${4 * r} %`, sp: r => `Renvoie ${20 + 3 * r} % des dégâts subis` },
  enfer: { n: 'Ailes Infernales', row: 2, c: '#ff6a2a', st: r => `Attaque +${3 * r} %`, sp: r => `Toutes les 5 s, 3 météores de feu (${150 + 20 * r} % de l'attaque)` },
  givre: { n: 'Ailes de Givre', row: 3, c: '#7ad8ff', st: r => `Vitesse d'attaque +${2 * r} %`, sp: r => `Tirs ralentissants · toutes les 10 s, gèle tous les démons ${(1 + 0.1 * r).toFixed(1)} s` },
  dechu: { n: 'Ailes du Déchu', row: 4, c: '#ffd27a', st: r => `Or gagné +${5 * r} %`, sp: r => `Régénère ${(0.3 + 0.05 * r).toFixed(2)} % des PV/s · une fois par vague, survit à un coup mortel` },
};
const WK = Object.keys(WINGS), WMAX = 10, wingUnlock = () => 40, wingCost = lv => 10 + lv * 8;
S.wings = S.wings || {}; if (S.wingEq === undefined) S.wingEq = null; if (S.plumes === undefined) S.plumes = 0;
const wlv = k => S.wings[k] || 0, wEq = () => (S.wingEq && wlv(S.wingEq) ? S.wingEq : null);
const WING_IMG = new Image(); WING_IMG.src = 'data:image/png;base64,WINGB64';
// ================= raid : l'Archidémon =================
const RAID_MAX = 2, RAID_DAY = () => new Date().toDateString();
S.raid = S.raid || { n: RAID_MAX, day: RAID_DAY(), best: 0 }; if (S.raid.day !== RAID_DAY()) { S.raid.day = RAID_DAY(); S.raid.n = RAID_MAX; }
const RNAMES = ['Morvane', 'Kael le Pâle', 'Sœur Ysolde', 'Brannoc', 'Vesper Cendre', 'Ilsa Corbeau', 'Thorne', 'Ulric le Brisé', 'Maelis', 'Osric Lamenoire', 'Edwyn', 'Sable', 'Garran', 'Lysandre', 'Dame Ombre'];
const RCLASS = { archere: 'Archère', mage: 'Mage de givre', sorcier: 'Sorcier', paladin: 'Paladin', seigneur: 'Seigneur noir' };
function raidAllies() { // 5 alliés proposés, renouvelés chaque jour
  let seed = 0; for (const ch of RAID_DAY()) seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const p = power(), names = RNAMES.slice(), cls = Object.keys(RCLASS);
  return [0, 1, 2, 3, 4].map(i => { const n = names.splice(Math.floor(rnd() * names.length), 1)[0], c = cls[i % cls.length], k = 0.55 + rnd() * 0.9; return { i, n, c, pw: Math.round(p * k), pct: Math.round(30 * k), rate: +(0.8 + rnd() * 0.8).toFixed(2), lv: Math.max(1, S.lvl + Math.round((rnd() - 0.4) * 6)) }; });
}
const RAID_TIERS = [1, 3, 6, 10, 16, 24, 35, 50, 70, 100];
function raidTier(dmg) { const u = dmg / Math.max(1, heroStats().atk * 12); let t = 0; while (t < RAID_TIERS.length && u >= RAID_TIERS[t]) t++; return t; }
let RSEL = [];
function keyTick0() {}""".replace('WINGB64', WB64))

# clé gagnée sur boss : plafonnée
rep("if (boss && !S.farm) { S.keys++; S.st.boss++;", "if (boss && !S.farm) { S.keys = Math.min(KEY_MAX + 2, S.keys + 1); S.st.boss++;")

# ============ effets des ailes ============
rep("  if (B.hero && B.hero.icT > 0) o.rate *= 0.75;", r"""  { const w = wEq(), r = w ? wlv(w) : 0;
    if (w === 'corbeau') { o.crit += 1.5 * r; o.ravens = 1.2 + 0.15 * r; }
    if (w === 'os') { o.pv *= 1 + 0.04 * r; o.thorns += 0.2 + 0.03 * r; }
    if (w === 'enfer') { o.atk *= 1 + 0.03 * r; o.wmet = 1.5 + 0.2 * r; }
    if (w === 'givre') { o.rate *= 1 + 0.02 * r; o.chill = true; o.wfrz = 1 + 0.1 * r; }
    if (w === 'dechu') { o.regen += 0.3 + 0.05 * r; o.undying = true; } }
  if (B.hero && B.hero.icT > 0) o.rate *= 0.75;""")
rep("const goldMul = () => (1 + 0.06 * tr('a_gold')", "const goldMul = () => (1 + 0.06 * tr('a_gold') + (wEq() === 'dechu' ? 0.05 * wlv('dechu') : 0)")
rep("  if (B.dun && !B.dun.end) { B.dun.t -= dt; if (B.dun.t <= 0) dunEnd(false, 'Temps écoulé'); }",
r"""  if (B.dun && !B.dun.end) { B.dun.t -= dt; if (B.dun.t <= 0) { if (B.dun.raid) dunEnd(true); else dunEnd(false, 'Temps écoulé'); } }
  if (fighting) { // ailes
    if (st.ravens) { B.rvT = (B.rvT || 3) - dt; if (B.rvT <= 0) { B.rvT = 6; const L = alive().sort(() => Math.random() - 0.5).slice(0, 3); for (const e of L) { const x = sx(e.X, e.z), y = py(e.z) - 30 * sOf(e.z); B.fx.push({ k: 'streak', x: CX + rand(-40, 40), y: YF - 120, x2: x, y2: y, t: 0, d: 0.3, c: '#a070ff' }); setTimeout(() => { if (!e.dead) { sfx('mort', x, y, 70 * sOf(e.z), 0.4); hitEnemy(e, st.atk * st.ravens, false); } }, 280); } } }
    if (st.wmet) { B.wmT = (B.wmT || 2.5) - dt; if (B.wmT <= 0) { B.wmT = 5; meteorShower(st.atk * st.wmet, 3); } }
    if (st.wfrz) { B.wfT = (B.wfT || 5) - dt; if (B.wfT <= 0) { B.wfT = 10; freezeAll(st.wfrz); } }
  }""")

# ============ dessin des ailes sur le chevalier ============
rep("  sprH(H.key, key, fr, CX, YF, sc);\n  if (B.shield > 0)", r"""  sprH(H.key, key, fr, CX, YF, sc);
  { const w = wEq(); if (w && WING_IMG.complete) { const seq = [0, 1, 2, 3, 2, 1], f = seq[Math.floor(time * (B.walk ? 9 : 5)) % 6], ws = 0.62 * sc / 1.5, wy = YF - heroTop(H.key) * sc * 0.72 + (anim === 'idle' ? Math.sin(time * 2.4) * 1.2 : 0), wx = CX + (di === 1 ? -4 : di === 3 ? 4 : 0);
    ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(WING_IMG, f * 168, WINGS[w].row * 168, 168, 168, wx - 84 * ws, wy - 48 * ws, 168 * ws, 168 * ws); ctx.restore();
    if (w === 'enfer' || w === 'givre' || w === 'dechu') { if (Math.random() < 0.3) B.fx.push({ k: 'p', x: wx + rand(-50, 50) * ws, y: wy + rand(-10, 60) * ws, vx: 0, vy: w === 'givre' ? 10 : -16, g: 0, c: WINGS[w].c, t: 0, d: 0.7, r: 1 }); } } }
  if (B.shield > 0)""")

# ============ raid : alliés qui tirent, boss géant ============
rep("const PARTY_X = [-0.34, 0.34];", "const PARTY_X = [-0.34, 0.34, -0.62];\nconst raidOn = () => B.dun && B.dun.raid;")
rep("function drawComp(i, time) {\n  const id = S.party[i]; if (!id || !S.comps[id]) return;", "function drawComp(i, time) {\n  const ra = raidOn() ? B.dun.allies[i] : null, id = ra ? ra.c : i < 2 ? S.party[i] : null; if (!id || (!ra && !S.comps[id])) return;")
rep("    B.cs = B.cs || []; for (let i = 0; i < 2; i++) { const id = S.party[i]; if (!id || !S.comps[id]) continue; const cs = B.cs[i] = B.cs[i] || { cd: rand(0.2, 0.8) }; cs.cd -= dt; cs.shootT = (cs.shootT || 0) - dt; if (!B.walk && cs.cd <= 0) { compFire(id, i); cs.cd = 1 / compRate(id); } }",
r"""    B.cs = B.cs || []; if (raidOn()) { B.dun.allies.forEach((a, i) => { const cs = B.cs[i] = B.cs[i] || { cd: rand(0.2, 0.8) }; cs.cd -= dt; cs.shootT = (cs.shootT || 0) - dt; if (cs.cd <= 0) { const t = alive()[0]; if (t) { const H0 = HEROES[a.c]; B.shots.push({ X: PARTY_X[i], z: 0.0, h: 30, tg: t, dmg: st.atk * a.pct / 100 * rand(0.9, 1.1), crit: false, t: 0, fx: H0.fx, solid: H0.solid, wr: -1 }); cs.shootT = 0.3; cs.face = Math.atan2(-(py(t.z) - YF), sx(t.X, t.z) - (CX + PARTY_X[i] * HW)); } cs.cd = 1 / a.rate; } }); }
    else for (let i = 0; i < 2; i++) { const id = S.party[i]; if (!id || !S.comps[id]) continue; const cs = B.cs[i] = B.cs[i] || { cd: rand(0.2, 0.8) }; cs.cd -= dt; cs.shootT = (cs.shootT || 0) - dt; if (!B.walk && cs.cd <= 0) { compFire(id, i); cs.cd = 1 / compRate(id); } }""")
rep("L.push({ z: -0.02, f: () => { drawComp(0, time); drawComp(1, time); } });", "L.push({ z: -0.02, f: () => { drawComp(0, time); drawComp(1, time); if (raidOn()) drawComp(2, time); } });")
rep("sc = (e.boss ? 2.3 : e.elite ? 1.75 : 1.55) * s;", "sc = (e.raid ? 3.1 : e.boss ? 2.3 : e.elite ? 1.75 : 1.55) * s;")
rep("function startDunWave() {\n  const D = B.dun,", r"""function startRaid() {
  if (B.dun) return; if (S.raid.n < 1) { toast('Plus d\'essais aujourd\'hui : ils reviennent demain'); return; } if (RSEL.length !== 3) { toast('Choisis 3 alliés'); return; }
  const AL = raidAllies(); tab = 'forge'; document.querySelectorAll('#nav button').forEach(x => x.classList.toggle('on', x.dataset.t === 'forge'));
  B.dun = { k: 'raid', lv: 1, w: 0, t: 30, raid: true, allies: RSEL.map(i => AL[i]) }; B.cs = []; B.walk = null; B.pend = 0; B.pendFn = null; B.scene = 'arena'; B.scroll = 0; B.fade = 1; closeM(); startWave();
}
function startDunWave() {
  if (B.dun.raid) { const D = B.dun; B.bi = 6; B.scene = 'arena'; placeDeco(); B.en = []; B.es = []; B.shots = [];
    B.wave = { n: stageIndex(), boss: true, left: 0, spawnT: 99, total: 1, killed: 0, dun: true };
    const st = enemyStats(stageIndex(), true); st.hp = 1e18; st.atk *= 0.6; spawnEnemy('beast4', 0, 0.9, st, true, 'void'); B.en[0].raid = 1; B.en[0].spd = 0.05;
    const H = heroStats(); B.hero.hpMax = H.pv; B.hero.hp = H.pv; B.hero.dead = 0; B.hero.reported = 0; B.hero.saved = 0; B.dmg = []; B.waveDmg = 0; B.cd = {}; B.banner = { a: 'L\'Archidémon', b: 'Inflige un maximum de dégâts en 30 s', t: 2 }; queueBiome(6); ui(); return; }
  const D = B.dun,""")
rep("  const D = B.dun; if (!D || D.end) return; D.end = true; B.en.forEach(e => { if (!e.dead) e.frozen = 99; });",
r"""  const D = B.dun; if (!D || D.end) return; D.end = true; B.en.forEach(e => { if (!e.dead) e.frozen = 99; });
  if (D.raid) { const dmg = B.waveDmg, t = raidTier(dmg), pl = 6 + t * 6; S.raid.n--; S.raid.best = Math.max(S.raid.best || 0, dmg); S.plumes += pl; S.st.dun++; B.banner = { a: `Palier ${t} / ${RAID_TIERS.length}`, b: `${fmt(dmg)} dégâts · +${pl} plumes`, t: 2.8 }; save(); setTimeout(() => { B.dun = null; B.scene = 'x'; B.fade = 1; B.hero.dead = 0; B.cs = []; startWave(); ui(); }, 2800); return; }""")
rep("$('biomeN').textContent = `${dunName(B.dun.k)} · niveau ${B.dun.lv}`;", "$('biomeN').textContent = B.dun.raid ? `Raid · ${fmt(B.waveDmg)} dégâts` : `${dunName(B.dun.k)} · niveau ${B.dun.lv}`;")
rep("if (B.dun) { const D = B.dun; $('waveBox').classList.add('boss'); $('waveBar').style.width = (Math.max(0, D.t) / 60 * 100).toFixed(1) + '%'; $('waveTxt').textContent = D.end ? '' : `${D.w < 3 ? `Vague ${D.w + 1}/3` : 'Boss'} · ${Math.ceil(Math.max(0, D.t))} s`; return; }",
    "if (B.dun) { const D = B.dun; $('waveBox').classList.add('boss'); $('waveBar').style.width = (Math.max(0, D.t) / (D.raid ? 30 : 60) * 100).toFixed(1) + '%'; $('waveTxt').textContent = D.end ? '' : D.raid ? `Archidémon · ${fmt(B.waveDmg)} · ${Math.ceil(Math.max(0, D.t))} s` : `${D.w < 3 ? `Vague ${D.w + 1}/3` : 'Boss'} · ${Math.ceil(Math.max(0, D.t))} s`; return; }")
rep("function heroDied() { if (B.dun) { dunEnd(false, 'Le héros est à terre'); return; }", "function heroDied() { if (B.dun) { if (B.dun.raid) dunEnd(true); else dunEnd(false, 'Le héros est à terre'); return; }")

# ============ page Donjons : onglets Ressources / Sets / Raid ============
rep("[['res', 'Ressources'], ['sets', 'Sets']], 'data-dtab')}<p class=\"knote\"", "[['res', 'Ressources'], ['sets', 'Sets'], ['raid', 'Raid']], 'data-dtab')}<p class=\"knote\"")
rep("[['res', 'Ressources'], ['sets', 'Sets']], 'data-dtab')}", "[['res', 'Ressources'], ['sets', 'Sets'], ['raid', 'Raid']], 'data-dtab')}")
rep("function dunHTML() {\n  if (DTAB === 'res') return rdHTML();", r"""function raidHTML() {
  const AL = raidAllies(), best = S.raid.best || 0;
  return `<div class="kp">${ktabs(DTAB, [['res', 'Ressources'], ['sets', 'Sets'], ['raid', 'Raid']], 'data-dtab')}
  <div class="kban kg kbt raidban"><div class="kbig"><b>${S.raid.n}</b><small>essai${S.raid.n > 1 ? 's' : ''}</small></div><div class="kbi"><b class="kname" style="color:#c070ff">L'Archidémon</b><small class="kdim">Un boss immortel. Inflige un maximum de dégâts en 30 s avec 3 alliés. Chaque palier atteint donne des plumes pour les ailes.</small><small class="kdim">${RAID_MAX} essais par jour · record : <b style="color:#ffd890">${fmt(best)}</b> (palier ${raidTier(best)})</small></div></div>
  <h4 class="kh">Choisis 3 alliés <small>${RSEL.length} / 3 · nouveaux alliés chaque jour</small></h4>
  ${AL.map(a => `<button type="button" class="kt krow ally ${RSEL.includes(a.i) ? 'gd' : ''}" data-ally="${a.i}"><canvas data-hc="${a.c}" width="72" height="72"></canvas><div class="kri"><b>${a.n}</b><small>${RCLASS[a.c]} · niveau ${a.lv}</small><small class="kdim">${a.pct} % de ton attaque · ${a.rate} tirs/s</small></div><div class="krb"><em class="kbadge ${RSEL.includes(a.i) ? '' : 'dim'}">${fmt(a.pw)}</em><small class="kdim" style="font-size:9.5px">puissance</small></div></button>`).join('')}
  <div class="kl" style="margin-top:6px"><div class="rtiers">${RAID_TIERS.map((u, i) => `<i class="${raidTier(best) > i ? 'on' : ''}" title="Palier ${i + 1}"><b>${i + 1}</b></i>`).join('')}</div><p class="knote" style="margin:6px 0 10px">Palier ${raidTier(best)} atteint · chaque palier ajoute 6 plumes (6 de base). Tu as <b style="color:#ffd890">${S.plumes} plumes</b>.</p><button class="btn gold" id="raidGo" type="button" style="width:100%" ${S.raid.n < 1 || RSEL.length !== 3 || B.dun ? 'disabled' : ''}>${S.raid.n < 1 ? 'Reviens demain' : RSEL.length !== 3 ? 'Choisis 3 alliés' : 'Affronter l\'Archidémon'}</button></div></div>`;
}
function dunHTML() {
  if (DTAB === 'res') return rdHTML();
  if (DTAB === 'raid') return raidHTML();""")
rep("    document.querySelectorAll('[data-dtab]').forEach(b => b.onclick = () => { DTAB = b.dataset.dtab; ui(); });",
r"""    document.querySelectorAll('[data-dtab]').forEach(b => b.onclick = () => { DTAB = b.dataset.dtab; ui(); });
    document.querySelectorAll('[data-ally]').forEach(b => b.onclick = () => { const i = +b.dataset.ally, j = RSEL.indexOf(i); if (j >= 0) RSEL.splice(j, 1); else if (RSEL.length < 3) RSEL.push(i); else { RSEL.shift(); RSEL.push(i); } const y = $('panel').scrollTop; ui(); $('panel').scrollTop = y; });
    if ($('raidGo')) $('raidGo').onclick = startRaid;
    document.querySelectorAll('[data-hc]').forEach(c => { const H = HEROES[c.dataset.hc], g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, 72, 72); sprH(H.key, 'idle_6', performance.now() / 80, 36, 70, H.sc * 0.62, 1, g); requestAnimationFrame(draw); }; draw(); });
    document.querySelectorAll('[data-ssw]').forEach(b => b.onclick = () => { const k = b.dataset.ssw, lv = S.dlv[k] - 1; if (lv < 1 || S.keys < 1) return; if (S.keys >= KEY_MAX) S.keyT = Date.now(); S.keys--; const r = dunReward(lv); S.seals[k] += r; S.st.dun++; save(); sfxPlay('reward'); toast(`Balayage : +${r} Sceaux · ${SETS[k].n}`); ui(); });""")
# sets : balayage + texte des clés
rep("<small class=\"kdim\">3 clés par jour · +1 par boss · perdue seulement si tu gagnes</small></div></div>\n  <div class=\"wmap\">", "<small class=\"kdim\">${KEY_MAX} clés max · +1 toutes les 2 h <span data-kt>${S.keys >= KEY_MAX ? '(plein)' : '(+1 dans ' + hms(keyLeft()) + ')'}</span> · +1 par boss</small></div></div>\n  <div class=\"wmap\">")
rep("<div class=\"kdb\"><span>Récompense<br><b>${dunReward(S.dlv[k])} Sceaux</b></span><button class=\"btn gold\" type=\"button\" data-dun=\"${k}\" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div>",
    "<div class=\"kdb\"><span>Récompense<br><b>${dunReward(S.dlv[k])} Sceaux</b></span></div><div class=\"row rdb\" style=\"margin-top:8px\"><button class=\"btn\" type=\"button\" data-ssw=\"${k}\" ${S.dlv[k] < 2 || S.keys < 1 || B.dun ? 'disabled' : ''}>Balayer<small>${S.dlv[k] < 2 ? 'bats le niveau 1' : 'niv. ' + (S.dlv[k] - 1) + ' · +' + dunReward(S.dlv[k] - 1) + ' Sceaux'}</small></button><button class=\"btn gold\" type=\"button\" data-dun=\"${k}\" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Combattre<small>niveau ${S.dlv[k]}</small></button></div>")
rep("  document.querySelectorAll('[data-rt]').forEach(el =>", "  document.querySelectorAll('[data-kt]').forEach(el => { el.textContent = S.keys >= KEY_MAX ? '(plein)' : '(+1 dans ' + hms(keyLeft()) + ')'; });\n  document.querySelectorAll('[data-rt]').forEach(el =>")
rep("if (S.keys < 1) { toast('Plus de clés : 3 reviennent chaque jour, +1 par boss de chapitre'); return; }", "if (S.keys < 1) { toast(`Plus de clés : +1 dans ${hms(keyLeft())}`); return; }")

# ============ Héros : sous-onglet Ailes ============
rep("[['profil', 'Profil'], ['comp', 'Troupe'], ['pet', 'Familier'], ['ach', 'Succès']], 'data-hs')", "[['profil', 'Profil'], ['wing', 'Ailes'], ['comp', 'Troupe'], ['pet', 'Familier'], ['ach', 'Succès']], 'data-hs')")
rep("    } else if (HSUB === 'pet') {", r"""    } else if (HSUB === 'wing') {
      body = `<div class="kl kachp"><b style="color:#ffd890">${S.plumes} plumes</b><small>Gagne des plumes en affrontant l'Archidémon (Donjons › Raid). Débloque des ailes, monte-les de niveau, et équipe-en une : elle apparaît sur le dos du chevalier.</small></div>
      ${WK.map(k => { const W0 = WINGS[k], r = wlv(k), eq = S.wingEq === k && r; return `<div class="kt krow wrow ${eq ? 'gd' : ''} ${r ? '' : 'lock'}"><canvas data-wg="${k}" width="96" height="72"></canvas><div class="kri"><b style="color:${W0.c}">${W0.n}${r ? ` <em class="kbadge" style="margin-left:4px">Nv ${r}</em>` : ''}</b><small>${W0.st(Math.max(1, r))}</small><small class="kdim">${W0.sp(Math.max(1, r))}</small></div><div class="krb">${r ? `<button class="btn sm ${eq ? 'red' : 'gold'}" type="button" data-weq="${k}">${eq ? 'Retirer' : 'Équiper'}</button><button class="btn sm" type="button" data-wup="${k}" ${r >= WMAX || S.plumes < wingCost(r) ? 'disabled' : ''}>${r >= WMAX ? 'Max' : 'Nv +1'}<small>${r >= WMAX ? '' : wingCost(r) + ' plumes'}</small></button>` : `<button class="btn gold sm" type="button" data-wun="${k}" ${S.plumes < wingUnlock() ? 'disabled' : ''}>Débloquer<small>${wingUnlock()} plumes</small></button>`}</div></div>`; }).join('')}`;
    } else if (HSUB === 'pet') {""")
rep("    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });", r"""    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });
    document.querySelectorAll('[data-wg]').forEach(c => { const W0 = WINGS[c.dataset.wg], g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, 96, 72); if (WING_IMG.complete) { const f = [0, 1, 2, 3, 2, 1][Math.floor(performance.now() / 190) % 6]; g.imageSmoothingEnabled = false; g.drawImage(WING_IMG, f * 168, W0.row * 168, 168, 130, 0, 0, 96, 74); } requestAnimationFrame(draw); }; draw(); });
    const keepY = () => { const y = $('panel').scrollTop; ui(); $('panel').scrollTop = y; };
    document.querySelectorAll('[data-wun]').forEach(b => b.onclick = () => { const k = b.dataset.wun; if (S.plumes < wingUnlock()) return; S.plumes -= wingUnlock(); S.wings[k] = 1; if (!wEq()) S.wingEq = k; save(); sfxPlay('reward'); toast(`${WINGS[k].n} débloquées !`); const st = heroStats(); B.hero.hpMax = st.pv; keepY(); });
    document.querySelectorAll('[data-wup]').forEach(b => b.onclick = () => { const k = b.dataset.wup, c = wingCost(wlv(k)); if (S.plumes < c || wlv(k) >= WMAX) return; S.plumes -= c; S.wings[k]++; save(); const st = heroStats(); B.hero.hpMax = st.pv; keepY(); });
    document.querySelectorAll('[data-weq]').forEach(b => b.onclick = () => { const k = b.dataset.weq; S.wingEq = S.wingEq === k ? null : k; save(); const st = heroStats(); B.hero.hpMax = st.pv; keepY(); });""")

# ============ divers : admin, aide ============
rep("tickets: () => { RDK.forEach(k => { S.rt[k] = { n: RT_MAX, t: Date.now() }; }); },", "tickets: () => { RDK.forEach(k => { S.rt[k] = { n: RT_MAX, t: Date.now() }; }); S.keys = KEY_MAX; S.raid.n = RAID_MAX; },\n    plumes: () => { S.plumes += 500; },")
s = s.replace('<button class="btn gold" data-a="tickets" type="button">Tickets pleins</button>', '<button class="btn gold" data-a="tickets" type="button">Tickets, clés et raid pleins</button><button class="btn gold" data-a="plumes" type="button">+500 plumes</button>', 1)
rep("'Clés', '3 par jour, +1 par boss de chapitre, certaines quêtes.'", "'Clés', '3 maximum, +1 toutes les 2 h, +1 par boss de chapitre, certaines quêtes.'")
rep("  ['#ff4a5a', IC.shield, 'Sceaux',", "  ['#c070ff', IC.star, 'Plumes', 'Affronter l\\'Archidémon (Donjons › Raid), 2 essais par jour. Plus tu infliges de dégâts, plus tu en gagnes.', 'Débloquer et améliorer les ailes (Héros › Ailes), qui apparaissent sur le chevalier et ont un effet unique.'],\n  ['#ff4a5a', IC.shield, 'Sceaux',")

s = s.replace("</style>", r"""
.wrow canvas{width:80px!important;height:60px!important;image-rendering:pixelated}
.wrow .krb .btn{min-width:84px}
.ally{width:100%}
.ally.gd{box-shadow:0 0 0 1px #ffd27a55}
.raidban .kbig b{color:#c070ff}
.rtiers{display:grid;grid-template-columns:repeat(10,1fr);gap:4px}
.rtiers i{height:26px;border-radius:5px;display:grid;place-items:center;background:#1a1012;border:1px solid #4a3828;font-style:normal}
.rtiers i b{font:400 11px var(--n);color:#8a7868}
.rtiers i.on{background:linear-gradient(#a060ff,#4a1a8a);border-color:#d8b0ff}.rtiers i.on b{color:#fff}
.ktabs .ktab{font-size:10.5px}
</style>""", 1)
open(P, 'w').write(s); print('ok')
