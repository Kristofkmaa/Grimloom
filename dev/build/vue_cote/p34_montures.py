# p34 : les reliques disparaissent, remplacées par les MONTURES (une par set : Sang, Os, Braise, Givre)
#  débloquées puis montées de niveau avec les Sceaux de leur donjon de set ; une seule montée à la fois
#  bonus de stat par niveau + les bonus de set (2 / 4 / 6) se réveillent aux niveaux 1 / 10 / 20 de la monture
#  les reliques possédées sont rendues en Sceaux ; le passe donne des Sceaux à la place des reliques
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p34 montures' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
# bonus de set : ceux de la monture montée
rep("function setCounts(eq) { const n = {}; for (const id of (S.relEq || [])) { const R = id && typeof REL !== 'undefined' && REL[id]; if (R) n[R.set] = (n[R.set] || 0) + 1; } return n; }",
    "function setCounts(eq) { const n = {}, k = S.mountEq, lv = k && S.mounts && S.mounts[k] || 0; if (lv) n[k] = lv >= 20 ? 6 : lv >= 10 ? 4 : 2; return n; } // p34 montures")
rep("  for (const id of S.relEq) if (id && S.rels[id]) { const v = relVal(id), k = RSTAT[REL[id].set]; if (k === 'atk') o.atk *= 1 + v / 100; else if (k === 'pv') o.pv *= 1 + v / 100; else if (k === 'rate') o.rate *= 1 + v / 100; else o.crit += v; }",
    "  { const k = S.mountEq, lv = k && S.mounts && S.mounts[k] || 0; if (lv) { const v = MNT[k].v * lv; if (MNT[k].k === 'atk') o.atk *= 1 + v / 100; else if (MNT[k].k === 'pv') o.pv *= 1 + v / 100; else if (MNT[k].k === 'rate') o.rate *= 1 + v / 100; else o.crit += v; } }")
# données + fiche
rep("function relSheet() {", r"""const MNT = { sang: { n: 'Destrier écarlate', k: 'atk', v: 1.5, ic: 'drop', d: 'Un destrier démoniaque à la crinière de sang' }, os: { n: 'Destrier d\'os', k: 'pv', v: 2, ic: 'shield', d: 'Un cheval squelette aux sabots de pierre' }, braise: { n: 'Cauchemar de braise', k: 'rate', v: 1.2, ic: 'flame', d: 'Une monture de feu qui laisse des braises' }, givre: { n: 'Loup du givre', k: 'crit', v: 0.5, ic: 'snow', d: 'Un loup géant au pelage de glace' } };
const MNT_MAX = 30, mntUnl = 20, mntCost = lv => 6 + lv * 2, MKN = { atk: 'Attaque', pv: 'Points de vie', rate: 'Vitesse d\'attaque', crit: 'Critique' };
S.mounts = S.mounts || {}; if (S.mountEq === undefined) S.mountEq = null;
if (!S.relGone) { S.relGone = 1; let g = 0; for (const id in (S.rels || {})) { const R = REL[id]; if (!R) continue; const n = (R.r + 1) * 6 * (S.rels[id].s || 1); S.seals[R.set] += n; g += n; } S.rels = {}; S.relEq = [null, null, null, null, null, null]; if (g) setTimeout(() => toast(`Les reliques deviennent des montures : +${g} Sceaux rendus`), 3000); }
function mountSheet() {
  const card = k => { const M = MNT[k], St = SETS[k], lv = S.mounts[k] || 0, eq = S.mountEq === k, c = lv ? mntCost(lv) : mntUnl, ok = S.seals[k] >= c && lv < MNT_MAX, tier = lv >= 20 ? 6 : lv >= 10 ? 4 : lv ? 2 : 0;
    return `<div class="mcard ${lv ? '' : 'lock'} ${eq ? 'eq' : ''}" style="--sc:${St.c}"><div class="mtop"><i class="mic">${IC[M.ic]}</i><div><b>${M.n}</b><small>${lv ? `Niveau ${lv} / ${MNT_MAX}` : M.d}</small></div>${eq ? '<em>Montée</em>' : ''}</div>
      <div class="mst">${MKN[M.k]} <b>+${(M.v * Math.max(1, lv)).toFixed(M.v % 1 ? 1 : 0)}${M.k === 'crit' ? ' pts' : ' %'}</b>${lv ? '' : ' au niveau 1'}</div>
      <div class="mset"><small>${St.n}</small>${St.b.map(([n, t], i) => `<p class="${tier >= n ? 'on' : ''}"><i>Nv ${[1, 10, 20][i]}</i>${t}</p>`).join('')}</div>
      <div class="mbt">${lv ? `<button class="btn ${eq ? '' : 'gold'}" type="button" data-meq="${k}">${eq ? 'Descendre' : 'Monter'}</button>` : ''}<button class="btn gold" type="button" data-mup="${k}" ${ok ? '' : 'disabled'}>${lv ? (lv >= MNT_MAX ? 'Niveau max' : 'Améliorer') : 'Débloquer'}<small>${lv >= MNT_MAX ? '' : `${c} Sceaux · tu as ${S.seals[k]}`}</small></button></div></div>`; };
  sheet(`<h3>Montures <button class="x" type="button" aria-label="Fermer">✕</button></h3><p class="knote" style="margin-top:0">Débloque et améliore les montures avec les <b>Sceaux</b> des donjons de set. Une seule montée à la fois : elle donne son bonus et réveille les pouvoirs de son set aux niveaux 1, 10 et 20.</p><div class="mgrid">${SETK.map(card).join('')}</div>`);
  const m = $('mbox');
  m.querySelectorAll('[data-mup]').forEach(b => b.onclick = () => { const k = b.dataset.mup, lv = S.mounts[k] || 0, c = lv ? mntCost(lv) : mntUnl; if (S.seals[k] < c || lv >= MNT_MAX) return; S.seals[k] -= c; S.mounts[k] = lv + 1; if (!lv && !S.mountEq) S.mountEq = k; sfxPlay('reward'); toast(lv ? `${MNT[k].n} niveau ${lv + 1}` : `${MNT[k].n} débloqué !`); save(); ui(); mountSheet(); });
  m.querySelectorAll('[data-meq]').forEach(b => b.onclick = () => { const k = b.dataset.meq; S.mountEq = S.mountEq === k ? null : k; save(); ui(); mountSheet(); });
}
function relSheet() {""")
rep("const fam = famSync().length && S.fam, w = wEq(), nRel = S.relEq.filter(Boolean).length,", "const fam = famSync().length && S.fam, w = wEq(), mk = S.mountEq,")
rep("""art('relSlot', 'rel', 'Reliques', nRel ? `<span class="rmini">${S.relEq.filter(Boolean).slice(0, 4).map(id => relSp(id)).join('')}</span><span class="lv">${nRel}/6</span>` : '<i class="wplus">+</i>', nRel > 0, '#ffc23a')""",
    """art('relSlot', 'rel', 'Monture', mk ? `<i class="mmini" style="color:${SETS[mk].c}">${IC[MNT[mk].ic]}</i><span class="lv">Nv ${S.mounts[mk]}</span>` : '<i class="wplus">+</i>', !!mk, mk ? SETS[mk].c : '')""")
rep("""<button type="button" class="slot art lockd" data-soon="Monture"><i class="flk">${IC.lock}</i><span class="nm">Monture</span></button>""", """<button type="button" class="slot art lockd" data-soon="Artefact mystère"><i class="flk">${IC.lock}</i><span class="nm">???</span></button>""")
rep("bind('relSlot', relSheet);", "bind('relSlot', mountSheet);")
rep("rel: [26, 'Reliques']", "rel: [26, 'Montures']")
rep("  rel: [null, 'Invoque des <b>reliques</b> avec les Sceaux des donjons, puis place-les sur l\\'autel : 6 emplacements et des bonus de set.', () => relSheet()],",
    "  rel: [null, 'Débloque des <b>montures</b> avec les Sceaux des donjons de set : chacune donne un bonus et réveille les pouvoirs de son set.', () => mountSheet()],")
# invocation : plus d'onglet Reliques
rep("[['fam', 'Familiers'], ['grim', 'Grimoire'], ['rel', 'Reliques']]", "[['fam', 'Familiers'], ['grim', 'Grimoire']]")
rep("  if (SUMTAB === 'rel') return relPage(pg);", "  if (SUMTAB === 'rel') SUMTAB = 'fam';")
# passe : Sceaux à la place des reliques
rep("function passCard(r) {", "const PRW0 = passRew; passRew = t => { const r = PRW0(t); if (r && r.rel) { const o = Object.assign({}, r); o.seals = 15 * o.rel; delete o.rel; return o; } return r; };\nfunction passCard(r) {")
# textes
rep("'Invoquer des reliques (page Invocation). 2, 4 ou 6 reliques du même set réveillent ses bonus.'", "'Débloquer et améliorer les montures (case Monture). Niveaux 1, 10 et 20 : les pouvoirs de son set se réveillent.'")
rep("Ils donnent des <b>Sceaux</b> pour invoquer des <b>reliques</b> (Sang, Os, Braises, Givre). Équipe-en 2, 4 ou 6 du même set sur l\\'autel pour réveiller ses bonus.",
    "Ils donnent des <b>Sceaux</b> pour débloquer et améliorer les <b>montures</b> (Sang, Os, Braises, Givre). Chaque monture réveille les pouvoirs de son set.")
s = s.replace('<style id="sv">', r'''<style id="sv">/* p34 montures */
.mgrid{display:flex;flex-direction:column;gap:10px}
.mcard{border-radius:14px;padding:10px;background:linear-gradient(#2a141c,#140a0e);border:2px solid color-mix(in srgb,var(--sc) 55%,#3a2028)}.mcard.eq{box-shadow:0 0 14px -4px var(--sc)}.mcard.lock{opacity:.85;border-color:#4a2a36}
.mtop{display:flex;align-items:center;gap:10px}.mtop .mic{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;color:var(--sc);background:radial-gradient(#3a1a20,#0c0507);border:2px solid var(--sc);flex:none}.mtop .mic svg{width:24px;height:24px}
.mtop b{display:block;font:400 16px var(--n);color:#fff}.mtop small{font:700 11px var(--b);color:#c8b098}.mtop em{margin-left:auto;font:800 10px var(--b);font-style:normal;color:#000;background:var(--sc);border-radius:8px;padding:2px 7px}
.mst{margin:8px 0 4px;font:700 12px var(--b);color:#d8c0b0}.mst b{color:var(--sc)}
.mset small{font:800 10px var(--b);letter-spacing:.08em;text-transform:uppercase;color:var(--sc)}.mset p{margin:3px 0;font:700 11px/1.3 var(--b);color:#7a6a60}.mset p.on{color:#f0e0d0}.mset p i{font-style:normal;display:inline-block;min-width:38px;color:var(--sc);font-weight:900}
.mbt{display:flex;gap:6px;margin-top:8px}.mbt .btn{flex:1}
#eqg .mmini{display:grid;place-items:center;width:36px;height:36px}#eqg .mmini svg{width:30px;height:30px}
''', 1)
open(P, 'w').write(s); print('p34 montures ok')
