P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v35.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
d = '/home/claude/grimloom/dunart/'
B64 = {k: open(d + k + '.b64').read() for k in ['map', 'sang', 'os', 'braise', 'givre']}
a = s.index("const DPOS = {"); b = s.index("function drawDunMap() {"); e = s.index("\n}\n", b) + 3
s = s[:a] + r"""const DPOS = { sang: [26, 27], os: [74, 27], braise: [26, 65], givre: [77, 65] }; // centre des clairières (% de la carte)
const DUNIMG = { map: 'data:image/jpeg;base64,MAPB64', sang: 'data:image/png;base64,SANGB64', os: 'data:image/png;base64,OSB64', braise: 'data:image/png;base64,BRAISEB64', givre: 'data:image/png;base64,GIVREB64' };
let DSEL = 'sang';
function dunHTML() {
  const k = DSEL;
  return `<div class="kp"><div class="kban kg kbt"><div class="kbig"><b>${S.keys}</b><small>clé${S.keys > 1 ? 's' : ''}</small></div><div class="kbi"><b class="kname">Les Terres Maudites</b><small class="kdim">Choisis un donjon sur la carte. 3 vagues + un boss en 60 s pour gagner des Sceaux de set.</small><small class="kdim">3 clés par jour · +1 par boss · perdue seulement si tu gagnes</small></div></div>
  <div class="wmap"><img class="wbg" src="${DUNIMG.map}" alt="">
   ${SETK.map(dd => `<button type="button" class="wdun ${dd === k ? 'on' : ''}" data-dsel="${dd}" style="left:${DPOS[dd][0]}%;top:${DPOS[dd][1]}%;--sc:${SETS[dd].c}"><i class="wgl"></i><img src="${DUNIMG[dd]}" alt="${DUNS[dd].n}">${dd === k ? '<i class="darr"></i>' : ''}<span class="wpl"><b>${DUNS[dd].n}</b><small>Niv. ${S.dlv[dd]}</small></span></button>`).join('')}
  </div>
  <div class="kl kdun" style="--sc:${SETS[k].c}"><div class="kdt"><div><b>${DUNS[k].n}</b><small>${SETS[k].n} · tu as ${S.seals[k]} Sceaux</small></div><em class="kbadge">Niv. ${S.dlv[k]}</em></div><div class="kds">${SETS[k].b.map(([c, t]) => `<div><em>${c}</em><span>${t}</span></div>`).join('')}</div><div class="kdb"><span>Récompense<br><b>${dunReward(S.dlv[k])} Sceaux</b></span><button class="btn gold" type="button" data-dun="${k}" ${S.keys < 1 || B.dun ? 'disabled' : ''}>Entrer</button></div></div></div>`;
}
function drawDunMap() {}
""" + s[e:]
for k, v in B64.items(): s = s.replace(k.upper() + 'B64', v, 1)
s = s.replace("</style>", r"""
.dmap{display:none}
.wmap{position:relative;margin:0 -10px 10px;aspect-ratio:1030/1526;overflow:hidden;border-top:1px solid #4a3828;border-bottom:1px solid #4a3828}
.wbg{position:absolute;inset:0;width:100%;height:100%;display:block;image-rendering:auto}
.wdun{position:absolute;width:33%;padding:0;border:0;background:none;transform:translate(-50%,-72%);cursor:pointer;display:flex;flex-direction:column;align-items:center}
.wdun img{width:100%;display:block;filter:drop-shadow(0 6px 6px #000a) brightness(.82);transition:filter .2s,transform .2s}
.wdun.on img{filter:drop-shadow(0 0 10px var(--sc)) drop-shadow(0 6px 6px #000a) brightness(1.05);transform:scale(1.06)}
.wgl{position:absolute;left:50%;top:62%;width:120%;height:60%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(closest-side,var(--sc),transparent);opacity:.18;pointer-events:none}
.wdun.on .wgl{opacity:.45}
.wpl{margin-top:-10px;display:flex;flex-direction:column;align-items:center;padding:2px 8px;border:10px solid transparent;border-image:var(--kTab) 32 / 10px stretch;background:linear-gradient(#0d0709ee,#0d0709ee) center/calc(100% - 4px) calc(100% - 4px) no-repeat border-box;white-space:nowrap}
.wpl b{font:900 10.5px var(--t);color:var(--sc)}.wpl small{font:800 9px var(--b);color:#c8b090}
.wdun.on .wpl{border-image-source:var(--kTabg);background:linear-gradient(#3a1018f0,#3a1018f0) center/calc(100% - 4px) calc(100% - 4px) no-repeat border-box}
.wdun .darr{top:-14px}
</style>""", 1)
open(P, 'w').write(s); print('ok')
