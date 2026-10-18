# p26 : sensations de combat
#  - arrivée des boss : bandeau sombre, nom en grand, rugissement, tremblement ; barre de vie avec le nom au-dessus du boss
#  - impacts : micro-pause sur les critiques, chiffres qui « sautent » (critiques plus gros, dorés)
#  - morts : onde + âmes à la couleur du biome, pièces d'or qui volent vers le compteur d'or
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p26 sensations' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

# --- boss : intro ---
rep("spawnEnemy(bo.key, 0, 1.45, st, true); B.banner = { a: 'Boss', b: bo.n, t: 2.2 }; }",
    "spawnEnemy(bo.key, 0, 1.45, st, true); bossIntro(bo.n, `Chapitre ${PC()} · ${biome().n}`); }")
rep("function spawnTick(dt) {", r"""function bossIntro(n, sub) { B.bossIn = { t: 0, n, sub }; B.banner = null; B.shake = Math.max(B.shake, 9); sfxPlay('roar'); const e = B.en[B.en.length - 1]; if (e) e.bossName = n; } // p26 sensations
function drawBossIntro() { const I = B.bossIn; if (!I) return; const D = 2.4, t = I.t; if (t > D) { B.bossIn = null; return; }
  const a = t < 0.25 ? t / 0.25 : t > D - 0.4 ? (D - t) / 0.4 : 1, y = YF - 130, slide = t < 0.3 ? (1 - t / 0.3) * 60 : 0;
  ctx.save(); ctx.globalAlpha = a * 0.75; const g = ctx.createLinearGradient(0, y - 40, 0, y + 40); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(0.25, 'rgba(10,0,4,.92)'); g.addColorStop(0.75, 'rgba(10,0,4,.92)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, y - 40, BW, 80);
  ctx.globalAlpha = a; ctx.fillStyle = '#c0142a'; ctx.fillRect(0, y - 27, BW, 1.5); ctx.fillRect(0, y + 26, BW, 1.5);
  ctx.textAlign = 'center'; ctx.font = '800 10px Nunito, sans-serif'; ctx.fillStyle = '#ff5a6a'; ctx.fillText('B O S S', BW / 2 - slide, y - 13);
  ctx.font = '900 22px Cinzel, serif'; const tw = ctx.measureText(I.n).width; if (tw > 220) ctx.font = `900 ${Math.floor(22 * 220 / tw)}px Cinzel, serif`; ctx.lineWidth = 5; ctx.strokeStyle = '#000'; ctx.shadowColor = '#ff2030'; ctx.shadowBlur = 14; ctx.strokeText(I.n, BW / 2 + slide, y + 10); ctx.fillStyle = '#ffd890'; ctx.fillText(I.n, BW / 2 + slide, y + 10); ctx.shadowBlur = 0;
  ctx.font = '700 9.5px Nunito, sans-serif'; ctx.fillStyle = '#d8b8a8'; ctx.fillText(I.sub, BW / 2, y + 23); ctx.restore(); }
function spawnTick(dt) {""")
rep("  if (B.banner) { const a = Math.min(1, B.banner.t * 2);", "  drawBossIntro();\n  if (B.banner) { const a = Math.min(1, B.banner.t * 2);")
# temps : intro, micro-pause
rep("function update(dt) {\n", "function update(dt) {\n  if (B.bossIn) B.bossIn.t += dt; if (B.hs > 0) { B.hs -= dt; dt *= 0.12; }\n")
# barre de vie du boss au-dessus de sa tête, avec son nom
rep("  if (!e.dead && e.spawn <= 0 && !e.boss) {", r"""  if (!e.dead && e.spawn <= 0 && e.boss && !e.raid) { const w = 96, hy = y - A.bh * sc - 12, f = clamp(e.hp / e.max, 0, 1); e.hpS = e.hpS === undefined ? f : e.hpS + (f - e.hpS) * 0.08;
    ctx.fillStyle = 'rgba(0,0,0,.75)'; ctx.fillRect(x - w / 2 - 2, hy - 2, w + 4, 9); ctx.fillStyle = '#ffffffaa'; ctx.fillRect(x - w / 2, hy, w * e.hpS, 5); ctx.fillStyle = e.enraged ? '#ff3020' : '#d01830'; ctx.fillRect(x - w / 2, hy, w * f, 5); ctx.strokeStyle = '#c8964a'; ctx.lineWidth = 1; ctx.strokeRect(x - w / 2 - 1.5, hy - 1.5, w + 3, 8);
    if (e.bossName) { ctx.textAlign = 'center'; ctx.font = '900 9px Cinzel, serif'; ctx.lineWidth = 3; ctx.strokeStyle = '#000'; ctx.strokeText(e.bossName, x, hy - 5); ctx.fillStyle = '#ffd890'; ctx.fillText(e.bossName, x, hy - 5); } }
  if (!e.dead && e.spawn <= 0 && !e.boss) {""")
# --- impacts ---
rep("if (e.flash > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: (e.raid ? 0.18 : 0.75) * al,", "if (e.flash > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: (e.raid ? 0.18 : A.hd ? (e.boss ? 0.22 : 0.4) : 0.75) * al * Math.min(1, e.flash * 12),")
rep("  sfxPlay(crit ? 'crit' : 'hit'); num(", "  if (crit && B.t - (B.hsT || -9) > 0.45) { B.hs = 0.06; B.hsT = B.t; }\n  sfxPlay(crit ? 'crit' : 'hit'); num(")
rep("ctx.textAlign = 'center'; for (const n of B.nums) { const p = n.t / 0.8; ctx.globalAlpha = p > 0.6 ? (1 - p) / 0.4 : 1; ctx.font = (n.k > 1.1 ? 22 : 15) + 'px Lilita, sans-serif'; ctx.lineWidth = 3; ctx.strokeStyle = '#000'; ctx.strokeText(n.s, n.x, n.y - p * 24); ctx.fillStyle = n.c; ctx.fillText(n.s, n.x, n.y - p * 24); } ctx.globalAlpha = 1;",
    r"""ctx.textAlign = 'center'; for (const n of B.nums) { const p = n.t / 0.8, big = n.k > 1.1, pop = n.t < 0.14 ? 1 + (1 - n.t / 0.14) * (big ? 0.9 : 0.45) : 1, dx = (n.vx === undefined ? (n.vx = rand(-14, 14)) : n.vx) * p;
    ctx.save(); ctx.globalAlpha = p > 0.6 ? (1 - p) / 0.4 : 1; ctx.translate(n.x + dx, n.y - p * 26 - (big ? 6 : 0)); ctx.scale(pop, pop); ctx.font = (big ? 23 : n.k < 1 ? 12 : 15) + 'px Lilita, sans-serif'; ctx.lineJoin = 'round'; ctx.lineWidth = big ? 4.5 : 3; ctx.strokeStyle = big ? '#3a0a00' : '#000'; ctx.strokeText(n.s, 0, 0);
    if (big) { const g = ctx.createLinearGradient(0, -16, 0, 2); g.addColorStop(0, '#fff6b0'); g.addColorStop(0.5, '#ffd23a'); g.addColorStop(1, '#ff7a1a'); ctx.fillStyle = g; ctx.shadowColor = '#ff8a20'; ctx.shadowBlur = 8; } else ctx.fillStyle = n.c;
    ctx.fillText(n.s, 0, 0); ctx.restore(); } ctx.globalAlpha = 1;""")
# --- morts ---
rep("num(sx(e.X, e.z), py(e.z) - 70 * sOf(e.z), '+' + fmt(g), '#ffc46a', 1); burst(sx(e.X, e.z), py(e.z) - 20 * sOf(e.z), '#c2142a', e.boss ? 40 : 12, 220);",
    "num(sx(e.X, e.z), py(e.z) - 70 * sOf(e.z), '+' + fmt(g), '#ffc46a', 0.85); burst(sx(e.X, e.z), py(e.z) - 20 * sOf(e.z), '#c2142a', e.boss ? 40 : 12, 220); deathFx(e); coinFly(sx(e.X, e.z), py(e.z) - 30 * sOf(e.z), e.boss ? 8 : e.elite ? 4 : 1);")
rep("function burst(x, y, c, n, sp) {", r"""function deathFx(e) { const x = sx(e.X, e.z), y = py(e.z) - 26 * sOf(e.z), c = (B.dun && B.dun.raid) ? '#ff3040' : biome().rune || '#ff3040', big = e.boss ? 2.2 : e.elite ? 1.4 : 1;
  B.fx.push({ k: 'ring2', x, y, t: 0, d: 0.45, c, r: 34 * big }); for (let i = 0; i < (e.boss ? 14 : 5); i++) B.fx.push({ k: 'p', x: x + rand(-10, 10) * big, y: y + rand(-14, 8) * big, vx: rand(-12, 12), vy: rand(-70, -35), g: 0, c, t: 0, d: rand(0.6, 1.1), r: rand(1.2, 2.4) }); }
let COINS = 0;
function coinFly(x, y, n) { const tg = $('goldD'), r = cv.getBoundingClientRect(); if (!tg || !r.width || document.hidden || COINS > 14) return; const k = r.width / BW, tr = tg.getBoundingClientRect(), tx = tr.left + 14, ty = tr.top + tr.height / 2;
  for (let i = 0; i < n; i++) { const el = document.createElement('i'); el.className = 'coinfly'; const x0 = r.left + x * k + rand(-8, 8), y0 = r.top + (y + OFFY) * k + rand(-8, 8); el.style.left = x0 + 'px'; el.style.top = y0 + 'px'; document.body.appendChild(el); COINS++;
    const up = rand(30, 60), a = el.animate([{ transform: 'translate(0,0) scale(.6)' }, { transform: `translate(${rand(-20, 20)}px,${-up}px) scale(1.1)`, offset: 0.3 }, { transform: `translate(${tx - x0}px,${ty - y0}px) scale(.7)` }], { duration: 650 + i * 60, easing: 'cubic-bezier(.45,0,.75,1)' });
    a.onfinish = () => { el.remove(); COINS--; tg.classList.remove('gpop'); void tg.offsetWidth; tg.classList.add('gpop'); }; } }
function burst(x, y, c, n, sp) {""")
rep("    if (f.k === 'w') { drawWisp(f); continue; }", "    if (f.k === 'w') { drawWisp(f); continue; }\n    if (f.k === 'ring2') { const q = p; ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = (1 - q) * 0.8; ctx.strokeStyle = f.c; ctx.lineWidth = 3 * (1 - q) + 0.5; ctx.beginPath(); ctx.ellipse(f.x, f.y + 18, f.r * (0.3 + q), f.r * (0.3 + q) * 0.35, 0, 0, TAU); ctx.stroke(); ctx.restore(); continue; }")
s = s.replace('<style id="sv">', '''<style id="sv">/* p26 sensations */
.coinfly{position:fixed;z-index:60;width:12px;height:12px;margin:-6px;border-radius:50%;pointer-events:none;background:radial-gradient(circle at 35% 35%,#fff6c0,#ffc94a 45%,#b86a10);box-shadow:0 0 6px #ffb040}
@keyframes gpop{40%{transform:scale(1.15);filter:brightness(1.5)}}#app #dock #goldD.gpop{animation:gpop .25s}
''', 1)
open(P, 'w').write(s); print('p26 sensations ok')
