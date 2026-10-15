// ================= reliques (sets à collectionner) =================
const RREL = [1, 1, 2, 2, 3, 4], RRATE = [0, 60, 28, 10, 2], RSTAT = { sang: 'atk', os: 'pv', braise: 'rate', givre: 'crit' };
const REL = {}; [['sang', ['Calice de Sang', 'Anneau Épineux', 'Croc du Vampire', 'Dague Rituelle', 'Cœur Captif', 'Couronne Sanglante']], ['os', ['Coupe-Crâne', 'Anneau d\'Os', 'Collier de Vertèbres', 'Cor d\'Os', 'Cage Thoracique', 'Couronne d\'Ossements']], ['braise', ['Lanterne Ardente', 'Anneau en Fusion', 'Amulette de Braise', 'Marteau du Brasier', 'Plume de Phénix', 'Couronne de Flammes']], ['givre', ['Orbe Glacial', 'Anneau Gelé', 'Amulette de Neige', 'Dague de Givre', 'Cœur Gelé', 'Couronne de Glace']]].forEach(([k, L], si) => L.forEach((n, j) => { REL[k + j] = { n, set: k, i: si * 6 + j, r: RREL[j] }; }));
S.rels = S.rels || {}; S.relEq = S.relEq || [null, null, null, null, null, null]; if (S.relPity === undefined) S.relPity = 0;
if (!S.relMig) { S.relMig = 1; for (const sl of SLOTS) { const it = S.eq[sl.id]; if (it && it.set) { const k = it.set, id = k + (Math.random() * 4 | 0); S.rels[id] = S.rels[id] || { s: 1, c: 0 }; const f = S.relEq.indexOf(null); if (f >= 0 && !S.relEq.includes(id)) S.relEq[f] = id; it.set = null; } } }
const sealTot = () => SETK.reduce((a, k) => a + (S.seals[k] || 0), 0);
function sealPay(n) { if (sealTot() < n) return false; while (n > 0) { const k = SETK.reduce((a, b) => S.seals[b] > S.seals[a] ? b : a); S.seals[k]--; n--; } return true; }
const relStar = id => (S.rels[id] || { s: 0 }).s, relVal = id => [0, 2, 3.5, 5, 8][REL[id].r] * (1 + 0.3 * (relStar(id) - 1));
const relTxt = id => { const R = REL[id], v = relVal(id) || [0, 2, 3.5, 5, 8][R.r], k = RSTAT[R.set]; return `${{ atk: 'Attaque', pv: 'Points de vie', rate: 'Vitesse d\'attaque', crit: 'Critique' }[k]} +${v % 1 ? v.toFixed(1) : v} %`; };
const relSp = (id, cls) => `<i class="rsp ${cls || ''}" style="background-position:${REL[id].i * 100 / 23}% 0"></i>`;
const relStars = id => { const s = relStar(id); return [1, 2, 3, 4, 5].map(i => `<i class="${i <= s ? 'on' : ''}">★</i>`).join(''); };
const relFeat = () => { const L = Object.keys(REL).filter(k => REL[k].r >= 3); return L[(banIdx() + 2) % L.length]; };
function relRoll() { let x = Math.random() * 100, t = 1; for (let i = 4; i >= 1; i--) { const lo = RRATE.slice(i + 1).reduce((a, b) => a + b, 0); if (x >= lo && x < lo + RRATE[i]) { t = i; break; } } return t; }
function relSummon(n) {
  const cost = n * 10; if (!sealPay(cost)) { toast('Pas assez de Sceaux : fais les donjons de sets'); return; } const got = []; if (!$('modal').hidden) closeM();
  for (let i = 0; i < n; i++) { S.relPity++; let t = relRoll(); if (S.relPity >= 40 && t < 3) t = 3; if (t >= 3) S.relPity = 0; const rf = relFeat(); const ids = Object.keys(REL).filter(k => REL[k].r === t), id = REL[rf].r === t && Math.random() < 0.5 ? rf : pick(ids);
    const o = S.rels[id]; let tx; if (!o) { S.rels[id] = { s: 1, c: 0 }; tx = 'Nouveau !'; const f = S.relEq.indexOf(null); if (f >= 0) S.relEq[f] = id; } else if (o.s >= 5) { S.seals[REL[id].set] += 2; tx = '+2 Sceaux'; } else { o.c++; if (o.c >= o.s) { o.c = 0; o.s++; tx = `${o.s} ★ !`; } else tx = '+1 copie'; } got.push([id, tx]); }
  save(); sumFx(FRC[Math.max(...got.map(([id]) => REL[id].r))], () => relReveal(got, n));
}
const relTile = (id, extra) => { const R = REL[id], o = S.rels[id], eq = S.relEq.includes(id); return `<button type="button" class="ftile rtile ${o ? '' : 'lock'} ${eq ? 'eq' : ''}" data-rel="${id}" style="--rc:${FRC[R.r]}">${relSp(id)}${eq ? '<em class="feq">Équipée</em>' : ''}<span class="fnm"><b>${o ? R.n : '???'}</b>${o ? `<span class="fst">${relStars(id)}</span>` : `<small>${FRN[R.r]}</small>`}</span>${extra ? `<em class="fex">${extra}</em>` : ''}</button>`; };
function relReveal(got, n) {
  const best = Math.max(...got.map(([id]) => REL[id].r)), d = document.createElement('div'); d.id = 'sumFx'; d.style.setProperty('--bc', FRC[best]);
  d.innerHTML = `<div class="sfglow"></div><h2>Invocation</h2><div class="fgridR ${got.length > 1 ? 'many' : ''}">${got.map(([id, t], i) => `<div class="frv" style="--d:${0.25 + i * 0.15}s">${relTile(id, t)}</div>`).join('')}</div>
  <div class="sfbtns"><button class="btn" type="button" id="sfOk">Fermer</button><button class="btn gold" type="button" id="sfAgain" ${sealTot() < n * 10 ? 'disabled' : ''}>Invoquer ×${n}<small>${n * 10} Sceaux · tu as ${fmt(sealTot())}</small></button></div>`;
  $('app').appendChild(d); $('sfOk').onclick = () => { d.remove(); B.gear = gear(); ui(); if ($('sumPg')) sumPage(); else relSheet(); }; $('sfAgain').onclick = () => { d.remove(); relSummon(n); };
}
function relSheet() {
  const sc = setCounts(), own = Object.keys(S.rels).length;
  sheet(`<h3>Autel des reliques <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="raltar">${S.relEq.map((id, i) => id ? `<button type="button" class="rslot on" data-rel="${id}" style="--rc:${FRC[REL[id].r]};--sc:${SETS[REL[id].set].c}">${relSp(id)}<i class="rsd"></i></button>` : `<div class="rslot"><b>+</b></div>`).join('')}</div>
  ${SETK.filter(k => sc[k]).map(k => `<div class="kl kset" style="--sc:${SETS[k].c};margin-top:8px"><div class="ksh"><b>${SETS[k].n}</b><em>${sc[k]} / 6</em></div>${SETS[k].b.map(([c, t]) => `<div class="setb ${sc[k] >= c ? 'on' : ''}"><em>${c}</em>${t}</div>`).join('')}</div>`).join('') || '<p class="knote" style="text-align:center">Équipe 2, 4 ou 6 reliques du même set pour réveiller ses bonus.</p>'}
  <button class="btn gold" type="button" id="rGo" style="width:100%;margin-top:10px">Invoquer des reliques<small>${fmt(sealTot())} Sceaux · donjons de sets</small></button>
  <h4 class="kh">Collection <small>${own} / 24</small></h4>${SETK.map(k => `<div class="rsetrow"><b style="color:${SETS[k].c}">${SETS[k].n}</b><div class="rgrid">${Object.keys(REL).filter(id => REL[id].set === k).map(id => relTile(id)).join('')}</div></div>`).join('')}`);
  const M = $('mbox'); M.querySelectorAll('[data-rel]').forEach(b => b.onclick = () => showRel(b.dataset.rel)); $('rGo').onclick = () => { closeM(); sumPage('rel'); };
}
function showRel(id) {
  const R = REL[id], o = S.rels[id], eqI = S.relEq.indexOf(id), free = S.relEq.indexOf(null);
  sheet(`<h3>${o ? R.n : 'Relique inconnue'} <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="fbig ${o ? '' : 'lock'}" style="--rc:${FRC[R.r]}">${relSp(id, 'big')}</div>
  <div class="fdt"><div><span>Set</span><b style="color:${SETS[R.set].c}">${SETS[R.set].n}</b></div><div><span>Rareté</span><b style="color:${FRC[R.r]}">${FRN[R.r]}</b></div>${o ? `<div><span>Étoiles</span><b class="fst">${relStars(id)}</b></div>` : ''}<div><span>Bonus</span><b>${relTxt(id)}</b></div>${o && o.s < 5 ? `<div><span>Prochaine étoile</span><b>${o.c} / ${o.s} copies</b></div>` : ''}</div>
  ${o ? (eqI >= 0 ? '<button class="btn" id="rUn" type="button" style="width:100%;margin-top:12px">Retirer de l\'autel</button>' : free >= 0 ? '<button class="btn gold" id="rEq" type="button" style="width:100%;margin-top:12px">Placer sur l\'autel</button>' : `<p class="knote" style="margin:12px 0 6px">Autel plein : choisis la relique à remplacer</p><div class="raltar sm">${S.relEq.map((x, i) => `<button type="button" class="rslot on" data-rep="${i}" style="--rc:${FRC[REL[x].r]}">${relSp(x)}</button>`).join('')}</div>`) : '<p class="knote" style="text-align:center">Invoque-la avec des Sceaux pour l\'obtenir.</p>'}`);
  const done = () => { save(); B.gear = gear(); const st = heroStats(); B.hero.hpMax = st.pv; ui(); relSheet(); };
  if ($('rUn')) $('rUn').onclick = () => { S.relEq[eqI] = null; done(); }; if ($('rEq')) $('rEq').onclick = () => { S.relEq[free] = id; done(); };
  $('mbox').querySelectorAll('[data-rep]').forEach(b => b.onclick = () => { S.relEq[+b.dataset.rep] = id; done(); });
  const x = $('mbox').querySelector('.x'); if (x) x.onclick = () => relSheet();
}
