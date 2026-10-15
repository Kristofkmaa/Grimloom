import base64
P='/home/claude/grimloom/src.html'
s=open(P).read(); open('/home/claude/grimloom/src.v52.html','w').write(s)
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:120]); s=s.replace(old,new)
b64=base64.b64encode(open('/home/claude/grimloom/evo/out_mage.png','rb').read()).decode()
anc="[[[0,150,0],[0,150,0],[0,150,0],[0,150,0]],[[0,150,0],[0,150,0],[0,150,0],[0,150,0]],[[0,150,0],[2,147,-6],[-2,147,6],[0,150,0]],[[0,140,-4],[0,132,-8]],[[0,172,0],[0,172,0],[0,172,0],[0,172,0]]]"
i=s.index("ASSETS.k_h_grandinq = {"); j=s.index(" }\n",s.index("anc: ASSETS.k_hunter.anc };",i))
s=s[:j]+"\n  { const am = {}; for (const kk in ah) am[kk] = ah[kk]; for (let d = 0; d < 8; d++) am['tir_' + d] = { row: 2, f0: 1, n: 2, k: 1 / 7 };\n  ASSETS.k_m_sorcier = { src: 'data:image/png;base64,"+b64+"', cw: 300, ch: 320, foot: 20, wOff: -20, anims: am, anc: "+anc+" }; }"+s[j:]
rep("  shiver: { n: 'Le Roi de l\\'Hiver',","  m_sorcier: { n: 'Le Sorcier', cls: 'mage', st: 0, lv: 1, atk: 1, hp: 1, d: 'Un sorcier encapuchonné. Son bâton de cristal lance des orbes qui explosent au contact.' },\n  shiver: { n: 'Le Roi de l\\'Hiver',")
rep("h_faucheur: [], h_seigsang: [], h_grandinq: [] };","h_faucheur: [], h_seigsang: [], h_grandinq: [], m_sorcier: [] };")
rep("const curForm = () => S.cls === 'hunter' ? S.hform : S.form;","const curForm = () => S.cls === 'hunter' ? S.hform : S.cls === 'mage' ? S.mform : S.form;")
rep("note: 'Ombre : coups critiques · Sang : vol de vie · Argent : tueur de boss et d\\'élites.' } };","note: 'Ombre : coups critiques · Sang : vol de vie · Argent : tueur de boss et d\\'élites.' }, mage: { t: 'du sorcier', a: ['m_sorcier'], b: [], c: [], note: 'Ses évolutions arrivent bientôt.' } };")
rep("const evoMul = E => E.cls === 'hunter' ? [0.95 * E.atk, 0.95 * E.hp] : [1.15 * E.atk, 1.2 * E.hp];","const evoMul = E => E.cls === 'hunter' ? [0.95 * E.atk, 0.95 * E.hp] : E.cls === 'mage' ? [1.35 * E.atk, 0.85 * E.hp] : [1.15 * E.atk, 1.2 * E.hp];")
rep("  if (S.cls === 'hunter') { const F = EVO[S.hform]","  if (S.cls === 'mage') { const F = EVO[S.mform], m = evoMul(F); Object.assign(H, { n: F.n, key: 'k_' + S.mform, atk: m[0], hp: m[1], spd: 0.9, fx: 'pglace', solid: 0, leech: 0, splash: 1, chill: 0, twin: 0, crit: 0, boss: 0 }); return; }\n  if (S.cls === 'hunter') { const F = EVO[S.hform]")
rep("if (S.cls === 'hunter') S.hform = k; else S.form = k;","if (S.cls === 'hunter') S.hform = k; else if (S.cls === 'mage') S.mform = k; else S.form = k;")
rep("if (!S.hform) S.hform = (S.lvl || 1) >= 15 ? 'hunter' : 'h_novice';","if (!S.hform) S.hform = (S.lvl || 1) >= 15 ? 'hunter' : 'h_novice'; if (!S.mform) S.mform = 'm_sorcier';")
rep("""    const clsCard = c => { const on = S.cls === c, k = c === 'hunter' ? S.hform : S.form; return `<div class="kt evc ${on ? 'gd' : ''}" style="min-height:130px"><canvas data-ev="${k}" width="96" height="104"></canvas><b>${c === 'hunter' ? 'Chasseur de démons' : 'Chevalier'}</b><small>${on ? 'Classe actuelle' : c === 'hunter' ? 'Deux arbalètes · rapide' : 'Épée · évolutions'}</small>""",
"""    const CL = { knight: ['Chevalier', 'Épée · équilibré', S.form], hunter: ['Chasseur', 'Deux arbalètes · rapide', S.hform], mage: ['Sorcier', 'Orbes explosives · lent', S.mform] };
    const clsCard = c => { const on = S.cls === c, k = CL[c][2]; return `<div class="kt evc ${on ? 'gd' : ''}" style="min-height:130px"><canvas data-ev="${k}" width="96" height="104"></canvas><b>${CL[c][0]}</b><small>${on ? 'Classe actuelle' : CL[c][1]}</small>""")
rep("""<div class="evrow">${clsCard('knight')}${clsCard('hunter')}</div>""","""<div class="evrow three">${clsCard('knight')}${clsCard('hunter')}${clsCard('mage')}</div>""")
rep("""${S.cls === 'hunter' ? ' · cadence ×1.4 · deux carreaux' : ''}""","""${S.cls === 'hunter' ? ' · cadence ×1.4 · deux carreaux' : S.cls === 'mage' ? ' · cadence ×0.9 · explosions' : ''}""")
rep("""      <h4 class="kh">Les débuts</h4><div class="evrow">${T.a.map(card).join('')}</div>
      <h4 class="kh">Choisis ta voie <small>au niveau 30 · le choix est définitif</small></h4><div class="evrow three">${T.b.map(card).join('')}</div>
      <h4 class="kh">Formes ultimes <small>au niveau 60</small></h4><div class="evrow three">${T.c.map(card).join('')}</div>""",
"""      ${T.b.length ? `<h4 class="kh">Les débuts</h4><div class="evrow">${T.a.map(card).join('')}</div>
      <h4 class="kh">Choisis ta voie <small>au niveau 30 · le choix est définitif</small></h4><div class="evrow three">${T.b.map(card).join('')}</div>
      <h4 class="kh">Formes ultimes <small>au niveau 60</small></h4><div class="evrow three">${T.c.map(card).join('')}</div>` : ''}""")
open(P,'w').write(s); print('ok')
