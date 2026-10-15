# p09 (TEMPORAIRE, à retirer) : dans « Choisis ton héros », toucher n'importe quelle forme la joue directement (test)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p09 test formes' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("""const ev = (k, lv) => `<div class="kt ${k === cur && !nw ? 'cur' : ''}">""", """const ev = (k, lv) => `<div class="kt ${k === cur && !nw ? 'cur' : ''}" data-tf="${k}" style="cursor:pointer">""")
rep("""    <h4 class="kh">Ses évolutions</h4>""", """    <h4 class="kh">Ses évolutions <small style="color:#ff8a8a">TEST : touche une forme pour la jouer</small></h4>""")
rep("""    el.querySelectorAll('[data-tc]').forEach(b => b.onclick = () => { TCLS = b.dataset.tc; titleView(); el.scrollTop = 0; });""",
"""    el.querySelectorAll('[data-tc]').forEach(b => b.onclick = () => { TCLS = b.dataset.tc; titleView(); el.scrollTop = 0; });
    el.querySelectorAll('[data-tf]').forEach(b => b.onclick = () => { const k = b.dataset.tf; S.cls = c; if (c === 'hunter') S.hform = k; else if (c === 'mage') S.mform = k; else S.form = k; applyEvo(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; S.started = 1; save(); titleClose(); toast('Test : ' + EVO[k].n); }); // p09 TEST""")
s = s.replace('<style id="sv">', '<style id="sv">/* p09 test formes */', 1)
open(P, 'w').write(s); print('p09 test formes ok')
