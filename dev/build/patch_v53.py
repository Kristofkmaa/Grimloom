import json
P='/home/claude/grimloom/src.html'
s=open(P).read(); open('/home/claude/grimloom/src.v53.html','w').write(s)
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:140]); s=s.replace(old,new)
mv=json.load(open('/home/claude/grimloom/evo/mevo.json'))
i=s.index("ASSETS.k_m_sorcier = {"); j=s.index(" }; }",i)+3
s=s[:j]+''.join(f"\n  ASSETS.k_{k} = {{ src: 'data:image/png;base64,{b}', cw: 300, ch: 320, foot: 20, wOff: -33, anims: am, anc: ASSETS.k_m_sorcier.anc }};" for k,b in mv.items())+s[j:]
rep("  m_sorcier: { n: 'Le Sorcier', cls: 'mage', st: 0, lv: 1, atk: 1, hp: 1, d: 'Un sorcier encapuchonné. Son bâton de cristal lance des orbes qui explosent au contact.' },",
"""  m_apprenti: { n: 'L\\'Apprenti', cls: 'mage', st: 0, lv: 1, atk: 1, hp: 1, d: 'Un jeune apprenti en robe rapiécée. Ses orbes explosent déjà au contact.' },
  m_sorcier: { n: 'Le Sorcier', cls: 'mage', st: 1, lv: 15, atk: 1.15, hp: 1.15, d: 'Bâton de cristal · attaque et PV +15 %' },
  m_pyro: { n: 'Le Pyromancien', cls: 'mage', st: 2, lv: 30, path: 'feu', atk: 1.5, hp: 1.15, fx: 'pfeu', splashK: 0.2, d: 'Voie du feu · explosions plus larges' },
  m_necro: { n: 'Le Nécromancien', cls: 'mage', st: 2, lv: 30, path: 'morts', atk: 1.35, hp: 1.3, fx: 'pmort', leech: 0.06, d: 'Voie des morts · vol de vie +6 %' },
  m_foudre: { n: 'L\\'Archimage de foudre', cls: 'mage', st: 2, lv: 30, path: 'foudre', atk: 1.35, hp: 1.2, spd: 1.15, d: 'Voie de la foudre · cadence +15 %' },
  m_brasier: { n: 'L\\'Avatar du Brasier', cls: 'mage', st: 3, lv: 60, path: 'feu', atk: 2.05, hp: 1.5, fx: 'pfeu', splashK: 0.4, d: 'Forme ultime · explosions dévastatrices' },
  m_liche: { n: 'La Liche', cls: 'mage', st: 3, lv: 60, path: 'morts', atk: 1.8, hp: 1.75, fx: 'pmort', leech: 0.12, d: 'Forme ultime · vol de vie +12 %' },
  m_tempete: { n: 'Le Maître des Tempêtes', cls: 'mage', st: 3, lv: 60, path: 'foudre', atk: 1.85, hp: 1.6, spd: 1.3, d: 'Forme ultime · cadence +30 %' },""")
rep("m_sorcier: [] };","m_apprenti: ['m_sorcier'], m_sorcier: ['m_pyro', 'm_necro', 'm_foudre'], m_pyro: ['m_brasier'], m_necro: ['m_liche'], m_foudre: ['m_tempete'], m_brasier: [], m_liche: [], m_tempete: [] };")
rep("mage: { t: 'du sorcier', a: ['m_sorcier'], b: [], c: [], note: '' } };","mage: { t: 'du sorcier', a: ['m_apprenti', 'm_sorcier'], b: ['m_pyro', 'm_necro', 'm_foudre'], c: ['m_brasier', 'm_liche', 'm_tempete'], note: 'Feu : explosions plus larges · Morts : vol de vie · Foudre : cadence de tir.' } };")
rep("Object.assign(H, { n: F.n, key: 'k_' + S.mform, atk: m[0], hp: m[1], spd: 0.9, fx: 'pglace', solid: 0, leech: 0, splash: 1, chill: 0, twin: 0, crit: 0, boss: 0 }); return; }",
    "Object.assign(H, { n: F.n, key: 'k_' + S.mform, atk: m[0], hp: m[1], spd: 0.9 * (F.spd || 1), fx: F.fx || 'pglace', solid: 0, leech: F.leech || 0, splash: 1, splashX: F.splashK || 0, chill: 0, twin: 0, crit: 0, boss: 0 }); return; }")
rep("if (!S.mform) S.mform = 'm_sorcier';","if (!S.mform) S.mform = (S.lvl || 1) >= 15 ? 'm_sorcier' : 'm_apprenti';")
rep("o.bigDmg += 0.08 * tr('c_boss') + (H.boss || 0);","o.bigDmg += 0.08 * tr('c_boss') + (H.boss || 0); o.splashK += H.splashX || 0;")
rep("""(S.cls === 'mage' ? '<small style="color:#ffd890">Ses évolutions arrivent bientôt</small>' : '<small style="color:#ffd890">Forme ultime atteinte</small>')""","""'<small style="color:#ffd890">Forme ultime atteinte</small>'""")
open(P,'w').write(s); print('ok')
