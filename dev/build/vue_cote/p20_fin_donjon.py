# p20 : écran de fin de donjon / raid (victoire ou échec, récompenses, bouton de retour) + suppression des messages inutiles
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p20 fin donjon' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

# messages au milieu de l'écran qui n'apportent rien
rep("function toast(t) {", "const TOAST_MUTE = /équipé|Meilleur objet|^Recyclé|^Clé bénie|^Coffre niveau|^Ouverture auto (activée|désactivée)|^Sac supprimé|^Stuff /; // p20 fin donjon\nfunction toast(t) { if (TOAST_MUTE.test(t)) return;")

# écran de fin
rep("function dunEnd(win, why) {", r"""function dunScreen(o) { // o : { win, title, sub, rows: [[icône, couleur, texte]], back }
  const d = document.createElement('div'); d.id = 'dunEnd'; d.className = o.win ? 'win' : 'lose';
  d.innerHTML = `<div class="deGlow"></div><div class="deBox"><small>${o.mode}</small><h2>${o.title}</h2><p>${o.sub}</p>
    ${o.rows.length ? `<div class="deRw">${o.rows.map(([ic, c, t], i) => `<div style="--c:${c};animation-delay:${0.35 + i * 0.12}s"><i>${IC[ic] || ''}</i><b>${t}</b></div>`).join('')}</div>` : ''}
    <button class="btn gold" type="button" id="deBack">Retour à l'aventure</button></div>`;
  $('app').appendChild(d); sfxPlay(o.win ? 'reward' : 'hurt');
  $('deBack').onclick = () => { d.remove(); o.back(); }; }
function dunEnd(win, why) {""")
back = "() => { B.dun = null; B.scene = 'x'; B.fade = 1; B.hero.dead = 0; B.cs = []; startWave(); ui(); }"
rep("B.banner = { a: `Palier ${t} / ${RAID_TIERS.length}`, b: `${fmt(dmg)} dégâts · +${pl} plumes`, t: 2.8 }; save(); setTimeout(() => { B.dun = null; B.scene = 'x'; B.fade = 1; B.hero.dead = 0; B.cs = []; startWave(); ui(); }, 2800); return; }",
    "save(); setTimeout(() => dunScreen({ win: true, mode: 'Raid · Archidémon', title: `Palier ${t} / ${RAID_TIERS.length}`, sub: `${fmt(dmg)} dégâts infligés`, rows: [['star', '#c070ff', `+${pl} plumes`], ['flame', '#c58aff', `+${2 + t} âmes`]], back: " + back + " }), 1100); return; }")
rep("B.banner = { a: 'Victoire !', b: `+${rdTxt(rw)} · niveau ${D.lv + 1} débloqué`, t: 2.4 }; }",
    "D.scr = { win: true, mode: dunName(D.k), title: 'Victoire !', sub: `Niveau ${D.lv} terminé · niveau ${D.lv + 1} débloqué`, rows: [[RD[D.k].ic, RD[D.k].c, '+' + rdTxt(rw)]] }; }")
rep("B.banner = { a: 'Victoire !', b: `+${r} Sceaux · ${SETS[D.k].n}`, t: 2.4 }; }",
    "D.scr = { win: true, mode: dunName(D.k), title: 'Victoire !', sub: `Niveau ${D.lv} terminé · niveau ${D.lv + 1} débloqué`, rows: [['shield', SETS[D.k].c, `+${r} Sceaux · ${SETS[D.k].n}`], ['book', '#ff9a6a', `+${5 + D.lv} pages`]] }; }")
rep("else B.banner = { a: 'Échec', b: `${why} · le ticket n'est pas consommé`, t: 2.4 };\n  save(); setTimeout(() => { B.dun = null; B.scene = 'x'; B.fade = 1; B.hero.dead = 0; startWave(); ui(); }, 2300);",
    "else D.scr = { win: false, mode: dunName(D.k), title: 'Échec', sub: why, rows: [['key', '#ffd890', 'Ton ticket n\\'est pas consommé']] };\n  save(); setTimeout(() => dunScreen(Object.assign(D.scr, { back: " + back + " })), win ? 1100 : 1400);")

s = s.replace('<style id="sv">', r'''<style id="sv">/* p20 fin donjon */
#dunEnd{position:absolute;inset:0;z-index:45;display:grid;place-items:center;padding:24px;background:radial-gradient(circle at 50% 40%,#2a1008e8,#050204f2 70%);animation:deIn .35s ease-out}
@keyframes deIn{from{opacity:0}}
#dunEnd .deGlow{position:absolute;left:50%;top:38%;width:520px;height:520px;margin:-260px;border-radius:50%;background:repeating-conic-gradient(#ffd27a22 0 8deg,transparent 8deg 22deg);animation:deSpin 14s linear infinite;pointer-events:none}
#dunEnd.lose .deGlow{background:repeating-conic-gradient(#ff304022 0 8deg,transparent 8deg 22deg)}
@keyframes deSpin{to{transform:rotate(360deg)}}
#dunEnd .deBox{position:relative;width:100%;max-width:320px;text-align:center;padding:20px 16px 16px;border-radius:18px;background:linear-gradient(#2e1823,#140910);border:2px solid #c8964a;box-shadow:0 0 40px #000,0 0 30px -6px #ffb040;animation:dePop .45s cubic-bezier(.2,1.5,.4,1)}
#dunEnd.lose .deBox{border-color:#8a2a3a;box-shadow:0 0 40px #000,0 0 30px -6px #ff3040}
@keyframes dePop{from{transform:scale(.6);opacity:0}}
#dunEnd small{display:block;font:800 11px var(--b);letter-spacing:.18em;text-transform:uppercase;color:#d6aa60}
#dunEnd h2{margin:6px 0 2px;font:900 34px var(--t);color:#ffd890;text-shadow:0 3px 0 #000,0 0 18px #ff9a2a}
#dunEnd.lose h2{color:#ff6a7a;text-shadow:0 3px 0 #000,0 0 18px #ff2040}
#dunEnd p{margin:0 0 14px;font:700 13px var(--b);color:#d8c0b0}
#dunEnd .deRw{display:flex;flex-direction:column;gap:7px;margin-bottom:16px}
#dunEnd .deRw div{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:12px;background:#0006;border:1.5px solid color-mix(in srgb,var(--c) 55%,transparent);animation:dePop .4s both}
#dunEnd .deRw i{display:grid;place-items:center;width:26px;height:26px;color:var(--c)}#dunEnd .deRw i svg{width:22px;height:22px}
#dunEnd .deRw b{font:400 17px var(--n);color:#fff;text-align:left}
#dunEnd .btn{width:100%}
''', 1)
open(P, 'w').write(s); print('p20 fin donjon ok')
