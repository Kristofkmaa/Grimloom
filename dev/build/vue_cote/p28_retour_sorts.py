# p28 : écran « Bon retour ! » (le coffre de temps récolté d'un geste) + pouvoirs plus lisibles (onde et éclair de couleur au lancement)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p28 retour sorts' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
# --- retour ---
rep("  if (away > 600 && (Date.now() - S.afkT) / 1000 > 1800) setTimeout(() => toast('Ton coffre de temps s\\'est rempli pendant ton absence'), 1500);",
    "  if (away > 600 && featOK('coffre') && afkCalc().sec > 600) q.push(next => backScreen(next)); // p28 retour sorts")
rep("let WQ = null;", r"""let WQ = null;
function backScreen(next) { const r = afkCalc(), h = Math.floor(r.sec / 3600), m = Math.floor(r.sec % 3600 / 60);
  dunScreen({ win: true, mode: 'Coffre de temps', title: 'Bon retour !', sub: `Ton héros a combattu pendant ${h ? h + ' h ' : ''}${m} min${r.sec >= AFK_MAX ? ' (coffre plein)' : ''}`, btn: 'Récolter',
    rows: [['coin', '#ffc23a', `+${fmt(r.gold)} or`], ['ham', '#e8dcc8', `+${fmt(r.ham)} clés`], ['book', '#ff9a6a', `+${fmt(r.pages)} pages`], ['star', '#7aff9a', `+${fmt(r.xp)} XP`]].filter(x => !/^\+0 /.test(x[2])),
    back: () => { const r2 = afkCalc(); S.gold += r2.gold; S.ham += r2.ham; S.pages += r2.pages; gainXP(r2.xp); S.afkT = Date.now(); passAdd(Math.round(r2.sec / 600)); save(); ui(); sfxPlay('reward'); if (next) next(); } }); }""")
rep("""<button class="btn gold" type="button" id="deBack">Retour à l'aventure</button>""", """<button class="btn gold" type="button" id="deBack">${o.btn || 'Retour à l\\'aventure'}</button>""")
# --- pouvoirs : onde de couleur, éclair d'écran, nom plus visible ---
rep("B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1);",
    "{ B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); B.fx.push({ k: 'ring2', x: CX, y: YF - 18, t: 0, d: 0.55, c: sp.c, r: 90 }); const rgb = [1, 3, 5].map(i => parseInt(sp.c.slice(i, i + 2), 16)).join(','); B.flash = { c: rgb, t: 0.22, a: 0.16 }; num(CX + 20, YF - 118, sp.n, sp.c, 1.05); B.shake = Math.max(B.shake, 2); }")
s = s.replace('<style id="sv">', '<style id="sv">/* p28 retour sorts */', 1)
open(P, 'w').write(s); print('p28 retour sorts ok')
