// ================= modules du hub : coffre de temps, connexion, roue, passe =================
if (!S.afkT) S.afkT = Date.now(); if (S.spins === undefined) S.spins = 0;
const AFK_MAX = 12 * 3600;
function afkCalc() { const sec = Math.min(AFK_MAX, Math.max(0, (Date.now() - S.afkT) / 1000)), n = stageIndex();
  return { sec, gold: Math.round(3 * Math.pow(1.11, n) * 0.22 * goldMul() * sec), xp: Math.round(sec * 0.08 * (1 + n * 0.25)), ham: Math.floor(sec / 3600 * afkHamH()), pages: Math.floor(sec / 300) }; }
function afkSheet() {
  const r = afkCalc(), h = Math.floor(r.sec / 3600), m = Math.floor(r.sec % 3600 / 60), pc = r.sec / AFK_MAX * 100;
  sheet(`<h3>Coffre de temps <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="afkTop"><div class="afkChest ${pc >= 100 ? 'full' : ''}">${IC.gem}</div><div><b>${h} h ${String(m).padStart(2, '0')}</b><small>sur 12 h maximum</small><div class="afkBar"><i style="width:${pc}%"></i></div></div></div>
  <p class="knote" style="margin:6px 0 10px">Il se remplit tout seul, que tu joues ou non. Plus tu avances dans les chapitres, plus il contient de butin.</p>
  <div class="list"><div>${IC.coin}<span>Or<b>+${fmt(r.gold)}</b></span></div><div>${IC.star}<span>Expérience<b>+${fmt(r.xp)}</b></span></div><div>${IC.ham}<span>Marteaux<b>+${fmt(r.ham)}</b></span></div><div>${IC.book}<span>Pages<b>+${fmt(r.pages)}</b></span></div></div>
  <button class="btn gold" type="button" id="afkGo" style="width:100%;margin-top:14px" ${r.sec < 60 ? 'disabled' : ''}>Récolter</button>`);
  $('afkGo').onclick = () => { const r2 = afkCalc(); S.gold += r2.gold; S.ham += r2.ham; S.pages += r2.pages; gainXP(r2.xp); S.afkT = Date.now(); passAdd(Math.round(r2.sec / 600)); save(); closeM(); ui(); toast(`Récolté : +${fmt(r2.gold)} or · +${r2.ham} marteaux · +${r2.pages} pages`); };
}
function loginView() {
  const d = new Date().toDateString(); if (S.loginDay !== d) return loginSheet(d);
  const day = S.loginStreak % 7, rw = LOGIN.map(r => r.gold ? Object.assign({}, r, { gold: Math.round(r.gold * 500 * Math.pow(1.12, stageIndex())) }) : r);
  sheet(`<h3>Connexion · 7 jours <button class="x" type="button" aria-label="Fermer">✕</button></h3><div class="login">${rw.map((r, i) => `<div class="${i < day ? 'got' : i === day ? 'now' : ''}"><small>Jour ${i + 1}</small><b>${rewTxt(r).replace(/ · /g, '<br>')}</b>${i < day ? '<em>✓</em>' : ''}</div>`).join('')}</div><p class="knote" style="text-align:center;margin-top:12px">Déjà récupéré aujourd'hui. Reviens demain pour le <b style="color:#ffd890">jour ${day + 1}</b>.</p>`);
}
// --- roue de la fortune ---
const WHEEL = [{ k: 'ham', v: 20, w: 28, c: '#5a3a28' }, { k: 'gold', v: 1, w: 25, c: '#6a4a10' }, { k: 'pages', v: 30, w: 20, c: '#5a2a18' }, { k: 'souls', v: 15, w: 12, c: '#3a1a5a' }, { k: 'seals', v: 12, w: 8, c: '#5a1020' }, { k: 'shards', v: 150, w: 15, c: '#2a2050' }, { k: 'ham', v: 80, w: 4, c: '#7a5a20' }, { k: 'souls', v: 100, w: 1, c: '#8a1a3a' }];
const wheelTxt = s => ({ ham: `${s.v} marteaux`, gold: `${fmt(wheelGold())} or`, pages: `${s.v} pages`, souls: `${s.v} âmes`, seals: `${s.v} Sceaux`, shards: `${s.v} éclats` }[s.k]);
const wheelGold = () => Math.round(400 * Math.pow(1.11, stageIndex()));
const wheelFree = () => S.wheelDay !== new Date().toDateString();
function wheelGive(s) { if (s.k === 'ham') S.ham += s.v; else if (s.k === 'gold') S.gold += wheelGold(); else if (s.k === 'pages') S.pages += s.v; else if (s.k === 'souls') S.souls += s.v; else if (s.k === 'shards') S.shards += s.v; else if (s.k === 'seals') S.seals[pick(SETK)] += s.v; }
let WROT = 0;
function wheelSheet() {
  const n = WHEEL.length, seg = 360 / n, can = wheelFree() || S.spins > 0;
  sheet(`<h3>Roue de la fortune <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="whWrap"><div class="whPtr"></div><div class="wheel" id="whl" style="transform:rotate(${WROT}deg);background:conic-gradient(${WHEEL.map((s, i) => `${s.c} ${i * seg}deg ${(i + 1) * seg}deg`).join(',')})">${WHEEL.map((s, i) => `<span style="transform:rotate(${i * seg + seg / 2}deg)"><b>${wheelTxt(s)}</b></span>`).join('')}</div><div class="whHub">${IC.star}</div></div>
  <p class="knote" style="text-align:center;margin:10px 0">${wheelFree() ? '1 tour gratuit aujourd\'hui' : 'Tour gratuit utilisé · reviens demain'}${S.spins ? ` · <b style="color:#ffd890">${S.spins} jeton${S.spins > 1 ? 's' : ''}</b> (passe de saison)` : ''}</p>
  <button class="btn gold" type="button" id="whGo" style="width:100%" ${can ? '' : 'disabled'}>${wheelFree() ? 'Tourner gratuitement' : S.spins ? 'Tourner · 1 jeton' : 'Plus de tours'}</button>`);
  $('whGo').onclick = () => { if (!(wheelFree() || S.spins > 0)) return; if (wheelFree()) S.wheelDay = new Date().toDateString(); else S.spins--; $('whGo').disabled = true;
    const tot = WHEEL.reduce((a, s) => a + s.w, 0); let x = Math.random() * tot, i = 0; for (; i < n; i++) { x -= WHEEL[i].w; if (x < 0) break; } i = Math.min(i, n - 1);
    const target = 360 - (i * seg + seg / 2) + rand(-seg * 0.3, seg * 0.3); WROT = WROT - (WROT % 360) + 360 * 5 + target; $('whl').style.transform = `rotate(${WROT}deg)`;
    setTimeout(() => { const s = WHEEL[i]; wheelGive(s); passAdd(10); save(); ui(); toast(`Roue : +${wheelTxt(s)} !`); if (s.w <= 4) { B.flash = { c: '255,210,120', t: 0.4, a: 0.4 }; } wheelSheet(); }, 3300); };
}
// --- passe de saison ---
const SEASON_MS = 28 * 86400000, seasonIdx = () => Math.floor(Date.now() / SEASON_MS), PASS_N = 30, passCost = t => 100 + 20 * t;
function passInit() { if (S.passS !== seasonIdx()) { S.passS = seasonIdx(); S.passP = 0; S.passClaim = {}; } }
function passTier() { passInit(); let p = S.passP, t = 0; while (t < PASS_N && p >= passCost(t + 1)) { p -= passCost(t + 1); t++; } return { t, p, need: t < PASS_N ? passCost(t + 1) : 1 }; }
function passAdd(n) { passInit(); const a = passTier().t; S.passP += n; const b = passTier().t; if (b > a) toast(`Passe de saison : palier ${b} atteint !`); }
function passRew(t) { if (t === 10) return { souls: 100, txt: '100 âmes' }; if (t === 20) return { rel: 3, txt: 'Relique légendaire' }; if (t === 30) return { fam: 4, txt: 'Familier mythique' };
  if (t % 5 === 0) return { spins: 2, seals: 20, txt: '2 jetons de roue · 20 Sceaux' }; return [{ ham: 30, txt: '30 marteaux' }, { souls: 15, txt: '15 âmes' }, { gold: 1, txt: 'Bourse d\'or' }, { pages: 40, txt: '40 pages' }][t % 4]; }
function passGive(r) { if (r.ham) S.ham += r.ham; if (r.souls) S.souls += r.souls; if (r.pages) S.pages += r.pages; if (r.spins) S.spins += r.spins; if (r.seals) S.seals[pick(SETK)] += r.seals; if (r.gold) S.gold += Math.round(1500 * Math.pow(1.11, stageIndex()));
  if (r.rel) { const L = Object.keys(REL).filter(k => REL[k].r === r.rel), id = pick(L), o = S.rels[id]; if (!o) S.rels[id] = { s: 1, c: 0 }; else if (o.s < 5) { o.c++; if (o.c >= o.s) { o.c = 0; o.s++; } } toast(`Relique : ${REL[id].n}`); }
  if (r.fam) { const L = Object.keys(FAM).filter(k => FAM[k].r === r.fam), id = pick(L), o = S.fams[id]; if (!o) S.fams[id] = { s: 1, c: 0 }; else if (o.s < 5) { o.c++; if (o.c >= o.s) { o.c = 0; o.s++; } } toast(`Familier : ${FAM[id].n}`); } }
function passSheet() {
  const P = passTier(), left = SEASON_MS - (Date.now() % SEASON_MS);
  sheet(`<h3>Passe de saison <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="psTop"><div class="psLv"><b>${P.t}</b><small>palier</small></div><div style="flex:1"><div class="psRow"><span>${P.t < PASS_N ? `${P.p} / ${P.need} points` : 'Passe terminé !'}</span><span>⏳ ${dhm(left)}</span></div><div class="afkBar"><i style="width:${P.t < PASS_N ? P.p / P.need * 100 : 100}%"></i></div></div></div>
  <p class="knote" style="margin:6px 0 8px">Gagne des points en jouant : démons, étapes, boss, forges, donjons, invocations, roue, coffre de temps.</p>
  <div class="psList">${Array.from({ length: PASS_N }, (_, i) => { const t = i + 1, r = passRew(t), ok = P.t >= t, got = S.passClaim[t], big = t % 10 === 0; return `<div class="psIt ${ok ? 'ok' : ''} ${got ? 'got' : ''} ${big ? 'big' : ''}"><em>${t}</em><span>${r.txt}</span>${got ? '<i>✓</i>' : ok ? `<button class="btn gold sm" type="button" data-pc="${t}">Prendre</button>` : `<small>${IC.lock}</small>`}</div>`; }).join('')}</div>`);
  $('mbox').querySelectorAll('[data-pc]').forEach(b => b.onclick = () => { const t = +b.dataset.pc; if (S.passClaim[t] || passTier().t < t) return; S.passClaim[t] = 1; passGive(passRew(t)); save(); ui(); const y = $('mbox').scrollTop; passSheet(); $('mbox').scrollTop = y; });
}
const passReady = () => { const P = passTier(); for (let t = 1; t <= P.t; t++) if (!S.passClaim[t]) return true; return false; };
function uiHub() { const a = $('hubAfk'); if (!a) return; const pc = Math.min(1, (Date.now() - S.afkT) / 1000 / AFK_MAX); a.style.setProperty('--p', (pc * 100).toFixed(1) + '%'); a.classList.toggle('full', pc >= 1);
  $('hubAfkD').hidden = pc < 0.25; $('hubLogD').hidden = S.loginDay === new Date().toDateString(); $('hubWhD').hidden = !(wheelFree() || S.spins > 0); $('hubPsD').hidden = !passReady(); }
