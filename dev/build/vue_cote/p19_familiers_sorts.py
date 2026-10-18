# p19 : chaque familier a son propre sort (selon son espèce ; la version « 2 » est plus rare donc plus forte)
#  puissance = (55 % + 20 % par rareté) × (1 + 20 % par étoile au-delà de la 1re), en plus de son tir habituel
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p19 familiers sorts' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("function castSpell(id) {", r"""// p19 familiers sorts : un sort par espèce de familier
const FSPL = {
  corbeau: { n: 'Nuée de corbeaux', cd: 8, c: '#c070ff', d: 'Quatre corbeaux fondent sur des démons au hasard' },
  chauve: { n: 'Morsure vampirique', cd: 7, c: '#ff4a6a', d: 'Mord le démon le plus proche et te soigne' },
  rat: { n: 'Rapine', cd: 9, c: '#ffc94a', d: 'Frappe le plus proche et vole de l\'or' },
  papillon: { n: 'Poudre d\'oubli', cd: 10, c: '#e8d0ff', d: 'Ralentit tous les démons 3 s et les blesse' },
  poisson: { n: 'Vague d\'ossements', cd: 9, c: '#7ad8ff', d: 'Une vague frappe tous les démons proches' },
  oeil: { n: 'Regard du vide', cd: 10, c: '#d080ff', d: 'Coup critique sur le démon le plus robuste' },
  champi: { n: 'Spores', cd: 11, c: '#9aff6a', d: 'Te soigne et empoisonne légèrement tous les démons' },
  araignee: { n: 'Toile', cd: 10, c: '#d8e8ff', d: 'Immobilise les 3 démons les plus proches' },
  slime: { n: 'Éclaboussure', cd: 8, c: '#7aff5a', d: 'Explosion acide autour du démon le plus proche' },
  fantome: { n: 'Feux follets', cd: 9, c: '#6affc0', d: 'Trois feux follets frappent des démons au hasard' },
  heaume: { n: 'Rempart', cd: 12, c: '#ffe6a0', d: 'Te donne un bouclier' },
  loup: { n: 'Hurlement', cd: 12, c: '#a0c8ff', d: 'Mord le plus proche, ta vitesse d\'attaque +30 % pendant 4 s' },
};
const famSpl = id => FSPL[id.replace(/2$/, '')], famPw = id => (0.55 + 0.2 * FAM[id].r) * (1 + 0.2 * (famStar(id) - 1));
function famCast(id, at) { const L = alive(), S0 = famSpl(id); if (!S0 || !L.length) return; const st = heroStats(), k = st.atk * famPw(id), kind = id.replace(/2$/, ''), near = () => L.reduce((a, b) => b.z < a.z ? b : a);
  B.fx.push({ k: 'ring2', x: at[0], y: at[1] + 10, t: 0, d: 0.4, c: S0.c, r: 26 }); num(clamp(at[0], 95, BW - 95), at[1] - 26, S0.n, S0.c, 0.8);
  const hit = (e, m, row, crit, delay) => { gfx('imp', row, ex(e), ey(e), 80 * sOf(e.z), 0.35, delay ? { t: -delay } : undefined); B.hitDelay = (delay || 0) * 1000; hitEnemy(e, k * m, !!crit); B.hitDelay = 0; };
  if (kind === 'corbeau') for (let i = 0; i < 4; i++) hit(pick(L), 0.9, 1, 0, i * 0.12);
  else if (kind === 'fantome') for (let i = 0; i < 3; i++) hit(pick(L), 1.2, 3, 0, i * 0.15);
  else if (kind === 'chauve') { hit(near(), 2.2, 1); B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + B.hero.hpMax * 0.03 * famPw(id)); num(CX, YF - 96, '+' + fmt(B.hero.hpMax * 0.03 * famPw(id)), '#7aff8a', 0.85); }
  else if (kind === 'rat') { hit(near(), 1.6, 2); const g = Math.round(goldMul() * 6 * Math.pow(1.11, (B.wave && B.wave.n) || 1) * famPw(id)); S.gold += g; coinFly(at[0], at[1], 2); uiTop(); }
  else if (kind === 'papillon') for (const e of L) { e.chill = Math.max(e.chill || 0, 3); hit(e, 0.5, 3); }
  else if (kind === 'poisson') for (const e of L.filter(e => e.z < 1.1)) hit(e, 1.2, 3, 0, e.z * 0.2);
  else if (kind === 'oeil') { const e = L.reduce((a, b) => b.hp > a.hp ? b : a); gfx('spl', 6, ex(e), py(e.z) - 50 * sOf(e.z), 120 * sOf(e.z), 0.6); hit(e, 3, 1, 1); }
  else if (kind === 'champi') { const h = B.hero.hpMax * 0.05 * famPw(id); B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + h); num(CX, YF - 96, '+' + fmt(h), '#7aff8a', 0.85); for (const e of L) hit(e, 0.4, 1); }
  else if (kind === 'araignee') for (const e of [...L].sort((a, b) => a.z - b.z).slice(0, 3)) { if (!e.boss) e.frozen = Math.max(e.frozen || 0, 1.5); hit(e, 0.8, 3); }
  else if (kind === 'slime') { const e = near(); gfx('imp', 1, ex(e), ey(e), 140 * sOf(e.z), 0.45); aoe(e, 0.2, k * 1.8, 'mort', S0.c); }
  else if (kind === 'heaume') { B.shield = Math.max(B.shield || 0, B.hero.hpMax * 0.06 * famPw(id)); gfx('spl', 1, CX, YF - 50, 130, 0.6); }
  else if (kind === 'loup') { hit(near(), 1.5, 3); B.howlT = 4; } }
function castSpell(id) {""")
rep("if (B.spFrT > 0) o.rate *= 1 + 0.6 * (B.spFrK || 1);", "if (B.spFrT > 0) o.rate *= 1 + 0.6 * (B.spFrK || 1); if (B.howlT > 0) o.rate *= 1.3;")
rep("B.spFrT = (B.spFrT || 0) - dt;", "B.spFrT = (B.spFrT || 0) - dt; B.howlT = (B.howlT || 0) - dt;")
rep("  if (fighting) { B.famTs = B.famTs || [];",
r"""  if (fighting) { B.famSp = B.famSp || []; famSync().forEach((id, i) => { const S0 = famSpl(id); if (!S0) return; B.famSp[i] = (B.famSp[i] === undefined ? 2 + i * 1.3 : B.famSp[i]) - dt; if (B.famSp[i] > 0) return; B.famSp[i] = S0.cd; const P0 = FAMPOS[i]; famCast(id, [CX + P0[0], YF + P0[1]]); }); }
  if (fighting) { B.famTs = B.famTs || [];""")
# fiche du familier : son sort
rep("<div><span>Attaque</span><b>Tire toutes les 2,5 s</b></div>",
    "<div><span>Attaque</span><b>Tire toutes les 2,5 s</b></div><div><span>Sort</span><b style=\"color:${famSpl(id).c}\">${famSpl(id).n}</b></div><div class=\"fspd\"><small>${famSpl(id).d} · toutes les ${famSpl(id).cd} s · puissance ${Math.round(famPw(id) * 100)} %</small></div>")
rep("""return `<button type="button" class="fsl on" data-fam="${id}" style="--rc:${FRC[F.r]}">${famSp(id)}<small>${famTxt(id)}</small></button>`; }).join('')}</div>""",
    """return `<button type="button" class="fsl on" data-fam="${id}" style="--rc:${FRC[F.r]}">${famSp(id)}<small>${famTxt(id)}</small><small style="color:${famSpl(id).c}">${famSpl(id).n}</small></button>`; }).join('')}</div>""")
rep("<p class=\"knote\">Chaque familier équipé tire sur les démons et donne son bonus.", "<p class=\"knote\">Chaque familier équipé tire sur les démons, donne son bonus et lance son propre sort.")
s = s.replace('<style id="sv">', '<style id="sv">/* p19 familiers sorts */\n.fdt .fspd{display:block!important;text-align:center}.fdt .fspd small{font:700 11px var(--b);color:#c8b0a0}\n', 1)
open(P, 'w').write(s); print('p19 familiers sorts ok')
