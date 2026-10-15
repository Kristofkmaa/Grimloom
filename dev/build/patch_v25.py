P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v25.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
# l'auto-forge reprend après le choix du joueur
rep("{ S.auto.on = false; save(); ui(); sfxPlay('reward'); toast('Auto-forge : meilleur objet trouvé !'); showItem(it, true); return; }",
    "{ S.auto.on = false; B.autoResume = true; save(); ui(); sfxPlay('reward'); toast('Meilleur objet trouvé !'); showItem(it, true); return; }")
rep("    $('mbox').querySelector('.x').onclick = () => { rec(); closeM(); };\n    $('sellB').onclick = () => { rec(); closeM(); };\n    $('eqB').onclick = () => { equipItem(it); save(); closeM(); equipFx(it); toast(`${nm} ${RAR[it.r].n.toLowerCase()} équipé`); };",
    "    const resume = () => { if (B.autoResume) { B.autoResume = false; if (S.ham > 0) { S.auto.on = true; autoT = 0.6; ui(); } } };\n    $('mbox').querySelector('.x').onclick = () => { rec(); closeM(); resume(); };\n    $('sellB').onclick = () => { rec(); closeM(); resume(); };\n    $('eqB').onclick = () => { equipItem(it); save(); closeM(); equipFx(it); toast(`${nm} ${RAR[it.r].n.toLowerCase()} équipé`); resume(); };")
rep("  $('aOn').onclick = () => { S.auto.on = !S.auto.on;", "  $('aOn').onclick = () => { S.auto.on = !S.auto.on; B.autoResume = false;")
# fumée : l'icône sort du coffre (0,5 s bien visible) puis part en fumée
rep("p.style.animationDelay = (0.25 + i * 0.07) + 's';", "p.style.animationDelay = (0.55 + i * 0.06) + 's';")
rep("setTimeout(() => p.remove(), 1500); }\n  setTimeout(() => c.remove(), 1300);", "setTimeout(() => p.remove(), 1800); }\n  setTimeout(() => c.remove(), 1300);")
rep("#forgeBtn .smk{position:absolute;bottom:236px;", "#forgeBtn .smk{position:absolute;bottom:150px;")
rep("@keyframes smk{0%{transform:translateY(10px) scale(.6);opacity:0}15%{transform:translateY(0) scale(1.15);opacity:1}45%{transform:translateY(-14px) scale(1);opacity:1;filter:none}100%{transform:translateY(-46px) scale(.7) rotate(-12deg);opacity:0;filter:grayscale(1) brightness(.4) blur(2px)}}",
    "@keyframes smk{0%{transform:translateY(0) scale(.4);opacity:0}12%{opacity:1}38%{transform:translateY(-86px) scale(1.25);opacity:1;filter:none}45%{transform:translateY(-90px) scale(1.15);opacity:1;filter:none}100%{transform:translateY(-120px) scale(.6) rotate(-14deg);opacity:0;filter:grayscale(1) brightness(.3) blur(3px)}}")
rep("#forgeBtn .puff{position:absolute;bottom:242px;", "#forgeBtn .puff{position:absolute;bottom:246px;")
open(P, 'w').write(s); print('ok')
