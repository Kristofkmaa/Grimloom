# p35 : les montures deviennent des GARDIENS volants (ils suivent le héros en vol, ne le modifient pas)
#  mêmes clés et mêmes Sceaux que p34 ; un gardien équipé attaque toutes les 5 s ; image : ASSETS.PET[clé] (planche 4×1 en vol) quand elle existe
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p35 gardiens' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const MKS = Object.keys(MNT),", r"""Object.assign(MNT.chopper, { n: 'Crâne-hélice', ic: 'skull', d: 'Un crâne qui vole grâce à une hélice en os bricolée' }); // p35 gardiens
Object.assign(MNT.cercueil, { n: 'Lanterne hantée', ic: 'sun', d: 'Une vieille lanterne où loge un petit fantôme grincheux' });
Object.assign(MNT.coq, { n: 'Hibou squelette', ic: 'wind', d: 'Un hibou d\'os aux grands yeux lumineux, très sérieux' });
Object.assign(MNT.escargot, { n: 'Raie des brumes', ic: 'drop', d: 'Une raie manta qui nage dans l\'air, lente et paisible' });
Object.assign(MNT.destrier_rouge, { n: 'Dragonnet écarlate', ic: 'flame', d: 'Un petit dragon rouge très fier de lui · se paie avec tous tes Sceaux' });
Object.assign(MNT.destrier_os, { n: 'Dragonnet d\'os', ic: 'snow', d: 'Un petit dragon squelette aux flammes bleues · se paie avec tous tes Sceaux' });
const MKS = Object.keys(MNT),""")
# attaque du gardien
rep("  if (fighting) { B.famTs = B.famTs || [];", """  if (fighting && S.mountEq && S.mounts[S.mountEq]) { B.gdT = (B.gdT === undefined ? 1.5 : B.gdT) - dt; if (B.gdT <= 0) { B.gdT = 5; const L = alive(); if (L.length) { const t = L.reduce((a, b) => b.z < a.z ? b : a), lv = S.mounts[S.mountEq]; B.shots.push({ X: 0, z: (GDPOS[0] - 46) / ZW, h: -GDPOS[1] + 6, tg: t, dmg: st.atk * (1.2 + 0.08 * lv), crit: false, t: 0, fx: 'arc', prj: 1, solid: 0, wr: -1, comp: 'fam' }); } } }
  if (fighting) { B.famTs = B.famTs || [];""")
rep("const FAMPOS = [", "const GDPOS = [-78, -150]; // p35 : position du gardien\nconst FAMPOS = [")
# dessin du gardien (quand sa planche existe)
rep("  famSync().forEach((id, i) => L.push({", """  { const k = S.mountEq, A = k && ASSETS.PET && ASSETS.PET[k]; if (A && S.mounts[k]) L.push({ z: 0.04, y: YF - 2, f: () => { const im = PETI[k]; if (!im || !im.complete) return; const bob = Math.sin(time * 2) * 6, x = CX + GDPOS[0], y = YF + GDPOS[1] + bob, sc = 70 / A.ch, f = Math.floor(time * 8) % (A.n || 4); ctx.save(); ctx.imageSmoothingEnabled = true; ctx.drawImage(im, f * A.cw, 0, A.cw, A.ch, x - A.cw * sc / 2, y - A.ch * sc / 2, A.cw * sc, A.ch * sc); ctx.restore(); } }); }
  famSync().forEach((id, i) => L.push({""")
rep("const MNTI = {};", "const PETI = {}; for (const k in (ASSETS.PET || {})) PETI[k] = lazyImg(ASSETS.PET[k].src);\nconst MNTI = {};")
# textes
rep("<canvas class=\"mic\" data-mnt=\"${k}\" width=\"96\" height=\"84\"></canvas>", "<i class=\"mic\" style=\"display:grid;place-items:center;color:var(--sc)\">${IC[M.ic]}</i>")
rep("""`<canvas class="mmini" data-mnt="${mk}" width="96" height="84"></canvas><span class="lv">""", """`<i class="mmini" style="display:grid;place-items:center;color:${SETS[MNT[mk].set].c}">${IC[MNT[mk].ic]}</i><span class="lv">""")
s = s.replace("<h3>Montures <button", "<h3>Gardiens <button").replace("Débloque et améliore les montures avec les <b>Sceaux</b> des donjons de set. Une seule montée à la fois : elle donne son bonus et réveille les pouvoirs de son set aux niveaux 1, 10 et 20.", "Débloque et améliore les gardiens avec les <b>Sceaux</b> des donjons de set. Un seul gardien t'accompagne : il vole près de toi, attaque toutes les 5 s, donne son bonus et réveille les pouvoirs de son set aux niveaux 1, 10 et 20.")
s = s.replace("'Descendre' : 'Monter'", "'Renvoyer' : 'Choisir'").replace("<em>Montée</em>", "<em>Avec toi</em>")
rep("art('relSlot', 'rel', 'Monture',", "art('relSlot', 'rel', 'Gardien',")
s = s.replace("rel: [26, 'Montures']", "rel: [26, 'Gardiens']").replace("Débloque des <b>montures</b> avec", "Débloque des <b>gardiens</b> volants avec").replace("'Débloquer et améliorer les montures (case Monture).", "'Débloquer et améliorer les gardiens (case Gardien).").replace("améliorer les <b>montures</b> (Sang, Os, Braises, Givre). Chaque monture réveille", "améliorer les <b>gardiens</b> (Sang, Os, Braises, Givre). Chaque gardien réveille")
s = s.replace("B2('allmnt', 'Toutes les montures') + B2('mnt20', 'Montures niveau 20')", "B2('allmnt', 'Tous les gardiens') + B2('mnt20', 'Gardiens niveau 20')")
s = s.replace("débloqué !`", "débloqué !`")
s = s.replace('<style id="sv">', '<style id="sv">/* p35 gardiens */\n.mtop .mic svg{width:30px;height:30px}#eqg .mmini svg{width:30px;height:30px}\n', 1)
open(P, 'w').write(s); print('p35 gardiens ok')
