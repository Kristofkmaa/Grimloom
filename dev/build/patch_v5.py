P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v5.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

# ---------- calcul de l'éveil ----------
rep("function drawHero(time) {", r'''// Éveil : le héros change d'apparence selon son équipement
// arme -> projectiles ; autres pièces (rareté moyenne) -> aura, contour lumineux, colonne de lumière, couronne
function gear() {
  const w = S.eq.arme ? S.eq.arme.r : -1, ar = SLOTS.filter(q => q.id !== 'arme').map(q => S.eq[q.id] ? S.eq[q.id].r + 1 : 0);
  return { w, a: Math.floor(ar.reduce((x, y) => x + y, 0) / ar.length + 1e-6) - 1 };
}
const EVEIL = [[2, 'Cercle runique sous les pieds'], [3, 'Âmes qui s\'élèvent autour du héros'], [4, 'Contour de lumière'], [5, 'Colonne de lumière'], [6, 'Couronne divine']];
const HS = document.createElement('canvas'), HG = HS.getContext('2d');
function heroSil(key, anim, fr, x, y, sc, col, alpha, grow) { // silhouette teintée du héros, pour le contour lumineux
  const A = ASSETS[key], R = A.anims[anim]; if (!R) return; const i = Math.max(0, Math.floor(fr)) % R.n;
  if (HS.width !== A.cw || HS.height !== A.ch) { HS.width = A.cw; HS.height = A.ch; }
  HG.globalCompositeOperation = 'copy'; HG.drawImage(IMG[key], i * A.cw, R.row * A.ch, A.cw, A.ch, 0, 0, A.cw, A.ch); HG.globalCompositeOperation = 'source-in'; HG.fillStyle = col; HG.fillRect(0, 0, A.cw, A.ch);
  const w = A.cw * sc, h = A.ch * sc; ctx.save(); ctx.globalAlpha = alpha; ctx.imageSmoothingEnabled = false;
  for (const [dx, dy] of [[-grow, 0], [grow, 0], [0, -grow], [0, grow]]) ctx.drawImage(HS, Math.round(x - w / 2 + dx), Math.round(y - h + A.foot * sc + dy), w, h);
  ctx.restore();
}
function drawHero(time) {''')

rep("""  ctx.fillStyle = 'rgba(0,0,0,.4)'; ctx.beginPath(); ctx.ellipse(CX, YF, 22, 6, 0, 0, TAU); ctx.fill();
  sprH(H.key, anim + '_' + di, fr, CX, YF, H.sc);""", """  const G = B.gear || gear(), ga = G.a, gc = ga >= 0 ? RAR[ga].c : '#fff', sc = H.sc * (1 + 0.035 * Math.max(0, ga)), key = anim + '_' + di;
  ctx.fillStyle = 'rgba(0,0,0,.4)'; ctx.beginPath(); ctx.ellipse(CX, YF, 22, 6, 0, 0, TAU); ctx.fill();
  if (ga >= 5) { const gr = ctx.createLinearGradient(0, YF - 170, 0, YF); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, gc); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.22 + Math.sin(time * 3) * 0.06; ctx.fillStyle = gr; ctx.fillRect(CX - 26, YF - 170, 52, 170); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; }
  if (ga >= 2) { // cercle runique qui tourne
    ctx.save(); ctx.translate(CX, YF); ctx.scale(1, 0.32); ctx.rotate(time * 0.8); ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = gc; ctx.globalAlpha = 0.55; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(0, 0, 34, 0, TAU); ctx.stroke(); ctx.setLineDash([6, 8]); ctx.beginPath(); ctx.arc(0, 0, 27, 0, TAU); ctx.stroke(); ctx.setLineDash([]);
    for (let i = 0; i < 6; i++) { const a = i * TAU / 6; ctx.fillStyle = gc; ctx.fillRect(Math.cos(a) * 34 - 2, Math.sin(a) * 34 - 2, 4, 4); }
    ctx.restore(); ctx.globalCompositeOperation = 'lighter'; glow(CX, YF - 4, 40, gc, 0.25); ctx.globalCompositeOperation = 'source-over';
  }
  if (ga >= 4) { ctx.globalCompositeOperation = 'lighter'; heroSil(H.key, key, fr, CX, YF, sc, gc, 0.55 + Math.sin(time * 4) * 0.15, 1.6); ctx.globalCompositeOperation = 'source-over'; }
  sprH(H.key, key, fr, CX, YF, sc);
  if (ga >= 6) { ctx.save(); ctx.translate(CX, YF - 78 * sc / H.sc + Math.sin(time * 2) * 2); ctx.scale(1, 0.35); ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = '#ffe680'; ctx.lineWidth = 3; ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(0, 0, 12, 0, TAU); ctx.stroke(); ctx.restore(); ctx.globalCompositeOperation = 'lighter'; glow(CX, YF - 78 * sc / H.sc, 22, '#ffe680', 0.4); ctx.globalCompositeOperation = 'source-over'; }""")

# particules d'âmes + traînées des projectiles
rep("  placeDeco();\n  const bi = biome();", """  placeDeco();
  { const G = B.gear || gear(); if (G.a >= 3 && Math.random() < dt * (4 + G.a * 3)) { const c = RAR[G.a].c; B.fx.push({ k: 'p', x: CX + rand(-26, 26), y: YF - rand(0, 20), vx: rand(-5, 5), vy: rand(-45, -20), g: -6, c: Math.random() < 0.3 ? '#fff' : c, t: 0, d: rand(0.8, 1.5), r: rand(0.7, 1.4) }); }
    for (const sh of B.shots) if (sh.wr >= 2 && Math.random() < dt * 30) B.fx.push({ k: 'p', x: sx(sh.X, sh.z) + rand(-2, 2), y: py(sh.z) - sh.h * sOf(sh.z) + rand(-2, 2), vx: 0, vy: 0, g: 0, c: RAR[sh.wr].c, t: 0, d: 0.35, r: 1.2 * sOf(sh.z) + 0.4 }); }
  const bi = biome();""")
rep("B.shots.push({ X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: H.splash, chill: H.chill });",
    "B.shots.push({ X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: H.splash, chill: H.chill, wr: (B.gear || gear()).w });")
rep("drawFx(s.fx, s.fx === 'arc' ? 6 : (s.t * 24) % 15, x, y, a, (s.fx === 'fleche' ? 54 : 64) * sc); if (!s.solid) glow(x, y, 20 * sc, 'rgba(255,120,80,1)', 0.5);",
    "const big = 1 + Math.max(0, s.wr) * 0.12; if (s.wr >= 1) { ctx.globalCompositeOperation = 'lighter'; glow(x, y, (14 + s.wr * 4) * sc, RAR[s.wr].c, 0.35 + s.wr * 0.06); ctx.globalCompositeOperation = s.solid ? 'source-over' : 'lighter'; } drawFx(s.fx, s.fx === 'arc' ? 6 : (s.t * 24) % 15, x, y, a, (s.fx === 'fleche' ? 54 : 64) * sc * big); if (!s.solid) glow(x, y, 20 * sc, 'rgba(255,120,80,1)', 0.5);")
rep("s.dead = 1; burst(sx(s.X, s.z), py(s.z) - s.h * sOf(s.z), '#ffd0a0', 3, 80);", "s.dead = 1; burst(sx(s.X, s.z), py(s.z) - s.h * sOf(s.z), s.wr >= 1 ? RAR[s.wr].c : '#ffd0a0', 3 + Math.max(0, s.wr) * 2, 80 + Math.max(0, s.wr) * 20);")

# mise à jour du cache quand l'équipement change
rep("function closeM() { $('modal').hidden = true; save();", "function closeM() { $('modal').hidden = true; save(); B.gear = gear();")
rep("function ui() {\n  uiTop();", "function ui() {\n  B.gear = gear(); uiTop();")

# onglet Héros : section Éveil
rep("""    <h3 style="margin-top:16px">Choisir le héros</h3>""", """    <h3 style="margin-top:16px">Éveil</h3><p style="margin:0 0 8px;color:var(--dim);font:700 12px/1.4 var(--b)">Ton arme change tes tirs. La rareté moyenne de tes 7 autres pièces fait évoluer ton héros.</p>
    <div class="eveil">${(() => { const G = gear(); return `<div class="ev on" style="--c:${G.w >= 0 ? RAR[G.w].c : '#6a3a48'}"><b>Arme ${G.w >= 0 ? RAR[G.w].n.toLowerCase() : '—'}</b><span>${G.w >= 0 ? 'Tirs plus gros, lueur et traînée de sa couleur' : 'Équipe une arme'}</span></div>` + EVEIL.map(([r, t]) => `<div class="ev ${G.a >= r ? 'on' : ''}" style="--c:${RAR[r].c}"><b>${RAR[r].n}</b><span>${t}</span>${G.a >= r ? '' : IC.lock}</div>`).join(''); })()}</div>
    <h3 style="margin-top:16px">Choisir le héros</h3>""")
rep(".soon{padding:22px 16px;text-align:center}", """.soon{padding:22px 16px;text-align:center}
.eveil{display:grid;gap:6px}
.ev{display:grid;grid-template-columns:96px 1fr auto;align-items:center;gap:8px;padding:8px 10px;border-radius:10px;background:#ffffff06;border:1.5px solid #ffffff10;font:700 12px var(--b);color:var(--dim)}
.ev b{font:400 14px var(--n);color:var(--c)}
.ev.on{border-color:var(--c);background:linear-gradient(90deg,color-mix(in srgb,var(--c) 22%,transparent),transparent);color:var(--txt);box-shadow:0 0 12px -6px var(--c)}
.ev svg{opacity:.5}""")

open(P, 'w').write(s)
print('ok')
s = open(P).read()
rep("for (const sl of SLOTS) S.eq[sl.id] = makeItem(r, sl); save();", "for (const sl of SLOTS) S.eq[sl.id] = makeItem(r, sl); save(); B.gear = gear();")
rep("god: () => B.god = !B.god, one: () => B.oneshot = !B.oneshot, strip: () => S.eq = {},", "god: () => B.god = !B.god, one: () => B.oneshot = !B.oneshot, strip: () => { S.eq = {}; B.gear = gear(); },")
open(P, 'w').write(s); print('ok2')
