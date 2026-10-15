# p19 (provisoire, en attendant des sorts propres aux familiers) : chaque familier lance un pouvoir offensif que le joueur n'a PAS équipé
#  à 50 % de puissance (+20 % par étoile), au rythme du pouvoir ×1,3, en plus de son tir habituel
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p19 familiers sorts' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("function castSpell(id) {\n  const st = heroStats(), k = spPct(id) / 100, L = alive(), sp = SPELLS[id]; if (!L.length && id !== 'shield' && id !== 'frenzy') return;\n  B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1);",
r"""const FSP = ['blades', 'meteor', 'nova', 'chain', 'plague', 'smite']; // p19 familiers sorts : pouvoirs offensifs
function famSpells() { const eq = S.slots.slice(0, slotCount()).filter(Boolean), pool = FSP.filter(k => !eq.includes(k)); return famSync().map((id, i) => pool.length ? pool[(i + Object.keys(FAM).indexOf(id)) % pool.length] : null); }
function castSpell(id) {
  const st = heroStats(), k = spPct(id) / 100 * (B.spMul || 1), L = alive(), sp = SPELLS[id]; if (!L.length && id !== 'shield' && id !== 'frenzy') return;
  if (B.famAt) num(B.famAt[0], B.famAt[1] - 26, sp.n, sp.c, 0.8); else { B.fx.push({ k: 'ring', x: CX, y: YF - 20, t: 0, d: 0.4, c: sp.c }); num(CX, YF - 110, sp.n, sp.c, 1); }""")
rep("  if (fighting) { B.famTs = B.famTs || [];",
r"""  if (fighting) { B.famSp = B.famSp || []; const FS = famSpells(); famSync().forEach((id, i) => { const k = FS[i]; if (!k) return; B.famSp[i] = (B.famSp[i] === undefined ? 2 + i * 1.3 : B.famSp[i]) - dt; if (B.famSp[i] > 0) return; B.famSp[i] = SPELLS[k].cd * 1.3; const P0 = FAMPOS[i];
    B.spMul = 0.5 * (1 + 0.2 * (famStar(id) - 1)); B.famAt = [CX + P0[0], YF + P0[1]]; B.fx.push({ k: 'ring', x: CX + P0[0], y: YF + P0[1], t: 0, d: 0.35, c: SPELLS[k].c }); try { castSpell(k); } finally { B.spMul = 1; B.famAt = null; } }); }
  if (fighting) { B.famTs = B.famTs || [];""")
# page Familiers : le pouvoir lancé par chaque familier équipé
rep("""return `<button type="button" class="fsl on" data-fam="${id}" style="--rc:${FRC[F.r]}">${famSp(id)}<small>${famTxt(id)}</small></button>`; }).join('')}</div>""",
    """const k = famSpells()[i]; return `<button type="button" class="fsl on" data-fam="${id}" style="--rc:${FRC[F.r]}">${famSp(id)}<small>${famTxt(id)}</small>${k ? `<small style="color:${SPELLS[k].c}">${SPELLS[k].n}</small>` : ''}</button>`; }).join('')}</div>""")
rep("<p class=\"knote\">Chaque familier équipé tire sur les démons et donne son bonus.", "<p class=\"knote\">Chaque familier équipé tire sur les démons, donne son bonus et lance un pouvoir que tu n'as pas équipé (50 % de puissance, +20 % par étoile).")
s = s.replace('<style id="sv">', '<style id="sv">/* p19 familiers sorts */', 1)
open(P, 'w').write(s); print('p19 familiers sorts ok')
