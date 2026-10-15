# patch v25 : le héros n'engage le combat que quand les démons arrivent vers le milieu de l'écran (RANGE)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v25' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const alive = () => B.en.filter(e => !e.dead && e.spawn <= 0);",
    "const alive = () => B.en.filter(e => !e.dead && e.spawn <= 0);\nconst RANGE = 0.36; // patch v25 : distance d'engagement (~milieu de l'écran)\nconst inRange = () => B.en.some(e => !e.dead && e.spawn <= 0 && e.z < RANGE);")
rep("B.en.some(e => !e.dead && e.spawn <= 0 && e.z < 1.05)) { heroFire();", "inRange()) { heroFire();")
rep("const t = alive.reduce((a, b) => (b.z + Math.abs(b.X) * 0.2 < a.z + Math.abs(a.X) * 0.2 ? b : a));",
    "const t = alive.reduce((a, b) => (b.z < a.z ? b : a));")
rep("const stop = e.ranged ? 0.42 : 0.07,", "const stop = e.ranged ? 0.28 : 0.07,")
rep("const h = B.hero, fighting = !B.walk && !h.dead && B.wave && alive().length > 0, st = heroStats();",
    "const h = B.hero, fighting = !B.walk && !h.dead && (B.wave || B.dun) && inRange(), st = heroStats();")
rep("if (!B.hero.dead && alive().length) ultGain(100 / ULT_CD * dt);", "if (!B.hero.dead && fighting) ultGain(100 / ULT_CD * dt);")
rep("if ((B.ult || 0) >= 100 && B.ultFullT && S.ultAuto !== false", "if (fighting && (B.ult || 0) >= 100 && B.ultFullT && S.ultAuto !== false")
rep("e.z -= sp * dt * (e.z > 1 ? 2.4 : 1);", "e.z -= sp * dt * (e.z > 1.1 ? 3.2 : e.z > RANGE ? 1.7 : 1);")
s = s.replace('<style id="sv">', '<style id="sv">/* patch v25 */', 1)
open(P, 'w').write(s); print('patch v25 ok')
