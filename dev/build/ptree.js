// ================= arbre passif (façon Path of Exile) =================
const PT_IC = { c_atk: 0, c_crit: 6, c_rate: 22, c_cdmg: 7, c_boss: 3, c_exec: 2, c_multi: 1, c_double: 5, k_berserk: 4, r_pv: 8, r_def: 10, r_regen: 11, r_leech: 12, r_esq: 13, r_thorns: 14, r_shield: 9, r_undying: 15, k_fort: 10, a_gold: 16, a_xp: 20, a_shard: 21, a_up: 17, a_luck: 21, a_ham: 19, a_comp: 18, a_twin: 19, k_midas: 23 };
const PT_BR = {
  carnage: { n: 'Carnage', c: '#ff4a5a', a: 150, minors: ['c_atk', 'c_crit', 'c_rate', 'c_atk', 'c_cdmg'], notables: [['Tueur de titans', { c_boss: 2 }], ['Exécution', { c_exec: 3 }], ['Tir fourchu', { c_multi: 2 }], ['Coup fatal', { c_cdmg: 3, c_crit: 2 }]], cap: ['Rafale maudite', { c_double: 1 }], key: ['Berserker', { k_berserk: 1 }] },
  rempart: { n: 'Rempart', c: '#5ab0ff', a: 30, minors: ['r_pv', 'r_def', 'r_regen', 'r_pv'], notables: [['Sangsue', { r_leech: 2 }], ['Épines', { r_thorns: 3 }], ['Égide', { r_shield: 2 }], ['Ombre fuyante', { r_esq: 3 }]], cap: ['Indomptable', { r_undying: 1 }], key: ['Forteresse', { k_fort: 1 }] },
  avarice: { n: 'Avarice', c: '#ffc23a', a: -90, minors: ['a_gold', 'a_xp', 'a_shard', 'a_up'], notables: [['Main bénie', { a_luck: 2 }], ['Forgeron', { a_ham: 2 }], ['Chasseur de raid', { a_comp: 2 }], ['Érudit', { a_xp: 3 }]], cap: ['Marteau béni', { a_twin: 1 }], key: ['Midas', { k_midas: 1 }] },
};
const PT = (() => { // génération déterministe du graphe
  const N = {}, E = [], add = (id, x, y, t, k, br, name) => { N[id] = { id, x, y, t, k, br, name }; return id; }, link = (a, b) => E.push([a, b]);
  add('start', 0, 0, 's', {}, null, 'Origine');
  const spine = {};
  for (const [b, D] of Object.entries(PT_BR)) {
    const A = D.a * Math.PI / 180, dx = Math.cos(A), dy = Math.sin(A), px = -dy, py = dx; let mi = 0; const nm = () => { const k = D.minors[mi++ % D.minors.length]; return { [k]: 1 }; };
    const P = i => [dx * (60 + 105 * i), dy * (60 + 105 * i)]; spine[b] = [];
    for (let i = 1; i <= 8; i++) { const [x, y] = P(i), last = i === 8, id = add(`${b}_s${i}`, x, y, last ? 'k' : 'm', last ? D.cap[1] : nm(), b, last ? D.cap[0] : null); spine[b].push(id); link(i === 1 ? 'start' : `${b}_s${i - 1}`, id); }
    [[2, -1], [3, 1], [5, -1], [6, 1]].forEach(([si, side], ci) => { const [bx, by] = P(si); let prev = `${b}_s${si}`;
      for (let j = 1; j <= 4; j++) { const ox = bx + px * side * 62 * j + dx * 30 * j, oy = by + py * side * 62 * j + dy * 30 * j, notable = j === 4, id = add(`${b}_c${ci}_${j}`, ox, oy, notable ? 'n' : 'm', notable ? D.notables[ci][1] : nm(), b, notable ? D.notables[ci][0] : null); link(prev, id); prev = id; }
      link(prev, `${b}_s${si + 2}`); });
    const [kx, ky] = P(7), side = (b === 'avarice' ? 1 : b === 'carnage' ? -1 : 1) * -1;
    const m1 = add(`${b}_k1`, kx + px * side * 70, ky + py * side * 70, 'm', nm(), b); link(`${b}_s7`, m1);
    const kk = add(`${b}_key`, kx + px * side * 150 + dx * 40, ky + py * side * 150 + dy * 40, 'k', D.key[1], b, D.key[0]); link(m1, kk);
  }
  const bs = Object.keys(PT_BR); // anneau entre les branches (au 1er nœud de chaque branche)
  for (let i = 0; i < 3; i++) { const b1 = bs[i], b2 = bs[(i + 1) % 3]; let a1 = PT_BR[b1].a, a2 = PT_BR[b2].a; while (a2 < a1) a2 += 360; if (a2 - a1 > 180) { [a1, a2] = [a2, a1 + 360]; }
    let prev = `${b1}_s2`; const gen = [['c_atk'], ['r_pv'], ['a_gold']][i];
    for (let j = 1; j <= 3; j++) { const ang = (a1 + (a2 - a1) * j / 4) * Math.PI / 180, r = 270, k = [ 'c_atk', 'r_pv', 'a_gold' ][(i + j) % 3], id = add(`ring${i}_${j}`, Math.cos(ang) * r, Math.sin(ang) * r, 'm', { [k]: 1 }, null); link(prev, id); prev = id; }
    link(prev, `${b2}_s2`); }
  const adj = {}; for (const id in N) adj[id] = []; for (const [a, b] of E) { adj[a].push(b); adj[b].push(a); }
  return { N, E, adj };
})();
let TRC = null;
function trCalc() { if (!S.ptree) { const old = S.tree ? Object.values(S.tree).reduce((a, b) => a + b, 0) : 0; S.tp += old; S.tree = {}; S.ptree = {}; } TRC = {}; for (const id in S.ptree) { const n = PT.N[id]; if (n) for (const k in n.k) TRC[k] = (TRC[k] || 0) + n.k[k]; } }
const ptHas = id => id === 'start' || !!(S.ptree && S.ptree[id]);
const ptCan = id => !ptHas(id) && PT.adj[id].some(ptHas);
function ptAlloc(id) { if (S.tp < 1 || !ptCan(id)) return; S.tp--; S.ptree[id] = 1; trCalc(); save(); const st = heroStats(); B.hero.hpMax = st.pv; B.gear = gear(); PT_V.pulse = { id, t: performance.now() }; sfxPlay('level'); ptRender(); }
const ptDesc = n => Object.entries(n.k).map(([k, v]) => NODE[k] ? NODE[k][3](v) : k).join('<br>');
const ptTitle = n => n.name || (NODE[Object.keys(n.k)[0]] || ['Nœud'])[0];
const PT_V = { x: 0, y: -120, z: 0.55, sel: null, pulse: null };
function ptRender() { // en-tête + détail ; le canvas est redessiné en continu
  const h = $('ptPts'); if (!h) return; h.innerHTML = `<b>${S.tp}</b><small>point${S.tp > 1 ? 's' : ''}</small>`; $('ptSpent').textContent = `${Object.keys(S.ptree).length} nœuds · niveau ${S.lvl}`;
  const d = $('ptDet'), n = PT_V.sel && PT.N[PT_V.sel];
  if (!n) { d.innerHTML = `<p class="knote" style="margin:0;text-align:center">Fais glisser pour explorer, pince ou molette pour zoomer.<br>Touche un nœud relié à ta zone dorée pour le débloquer.</p>`; return; }
  const has = ptHas(n.id), can = ptCan(n.id), c = n.br ? PT_BR[n.br].c : '#f0c46a', kind = { m: 'Nœud', n: 'Notable', k: 'Nœud clé', s: 'Départ' }[n.t];
  d.innerHTML = `<div class="ptdh"><i style="--c:${c}">${kind}</i><b style="color:${c}">${ptTitle(n)}</b></div><p>${n.t === 's' ? 'Le cœur de ton arbre : tout part d\'ici.' : ptDesc(n)}</p>${n.t === 's' ? '' : has ? '<div class="ptok">✓ Débloqué</div>' : `<button class="btn gold" id="ptGo" type="button" ${can && S.tp > 0 ? '' : 'disabled'}>${!can ? 'Relie-le d\'abord à ta zone' : S.tp > 0 ? 'Débloquer · 1 point' : 'Plus de points : monte de niveau'}</button>`}`;
  if ($('ptGo')) $('ptGo').onclick = () => ptAlloc(n.id);
}
const PT_SZ = { m: [92, 24], n: [118, 40], k: [150, 56], s: [150, 0] }, PT_FC = { m: 0, n: 1, k: 2, s: 3 };
function ptDraw() {
  const cv = $('ptCv'); if (!cv || !cv.isConnected) return; requestAnimationFrame(ptDraw);
  const W = cv.clientWidth, H = cv.clientHeight, dpr = Math.min(2, devicePixelRatio || 1); if (cv.width !== Math.round(W * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const g = cv.getContext('2d'), V = PT_V, t = performance.now() / 1000; g.setTransform(dpr, 0, 0, dpr, 0, 0); g.imageSmoothingEnabled = false;
  g.fillStyle = '#05030a'; g.fillRect(0, 0, W, H);
  const T = (x, y) => [W / 2 + (x - V.x) * V.z, H / 2 + (y - V.y) * V.z];
  const bg = IMG.pt_bg; if (bg && bg.complete) { const S2 = 2500 * V.z, [bx, by] = T(0, 0); g.globalAlpha = 0.85; g.drawImage(bg, bx - S2 / 2, by - S2 / 2, S2, S2); g.globalAlpha = 1; }
  // liaisons
  for (const [a, b] of PT.E) { const A = PT.N[a], Bn = PT.N[b], ha = ptHas(a), hb = ptHas(b), [x1, y1] = T(A.x, A.y), [x2, y2] = T(Bn.x, Bn.y);
    if (ha && hb) { g.strokeStyle = '#ffd27a'; g.lineWidth = Math.max(2, 7 * V.z); g.shadowColor = '#ff9a2a'; g.shadowBlur = 12; }
    else if (ha || hb) { g.strokeStyle = `rgba(240,196,106,${0.35 + 0.2 * Math.sin(t * 3)})`; g.lineWidth = Math.max(1.5, 5 * V.z); g.shadowBlur = 0; }
    else { g.strokeStyle = '#3a2e30'; g.lineWidth = Math.max(1.5, 5 * V.z); g.shadowBlur = 0; }
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); }
  g.shadowBlur = 0;
  const fr = IMG.pt_fr, ic = IMG.pt_ic;
  for (const id in PT.N) { const n = PT.N[id], [x, y] = T(n.x, n.y); if (x < -80 || y < -80 || x > W + 80 || y > H + 80) continue;
    const has = ptHas(id), can = ptCan(id) && S.tp > 0, [fs, is] = PT_SZ[n.t], F = fs * V.z, I = is * V.z, col = n.br ? PT_BR[n.br].c : '#f0c46a';
    if (can) { g.globalCompositeOperation = 'lighter'; g.fillStyle = col; g.globalAlpha = 0.18 + 0.12 * Math.sin(t * 4); g.beginPath(); g.arc(x, y, F * 0.36, 0, 7); g.fill(); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; }
    g.fillStyle = '#0a0608'; g.beginPath(); g.arc(x, y, F * 0.2, 0, 7); g.fill();
    if (I > 2 && ic && ic.complete && n.t !== 's') { const k = Object.keys(n.k)[0], ii = PT_IC[k] || 0; g.globalAlpha = has ? 1 : can ? 0.75 : 0.35; g.drawImage(ic, (ii % 6) * 96, Math.floor(ii / 6) * 96, 96, 96, x - I / 2, y - I / 2, I, I); g.globalAlpha = 1; }
    if (n.t === 's') { const sp = ASSETS[HEROES.chevalier.key]; if (sp) sprH(HEROES.chevalier.key, 'idle_6', t * 8, x, y + F * 0.17, F * 0.26 / 100, 1, g); }
    if (fr && fr.complete) g.drawImage(fr, PT_FC[n.t] * 192, (has ? 1 : 0) * 192, 192, 192, x - F / 2, y - F / 2, F, F);
    if (V.sel === id) { g.strokeStyle = '#fff'; g.lineWidth = 2; g.setLineDash([5, 4]); g.beginPath(); g.arc(x, y, F * 0.42, 0, 7); g.stroke(); g.setLineDash([]); }
    if (V.pulse && V.pulse.id === id) { const p = (performance.now() - V.pulse.t) / 600; if (p < 1) { g.strokeStyle = `rgba(255,210,122,${1 - p})`; g.lineWidth = 4; g.beginPath(); g.arc(x, y, F * (0.3 + p * 0.6), 0, 7); g.stroke(); } }
    if (n.t === 'k' && V.z > 0.4) { g.font = `900 ${Math.round(13 * Math.min(1.4, V.z * 1.6))}px Cinzel, serif`; g.textAlign = 'center'; g.lineWidth = 3; g.strokeStyle = '#000'; g.fillStyle = col; g.strokeText(n.name, x, y + F * 0.48); g.fillText(n.name, x, y + F * 0.48); }
  }
  for (const [b, D] of Object.entries(PT_BR)) { if (V.z > 0.75) continue; const A = D.a * Math.PI / 180, [x, y] = T(Math.cos(A) * 1080, Math.sin(A) * 1080); g.font = `900 ${Math.round(22 * Math.max(0.7, V.z * 1.6))}px Cinzel, serif`; g.textAlign = 'center'; g.lineWidth = 4; g.strokeStyle = '#000'; g.fillStyle = D.c; g.strokeText(D.n, x, y); g.fillText(D.n, x, y); }
}
function ptBind() {
  const cv = $('ptCv'), P = new Map(); let pinch = null, moved = 0;
  const hit = (cx, cy) => { const r = cv.getBoundingClientRect(), W = r.width, H = r.height, wx = (cx - r.left - W / 2) / PT_V.z + PT_V.x, wy = (cy - r.top - H / 2) / PT_V.z + PT_V.y; let best = null, bd = 1e9; for (const id in PT.N) { const n = PT.N[id], d = Math.hypot(n.x - wx, n.y - wy), lim = PT_SZ[n.t][0] * 0.42; if (d < lim && d < bd) { bd = d; best = id; } } return best; };
  const clamp2 = () => { PT_V.z = Math.max(0.22, Math.min(1.6, PT_V.z)); PT_V.x = Math.max(-1150, Math.min(1150, PT_V.x)); PT_V.y = Math.max(-1150, Math.min(1150, PT_V.y)); };
  cv.onpointerdown = e => { cv.setPointerCapture(e.pointerId); P.set(e.pointerId, [e.clientX, e.clientY]); moved = 0; if (P.size === 2) { const [a, b] = [...P.values()]; pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), z: PT_V.z }; } };
  cv.onpointermove = e => { if (!P.has(e.pointerId)) return; const o = P.get(e.pointerId); P.set(e.pointerId, [e.clientX, e.clientY]);
    if (P.size === 2 && pinch) { const [a, b] = [...P.values()]; PT_V.z = pinch.z * Math.hypot(a[0] - b[0], a[1] - b[1]) / pinch.d; moved = 99; }
    else if (P.size === 1) { const dx = e.clientX - o[0], dy = e.clientY - o[1]; moved += Math.abs(dx) + Math.abs(dy); PT_V.x -= dx / PT_V.z; PT_V.y -= dy / PT_V.z; }
    clamp2(); };
  cv.onpointerup = cv.onpointercancel = e => { if (P.size === 1 && moved < 10 && e.type === 'pointerup') { const id = hit(e.clientX, e.clientY); PT_V.sel = id; ptRender(); } P.delete(e.pointerId); if (P.size < 2) pinch = null; };
  cv.onwheel = e => { e.preventDefault(); PT_V.z *= e.deltaY < 0 ? 1.12 : 1 / 1.12; clamp2(); };
  cv.ondblclick = e => { const id = hit(e.clientX, e.clientY); if (id && ptCan(id)) ptAlloc(id); };
}
