P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v15.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
ANVIL = '''<svg class="anv" viewBox="0 0 120 90" aria-hidden="true"><defs><linearGradient id="anI" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a94a6"/><stop offset=".25" stop-color="#4a5262"/><stop offset="1" stop-color="#1c2028"/></linearGradient><linearGradient id="anH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a7f8c"/><stop offset=".5" stop-color="#c8ced8"/><stop offset="1" stop-color="#4a505c"/></linearGradient><radialGradient id="anG"><stop offset="0" stop-color="#fff2a0"/><stop offset=".45" stop-color="#ff9a20"/><stop offset="1" stop-color="#ff4a10" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="58" cy="84" rx="40" ry="5" fill="#0006"/>
<path d="M38 84h42l-6-12H44z" fill="#2a1a10"/><path d="M44 72h30l-4-10H48z" fill="url(#anI)"/>
<path d="M50 62h18l2-8H48z" fill="#262a34"/>
<path d="M28 44h66v6c0 3-2 5-5 5H32c-2 0-4-2-4-4z" fill="url(#anI)"/><path d="M28 44C18 44 8 46 3 50c6 1 15 2 25 5z" fill="url(#anI)"/>
<path d="M4 50c8-4 16-5 24-5h66" stroke="#d8dee8" stroke-width="1.6" fill="none" opacity=".8"/>
<circle class="glo" cx="62" cy="42" r="14" fill="url(#anG)"/><rect x="52" y="39" width="22" height="5" rx="2" fill="#ffb030" stroke="#ff6a10"/>
<g class="spk" fill="#ffe27a"><circle cx="62" cy="38" r="1.6"/><circle cx="50" cy="32" r="1.2"/><circle cx="74" cy="30" r="1.4"/><circle cx="44" cy="40" r="1"/><circle cx="80" cy="38" r="1.1"/><circle cx="58" cy="26" r="1"/></g>
<g class="ham"><rect x="94" y="22" width="5" height="58" rx="2" fill="#8a5a2a" stroke="#4a2a10"/><rect x="94" y="62" width="5" height="10" fill="#3a2010"/><rect x="83" y="8" width="27" height="15" rx="3" fill="url(#anH)" stroke="#2a2e36"/><rect x="94" y="8" width="5" height="15" fill="#d8a03a"/></g></svg>'''
# icône du bouton remplacée par l'enclume animée
rep('<button id="forgeBtn" type="button"><svg class="i" viewBox="0 0 24 24"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z" fill="#6a2a06"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z" fill="#3a1404"/></svg>',
    '<button id="forgeBtn" type="button">' + ANVIL)
rep("#forgeBtn.empty::before{display:none}", """#forgeBtn.empty::before{display:none}
#forgeBtn{overflow:visible}
#forgeBtn svg.anv{width:84px;height:63px;margin:-14px 0 -6px -6px;font-size:inherit;filter:drop-shadow(0 3px 0 #6a2a0688)}
#forgeBtn .ham{transform-box:view-box;transform-origin:96px 80px;transform:rotate(8deg)}
#forgeBtn .spk{opacity:0;transform-box:view-box;transform-origin:62px 40px}
#forgeBtn .glo{opacity:.55;animation:anglo 1.6s ease-in-out infinite}
@keyframes anglo{50%{opacity:.9}}
#forgeBtn.strike .ham{animation:anhit .38s ease-in}
#forgeBtn.strike .spk{animation:anspk .38s ease-out}
#forgeBtn.strike .glo{animation:anflash .38s}
#forgeBtn.auto .ham{animation:anhit .45s ease-in infinite}
#forgeBtn.auto .spk{animation:anspk .45s ease-out infinite}
@keyframes anhit{0%{transform:rotate(8deg)}40%{transform:rotate(26deg)}72%{transform:rotate(-30deg)}100%{transform:rotate(8deg)}}
@keyframes anspk{0%,68%{opacity:0;transform:scale(.4)}74%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(1.8)}}
@keyframes anflash{70%{opacity:.6}76%{opacity:1;transform:scale(1.3)}}
#forgeBtn.empty .glo{display:none}""")
# l'animation joue avant l'ouverture de l'objet forgé
rep("""function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }""",
"""let forging = false;
function strikeFx() { const b = $('forgeBtn'); b.classList.remove('strike'); void b.offsetWidth; b.classList.add('strike'); }
function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }
  if (forging) return; forging = true; strikeFx(); setTimeout(() => { forging = false; forgeNow(); }, 300);
}
function forgeNow() {
  hamTick(); if (S.ham <= 0) return;""")
rep("$('forgeBtn').classList.toggle('empty', S.ham <= 0);", "$('forgeBtn').classList.toggle('empty', S.ham <= 0); $('forgeBtn').classList.toggle('auto', !!S.auto.on && S.ham > 0);")
open(P, 'w').write(s); print('ok')
