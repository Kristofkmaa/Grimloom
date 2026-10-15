P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v8.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

# noms de boss réutilisables
rep("const BOSSES = ['p_idle', 'beast1', 'beast2', 'beast3', 'beast5', 'beast4'];",
    "const BOSSES = ['p_idle', 'beast1', 'beast2', 'beast3', 'beast5', 'beast4'];\nconst BNAMES = ['Le Démon écarlate', 'La Bête ardente', 'L\\'Arachnide écarlate', 'La Bête pâle', 'La Wyverne', 'La Bête ailée'];")

# bouton carte dans le HUD + ruban cliquable
rep('      <button id="adminBtn"', '      <button id="mapBtn" type="button" aria-label="Carte du monde"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M9 3 3 5.5v15.5l6-2.5 6 2.5 6-2.5V3l-6 2.5zm0 2.2 6 2.5v11.1l-6-2.5z"/></svg></button>\n      <button id="adminBtn"')
rep("#adminBtn{", "#mapBtn{width:32px;height:32px;border-radius:50%;border:1.5px solid var(--goldd);background:linear-gradient(#3a2230,#14080d);color:var(--gold2);display:grid;place-items:center;font-size:17px;padding:0;box-shadow:0 0 10px -2px #f0c46a80}\n#adminBtn{")
rep("#ribbon{display:inline-flex;", "#ribbon{pointer-events:auto;cursor:pointer;display:inline-flex;")

# écran carte
rep('<div id="modal" hidden>', '''<div id="map" hidden><div id="mapHead"><div><b>Carte du monde</b><small id="mapProg"></small></div><button class="x" id="mapClose" type="button" aria-label="Fermer">✕</button></div><div id="mapScroll"><div id="mapInner"><canvas id="mapC"></canvas><div id="mapMe"><canvas id="mapAv" width="44" height="44"></canvas></div></div></div></div>
<div id="modal" hidden>''')
rep("#toast{", """#map{position:fixed;inset:0;z-index:8;margin:0 auto;max-width:480px;background:#07030a;display:flex;flex-direction:column;animation:fadein .25s}
#map[hidden]{display:none}
@keyframes fadein{from{opacity:0}}
#mapHead{flex:none;display:flex;align-items:center;justify-content:space-between;padding:calc(10px + env(safe-area-inset-top)) 14px 10px;background:linear-gradient(#2a1420,#12070d);border-bottom:1.5px solid #6b3a2e;box-shadow:0 6px 16px #000a;z-index:2}
#mapHead b{display:block;font:900 18px var(--t);color:var(--gold2);letter-spacing:.06em;text-shadow:0 2px 0 #000}
#mapHead small{font:800 12px var(--b);color:var(--dim)}
#mapScroll{flex:1;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain}
#mapInner{position:relative}
#mapC{display:block;width:100%}
#mapMe{position:absolute;width:52px;height:52px;margin:-62px 0 0 -26px;border-radius:50%;border:3px solid var(--gold2);background:radial-gradient(#5a2a3a,#1a0b10);box-shadow:0 0 0 4px #00000080,0 0 22px var(--gold);animation:bob 1.4s ease-in-out infinite;pointer-events:none;overflow:hidden}
#mapMe::after{content:'';position:absolute;left:50%;bottom:-12px;margin-left:-8px;border:8px solid transparent;border-top-color:var(--gold2)}
#mapMe canvas{width:46px;height:46px;image-rendering:pixelated}
@keyframes bob{50%{transform:translateY(-6px)}}
#toast{""")

rep("// ---------- panneau admin ----------", r"""// ---------- carte du monde ----------
const MAP = { HR: 560, top: 70, nodes: [] };
function nodePos(k, i, first, last, W) { // k = chapitre, i = 0..9
  const regTop = MAP.top + (last - k) * MAP.HR, y = regTop + MAP.HR - 70 - i * (MAP.HR - 150) / 9;
  const x = W / 2 + Math.sin(i * 0.95 + k * 1.7) * W * 0.3 + Math.sin(i * 2.3 + k) * W * 0.04;
  return [x, y];
}
function demOn(g, key, x, y, sc) { const A = ASSETS.DEM[key], im = IMG['D_' + key]; if (!A || !im.complete) return; const R = A.anims.idle_S || A.anims.walk_S; g.save(); g.imageSmoothingEnabled = false; g.translate(Math.round(x), Math.round(y)); g.scale(sc, sc); g.drawImage(im, 0, R[0] * A.ch, A.cw, A.ch, -A.ax, -(A.ch - A.foot), A.cw, A.ch); g.restore(); }
function openMap() {
  $('map').hidden = false; const c = $('mapC'), W = $('mapScroll').clientWidth || 400, dpr = Math.min(2, devicePixelRatio || 1);
  const first = Math.max(1, S.c - 3), last = S.c + 1, H = MAP.top + (last - first + 1) * MAP.HR + 40;
  c.style.height = H + 'px'; c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.imageSmoothingEnabled = false;
  const done = (S.c - 1) * 10 + S.s - 1; $('mapProg').textContent = `${done} étapes terminées · ${S.c - 1} boss vaincus`;
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  g.fillStyle = '#07030a'; g.fillRect(0, 0, W, H);
  MAP.nodes = [];
  for (let k = last; k >= first; k--) {
    const bi = BIOMES[(k - 1) % BIOMES.length], regTop = MAP.top + (last - k) * MAP.HR, locked = k > S.c;
    // sol du biome en motif de tuiles
    const t = document.createElement('canvas'); t.width = t.height = 64; const tg = t.getContext('2d'); tg.imageSmoothingEnabled = false;
    for (let j = 0; j < 4; j++) { const f = bi.floor[j % bi.floor.length]; tg.drawImage(IMG.tiles, f[0], f[1], 32, 32, (j % 2) * 32, (j >> 1) * 32, 32, 32); }
    tg.globalCompositeOperation = 'multiply'; tg.fillStyle = bi.mul; tg.fillRect(0, 0, 64, 64);
    g.save(); g.beginPath(); g.rect(0, regTop, W, MAP.HR); g.clip(); g.fillStyle = g.createPattern(t, 'repeat'); g.translate(0, regTop); g.fillRect(0, 0, W, MAP.HR); g.translate(0, -regTop);
    // assombrissement et halo central de la couleur du biome
    g.fillStyle = 'rgba(8,3,8,.45)'; g.fillRect(0, regTop, W, MAP.HR);
    let q = g.createRadialGradient(W / 2, regTop + MAP.HR / 2, 20, W / 2, regTop + MAP.HR / 2, W * 0.9); q.addColorStop(0, bi.light.replace(',1)', ',.18)')); q.addColorStop(1, 'rgba(0,0,0,.55)'); g.fillStyle = q; g.fillRect(0, regTop, W, MAP.HR);
    // décor propre au biome
    for (let n = 0; n < 16; n++) {
      const x = rnd() * W, y = regTop + 40 + rnd() * (MAP.HR - 80), r = rnd();
      let near = false; for (let i = 0; i < 10; i++) { const [nx, ny] = nodePos(k, i, first, last, W); if (hyp(nx - x, ny - y) < 46) near = true; } if (near) continue;
      if (bi.drip) { g.fillStyle = 'rgba(80,150,255,.18)'; g.beginPath(); g.ellipse(x, y, 18 + r * 22, 6 + r * 6, 0, 0, TAU); g.fill(); g.strokeStyle = 'rgba(150,200,255,.25)'; g.stroke(); }
      else if (bi.embers) { g.strokeStyle = `rgba(255,${120 + r * 80 | 0},40,.55)`; g.lineWidth = 2; g.beginPath(); g.moveTo(x, y); for (let m = 0; m < 4; m++) g.lineTo(x + (rnd() - 0.5) * 40, y + (rnd() - 0.5) * 20); g.stroke(); }
      else if (bi.spores) { g.fillStyle = 'rgba(90,170,70,.22)'; g.beginPath(); g.arc(x, y, 8 + r * 16, 0, TAU); g.fill(); }
      if (r < 0.35) g.drawImage(IMG.deco, 1, 20, 13, 44, x - 9, y - 66, 19, 66);
      else if (r < 0.6) { const U = [[144, 124, 16, 20], [162, 128, 12, 16], [144, 172, 16, 20]][n % 3]; g.drawImage(IMG.deco, ...U, x - U[2], y - U[3] * 2, U[2] * 2, U[3] * 2); }
      else if (r < 0.8) { g.fillStyle = '#d8cfc0'; g.beginPath(); g.arc(x, y, 4, 0, TAU); g.fill(); g.fillStyle = '#000'; g.fillRect(x - 2.5, y - 1.5, 1.6, 1.6); g.fillRect(x + 1, y - 1.5, 1.6, 1.6); }
    }
    // chemin
    const pts = Array.from({ length: 10 }, (_, i) => nodePos(k, i, first, last, W));
    const path = (w, col, dash) => { g.beginPath(); g.moveTo(pts[0][0], pts[0][1] + 60); pts.forEach((p, i) => { if (i) { const o = pts[i - 1]; g.quadraticCurveTo(o[0], (o[1] + p[1]) / 2 + 10, (o[0] + p[0]) / 2, (o[1] + p[1]) / 2); } }); g.lineTo(pts[9][0], pts[9][1]); g.lineWidth = w; g.strokeStyle = col; g.setLineDash(dash || []); g.lineCap = 'round'; g.stroke(); g.setLineDash([]); };
    path(18, 'rgba(0,0,0,.55)'); path(12, '#5a4038'); path(3, 'rgba(255,230,180,.25)', [6, 10]);
    g.restore();
    // brume des chapitres verrouillés
    if (locked) { g.fillStyle = 'rgba(6,2,8,.72)'; g.fillRect(0, regTop, W, MAP.HR); }
    // bord rocheux entre régions
    g.fillStyle = '#07030a'; g.beginPath(); g.moveTo(0, regTop); for (let x = 0; x <= W; x += 16) g.lineTo(x, regTop + 6 + rnd() * 12); g.lineTo(W, regTop); g.fill();
    q = g.createLinearGradient(0, regTop, 0, regTop + 50); q.addColorStop(0, 'rgba(0,0,0,.8)'); q.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = q; g.fillRect(0, regTop, W, 50);
    // nœuds
    for (let i = 0; i < 10; i++) {
      const [x, y] = pts[i], idx = (k - 1) * 10 + i + 1, cur = (S.c - 1) * 10 + S.s, isB = i === 9, cleared = idx < cur, now = idx === cur, R = isB ? 24 : 15;
      if (isB) { demOn(g, BOSSES[(k - 1) % BOSSES.length] === 'p_idle' ? 'spawn1' : BOSSES[(k - 1) % BOSSES.length], x, y - 14, locked ? 0.55 : 0.75); if (locked || !cleared) { g.globalCompositeOperation = 'source-atop'; } g.globalCompositeOperation = 'source-over'; }
      if (cleared || now) { g.globalCompositeOperation = 'lighter'; const gq = g.createRadialGradient(x, y, 0, x, y, R * 2.4); gq.addColorStop(0, now ? 'rgba(255,90,110,.6)' : 'rgba(255,200,90,.45)'); gq.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gq; g.fillRect(x - R * 3, y - R * 3, R * 6, R * 6); g.globalCompositeOperation = 'source-over'; }
      g.fillStyle = '#0b0508'; g.beginPath(); g.arc(x, y + 3, R + 3, 0, TAU); g.fill();
      const cg = g.createLinearGradient(0, y - R, 0, y + R); if (cleared) { cg.addColorStop(0, '#ffe39a'); cg.addColorStop(1, '#b86a14'); } else if (now) { cg.addColorStop(0, '#ff7088'); cg.addColorStop(1, '#8a1028'); } else { cg.addColorStop(0, '#4a3640'); cg.addColorStop(1, '#22141a'); }
      g.fillStyle = cg; g.beginPath(); g.arc(x, y, R, 0, TAU); g.fill(); g.lineWidth = 2.5; g.strokeStyle = cleared ? '#fff2c0' : now ? '#ffd0d8' : '#6a5058'; g.stroke();
      g.textAlign = 'center'; g.textBaseline = 'middle';
      if (isB) { g.font = '400 13px Lilita, sans-serif'; g.fillStyle = cleared ? '#3a1404' : '#fff'; g.fillText(cleared ? '✓' : 'BOSS', x, y + 1); }
      else { g.font = '400 14px Lilita, sans-serif'; g.fillStyle = cleared ? '#3a1404' : now ? '#fff' : '#a08890'; g.fillText(cleared ? '✓' : String(i + 1), x, y + 1); }
      if (isB && !locked) { g.font = '900 11px Cinzel, serif'; g.fillStyle = '#ffd0d8'; g.strokeStyle = '#000'; g.lineWidth = 3; g.strokeText(BNAMES[(k - 1) % BNAMES.length], x, y + R + 14); g.fillText(BNAMES[(k - 1) % BNAMES.length], x, y + R + 14); }
      MAP.nodes.push({ x, y, k, s: i + 1, idx, cleared, now, R });
      if (now) { const m = $('mapMe'); m.style.left = x + 'px'; m.style.top = (y - R) + 'px'; }
    }
    // bannière du chapitre
    const bx = W / 2, by = regTop + 30; g.fillStyle = locked ? '#2a1a20' : '#7a1a30'; g.strokeStyle = '#f0c46a'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(bx - 120, by - 16); g.lineTo(bx + 120, by - 16); g.lineTo(bx + 110, by); g.lineTo(bx + 120, by + 16); g.lineTo(bx - 120, by + 16); g.lineTo(bx - 110, by); g.closePath(); g.fill(); g.stroke();
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = '900 13px Cinzel, serif'; g.fillStyle = '#ffe3a0'; g.fillText(locked ? `CHAPITRE ${k} · ???` : `CHAPITRE ${k} · ${bi.n.toUpperCase()}`, bx, by + 1);
    if (locked) { g.font = '400 30px Lilita, sans-serif'; g.fillStyle = 'rgba(255,220,180,.35)'; g.fillText('?', W / 2, regTop + MAP.HR / 2); }
  }
  // médaillon du héros sur l'étape en cours
  const a = $('mapAv'), ag = a.getContext('2d'), Hh = HEROES[S.hero]; ag.clearRect(0, 0, 44, 44); sprH(Hh.key, 'idle_6', 0, 22, 22 + 50 * Hh.sc, Hh.sc * 1.15, 1, ag);
  const me = MAP.nodes.find(n => n.now); if (me) $('mapScroll').scrollTop = Math.max(0, me.y - $('mapScroll').clientHeight * 0.55);
}
$('mapC').addEventListener('click', ev => {
  const r = $('mapC').getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, n = MAP.nodes.find(q => hyp(q.x - x, q.y - y) < q.R + 10); if (!n) return;
  if (n.now) { $('map').hidden = true; if (S.farm) challenge(); else toast(`Tu es déjà sur ${label(n.k, n.s)}`); }
  else if (n.cleared) { if (n.s === 10) { toast('Boss déjà vaincu : choisis une étape normale pour farmer'); return; } S.farm = true; S.fc = n.k; S.fs = n.s; save(); $('map').hidden = true; B.pend = 0; B.pendFn = null; B.walk = null; B.fade = 1; B.scroll = 0; startWave(); toast(`Farm sur ${label(n.k, n.s)}`); }
  else toast('Étape verrouillée');
});
$('mapBtn').onclick = openMap; $('ribbon').onclick = openMap; $('mapClose').onclick = () => $('map').hidden = true;
// ---------- panneau admin ----------""")

open(P, 'w').write(s)
print('ok')
