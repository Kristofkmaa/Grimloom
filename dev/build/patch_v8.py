P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v9.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

# ---------- sauvegarde : sac ----------
rep("forged: 0, best: 1 };\ntry { const o = JSON.parse(localStorage.getItem(KEY)); if (o) S = Object.assign(S, o); } catch (e) { }",
    "forged: 0, best: 1, bag: [] };\ntry { const o = JSON.parse(localStorage.getItem(KEY)); if (o) S = Object.assign(S, o); } catch (e) { }\nif (!Array.isArray(S.bag)) S.bag = [];\nconst BAG_MAX = 40;")

# ---------- sets ----------
rep("function heroStats() {", r"""// ================= sets d'équipement (bonus à 2, 4 et 6 pièces) =================
const SETS = {
  sang: { n: 'Étreinte du Sang', c: '#ff3a5a', b: [[2, 'Vol de vie +5 %'], [4, 'Attaque +25 %'], [6, 'Chaque démon tué rend 5 % des PV · +35 % de dégâts aux élites et boss']] },
  os: { n: 'Garde de l\'Ossuaire', c: '#e8dcc0', b: [[2, 'Points de vie +20 %'], [4, 'Défense +40 % · régénération +1 %/s'], [6, 'Dégâts subis −30 % · la défense augmente l\'attaque']] },
  braise: { n: 'Furie des Braises', c: '#ff8a2a', b: [[2, 'Vitesse d\'attaque +15 %'], [4, 'Tirs explosifs (40 % autour de la cible)'], [6, 'Toutes les 5 attaques : nova de feu à 300 % sur tous les démons']] },
  givre: { n: 'Murmure du Givre', c: '#7ad8ff', b: [[2, 'Critique +8 %'], [4, 'Les tirs ralentissent les démons'], [6, 'Dégâts critiques +100 % · +30 % de dégâts aux démons ralentis']] },
};
const SETK = Object.keys(SETS);
function setCounts(eq) { const n = {}; for (const sl of SLOTS) { const it = (eq || S.eq)[sl.id]; if (it && it.set) n[it.set] = (n[it.set] || 0) + 1; } return n; }
function heroStats() {""")
rep("""  return { atk, pv, def: t.def, crit: Math.min(75, t.crit), cdmg: t.cdmg, rate: 1.1 * H.spd * (1 + t.vit / 100), vol: t.vol, regen: t.regen, esq: Math.min(40, t.esq) };
}""", """  const o = { atk, pv, def: t.def, crit: t.crit, cdmg: t.cdmg, rate: 1.1 * H.spd * (1 + t.vit / 100), vol: t.vol, regen: t.regen, esq: Math.min(40, t.esq), splash: !!H.splash, chill: !!H.chill, killHeal: 0, bigDmg: 0, dmgRed: 0, nova: false, slowBonus: 0 };
  const n = setCounts(), has = (k, c) => (n[k] || 0) >= c;
  if (has('sang', 2)) o.vol += 5; if (has('sang', 4)) o.atk *= 1.25; if (has('sang', 6)) { o.killHeal = 5; o.bigDmg = 0.35; }
  if (has('os', 2)) o.pv *= 1.2; if (has('os', 4)) { o.def *= 1.4; o.regen += 1; } if (has('os', 6)) { o.dmgRed = 0.3; o.atk += o.def * 0.8; }
  if (has('braise', 2)) o.rate *= 1.15; if (has('braise', 4)) o.splash = true; if (has('braise', 6)) o.nova = true;
  if (has('givre', 2)) o.crit += 8; if (has('givre', 4)) o.chill = true; if (has('givre', 6)) { o.cdmg += 100; o.slowBonus = 0.3; }
  o.crit = Math.min(75, o.crit); return o;
}""")
# appartenance à un set (rare et plus)
rep("  return { slot: sl.id, r, L, main, subs, v: Math.round(4 * SCALE(L) * RMULT[r]) };",
    "  const set = r >= 2 && Math.random() < 0.3 + (r - 2) * 0.12 ? pick(SETK) : null;\n  return { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7), slot: sl.id, r, L, main, subs, set, v: Math.round(4 * SCALE(L) * RMULT[r]) };")
rep("function itemPower(it) { const o = itemStats(it); let p = 0;", "function itemPower(it) { const o = itemStats(it); let p = it.set ? 30 * (it.r + 1) * (1 + it.L * 0.05) : 0;")

# ---------- effets des sets en combat ----------
rep("const crit = Math.random() * 100 < st.crit, dmg = st.atk * (crit ? st.cdmg / 100 : 1) * rand(0.92, 1.08);\n  B.shots.push({ X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: H.splash, chill: H.chill,",
    "const crit = Math.random() * 100 < st.crit, dmg = st.atk * (crit ? st.cdmg / 100 : 1) * rand(0.92, 1.08) * (1 + (t.boss || t.elite ? st.bigDmg : 0) + (t.chill > 0 ? st.slowBonus : 0));\n  if (st.nova && (B.shotN = (B.shotN || 0) + 1) % 5 === 0) novaFire(st);\n  B.shots.push({ X: 0, z: 0.02, h: 40, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: st.splash, chill: st.chill,")
rep("function hitEnemy(e, dmg, crit) {", """function novaFire(st) { // set Furie des Braises (6) : onde de feu sur tous les démons visibles
  B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.6, c: '#ff8a2a' }); B.shake = Math.max(B.shake, 3);
  for (const e of B.en) if (!e.dead && e.spawn <= 0) { sfx('feu', sx(e.X, e.z), py(e.z) - 20 * sOf(e.z), 70 * sOf(e.z), 0.4); hitEnemy(e, st.atk * 3, false); }
}
function hitEnemy(e, dmg, crit) {""")
rep("if (e.hp <= 0) { e.dead = 1; e.deadT = 0;", "if (e.hp <= 0) { e.dead = 1; e.deadT = 0; if (st.killHeal) B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + B.hero.hpMax * st.killHeal / 100);")
rep("d = Math.max(1, d * (100 / (100 + st.def * 4)));", "d = Math.max(1, d * (100 / (100 + st.def * 4)) * (1 - st.dmgRed));")
# anneau de la nova
rep("for (const f of B.fx) { const p = f.t / f.d; if (f.k === 'p') {", "for (const f of B.fx) { const p = f.t / f.d; if (f.k === 'ring') { ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = f.c; ctx.globalAlpha = 1 - p; ctx.lineWidth = 6 * (1 - p) + 1; ctx.beginPath(); ctx.ellipse(f.x, f.y, 30 + p * 260, (30 + p * 260) * 0.35, 0, 0, TAU); ctx.stroke(); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; continue; } if (f.k === 'p') {")

# ---------- fiche d'objet : set + actions sac ----------
rep("""<div class="stats">${statLines(it, other)}</div><div class="pw">""", """<div class="stats">${statLines(it, other)}</div>${setHTML(it)}<div class="pw">""")
a = s.index("function showItem(it, isNew) {"); b = s.index("function equipFx(it)")
s = s[:a] + r'''function setHTML(it) {
  if (!it.set) return ''; const S0 = SETS[it.set], n = setCounts()[it.set] || 0;
  return `<div class="setbox" style="--sc:${S0.c}"><div class="sethd"><b>${S0.n}</b><span>${n} / 6 équipées</span></div>${S0.b.map(([k, t]) => `<div class="setb ${n >= k ? 'on' : ''}"><em>${k}</em>${t}</div>`).join('')}</div>`;
}
function toBag(it) { if (S.bag.length >= BAG_MAX) { toast('Sac plein'); return false; } S.bag.push(it); return true; }
function equipItem(it) { const cur = S.eq[it.slot]; S.bag = S.bag.filter(x => x !== it && x.id !== it.id); if (cur) S.bag.push(cur); S.eq[it.slot] = it; }
function showItem(it, mode) { // mode : true = forgé, null = équipé, 'bag' = dans le sac
  const cur = S.eq[it.slot], nm = SLOTS.find(q => q.id === it.slot).n, isNew = mode === true;
  if (isNew || mode === 'bag') {
    const better = !cur || itemPower(it) > itemPower(cur), full = isNew && S.bag.length >= BAG_MAX;
    sheet(`<h3>${isNew ? 'Nouvel objet' : 'Objet du sac'} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, isNew ? 'Forgé' : 'Dans le sac', cur)}${cur ? cardHTML(cur, 'Équipé actuellement', null, 'cur') : ''}
    <div class="row" style="margin-top:14px"><button class="btn" id="sellB" type="button" style="flex:1">Vendre<small>+${fmt(it.v)} or</small></button>${isNew ? `<button class="btn" id="bagB" type="button" style="flex:1" ${full ? 'disabled' : ''}>Garder<small>sac ${S.bag.length}/${BAG_MAX}</small></button>` : ''}<button class="btn ${better ? 'gold' : ''}" id="eqB" type="button" style="flex:1.3">Équiper<small>${cur ? 'l\'ancien va au sac' : 'emplacement vide'}</small></button></div>`);
    $('mbox').querySelector('.x').onclick = isNew ? () => { if (!toBag(it)) S.gold += it.v; closeM(); } : () => openBag(it.slot);
    $('sellB').onclick = () => { S.gold += it.v; S.bag = S.bag.filter(x => x.id !== it.id); if (isNew) closeM(); else openBag(); toast(`Vendu +${fmt(it.v)} or`); };
    if ($('bagB')) $('bagB').onclick = () => { toBag(it); closeM(); toast(`${nm} rangé dans le sac`); };
    $('eqB').onclick = () => { if (cur && S.bag.length >= BAG_MAX && isNew) { S.gold += cur.v; S.eq[it.slot] = it; } else equipItem(it); closeM(); equipFx(it); toast(`${nm} ${RAR[it.r].n.toLowerCase()} équipé`); };
  } else {
    const alt = S.bag.filter(x => x.slot === it.slot).length;
    sheet(`<h3>${nm} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Équipé', null)}
    <div class="row" style="margin-top:14px"><button class="btn" id="unB" type="button" style="flex:1">Retirer<small>vers le sac</small></button><button class="btn gold" id="altB" type="button" style="flex:1.3" ${alt ? '' : 'disabled'}>Changer<small>${alt} dans le sac</small></button></div>`);
    $('unB').onclick = () => { if (toBag(it)) { delete S.eq[it.slot]; closeM(); } };
    $('altB').onclick = () => openBag(it.slot);
  }
  $('mbox').querySelectorAll('[data-ci]').forEach(c => eqIcon(c, c.dataset.ci === 'Équipé actuellement' ? cur : it));
}
// ---------- sac ----------
let BAGF = 'all';
function openBag(f) {
  if (f) BAGF = f; const list = S.bag.filter(x => BAGF === 'all' || x.slot === BAGF).sort((a, b) => b.r - a.r || itemPower(b) - itemPower(a));
  const worse = S.bag.filter(x => !x.set && S.eq[x.slot] && itemPower(x) <= itemPower(S.eq[x.slot]));
  sheet(`<h3>Sac · ${S.bag.length}/${BAG_MAX} <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="bagf"><button type="button" data-f="all" class="${BAGF === 'all' ? 'on' : ''}">Tout</button>${SLOTS.map(q => `<button type="button" data-f="${q.id}" class="${BAGF === q.id ? 'on' : ''}"><canvas data-bi="${q.id}" width="24" height="24"></canvas></button>`).join('')}</div>
  <div class="baggrid">${list.length ? list.map(it => `<button type="button" class="slot" data-id="${it.id}" style="color:${RAR[it.r].c};border-color:${RAR[it.r].c};background:radial-gradient(circle at 50% 38%,${RAR[it.r].c}88,${RAR[it.r].c}22 60%,#170b11)"><canvas data-ic2="${it.id}"></canvas><span class="lv">Nv ${it.L}</span>${it.set ? `<i class="setdot" style="background:${SETS[it.set].c}"></i>` : ''}${S.eq[it.slot] && itemPower(it) > itemPower(S.eq[it.slot]) ? '<i class="upA">▲</i>' : ''}</button>`).join('') : '<p class="empty">Aucun objet ici. Garde des objets en forgeant avec « Garder ».</p>'}</div>
  <button class="btn" id="sellW" type="button" style="width:100%;margin-top:12px" ${worse.length ? '' : 'disabled'}>Vendre les objets moins bons<small>${worse.length} objet${worse.length > 1 ? 's' : ''} sans set · +${fmt(worse.reduce((a, x) => a + x.v, 0))} or</small></button>`);
  $('mbox').querySelectorAll('[data-bi]').forEach(c => eqIcon(c, null, c.dataset.bi));
  $('mbox').querySelectorAll('[data-ic2]').forEach(c => eqIcon(c, S.bag.find(x => x.id === c.dataset.ic2)));
  $('mbox').querySelectorAll('[data-f]').forEach(b => b.onclick = () => openBag(b.dataset.f));
  $('mbox').querySelectorAll('[data-id]').forEach(b => b.onclick = () => showItem(S.bag.find(x => x.id === b.dataset.id), 'bag'));
  $('sellW').onclick = () => { const g = worse.reduce((a, x) => a + x.v, 0); S.bag = S.bag.filter(x => !worse.includes(x)); S.gold += g; save(); openBag(); toast(`+${fmt(g)} or`); };
}
''' + s[b:]

# ---------- bouton Sac dans la barre de forge (à la place du bouton Boss) ----------
rep('''<button class="dk red" id="bossBtn" type="button">''', '''<button class="dk" id="bagBtn" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M9 4.5a3 3 0 0 1 6 0V6h3.2a1 1 0 0 1 1 .9l1.3 13a1 1 0 0 1-1 1.1H4.5a1 1 0 0 1-1-1.1l1.3-13a1 1 0 0 1 1-.9H9zm1.8 0V6h2.4V4.5a1.2 1.2 0 0 0-2.4 0zM9 9.5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm6 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/></svg><small id="bagN">0/40</small></button>
    <button class="dk red" id="bossBtn" type="button">''')
rep("$('forgeBtn').onclick = forge;", "$('forgeBtn').onclick = forge; $('bagBtn').onclick = () => openBag('all');")
rep("$('flv').textContent = S.forge;", "$('flv').textContent = S.forge; $('bagN').textContent = `${S.bag.length}/${BAG_MAX}`;")

# ---------- sets visibles : pastille sur les emplacements + résumé ----------
rep("${it ? `<i class=\"gem\"></i><span class=\"lv\">Nv ${it.L}</span>` : ''}", "${it ? `<i class=\"gem\"></i><span class=\"lv\">Nv ${it.L}</span>${it.set ? `<i class=\"setdot\" style=\"background:${SETS[it.set].c}\"></i>` : ''}` : ''}")
rep('''<span style="color:#9ad0ff">${IC.shield}${fmt(st.def)}</span></div></div>''', '''<span style="color:#9ad0ff">${IC.shield}${fmt(st.def)}</span></div>${Object.entries(setCounts()).filter(([, n]) => n >= 1).map(([k, n]) => `<div class="setchip" style="--sc:${SETS[k].c}">${SETS[k].n} ${n}/6</div>`).join('')}</div>''')

# ---------- styles ----------
rep(".eveil{display:grid;gap:6px}", """.eveil{display:grid;gap:6px}
.setbox{margin-top:8px;padding:8px 10px;border-radius:10px;background:linear-gradient(90deg,color-mix(in srgb,var(--sc) 16%,transparent),transparent);border:1.5px solid color-mix(in srgb,var(--sc) 60%,transparent)}
.sethd{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px}
.sethd b{font:900 13px var(--t);color:var(--sc);letter-spacing:.04em}
.sethd span{font:800 11px var(--b);color:var(--dim)}
.setb{display:flex;gap:8px;align-items:center;font:700 12px/1.35 var(--b);color:#8a7078;padding:2px 0}
.setb em{font:400 12px var(--n);font-style:normal;width:22px;height:22px;flex:none;display:grid;place-items:center;border-radius:6px;background:#ffffff0c;border:1px solid #ffffff18}
.setb.on{color:#fff}
.setb.on em{background:var(--sc);color:#1a0b10;border-color:var(--sc)}
.setdot{position:absolute;left:3px;bottom:3px;width:9px;height:9px;border-radius:50%;border:1.5px solid #000;box-shadow:0 0 6px currentColor}
.setchip{margin-top:4px;font:800 10px var(--b);padding:2px 8px;border-radius:8px;color:var(--sc);border:1px solid color-mix(in srgb,var(--sc) 60%,transparent);background:#0006;white-space:nowrap}
.bagf{display:flex;gap:5px;margin-bottom:10px;overflow-x:auto}
.bagf button{flex:none;height:38px;min-width:38px;padding:0 8px;border-radius:10px;border:1.5px solid #5a3040;background:#14080d;color:var(--dim);font:400 14px var(--n);display:grid;place-items:center}
.bagf button.on{border-color:var(--gold);color:var(--gold2);background:#2a1620}
.bagf canvas{width:24px;height:24px;image-rendering:pixelated}
.baggrid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;max-height:46vh;overflow:auto;padding:2px}
.baggrid .slot{width:100%;height:auto;aspect-ratio:1}
.baggrid .slot canvas{width:34px;height:34px}
.baggrid .slot .lv{right:2px;top:2px;font-size:10px;padding:0 4px}
.upA{position:absolute;right:3px;bottom:2px;font:400 13px var(--n);font-style:normal;color:#5ae07a;text-shadow:0 1px 0 #000}
.empty{grid-column:1/-1;text-align:center;color:var(--dim);font:700 13px/1.5 var(--b);padding:20px 0}""")
# fiche héros : bonus de sets actifs
rep('''    <h3 style="margin-top:16px">Éveil</h3>''', '''    ${Object.keys(setCounts()).length ? `<h3 style="margin-top:16px">Sets</h3>${Object.entries(setCounts()).map(([k, n]) => `<div class="setbox" style="--sc:${SETS[k].c}"><div class="sethd"><b>${SETS[k].n}</b><span>${n} / 6</span></div>${SETS[k].b.map(([c, t]) => `<div class="setb ${n >= c ? 'on' : ''}"><em>${c}</em>${t}</div>`).join('')}</div>`).join('')}` : ''}
    <h3 style="margin-top:16px">Éveil</h3>''')
# admin : forger des objets de set
rep('<button class="btn" data-a="strip" type="button">Tout retirer</button></div>', '<button class="btn" data-a="strip" type="button">Tout retirer</button></div><div class="lbl2">Sets (6 pièces légendaires)</div><div class="adm">${SETK.map(k => `<button class="btn" type="button" data-set="${k}" style="border-color:${SETS[k].c};color:${SETS[k].c}">${SETS[k].n}</button>`).join(\'\')}<button class="btn" data-a="fillbag" type="button">Remplir le sac</button></div>')
rep("god: () => B.god = !B.god,", "fillbag: () => { while (S.bag.length < BAG_MAX) S.bag.push(makeItem()); }, god: () => B.god = !B.god,")
rep("  $('mbox').querySelectorAll('[data-sp]').forEach(", "  $('mbox').querySelectorAll('[data-set]').forEach(b => b.onclick = () => { const k = b.dataset.set; SLOTS.slice(0, 6).forEach(sl => { const it = makeItem(4, sl); it.set = k; S.eq[sl.id] = it; }); save(); B.gear = gear(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; showAdmin(); toast(`Set ${SETS[k].n} équipé`); });\n  $('mbox').querySelectorAll('[data-sp]').forEach(")

open(P, 'w').write(s)
print('ok')
