# patch v22 : héros de profil plus grand (+25 %), démons qui s'arrêtent un peu plus loin
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v22' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const im = SIDEI[curForm()], sc = 0.69 * (SA.k || 1);", "const im = SIDEI[curForm()], sc = HSC * 0.69 * (SA.k || 1);")
s = s.replace("<style id=\"sv\">", "<style id=\"sv\">/* patch v22 */", 1)
rep("const sideHero = () =>", "const HSC = 1.25; // taille du héros de profil\nconst sideHero = () =>")
rep("sx = (X, z) => CX + 30 + z * ZW;", "sx = (X, z) => CX + 46 + z * ZW;")
rep("ws = 0.5; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(CX - 8, YF - 70);", "ws = 0.62; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(CX - 10, YF - 88);", 2)
rep("x = CX - 32, y = YF - 76 + bob, sz = 48 + F.r * 3;", "x = CX - 62, y = YF - 112 + bob, sz = 52 + F.r * 3;")
rep("h: 64, tg: t", "h: 78, tg: t")
rep("X: (i ? -1 : 1) * 0.06, h: 56", "X: (i ? -1 : 1) * 0.06, h: 68")
open(P, 'w').write(s); print('patch v22 ok')
