# p16 : le Chevalier se bat au corps à corps (coup d'épée, sans projectile), les démons viennent tous au contact
#  le coup touche la cible et entaille les démons collés à elle (50 %) ; les talents « tir multiple / double » deviennent des coups en plus
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p16 chevalier melee' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

rep("  const shot = { X: 0, z: 0.02, h: 78, tg: t, dmg, crit,",
    "  if (S.cls === 'knight') { knightSwing(t, dmg, crit, st, H); return; } // p16 chevalier melee\n  const shot = { X: 0, z: 0.02, h: 78, tg: t, dmg, crit,")
rep("const inRange = () => B.en.some(e => !e.dead && e.spawn <= 0 && e.z < RANGE);",
r"""const inRange = () => B.en.some(e => !e.dead && e.spawn <= 0 && e.z < RANGE);
const MELEE = 0.26, inMelee = () => B.en.some(e => !e.dead && e.spawn <= 0 && e.z < MELEE); // portée de l'épée
function knightSwing(t, dmg, crit, st, H) { // l'impact arrive au milieu du geste (image 2 de l'attaque)
  const extra = (st.multi && Math.random() < st.multi ? 1 : 0) + (st.dbl && (B.dblN = (B.dblN || 0) + 1) % 3 === 0 ? 1 : 0);
  B.mHits = B.mHits || []; B.mHits.push({ at: B.t + 0.15, t, dmg, crit, st, prj: H.prj, extra });
  B.hero.shootT = 0.3; B.hero.altN = (B.hero.altN || 0) + 1; B.hero.shotAt = B.t; }
function meleeTick() { if (!B.mHits || !B.mHits.length) return; const now = B.t, keep = [];
  for (const m of B.mHits) { if (now < m.at) { keep.push(m); continue; } let t = m.t; if (t.dead || t.z > MELEE + 0.1) { const L = alive().filter(e => e.z < MELEE + 0.1); if (!L.length) continue; t = L.reduce((a, b) => b.z < a.z ? b : a); }
    const x = ex(t), y = ey(t) - 18, el = { 1: '#b070ff', 2: '#ff8a30', 3: '#8ad8ff' }[m.prj] || '#ffffff';
    B.fx.push({ k: 'slash', x: x - 10, y, t: 0, d: 0.22, c: el, big: m.crit }); if (m.prj) gfx('imp', m.prj, x, y, 90 * (m.crit ? 1.3 : 1) * 0.62, 0.3);
    hitEnemy(t, m.dmg, m.crit); if (m.st.chill) t.chill = 1.5; B.shake = Math.max(B.shake, m.crit ? 3 : 1.5);
    for (const o of alive()) if (o !== t && Math.abs(o.z - t.z) < 0.14) hitEnemy(o, m.dmg * (m.st.splash ? Math.max(0.5, m.st.splashK) : 0.5), false); // entaille ceux qui sont collés
    const o2 = alive().filter(e => e !== t && e.z < MELEE + 0.1); for (let i = 0; i < m.extra && o2.length; i++) { const e = pick(o2); B.fx.push({ k: 'slash', x: ex(e) - 10, y: ey(e) - 18, t: -0.06, d: 0.22, c: el }); hitEnemy(e, m.dmg, false); } }
  B.mHits = keep; }""")
rep("    if (!B.walk && h.cd <= 0 && inRange()) { heroFire(); h.cd = 1 / st.rate; }",
    "    if (!B.walk && h.cd <= 0 && (S.cls === 'knight' ? inMelee() : inRange())) { heroFire(); h.cd = 1 / st.rate; }\n    meleeTick();")
rep("const stop = e.ranged ? 0.42 : 0.07,", "const stop = e.ranged && S.cls !== 'knight' ? 0.42 : 0.07,") # contre le Chevalier, tout le monde vient au contact
# l'entaille : un arc lumineux en croissant
rep("    if (f.k === 'w') { drawWisp(f); continue; }",
    "    if (f.k === 'w') { drawWisp(f); continue; }\n    if (f.k === 'slash') { const q = clamp(f.t / f.d, 0, 1); if (f.t < 0) continue; const R = f.big ? 34 : 26; ctx.save(); ctx.translate(f.x, f.y); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 1 - q; ctx.strokeStyle = f.c; ctx.lineCap = 'round'; for (const [w, r] of [[7 * (1 - q) + 1, R], [3, R - 5]]) { ctx.lineWidth = w; ctx.beginPath(); ctx.arc(0, 0, r, -1.9 + q * 0.6, -1.9 + 0.6 + q * 2.4); ctx.stroke(); } ctx.restore(); continue; }")
rep("e.kz += 0.04 * (e.boss ? 0.2 : 1);", "") # aucun recul : comme dans Mushroom, les démons avancent quoi qu'il arrive
s = s.replace('<style id="sv">', '<style id="sv">/* p16 chevalier melee */', 1)
open(P, 'w').write(s); print('p16 chevalier melee ok')
