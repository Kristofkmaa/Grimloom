# p36 : les familiers marchent au sol derrière le héros (petits bonds), le ciel est laissé au gardien (grosse bête volante)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p36 familiers sol' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const FAMPOS = [[-44, -122], [26, -150], [-20, -176], [62, -118], [88, -168]];", "const FAMPOS = [[-44, 2], [-70, 6], [-92, 1], [-30, 13], [-60, 15]]; // p36 familiers sol : au sol derrière le héros")
rep("P0 = FAMPOS[i], bob = Math.sin(time * 2.4 + i * 1.3) * 5, x = CX + P0[0], y = YF + P0[1] + bob, sz = (52 + F.r * 3) * (i ? 0.8 : 1);",
    "P0 = FAMPOS[i], sz = (40 + F.r * 3) * (i ? 0.85 : 1), hop = Math.abs(Math.sin(time * (B.walk ? 9 : 2.2) + i * 1.3)) * (B.walk ? 7 : 2.5), x = CX + P0[0], y = YF + P0[1] - sz * 0.42 - hop;")
rep("famSync().forEach((id, i) => L.push({ z: 0.05 + i * 0.01, y: YF - 1 - i,", "famSync().forEach((id, i) => L.push({ z: 0.05 + i * 0.01, y: YF + FAMPOS[i][1] - 0.5,")
rep("const GDPOS = [-78, -150];", "const GDPOS = [-56, -168];")
rep("sc = 70 / A.ch, f = Math.floor(time * 8)", "sc = 105 / A.ch, f = Math.floor(time * 8)")
rep("ctx.ellipse(x, YF - 6, 14, 3.5, 0, 0, 7)", "ctx.ellipse(x, YF + FAMPOS[i][1] - 2, 13, 3.5, 0, 0, 7)")
s = s.replace('<style id="sv">', '<style id="sv">/* p36 familiers sol */', 1)
open(P, 'w').write(s); print('p36 familiers sol ok')
