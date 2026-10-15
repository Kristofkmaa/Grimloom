import base64
P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v30.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
K = lambda n: 'data:image/png;base64,' + base64.b64encode(open('/home/claude/grimloom/kenney/' + n + '.png', 'rb').read()).decode()

a = s.index("  } else if (tab === 'hero') {"); b = s.index("\n}\nfunction uiTop()")
s = s[:a] + r"""  } else if (tab === 'hero') {
    const H = HEROES[S.hero], nAch = ACH.filter(a => S.ach[a[0]]).length, G = gear(), sc = setCounts();
    const tile = (ic, c, cap, val, cls) => `<div class="kt ${cls || ''}" style="--c:${c}"><i class="ki">${IC[ic]}</i><span><small>${cap}</small><b>${val}</b></span></div>`;
    let body = '';
    if (HSUB === 'profil') {
      body = `<div class="kgrid">${tile('sword', '#ff9a6a', 'Attaque', fmt(st.atk))}${tile('heart', '#ff6a7a', 'Vie', fmt(st.pv))}${tile('shield', '#9ad0ff', 'Défense', fmt(st.def))}${tile('bolt', '#ffd27a', 'Cadence', st.rate.toFixed(2))}${tile('star', '#ffe06a', 'Critique', st.crit.toFixed(1) + ' %')}${tile('star', '#ff8a3a', 'Dég. crit.', Math.round(st.cdmg) + ' %')}${tile('drop', '#e04a5a', 'Vol de vie', st.vol.toFixed(1) + ' %')}${tile('wind', '#8ae0b0', 'Esquive', st.esq.toFixed(1) + ' %')}${st.regen ? tile('heart', '#7aff9a', 'Régénération', st.regen.toFixed(1) + ' %/s') : ''}</div>
      <h4 class="kh">Éveil</h4><div class="kevo">${EVEIL.map(([r]) => `<i class="${G.a >= r ? 'on' : ''}" style="--c:${RAR[r].c}"></i>`).join('')}</div><p class="knote">${(() => { const nx = EVEIL.find(([r]) => G.a < r); return nx ? `Prochain : <b style="color:${RAR[nx[0]].c}">${nx[1]}</b>, quand ton équipement sera en moyenne ${RAR[nx[0]].n.toLowerCase()}.` : 'Éveil complet !'; })()}</p>
      ${Object.keys(sc).length ? `<h4 class="kh">Sets gravés</h4>${Object.entries(sc).map(([k, n]) => `<div class="kl kset" style="--sc:${SETS[k].c}"><div class="ksh"><b>${SETS[k].n}</b><em>${n} / 6</em></div>${SETS[k].b.map(([c, t]) => `<div class="setb ${n >= c ? 'on' : ''}"><em>${c}</em>${t}</div>`).join('')}</div>`).join('')}` : ''}
      <h4 class="kh">Progression</h4><div class="kgrid">${tile('gate', '#d6aa60', 'Meilleure étape', `${Math.floor((S.best - 1) / 10) + 1}-${(S.best - 1) % 10 + 1}`)}${tile('skull', '#c8b0a0', 'Démons tués', fmt(S.kills))}${tile('ham', '#d8dee8', 'Objets forgés', fmt(S.forged))}${tile('star', '#ffd27a', 'Succès', `${nAch} / ${ACH.length}`)}</div>`;
    } else if (HSUB === 'comp') {
      body = `<p class="knote" style="margin-top:0">Deux compagnons se battent à côté du chevalier. Monte-les de niveau avec de l'or.</p>
      <div class="kparty">${[0, 1].map(i => { const id = S.party[i]; return id ? `<div class="kt gd kps"><canvas data-pc="${id}" width="64" height="64"></canvas><span><small>${i ? 'Droite' : 'Gauche'}</small><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><em>Nv ${compLv(id)}</em></span></div>` : `<div class="kt kps empty"><span><small>${i ? 'Droite' : 'Gauche'}</small><b>Place libre</b></span></div>`; }).join('')}</div>
      ${Object.keys(COMPS).map(id => { const C = COMPS[id], o = S.comps[id], open = S.c >= C.unlock, inP = S.party.indexOf(id); return `<div class="kt krow ${o ? '' : 'lock'} ${inP >= 0 ? 'gd' : ''}"><canvas data-hc="${id}" width="72" height="72"></canvas><div class="kri"><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><small>${C.d}</small><small class="kdim">${o ? `Nv ${o.lv} · ${Math.round(compDmgPct(id))} % de ton attaque · ${compRate(id).toFixed(2)} tirs/s` : open ? 'Prêt à rejoindre ta troupe' : `Chapitre ${C.unlock}`}</small></div><div class="krb">${o ? `<button class="btn gold sm" type="button" data-up="${id}" ${S.gold < compCost(id) ? 'disabled' : ''}>Nv +1<small>${fmt(compCost(id))} or</small></button><button class="btn sm ${inP >= 0 ? 'red' : ''}" type="button" data-pt="${id}">${inP >= 0 ? 'Retirer' : 'Équiper'}</button>` : `<button class="btn gold sm" type="button" data-rc="${id}" ${open ? '' : 'disabled'}>Recruter</button>`}</div></div>`; }).join('')}`;
    } else if (HSUB === 'pet') {
      body = `<p class="knote" style="margin-top:0">Un familier flotte à côté du héros et donne un bonus. Touche-le pour l'équiper ou le retirer.</p>${Object.entries(PETS).map(([k, P0]) => { const open = S.c >= P0.unlock; return `<div class="kt krow pet2 ${S.pet === k ? 'gd' : ''} ${open ? '' : 'lock'}" data-pet="${open ? k : ''}"><canvas data-pd="${P0.dem}" width="48" height="48"></canvas><div class="kri"><b>${P0.n}</b><small>${open ? P0.d : 'Se débloque au chapitre ' + P0.unlock}</small></div><div class="krb">${S.pet === k ? '<em class="kbadge">Équipé</em>' : open ? '<em class="kbadge dim">Équiper</em>' : IC.lock}</div></div>`; }).join('')}`;
    } else {
      body = `<div class="kl kachp"><b>${nAch} / ${ACH.length}</b><div class="xpbar"><i style="width:${nAch / ACH.length * 100}%"></i></div><small>Chaque succès donne un bonus permanent.</small></div>${ACH.map(a => `<div class="kt krow ach2 ${S.ach[a[0]] ? 'gd' : 'lock'}"><i class="ki" style="--c:${S.ach[a[0]] ? '#ffd27a' : '#6a5a50'}">${S.ach[a[0]] ? IC.star : IC.lock}</i><div class="kri"><b>${a[1]}</b><small>${a[2]}</small></div><div class="krb"><em class="kbadge ${S.ach[a[0]] ? '' : 'dim'}">${Object.entries(a[4]).map(([k, v]) => `+${v} % ${{ atk: 'att.', pv: 'PV', gold: 'or' }[k]}`).join(' ')}</em></div></div>`).join('')}`;
    }
    $('panel').innerHTML = `<div class="kp"><div class="kban kg"><canvas id="heroC" width="96" height="112"></canvas><div class="kbi"><b class="kname">${H.n}</b><small class="ktitle">${title()}</small><div class="kpow"><small>Puissance</small><b>${fmt(power(st))}</b></div><div class="kxpl"><span>Niveau ${S.lvl}</span><span>${fmt(S.xp)} / ${fmt(xpNeed(S.lvl))}</span></div><div class="kxp"><i style="width:${(S.xp / xpNeed(S.lvl) * 100).toFixed(1)}%"></i></div></div>${S.tp ? `<button class="ktp" id="goTree" type="button">+${S.tp}<small>talent${S.tp > 1 ? 's' : ''}</small></button>` : ''}</div>
      ${ktabs(HSUB, [['profil', 'Profil'], ['comp', 'Troupe'], ['pet', 'Familier'], ['ach', 'Succès']], 'data-hs')}<div class="kbody">${body}</div></div>`;
    document.querySelectorAll('[data-hs]').forEach(b => b.onclick = () => { HSUB = b.dataset.hs; ui(); });
    document.querySelectorAll('[data-hc],[data-pc]').forEach(c => { const id = c.dataset.hc || c.dataset.pc, H = HEROES[id], big = !!c.dataset.hc, W = c.width; const g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, W, W); sprH(H.key, 'idle_6', performance.now() / 80, W / 2, W - 2, H.sc * (big ? 0.62 : 0.55), 1, g); requestAnimationFrame(draw); }; draw(); });
    if ($('goTree')) $('goTree').onclick = () => document.querySelector('#nav [data-t="talent"]').click();
    document.querySelectorAll('[data-pet]').forEach(b => b.onclick = () => { const k = b.dataset.pet; if (!k) return; S.pet = S.pet === k ? null : k; save(); ui(); });
    document.querySelectorAll('[data-pd]').forEach(c => { const g = c.getContext('2d'), key = c.dataset.pd, A = ASSETS.DEM[key], im = IMG['D_' + key]; const R = A.anims.walk_S; g.imageSmoothingEnabled = false; const sc = 40 / Math.max(A.cw, A.ch) * 1.4; g.drawImage(im, 0, R[0] * A.ch, A.cw, A.ch, 24 - A.ax * sc, 46 - (A.ch - A.foot) * sc, A.cw * sc, A.ch * sc); });
    document.querySelectorAll('[data-rc]').forEach(b => b.onclick = () => { const id = b.dataset.rc; S.comps[id] = { lv: 1 }; const f = S.party.indexOf(null); if (f >= 0) S.party[f] = id; save(); toast(`${HEROES[id].n} rejoint ta troupe`); ui(); });
    document.querySelectorAll('[data-up]').forEach(b => b.onclick = () => { const id = b.dataset.up, c = compCost(id); if (S.gold < c) return; S.gold -= c; S.comps[id].lv++; S.st.comp++; save(); ui(); });
    document.querySelectorAll('[data-pt]').forEach(b => b.onclick = () => { const id = b.dataset.pt, i = S.party.indexOf(id); if (i >= 0) S.party[i] = null; else { const f = S.party.indexOf(null); S.party[f >= 0 ? f : 1] = id; } B.cs = []; save(); ui(); });
  } else if (tab === 'talent') {
    const T = TREE[TBR], sp = branchSpent(TBR), sel = TSEL && NODE[TSEL] && nodeBranch(TSEL) === TBR ? TSEL : null;
    $('panel').innerHTML = `<div class="kp"><div class="kban kg kbt"><div class="kbig"><b>${S.tp}</b><small>point${S.tp > 1 ? 's' : ''} à placer</small></div><div class="kbi"><b class="kname">Arbre de talents</b><small class="kdim">Niveau ${S.lvl} · 1 point par niveau</small><small class="kdim">${treeSpent()} points placés · 4 points par palier</small></div><button class="btn sm" id="tReset" type="button" ${treeSpent() ? '' : 'disabled'}>Réinitialiser<small>${fmt(resetCost())} or</small></button></div>
      ${ktabs(TBR, Object.entries(TREE).map(([k, B0]) => [k, `${B0.n} · ${branchSpent(k)}`]), 'data-br')}
      <p class="knote kc" style="--tc:${T.c}">${T.d} · ${sp} point${sp > 1 ? 's' : ''} dans la branche</p>
      <div class="ktree" style="--tc:${T.c}">${T.tiers.map((row, ti) => { const open = sp >= ti * TIER_REQ; return `<div class="ktier ${open ? 'open' : ''}"><div class="ktl">${open ? `Palier ${ti + 1}` : `${IC.lock} ${ti * TIER_REQ} pts`}</div><div class="ktn">${row.map(k => { const N = NODE[k], r = tr(k); return `<button type="button" class="kt knode ${r ? 'gd' : ''} ${open ? '' : 'lock'} ${sel === k ? 'sel' : ''} ${N[1] === 1 ? 'cap' : ''} ${open && r < N[1] && S.tp > 0 ? 'can' : ''}" data-tn="${k}"><i class="ki" style="--c:${r ? T.c : '#8a7868'}">${open ? IC[N[2]] : IC.lock}</i><span><b>${N[0]}</b><small>${N[3](Math.max(1, r))}</small></span><em>${r}/${N[1]}</em></button>`; }).join('')}</div></div>`; }).join('')}</div>
      <div class="kl kdet">${sel ? (() => { const N = NODE[sel], r = tr(sel), open = nodeOpen(sel); return `<b class="kdn" style="color:${T.c}">${N[0]} <em>${r}/${N[1]}</em></b><p>${r ? `<span>Actuel :</span> ${N[3](r)}` : ''}${r < N[1] ? `${r ? '<br>' : ''}<span>${r ? 'Rang suivant' : 'Effet'} :</span> ${N[3](r + 1)}` : '<br><em>Rang maximum</em>'}</p>${open ? `<button class="btn gold" id="tAdd" type="button" ${S.tp > 0 && r < N[1] ? '' : 'disabled'}>${r >= N[1] ? 'Maximum atteint' : S.tp > 0 ? 'Ajouter un point' : 'Plus de points : monte de niveau'}</button>` : `<div class="tlock">${IC.lock} Place ${nodeTier(sel) * TIER_REQ - sp} point(s) de plus dans ${T.n}</div>`}`; })() : `<p class="knote" style="margin:0">Touche un talent pour voir son effet et y placer un point. Le dernier palier change ta façon de jouer.</p>`}</div></div>`;
    document.querySelectorAll('[data-br]').forEach(b => b.onclick = () => { TBR = b.dataset.br; TSEL = null; ui(); });
    document.querySelectorAll('[data-tn]').forEach(b => b.onclick = () => { TSEL = b.dataset.tn; ui(); });
    if ($('tAdd')) $('tAdd').onclick = () => { const k = TSEL, N = NODE[k]; if (S.tp < 1 || tr(k) >= N[1] || !nodeOpen(k)) return; S.tp--; S.tree[k] = tr(k) + 1; save(); const st = heroStats(); B.hero.hpMax = st.pv; sfxPlay('level'); ui(); };
    $('tReset').onclick = () => { const c = resetCost(); if (S.gold < c) { toast('Pas assez d\'or'); return; } if (!confirm('Réinitialiser l\'arbre ? Tous les points seront rendus.')) return; S.gold -= c; S.tp += treeSpent(); S.tree = {}; save(); toast('Arbre réinitialisé'); ui(); };
  } else if (tab === 'skills') {
    const n = slotCount(), owned = Object.keys(S.spells).length;
    const spt = (id, extra) => { const sp = SPELLS[id], o = S.spells[id]; return `<button type="button" class="kt kspell ${o ? '' : 'lock'} ${S.slots.includes(id) ? 'gd' : ''}" data-sp="${id}" style="--c:${sp.c}"><i class="ki">${IC[sp.ic]}</i><span><b>${sp.n}</b><small style="color:${SPRC[sp.r]}">${o ? `Nv ${o.lv} · ${o.cp}/${o.lv}` : SPR[sp.r]}</small></span></button>`; };
    $('panel').innerHTML = `<div class="kp"><div class="kban kg kbt"><div class="kbig"><b>${S.pages}</b><small>pages</small></div><div class="kbi"><b class="kname">Grimoire</b><small class="kdim">Les pouvoirs se lancent seuls en combat.</small><div class="kbtns"><button class="btn sm" type="button" id="sum1" ${S.pages < 10 ? 'disabled' : ''}>Invoquer ×1<small>10 pages</small></button><button class="btn gold sm" type="button" id="sum10" ${S.pages < 100 ? 'disabled' : ''}>×10<small>100 pages</small></button></div></div></div>
      <h4 class="kh">Équipés</h4><div class="kslots">${[0, 1, 2].map(i => { const id = S.slots[i]; if (i >= n) return `<div class="kt kslot lock"><i class="ki">${IC.lock}</i><small>Chapitre ${i === 1 ? 2 : 4}</small></div>`; return id ? `<button type="button" class="kt gd kslot" data-sp="${id}" style="--c:${SPELLS[id].c}"><i class="ki">${IC[SPELLS[id].ic]}</i><b>${SPELLS[id].n}</b><small>Nv ${S.spells[id].lv}</small></button>` : `<div class="kt kslot empty"><b>+</b><small>Libre</small></div>`; }).join('')}</div>
      <h4 class="kh">Grimoire <small>${owned} / ${Object.keys(SPELLS).length} · touche un pouvoir pour l'équiper</small></h4><div class="kgrid">${Object.keys(SPELLS).map(id => spt(id)).join('')}</div></div>`;
    $('sum1').onclick = () => summon(1); $('sum10').onclick = () => summon(10);
    document.querySelectorAll('[data-sp]').forEach(b => b.onclick = () => showSpell(b.dataset.sp));
  } else {
    $('panel').innerHTML = dunHTML();
    document.querySelectorAll('[data-dun]').forEach(b => b.onclick = () => startDungeon(b.dataset.dun));
  }""" + s[b:]

a = s.index("function dunHTML() {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r"""function dunHTML() {
  return `<div class="kp"><div class="kban kg kbt"><div class="kbig"><b>${S.keys}</b><small>clé${S.keys > 1 ? 's' : ''}</small></div><div class="kbi"><b class="kname">Donjons des sets</b><small class="kdim">3 vagues + un boss en 60 s. Gagne des Sceaux pour graver un set sur une pièce que tu portes.</small><small class="kdim">3 clés par jour · +1 par boss · perdue seulement si tu gagnes</small></div></div>
  ${SETK.map(k => `<div class="kl kdun" style="--sc:${SETS[k].c}"><div class="kdt"><div><b>${DUNS[k].n}</b><small>${SETS[k].n}</small></div><em class="kbadge">Niv. ${S.dlv[k]}</em></div><div class="kds">${SETS[k].b.map(([c, t]) => `<div><em>${c}</em><span>${t}</span></div>`).join('')}</div><div class="kdb"><span>Récompense <b>${dunReward(S.dlv[k])} Sceaux</b><br>Tu en as <b>${S.seals[k]}</b></span><button class="btn gold" type="button" data-dun="${k}" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div></div>`).join('')}</div>`;
}
""" + s[b:]

rep("let tab = 'forge', TSEL = null, HSUB = 'profil';", "let tab = 'forge', TSEL = null, HSUB = 'profil', TBR = 'carnage';\nconst ktabs = (cur, L, attr) => `<div class=\"ktabs\">${L.map(([k, n]) => `<button type=\"button\" class=\"ktab ${cur === k ? 'on' : ''}\" ${attr}=\"${k}\">${n}</button>`).join('')}</div>`;")

css = r"""
/* ===== interface Kenney (cadres or vieilli / os) ===== */
:root{--kG:url(GOLD23);--kT:url(BONE10);--kTg:url(GOLD10);--kTab:url(BONE01);--kTabg:url(GOLD01);--kL:url(BONE14);--kDiv:url(DIVF)}
.kg{border:22px solid transparent;border-image:var(--kG) 32 / 22px stretch;background:linear-gradient(#1c0d13,#0d0709) center/calc(100% + 30px) calc(100% + 30px) no-repeat padding-box}
.kt{position:relative;border:16px solid transparent;border-image:var(--kT) 32 / 16px stretch;background:linear-gradient(#170c10,#0e0709) center/calc(100% - 8px) calc(100% - 8px) no-repeat border-box;color:var(--txt);text-align:left;padding:0;font:inherit}
.kt.gd{border-image-source:var(--kTg);background:linear-gradient(#3e1220,#1c080e) center/calc(100% - 8px) calc(100% - 8px) no-repeat border-box}
.kt.lock{opacity:.5}
.kl{border:20px solid transparent;border-image:var(--kL) 32 / 20px stretch;background:linear-gradient(#0f0809,#0f0809) center/calc(100% - 10px) calc(100% - 10px) no-repeat border-box}
.kp{display:flex;flex-direction:column;padding-top:10px}
.kban{position:relative;display:flex;align-items:center;gap:12px;min-height:118px;margin-bottom:10px}
.kban canvas{width:84px;height:98px;flex:none;image-rendering:pixelated;margin:-14px 0 -14px -8px}
.kbi{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.kname{font:900 15px/1.15 var(--t);color:#f2d79a;letter-spacing:.03em}
.ktitle{font:800 10px var(--b);color:#b89a7a;letter-spacing:.12em;text-transform:uppercase}
.kdim{font:700 11px/1.35 var(--b);color:#a08a78}
.kpow{display:flex;align-items:baseline;gap:8px;margin:4px 0 2px}.kpow small{font:900 9px var(--b);color:#a08a78;letter-spacing:.14em;text-transform:uppercase}.kpow b{font:900 22px var(--t);color:#ffd890;text-shadow:0 2px 6px #000}
.kxpl{display:flex;justify-content:space-between;font:800 10.5px var(--b);color:#b89a7a}
.kxp{height:6px;border-radius:3px;background:#2a1a18;overflow:hidden;margin-top:3px}.kxp i{display:block;height:100%;background:linear-gradient(90deg,#8a1a1a,#e05a2a)}
.ktp{position:absolute;right:-8px;top:-10px;display:flex;flex-direction:column;align-items:center;padding:4px 8px;border-radius:10px;border:1.5px solid #d6aa60;background:linear-gradient(#5a1828,#2a0a12);color:#ffe6b0;font:900 16px var(--t);line-height:1;box-shadow:0 0 12px #ff5a2a55;animation:tcan 1.4s infinite}
.ktp small{font:800 8.5px var(--b);color:#e8c8a0}
.kbt .kbig{display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:66px;padding:0 4px;border-right:1px solid #ffffff14}
.kbig b{font:900 30px/1 var(--t);color:#ffd890;text-shadow:0 2px 8px #000}.kbig small{font:900 9px var(--b);color:#b89a7a;letter-spacing:.1em;text-transform:uppercase;margin-top:3px;text-align:center}
.kbt .btn.sm{align-self:center}
.kbtns{display:flex;gap:6px;margin-top:6px}.kbtns .btn{flex:1}
.ktabs{display:flex;gap:6px;margin-bottom:10px;position:sticky;top:0;z-index:6;padding:4px 0;background:#0b0608}
.ktab{flex:1;min-height:40px;border:12px solid transparent;border-image:var(--kTab) 32 / 12px stretch;background:linear-gradient(#0d0709,#0d0709) center/calc(100% - 6px) calc(100% - 6px) no-repeat border-box;font:900 11.5px var(--t);color:#a89080;letter-spacing:.03em;padding:0;white-space:nowrap}
.ktab.on{border-image-source:var(--kTabg);background:linear-gradient(#5a1828,#2a0a12) center/calc(100% - 6px) calc(100% - 6px) no-repeat border-box;color:#ffe6b0}
.kbody{display:flex;flex-direction:column}
.kh{margin:16px 0 8px;font:900 13px var(--t);color:#d6aa60;letter-spacing:.08em;text-transform:uppercase;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.kh::after{content:'';flex:1;min-width:30px;height:12px;background:var(--kDiv) left center/auto 12px no-repeat;transform:scaleX(-1);opacity:.7}
.kh small{font:700 10.5px var(--b);color:#a08a78;letter-spacing:0;text-transform:none;order:3;flex-basis:100%}
.knote{margin:8px 0 0;font:700 12px/1.45 var(--b);color:#a89080}
.kgrid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.kgrid .kt{min-height:62px;display:grid;grid-template-columns:24px 1fr;align-items:center;column-gap:8px;padding:0 2px}
.ki{font-style:normal;font-size:20px;color:var(--c,#d6aa60);display:grid;place-items:center}
.kt span{display:flex;flex-direction:column;min-width:0}.kt span small{font:900 9px var(--b);color:#a08a78;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.kt span b{font:900 17px/1.15 var(--t);color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kevo{display:flex;justify-content:space-between;padding:0 6px}.kevo i{width:36px;height:36px;border-radius:50%;border:2px solid #4a3828;background:#0e0709}.kevo i.on{border-color:var(--c);box-shadow:0 0 12px var(--c);background:radial-gradient(circle,var(--c),#000 85%)}
.kset .ksh{display:flex;justify-content:space-between;margin-bottom:6px}.kset .ksh b{font:900 14px var(--t);color:var(--sc)}.kset .ksh em{font:400 14px var(--n);font-style:normal;color:#fff}
.kset .setb{font:700 11.5px var(--b);color:#8a7868;display:flex;gap:6px;padding:2px 0}.kset .setb.on{color:var(--txt)}.kset .setb em{font-style:normal;color:var(--sc);font-weight:900}
.kparty{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:10px 0}
.kps{min-height:76px;display:flex!important;align-items:center;gap:6px}.kps canvas{width:52px;height:52px;image-rendering:pixelated}.kps em{font:400 13px var(--n);font-style:normal;color:#ffd890}.kps.empty{justify-content:center;text-align:center}.kps.empty span{align-items:center}
.krow{display:flex!important;align-items:center;gap:10px;min-height:76px;margin-bottom:6px;padding:0 2px}
.krow canvas{width:56px;height:56px;flex:none;image-rendering:pixelated}
.kri{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px}.kri b{font:900 14px var(--t);color:#f2d79a}.kri small{font:700 11.5px/1.35 var(--b);color:var(--txt)}.kri small.kdim{color:#a08a78}
.krb{display:flex;flex-direction:column;gap:4px;align-items:flex-end}.krb .btn{min-width:84px}
.kbadge{font:800 10.5px var(--b);font-style:normal;padding:3px 9px;border-radius:9px;background:#d6aa60;color:#2a1004;white-space:nowrap}.kbadge.dim{background:#2a1c18;color:#a08a78;border:1px solid #4a3828}
.ach2{min-height:64px}.ach2 .ki{width:28px;font-size:20px}
.kachp{margin-bottom:8px}.kachp b{font:900 24px var(--t);color:#ffd890}.kachp small{display:block;margin-top:6px;font:700 11.5px var(--b);color:#a08a78}
.kc{color:var(--tc);font-weight:900;margin:0 0 6px}
.ktree{display:flex;flex-direction:column;gap:4px}
.ktier{position:relative;display:grid;grid-template-columns:52px 1fr;gap:6px;align-items:center}
.ktier + .ktier::before{content:'';position:absolute;left:25px;top:-8px;width:2px;height:12px;background:#ffffff20}
.ktier.open + .ktier.open::before{background:var(--tc);box-shadow:0 0 6px var(--tc)}
.ktl{font:900 9.5px var(--b);color:#a08a78;letter-spacing:.06em;text-transform:uppercase;text-align:center;display:flex;flex-direction:column;align-items:center;gap:2px}.ktl svg{font-size:13px}
.ktier.open .ktl{color:var(--tc)}
.ktn{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:6px}
.knode{min-height:66px;display:grid!important;grid-template-columns:24px 1fr;align-items:center;column-gap:6px;padding:0 2px!important}
.knode span b{font-size:12px!important;white-space:normal!important;line-height:1.1!important}.knode span small{text-transform:none!important;letter-spacing:0!important;font:700 10px/1.25 var(--b)!important;white-space:normal!important;color:#b8a090!important}
.knode em{position:absolute;right:-6px;top:-8px;font:400 10px/1 var(--n);font-style:normal;padding:2px 5px;border-radius:7px;background:#0c0508;border:1px solid #6a5232;color:#d8c0a0}
.knode.gd em{background:var(--tc);color:#1a0a0a;border-color:var(--tc)}
.knode.sel{outline:2px solid #fff;outline-offset:2px}
.knode.can{animation:kcan 1.4s ease-in-out infinite}@keyframes kcan{50%{filter:brightness(1.35) drop-shadow(0 0 6px var(--tc))}}
.knode.cap{border-image-source:var(--kTg)}
.kdet{position:sticky;bottom:0;margin-top:10px;z-index:5;box-shadow:0 -8px 18px #000c}
.kdn{display:block;font:900 15px var(--t)}.kdn em{font:400 13px var(--n);font-style:normal;color:#fff;margin-left:6px}
.kdet p{margin:6px 0 10px;font:700 13px/1.45 var(--b);color:var(--txt)}.kdet p span{color:#d6aa60}.kdet .btn{width:100%}
.kslots{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.kslot{min-height:96px;display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:2px;text-align:center!important}
.kslot .ki{font-size:26px}.kslot b{font:900 11.5px/1.15 var(--t);color:#f2d79a}.kslot small{font:800 10px var(--b);color:#a08a78}.kslot.empty b{font:400 28px var(--n);color:#6a5a50}
.kspell{min-height:62px}
.kdun{margin-bottom:10px}
.kdt{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.kdt b{display:block;font:900 16px var(--t);color:var(--sc)}.kdt small{font:800 11.5px var(--b);color:#a08a78}
.kds{display:grid;gap:4px;margin:10px 0}.kds div{display:flex;gap:8px;font:700 11.5px/1.35 var(--b);color:var(--txt)}.kds em{flex:none;width:20px;height:20px;border-radius:5px;display:grid;place-items:center;font:400 11px var(--n);font-style:normal;background:color-mix(in srgb,var(--sc) 40%,#000);color:#fff}
.kdb{display:flex;align-items:center;justify-content:space-between;gap:10px}.kdb span{font:700 11.5px/1.4 var(--b);color:#a08a78}.kdb b{color:#ffd890}.kdb .btn{min-width:100px;min-height:44px}
/* barre du bas */
#nav{gap:4px;padding:6px 6px calc(6px + env(safe-area-inset-bottom));background:linear-gradient(#0c0608,#050304)!important;border-top:1px solid #4a3828!important}
#nav button{height:58px!important;border:14px solid transparent!important;border-image:var(--kT) 32 / 14px stretch!important;background:linear-gradient(#150b0f,#0d0709) center/calc(100% - 6px) calc(100% - 6px) no-repeat border-box!important;border-radius:0!important;padding:0!important;gap:1px!important;font:800 9.5px var(--b)!important;color:#8a7868!important}
#nav button svg{font-size:18px!important}
#nav button.on{border-image-source:var(--kTg)!important;background:linear-gradient(#5a1828,#2a0a12) center/calc(100% - 6px) calc(100% - 6px) no-repeat border-box!important;color:#ffe0a0!important}
#nav button.on::before{display:none!important}
"""
css = css.replace('GOLD23', K('gold_border_panel-border-023')).replace('BONE10', K('bone_border_panel-border-010')).replace('GOLD10', K('gold_border_panel-border-010')).replace('BONE01', K('bone_border_panel-border-001')).replace('GOLD01', K('gold_border_panel-border-001')).replace('BONE14', K('bone_border_panel-border-014')).replace('DIVF', K('gold_dividerfade_divider-fade-001'))
s = s.replace("</style>", css + "</style>", 1)
open(P, 'w').write(s); print('ok')
