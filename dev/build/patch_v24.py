P = '/home/claude/grimloom/src.html'
s = open(P).read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
# auto-forge : s'arrête sur un meilleur objet, recycle le reste en fumée
rep("""  if (S.auto.equip && (!cur || itemPower(it) > itemPower(cur)) && !(cur && cur.set && !it.set)) { if (cur) recycle(cur); S.eq[it.slot] = it; S.st.equip++; equipFx(it); num(CX, YF - 120, `${SLOTS.find(q => q.id === it.slot).n} équipé`, RAR[it.r].c, 1); B.gear = gear(); const st = heroStats(); B.hero.hpMax = st.pv; }
  else recycle(it);""", """  if ((!cur || itemPower(it) > itemPower(cur)) && !(cur && cur.set && !it.set)) { S.auto.on = false; save(); ui(); sfxPlay('reward'); toast('Auto-forge : meilleur objet trouvé !'); showItem(it, true); return; }
  recycle(it);""")
rep("function recycle(it) { const sh = shardsOf(it); S.gold += it.v; S.shards += sh; return sh; }",
    r"""function recycle(it) { const sh = shardsOf(it); S.gold += it.v; S.shards += sh; smokeFx(it); return sh; }
function smokeFx(it) { // petite icône de l'objet qui part en fumée au-dessus de la forge
  const btn = $('forgeBtn'); if (!btn || !btn.offsetParent) return; const c = document.createElement('canvas'); c.className = 'smk'; eqIcon(c, it, it.slot);
  c.style.setProperty('--rc', RAR[it.r].c); c.style.left = (50 + rand(-14, 14)) + '%'; btn.appendChild(c);
  for (let i = 0; i < 5; i++) { const p = document.createElement('i'); p.className = 'puff'; p.style.left = `calc(${c.style.left} + ${rand(-16, 16)}px)`; p.style.animationDelay = (0.25 + i * 0.07) + 's'; p.style.setProperty('--dx', rand(-18, 18) + 'px'); btn.appendChild(p); setTimeout(() => p.remove(), 1500); }
  setTimeout(() => c.remove(), 1300);
}""")
rep("""  <div class="row"><button class="btn ${S.auto.equip ? 'gold' : ''}" type="button" id="aEq" style="flex:1">Équiper le meilleur<small>${S.auto.equip ? 'oui' : 'non'}</small></button>""", """  <div class="row">""")
rep("  $('aEq').onclick = () => { S.auto.equip = !S.auto.equip; save(); showForge(); };\n", "")
rep("Équipe ce qui est meilleur (sans retirer un set gravé) et recycle le reste en or et éclats.", "Forge en boucle, recycle tout ce qui est moins bon en or et éclats, et s'arrête dès qu'un objet meilleur que le tien sort pour te laisser choisir.")
s = s.replace("</style>", r"""
#forgeBtn .smk{position:absolute;bottom:150px;width:30px;height:30px;margin-left:-15px;image-rendering:pixelated;z-index:4;pointer-events:none;border-radius:8px;background:radial-gradient(circle,color-mix(in srgb,var(--rc) 55%,transparent),transparent 70%);animation:smk 1.25s ease-out forwards}
@keyframes smk{0%{transform:translateY(10px) scale(.6);opacity:0}15%{transform:translateY(0) scale(1.15);opacity:1}45%{transform:translateY(-14px) scale(1);opacity:1;filter:none}100%{transform:translateY(-46px) scale(.7) rotate(-12deg);opacity:0;filter:grayscale(1) brightness(.4) blur(2px)}}
#forgeBtn .puff{position:absolute;bottom:156px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:radial-gradient(circle,#b8a8b0cc,#6a5a6266 60%,transparent 72%);z-index:4;pointer-events:none;opacity:0;animation:puff 1s ease-out forwards}
@keyframes puff{0%{transform:translate(0,0) scale(.4);opacity:0}25%{opacity:.85}100%{transform:translate(var(--dx),-50px) scale(2.2);opacity:0}}
</style>""", 1)
open(P, 'w').write(s); print('ok')
