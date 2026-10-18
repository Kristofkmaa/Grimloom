# p30 : équilibrage (d'après une simulation de joueur qui n'ouvre que des coffres)
#  - le niveau du héros donne +3 % d'attaque et de PV par niveau (avant : aucun effet direct)
#  - quand on farme (étape déjà faite / repli), un démon tué donne une clé une fois sur trois : on n'est plus bloqué sans clés devant un boss
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p30 equilibrage' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("  const atk = t.atk * (1 + t.atkp / 100) * H.atk, pv = t.pv * (1 + t.pvp / 100) * H.hp;",
    "  const LV = 1 + 0.03 * Math.max(0, (S.lvl || 1) - 1), atk = t.atk * (1 + t.atkp / 100) * H.atk * LV, pv = t.pv * (1 + t.pvp / 100) * H.hp * LV; // p30 equilibrage")
rep("function hamNewKill(e) { if (PS() === 10 && !(B.wave && B.wave.boss)) return 0; if (B.dun || S.farm || stageIndex() < S.best) return 0;",
    "function hamNewKill(e) { if (PS() === 10 && !(B.wave && B.wave.boss)) return 0; if (B.dun) return 0; if (S.farm || stageIndex() < S.best) { if (Math.random() < 1 / 3) { S.ham += 1; return 1; } return 0; }")
s = s.replace('<style id="sv">', '<style id="sv">/* p30 equilibrage */', 1)
open(P, 'w').write(s); print('p30 equilibrage ok')
