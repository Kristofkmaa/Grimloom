// ================= familiers (gacha) =================
const FRC = ['#b8aea4', '#4a9aff', '#b060ff', '#ffc23a', '#ff3a3a'], FRN = ['Commun', 'Rare', 'Épique', 'Légendaire', 'Mythique'], FRATE = [55, 28, 12, 4, 1];
const FAM = {
  corbeau: { n: 'Corbeau des Tombes', i: 0, r: 0, k: 'atk', v: 3, p: 1 }, chauve: { n: 'Chauve-souris du Clocher', i: 1, r: 0, k: 'rate', v: 3, p: 1 }, rat: { n: 'Rat des Cryptes', i: 2, r: 0, k: 'gold', v: 6, p: 2 },
  papillon: { n: 'Phalène Pâle', i: 10, r: 0, k: 'xp', v: 6, p: 4 }, poisson: { n: 'Poisson d\'Ossements', i: 11, r: 0, k: 'pv', v: 4, p: 5 },
  oeil: { n: 'Œil Ailé', i: 3, r: 1, k: 'crit', v: 2, p: 2 }, champi: { n: 'Champignon Sporifère', i: 8, r: 1, k: 'regen', v: 0.3, p: 4 }, araignee: { n: 'Araignée des Ronces', i: 5, r: 1, k: 'cdmg', v: 10, p: 6 },
  slime: { n: 'Gelée du Charnier', i: 4, r: 2, k: 'vol', v: 2, p: 1 }, fantome: { n: 'Feu Follet', i: 6, r: 2, k: 'esq', v: 3, p: 5 },
  heaume: { n: 'Heaume Hanté', i: 9, r: 3, k: 'pv', v: 14, p: 0 }, loup: { n: 'Loup des Brumes', i: 7, r: 4, k: 'atk', v: 14, p: 1 },
};
const FK = { atk: ['Attaque', '%'], pv: ['Points de vie', '%'], rate: ['Vitesse d\'attaque', '%'], crit: ['Critique', ' %'], cdmg: ['Dégâts critiques', ' %'], vol: ['Vol de vie', ' %'], esq: ['Esquive', ' %'], regen: ['Régénération', ' %/s'], gold: ['Or gagné', '%'], xp: ['Expérience', '%'] };
if (S.souls === undefined) S.souls = 10; S.fams = S.fams || {}; if (S.fam === undefined) S.fam = null; if (S.famPity === undefined) S.famPity = 0; S.pet = null;
const famStar = id => (S.fams[id] || { s: 0 }).s, famVal = id => FAM[id].v * (1 + 0.4 * (famStar(id) - 1));
const famTxt = id => { const F = FAM[id], K = FK[F.k], v = famStar(id) ? famVal(id) : F.v; return `${K[0]} +${v < 1 ? v.toFixed(2) : v % 1 ? v.toFixed(1) : v}${K[1]}`; };
const famColl = () => Object.keys(S.fams).reduce((a, id) => a + 0.6 * (1 + 0.5 * FAM[id].r) * (1 + 0.2 * (famStar(id) - 1)), 0);
const famK = k => (S.fam && FAM[S.fam] && FAM[S.fam].k === k && S.fams[S.fam] ? famVal(S.fam) : 0);
const famStars = id => { const s = famStar(id); return [1, 2, 3, 4, 5].map(i => `<i class="${i <= s ? 'on' : ''}">★</i>`).join(''); };
function famRoll(force) { let tier; if (force !== undefined) tier = force; else { let x = Math.random() * 100; tier = 0; for (let i = 4; i >= 0; i--) { const lo = FRATE.slice(i + 1).reduce((a, b) => a + b, 0); if (x < lo + FRATE[i] && x >= lo) { tier = i; break; } } const lo2 = 0; x = x; }
  const ids = Object.keys(FAM).filter(k => FAM[k].r === tier); return pick(ids.length ? ids : Object.keys(FAM)); }
function famSummon(n) {
  const cost = n * 10; if (S.souls < cost) { toast('Pas assez d\'âmes'); return; } S.souls -= cost; const got = [];
  for (let i = 0; i < n; i++) { S.famPity++; let id = famRoll(); if (S.famPity >= 40 && FAM[id].r < 3) id = famRoll(Math.random() < 0.8 ? 3 : 4); if (FAM[id].r >= 3) S.famPity = 0;
    const o = S.fams[id]; let t; if (!o) { S.fams[id] = { s: 1, c: 0 }; t = 'Nouveau !'; if (!S.fam) S.fam = id; } else if (o.s >= 5) { S.souls += 2; t = '+2 âmes'; } else { o.c++; if (o.c >= o.s) { o.c = 0; o.s++; t = `${o.s} ★ !`; } else t = `+1 copie`; } got.push([id, t]); }
  save(); famReveal(got, n);
}
const famSp = (id, cls) => `<i class="fsp ${cls || ''}" style="background-position:${FAM[id].i * 100 / 11}% 0"></i>`;
const famTile = (id, extra) => { const F = FAM[id], o = S.fams[id]; return `<button type="button" class="ftile ${o ? '' : 'lock'} ${S.fam === id ? 'eq' : ''}" data-fam="${id}" style="--rc:${FRC[F.r]};background-position:${F.r * 25}% 0">${famSp(id)}${S.fam === id ? '<em class="feq">Équipé</em>' : ''}<span class="fnm"><b>${o ? F.n : '???'}</b>${o ? `<span class="fst">${famStars(id)}</span>` : `<small>${FRN[F.r]}</small>`}</span>${extra ? `<em class="fex">${extra}</em>` : ''}</button>`; };
function famReveal(got, n) {
  const best = Math.max(...got.map(([id]) => FAM[id].r)), d = document.createElement('div'); d.id = 'sumFx'; d.style.setProperty('--bc', FRC[best]);
  d.innerHTML = `<div class="sfglow"></div><h2>Invocation</h2><div class="fgridR ${got.length > 1 ? 'many' : ''}">${got.map(([id, t], i) => `<div class="frv" style="--d:${0.25 + i * 0.15}s">${famTile(id, t)}</div>`).join('')}</div>
  <div class="sfbtns"><button class="btn" type="button" id="sfOk">Fermer</button><button class="btn gold" type="button" id="sfAgain" ${S.souls < n * 10 ? 'disabled' : ''}>Invoquer ×${n}<small>${n * 10} âmes · tu as ${fmt(S.souls)}</small></button></div>`;
  $('app').appendChild(d); B.flash = { c: '200,140,255', t: 0.3, a: 0.2 };
  $('sfOk').onclick = () => { d.remove(); ui(); }; $('sfAgain').onclick = () => { d.remove(); famSummon(n); };
}
function showFam(id) {
  const F = FAM[id], o = S.fams[id], need = o ? o.s : 1;
  sheet(`<h3>${o ? F.n : 'Familier inconnu'} <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="fbig ${o ? '' : 'lock'}" style="--rc:${FRC[F.r]}">${famSp(id, 'big')}</div>
  <div class="fdt"><div><span>Rareté</span><b style="color:${FRC[F.r]}">${FRN[F.r]}</b></div>${o ? `<div><span>Étoiles</span><b class="fst">${famStars(id)}</b></div>` : ''}<div><span>Bonus équipé</span><b>${famTxt(id)}</b></div><div><span>Attaque</span><b>Tire toutes les 2,5 s</b></div>${o && o.s < 5 ? `<div><span>Prochaine étoile</span><b>${o.c} / ${need} copies</b></div>` : ''}</div>
  ${o ? `<button class="btn ${S.fam === id ? '' : 'gold'}" id="fEq" type="button" style="width:100%;margin-top:12px">${S.fam === id ? 'Retirer' : 'Équiper'}</button>` : '<p class="knote" style="text-align:center">Invoque-le avec des âmes pour l\'obtenir.</p>'}`);
  if ($('fEq')) $('fEq').onclick = () => { S.fam = S.fam === id ? null : id; save(); closeM(); ui(); };
}
function famHTML() {
  const ids = Object.keys(FAM).sort((a, b) => FAM[b].r - FAM[a].r), own = ids.filter(id => S.fams[id]).length, eq = S.fam && FAM[S.fam];
  return `<div class="fban"><div class="fbt"><b>Familiers</b><small>${own} / ${ids.length} invoqués</small></div><div class="sppg"><i class="fsoul"></i><b>${fmt(S.souls)}</b><small>âmes</small></div>
    <div class="fbtns"><button class="btn sm" type="button" id="fs1" ${S.souls < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 âmes</small></button><button class="btn gold sm" type="button" id="fs10" ${S.souls < 100 ? 'disabled' : ''}>Invoquer ×10<small>100 âmes</small></button></div></div>
  <p class="knote" style="margin:6px 0 0">Légendaire garanti dans <b style="color:#ffd890">${40 - S.famPity}</b> invocations · ${FRN.map((n, i) => `<span style="color:${FRC[i]}">${n} ${FRATE[i]} %</span>`).join(' · ')}</p>
  <h4 class="kh">Compagnon</h4>
  ${eq ? `<div class="kl fcur" data-fam="${S.fam}" style="--rc:${FRC[eq.r]}">${famSp(S.fam, 'mid')}<div><b style="color:${FRC[eq.r]}">${eq.n}</b><span class="fst">${famStars(S.fam)}</span><small>${famTxt(S.fam)} · tire sur les démons</small></div></div>` : '<p class="knote">Aucun familier équipé : touche-en un dans ta collection.</p>'}
  <p class="knote">Bonus de collection : <b style="color:#ffd890">attaque et PV +${famColl().toFixed(1)} %</b> (chaque familier possédé compte)</p>
  <h4 class="kh">Collection</h4><div class="fgrid">${ids.map(id => famTile(id)).join('')}</div>`;
}
