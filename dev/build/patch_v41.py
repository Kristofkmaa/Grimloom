import json
P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v41.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
EV = json.load(open('/home/claude/grimloom/evo/evo.json'))

# ---------- planches des 8 formes à la place de l'ancien chevalier ----------
a = s.index("{ const an = {}, k = { idle"); b = s.index("for (const k in ASSETS) if (ASSETS[k].src) {", a)
block = "{ const an = {}, k = { idle: 5 / 12, course: 0.5, tir: 4 / 14.5, touche: 2 / 12.5 };\n  for (let d = 0; d < 8; d++) { const front = d >= 5 && d <= 7; an['idle_' + d] = { row: front ? 4 : 0, n: 4, k: k.idle }; an['course_' + d] = { row: 1, n: 4, k: k.course }; an['tir_' + d] = { row: 2, n: 4, k: k.tir }; an['touche_' + d] = { row: 3, n: 2, k: k.touche }; }\n"
for n, v in EV.items():
    block += f"  ASSETS.k_{n} = {{ src: 'data:image/png;base64,{v['b64']}', cw: 300, ch: 320, foot: 20, anims: an, anc: {json.dumps(v['anc'])} }};\n"
block += "}\n"
s = s[:a] + block + s[b:]

# ---------- évolutions ----------
rep("const RAR = [", r"""// ================= évolution du héros (comme Legend of Mushroom) =================
const EVO = {
  ecuyer: { n: 'L\'Écuyer', st: 0, lv: 1, atk: 1, hp: 1, d: 'Un jeune écuyer en armure légère. Tout commence ici.' },
  chev: { n: 'Le Chevalier', st: 1, lv: 15, atk: 1.15, hp: 1.15, d: 'Armure complète · attaque et PV +15 %' },
  mort: { n: 'Le Chevalier de la Mort', st: 2, lv: 30, path: 'mort', atk: 1.35, hp: 1.3, fx: 'pmort', leech: 0.06, d: 'Voie de l\'ombre · vol de vie +6 %' },
  enfer: { n: 'Le Chevalier Infernal', st: 2, lv: 30, path: 'enfer', atk: 1.45, hp: 1.2, fx: 'pfeu', splash: 1, d: 'Voie du feu · tirs explosifs' },
  givre: { n: 'Le Chevalier de Givre', st: 2, lv: 30, path: 'givre', atk: 1.3, hp: 1.4, fx: 'pglace', chill: 1, d: 'Voie de la glace · tirs ralentissants' },
  smort: { n: 'Le Seigneur de la Mort', st: 3, lv: 60, path: 'mort', atk: 1.8, hp: 1.7, fx: 'pmort', leech: 0.12, d: 'Forme ultime · vol de vie +12 %' },
  sfeu: { n: 'Le Seigneur des Flammes', st: 3, lv: 60, path: 'enfer', atk: 1.95, hp: 1.55, fx: 'pfeu', splash: 1, d: 'Forme ultime · explosions renforcées' },
  shiver: { n: 'Le Roi de l\'Hiver', st: 3, lv: 60, path: 'givre', atk: 1.7, hp: 1.9, fx: 'pglace', chill: 1, d: 'Forme ultime · gel et robustesse' },
};
const EVO_NEXT = { ecuyer: ['chev'], chev: ['mort', 'enfer', 'givre'], mort: ['smort'], enfer: ['sfeu'], givre: ['shiver'], smort: [], sfeu: [], shiver: [] };
const evoReady = () => EVO_NEXT[S.form].some(k => S.lvl >= EVO[k].lv);
function applyEvo() { const E = EVO[S.form], H = HEROES.chevalier; Object.assign(H, { n: E.n, key: 'k_' + S.form, atk: 1.15 * E.atk, hp: 1.2 * E.hp, fx: E.fx || 'arc', leech: E.leech || 0.03, splash: E.splash || 0, chill: E.chill || 0 }); }
function evolve(k) { if (!EVO_NEXT[S.form].includes(k) || S.lvl < EVO[k].lv) return; S.form = k; applyEvo(); save(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; B.flash = { c: '255,240,200', t: 0.6, a: 0.6 }; B.shake = 8; B.banner = { a: 'Évolution !', b: EVO[k].n, t: 2.6 }; equipFx({ r: 6 }); sfxPlay('reward'); ui(); }
const RAR = [""")
rep("const RT_MAX = 3", "const RT_MAX = 3", 0) if False else None
# état : forme de départ, migration des anciennes sauvegardes
rep("S.hero = 'chevalier';", "S.hero = 'chevalier'; if (!S.form) S.form = (S.lvl || 1) >= 30 ? 'mort' : (S.lvl || 1) >= 15 ? 'chev' : 'ecuyer';")
rep("const RAR = [\n", "const RAR = [\n", 1)
rep("const HEROES = {", "const HEROES = {", 1)
# applyEvo après déclaration
rep("const RMULT = [", "applyEvo();\nconst RMULT = [")
rep("function gainXP(x) { x *= 1 + 0.08 * tr('a_xp'); S.xp += x; while (S.xp >= xpNeed(S.lvl)) { S.xp -= xpNeed(S.lvl); S.lvl++; S.tp++; toast(`Niveau ${S.lvl} ! +1 point de talent`); sfxPlay('level'); } }",
    "function gainXP(x) { x *= 1 + 0.08 * tr('a_xp'); S.xp += x; while (S.xp >= xpNeed(S.lvl)) { S.xp -= xpNeed(S.lvl); S.lvl++; S.tp++; toast(`Niveau ${S.lvl} ! +1 point de talent`); sfxPlay('level'); if (EVO_NEXT[S.form].some(k => S.lvl === EVO[k].lv)) setTimeout(() => toast('Une évolution est disponible ! (Héros › Évolution)'), 900); } }")
rep("function sprH(key, anim, fr, x, y, sc, alpha, g) { g = g || ctx; const A = ASSETS[key], R = A.anims[anim];", "function sprH(key, anim, fr, x, y, sc, alpha, g) { g = g || ctx; const A = ASSETS[key]; if (!A) return; const R = A.anims[anim];")

# ---------- plus de compagnons ni d'alliés ----------
rep("function drawComp(i, time) {", "function drawComp(i, time) { return;")
rep("    else for (let i = 0; i < 2; i++) { const id = S.party[i]; if (!id || !S.comps[id]) continue;", "    else for (let i = 0; i < 0; i++) { const id = S.party[i]; if (!id || !S.comps[id]) continue;")
rep("B.cs = B.cs || []; if (raidOn()) { B.dun.allies.forEach(", "B.cs = B.cs || []; if (raidOn() && 0) { B.dun.allies.forEach(")
rep("function power(st) { st = st || heroStats(); const cp = S.party.reduce((a, id) => a + (id && S.comps[id] ? st.atk * compDmgPct(id) / 100 * compRate(id) * 12 : 0), 0);", "function power(st) { st = st || heroStats(); const cp = 0;")
rep("  a_comp: ['Chef de meute', 3, 'sword', r => `Dégâts des compagnons +${10 * r} %`],", "  a_comp: ['Chasseur de raid', 3, 'star', r => `Plumes gagnées au raid +${15 * r} %`],")
rep("const dmg = B.waveDmg, t = raidTier(dmg), pl = 6 + t * 6;", "const dmg = B.waveDmg, t = raidTier(dmg), pl = Math.round((6 + t * 6) * (1 + 0.15 * tr('a_comp')));")
rep("  ['comp', n => `Monter des compagnons de ${n} niveaux`, 2], ['dun', n => `Réussir ${n} donjons`, 1],", "  ['dun', n => `Réussir ${n} donjons`, 1],")
rep("if (RSEL.length !== 3) { toast('Choisis 3 alliés'); return; }", "")
rep("raid: true, allies: RSEL.map(i => AL[i]) };", "raid: true, allies: [] };")
a = s.index("  <h4 class=\"kh\">Choisis 3 alliés"); b = s.index("  <div class=\"kl\" style=\"margin-top:6px\"><div class=\"rtiers\">", a)
s = s[:a] + s[b:]
rep("${S.raid.n < 1 || RSEL.length !== 3 || B.dun ? 'disabled' : ''}>${S.raid.n < 1 ? 'Reviens demain' : RSEL.length !== 3 ? 'Choisis 3 alliés' : 'Affronter l\\'Archidémon'}</button>", "${S.raid.n < 1 || B.dun ? 'disabled' : ''}>${S.raid.n < 1 ? 'Reviens demain' : 'Affronter l\\'Archidémon'}</button>")
rep("Un boss immortel. Inflige un maximum de dégâts en 30 s avec 3 alliés.", "Un boss immortel. Inflige un maximum de dégâts en 30 s.")
rep("'Calculée à partir de ton équipement, talents et compagnons.'", "'Calculée à partir de ton équipement, de tes talents et de ton évolution.'")
rep("allcp: () => { Object.keys(COMPS).forEach(k => S.comps[k] = { lv: 10 }); },", "allcp: () => { S.lvl = Math.max(S.lvl, 60); },")
s = s.replace('<button class="btn" data-a="allcp" type="button">Tous les compagnons Nv 10</button>', '<button class="btn" data-a="allcp" type="button">Niveau 60 (évolutions)</button>', 1)

# ---------- onglet Héros › Évolution (à la place de Troupe) ----------
rep("[['profil', 'Profil'], ['wing', 'Ailes'], ['comp', 'Troupe'], ['pet', 'Familier'], ['ach', 'Succès']], 'data-hs')", "[['profil', 'Profil'], ['evo', 'Évolution'], ['wing', 'Ailes'], ['pet', 'Familier'], ['ach', 'Succès']], 'data-hs')")
rep("    } else if (HSUB === 'comp') {", r"""    } else if (HSUB === 'evo') {
      const cur = EVO[S.form], card = k => { const E = EVO[k], own = k === S.form, past = E.st < cur.st && (E.st < 2 || E.path === cur.path), next = EVO_NEXT[S.form].includes(k), can = next && S.lvl >= E.lv, closed = E.st >= 2 && cur.st >= 2 && E.path !== cur.path;
        return `<div class="kt evc ${own ? 'gd' : ''} ${closed || (!own && !past && !next) ? 'lock' : ''}"><canvas data-ev="${k}" width="96" height="104"></canvas><b>${E.n.replace(/^(Le |L')/, '')}</b><small>${own ? 'Forme actuelle' : past ? 'Passée' : closed ? 'Autre voie' : 'Niveau ' + E.lv}</small>${can ? `<button class="btn gold sm" type="button" data-evo="${k}">Évoluer</button>` : ''}</div>`; };
      body = `<div class="kl evcur"><canvas data-ev="${S.form}" data-big="1" width="150" height="160"></canvas><div class="kri"><b style="font-size:16px">${cur.n}</b><small>${cur.d}</small><small class="kdim">Attaque ×${(1.15 * cur.atk).toFixed(2)} · PV ×${(1.2 * cur.hp).toFixed(2)}</small>${EVO_NEXT[S.form].length ? `<small class="kdim">Prochaine évolution au niveau <b style="color:#ffd890">${Math.min(...EVO_NEXT[S.form].map(k => EVO[k].lv))}</b> (tu es niveau ${S.lvl})</small>` : '<small style="color:#ffd890">Forme ultime atteinte</small>'}</div></div>
      <h4 class="kh">Les débuts</h4><div class="evrow">${card('ecuyer')}${card('chev')}</div>
      <h4 class="kh">Choisis ta voie <small>au niveau 30 · le choix est définitif</small></h4><div class="evrow three">${card('mort')}${card('enfer')}${card('givre')}</div>
      <h4 class="kh">Formes ultimes <small>au niveau 60</small></h4><div class="evrow three">${card('smort')}${card('sfeu')}${card('shiver')}</div>
      <p class="knote">Mort : vol de vie et tirs d'ombre · Feu : tirs explosifs · Glace : tirs ralentissants et plus de PV.</p>`;
    } else if (HSUB === 'comp') {""")
rep("    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });", r"""    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });
    document.querySelectorAll('[data-ev]').forEach(c => { const k = 'k_' + c.dataset.ev, big = !!c.dataset.big, g = c.getContext('2d'), W = c.width, Hh = c.height; const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, W, Hh); sprH(k, 'idle_6', performance.now() / 80, W / 2, Hh - 2, (Hh - 6) / 250, 1, g); requestAnimationFrame(draw); }; draw(); });
    document.querySelectorAll('[data-evo]').forEach(b => b.onclick = () => { const k = b.dataset.evo; if (EVO[k].st === 2 && !confirm(`Choisir la voie : ${EVO[k].n} ? Ce choix est définitif.`)) return; evolve(k); });""")
rep("let tab = 'forge', TSEL = null, HSUB = 'profil'", "let tab = 'forge', TSEL = null, HSUB = 'evo'")
# pastille sur l'onglet Héros
rep('    <button data-t="hero" type="button">', '    <button data-t="hero" type="button"><i class="dot" id="evDot" hidden>!</i>')
rep("  $('tpDot').hidden = S.tp < 1;", "  $('evDot').hidden = !evoReady();\n  $('tpDot').hidden = S.tp < 1;")
s = s.replace("</style>", r"""
.evcur{display:flex;align-items:center;gap:10px;margin-bottom:6px}.evcur canvas{width:120px;height:128px;image-rendering:pixelated;flex:none}
.evrow{display:grid;grid-template-columns:1fr 1fr;gap:6px}.evrow.three{grid-template-columns:repeat(3,1fr)}
.evc{display:flex!important;flex-direction:column;align-items:center;gap:2px;padding:2px 0 4px!important;text-align:center!important;min-height:150px}
.evc canvas{width:76px;height:82px;image-rendering:pixelated}
.evc b{font:900 11px/1.15 var(--t);color:#f2d79a}.evc small{font:800 9.5px var(--b);color:#a08a78}
.evc .btn{margin-top:4px;min-height:32px;padding:2px 10px;font-size:12px;animation:tcan 1.4s infinite}
</style>""", 1)
open(P, 'w').write(s); print('ok')
