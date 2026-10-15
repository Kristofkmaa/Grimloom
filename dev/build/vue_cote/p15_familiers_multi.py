# p15 : plusieurs familiers équipés à la fois (comme Legend of Mushroom)
#  1 emplacement au départ, +1 aux étapes 3-1, 4-1, 5-1, 6-1 (5 max). Chaque familier tire et donne son bonus.
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p15 familiers multi' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

# données : liste des familiers équipés
rep("const famK = k => (S.fam && FAM[S.fam] && FAM[S.fam].k === k && S.fams[S.fam] ? famVal(S.fam) : 0);",
r"""const FAM_UNL = [0, 21, 31, 41, 51]; // p15 familiers multi : étape (index) qui ouvre chaque emplacement
const famSlots = () => FAM_UNL.filter(i => (S.best || 1) >= i).length;
function famSync() { if (!Array.isArray(S.famEq)) S.famEq = S.fam ? [S.fam] : []; if (S.fam && !S.famEq.length && S.fams[S.fam]) S.famEq.push(S.fam);
  S.famEq = S.famEq.filter((id, i, a) => FAM[id] && S.fams[id] && a.indexOf(id) === i).slice(0, famSlots()); S.fam = S.famEq[0] || null; return S.famEq; }
const famK = k => famSync().reduce((a, id) => a + (FAM[id].k === k ? famVal(id) : 0), 0);""")
rep("if (!S.fam) S.fam = id;", "famSync(); if (S.famEq.length < famSlots() && !S.famEq.includes(id)) S.famEq.push(id);")
# combat : chaque familier tire avec son propre rythme
rep("  if (S.fam && FAM[S.fam] && S.fams[S.fam] && fighting) { B.famT = (B.famT || 1) - dt; if (B.famT <= 0) { B.famT = 2.5; const L = alive(); if (L.length) { const F = FAM[S.fam], t = L.reduce((a, b) => b.z < a.z ? b : a); B.shots.push({ X: 0, z: -0.34, h: 122, tg: t, dmg: st.atk * 0.18 * (1 + 0.3 * F.r) * (1 + 0.25 * (famStar(S.fam) - 1)), crit: false, t: 0, fx: 'arc', prj: F.p, solid: 0, wr: -1, comp: 'fam' }); } } }",
    "  if (fighting) { B.famTs = B.famTs || []; famSync().forEach((id, i) => { B.famTs[i] = (B.famTs[i] === undefined ? 0.6 + i * 0.45 : B.famTs[i]) - dt; if (B.famTs[i] > 0) return; B.famTs[i] = 2.5; const L = alive(); if (!L.length) return; const F = FAM[id], t = L.reduce((a, b) => b.z < a.z ? b : a), P0 = FAMPOS[i]; B.shots.push({ X: 0, z: (P0[0] - 46) / ZW, h: -P0[1] + 6, tg: t, dmg: st.atk * 0.18 * (1 + 0.3 * F.r) * (1 + 0.25 * (famStar(id) - 1)), crit: false, t: 0, fx: 'arc', prj: F.p, solid: 0, wr: -1, comp: 'fam' }); }); }")
# affichage : jusqu'à 5 familiers qui flottent derrière le héros
old = s[s.index("  if (S.fam && FAM[S.fam] && S.fams[S.fam]) L.push({ z: 0.05, y: YF - 1, f: () => {"):]
old = old[:old.index("} } });\n") + len("} } });\n")]
rep(old, r"""  famSync().forEach((id, i) => L.push({ z: 0.05 + i * 0.01, y: YF - 1 - i, f: () => { const F = FAM[id], im = IMG.fam_sp, P0 = FAMPOS[i], bob = Math.sin(time * 2.4 + i * 1.3) * 5, x = CX + P0[0], y = YF + P0[1] + bob, sz = (52 + F.r * 3) * (i ? 0.8 : 1);
    ctx.globalCompositeOperation = 'lighter'; glow(x, y, 26 + F.r * 4, FRC[F.r], 0.28 + 0.06 * F.r); ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = '#0006'; ctx.beginPath(); ctx.ellipse(x, YF - 6, 14, 3.5, 0, 0, 7); ctx.fill();
    if (im && im.complete) { ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(im, F.i * 128, 0, 128, 128, x - sz / 2, y - sz / 2, sz, sz); ctx.restore(); } } }));
""")
rep("const famK = k =>", "const FAMPOS = [[-44, -122], [26, -150], [-20, -176], [62, -118], [88, -168]]; // position de chaque familier (par rapport au héros)\nconst famK = k =>")
# fiche d'un familier : équiper / retirer
rep("  ${o ? `<button class=\"btn ${S.fam === id ? '' : 'gold'}\" id=\"fEq\" type=\"button\" style=\"width:100%;margin-top:12px\">${S.fam === id ? 'Retirer' : 'Équiper'}</button>` : '<p class=\"knote\" style=\"text-align:center\">Invoque-le depuis le portail d\\'Invocation.</p>'}`);\n  if ($('fEq')) $('fEq').onclick = () => { S.fam = S.fam === id ? null : id; save(); ui(); famSheet(); };",
    "  ${o ? (famSync().includes(id) ? `<button class=\"btn\" id=\"fEq\" type=\"button\" style=\"width:100%;margin-top:12px\">Retirer</button>` : S.famEq.length < famSlots() ? `<button class=\"btn gold\" id=\"fEq\" type=\"button\" style=\"width:100%;margin-top:12px\">Équiper<small>${S.famEq.length + 1} / ${famSlots()} emplacements</small></button>` : `<button class=\"btn gold\" id=\"fEq\" type=\"button\" style=\"width:100%;margin-top:12px\">Remplacer ${FAM[S.famEq[S.famEq.length - 1]].n.split(' ')[0]}<small>tous les emplacements sont pris (${famSlots()} / ${famSlots()})</small></button>`) : '<p class=\"knote\" style=\"text-align:center\">Invoque-le depuis le portail d\\'Invocation.</p>'}`);\n  if ($('fEq')) $('fEq').onclick = () => { famSync(); const j = S.famEq.indexOf(id); if (j >= 0) S.famEq.splice(j, 1); else if (S.famEq.length < famSlots()) S.famEq.push(id); else S.famEq[S.famEq.length - 1] = id; famSync(); B.famTs = []; save(); ui(); famSheet(); };")
rep("S.fam === id", "famSync().includes(id)", 2)
# page Familiers : la rangée des emplacements
rep("""  return `<h4 class="kh" style="margin-top:0">Compagnon</h4>
  ${eq ? `<div class="kl fcur" data-fam="${S.fam}" style="--rc:${FRC[eq.r]}">${famSp(S.fam, 'mid')}<div><b style="color:${FRC[eq.r]}">${eq.n}</b><span class="fst">${famStars(S.fam)}</span><small>${famTxt(S.fam)} · tire sur les démons</small></div></div>` : '<p class="knote">Aucun familier équipé : touche-en un dans ta collection.</p>'}""",
"""  const fe = famSync(), nS = famSlots();
  return `<h4 class="kh" style="margin-top:0">Familiers équipés <b class="spCnt">${fe.length} / ${nS}</b></h4>
  <div class="fslots">${FAM_UNL.map((u, i) => { const id = fe[i]; if (i >= nS) return `<div class="fsl lk"><i>${IC.lock}</i><small>Étape ${stName(u)}</small></div>`; if (!id) return `<div class="fsl em"><b>+</b><small>Libre</small></div>`; const F = FAM[id]; return `<button type="button" class="fsl on" data-fam="${id}" style="--rc:${FRC[F.r]}">${famSp(id)}<small>${famTxt(id)}</small></button>`; }).join('')}</div>
  <p class="knote">Chaque familier équipé tire sur les démons et donne son bonus. ${fe.length ? '' : 'Touche-en un dans ta collection pour l\\'équiper.'}</p>""")
# case Familier de la grille d'équipement
rep("const fam = S.fam && S.fams[S.fam], w = wEq(),", "const fam = famSync().length && S.fam, w = wEq(),")
rep("""fam ? `<canvas id="famMini" width="64" height="64"></canvas><span class="lv">${famStar(S.fam)}★</span>` : '<i class="wplus">+</i>'""",
    """fam ? `<canvas id="famMini" width="64" height="64"></canvas><span class="lv">${S.famEq.length}/${famSlots()}</span>` : '<i class="wplus">+</i>'""")
s = s.replace('<style id="sv">', r'''<style id="sv">/* p15 familiers multi */
.fslots{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:8px}
.fsl{position:relative;aspect-ratio:1;border-radius:12px;border:2px solid #4a2a36;background:radial-gradient(circle at 50% 40%,#3a2030,#170b11);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2px;color:#a08a78;overflow:hidden}
.fsl.on{border-color:var(--rc);box-shadow:0 0 10px -3px var(--rc)}.fsl.on>*:first-child{width:70%!important;height:auto!important;max-height:62%}
.fsl small{font:800 7.5px/1.1 var(--b);text-align:center;color:#d8c0a8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.fsl.em b{font:400 20px/1 var(--n);color:#8a6a50}.fsl.lk{opacity:.5}.fsl.lk i{display:grid;place-items:center}.fsl.lk svg{width:16px;height:16px}
''', 1)
open(P, 'w').write(s); print('p15 familiers multi ok')
