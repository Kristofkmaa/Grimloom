P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v26.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
# plus d'animation CSS en boucle : chaque forge auto joue la vraie animation
rep("$('forgeBtn').classList.toggle('auto', !!S.auto.on && S.ham > 0);", "")
rep("setTimeout(() => set(''), 1100)]; }", "setTimeout(() => set(''), 1200)]; }")
# cycle auto calé sur l'animation : coup (0 s) → coffre ouvert → objet qui sort (0,48 s) → fumée → coup suivant (1,6 s)
a = s.index("function autoForgeTick(dt) {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r"""let autoBusy = false;
function autoForgeTick(dt) {
  if (!S.auto.on || S.ham <= 0 || !$('modal').hidden || autoBusy) return; autoT -= dt; if (autoT > 0) return; autoT = 1.6;
  S.ham--; if (tr('a_twin') && Math.random() < 0.1) S.ham++; S.forged++; autoBusy = true; strikeFx(); uiTop();
  setTimeout(() => {
    autoBusy = false; const it = makeItem(), cur = S.eq[it.slot]; S.st.bestR = Math.max(S.st.bestR, it.r);
    if ((!cur || itemPower(it) > itemPower(cur)) && !(cur && cur.set && !it.set)) { S.auto.on = false; B.autoResume = true; save(); ui(); sfxPlay('reward'); toast('Meilleur objet trouvé !'); showItem(it, true); return; }
    recycle(it);
    if (S.ham <= 0) { S.auto.on = false; toast('Auto-forge en pause : plus de marteaux'); }
    save(); if (tab === 'forge') ui(); else uiTop();
  }, 480);
}
""" + s[b:]
# fumée plus grosse et plus lente : sort 0,15 s, reste 0,5 s, se dissout 0,4 s
rep("#forgeBtn .smk{position:absolute;bottom:150px;width:30px;height:30px;margin-left:-15px;", "#forgeBtn .smk{position:absolute;bottom:150px;width:52px;height:52px;margin-left:-26px;")
rep("animation:smk 1.5s ease-out forwards", "animation:smk 1.1s ease-out forwards")
rep("@keyframes smk{0%{transform:translateY(0) scale(.4);opacity:0}8%{opacity:1}20%{transform:translateY(-86px) scale(1.3);opacity:1;filter:none}53%{transform:translateY(-94px) scale(1.15);opacity:1;filter:none}100%{transform:translateY(-124px) scale(.6) rotate(-14deg);opacity:0;filter:grayscale(1) brightness(.3) blur(3px)}}",
    "@keyframes smk{0%{transform:translateY(0) scale(.3);opacity:0}6%{opacity:1}14%{transform:translateY(-80px) scale(1.25);opacity:1;filter:none}20%{transform:translateY(-86px) scale(1);filter:none}60%{transform:translateY(-92px) scale(1);opacity:1;filter:none}100%{transform:translateY(-118px) scale(.55) rotate(-14deg);opacity:0;filter:grayscale(1) brightness(.3) blur(4px)}}")
rep("c.style.left = (50 + rand(-14, 14)) + '%';", "c.style.left = '50%';")
rep("p.style.animationDelay = (0.8 + i * 0.06) + 's';", "p.style.animationDelay = (0.62 + i * 0.05) + 's';")
rep("for (let i = 0; i < 5; i++) { const p = document.createElement('i');", "for (let i = 0; i < 7; i++) { const p = document.createElement('i');")
rep("p.style.left = `calc(${c.style.left} + ${rand(-16, 16)}px)`;", "p.style.left = `calc(50% + ${rand(-22, 22)}px)`;")
rep("setTimeout(() => p.remove(), 2000); }\n  setTimeout(() => c.remove(), 1550);", "setTimeout(() => p.remove(), 1800); }\n  setTimeout(() => c.remove(), 1150);")
rep("#forgeBtn .puff{position:absolute;bottom:246px;width:16px;height:16px;margin-left:-8px;", "#forgeBtn .puff{position:absolute;bottom:236px;width:24px;height:24px;margin-left:-12px;")
open(P, 'w').write(s); print('ok')
