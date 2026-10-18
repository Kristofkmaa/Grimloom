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
    "function setCounts(eq) { const n = {}, k = S.mountEq, lv = k && S.mounts && S.mounts[k] || 0; if (lv && MNT[k]) n[MNT[k].set] = lv >= 20 ? 6 : lv >= 10 ? 4 : 2; return n; } // p34 montures")
rep("  for (const id of S.relEq) if (id && S.rels[id]) { const v = relVal(id), k = RSTAT[REL[id].set]; if (k === 'atk') o.atk *= 1 + v / 100; else if (k === 'pv') o.pv *= 1 + v / 100; else if (k === 'rate') o.rate *= 1 + v / 100; else o.crit += v; }",
    "  { const k = S.mountEq, lv = k && S.mounts && S.mounts[k] || 0; if (lv && MNT[k]) { const v = MNT[k].v * lv; if (MNT[k].k === 'atk') o.atk *= 1 + v / 100; else if (MNT[k].k === 'pv') o.pv *= 1 + v / 100; else if (MNT[k].k === 'rate') o.rate *= 1 + v / 100; else o.crit += v; } }")
# données + fiche
rep("function relSheet() {", r"""const MNT = { // set : pouvoirs réveillés · any : se paie avec n'importe quels Sceaux · seat : selle dans la case de la planche (ASSETS.MOUNT)
  chopper: { n: 'Chopper d\'ossements', set: 'sang', k: 'atk', v: 1.5, ic: 'skull', d: 'Une moto faite d\'os, phare en crâne, pots d\'échappement en tibias', seat: [92, 100] },
  cercueil: { n: 'Cercueil à roulettes', set: 'os', k: 'pv', v: 2, ic: 'shield', d: 'Un cercueil sur roues propulsé par un petit moteur qui crachote', seat: [126, 112] },
  coq: { n: 'Coq des enfers', set: 'braise', k: 'rate', v: 1.2, ic: 'wind', d: 'Un poulet démoniaque géant, très en colère, qui court très vite', seat: [115, 90] },
  escargot: { n: 'Escargot de siège', set: 'givre', k: 'crit', v: 0.5, ic: 'gem', d: 'Un escargot énorme portant une tour de guet sur sa coquille', seat: [166, 100] },
  destrier_rouge: { n: 'Destrier écarlate', set: 'sang', any: 1, k: 'atk', v: 2.2, ic: 'flame', d: 'Un destrier démoniaque à la crinière de flammes · se paie avec tous tes Sceaux', seat: [104, 88] },
  destrier_os: { n: 'Destrier d\'os', set: 'os', any: 1, k: 'pv', v: 3, ic: 'snow', d: 'Un cheval squelette aux flammes bleues · se paie avec tous tes Sceaux', seat: [112, 90] } };
const MKS = Object.keys(MNT), MNT_MAX = 30, mntUnl = k => MNT[k].any ? 45 : 20, mntCost = (k, lv) => Math.round((6 + lv * 2) * (MNT[k].any ? 1.5 : 1)), MKN = { atk: 'Attaque', pv: 'Points de vie', rate: 'Vitesse d\'attaque', crit: 'Critique' };
const mSeals = k => MNT[k].any ? sealTot() : S.seals[MNT[k].set], mPay = (k, c) => MNT[k].any ? sealPay(c) : (S.seals[MNT[k].set] >= c && (S.seals[MNT[k].set] -= c, true));
S.mounts = S.mounts || {}; if (S.mountEq === undefined) S.mountEq = null; { const OLD = { sang: 'chopper', os: 'cercueil', braise: 'coq', givre: 'escargot' }; for (const o in OLD) if (S.mounts[o]) { S.mounts[OLD[o]] = Math.max(S.mounts[OLD[o]] || 0, S.mounts[o]); delete S.mounts[o]; } if (OLD[S.mountEq]) S.mountEq = OLD[S.mountEq]; if (S.mountEq && !MNT[S.mountEq]) S.mountEq = null; }
if (!S.relGone) { S.relGone = 1; let g = 0; for (const id in (S.rels || {})) { const R = REL[id]; if (!R) continue; const n = (R.r + 1) * 6 * (S.rels[id].s || 1); S.seals[R.set] += n; g += n; } S.rels = {}; S.relEq = [null, null, null, null, null, null]; if (g) setTimeout(() => toast(`Les reliques deviennent des montures : +${g} Sceaux rendus`), 3000); }
function mountSheet() {
  const card = k => { const M = MNT[k], St = SETS[M.set], lv = S.mounts[k] || 0, eq = S.mountEq === k, c = lv ? mntCost(k, lv) : mntUnl(k), ok = mSeals(k) >= c && lv < MNT_MAX, tier = lv >= 20 ? 6 : lv >= 10 ? 4 : lv ? 2 : 0;
    return `<div class="mcard ${lv ? '' : 'lock'} ${eq ? 'eq' : ''}" style="--sc:${St.c}"><div class="mtop"><canvas class="mic" data-mnt="${k}" width="96" height="84"></canvas><div><b>${M.n}</b><small>${lv ? `Niveau ${lv} / ${MNT_MAX}` : M.d}</small></div>${eq ? '<em>Montée</em>' : ''}</div>
      <div class="mst">${MKN[M.k]} <b>+${(M.v * Math.max(1, lv)).toFixed(M.v % 1 ? 1 : 0)}${M.k === 'crit' ? ' pts' : ' %'}</b>${lv ? '' : ' au niveau 1'}</div>
      <div class="mset"><small>${St.n}</small>${St.b.map(([n, t], i) => `<p class="${tier >= n ? 'on' : ''}"><i>Nv ${[1, 10, 20][i]}</i>${t}</p>`).join('')}</div>
      <div class="mbt">${lv ? `<button class="btn ${eq ? '' : 'gold'}" type="button" data-meq="${k}">${eq ? 'Descendre' : 'Monter'}</button>` : ''}<button class="btn gold" type="button" data-mup="${k}" ${ok ? '' : 'disabled'}>${lv ? (lv >= MNT_MAX ? 'Niveau max' : 'Améliorer') : 'Débloquer'}<small>${lv >= MNT_MAX ? '' : `${c} Sceaux${M.any ? ' (tous)' : ''} · tu as ${mSeals(k)}`}</small></button></div></div>`; };
  sheet(`<h3>Montures <button class="x" type="button" aria-label="Fermer">✕</button></h3><p class="knote" style="margin-top:0">Débloque et améliore les montures avec les <b>Sceaux</b> des donjons de set. Une seule montée à la fois : elle donne son bonus et réveille les pouvoirs de son set aux niveaux 1, 10 et 20.</p><div class="mgrid">${MKS.map(card).join('')}</div>`);
  const m = $('mbox');
  m.querySelectorAll('[data-mup]').forEach(b => b.onclick = () => { const k = b.dataset.mup, lv = S.mounts[k] || 0, c = lv ? mntCost(k, lv) : mntUnl(k); if (lv >= MNT_MAX || !mPay(k, c)) return; S.mounts[k] = lv + 1; if (!lv && !S.mountEq) S.mountEq = k; sfxPlay('reward'); toast(lv ? `${MNT[k].n} niveau ${lv + 1}` : `${MNT[k].n} débloqué !`); save(); ui(); mountSheet(); });
  mntIcons(m);
  m.querySelectorAll('[data-meq]').forEach(b => b.onclick = () => { const k = b.dataset.meq; S.mountEq = S.mountEq === k ? null : k; save(); ui(); mountSheet(); });
}
function mntIcons(root) { root.querySelectorAll('canvas[data-mnt]').forEach(c => { const k = c.dataset.mnt, A = ASSETS.MOUNT && ASSETS.MOUNT[k], im = MNTI[k]; if (!A || !im) return; const dr = () => { if (!c.isConnected) return; if (!im.complete || !im.naturalWidth) return setTimeout(dr, 120); const g = c.getContext('2d'); g.clearRect(0, 0, c.width, c.height); g.imageSmoothingEnabled = true; const sc = Math.min(c.width / A.cw, c.height / A.ch) * 1.25; g.drawImage(im, 0, A.ch, A.cw, A.ch, (c.width - A.cw * sc) / 2, c.height - (A.ch - A.foot * 0.6) * sc, A.cw * sc, A.ch * sc); }; dr(); }); }
const MNTI = {}; for (const k in (ASSETS.MOUNT || {})) MNTI[k] = lazyImg(ASSETS.MOUNT[k].src);
// en combat : la monture sous le héros (course pendant les avances, attente, action au début de chaque vague)
function mountDraw(time, anim) { const k = S.mountEq, A = k && ASSETS.MOUNT && ASSETS.MOUNT[k], im = k && MNTI[k], h = B.hero; if (!A || !im || h.dead || !im.complete || !im.naturalWidth) return false;
  if (B.walk) B.mntW = 1; else if (B.mntW) { B.mntW = 0; B.mntAct = B.t; }
  const msc = (A.k || 0.5) * 1.35, M = MNT[k], act = B.t - (B.mntAct ?? -9), [qx, qy] = M.seat, foot = A.ch - A.foot; let row = 1, f = Math.floor(time * 4) % 4, up = 0;
  if (B.walk) { row = 0; f = Math.floor(time * 11) % 4; } else if (act < 0.9) { row = 2; f = clamp(Math.floor(act / 0.9 * 4), 0, 3); up = Math.sin(act / 0.9 * Math.PI) * 10; }
  const x0 = CX - (qx - 0) * msc, y0 = YF - foot * msc, seatY = y0 + qy * msc, lift = YF - seatY - 24 + up;
  ctx.save(); ctx.beginPath(); ctx.rect(-50, -OFFY - 300, BW + 100, seatY + 8 - up + OFFY + 300); ctx.clip(); ctx.translate(0, -lift); B.mntIn = 1; try { drawSideHero(time, anim === 'course' ? 'idle' : anim); } finally { B.mntIn = 0; } ctx.restore();
  ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im, f * A.cw, row * A.ch, A.cw, A.ch, Math.round(x0), Math.round(y0), Math.round(A.cw * msc), Math.round(A.ch * msc)); ctx.restore();
  if (B.walk && Math.random() < 0.4) B.fx.push({ k: 'p', x: x0 + rand(10, 40) * msc, y: YF - rand(0, 6), vx: rand(-40, -10), vy: rand(-20, -5), g: 0, c: '#8a7a6a', t: 0, d: 0.5, r: rand(1, 2.2) });
  return true; }
function relSheet() {""")
rep("const fam = famSync().length && S.fam, w = wEq(), nRel = S.relEq.filter(Boolean).length,", "const fam = famSync().length && S.fam, w = wEq(), mk = S.mountEq,")
rep("""art('relSlot', 'rel', 'Reliques', nRel ? `<span class="rmini">${S.relEq.filter(Boolean).slice(0, 4).map(id => relSp(id)).join('')}</span><span class="lv">${nRel}/6</span>` : '<i class="wplus">+</i>', nRel > 0, '#ffc23a')""",
    """art('relSlot', 'rel', 'Monture', mk ? `<canvas class="mmini" data-mnt="${mk}" width="96" height="84"></canvas><span class="lv">Nv ${S.mounts[mk]}</span>` : '<i class="wplus">+</i>', !!mk, mk ? SETS[MNT[mk].set].c : '')""")
rep("""<button type="button" class="slot art lockd" data-soon="Monture"><i class="flk">${IC.lock}</i><span class="nm">Monture</span></button>""", """<button type="button" class="slot art lockd" data-soon="Artefact mystère"><i class="flk">${IC.lock}</i><span class="nm">???</span></button>""")
rep("bind('relSlot', relSheet);", "bind('relSlot', mountSheet); mntIcons($('panel'));")
rep("rel: [26, 'Reliques']", "rel: [26, 'Montures']")
rep("  rel: [null, 'Invoque des <b>reliques</b> avec les Sceaux des donjons, puis place-les sur l\\'autel : 6 emplacements et des bonus de set.', () => relSheet()],",
    "  rel: [null, 'Débloque des <b>montures</b> avec les Sceaux des donjons de set : chacune donne un bonus et réveille les pouvoirs de son set.', () => mountSheet()],")
rep("function drawSideHero(time, anim) { const h = B.hero, SA = ASSETS.side && ASSETS.side[curForm()];", "function drawSideHero(time, anim) { if (!B.mntIn && typeof mountDraw === 'function' && mountDraw(time, anim)) return; const h = B.hero, SA = ASSETS.side && ASSETS.side[curForm()];")
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
.mtop{display:flex;align-items:center;gap:10px}.mtop .mic{width:72px;height:63px;border-radius:12px;background:radial-gradient(#3a1a20,#0c0507);border:2px solid var(--sc);flex:none}
.mtop b{display:block;font:400 16px var(--n);color:#fff}.mtop small{font:700 11px var(--b);color:#c8b098}.mtop em{margin-left:auto;font:800 10px var(--b);font-style:normal;color:#000;background:var(--sc);border-radius:8px;padding:2px 7px}
.mst{margin:8px 0 4px;font:700 12px var(--b);color:#d8c0b0}.mst b{color:var(--sc)}
.mset small{font:800 10px var(--b);letter-spacing:.08em;text-transform:uppercase;color:var(--sc)}.mset p{margin:3px 0;font:700 11px/1.3 var(--b);color:#7a6a60}.mset p.on{color:#f0e0d0}.mset p i{font-style:normal;display:inline-block;min-width:38px;color:var(--sc);font-weight:900}
.mbt{display:flex;gap:6px;margin-top:8px}.mbt .btn{flex:1}
#eqg .mmini{width:88%;height:auto;max-height:66%}
''', 1)
open(P, 'w').write(s); print('p34 montures ok')
