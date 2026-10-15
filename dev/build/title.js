// ================= écran titre : menu, choix du héros, tutoriel, options =================
let TITLE = false, TV = 'home', TCLS = null, TPAGE = 0, TAFTER = null, TFIRST = true;
const TCL = {
  knight: { n: 'Chevalier', r: 'Épée · équilibré', d: 'Un guerrier en armure qui tient bon face aux hordes. Robuste et régulier, il se soigne un peu à chaque coup.', pip: [3, 5, 3, 1] },
  hunter: { n: 'Chasseur', r: 'Deux arbalètes · rapide', d: 'Agile et implacable : il tire deux carreaux à chaque attaque. Fragile, mais rien ne le suit en vitesse.', pip: [4, 2, 5, 1] },
  mage: { n: 'Sorcier', r: 'Orbes explosives · lent', d: 'Ses orbes explosent au contact et frappent tous les démons autour. Lent et fragile, mais redoutable en groupe.', pip: [4, 2, 2, 5] },
};
const TPIP = ['Dégâts', 'Résistance', 'Vitesse', 'Zone'];
const TUTO = [
  ['sword', 'Le combat est automatique', 'Ton héros avance seul dans les cryptes et abat les démons. Chaque vague franchie te rapproche du <b>boss du chapitre</b>.'],
  ['ham', 'Forge ton équipement', 'Touche l\'<b>enclume</b> pour forger avec tes marteaux. Si l\'objet est meilleur, équipe-le. Sinon, recycle-le en <b>éclats</b> pour améliorer ton stuff.'],
  ['tree', 'Monte en puissance', 'Chaque niveau donne un <b>point de talent</b>. Aux niveaux <b>15, 30 et 60</b>, ton héros évolue. Au 30, choisis ta voie : le choix est définitif.'],
  ['gate', 'Donjons et raid', 'Les <b>donjons</b> donnent de l\'or, de l\'XP et des pages grâce à des tickets qui se rechargent. Le <b>raid</b> te fait gagner des plumes pour forger des ailes.'],
  ['star', 'Même absent, tu progresses', 'Ton héros farme jusqu\'à <b>8 h</b> sans toi. Reviens chaque jour pour ta <b>récompense quotidienne</b>. Touche <b>?</b> en jeu pour revoir les ressources.'],
];
const tNew = () => !S.started && !(S.forged > 0);
const tBack = '<button type="button" data-tv="home" aria-label="Retour">‹</button>';
function tCan(k, w, h, cls) { return `<canvas data-tk="${k}" width="${w}" height="${h}" class="${cls || ''}"></canvas>`; }
function tCur(c) { return c === 'hunter' ? S.hform : c === 'mage' ? S.mform : S.form; }
function titleView() {
  const el = $('tIn'), nw = tNew();
  if (TV === 'home') {
    el.innerHTML = `<div class="tLogo"><h1>GRIMLOOM</h1><small>Forge ton destin dans les ténèbres</small></div>
    <div class="tHero">${tCan('k_' + tCur(S.cls), 200, 220)}</div>
    <div class="tMenu">
      <button class="btn gold" type="button" id="tPlay">${nw ? 'Commencer l\'aventure' : 'Continuer l\'aventure'}</button>
      <div class="tRow">
        <button class="btn" type="button" data-tv="heroes">${IC.sword}Héros</button>
        <button class="btn" type="button" data-tv="tuto">${IC.book}Tutoriel</button>
        <button class="btn" type="button" data-tv="opt">${IC.gem}Options</button>
      </div>
    </div>
    <div class="tFoot">${nw ? 'Une nouvelle légende commence' : `${TCL[S.cls].n} · niveau ${S.lvl} · chapitre ${S.c}`}</div>`;
    $('tPlay').onclick = () => { if (nw) { TCLS = S.cls; TV = 'heroes'; titleView(); } else titleClose(); };
  } else if (TV === 'heroes') {
    const c = TCLS || S.cls, T = ETREE[c], C = TCL[c], cur = tCur(c);
    const ev = (k, lv) => `<div class="kt ${k === cur && !nw ? 'cur' : ''}">${tCan('k_' + k, 60, 66)}<b>${EVO[k].n.replace(/^(Le |La |L')/, '')}</b><small>${lv}</small></div>`;
    el.innerHTML = `<div class="tHead">${tBack}<h2>Choisis ton héros</h2></div>
    <div class="tCls">${Object.keys(TCL).map(k => `<div class="kt ${k === c ? 'gd' : ''}" data-tc="${k}">${tCan('k_' + ETREE[k].a[0], 72, 80)}<b>${TCL[k].n}</b><small>${TCL[k].r.split(' · ')[1]}</small></div>`).join('')}</div>
    <div class="kl tBig">${tCan('k_' + T.a[0], 128, 140)}<div><h3>${C.n}</h3><small style="font:800 11px var(--b);color:#d6aa60">${C.r}</small><p>${C.d}</p>${C.pip.map((v, i) => `<div class="tPip">${TPIP[i]}<i>${[1, 2, 3, 4, 5].map(j => `<u class="${j <= v ? 'on' : ''}"></u>`).join('')}</i></div>`).join('')}</div></div>
    <h4 class="kh">Ses évolutions</h4>
    <div class="tEvo two">${ev(T.a[0], 'Départ')}<div class="tArr">›</div>${ev(T.a[1], 'Niveau 15')}</div>
    <div class="tArr">⌄</div>
    <p class="knote" style="margin:0 0 6px;text-align:center">Au niveau 30, choisis une voie</p>
    <div class="tEvo">${T.b.map(k => ev(k, 'Niveau 30')).join('')}</div>
    <div class="tEvo" style="margin-top:2px">${T.b.map(() => '<div class="tArr">⌄</div>').join('')}</div>
    <div class="tEvo">${T.c.map(k => ev(k, 'Niveau 60')).join('')}</div>
    <div class="tGo"><button class="btn gold" type="button" id="tGo">${nw ? `Partir avec le ${C.n}` : c === S.cls ? 'Reprendre l\'aventure' : `Jouer le ${C.n}`}</button></div>`;
    el.querySelectorAll('[data-tc]').forEach(b => b.onclick = () => { TCLS = b.dataset.tc; titleView(); el.scrollTop = 0; });
    $('tGo').onclick = () => {
      if (c !== S.cls) { S.cls = c; applyEvo(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; }
      if (nw) { S.started = 1; save(); TPAGE = 0; TAFTER = 'play'; TV = 'tuto'; titleView(); } else { save(); titleClose(); }
    };
  } else if (TV === 'tuto') {
    const P = TUTO[TPAGE], last = TPAGE === TUTO.length - 1;
    el.innerHTML = `<div class="tHead">${TAFTER === 'play' ? '<button type="button" id="tSkip" aria-label="Passer" style="width:auto;padding:0 12px;font-size:14px">Passer</button>' : tBack}<h2>Comment jouer</h2></div>
    <div class="tTuto"><div class="tMed">${IC[P[0]]}</div><h3>${P[1]}</h3><p>${P[2]}</p></div>
    <div class="tDots">${TUTO.map((_, i) => `<i class="${i === TPAGE ? 'on' : ''}"></i>`).join('')}</div>
    <div class="tNav"><button class="btn" type="button" id="tPrev" ${TPAGE ? '' : 'disabled style="opacity:.4"'}>Précédent</button><button class="btn gold" type="button" id="tNext">${last ? (TAFTER === 'play' ? 'À l\'aventure !' : 'J\'ai compris') : 'Suivant'}</button></div>`;
    const done = () => { if (TAFTER === 'play') { TAFTER = null; titleClose(); } else { TV = 'home'; titleView(); } };
    $('tPrev').onclick = () => { if (TPAGE) { TPAGE--; titleView(); } };
    $('tNext').onclick = () => { if (last) done(); else { TPAGE++; titleView(); } };
    if ($('tSkip')) $('tSkip').onclick = done;
  } else if (TV === 'opt') {
    const vol = Math.round((S.vol === undefined ? 1 : S.vol) * 100);
    el.innerHTML = `<div class="tHead">${tBack}<h2>Options</h2></div>
    <div class="kl" style="padding:0 6px">
      <div class="tOpt"><span>Musique<small>Ambiance des cryptes et des boss</small></span><button type="button" class="tTog ${S.snd ? 'on' : ''}" id="tSnd" aria-label="Musique"></button></div>
      <div class="tOpt" style="border:0"><span>Volume<small id="tVolT">${vol} %</small></span><input type="range" min="0" max="100" value="${vol}" id="tVol" aria-label="Volume"></div>
    </div>
    <div class="tLinks">
      <button class="btn" type="button" id="tTuto">Revoir le tutoriel</button>
      <button class="btn" type="button" id="tAdm">Panneau admin</button>
      <button class="btn dng" type="button" id="tReset">Effacer la partie</button>
    </div>`;
    $('tSnd').onclick = () => { S.snd = !S.snd; save(); if (S.snd) { audioInit(); music(true); } else music(false); if (typeof sndIcon === 'function') sndIcon(); titleView(); };
    $('tVol').oninput = e => { S.vol = e.target.value / 100; $('tVolT').textContent = e.target.value + ' %'; if (MUSG && S.snd) MUSG.gain.setTargetAtTime(0.3 * S.vol, AC.currentTime, 0.05); };
    $('tVol').onchange = () => save();
    $('tTuto').onclick = () => { TPAGE = 0; TAFTER = null; TV = 'tuto'; titleView(); };
    $('tAdm').onclick = () => { titleClose(); showAdmin(); };
    $('tReset').onclick = () => { if (!confirm('Effacer toute ta progression ? Cette action est définitive.')) return; window.__noSave = true; try { localStorage.removeItem(KEY); } catch (e) { } location.reload(); };
  }
  el.querySelectorAll('[data-tv]').forEach(b => b.onclick = () => { TV = b.dataset.tv; if (TV === 'tuto') { TPAGE = 0; TAFTER = null; } if (TV === 'heroes') TCLS = S.cls; titleView(); el.scrollTop = 0; });
}
function titleDraw(t) {
  if (!TITLE) return; requestAnimationFrame(titleDraw);
  document.querySelectorAll('#tIn canvas[data-tk]').forEach(c => { const g = c.getContext('2d'), W = c.width, Hh = c.height; g.clearRect(0, 0, W, Hh); sprH(c.dataset.tk, 'idle_6', t / 80, W / 2, Hh - 2, (Hh - 6) / 250, 1, g); });
}
function titleOpen(v) { TITLE = true; TV = v || 'home'; $('title').hidden = false; if (!$('tBg').style.backgroundImage) $('tBg').style.backgroundImage = `url(${DUNIMG.map})`; titleView(); requestAnimationFrame(titleDraw); }
function titleClose() { TITLE = false; $('title').hidden = true; last = performance.now(); ui(); if (TFIRST) { TFIRST = false; if (TAFTER_HAM !== null) { const h = TAFTER_HAM; TAFTER_HAM = null; setTimeout(() => welcome(h), 300); } } }
let TAFTER_HAM = null;
