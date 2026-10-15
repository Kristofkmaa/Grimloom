# patch v23 : animation de tir de profil calée sur le moment du tir (le Chasseur tire deux flèches, son shootT est long)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v23' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("else if (anim === 'tir') { f = clamp(Math.floor((1 - Math.max(0, h.shootT) / 0.3) * 4), 0, 3); }",
    "else if (anim === 'tir') { f = clamp(Math.floor((B.t - (h.shotAt || 0)) / 0.32 * 4), 0, 3); }")
s = s.replace('<style id="sv">', '<style id="sv">/* patch v23 */', 1)
open(P, 'w').write(s); print('patch v23 ok')
