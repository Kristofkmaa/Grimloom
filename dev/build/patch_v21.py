# patch v21 : le Chasseur passe des deux arbalètes à l'arc (textes ; tir double conservé = deux flèches)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v21' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("Un jeune pisteur en cuir usé. Deux arbalètes et beaucoup à prouver.", "Un jeune pisteur en cuir usé. Un arc de frêne et beaucoup à prouver.")
rep("'Deux arbalètes · rapide'", "'Arc · rapide'", 2)
rep("' · cadence ×1.4 · deux carreaux'", "' · cadence ×1.4 · deux flèches'")
rep("base_h: ['Pluie de carreaux', '14 carreaux tombent du ciel (180 % chacun).']", "base_h: ['Pluie de flèches', '14 flèches tombent du ciel (180 % chacun).']")
rep("il tire deux carreaux à chaque attaque", "il décoche deux flèches à chaque attaque")
s = s.replace('<style id="sv">', '<style id="sv">/* patch v21 */', 1)
open(P, 'w').write(s); print('patch v21 ok')
