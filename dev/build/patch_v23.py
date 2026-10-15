P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v23.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# ---------- données de l'arbre ----------
rep("const TAL_MAX = 25;", r"""const TAL_MAX = 25;
// ================= arbre de talents =================
const TREE = {
  carnage: { n: 'Carnage', c: '#ff4a5a', d: 'Attaque', tiers: [['c_atk'], ['c_crit', 'c_rate'], ['c_boss'], ['c_cdmg', 'c_exec'], ['c_multi'], ['c_double']] },
  rempart: { n: 'Rempart', c: '#5ab0ff', d: 'Survie', tiers: [['r_pv'], ['r_def', 'r_regen'], ['r_leech'], ['r_esq', 'r_thorns'], ['r_shield'], ['r_undying']] },
  avarice: { n: 'Avarice', c: '#ffc23a', d: 'Forge et butin', tiers: [['a_gold'], ['a_shard', 'a_xp'], ['a_ham'], ['a_luck', 'a_up'], ['a_comp'], ['a_twin']] },
};
const NODE = {
  c_atk: ['Lame affûtée', 5, 'sword', r => `Attaque +${3 * r} %`], c_crit: ['Œil du boucher', 5, 'star', r => `Critique +${r} %`], c_rate: ['Frénésie', 5, 'wind', r => `Vitesse d'attaque +${3 * r} %`],
  c_boss: ['Tueur de titans', 3, 'skull', r => `Dégâts aux boss et élites +${8 * r} %`], c_cdmg: ['Coup fatal', 5, 'star', r => `Dégâts critiques +${8 * r} %`], c_exec: ['Exécution', 5, 'sword', r => `+${6 * r} % de dégâts aux démons sous 30 % de PV`],
  c_multi: ['Tir fourchu', 3, 'bolt', r => `${5 * r} % de chances de tirer un projectile en plus`], c_double: ['Rafale maudite', 1, 'bolt', () => 'Un tir sur trois se dédouble'],
  r_pv: ['Chair de pierre', 5, 'heart', r => `Points de vie +${4 * r} %`], r_def: ['Carapace', 5, 'shield', r => `Dégâts subis −${1.5 * r} %`], r_regen: ['Sang noir', 5, 'heart', r => `Régénère ${(0.3 * r).toFixed(1)} % des PV par seconde`],
  r_leech: ['Sangsue', 3, 'drop', r => `Vol de vie +${r} %`], r_esq: ['Ombre fuyante', 5, 'wind', r => `Esquive +${1.5 * r} %`], r_thorns: ['Épines', 5, 'shield', r => `Renvoie ${20 * r} % des dégâts subis`],
  r_shield: ['Égide', 3, 'shield', r => `Bouclier de ${5 * r} % des PV au début de chaque vague`], r_undying: ['Indomptable', 1, 'heart', () => 'Une fois par vague, survit à un coup mortel avec 30 % de PV'],
  a_gold: ['Cupidité', 5, 'drop', r => `Or gagné +${6 * r} %`], a_shard: ['Récupérateur', 5, 'gem', r => `Éclats de recyclage +${10 * r} %`], a_xp: ['Érudit', 5, 'star', r => `Expérience +${8 * r} %`],
  a_ham: ['Forgeron infatigable', 3, 'ham', r => `Marteaux régénérés ${8 * r} % plus vite`], a_luck: ['Main bénie', 5, 'star', r => `Chances de rareté comme une forge +${(0.6 * r).toFixed(1)} niveau`], a_up: ['Économe', 5, 'drop', r => `Améliorations ${5 * r} % moins chères`],
  a_comp: ['Chef de meute', 3, 'sword', r => `Dégâts des compagnons +${10 * r} %`], a_twin: ['Marteau béni', 1, 'ham', () => '10 % de chances qu\'une forge ne consomme pas de marteau'],
};
const TIER_REQ = 4; // points dépensés dans la branche pour débloquer le palier suivant
const tr = k => (S.tree && S.tree[k]) || 0;
const branchSpent = b => TREE[b].tiers.flat().reduce((a, k) => a + tr(k), 0);
const nodeBranch = k => Object.keys(TREE).find(b => TREE[b].tiers.flat().includes(k));
const nodeTier = k => TREE[nodeBranch(k)].tiers.findIndex(t => t.includes(k));
const nodeOpen = k => branchSpent(nodeBranch(k)) >= nodeTier(k) * TIER_REQ;
const treeSpent = () => Object.keys(TREE).reduce((a, b) => a + branchSpent(b), 0);
const resetCost = () => Math.round(80 * Math.pow(S.lvl, 1.6));""")

# migration : les anciens points de talent sont rendus
rep("S.tal = Object.assign({ force: 0, vit: 0, prec: 0, brut: 0, cel: 0, avar: 0 }, S.tal || {});",
    "S.tal = Object.assign({ force: 0, vit: 0, prec: 0, brut: 0, cel: 0, avar: 0 }, S.tal || {}); if (!S.tree) { S.tree = {}; const old = Object.values(S.tal).reduce((a, b) => a + b, 0); S.tp += old; Object.keys(S.tal).forEach(k => S.tal[k] = 0); }")

# ---------- effets ----------
rep("  o.atk *= (1 + 0.03 * T.force + A.atk / 100) * (PT === 'braise' ? 1.06 : 1); o.pv *= 1 + 0.04 * T.vit + A.pv / 100; o.crit += 0.5 * T.prec; o.cdmg += 5 * T.brut + (PT === 'griffe' ? 10 : 0); o.rate *= 1 + 0.02 * T.cel; if (PT === 'sangsue') o.vol += 2;",
    """  o.atk *= (1 + 0.03 * tr('c_atk') + A.atk / 100) * (PT === 'braise' ? 1.06 : 1); o.pv *= 1 + 0.04 * tr('r_pv') + A.pv / 100; o.crit += tr('c_crit'); o.cdmg += 8 * tr('c_cdmg') + (PT === 'griffe' ? 10 : 0); o.rate *= 1 + 0.03 * tr('c_rate'); if (PT === 'sangsue') o.vol += 2;
  o.bigDmg += 0.08 * tr('c_boss'); o.exec = 0.06 * tr('c_exec'); o.multi = 0.05 * tr('c_multi'); o.dbl = tr('c_double') > 0;
  o.dmgRed = Math.min(0.6, o.dmgRed + 0.015 * tr('r_def')); o.regen += 0.3 * tr('r_regen'); o.vol += tr('r_leech'); o.esq = Math.min(45, o.esq + 1.5 * tr('r_esq')); o.thorns += 0.05 * tr('r_thorns'); o.undying = tr('r_undying') > 0;""")
rep("const goldMul = () => (1 + 0.05 * S.tal.avar + achBonus().gold / 100) * (S.pet === 'ombre' ? 1.08 : 1);",
    "const goldMul = () => (1 + 0.06 * tr('a_gold') + achBonus().gold / 100) * (S.pet === 'ombre' ? 1.08 : 1);")
rep("const shardsOf = it => Math.round(SHARDV[it.r] * (1 + (it.L - 1) * 0.15));", "const shardsOf = it => Math.round(SHARDV[it.r] * (1 + (it.L - 1) * 0.15) * (1 + 0.1 * tr('a_shard')));")
rep("function gainXP(x) { S.xp += x;", "function gainXP(x) { x *= 1 + 0.08 * tr('a_xp'); S.xp += x;")
rep("const n = Math.floor((now - S.hamT) / HAM_T); if (n > 0) { S.ham = Math.min(HAM_MAX, S.ham + n); S.hamT += n * HAM_T; } }",
    "const T0 = HAM_T / (1 + 0.08 * tr('a_ham')), n = Math.floor((now - S.hamT) / T0); if (n > 0) { S.ham = Math.min(HAM_MAX, S.ham + n); S.hamT += n * T0; } }")
rep("function rollRarity() { const w = rarityWeights(S.forge);", "function rollRarity() { const w = rarityWeights(S.forge + 0.6 * tr('a_luck'));")
rep("const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r]);\nconst upShards = it => Math.round(3 * Math.pow(1.18, it.L - 1) * (1 + it.r * 0.3));",
    "const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r] * (1 - 0.05 * tr('a_up')));\nconst upShards = it => Math.max(1, Math.round(3 * Math.pow(1.18, it.L - 1) * (1 + it.r * 0.3) * (1 - 0.05 * tr('a_up'))));")
rep("const compDmgPct = id => COMPS[id].pct * (1 + 0.12 * (Math.max(1, compLv(id)) - 1));", "const compDmgPct = id => COMPS[id].pct * (1 + 0.12 * (Math.max(1, compLv(id)) - 1)) * (1 + 0.1 * tr('a_comp'));")
# exécution, tir fourchu, rafale
rep("const crit = Math.random() * 100 < st.crit, dmg = st.atk * (crit ? st.cdmg / 100 : 1) * rand(0.92, 1.08) * (1 + (t.boss || t.elite ? st.bigDmg : 0) + (t.chill > 0 ? st.slowBonus : 0));",
    "const crit = Math.random() * 100 < st.crit, dmg = st.atk * (crit ? st.cdmg / 100 : 1) * rand(0.92, 1.08) * (1 + (t.boss || t.elite ? st.bigDmg : 0) + (t.chill > 0 ? st.slowBonus : 0) + (t.hp < t.max * 0.3 ? st.exec : 0));")
rep("  B.shots.push({ X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: st.splash, splashK: st.splashK, chill: st.chill, wr: (B.gear || gear()).w });\n  B.hero.shootT = 0.3;",
    """  const shot = { X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: st.splash, splashK: st.splashK, chill: st.chill, wr: (B.gear || gear()).w }; B.shots.push(shot);
  const extra = (st.multi && Math.random() < st.multi ? 1 : 0) + (st.dbl && (B.dblN = (B.dblN || 0) + 1) % 3 === 0 ? 1 : 0);
  for (let i = 0; i < extra; i++) { const o = alive.filter(e => e !== t); B.shots.push(Object.assign({}, shot, { tg: o.length ? pick(o) : t, X: (i ? -1 : 1) * 0.06, h: 34 })); }
  B.hero.shootT = 0.3;""")
# indomptable + égide
rep("  if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0;",
    "  if (B.hero.hp <= 0 && st.undying && !B.hero.saved) { B.hero.saved = 1; B.hero.hp = B.hero.hpMax * 0.3; num(CX, YF - 110, 'Indomptable !', '#5ab0ff', 1.4); B.flash = { c: '90,176,255', t: 0.4, a: 0.3 }; }\n  if (B.hero.hp <= 0) { B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0;")
rep("B.hero.psT = 0; B.hero.icT = 0; B.dmg = []; B.waveDmg = 0;\n  ui();\n}",
    "B.hero.psT = 0; B.hero.icT = 0; B.hero.saved = 0; B.dmg = []; B.waveDmg = 0;\n  if (tr('r_shield')) B.shield = Math.max(B.shield || 0, H.pv * 0.05 * tr('r_shield'));\n  ui();\n}")
# marteau béni
rep("function forgeNow() {\n  hamTick(); if (S.ham <= 0) return;", "function forgeNow() {\n  hamTick(); if (S.ham <= 0) return; if (tr('a_twin') && Math.random() < 0.1) { S.ham++; toast('Marteau béni : forge gratuite !'); }")
rep("  S.ham--; S.forged++; const it = makeItem(), cur = S.eq[it.slot];", "  S.ham--; if (tr('a_twin') && Math.random() < 0.1) S.ham++; S.forged++; const it = makeItem(), cur = S.eq[it.slot];")

# ---------- icônes ----------
rep("const IC = {", """const IC = {
  gem: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 5 9l7 13 7-13zm0 3.2L16.4 9H7.6z"/></svg>',
  ham: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z"/></svg>',
  tree: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="4.5" r="2.6"/><circle cx="5" cy="12" r="2.6"/><circle cx="19" cy="12" r="2.6"/><circle cx="12" cy="19.5" r="2.6"/><path d="M11 6.5h2v11h-2zM6.4 10.4l4.8-4.8 1.4 1.4-4.8 4.8zM12.8 7l1.4-1.4 4.8 4.8-1.4 1.4z"/></svg>',""")

# ---------- onglet Talents ----------
rep('    <button data-t="skills" type="button">', '    <button data-t="talent" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="4.5" r="2.6"/><circle cx="5" cy="12" r="2.6"/><circle cx="19" cy="12" r="2.6"/><circle cx="12" cy="19.5" r="2.6"/><path d="M11 6.5h2v11h-2zM6.4 10.4l4.8-4.8 1.4 1.4-4.8 4.8zM12.8 7l1.4-1.4 4.8 4.8-1.4 1.4z"/></svg>Talents<i class="dot" id="tpDot" hidden></i></button>\n    <button data-t="skills" type="button">')
rep("#nav{display:grid;grid-template-columns:repeat(4,1fr);", "#nav{display:grid;grid-template-columns:repeat(5,1fr);")
rep("  } else if (tab === 'skills') {", r"""  } else if (tab === 'talent') {
    const sel = TSEL && NODE[TSEL] ? TSEL : null;
    $('panel').innerHTML = `<div class="frame tt"><div class="tthd"><div><b>${S.tp}</b><small>point${S.tp > 1 ? 's' : ''} à placer</small></div><span>Niveau ${S.lvl} · 1 point par niveau</span><button class="btn" id="tReset" type="button" ${treeSpent() ? '' : 'disabled'}>Réinitialiser<small>${fmt(resetCost())} or</small></button></div>
    <div class="ttree">${Object.entries(TREE).map(([b, T]) => `<div class="tbr" style="--tc:${T.c}"><div class="tbh"><b>${T.n}</b><small>${T.d} · ${branchSpent(b)} pts</small></div>${T.tiers.map((row, ti) => `<div class="trow ${branchSpent(b) >= ti * TIER_REQ ? 'open' : ''}">${row.map(k => { const N = NODE[k], r = tr(k), open = nodeOpen(k); return `<button type="button" class="tn ${r ? 'on' : ''} ${r >= N[1] ? 'max' : ''} ${open ? '' : 'lock'} ${sel === k ? 'sel' : ''} ${N[1] === 1 ? 'cap' : ''} ${open && r < N[1] && S.tp > 0 ? 'can' : ''}" data-tn="${k}">${open ? IC[N[2]] : IC.lock}<em>${r}/${N[1]}</em></button>`; }).join('')}</div>`).join('')}</div>`).join('')}</div>
    <div class="tdet">${sel ? (() => { const N = NODE[sel], r = tr(sel), open = nodeOpen(sel), b = nodeBranch(sel); return `<div class="tdh" style="--tc:${TREE[b].c}"><b>${N[0]}</b><small>${TREE[b].n} · palier ${nodeTier(sel) + 1} · rang ${r}/${N[1]}</small></div><p>${r ? `<span>Actuel :</span> ${N[3](r)}` : ''}${r < N[1] ? `${r ? '<br>' : ''}<span>${r ? 'Rang suivant' : 'Effet'} :</span> ${N[3](r + 1)}` : '<br><em>Rang maximum</em>'}</p>${open ? `<button class="btn gold" id="tAdd" type="button" ${S.tp > 0 && r < N[1] ? '' : 'disabled'}>${r >= N[1] ? 'Maximum atteint' : S.tp > 0 ? 'Ajouter un point' : 'Plus de points : monte de niveau'}</button>` : `<div class="tlock">${IC.lock} Place ${nodeTier(sel) * TIER_REQ - branchSpent(b)} point(s) de plus dans ${TREE[b].n} pour débloquer</div>`}`; })() : '<p class="thint">Touche un talent pour voir son effet. Chaque palier se débloque avec 4 points de plus dans la branche. Le sommet de chaque branche change ta façon de jouer.</p>'}</div></div>`;
    document.querySelectorAll('[data-tn]').forEach(b => b.onclick = () => { TSEL = b.dataset.tn; ui(); });
    if ($('tAdd')) $('tAdd').onclick = () => { const k = TSEL, N = NODE[k]; if (S.tp < 1 || tr(k) >= N[1] || !nodeOpen(k)) return; S.tp--; S.tree[k] = tr(k) + 1; save(); const st = heroStats(); B.hero.hpMax = st.pv; sfxPlay('level'); ui(); };
    $('tReset').onclick = () => { const c = resetCost(); if (S.gold < c) { toast('Pas assez d\'or'); return; } if (!confirm('Réinitialiser l\'arbre ? Tous les points seront rendus.')) return; S.gold -= c; S.tp += treeSpent(); S.tree = {}; save(); toast('Arbre réinitialisé'); ui(); };
  } else if (tab === 'skills') {""")
rep("let tab = 'forge';", "let tab = 'forge', TSEL = null;")
# pastille de points disponibles
rep("  $('bossBtn').style.display = 'none';", "  $('tpDot').hidden = S.tp < 1; $('tpDot').textContent = S.tp;\n  $('bossBtn').style.display = 'none';")
# onglet Héros : liste des anciens talents remplacée par un lien
a = s.index("    ${Object.entries(TALENTS).map(([k, [n, d, ic]])"); b = s.index("\n", a)
s = s[:a] + "    <button class=\"btn gold\" id=\"goTree\" type=\"button\" style=\"width:100%;margin-top:10px\">Arbre de talents<small>${S.tp} point${S.tp > 1 ? 's' : ''} à placer</small></button>" + s[b:]
rep("    document.querySelectorAll('[data-tal]').forEach(b => b.onclick = () => {", "    $('goTree').onclick = () => document.querySelector('#nav [data-t=\"talent\"]').click();\n    document.querySelectorAll('[data-tal]').forEach(b => b.onclick = () => {")

s = s.replace("</style>", r"""
/* ---- arbre de talents ---- */
#nav button{font-size:10.5px}
#nav .dot{position:absolute;top:2px;right:18%;min-width:17px;height:17px;padding:0 4px;border-radius:9px;background:#3ad05a;border:2px solid #0c0610;color:#fff;font:400 11px/13px var(--n);font-style:normal}
.tt{padding:10px}
.tthd{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.tthd > div{display:flex;flex-direction:column;align-items:center;min-width:54px;padding:4px 8px;border-radius:12px;background:#0006;border:1.5px solid var(--gold)}
.tthd > div b{font:400 22px var(--n);color:var(--gold2);line-height:1}.tthd > div small{font:800 9px var(--b);color:var(--dim)}
.tthd span{flex:1;font:700 11px/1.3 var(--b);color:var(--dim)}
.tthd .btn{min-height:40px;font-size:12px;padding:4px 10px}
.ttree{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.tbr{display:flex;flex-direction:column;align-items:center;gap:0;padding:6px 2px 8px;border-radius:14px;background:linear-gradient(color-mix(in srgb,var(--tc) 14%,#1a0c12),#120709);border:1.5px solid color-mix(in srgb,var(--tc) 45%,transparent)}
.tbh{text-align:center;margin-bottom:6px}.tbh b{display:block;font:900 13px var(--t);color:var(--tc);letter-spacing:.05em}.tbh small{font:800 9.5px var(--b);color:var(--dim)}
.trow{position:relative;display:flex;justify-content:center;gap:8px;padding:9px 0}
.trow + .trow::before{content:'';position:absolute;top:-6px;left:50%;width:3px;height:15px;margin-left:-1.5px;border-radius:2px;background:#ffffff18}
.trow.open + .trow.open::before{background:var(--tc);box-shadow:0 0 6px var(--tc)}
.tn{position:relative;width:44px;height:44px;border-radius:50%;padding:0;display:grid;place-items:center;font-size:19px;color:#8a7078;background:radial-gradient(circle at 50% 35%,#3a2630,#150a0f);border:2px solid #4a3038;box-shadow:inset 0 -3px 0 #0007}
.tn em{position:absolute;bottom:-7px;left:50%;transform:translateX(-50%);font:400 10px/1 var(--n);font-style:normal;padding:2px 5px;border-radius:7px;background:#0c0508;border:1.5px solid #4a3038;color:#a08890;white-space:nowrap}
.tn.lock{opacity:.45}
.tn.on{color:#fff;border-color:var(--tc);background:radial-gradient(circle at 50% 35%,color-mix(in srgb,var(--tc) 70%,#fff 10%),color-mix(in srgb,var(--tc) 35%,#150a0f));box-shadow:0 0 12px -2px var(--tc),inset 0 -3px 0 #0006}
.tn.on em{border-color:var(--tc);color:#fff}
.tn.max em{background:var(--tc);color:#1a0a0a}
.tn.cap{width:52px;height:52px;border-radius:14px;transform:rotate(45deg)}.tn.cap > svg{transform:rotate(-45deg)}.tn.cap em{transform:translateX(-50%) rotate(-45deg);bottom:-4px;left:4px}
.tn.can{animation:tcan 1.4s ease-in-out infinite}
@keyframes tcan{50%{box-shadow:0 0 14px 0 var(--tc),inset 0 -3px 0 #0007}}
.tn.sel{outline:2px solid #fff;outline-offset:3px}
.tdet{margin-top:10px;padding:10px 12px;border-radius:12px;background:#0005;border:1px solid #ffffff12;min-height:92px}
.tdh b{display:block;font:900 15px var(--t);color:var(--tc)}.tdh small{font:800 11px var(--b);color:var(--dim)}
.tdet p{margin:6px 0 10px;font:700 13px/1.45 var(--b);color:var(--txt)}.tdet p span{color:var(--gold2)}.tdet p em{color:var(--dim)}
.tdet .btn{width:100%}
.tlock{display:flex;align-items:center;gap:6px;font:800 12px var(--b);color:#ff9a9a}
.thint{margin:0;font:700 12px/1.45 var(--b);color:var(--dim)}
</style>""", 1)
open(P, 'w').write(s); print('ok')
