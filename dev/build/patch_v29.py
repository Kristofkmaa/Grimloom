P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v29.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

PGHD = "const pghd = (t, sub, right) => `<div class=\"pghd\"><div><h2>${t}</h2><small>${sub}</small></div>${right || ''}</div>`;\nconst stabs = (cur, L, attr) => `<div class=\"stabs\">${L.map(([k, n, dot]) => `<button type=\"button\" class=\"${cur === k ? 'on' : ''}\" ${attr}=\"${k}\">${n}${dot ? `<i>${dot}</i>` : ''}</button>`).join('')}</div>`;\n"
rep("let tab = 'forge', TSEL = null;", "let tab = 'forge', TSEL = null, HSUB = 'profil';\n" + PGHD)

# ---------- plein écran hors de l'onglet équipement ----------
rep("  B.gear = gear(); uiTop(); const st = heroStats(), br = bestRar();", "  const wasFull = document.body.classList.contains('full'); document.body.classList.toggle('full', tab !== 'forge'); if (wasFull && tab === 'forge') requestAnimationFrame(fit); $('panel').scrollTop = 0;\n  B.gear = gear(); uiTop(); const st = heroStats(), br = bestRar();")
rep("draw(clock); heroPortrait(clock);", "if (!document.body.classList.contains('full')) draw(clock); heroPortrait(clock);")

# ---------- page Héros ----------
a = s.index("  } else if (tab === 'hero') {"); b = s.index("  } else if (tab === 'talent') {")
s = s[:a] + r"""  } else if (tab === 'hero') {
    const H = HEROES[S.hero], nAch = ACH.filter(a => S.ach[a[0]]).length, G = gear(), sc = setCounts();
    let body = '';
    if (HSUB === 'profil') {
      body = `<div class="hcard" style="--aura:${br >= 0 ? RAR[br].c + '88' : '#5a2a3a'}"><canvas id="heroC" width="96" height="112"></canvas><div class="hci"><b>${H.n}</b><span class="htitle">${title()}</span><div class="hlv"><em>Niveau ${S.lvl}</em><small>${fmt(S.xp)} / ${fmt(xpNeed(S.lvl))} XP</small></div><div class="xpbar"><i style="width:${(S.xp / xpNeed(S.lvl) * 100).toFixed(1)}%"></i></div>${S.tp ? `<button class="btn gold sm" id="goTree" type="button">${S.tp} point${S.tp > 1 ? 's' : ''} de talent à placer</button>` : ''}</div></div>
      <div class="bigst"><div class="pw">${IC.star}<span>Puissance</span><b>${fmt(power(st))}</b></div><div style="--c:#ff9a6a">${IC.sword}<span>Attaque</span><b>${fmt(st.atk)}</b></div><div style="--c:#ff6a7a">${IC.heart}<span>Points de vie</span><b>${fmt(st.pv)}</b></div><div style="--c:#9ad0ff">${IC.shield}<span>Défense</span><b>${fmt(st.def)}</b></div></div>
      <h4 class="sect">Combat</h4><div class="rows">${[['Attaques par seconde', st.rate.toFixed(2)], ['Critique', st.crit.toFixed(1) + ' %'], ['Dégâts critiques', Math.round(st.cdmg) + ' %'], ['Vol de vie', st.vol.toFixed(1) + ' %'], ['Régénération', st.regen.toFixed(1) + ' %/s'], ['Esquive', st.esq.toFixed(1) + ' %']].map(([a, b]) => `<div><span>${a}</span><b>${b}</b></div>`).join('')}</div>
      <h4 class="sect">Éveil <small>évolue avec la rareté de ton équipement</small></h4><div class="evtrack">${EVEIL.map(([r, t]) => `<div class="evs ${G.a >= r ? 'on' : ''}" style="--c:${RAR[r].c}"><i></i><small>${RAR[r].n}</small></div>`).join('')}</div><p class="evnext">${(() => { const nx = EVEIL.find(([r]) => G.a < r); return nx ? `Prochain : <b style="color:${RAR[nx[0]].c}">${nx[1]}</b> quand ton équipement sera en moyenne ${RAR[nx[0]].n.toLowerCase()}.` : 'Éveil complet !'; })()}</p>
      ${Object.keys(sc).length ? `<h4 class="sect">Sets gravés</h4>${Object.entries(sc).map(([k, n]) => `<div class="setbox" style="--sc:${SETS[k].c}"><div class="sethd"><b>${SETS[k].n}</b><span>${n} / 6</span></div>${SETS[k].b.map(([c, t]) => `<div class="setb ${n >= c ? 'on' : ''}"><em>${c}</em>${t}</div>`).join('')}</div>`).join('')}` : ''}
      <h4 class="sect">Progression</h4><div class="rows"><div><span>Meilleure étape</span><b>${Math.floor((S.best - 1) / 10) + 1}-${(S.best - 1) % 10 + 1}</b></div><div><span>Démons tués</span><b>${fmt(S.kills)}</b></div><div><span>Objets forgés</span><b>${fmt(S.forged)}</b></div></div>`;
    } else if (HSUB === 'comp') {
      body = `<p class="pgtip">Deux compagnons se battent à côté du chevalier. Monte-les de niveau avec de l'or.</p>
      <div class="party">${[0, 1].map(i => { const id = S.party[i]; return `<div class="pslot ${id ? '' : 'empty'}">${id ? `<canvas data-pc="${id}" width="64" height="64"></canvas><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><small>Nv ${compLv(id)}</small>` : `<b>+</b><small>${i ? 'Droite' : 'Gauche'}</small>`}</div>`; }).join('')}</div>
      <div class="comps">${Object.keys(COMPS).map(id => { const C = COMPS[id], o = S.comps[id], open = S.c >= C.unlock, inP = S.party.indexOf(id); return `<div class="comp ${o ? '' : 'lock'}"><canvas data-hc="${id}" width="72" height="72"></canvas><div class="ci"><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><small>${C.d}</small><small>${o ? `Nv ${o.lv} · ${Math.round(compDmgPct(id))} % de ton attaque · ${compRate(id).toFixed(2)} tirs/s` : open ? 'Prêt à rejoindre ta troupe' : `Se débloque au chapitre ${C.unlock}`}</small></div><div class="cb">${o ? `<button class="btn gold" type="button" data-up="${id}" ${S.gold < compCost(id) ? 'disabled' : ''}>Niveau +1<small>${fmt(compCost(id))} or</small></button><button class="btn ${inP >= 0 ? 'red' : ''}" type="button" data-pt="${id}">${inP >= 0 ? 'Retirer' : 'Équiper'}</button>` : `<button class="btn gold" type="button" data-rc="${id}" ${open ? '' : 'disabled'}>Recruter</button>`}</div></div>`; }).join('')}</div>`;
    } else if (HSUB === 'pet') {
      body = `<p class="pgtip">Un familier flotte à côté du héros et donne un bonus. Touche-le pour l'équiper ou le retirer.</p><div class="pets big">${Object.entries(PETS).map(([k, P0]) => { const open = S.c >= P0.unlock; return `<div class="pet ${S.pet === k ? 'on' : ''} ${open ? '' : 'lock'}" data-pet="${open ? k : ''}"><canvas data-pd="${P0.dem}" width="48" height="48"></canvas><div><b>${P0.n}</b><small>${open ? P0.d : 'Chapitre ' + P0.unlock}</small>${S.pet === k ? '<em>Équipé</em>' : ''}</div></div>`; }).join('')}</div>`;
    } else {
      body = `<div class="achp"><b>${nAch} / ${ACH.length}</b><div class="xpbar"><i style="width:${nAch / ACH.length * 100}%"></i></div><small>Chaque succès donne un bonus permanent.</small></div><div class="achs">${ACH.map(a => `<div class="ach ${S.ach[a[0]] ? 'on' : ''}"><span><b>${a[1]}</b><br>${a[2]}</span><em>${Object.entries(a[4]).map(([k, v]) => `+${v} % ${{ atk: 'attaque', pv: 'PV', gold: 'or' }[k]}`).join('')}</em></div>`).join('')}</div>`;
    }
    $('panel').innerHTML = `<div class="pg">${pghd('Héros', 'Ton chevalier, sa troupe et ses trophées')}${stabs(HSUB, [['profil', 'Profil', S.tp || ''], ['comp', 'Compagnons'], ['pet', 'Familiers'], ['ach', 'Succès']], 'data-hs')}<div class="pgb">${body}</div></div>`;
    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });
    document.querySelectorAll('[data-hc],[data-pc]').forEach(c => { const id = c.dataset.hc || c.dataset.pc, H = HEROES[id], big = !!c.dataset.hc, W = c.width; const g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, W, W); sprH(H.key, 'idle_6', performance.now() / 80, W / 2, W - 2, H.sc * (big ? 0.62 : 0.55), 1, g); requestAnimationFrame(draw); }; draw(); });
    if ($('goTree')) $('goTree').onclick = () => document.querySelector('#nav [data-t="talent"]').click();
    document.querySelectorAll('[data-pet]').forEach(b => b.onclick = () => { const k = b.dataset.pet; if (!k) return; S.pet = S.pet === k ? null : k; save(); ui(); });
    document.querySelectorAll('[data-pd]').forEach(c => { const g = c.getContext('2d'), key = c.dataset.pd, A = ASSETS.DEM[key], im = IMG['D_' + key]; const R = A.anims.walk_S; g.imageSmoothingEnabled = false; const sc = 40 / Math.max(A.cw, A.ch) * 1.4; g.drawImage(im, 0, R[0] * A.ch, A.cw, A.ch, 24 - A.ax * sc, 46 - (A.ch - A.foot) * sc, A.cw * sc, A.ch * sc); });
    document.querySelectorAll('[data-rc]').forEach(b => b.onclick = () => { const id = b.dataset.rc; S.comps[id] = { lv: 1 }; const f = S.party.indexOf(null); if (f >= 0) S.party[f] = id; save(); toast(`${HEROES[id].n} rejoint ta troupe`); ui(); });
    document.querySelectorAll('[data-up]').forEach(b => b.onclick = () => { const id = b.dataset.up, c = compCost(id); if (S.gold < c) return; S.gold -= c; S.comps[id].lv++; S.st.comp++; save(); ui(); });
    document.querySelectorAll('[data-pt]').forEach(b => b.onclick = () => { const id = b.dataset.pt, i = S.party.indexOf(id); if (i >= 0) S.party[i] = null; else { const f = S.party.indexOf(null); S.party[f >= 0 ? f : 1] = id; } B.cs = []; save(); ui(); });
""" + s[b:]

# ---------- page Talents ----------
rep("""    $('panel').innerHTML = `<div class="frame tt"><div class="tthd"><div><b>${S.tp}</b><small>point${S.tp > 1 ? 's' : ''} à placer</small></div><span>Niveau ${S.lvl} · 1 point par niveau</span><button class="btn" id="tReset" type="button" ${treeSpent() ? '' : 'disabled'}>Réinitialiser<small>${fmt(resetCost())} or</small></button></div>""",
    """    $('panel').innerHTML = `<div class="pg tt">${pghd('Talents', `Niveau ${S.lvl} · 1 point par niveau · 4 points par palier`, `<div class="chip big"><b>${S.tp}</b><small>point${S.tp > 1 ? 's' : ''}</small></div>`)}""")
rep("""<div class="tdet">${sel ?""", """<div class="tfoot"><button class="btn sm" id="tReset" type="button" ${treeSpent() ? '' : 'disabled'}>Réinitialiser l'arbre · ${fmt(resetCost())} or</button></div><div class="tdet">${sel ?""")

# ---------- page Pouvoirs ----------
rep("""    $('panel').innerHTML = `<div class="frame" style="padding:12px"><h3>Pouvoirs équipés</h3><div class="spslots">""",
    """    $('panel').innerHTML = `<div class="pg">${pghd('Pouvoirs', 'Lancés automatiquement en combat', `<div class="chip">${IC.book}<b>${S.pages}</b><small>pages</small></div>`)}<div class="pgb"><h4 class="sect">Équipés</h4><div class="spslots">""")
rep("""    <div class="summon"><div><b>${S.pages}</b><small>pages de grimoire</small><small>+1 par vague · +10 par boss · donjons</small></div><button class="btn" type="button" id="sum1" ${S.pages < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 pages</small></button><button class="btn gold" type="button" id="sum10" ${S.pages < 100 ? 'disabled' : ''}>×10<small>100 pages</small></button></div>
    <h3 style="margin-top:14px">Grimoire · ${owned}/${Object.keys(SPELLS).length}</h3><div class="spgrid">${Object.keys(SPELLS).map(id => spCard(id)).join('')}</div></div>`;""",
    """    <h4 class="sect">Invocation</h4><div class="summon2"><p>Chaque invocation donne un pouvoir au hasard, ou de l'expérience pour un pouvoir déjà obtenu.</p><div class="row"><button class="btn" type="button" id="sum1" ${S.pages < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 pages</small></button><button class="btn gold" type="button" id="sum10" ${S.pages < 100 ? 'disabled' : ''}>Invoquer ×10<small>100 pages</small></button></div></div>
    <h4 class="sect">Grimoire <small>${owned} / ${Object.keys(SPELLS).length} · touche un pouvoir pour l'équiper</small></h4><div class="spgrid">${Object.keys(SPELLS).map(id => spCard(id)).join('')}</div></div></div>`;""")

# ---------- page Donjons ----------
a = s.index("function dunHTML() {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r"""function dunHTML() {
  return `<div class="pg">${pghd('Donjons', '3 vagues + un boss en 60 secondes', `<div class="chip">${IC.key}<b>${S.keys}</b><small>clés</small></div>`)}<div class="pgb"><p class="pgtip">Gagne des <b>Sceaux</b> pour graver un set sur une pièce que tu portes. 3 clés par jour, +1 par boss de chapitre. La clé n'est perdue qu'en cas de victoire.</p>
  ${SETK.map(k => `<div class="dun2" style="--sc:${SETS[k].c}"><div class="dtop"><div><b>${DUNS[k].n}</b><small>${SETS[k].n}</small></div><span class="dlv">Niv. ${S.dlv[k]}</span></div><div class="dset">${SETS[k].b.map(([c, t]) => `<div><em>${c}</em>${t}</div>`).join('')}</div><div class="dbot"><span>Récompense <b>${dunReward(S.dlv[k])} Sceaux</b> · tu en as <b>${S.seals[k]}</b></span><button class="btn gold" type="button" data-dun="${k}" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div></div>`).join('')}</div></div>`;
}
""" + s[b:]
# entrer dans un donjon ramène sur l'écran de combat
rep("B.dun = { k, lv: S.dlv[k], w: 0, t: 60 };", "tab = 'forge'; document.querySelectorAll('#nav button').forEach(x => x.classList.toggle('on', x.dataset.t === 'forge'));\n  B.dun = { k, lv: S.dlv[k], w: 0, t: 60 };")

rep("const IC = {", """const IC = {
  book: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h7a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-5a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h5z"/></svg>',
  key: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>',""")

s = s.replace("</style>", r"""
/* ===== pages plein écran ===== */
body.full #stageWrap,body.full #questBar,body.full #botBar,body.full #stageBar{display:none!important}
body.full #panel{padding:0 12px 14px}
.pg{display:flex;flex-direction:column;gap:0}
.pghd{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 2px 10px}
.pghd h2{margin:0;font:900 24px var(--t);color:var(--gold2);letter-spacing:.06em;text-shadow:0 3px 0 #000}
.pghd small{display:block;margin-top:2px;font:700 12px var(--b);color:var(--dim)}
.chip{display:flex;align-items:center;gap:6px;padding:6px 12px;border-radius:14px;background:#0007;border:1.5px solid var(--goldd);color:var(--gold);font-size:17px;white-space:nowrap}
.chip b{font:400 20px var(--n);color:var(--gold2)}.chip small{font:800 10px var(--b);color:var(--dim)}
.chip.big{flex-direction:column;gap:0;padding:4px 14px;border-color:var(--gold)}.chip.big b{font-size:26px;line-height:1}
.stabs{display:flex;gap:4px;padding:4px;margin-bottom:12px;border-radius:14px;background:#0006;border:1px solid #ffffff10;position:sticky;top:0;z-index:5;backdrop-filter:blur(6px)}
.stabs button{flex:1;position:relative;min-height:38px;border:0;border-radius:10px;background:none;color:var(--dim);font:800 12.5px var(--b);padding:0 4px}
.stabs button.on{background:linear-gradient(#7a1a30,#4a0e1e);color:#ffe3a0;box-shadow:inset 0 1px 0 #ffffff20,0 2px 6px #0008}
.stabs button i{position:absolute;top:2px;right:4px;min-width:16px;height:16px;border-radius:8px;background:#3ad05a;color:#fff;font:400 10px/16px var(--n);font-style:normal}
.pgb{display:flex;flex-direction:column}
.sect{margin:18px 0 8px;font:900 15px var(--t);color:var(--gold2);letter-spacing:.06em;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.sect:first-child{margin-top:0}
.sect small{font:700 11px var(--b);color:var(--dim);letter-spacing:0}
.pgtip{margin:0 0 12px;font:700 13px/1.45 var(--b);color:var(--dim)}.pgtip b{color:var(--gold2)}
.btn.sm{min-height:36px;font-size:12.5px;padding:4px 12px}
.hcard{display:flex;gap:14px;align-items:center;padding:12px;border-radius:16px;background:linear-gradient(135deg,#2e1622,#150a10);border:1.5px solid #6b3a2e}
.hcard canvas{width:96px;height:112px;flex:none;image-rendering:pixelated;border-radius:12px;background:radial-gradient(60% 40% at 50% 85%,var(--aura),#140a0f)}
.hci{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}
.hci > b{font:900 17px/1.15 var(--t);color:var(--gold2)}
.htitle{align-self:flex-start;font:800 11px var(--b);padding:2px 8px;border-radius:8px;background:#ffc23a22;color:#ffd27a;border:1px solid #ffc23a55}
.hlv{display:flex;justify-content:space-between;align-items:baseline;margin-top:4px}.hlv em{font:400 16px var(--n);font-style:normal;color:#fff}.hlv small{font:700 11px var(--b);color:var(--dim)}
.hci .btn{margin-top:6px}
.bigst{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.bigst div{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center;padding:10px 12px;border-radius:14px;background:#ffffff07;border:1px solid #ffffff12;color:var(--c,var(--gold))}
.bigst svg{grid-row:span 2;font-size:24px}.bigst span{font:800 11px var(--b);color:var(--dim)}.bigst b{font:400 22px/1.1 var(--n);color:#fff}
.bigst .pw{grid-column:span 2;background:linear-gradient(90deg,#4a2a10,#1a0c10);border-color:#c88a1a88}.bigst .pw b{font-size:28px;color:#ffe3a0}
.rows{display:grid;border-radius:14px;overflow:hidden;border:1px solid #ffffff10}
.rows div{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#ffffff05;font:700 13px var(--b);color:var(--dim)}
.rows div:nth-child(odd){background:#ffffff0a}.rows b{font:400 16px var(--n);color:#fff}
.evtrack{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;position:relative}
.evs{display:flex;flex-direction:column;align-items:center;gap:5px}.evs i{width:26px;height:26px;border-radius:50%;border:2px solid #4a3038;background:#150a0f}
.evs.on i{border-color:var(--c);background:radial-gradient(circle,var(--c),color-mix(in srgb,var(--c) 30%,#000));box-shadow:0 0 12px var(--c)}
.evs small{font:800 9.5px var(--b);color:var(--dim)}.evs.on small{color:var(--c)}
.evnext{margin:10px 0 0;font:700 12px/1.45 var(--b);color:var(--dim)}
.achp{padding:12px;border-radius:14px;background:#ffffff07;border:1px solid #ffffff12;margin-bottom:10px}.achp b{font:400 24px var(--n);color:var(--gold2)}.achp small{display:block;margin-top:6px;font:700 12px var(--b);color:var(--dim)}
.pets.big{grid-template-columns:1fr}.pets.big .pet{padding:12px;gap:12px}.pets.big canvas{width:64px;height:64px}.pets.big .pet b{font-size:15px}.pets.big .pet small{font-size:12.5px}.pet em{display:inline-block;margin-top:4px;font:800 10px var(--b);font-style:normal;padding:2px 8px;border-radius:8px;background:var(--gold);color:#2a1004}
.spslots .sps{min-height:96px;justify-content:center}
.summon2{padding:12px;border-radius:14px;background:linear-gradient(135deg,#2e1430,#140a14);border:1.5px solid #8a4ac066}
.summon2 p{margin:0 0 10px;font:700 12.5px/1.45 var(--b);color:var(--dim)}.summon2 .row{gap:8px}.summon2 .btn{flex:1;min-height:50px}
.dun2{margin-bottom:10px;padding:12px;border-radius:16px;background:linear-gradient(135deg,color-mix(in srgb,var(--sc) 16%,#1c0d14),#110709);border:1.5px solid color-mix(in srgb,var(--sc) 55%,transparent);border-left:5px solid var(--sc)}
.dtop{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.dtop b{display:block;font:900 17px var(--t);color:var(--sc)}.dtop small{font:800 12px var(--b);color:var(--dim)}
.dlv{font:400 14px var(--n);padding:3px 10px;border-radius:10px;background:#0007;border:1.5px solid var(--sc);color:#fff;white-space:nowrap}
.dset{display:grid;gap:4px;margin:10px 0}.dset div{display:flex;gap:8px;font:700 11.5px/1.35 var(--b);color:var(--txt)}.dset em{flex:none;width:20px;height:20px;border-radius:6px;display:grid;place-items:center;font:400 11px var(--n);font-style:normal;background:color-mix(in srgb,var(--sc) 35%,#000);color:#fff}
.dbot{display:flex;align-items:center;justify-content:space-between;gap:10px}.dbot span{font:700 12px var(--b);color:var(--dim)}.dbot b{color:var(--gold2)}.dbot .btn{min-width:96px;min-height:44px}
.tt .ttree{gap:8px}.tt .tn{width:50px;height:50px;font-size:21px}.tt .tn.cap{width:56px;height:56px}.tt .trow{padding:11px 0}
.tfoot{display:flex;justify-content:flex-end;margin-top:10px}
.tt .tdet{position:sticky;bottom:0;background:linear-gradient(#1e0e16,#140a0f);border:1.5px solid #6b3a2e;box-shadow:0 -6px 16px #000a;z-index:4}
</style>""", 1)
open(P, 'w').write(s); print('ok')
