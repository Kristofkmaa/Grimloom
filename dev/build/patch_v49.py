import json
P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v49.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
hj = json.load(open('/home/claude/grimloom/evo/hunter.json'))
rep("for (const k in ASSETS) if (ASSETS[k].src) {", "{ const ah = {}, k = { idle: 5 / 12, course: 0.55, tir: 4 / 13, touche: 2 / 12.5 }; for (let d = 0; d < 8; d++) { const front = d >= 5 && d <= 7; ah['idle_' + d] = { row: front ? 4 : 0, n: 4, k: k.idle }; ah['course_' + d] = { row: 1, n: 4, k: k.course }; ah['tir_' + d] = { row: 2, n: 4, k: k.tir }; ah['touche_' + d] = { row: 3, n: 2, k: k.touche }; }\n  ASSETS.k_hunter = { src: 'data:image/png;base64," + hj['b64'] + "', cw: 300, ch: 320, foot: 20, anims: ah, anc: " + json.dumps(hj['anc']) + " }; }\nfor (const k in ASSETS) if (ASSETS[k].src) {")
rep("function applyEvo() { const E = EVO[S.form], H = HEROES.chevalier; Object.assign(H, { n: E.n, key: 'k_' + S.form, atk: 1.15 * E.atk, hp: 1.2 * E.hp, fx: E.fx || 'arc', leech: E.leech || 0.03, splash: E.splash || 0, chill: E.chill || 0 }); }",
    "function applyEvo() { const E = EVO[S.form], H = HEROES.chevalier;\n  if (S.cls === 'hunter') { const m = S.lvl >= 60 ? 1.8 : S.lvl >= 30 ? 1.35 : S.lvl >= 15 ? 1.15 : 1; Object.assign(H, { n: 'Le Chasseur de démons', key: 'k_hunter', atk: 0.95 * m, hp: 0.95 * m, spd: 1.4, fx: 'fleche', solid: 1, leech: 0, splash: 0, chill: 0, twin: 1 }); return; }\n  Object.assign(H, { n: E.n, key: 'k_' + S.form, atk: 1.15 * E.atk, hp: 1.2 * E.hp, spd: 1.0, solid: 0, twin: 0, fx: E.fx || 'arc', leech: E.leech || 0.03, splash: E.splash || 0, chill: E.chill || 0 }); }\nfunction setClass(c) { if (S.cls === c) return; S.cls = c; applyEvo(); save(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; B.flash = { c: '255,240,200', t: 0.5, a: 0.5 }; B.banner = { a: 'Nouvelle classe', b: HEROES.chevalier.n, t: 2 }; equipFx({ r: 5 }); ui(); }")
rep("S.hero = 'chevalier'; if (!S.form)", "S.hero = 'chevalier'; if (!S.cls) S.cls = 'knight'; if (!S.form)")
# double tir du chasseur
rep("const extra = (st.multi && Math.random() < st.multi ? 1 : 0) + (st.dbl && (B.dblN = (B.dblN || 0) + 1) % 3 === 0 ? 1 : 0);",
    "const extra = (st.multi && Math.random() < st.multi ? 1 : 0) + (st.dbl && (B.dblN = (B.dblN || 0) + 1) % 3 === 0 ? 1 : 0) + (H.twin ? 1 : 0);")
# niveau → multiplicateur du chasseur à jour
rep("S.lvl++; S.tp++;", "S.lvl++; S.tp++; if (S.cls === 'hunter') applyEvo();")
# choix de la classe dans l'onglet Évolution
rep("    } else if (HSUB === 'evo') {\n", r"""    } else if (HSUB === 'evo' && S.cls === 'hunter') {
      body = `<h4 class="kh" style="margin-top:0">Classe</h4><div class="evrow">${clsCard('knight')}${clsCard('hunter')}</div>
      <div class="kl evcur" style="margin-top:10px"><canvas data-ev="hunter" data-big="1" width="150" height="160"></canvas><div class="kri"><b style="font-size:16px">Le Chasseur de démons</b><small>Agile et rapide : tire avec deux arbalètes, deux carreaux à chaque attaque.</small><small class="kdim">Attaque ×${HEROES.chevalier.atk.toFixed(2)} · PV ×${HEROES.chevalier.hp.toFixed(2)} · cadence ×1.4</small><small class="kdim">Sa puissance grandit aux niveaux 15, 30 et 60.</small><small style="color:#ffd890">Ses évolutions arrivent bientôt.</small></div></div>`;
    } else if (HSUB === 'evo') {
""")
rep("      body = `<div class=\"kl evcur\"><canvas data-ev=\"${S.form}\"", "      body = `<h4 class=\"kh\" style=\"margin-top:0\">Classe</h4><div class=\"evrow\">${clsCard('knight')}${clsCard('hunter')}</div><h4 class=\"kh\">Évolution du chevalier</h4><div class=\"kl evcur\"><canvas data-ev=\"${S.form}\"")
rep("  const H = HEROES[S.hero], nAch = ACH.filter(a => S.ach[a[0]]).length,", "  const clsCard = c => { const on = S.cls === c, k = c === 'hunter' ? 'hunter' : S.form; return `<div class=\"kt evc ${on ? 'gd' : ''}\" style=\"min-height:130px\"><canvas data-ev=\"${k}\" width=\"96\" height=\"104\"></canvas><b>${c === 'hunter' ? 'Chasseur de démons' : 'Chevalier'}</b><small>${on ? 'Classe actuelle' : c === 'hunter' ? 'Deux arbalètes · rapide' : 'Épée · évolutions'}</small>${on ? '' : `<button class=\"btn gold sm\" type=\"button\" data-cls=\"${c}\">Choisir</button>`}</div>`; };\n    const H = HEROES[S.hero], nAch = ACH.filter(a => S.ach[a[0]]).length,")
rep("    document.querySelectorAll('[data-evo]').forEach(b =>", "    document.querySelectorAll('[data-cls]').forEach(b => b.onclick = () => setClass(b.dataset.cls));\n    document.querySelectorAll('[data-evo]').forEach(b =>")
open(P, 'w').write(s); print('ok')
