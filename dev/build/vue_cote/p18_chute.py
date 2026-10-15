# p18 : les effets d'ultime et les pouvoirs Lames / Châtiment tombent du haut de l'écran (comme les météores), les dégâts arrivent à l'impact
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p18 chute' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
FALL = 0.26
rep("function hitEnemy(e, dmg, crit) {", "const FALL = %s; // p18 chute : durée de la chute des effets\nfunction hitEnemy(e, dmg, crit) { if (B.hitDelay) { setTimeout(() => hitEnemy(e, dmg, crit), B.hitDelay); return; }" % FALL)
rep("const each = (f, gap) => alive().forEach((e, i) => setTimeout(() => { if (!e.dead) f(e); }, (gap || 0) * i));",
    "const each = (f, gap) => alive().forEach((e, i) => setTimeout(() => { if (!e.dead) { B.hitDelay = FALL * 1000; f(e); B.hitDelay = 0; } }, (gap || 0) * i));")
rep("gfx('ult', row, ex(e), py(e.z) - W2 * 0.875 / 2 + 4 * sOf(e.z), W2, d || 0.6, o); };",
    "gfx('ult', row, ex(e), py(e.z) - W2 * 0.875 / 2 + 4 * sOf(e.z), W2, (d || 0.6) + FALL, Object.assign({ fall: 1 }, o || {})); };")
rep("gfx('spl', 0, ex(e), ey(e), 120 * sOf(e.z), 0.5, { t: -i * 0.06 }); hitEnemy(e, st.atk * k, false); }",
    "gfx('spl', 0, ex(e), ey(e), 120 * sOf(e.z), 0.5 + FALL, { t: -i * 0.06, fall: 1 }); B.hitDelay = (FALL + i * 0.06) * 1000; hitEnemy(e, st.atk * k, false); B.hitDelay = 0; }")
rep("gfx('spl', 6, ex(e), py(e.z) - 50 * sOf(e.z), 200 * sOf(e.z), 0.8); B.shake = Math.max(B.shake, 6); hitEnemy(e, st.atk * k, true); }",
    "gfx('spl', 6, ex(e), py(e.z) - 50 * sOf(e.z), 200 * sOf(e.z), 0.8 + FALL, { fall: 1 }); setTimeout(() => { B.shake = Math.max(B.shake, 6); }, FALL * 1000); B.hitDelay = FALL * 1000; hitEnemy(e, st.atk * k, true); B.hitDelay = 0; }")
rep("    if (f.k === 'g') { const A = ASSETS['fx_' + f.sh]; drawG(",
    "    if (f.k === 'g' && f.fall) { const A = ASSETS['fx_' + f.sh]; if (f.t < FALL) { const q = f.t / FALL, top = -OFFY - f.w * 0.5, yy = f.y - (f.y - top) * (1 - q * q); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.35; for (let k = 1; k <= 3; k++) drawG(f.sh, f.row, 0, f.x, yy - k * 22, f.w * (1 - k * 0.12), 0, 0.25); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; drawG(f.sh, f.row, 0, f.x, yy, f.w, 0, 1); } else { const q = (f.t - FALL) / (f.d - FALL); if (!f.boom) { f.boom = 1; B.shake = Math.max(B.shake, 2); } drawG(f.sh, f.row, q * A.n, f.x, f.y, f.w, 0, Math.min(1, (1 - q) * 3)); } continue; }\n    if (f.k === 'g') { const A = ASSETS['fx_' + f.sh]; drawG(")
s = s.replace('<style id="sv">', '<style id="sv">/* p18 chute */', 1)
open(P, 'w').write(s); print('p18 chute ok')
