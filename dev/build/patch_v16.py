import re
P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v16.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
b64 = open('/home/claude/grimloom/forgeart/sheet.b64').read()
# l'enclume laisse place au zombie qui porte le coffre
a = s.index('<svg class="anv"'); b = s.index('</svg>', a) + 6
s = s[:a] + '<span class="zc" aria-hidden="true"></span>' + s[b:]
rep("#forgeBtn.empty .glo{display:none}", """#forgeBtn.empty .glo{display:none}
#forgeBtn .zc{flex:none;width:64px;height:66px;position:relative;margin-left:-4px}
#forgeBtn .zc::after{content:'';position:absolute;left:-4px;bottom:-4px;width:64px;height:108px;background:url(data:image/png;base64,""" + b64 + """) 0 0/400% 100% no-repeat;filter:drop-shadow(0 3px 0 #6a2a0670);animation:zbob 1.4s ease-in-out infinite}
@keyframes zbob{50%{transform:translateY(-2px)}}
#forgeBtn .zc.f1::after{background-position:33.333% 0;animation:none}
#forgeBtn .zc.f2::after{background-position:66.667% 0;animation:none;transform:scale(1.04)}
#forgeBtn .zc.f3::after{background-position:100% 0;animation:zpop .35s ease-out}
@keyframes zpop{0%{transform:scale(1.1)}100%{transform:scale(1)}}
#forgeBtn.auto .zc::after{animation:zauto .9s steps(1) infinite}
@keyframes zauto{0%{background-position:0 0}25%{background-position:33.333% 0}40%{background-position:66.667% 0}55%,100%{background-position:100% 0}}
#forgeBtn.empty .zc::after{filter:grayscale(1) brightness(.7)}""")
rep("function strikeFx() { const b = $('forgeBtn'); b.classList.remove('strike'); void b.offsetWidth; b.classList.add('strike'); }",
    "let zcT = []; function strikeFx() { const z = $('forgeBtn').querySelector('.zc'); if (!z) return; zcT.forEach(clearTimeout); const set = c => { z.className = 'zc ' + c; }; set('f1'); zcT = [setTimeout(() => set('f2'), 120), setTimeout(() => set('f3'), 260), setTimeout(() => set(''), 1100)]; }")
open(P, 'w').write(s); print('ok')
