import json
P='/home/claude/grimloom/src.html'
s=open(P).read(); open('/home/claude/grimloom/src.v50.html','w').write(s)
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:120]); s=s.replace(old,new)
hv=json.load(open('/home/claude/grimloom/evo/hevo.json'))
assets=''.join(f"\n  ASSETS.k_{k} = {{ src: 'data:image/png;base64,{v['b64']}', cw: 300, ch: 320, foot: 20, wOff: -20, anims: ah, anc: ASSETS.k_hunter.anc }};" for k,v in hv.items())
rep(" anims: ah, anc: [[[1.0, 149.8, 0]", " anims: ah, anc: [[[1.0, 149.8, 0]")
i=s.index("ASSETS.k_hunter = {"); j=s.index("}; }\n",i)
s=s[:j]+"};"+assets+" }\n"+s[j+5:]
rep("  shiver: { n: 'Le Roi de l\\'Hiver',", """  h_novice: { n: 'Le Pisteur novice', cls: 'hunter', st: 0, lv: 1, atk: 1, hp: 1, d: 'Un jeune pisteur en cuir usé. Deux arbalètes et beaucoup à prouver.' },
  hunter: { n: 'Le Chasseur de démons', cls: 'hunter', st: 1, lv: 15, atk: 1.15, hp: 1.15, d: 'Armure de chasseur · attaque et PV +15 %' },
  h_ombre: { n: 'Le Rôdeur de l\\'Ombre', cls: 'hunter', st: 2, lv: 30, path: 'ombre', atk: 1.45, hp: 1.2, crit: 10, d: 'Voie de l\\'ombre · critique +10 %' },
  h_sang: { n: 'Le Chasseur de Sang', cls: 'hunter', st: 2, lv: 30, path: 'sang', atk: 1.35, hp: 1.3, leech: 0.06, d: 'Voie du sang · vol de vie +6 %' },
  h_argent: { n: 'L\\'Inquisiteur d\\'Argent', cls: 'hunter', st: 2, lv: 30, path: 'argent', atk: 1.4, hp: 1.25, boss: 0.25, d: 'Voie sacrée · dégâts aux boss et élites +25 %' },
  h_faucheur: { n: 'Le Faucheur des Ténèbres', cls: 'hunter', st: 3, lv: 60, path: 'ombre', atk: 1.95, hp: 1.55, crit: 18, d: 'Forme ultime · critique +18 %' },
  h_seigsang: { n: 'Le Seigneur du Sang', cls: 'hunter', st: 3, lv: 60, path: 'sang', atk: 1.8, hp: 1.7, leech: 0.12, d: 'Forme ultime · vol de vie +12 %' },
  h_grandinq: { n: 'Le Grand Inquisiteur', cls: 'hunter', st: 3, lv: 60, path: 'argent', atk: 1.85, hp: 1.65, boss: 0.5, d: 'Forme ultime · dégâts aux boss et élites +50 %' },
  shiver: { n: 'Le Roi de l\\'Hiver',""")
rep("smort: [], sfeu: [], shiver: [] };", """smort: [], sfeu: [], shiver: [], h_novice: ['hunter'], hunter: ['h_ombre', 'h_sang', 'h_argent'], h_ombre: ['h_faucheur'], h_sang: ['h_seigsang'], h_argent: ['h_grandinq'], h_faucheur: [], h_seigsang: [], h_grandinq: [] };
const curForm = () => S.cls === 'hunter' ? S.hform : S.form;
const TREE = { knight: { t: 'du chevalier', a: ['ecuyer', 'chev'], b: ['mort', 'enfer', 'givre'], c: ['smort', 'sfeu', 'shiver'], note: 'Mort : vol de vie et tirs d\\'ombre · Feu : tirs explosifs · Glace : tirs ralentissants et plus de PV.' }, hunter: { t: 'du chasseur', a: ['h_novice', 'hunter'], b: ['h_ombre', 'h_sang', 'h_argent'], c: ['h_faucheur', 'h_seigsang', 'h_grandinq'], note: 'Ombre : coups critiques · Sang : vol de vie · Argent : tueur de boss et d\\'élites.' } };
const evoMul = E => E.cls === 'hunter' ? [0.95 * E.atk, 0.95 * E.hp] : [1.15 * E.atk, 1.2 * E.hp];""")
rep("const evoReady = () => S.cls !== 'hunter' && EVO_NEXT[S.form].some(k => S.lvl >= EVO[k].lv);","const evoReady = () => EVO_NEXT[curForm()].some(k => S.lvl >= EVO[k].lv);")
rep("  if (S.cls === 'hunter') { const m = S.lvl >= 60 ? 1.8 : S.lvl >= 30 ? 1.35 : S.lvl >= 15 ? 1.15 : 1; Object.assign(H, { n: 'Le Chasseur de démons', key: 'k_hunter', atk: 0.95 * m, hp: 0.95 * m, spd: 1.4, fx: 'fleche', solid: 1, leech: 0, splash: 0, chill: 0, twin: 1 }); return; }",
    "  if (S.cls === 'hunter') { const F = EVO[S.hform], m = evoMul(F); Object.assign(H, { n: F.n, key: 'k_' + S.hform, atk: m[0], hp: m[1], spd: 1.4, fx: 'fleche', solid: 1, leech: F.leech || 0, splash: 0, chill: 0, twin: 1, crit: F.crit || 0, boss: F.boss || 0 }); return; }")
rep("splash: E.splash || 0, chill: E.chill || 0 }); }","splash: E.splash || 0, chill: E.chill || 0, crit: 0, boss: 0 }); }")
rep("function evolve(k) { if (!EVO_NEXT[S.form].includes(k) || S.lvl < EVO[k].lv) return; S.form = k;","function evolve(k) { if (!EVO_NEXT[curForm()].includes(k) || S.lvl < EVO[k].lv) return; if (S.cls === 'hunter') S.hform = k; else S.form = k;")
rep("if (!S.form) S.form = (S.lvl || 1) >= 30 ? 'mort' : (S.lvl || 1) >= 15 ? 'chev' : 'ecuyer'; applyEvo();","if (!S.form) S.form = (S.lvl || 1) >= 30 ? 'mort' : (S.lvl || 1) >= 15 ? 'chev' : 'ecuyer'; if (!S.hform) S.hform = (S.lvl || 1) >= 15 ? 'hunter' : 'h_novice'; applyEvo();")
rep("o.bigDmg += 0.08 * tr('c_boss');","o.bigDmg += 0.08 * tr('c_boss') + (H.boss || 0); o.crit += H.crit || 0;")
rep("if (S.cls === 'hunter') applyEvo(); toast(","toast(")
rep("if (EVO_NEXT[S.form].some(k => S.lvl === EVO[k].lv))","if (EVO_NEXT[curForm()].some(k => S.lvl === EVO[k].lv))")
# UI
rep("k = c === 'hunter' ? 'hunter' : S.form;","k = c === 'hunter' ? S.hform : S.form;")
i=s.index("    } else if (HSUB === 'evo' && S.cls === 'hunter') {"); j=s.index("    } else if (HSUB === 'evo') {")
s=s[:i]+s[j:]
i=s.index("    } else if (HSUB === 'evo') {"); j=s.index("    } else if (HSUB === 'comp') {")
s=s[:i]+"""    } else if (HSUB === 'evo') {
      const T = TREE[S.cls], f = curForm(), cur = EVO[f], cm = evoMul(cur), card = k => { const E = EVO[k], own = k === f, past = E.st < cur.st && (E.st < 2 || E.path === cur.path), next = EVO_NEXT[f].includes(k), can = next && S.lvl >= E.lv, closed = E.st >= 2 && cur.st >= 2 && E.path !== cur.path;
        return `<div class="kt evc ${own ? 'gd' : ''} ${closed || (!own && !past && !next) ? 'lock' : ''}"><canvas data-ev="${k}" width="96" height="104"></canvas><b>${E.n.replace(/^(Le |L')/, '')}</b><small>${own ? 'Forme actuelle' : past ? 'Passée' : closed ? 'Autre voie' : 'Niveau ' + E.lv}</small>${can ? `<button class="btn gold sm" type="button" data-evo="${k}">Évoluer</button>` : ''}</div>`; };
      body = `<h4 class="kh" style="margin-top:0">Classe</h4><div class="evrow">${clsCard('knight')}${clsCard('hunter')}</div><h4 class="kh">Évolution ${T.t}</h4><div class="kl evcur"><canvas data-ev="${f}" data-big="1" width="150" height="160"></canvas><div class="kri"><b style="font-size:16px">${cur.n}</b><small>${cur.d}</small><small class="kdim">Attaque ×${cm[0].toFixed(2)} · PV ×${cm[1].toFixed(2)}${S.cls === 'hunter' ? ' · cadence ×1.4 · deux carreaux' : ''}</small>${EVO_NEXT[f].length ? `<small class="kdim">Prochaine évolution au niveau <b style="color:#ffd890">${Math.min(...EVO_NEXT[f].map(k => EVO[k].lv))}</b> (tu es niveau ${S.lvl})</small>` : '<small style="color:#ffd890">Forme ultime atteinte</small>'}</div></div>
      <h4 class="kh">Les débuts</h4><div class="evrow">${T.a.map(card).join('')}</div>
      <h4 class="kh">Choisis ta voie <small>au niveau 30 · le choix est définitif</small></h4><div class="evrow three">${T.b.map(card).join('')}</div>
      <h4 class="kh">Formes ultimes <small>au niveau 60</small></h4><div class="evrow three">${T.c.map(card).join('')}</div>
      <p class="knote">${T.note}</p>`;
"""+s[j:]
open(P,'w').write(s); print('ok')
