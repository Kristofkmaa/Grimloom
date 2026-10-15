P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v22.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# --- état : plus de sac, des éclats ---
rep("if (!Array.isArray(S.bag)) S.bag = [];", "if (!Array.isArray(S.bag)) S.bag = []; if (S.shards === undefined) S.shards = 0;")
rep("const BAG_MAX = 40;", """const BAG_MAX = 40;
// ---------- recyclage : chaque objet non gardé donne de l'or et des éclats ----------
const SHARDV = [1, 2, 4, 8, 16, 32, 64];
const shardsOf = it => Math.round(SHARDV[it.r] * (1 + (it.L - 1) * 0.15));
function recycle(it) { const sh = shardsOf(it); S.gold += it.v; S.shards += sh; return sh; }
if (S.bag.length) { let g = 0, sh = 0; for (const it of S.bag) { g += it.v; sh += shardsOf(it); } S.gold += g; S.shards += sh; S.bag = []; setTimeout(() => toast(`Sac supprimé : objets recyclés (+${g} or, +${sh} éclats)`), 2500); }""")

# --- fenêtre d'objet ---
a = s.index("function toBag(it)"); b = s.index("// ---------- sac ----------")
s = s[:a] + r"""function equipItem(it) { sfxPlay('equip'); S.st.equip++; const cur = S.eq[it.slot]; if (cur) recycle(cur); S.eq[it.slot] = it; }
const SHARD_IC = '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 5 9l7 13 7-13zm0 3.2L16.4 9H7.6z"/></svg>';
function showItem(it, mode) { // mode : true = forgé, null = équipé
  const cur = S.eq[it.slot], nm = SLOTS.find(q => q.id === it.slot).n, isNew = mode === true;
  if (isNew) {
    const better = !cur || itemPower(it) > itemPower(cur), sh = shardsOf(it);
    sheet(`<h3>Nouvel objet <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Forgé', cur)}${cur ? cardHTML(cur, 'Équipé actuellement', null, 'cur') : ''}
    <div class="row" style="margin-top:14px"><button class="btn" id="sellB" type="button" style="flex:1">Recycler<small>+${fmt(it.v)} or · +${sh} éclats</small></button><button class="btn ${better ? 'gold' : ''}" id="eqB" type="button" style="flex:1.3">Équiper<small>${cur ? 'l\'ancien est recyclé' : 'emplacement vide'}</small></button></div>`);
    const rec = () => { sfxPlay('sell'); const n = recycle(it); save(); toast(`Recyclé : +${fmt(it.v)} or · +${n} éclats`); };
    $('mbox').querySelector('.x').onclick = () => { rec(); closeM(); };
    $('sellB').onclick = () => { rec(); closeM(); };
    $('eqB').onclick = () => { equipItem(it); save(); closeM(); equipFx(it); toast(`${nm} ${RAR[it.r].n.toLowerCase()} équipé`); };
  } else {
    const cs = upShards(it), ok = S.gold >= upCost(it) && S.shards >= cs;
    sheet(`<h3>${nm} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Équipé', null)}
    <button class="btn gold" id="upI" type="button" style="width:100%;margin-top:12px" ${ok ? '' : 'disabled'}>Améliorer au niveau ${it.L + 1}<small>${fmt(upCost(it))} or · ${fmt(cs)} éclats — tu as ${fmt(S.gold)} or · ${fmt(S.shards)} éclats</small></button>
    ${it.r >= 2 ? '<button class="btn red" id="egB" type="button" style="width:100%;margin-top:10px">Graver un set<small>avec les Sceaux des donjons</small></button>' : ''}`);
    $('upI').onclick = () => { if (upgradeItem(it)) { B.gear = gear(); showItem(it, null); } };
    if ($('egB')) $('egB').onclick = () => openEngrave(it, () => showItem(it, null));
  }
  $('mbox').querySelectorAll('[data-ci]').forEach(c => eqIcon(c, c.dataset.ci === 'Équipé actuellement' ? cur : it));
}
""" + s[b:]
# supprimer openBag
a = s.index("// ---------- sac ----------"); b = s.index("\n}\n", s.index("function openBag(f)")) + 3
s = s[:a] + s[b:]
# amélioration : or + éclats ; fusion retirée
rep("const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r]);", "const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r]);\nconst upShards = it => Math.round(3 * Math.pow(1.18, it.L - 1) * (1 + it.r * 0.3));")
rep("function upgradeItem(it) { const c = upCost(it); if (S.gold < c) return false; S.gold -= c;", "function upgradeItem(it) { const c = upCost(it), cs = upShards(it); if (S.gold < c || S.shards < cs) { toast('Pas assez ' + (S.gold < c ? 'd\\'or' : 'd\\'éclats : recycle des objets')); return false; } S.gold -= c; S.shards -= cs;")
a = s.index("function autoFuse() {"); b = s.index("\n}\n", a) + 3; s = s[:a] + s[b:]

# --- auto-forge : équipe le meilleur, recycle le reste ---
rep("if (S.auto.equip && (!cur || itemPower(it) > itemPower(cur))) { if (cur && (cur.set || cur.r >= S.auto.keep) && S.bag.length < BAG_MAX) S.bag.push(cur); else if (cur) S.gold += cur.v; S.eq[it.slot] = it;",
    "if (S.auto.equip && (!cur || itemPower(it) > itemPower(cur)) && !(cur && cur.set && !it.set)) { if (cur) recycle(cur); S.eq[it.slot] = it;")
rep("  else if (it.r >= S.auto.keep && S.bag.length < BAG_MAX) { S.bag.push(it); num(CX, YF - 120, `${RAR[it.r].n} gardé`, RAR[it.r].c, 1); }\n  else S.gold += it.v;",
    "  else recycle(it);")
a = s.index("  <div class=\"lbl2\">Garder dans le sac à partir de</div>"); b = s.index("</div>", s.index('<div class="seg">', a)) + 6
s = s[:a] + s[b:]
rep("  $('mbox').querySelectorAll('[data-keep]').forEach(b => b.onclick = () => { S.auto.keep = +b.dataset.keep; save(); showForge(); });\n", "")
rep("Équipe ce qui est meilleur, garde la rareté choisie, vend le reste.", "Équipe ce qui est meilleur (sans retirer un set gravé) et recycle le reste en or et éclats.")

# --- bouton du sac → réglages de l'auto-forge ---
a = s.index('<button class="dk" id="bagBtn" type="button">'); b = s.index('</button>', a) + 9
s = s[:a] + '<button class="dk" id="bagBtn" type="button" aria-label="Auto-forge"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3.3h-4l-.4 2.6a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1a7.4 7.4 0 0 0 1.7 1l.4 2.6h4l.4-2.6a7.4 7.4 0 0 0 1.7-1l2.5 1 2-3.5zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z" transform="translate(-1 0)"/></svg><small id="bagN">Auto</small></button>' + s[b:]
rep("$('bagN').textContent = `${S.bag.length}/${BAG_MAX}`;", "$('bagN').textContent = S.auto.on ? 'Auto ON' : 'Auto'; $('bagBtn').classList.toggle('on', !!S.auto.on);")
rep("$('bagBtn').onclick = () => openBag('all');", "$('bagBtn').onclick = showForge;")
s = s.replace("</style>", "#bagBtn.on{border-color:#5ae07a;box-shadow:0 0 12px -2px #5ae07a}#bagBtn.on small{color:#7aff9a}\n.shardp{display:inline-flex;align-items:center;gap:4px;color:#b8a0ff}\n</style>", 1)

# --- admin ---
rep("rset6: () => {", "shards: () => { S.shards += 1000; },\n    rset6: () => {")
s = s.replace('<button class="btn" data-a="fillbag" type="button">Remplir le sac</button>', '<button class="btn gold" data-a="shards" type="button">+1000 éclats</button>', 1)
s = s.replace('<button class="btn gold" data-a="rset6" type="button">6 pièces de set au sac</button>', '', 1)
open(P, 'w').write(s); print('ok')
