P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v36.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# ---------- données ----------
rep("function keyTick() {", r"""// ================= donjons de ressources (tickets qui se rechargent) =================
const RD = {
  or: { n: 'Mine aux trésors', bi: 3, c: '#ffc23a', ic: 'coin', what: 'or', d: 'Des démons gorgés d\'or' },
  xp: { n: 'Puits des âmes', bi: 6, c: '#7aff9a', ic: 'star', what: 'XP', d: 'Les âmes errantes renforcent ton héros' },
  eclats: { n: 'Caveau de cristal', bi: 5, c: '#b48aff', ic: 'gem', what: 'éclats', d: 'Des démons de givre chargés d\'éclats' },
  pages: { n: 'Scriptorium maudit', bi: 1, c: '#ff9a6a', ic: 'book', what: 'pages', d: 'Des grimoires interdits à piller' },
};
const RDK = Object.keys(RD), RT_MAX = 3, RT_MS = 2 * 3600 * 1000;
S.rt = S.rt || {}; S.rlv = S.rlv || {}; RDK.forEach(k => { S.rt[k] = S.rt[k] || { n: RT_MAX, t: Date.now() }; S.rlv[k] = S.rlv[k] || 1; });
function rtTick(k) { const r = S.rt[k], now = Date.now(); if (r.n >= RT_MAX) { r.t = now; return r; } const g = Math.floor((now - r.t) / RT_MS); if (g > 0) { r.n = Math.min(RT_MAX, r.n + g); r.t = r.n >= RT_MAX ? now : r.t + g * RT_MS; } return r; }
const rtLeft = k => { const r = rtTick(k); return r.n >= RT_MAX ? 0 : RT_MS - (Date.now() - r.t); };
const hms = ms => { const m = Math.ceil(ms / 60000), h = Math.floor(m / 60); return h ? `${h} h ${String(m % 60).padStart(2, '0')}` : `${m} min`; };
function rdReward(k, lv) { const si = Math.max(1, S.best), f = 1 + 0.35 * (lv - 1);
  return k === 'or' ? { gold: Math.round(120 * Math.pow(1.11, si) * f) } : k === 'xp' ? { xp: Math.round(xpNeed(S.lvl) * 0.5 * (1 + 0.2 * (lv - 1))) } : k === 'eclats' ? { shards: Math.round((20 + si * 1.5) * f) } : { pages: 25 + 10 * (lv - 1) }; }
const rdTxt = r => r.gold ? `${fmt(r.gold)} or` : r.xp ? `${fmt(r.xp)} XP` : r.shards ? `${fmt(r.shards)} éclats` : `${fmt(r.pages)} pages`;
function rdGive(r) { if (r.gold) S.gold += r.gold; if (r.xp) gainXP(r.xp / (1 + 0.08 * tr('a_xp'))); if (r.shards) S.shards += r.shards; if (r.pages) S.pages += r.pages; }
const dunName = k => (DUNS[k] || RD[k]).n;
function startRDun(k) { if (B.dun) return; if (rtTick(k).n < 1) { toast(`Plus de tickets : +1 dans ${hms(rtLeft(k))}`); return; }
  tab = 'forge'; document.querySelectorAll('#nav button').forEach(x => x.classList.toggle('on', x.dataset.t === 'forge'));
  B.dun = { k, lv: S.rlv[k], w: 0, t: 60, res: true }; B.walk = null; B.pend = 0; B.pendFn = null; B.scene = 'arena'; B.scroll = 0; B.fade = 1; closeM(); startWave(); }
function sweepRDun(k) { const lv = S.rlv[k] - 1; if (lv < 1) return; if (rtTick(k).n < 1) { toast(`Plus de tickets : +1 dans ${hms(rtLeft(k))}`); return; }
  const r = S.rt[k]; if (r.n >= RT_MAX) r.t = Date.now(); r.n--; const rw = rdReward(k, lv); rdGive(rw); S.st.dun++; save(); sfxPlay('reward'); toast(`Balayage niveau ${lv} : +${rdTxt(rw)}`); ui(); }
function keyTick() {""")

# ---------- combat de donjon générique ----------
rep("const D = B.dun, n = 4 + (D.lv - 1) * 5; B.bi = DUNS[D.k].bi;", "const D = B.dun, n = D.res ? Math.max(4 + (D.lv - 1) * 5, Math.round(stageIndex() * 0.75) + (D.lv - 1) * 3) : 4 + (D.lv - 1) * 5; B.bi = (DUNS[D.k] || RD[D.k]).bi;")
rep("B.banner = { a: DUNS[D.k].n, b: `Niveau ${D.lv} · 3 vagues + boss en 60 s`, t: 2 }; }", "B.banner = { a: dunName(D.k), b: `Niveau ${D.lv} · 3 vagues + boss en 60 s`, t: 2 }; }")
rep("  if (win) { const r = dunReward(D.lv);", "  if (win && D.res) { const rw = rdReward(D.k, D.lv), r = S.rt[D.k]; if (r.n >= RT_MAX) r.t = Date.now(); r.n--; rdGive(rw); S.rlv[D.k]++; S.st.dun++; B.banner = { a: 'Victoire !', b: `+${rdTxt(rw)} · niveau ${D.lv + 1} débloqué`, t: 2.4 }; }\n  else if (win) { const r = dunReward(D.lv);")
rep("else B.banner = { a: 'Échec', b: `${why} · la clé n'est pas consommée`, t: 2.4 };", "else B.banner = { a: 'Échec', b: `${why} · ${D.res ? 'le ticket' : 'la clé'} n'est pas consommé${D.res ? '' : 'e'}`, t: 2.4 };")
rep("$('biomeN').textContent = `${DUNS[B.dun.k].n} · niveau ${B.dun.lv}`;", "$('biomeN').textContent = `${dunName(B.dun.k)} · niveau ${B.dun.lv}`;")

# ---------- page : onglets Sets / Ressources ----------
rep("let DSEL = 'sang';\nfunction dunHTML() {\n  const k = DSEL;\n  return `<div class=\"kp\">",
    "let DSEL = 'sang', DTAB = 'res';\nfunction rdHTML() {\n  return `<div class=\"kp\">${ktabs(DTAB, [['res', 'Ressources'], ['sets', 'Sets']], 'data-dtab')}<p class=\"knote\" style=\"margin:0 0 10px\">Chaque donjon a ses propres tickets : <b style=\"color:#ffd890\">${RT_MAX} maximum, +1 toutes les 2 h</b>. Le ticket n'est utilisé qu'en cas de victoire. Une fois un niveau battu, tu peux le <b style=\"color:#ffd890\">balayer</b> pour gagner sa récompense tout de suite.</p>\n  ${RDK.map(k => { const R = RD[k], t = rtTick(k), lv = S.rlv[k], rw = rdReward(k, lv); return `<div class=\"kl rdun\" style=\"--sc:${R.c}\"><div class=\"rdt\"><i class=\"rdic\">${IC[R.ic]}</i><div class=\"rdi\"><b>${R.n}</b><small>${R.d}</small></div><em class=\"kbadge\">Niv. ${lv}</em></div><div class=\"rdm\"><div><small>Récompense</small><b>+${rdTxt(rw)}</b></div><div class=\"rdtk\"><small>Tickets</small><b>${[...Array(RT_MAX)].map((_, i) => `<i class=\"${i < t.n ? 'on' : ''}\"></i>`).join('')}</b><small class=\"rtcd\" data-rt=\"${k}\">${t.n >= RT_MAX ? 'plein' : '+1 dans ' + hms(rtLeft(k))}</small></div></div><div class=\"row rdb\"><button class=\"btn\" type=\"button\" data-rsw=\"${k}\" ${lv < 2 || t.n < 1 || B.dun ? 'disabled' : ''}>Balayer<small>${lv < 2 ? 'bats le niveau 1' : 'niv. ' + (lv - 1) + ' · +' + rdTxt(rdReward(k, lv - 1))}</small></button><button class=\"btn gold\" type=\"button\" data-rdun=\"${k}\" ${t.n < 1 || B.dun ? 'disabled' : ''}>Combattre<small>niveau ${lv}</small></button></div></div>`; }).join('')}</div>`;\n}\nfunction dunHTML() {\n  if (DTAB === 'res') return rdHTML();\n  const k = DSEL;\n  return `<div class=\"kp\">${ktabs(DTAB, [['res', 'Ressources'], ['sets', 'Sets']], 'data-dtab')}")
rep("    document.querySelectorAll('[data-dsel]').forEach(b => b.onclick = () => { DSEL = b.dataset.dsel; const y = $('panel').scrollTop; ui(); $('panel').scrollTop = y; });",
    "    document.querySelectorAll('[data-dsel]').forEach(b => b.onclick = () => { DSEL = b.dataset.dsel; const y = $('panel').scrollTop; ui(); $('panel').scrollTop = y; });\n    document.querySelectorAll('[data-dtab]').forEach(b => b.onclick = () => { DTAB = b.dataset.dtab; ui(); });\n    document.querySelectorAll('[data-rdun]').forEach(b => b.onclick = () => startRDun(b.dataset.rdun));\n    document.querySelectorAll('[data-rsw]').forEach(b => b.onclick = () => sweepRDun(b.dataset.rsw));")
# compte à rebours vivant
rep("  $('tpDot').hidden = S.tp < 1;", "  document.querySelectorAll('[data-rt]').forEach(el => { const k = el.dataset.rt, n = rtTick(k).n; el.textContent = n >= RT_MAX ? 'plein' : '+1 dans ' + hms(rtLeft(k)); });\n  $('tpDot').hidden = S.tp < 1;")
# icône pièce
rep("const IC = {", "const IC = {\n  coin: '<svg class=\"i\" viewBox=\"0 0 24 24\" fill=\"currentColor\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><circle cx=\"12\" cy=\"12\" r=\"5.5\" fill=\"#0006\"/></svg>',")
# admin
rep("shards: () => { S.shards += 1000; },", "shards: () => { S.shards += 1000; },\n    tickets: () => { RDK.forEach(k => { S.rt[k] = { n: RT_MAX, t: Date.now() }; }); },")
s = s.replace('<button class="btn gold" data-a="shards" type="button">+1000 éclats</button>', '<button class="btn gold" data-a="shards" type="button">+1000 éclats</button><button class="btn gold" data-a="tickets" type="button">Tickets pleins</button>', 1)
# aide
rep("  ['#ff4a5a', IC.shield, 'Sceaux',", "  ['#7aff9a', IC.coin, 'Tickets de donjon', 'Chaque donjon de ressources en a 3 maximum, +1 toutes les 2 h.', 'Entrer dans la Mine aux trésors, le Puits des âmes, le Caveau de cristal ou le Scriptorium (perdu seulement si tu gagnes), ou balayer un niveau déjà battu.'],\n  ['#ff4a5a', IC.shield, 'Sceaux',")

s = s.replace("</style>", r"""
.rdun{margin-bottom:10px}
.rdt{display:flex;align-items:center;gap:10px}
.rdic{flex:none;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;font-size:24px;font-style:normal;color:var(--sc);background:radial-gradient(circle at 50% 35%,color-mix(in srgb,var(--sc) 30%,#1a0c10),#0c0608);border:2px solid var(--sc);box-shadow:0 0 14px -4px var(--sc)}
.rdi{flex:1;min-width:0}.rdi b{display:block;font:900 15px var(--t);color:var(--sc)}.rdi small{font:700 11.5px var(--b);color:#a08a78}
.rdm{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;margin:10px 0;padding:8px 10px;border-radius:10px;background:#ffffff06;border:1px solid #ffffff10}
.rdm small{display:block;font:800 9.5px var(--b);color:#a08a78;letter-spacing:.08em;text-transform:uppercase}.rdm b{font:900 17px var(--t);color:#fff}
.rdtk{text-align:right}.rdtk b{display:flex;gap:4px;justify-content:flex-end;margin:3px 0}.rdtk i{width:14px;height:18px;border-radius:3px;border:1.5px solid #6a5232;background:#1a100c}.rdtk i.on{background:linear-gradient(#9affb0,#2aa04a);border-color:#bfffcf;box-shadow:0 0 8px #5ae07a88}
.rdtk .rtcd{text-transform:none;letter-spacing:0;font-size:10.5px;color:#c8b090}
.rdb{gap:8px}.rdb .btn{flex:1;min-height:46px}
</style>""", 1)
open(P, 'w').write(s); print('ok')
