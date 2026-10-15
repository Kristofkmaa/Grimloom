// ================= page Invocation (bannières, vedette, animation) =================
let SUMTAB = 'fam';
const BAN_MS = 3 * 86400000, banIdx = () => Math.floor(Date.now() / BAN_MS), banLeft = () => BAN_MS - (Date.now() % BAN_MS);
const famFeat = () => { const L = Object.keys(FAM).filter(k => FAM[k].r >= 3); return L[banIdx() % L.length]; };
const spFeat = () => { const L = Object.keys(SPELLS).filter(k => SPELLS[k].r >= 3); return L[(banIdx() + 1) % L.length]; };
const dhm = ms => { const h = Math.floor(ms / 3600000), d = Math.floor(h / 24); return d ? `${d} j ${h % 24} h` : `${h} h ${Math.floor(ms / 60000) % 60} min`; };
function sumFx(color, cb) { // cercle runique + rayon de la couleur de la meilleure rareté
  const d = document.createElement('div'); d.id = 'sumAnim'; d.style.setProperty('--bc', color);
  d.innerHTML = '<div class="saCircle"><i></i><i></i><i></i></div><div class="saBeam"></div><div class="saFlash"></div><small>Touche pour passer</small>';
  $('app').appendChild(d); let done = false; const end = () => { if (done) return; done = true; d.remove(); cb(); };
  d.onclick = end; setTimeout(end, 2100);
}
function sumPage(tab) {
  if (tab) SUMTAB = tab; let pg = $('sumPg'); if (!pg) { pg = document.createElement('div'); pg.id = 'sumPg'; $('app').appendChild(pg); }
  const fam = SUMTAB === 'fam', ff = famFeat(), sf = spFeat(), F = FAM[ff], SP = SPELLS[sf];
  const cur = fam ? S.souls : S.pages, curN = fam ? 'âmes' : 'pages', pity = fam ? S.famPity : (S.spPity || 0);
  pg.innerHTML = `<div class="spHead"><button type="button" class="spX" aria-label="Fermer">‹</button><b>Invocation</b><div class="spCur">${fam ? '<i class="fsoul"></i>' : IC.book}<b>${fmt(cur)}</b><small>${curN}</small></div></div>
  <div class="spTabs"><button type="button" data-st="fam" class="${fam ? 'on' : ''}">Familiers</button><button type="button" data-st="grim" class="${fam ? '' : 'on'}">Grimoire</button></div>
  <div class="spBan" style="background-image:url(${fam ? SUMBAN.fam : SUMBAN.grim})"><div class="spGlow"></div>
    <div class="spTxt"><em>${fam ? 'Bannière des familiers' : 'Bannière du grimoire'}</em><h2>INVOCATION</h2><small>Vedette · chances ×2</small></div>
    <div class="spFeat" style="--rc:${fam ? FRC[F.r] : SPRC[SP.r]}">${fam ? `<canvas data-famc="${ff}" width="96" height="96"></canvas>` : `<canvas data-spv="${sf}" width="128" height="96"></canvas>`}<b>${fam ? F.n : SP.n}</b><small>${fam ? FRN[F.r] : SPR[SP.r]}</small></div>
    <div class="spTime">⏳ Change dans ${dhm(banLeft())}</div></div>
  <div class="spPity"><div><span>Légendaire garanti</span><b>${pity} / 40</b></div><i><u style="width:${Math.min(100, pity / 40 * 100)}%"></u></i></div>
  <div class="spRates">${fam ? FRN.map((n, i) => `<span style="color:${FRC[i]}">${n} ${FRATE[i]} %</span>`).join('') : [1, 2, 3, 4].map(r => `<span style="color:${SPRC[r]}">${SPR[r]} ${[0, 50, 30, 15, 5][r]} %</span>`).join('')}</div>
  <div class="spBtns"><button class="btn" type="button" id="spOne" ${cur < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 ${curN}</small></button><button class="btn gold" type="button" id="spTen" ${cur < 100 ? 'disabled' : ''}>Invoquer ×10<small>100 ${curN}</small></button></div>
  <button type="button" class="spColl" id="spColl">${fam ? `Voir la collection · ${Object.keys(S.fams).length} / ${Object.keys(FAM).length}` : `Voir le grimoire · ${Object.keys(S.spells).length} / ${Object.keys(SPELLS).length}`} ›</button>
  <p class="spWhere">${fam ? 'Âmes : boss (+8), nouvelles étapes (+1), raid.' : 'Pages : étapes, boss, Scriptorium maudit, hors ligne.'}</p>`;
  pg.querySelector('.spX').onclick = () => { pg.remove(); ui(); };
  pg.querySelectorAll('[data-st]').forEach(b => b.onclick = () => sumPage(b.dataset.st));
  $('spOne').onclick = () => fam ? famSummon(1) : summon(1); $('spTen').onclick = () => fam ? famSummon(10) : summon(10);
  $('spColl').onclick = () => { pg.remove(); if (fam) famSheet(); else { document.querySelector('#nav [data-t="skills"]').click(); } };
  pg.querySelectorAll('canvas[data-famc]').forEach(c => { const g = c.getContext('2d'), im = IMG.fam_sp, Fx = FAM[c.dataset.famc]; const dr = () => { if (!c.isConnected) return; g.clearRect(0, 0, 96, 96); g.imageSmoothingEnabled = false; if (im.complete) g.drawImage(im, Fx.i * 128, 0, 128, 128, 0, 4 + Math.sin(performance.now() / 400) * 4, 96, 96); requestAnimationFrame(dr); }; dr(); });
  spvLoop();
}
