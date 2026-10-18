# p32 : passe de combat vertical (fond ASSETS.passV 941×1672, dev/assets_pass.js) : les 100 paliers défilent de haut en bas
#  le long du rail, en zigzag ; s'ouvre sur le premier palier non récupéré
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p32 passe vertical' not in s
a = s.index('function passSheet() {'); b = s.index('  SKC = () => { PSPG = -1; };\n}\n', a) + len('  SKC = () => { PSPG = -1; };\n}\n')
s = s[:a] + r"""let PSCR = null; // p32 passe vertical
function passSheet() { if (!featOK('passe')) { toast(featMsg('passe')); return; }
  if (ASSETS.passV) UIA.passv = ASSETS.passV;
  const P = passTier(), left = SEASON_MS - (Date.now() % SEASON_MS), W = 941, H = 1672, ready = passReady(), old = document.querySelector('.psList'), keep = old ? old.scrollTop : null;
  let rows = '';
  for (let t = 1; t <= PASS_N; t++) { const r = passRew(t), ok = P.t >= t, got = S.passClaim[t], big = t % 10 === 0;
    rows += `<div class="psRow ${t % 2 ? 'l' : 'r'} ${ok ? 'ok' : ''}" data-row="${t}"><span class="psNode ${ok ? 'ok' : ''} ${big ? 'big' : ''}">${t}</span>
      <div class="psC ${ok ? 'ok' : 'lock'} ${got ? 'got' : ''} ${ok && !got ? 'claim' : ''}" data-pt="${t}" style="background-image:url(${big ? UIA.cMile : ok ? UIA.cNorm : UIA.cLock})">${passCard(r)}${got ? `<img class="psK" alt="" src="${UIA.chk}">` : ''}</div></div>`; }
  skin('passv', W, H, `<div class="z psHead" style="${zP(262, 226, 680, 288, W, H)}"><b>Palier ${P.t}</b><div class="skBar"><i style="width:${P.t < PASS_N ? P.p / P.need * 100 : 100}%"></i></div><small>${P.t < PASS_N ? `${fmt(P.p)} / ${fmt(P.need)}` : 'Terminé'}</small></div>
    <div class="z psList" style="${zP(162, 334, 783, 1422, W, H)}"><div class="psRail"><i style="height:${Math.min(100, P.t / PASS_N * 100)}%"></i></div>${rows}</div>
    ${ready ? `<button class="z skBtn" type="button" id="psAll" style="${zP(285, 1472, 668, 1534, W, H)}">Tout récupérer</button>` : `<div class="z skNote" style="${zP(285, 1472, 668, 1534, W, H)}">⏳ Fin de saison dans ${dhm(left)}</div>`}`,
    `<div class="psInfo"><span>Points : démons, étapes, boss, coffres, donjons, invocations, roue, coffre, connexion.</span></div>`);
  const L = document.querySelector('.psList');
  if (keep !== null) L.scrollTop = keep; else { let f = 1; while (f <= P.t && S.passClaim[f]) f++; const row = L.querySelector(`[data-row="${Math.min(f, PASS_N)}"]`); if (row) L.scrollTop = Math.max(0, row.offsetTop - L.clientHeight * 0.3); }
  document.querySelectorAll('.psC.claim').forEach(c => c.onclick = () => { const t = +c.dataset.pt; if (S.passClaim[t] || passTier().t < t) return; S.passClaim[t] = 1; passGive(passRew(t)); sfxPlay('reward'); toast(`Palier ${t} : ${passTxt(passRew(t))}`); save(); ui(); passSheet(); });
  document.querySelectorAll('.psC:not(.claim)').forEach(c => c.onclick = () => toast(`Palier ${c.dataset.pt} : ${passTxt(passRew(+c.dataset.pt))}`));
  if ($('psAll')) $('psAll').onclick = () => { const P2 = passTier(); let n = 0; for (let t = 1; t <= P2.t; t++) if (!S.passClaim[t]) { S.passClaim[t] = 1; passGive(passRew(t)); n++; } sfxPlay('reward'); toast(`${n} palier${n > 1 ? 's' : ''} récupéré${n > 1 ? 's' : ''}`); save(); ui(); passSheet(); };
}
""" + s[b:]
s = s.replace('<style id="sv">', r'''<style id="sv">/* p32 passe vertical */
.s-passv .sknX{width:8cqw;height:8cqw;font-size:4cqw;right:2%;top:1%}
.s-passv .psHead{gap:2cqw;padding:0 3cqw}.s-passv .psHead b{font-size:4.2cqw}.s-passv .psHead .skBar{height:2.4cqw}.s-passv .psHead small{font-size:3cqw}
.s-passv .skBtn{font-size:4.6cqw}.s-passv .skNote{font-size:3.4cqw;display:grid;place-items:center;color:#e8d0b0}
.psList{display:block!important;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;scrollbar-width:none;padding:4cqw 0 8cqw;-webkit-mask:linear-gradient(transparent,#000 4%,#000 94%,transparent)}.psList::-webkit-scrollbar{display:none}
.psRail{position:absolute;left:calc(50% - .6cqw);top:0;width:1.2cqw;height:calc(var(--n,100) * 1px);display:none}
.psRow{position:relative;height:21cqw;flex:none}
.psNode{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:7.4cqw;height:7.4cqw;border-radius:50%;display:grid;place-items:center;font:400 3.2cqw/1 var(--n);color:#9a8a80;background:radial-gradient(#2a1a18,#0c0607);border:.5cqw solid #6a4a2a;box-shadow:0 0 0 .4cqw #000a;z-index:2}
.psNode.ok{color:#fff;border-color:#ffc44a;background:radial-gradient(#c8401a,#5a0e0a);box-shadow:0 0 2.4cqw #ff8a2a}.psNode.big{width:9cqw;height:9cqw;font-size:3.8cqw}
.psRow .psC{position:absolute;top:50%;transform:translateY(-50%);width:27cqw;aspect-ratio:163/240;gap:.7cqw;padding-top:3cqw}
.psRow.l .psC{right:calc(50% + 6cqw)}.psRow.r .psC{left:calc(50% + 6cqw)}
.psRow .psC i{width:8cqw;height:8cqw}.psRow .psC b{font-size:3.6cqw}.psRow .psC small{font-size:2.4cqw}.psRow .psC.claim{filter:drop-shadow(0 0 2.4cqw #ffb040)}
.psRow::before{content:'';position:absolute;top:50%;height:.6cqw;width:6cqw;background:#6a4a2a}.psRow.l::before{right:50%}.psRow.r::before{left:50%}.psRow.ok::before{background:#ffc44a;box-shadow:0 0 1cqw #ff9a2a}
''', 1)
open(P, 'w').write(s); print('p32 passe vertical ok')
