import json
P='/home/claude/grimloom/src.html'; s=open(P).read()
def rep(a,b,c=1):
    global s
    assert s.count(a)==c,(s.count(a),a[:100]); s=s.replace(a,b)
fx=json.load(open('/home/claude/grimloom/fxart/fx.json'))
load=''.join(f"ASSETS.fx_{k} = {{ src: 'data:image/png;base64,{v['b64']}', cw: {v['cw']}, ch: {v['ch']}, n: {v['n']} }};\n" for k,v in fx.items())
rep("for (const k in ASSETS) if (ASSETS[k].src) {", load+"for (const k in ASSETS) if (ASSETS[k].src) {")
# helpers
rep("function sfx(id, x, y, w, d, a) {","""// effets ChatGPT : fx_prj (projectiles en boucle), fx_imp (impacts), fx_spl (pouvoirs). Lignes = type.
function gfx(sh, row, x, y, w, d, o) { B.fx.push(Object.assign({ k: 'g', sh, row, x, y, w, t: 0, d }, o || {})); }
function drawG(sh, row, fr, x, y, w, a, alpha) { const A = ASSETS['fx_' + sh], im = IMG['fx_' + sh]; if (!A || !im || !im.complete) return; const i = clamp(Math.floor(fr), 0, A.n - 1), h = w * A.ch / A.cw; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(x, y); if (a) ctx.rotate(a); if (alpha !== undefined) ctx.globalAlpha = alpha; ctx.drawImage(im, i * A.cw, row * A.ch, A.cw, A.ch, -w / 2, -h / 2, w, h); ctx.restore(); }
function sfx(id, x, y, w, d, a) {""")
rep("if (f.k === 'p') { ctx.globalAlpha = 1 - p;","if (f.k === 'g') { const A = ASSETS['fx_' + f.sh]; drawG(f.sh, f.row, f.loop ? 1 + (f.t * 10) % 3 : p * A.n, f.x, f.y, f.w, f.a || 0, f.loop ? Math.min(1, (1 - p) * 4) * (f.al || 1) : Math.min(1, (1 - p) * 3)); continue; } if (f.k === 'p') { ctx.globalAlpha = 1 - p;")
# projectiles
rep("drawFx(s.fx, s.fx === 'arc' ? 6 : (s.t * 24) % 15, x, y, a, (s.fx === 'fleche' ? 54 : 64) * sc * big);",
    "if (s.prj !== undefined) drawG('prj', s.prj, (s.t * 14) % 4, x, y, a, 0) || drawG('prj', s.prj, (s.t * 14) % 4, x, y, (s.prj === 4 ? 78 : 92) * sc * big, a); else drawFx(s.fx, s.fx === 'arc' ? 6 : (s.t * 24) % 15, x, y, a, (s.fx === 'fleche' ? 54 : 64) * sc * big);")
rep("if (!s.solid) glow(x, y, 20 * sc, 'rgba(255,120,80,1)', 0.5); ctx.globalCompositeOperation = 'source-over'; }","if (!s.solid && s.prj === undefined) glow(x, y, 20 * sc, 'rgba(255,120,80,1)', 0.5); ctx.globalCompositeOperation = 'source-over'; }")
rep("const shot = { X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid,","const shot = { X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, prj: H.prj, solid: H.solid,")
# impacts
rep("if (!e.dead) { hitEnemy(e, s.dmg, s.crit); if (s.comp === 'paladin')","if (!e.dead) { if (s.prj !== undefined) gfx('imp', s.prj, sx(e.X, e.z), py(e.z) - 26 * sOf(e.z), (s.splash ? 150 : 84) * sOf(e.z) * (s.crit ? 1.3 : 1), s.splash ? 0.45 : 0.32); hitEnemy(e, s.dmg, s.crit); if (s.comp === 'paladin')")
rep("if (s.splash) { sfx('feu', sx(e.X, e.z), py(e.z) - 20 * sOf(e.z), 80 * sOf(e.z), 0.35);","if (s.splash) { if (s.prj === undefined) sfx('feu', sx(e.X, e.z), py(e.z) - 20 * sOf(e.z), 80 * sOf(e.z), 0.35);")
rep("s.dead = 1; burst(sx(s.X, s.z), py(s.z) - s.h * sOf(s.z), s.wr >= 1 ? RAR[s.wr].c : '#ffd0a0', 3 + Math.max(0, s.wr) * 2, 80 + Math.max(0, s.wr) * 20); }",
    "s.dead = 1; if (s.prj === undefined || s.wr >= 1) burst(sx(s.X, s.z), py(s.z) - s.h * sOf(s.z), s.wr >= 1 ? RAR[s.wr].c : '#ffd0a0', 3 + Math.max(0, s.wr) * 2, 80 + Math.max(0, s.wr) * 20); }")
# index de projectile par classe / forme
rep("Object.assign(H, { n: F.n, key: 'k_' + S.mform,","Object.assign(H, { prj: { pfeu: 6, pmort: 7 }[F.fx] || (F.path === 'foudre' ? 8 : 5), n: F.n, key: 'k_' + S.mform,")
rep("Object.assign(H, { n: F.n, key: 'k_' + S.hform,","Object.assign(H, { prj: 4, n: F.n, key: 'k_' + S.hform,")
rep("Object.assign(H, { n: E.n, key: 'k_' + S.form,","Object.assign(H, { prj: { pmort: 1, pfeu: 2, pglace: 3 }[E.fx] || 0, n: E.n, key: 'k_' + S.form,")
# pouvoirs
rep("sfx('epee', ex(e), ey(e), 80 * sOf(e.z), 0.3, rand(0, TAU)); hitEnemy(e, st.atk * k, false); }","gfx('spl', 0, ex(e), ey(e), 120 * sOf(e.z), 0.5, { t: -i * 0.06 }); hitEnemy(e, st.atk * k, false); }")
rep("else if (id === 'shield') B.shield = Math.max(B.shield || 0, B.hero.hpMax * k / 6);","else if (id === 'shield') { B.shield = Math.max(B.shield || 0, B.hero.hpMax * k / 6); gfx('spl', 1, CX, YF - 50, 170, 0.7); }")
rep("    B.fx.push({ k: 'streak', x: tx + 60, y: ty - 160, x2: tx, y2: ty, t: -i * 0.07, d: 0.35, c: '#ffb040' });\n    setTimeout(() => { if (!e.dead) { sfx('feu', tx, ty, 110 * sOf(e.z), 0.45);",
    "    gfx('spl', 2, tx - 10 * sOf(e.z), ty - 30 * sOf(e.z), 190 * sOf(e.z), 0.7, { t: -i * 0.07 });\n    setTimeout(() => { if (!e.dead) {")
rep("else if (id === 'nova') { freezeAll(2); for (const e of L) { sfx('glace', ex(e), ey(e), 80 * sOf(e.z), 0.4); hitEnemy(e, st.atk * k, false); } }",
    "else if (id === 'nova') { freezeAll(2); gfx('spl', 3, CX, YF - 20, 420, 0.7); for (const e of L) { gfx('imp', 3, ex(e), ey(e), 90 * sOf(e.z), 0.4); hitEnemy(e, st.atk * k, false); } }")
rep("B.fx.push({ k: 'bolt', pts, t: 0, d: 0.35 }); }","B.fx.push({ k: 'bolt', pts, t: 0, d: 0.35 }); pts.slice(1).forEach((q, j) => gfx('spl', 4, q[0], q[1], 130, 0.45, { t: -j * 0.04 })); }")
rep("for (let i = 0; i < 6; i++) B.fx.push({ k: 'p', x: rand(40, BW - 40), y: rand(py(0.9), py(0.1)), vx: rand(-8, 8), vy: rand(-14, -4), g: 0, c: pick(['#7aff5a', '#3ad04a', '#b0ff80']), t: 0, d: 1, r: rand(1.5, 3) }); }",
    "const PL = alive(); for (let i = 0; i < Math.min(3, PL.length); i++) { const e = pick(PL); gfx('spl', 5, ex(e), ey(e) - 10 * sOf(e.z), 150 * sOf(e.z), 0.9); } }")
rep("B.fx.push({ k: 'pillar', x: ex(e), y: py(e.z), t: 0, d: 0.7 });","gfx('spl', 6, ex(e), py(e.z) - 50 * sOf(e.z), 200 * sOf(e.z), 0.8);")
rep("else if (id === 'frenzy') { B.spFrT = 6; B.spFrK = spPct(id) / 300; }","else if (id === 'frenzy') { B.spFrT = 6; B.spFrK = spPct(id) / 300; gfx('spl', 7, CX, YF - 30, 190, 0.7); }")
# aura de frénésie et bouclier persistants
rep("  if (B.frenzyT > 0 || B.spFrT > 0) { ctx.globalCompositeOperation = 'lighter';","  if (B.spFrT > 0.4) drawG('spl', 7, 1 + (time * 9) % 3, CX, YF - 30, 170, 0, 0.45);\n  if (B.shield > 0) drawG('spl', 1, 2 + (time * 3) % 2, CX, YF - 50, 150, 0, 0.32);\n  if (B.frenzyT > 0 || B.spFrT > 0) { ctx.globalCompositeOperation = 'lighter';")
open(P,'w').write(s); print('ok')
