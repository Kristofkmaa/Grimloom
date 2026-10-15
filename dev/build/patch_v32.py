P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v32.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
b64 = open('/home/claude/grimloom/anvilart/anvil_sheet.b64').read()
rep('<canvas class="chest" width="64" height="64" aria-hidden="true"></canvas>', '<canvas class="chest" width="288" height="432" aria-hidden="true"></canvas>')
a = s.index("const CHEST_IMG = new Image();"); b = s.index("let zcT = []; function strikeFx() {")
s = s[:a] + r"""const CHEST_IMG = new Image(); CHEST_IMG.src = 'data:image/png;base64,""" + b64 + r"""';
let chestT = [], chestFr = 0;
function chestDraw() { const c = document.querySelector('#forgeBtn .chest'); if (!c || !CHEST_IMG.complete) return; const g = c.getContext('2d'); g.clearRect(0, 0, 288, 432); g.drawImage(CHEST_IMG, chestFr * 288, 0, 288, 432, 0, 0, 288, 432); }
CHEST_IMG.onload = chestDraw;
function chestOpen(r, cb) { // enclume : marteau levé → descente → impact (étincelles) → rebond
  const b = $('forgeBtn'); chestT.forEach(clearTimeout); const set = f => { chestFr = f; chestDraw(); };
  b.classList.remove('copen'); set(1);
  chestT = [setTimeout(() => { set(2); void b.offsetWidth; b.classList.add('copen'); B.shake = Math.max(B.shake, r >= 4 ? 5 : 2); }, 110), setTimeout(() => set(3), 280), setTimeout(() => cb && cb(), 430), setTimeout(() => { set(0); b.classList.remove('copen'); }, 700)];
}
""" + s[b:]
s = s.replace("</style>", r"""
#forgeBtn .chest{width:160px!important;height:240px!important;margin-left:-80px!important;bottom:22px!important;filter:drop-shadow(0 6px 6px #000a)!important;animation:none!important;image-rendering:auto!important}
#forgeBtn.cpop .chest{animation:none!important}
#forgeBtn .cglow{bottom:96px!important;width:150px!important;height:90px!important;margin-left:-75px!important;--rc:#ff8a2a}
#forgeBtn.copen .cglow{opacity:.8;animation:cglow .4s ease-out}
#forgeBtn.copen .chest{filter:drop-shadow(0 6px 6px #000a)!important}
#forgeBtn .smk{bottom:118px!important}#forgeBtn .fl{bottom:186px!important}#forgeBtn .puff{bottom:190px!important}
#forgeBtn.empty .chest{filter:grayscale(1) brightness(.6)!important}
</style>""", 1)
open(P, 'w').write(s); print('ok')
