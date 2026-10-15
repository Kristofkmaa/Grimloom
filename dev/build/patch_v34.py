P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v34.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
a = s.index("function dunHTML() {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r"""const DPOS = { sang: [0.25, 118], os: [0.75, 92], braise: [0.25, 292], givre: [0.75, 268] }, DMAP_H = 420;
let DSEL = 'sang';
function dunHTML() {
  const k = DSEL;
  return `<div class="kp"><div class="kban kg kbt"><div class="kbig"><b>${S.keys}</b><small>clé${S.keys > 1 ? 's' : ''}</small></div><div class="kbi"><b class="kname">Les Donjons</b><small class="kdim">Choisis une porte. 3 vagues + un boss en 60 s pour gagner des Sceaux de set.</small><small class="kdim">3 clés par jour · +1 par boss · perdue seulement si tu gagnes</small></div></div>
  <div class="dmap" style="height:${DMAP_H}px"><canvas id="dmapC"></canvas>
   ${SETK.map(d => `<button type="button" class="dmk ${d === k ? 'on' : ''}" data-dsel="${d}" style="left:${DPOS[d][0] * 100}%;top:${DPOS[d][1]}px;--sc:${SETS[d].c}"><span class="dpl"><b>${DUNS[d].n}</b><small>Niv. ${S.dlv[d]} · ${S.seals[d]} sceaux</small></span>${d === k ? '<i class="darr"></i>' : ''}</button>`).join('')}
   <div class="dcamp"><small>Campement</small></div></div>
  <div class="kl kdun" style="--sc:${SETS[k].c}"><div class="kdt"><div><b>${DUNS[k].n}</b><small>${SETS[k].n}</small></div><em class="kbadge">Niv. ${S.dlv[k]}</em></div><div class="kds">${SETS[k].b.map(([c, t]) => `<div><em>${c}</em><span>${t}</span></div>`).join('')}</div><div class="kdb"><span>Récompense <b>${dunReward(S.dlv[k])} Sceaux</b><br>Tu en as <b>${S.seals[k]}</b></span><button class="btn gold" type="button" data-dun="${k}" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div></div></div>`;
}
function drawDunMap() {
  const c = $('dmapC'); if (!c) return; const W = c.parentNode.clientWidth, H = DMAP_H, dpr = Math.min(2, devicePixelRatio || 1); c.width = W * dpr; c.height = H * dpr; c.style.width = W + 'px'; c.style.height = H + 'px';
  const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.imageSmoothingEnabled = false;
  g.fillStyle = '#0a0607'; g.fillRect(0, 0, W, H);
  // sol de la crypte en motif
  const t = document.createElement('canvas'); t.width = t.height = 64; const tg = t.getContext('2d'); tg.imageSmoothingEnabled = false;
  [[736, 320], [784, 320], [736, 368], [784, 368]].forEach((f, j) => tg.drawImage(IMG.tiles, f[0], f[1], 32, 32, (j % 2) * 32, (j >> 1) * 32, 32, 32));
  g.globalAlpha = 0.32; g.fillStyle = g.createPattern(t, 'repeat'); g.save(); g.scale(1.5, 1.5); g.fillRect(0, 0, W, H); g.restore(); g.globalAlpha = 1;
  let seed = 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  // flaques de terre et gravats
  for (let i = 0; i < 9; i++) { g.globalAlpha = 0.35; g.drawImage(IMG.tiles, 736, 416, 64, 64, rnd() * W - 30, rnd() * H - 30, 96, 96); } g.globalAlpha = 1;
  // halos des donjons
  g.globalCompositeOperation = 'lighter';
  for (const d of SETK) { const [px, py] = DPOS[d], x = px * W, y = py + 40, q = g.createRadialGradient(x, y, 0, x, y, 120); q.addColorStop(0, SETS[d].c + '55'); q.addColorStop(1, '#0000'); g.fillStyle = q; g.fillRect(x - 130, y - 130, 260, 260); }
  g.globalCompositeOperation = 'source-over';
  // chemins depuis le campement
  const cx = W / 2, cy = H - 34;
  for (const d of SETK) { const x = DPOS[d][0] * W, y = DPOS[d][1] + 84; const path = () => { g.beginPath(); g.moveTo(cx, cy); g.quadraticCurveTo((cx + x) / 2 + (x < cx ? -40 : 40), (cy + y) / 2 + 30, x, y); };
    path(); g.lineWidth = 12; g.strokeStyle = 'rgba(0,0,0,.55)'; g.lineCap = 'round'; g.stroke(); path(); g.lineWidth = 7; g.strokeStyle = '#3a2a22'; g.stroke(); path(); g.lineWidth = 2; g.setLineDash([5, 9]); g.strokeStyle = d === DSEL ? '#ffd27a' : 'rgba(220,190,150,.35)'; g.stroke(); g.setLineDash([]); }
  // décor : crânes, urnes, poteaux
  for (let i = 0; i < 14; i++) { const x = rnd() * W, y = 30 + rnd() * (H - 60), r = rnd(); if (SETK.some(d => Math.hypot(DPOS[d][0] * W - x, DPOS[d][1] + 50 - y) < 70) || Math.hypot(cx - x, cy - y) < 50) continue;
    if (r < 0.4) { g.fillStyle = '#d8cfc0'; g.beginPath(); g.arc(x, y, 4, 0, TAU); g.fill(); g.fillStyle = '#000'; g.fillRect(x - 2.5, y - 1.5, 1.6, 1.6); g.fillRect(x + 1, y - 1.5, 1.6, 1.6); }
    else if (r < 0.75) { const U = [[144, 124, 16, 20], [162, 128, 12, 16], [144, 172, 16, 20]][i % 3]; g.drawImage(IMG.deco, ...U, x - U[2], y - U[3] * 2, U[2] * 2, U[3] * 2); }
    else g.drawImage(IMG.deco, 1, 20, 13, 44, x - 9, y - 66, 19, 66); }
  // portes des donjons
  for (const d of SETK) { const x = DPOS[d][0] * W, y = DPOS[d][1], w = 64 * 1.25, h = 105 * 1.25; g.fillStyle = 'rgba(0,0,0,.5)'; g.beginPath(); g.ellipse(x, y + h - 4, w * 0.55, 8, 0, 0, TAU); g.fill(); g.drawImage(IMG.tiles, 880, 0, 64, 105, x - w / 2, y, w, h);
    g.globalCompositeOperation = 'lighter'; const q = g.createRadialGradient(x, y + h * 0.6, 0, x, y + h * 0.6, 34); q.addColorStop(0, SETS[d].c + (d === DSEL ? 'cc' : '77')); q.addColorStop(1, '#0000'); g.fillStyle = q; g.fillRect(x - 40, y + h * 0.6 - 40, 80, 80); g.globalCompositeOperation = 'source-over'; }
  // campement : le chevalier
  const H0 = HEROES[S.hero]; g.fillStyle = 'rgba(0,0,0,.5)'; g.beginPath(); g.ellipse(cx, cy + 4, 22, 6, 0, 0, TAU); g.fill(); sprH(H0.key, 'idle_6', 0, cx, cy + 6, H0.sc * 0.42, 1, g);
  g.globalCompositeOperation = 'lighter'; let q = g.createRadialGradient(cx, cy, 0, cx, cy, 50); q.addColorStop(0, 'rgba(255,140,60,.35)'); q.addColorStop(1, '#0000'); g.fillStyle = q; g.fillRect(cx - 60, cy - 60, 120, 120); g.globalCompositeOperation = 'source-over';
  // brume sur les bords
  q = g.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.35, W / 2, H / 2, Math.max(W, H) * 0.75); q.addColorStop(0, 'rgba(0,0,0,0)'); q.addColorStop(1, 'rgba(0,0,0,.85)'); g.fillStyle = q; g.fillRect(0, 0, W, H);
}
""" + s[b:]
rep("""    $('panel').innerHTML = dunHTML();
    document.querySelectorAll('[data-dun]').forEach(b => b.onclick = () => startDungeon(b.dataset.dun));""",
"""    $('panel').innerHTML = dunHTML(); requestAnimationFrame(drawDunMap);
    document.querySelectorAll('[data-dsel]').forEach(b => b.onclick = () => { DSEL = b.dataset.dsel; const y = $('panel').scrollTop; ui(); $('panel').scrollTop = y; });
    document.querySelectorAll('[data-dun]').forEach(b => b.onclick = () => startDungeon(b.dataset.dun));""")
s = s.replace("</style>", r"""
.dmap{position:relative;margin-bottom:10px;border:20px solid transparent;border-image:var(--kL) 32 / 20px stretch;margin-left:-4px;margin-right:-4px}
.dmap canvas{position:absolute;inset:-6px;width:calc(100% + 12px)!important;display:block}
.dmk{position:absolute;width:110px;height:170px;margin-left:-55px;margin-top:-6px;padding:0;border:0;background:none;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;cursor:pointer}
.dpl{display:flex;flex-direction:column;align-items:center;padding:3px 8px;border:10px solid transparent;border-image:var(--kTab) 32 / 10px stretch;background:linear-gradient(#0d0709e8,#0d0709e8) center/calc(100% - 4px) calc(100% - 4px) no-repeat border-box;margin-bottom:-26px;white-space:nowrap}
.dpl b{font:900 11px var(--t);color:var(--sc);letter-spacing:.03em}.dpl small{font:800 9.5px var(--b);color:#b89a7a}
.dmk.on .dpl{border-image-source:var(--kTabg);background:linear-gradient(#3a1018f0,#3a1018f0) center/calc(100% - 4px) calc(100% - 4px) no-repeat border-box}
.darr{position:absolute;top:-22px;left:50%;margin-left:-8px;width:0;height:0;border:8px solid transparent;border-top:12px solid #ffd27a;filter:drop-shadow(0 0 6px #ffb04a);animation:darr 1s ease-in-out infinite}
@keyframes darr{50%{transform:translateY(6px)}}
.dcamp{position:absolute;left:50%;bottom:-4px;transform:translateX(-50%);font:800 9.5px var(--b);color:#c8a878;letter-spacing:.12em;text-transform:uppercase;pointer-events:none}
</style>""", 1)
open(P, 'w').write(s); print('ok')
