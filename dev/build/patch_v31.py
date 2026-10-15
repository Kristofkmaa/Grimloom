P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v31.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
b64 = open('/home/claude/grimloom/chests_sheet.b64').read()
# coffre à la place du zombie
rep('<button id="forgeBtn" type="button"><span class="zc" aria-hidden="true"></span>', '<button id="forgeBtn" type="button"><i class="cglow"></i><canvas class="chest" width="64" height="64" aria-hidden="true"></canvas>')
rep("let zcT = []; function strikeFx() {", r"""// ---------- coffre de forge : il prend la couleur de la rareté puis s'ouvre ----------
const CHEST_IMG = new Image(); CHEST_IMG.src = 'data:image/png;base64,""" + b64 + r"""';
const CHEST_ROW = [1, 2, 3, 4, 5, 6, 7]; // rareté → ligne (0 = coffre mystère)
let chestT = [], chestRow = 0, chestFr = 0;
function chestDraw() { const c = document.querySelector('#forgeBtn .chest'); if (!c || !CHEST_IMG.complete) return; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 64, 64); g.drawImage(CHEST_IMG, chestFr * 64, chestRow * 64, 64, 64, 0, 0, 64, 64); }
CHEST_IMG.onload = chestDraw;
function chestOpen(r, cb) {
  const b = $('forgeBtn'); chestT.forEach(clearTimeout); chestRow = CHEST_ROW[r] || 1; chestFr = 0; chestDraw();
  b.style.setProperty('--rc', RAR[r].c); b.classList.remove('copen', 'cpop'); void b.offsetWidth; b.classList.add('cpop'); if (r >= 4) B.shake = Math.max(B.shake, 3 + r);
  chestT = [1, 2, 3, 4, 5].map(f => setTimeout(() => { chestFr = f; chestDraw(); if (f === 3) b.classList.add('copen'); }, 180 + f * 65));
  chestT.push(setTimeout(() => cb && cb(), 560));
  chestT.push(setTimeout(() => { b.classList.remove('copen', 'cpop'); chestRow = 0; chestFr = 0; chestDraw(); }, 1250));
}
let zcT = []; function strikeFx() {""")
rep("""function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }
  if (forging) return; forging = true; strikeFx(); setTimeout(() => { forging = false; forgeNow(); }, 480);
}
function forgeNow() {
  hamTick(); if (S.ham <= 0) return; if (tr('a_twin') && Math.random() < 0.1) { S.ham++; toast('Marteau béni : forge gratuite !'); }
  S.ham--; S.forged++; const it = makeItem(); S.st.bestR = Math.max(S.st.bestR, it.r); sfxPlay('forge'); save();
  showItem(it, true);
}""", """function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }
  if (forging) return; forging = true;
  if (tr('a_twin') && Math.random() < 0.1) { S.ham++; toast('Marteau béni : forge gratuite !'); }
  S.ham--; S.forged++; const it = makeItem(); S.st.bestR = Math.max(S.st.bestR, it.r); save(); uiTop();
  chestOpen(it.r, () => { forging = false; showItem(it, true); });
}""")
rep("""  S.ham--; if (tr('a_twin') && Math.random() < 0.1) S.ham++; S.forged++; autoBusy = true; strikeFx(); uiTop();
  setTimeout(() => {
    autoBusy = false; const it = makeItem(), cur = S.eq[it.slot]; S.st.bestR = Math.max(S.st.bestR, it.r);""", """  S.ham--; if (tr('a_twin') && Math.random() < 0.1) S.ham++; S.forged++; autoBusy = true; uiTop();
  const it = makeItem(), cur = S.eq[it.slot]; S.st.bestR = Math.max(S.st.bestR, it.r);
  chestOpen(it.r, () => {
    autoBusy = false;""")
rep("""    save(); if (tab === 'forge') ui(); else uiTop();
  }, 480);
}""", """    save(); if (tab === 'forge') ui(); else uiTop();
  });
}""")
s = s.replace("</style>", r"""
#forgeBtn .zc{display:none!important}
#forgeBtn .chest{position:absolute;left:50%;bottom:6px;width:192px;height:192px;margin-left:-96px;image-rendering:pixelated;z-index:1;cursor:pointer;filter:drop-shadow(0 6px 6px #000c);animation:cidle 2.4s ease-in-out infinite;transform-origin:50% 85%}
@keyframes cidle{50%{transform:translateY(-3px)}}
#forgeBtn .cglow{position:absolute;left:50%;bottom:30px;width:220px;height:170px;margin-left:-110px;border-radius:50%;background:radial-gradient(closest-side,var(--rc,#ff6a2a),transparent);opacity:0;z-index:0;pointer-events:none;transition:opacity .25s}
#forgeBtn.cpop .chest{animation:cpop .3s ease-out}
@keyframes cpop{0%{transform:scale(.7) translateY(10px);filter:brightness(3) drop-shadow(0 0 20px var(--rc))}60%{transform:scale(1.12)}100%{transform:scale(1);filter:drop-shadow(0 6px 6px #000c)}}
#forgeBtn.cpop .cglow{opacity:.35}
#forgeBtn.copen .cglow{opacity:.75;animation:cglow .6s ease-out}
@keyframes cglow{0%{transform:scale(.6)}100%{transform:scale(1.1)}}
#forgeBtn.copen .chest{filter:drop-shadow(0 0 14px var(--rc)) drop-shadow(0 6px 6px #000c)}
#forgeBtn.empty .chest{filter:grayscale(1) brightness(.6)}
#forgeBtn .smk{bottom:104px!important}
#forgeBtn .fl{bottom:196px!important}
#forgeBtn .puff{bottom:200px!important}
</style>""", 1)
open(P, 'w').write(s); print('ok')
