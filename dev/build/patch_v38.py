P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v38.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
rep('<div class="shardp" title="Éclats : recycle des objets, sert à les améliorer">${SHARD_IC}<b>${fmt(S.shards)}</b> éclats</div>',
    '<div class="shardp" title="Éclats : recycle des objets, sert à les améliorer">${SHARD_IC}<b>${fmt(S.shards)}</b> éclats</div><button type="button" id="wingSlot" class="kt wslot ${wEq() ? \'gd\' : \'\'}">${wEq() ? `<canvas id="wingMini" width="84" height="54"></canvas><span><small>Ailes · Nv ${wlv(wEq())}</small><b style="color:${WINGS[wEq()].c}">${WINGS[wEq()].n.replace(\'Ailes \', \'\').replace(/^(du |de |d\')/, \'\')}</b></span>` : `<i class="wplus">+</i><span><small>Emplacement</small><b>Ailes</b></span>`}</button>')
rep("    requestAnimationFrame(drawHeroCard);", r"""    requestAnimationFrame(drawHeroCard);
    $('wingSlot').onclick = wingSheet;
    { const c = $('wingMini'); if (c) { const w = wEq(), g = c.getContext('2d'); const draw = () => { if (!c.isConnected || !wEq()) return; g.clearRect(0, 0, 84, 54); if (WING_IMG.complete) { const f = [0, 1, 2, 3, 2, 1][Math.floor(performance.now() / 190) % 6]; g.imageSmoothingEnabled = false; g.drawImage(WING_IMG, f * 168, WINGS[w].row * 168, 168, 108, 0, 0, 84, 54); } requestAnimationFrame(draw); }; draw(); } }""")
rep("function showForge() {", r"""function wingSheet() { // choisir ses ailes depuis la fiche d'équipement
  sheet(`<h3>Ailes <button class="x" type="button" aria-label="Fermer">✕</button></h3><p style="margin:0 0 10px;color:var(--dim);font:700 12.5px/1.4 var(--b)">Tu as <b style="color:#ffd890">${S.plumes} plumes</b> (Donjons › Raid). Une seule paire équipée, elle apparaît sur le dos du chevalier.</p>
  ${WK.map(k => { const W0 = WINGS[k], r = wlv(k), eq = S.wingEq === k && r; return `<div class="kt krow wrow ${eq ? 'gd' : ''} ${r ? '' : 'lock'}"><canvas data-wg="${k}" width="96" height="72"></canvas><div class="kri"><b style="color:${W0.c}">${W0.n}${r ? ` <em class="kbadge" style="margin-left:4px">Nv ${r}</em>` : ''}</b><small>${W0.st(Math.max(1, r))}</small><small class="kdim">${W0.sp(Math.max(1, r))}</small></div><div class="krb">${r ? `<button class="btn sm ${eq ? 'red' : 'gold'}" type="button" data-weq="${k}">${eq ? 'Retirer' : 'Équiper'}</button><button class="btn sm" type="button" data-wup="${k}" ${r >= WMAX || S.plumes < wingCost(r) ? 'disabled' : ''}>${r >= WMAX ? 'Max' : 'Nv +1'}<small>${r >= WMAX ? '' : wingCost(r) + ' plumes'}</small></button>` : `<button class="btn gold sm" type="button" data-wun="${k}" ${S.plumes < wingUnlock() ? 'disabled' : ''}>Débloquer<small>${wingUnlock()} plumes</small></button>`}</div></div>`; }).join('')}`);
  const mb = $('mbox'); mb.querySelector('.x').onclick = () => { closeM(); ui(); };
  mb.querySelectorAll('[data-wg]').forEach(c => { const W0 = WINGS[c.dataset.wg], g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, 96, 72); if (WING_IMG.complete) { const f = [0, 1, 2, 3, 2, 1][Math.floor(performance.now() / 190) % 6]; g.imageSmoothingEnabled = false; g.drawImage(WING_IMG, f * 168, W0.row * 168, 168, 130, 0, 0, 96, 74); } requestAnimationFrame(draw); }; draw(); });
  const after = () => { save(); const st = heroStats(); B.hero.hpMax = st.pv; wingSheet(); };
  mb.querySelectorAll('[data-wun]').forEach(b => b.onclick = () => { const k = b.dataset.wun; if (S.plumes < wingUnlock()) return; S.plumes -= wingUnlock(); S.wings[k] = 1; if (!wEq()) S.wingEq = k; sfxPlay('reward'); toast(`${WINGS[k].n} débloquées !`); after(); });
  mb.querySelectorAll('[data-wup]').forEach(b => b.onclick = () => { const k = b.dataset.wup, c = wingCost(wlv(k)); if (S.plumes < c || wlv(k) >= WMAX) return; S.plumes -= c; S.wings[k]++; after(); });
  mb.querySelectorAll('[data-weq]').forEach(b => b.onclick = () => { const k = b.dataset.weq; S.wingEq = S.wingEq === k ? null : k; equipFx({ r: 4 }); after(); });
}
function showForge() {""")
s = s.replace("</style>", r"""
#heroCell .wslot{order:-1;margin-top:6px;display:flex;align-items:center;gap:6px;min-width:150px;min-height:52px;padding:0 6px 0 0;cursor:pointer}
.wslot canvas{width:62px;height:40px;image-rendering:pixelated;flex:none}
.wslot span small{font-size:8.5px!important}.wslot span b{font-size:13px!important}
.wslot .wplus{width:40px;text-align:center;font:400 26px var(--n);font-style:normal;color:#8a7868}
#forgeBtn .chest{width:140px!important;height:210px!important;margin-left:-70px!important}
</style>""", 1)
open(P, 'w').write(s); print('ok')
