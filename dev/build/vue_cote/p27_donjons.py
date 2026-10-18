# p27 : chaque donjon a son boss nommé (le boss HD de son biome quand il existe), une intro de boss et une ambiance de couleur propre
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p27 donjons' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("  if (boss) { const st = enemyStats(n, true); st.hp *= 0.8; spawnEnemy(pick(['beast1', 'beast2', 'beast3', 'beast4', 'beast5']), 0, 1.45, st, true); }",
r"""  if (boss) { const st = enemyStats(n, true); st.hp *= 0.8; const M = BMOBS[B.bi % BMOBS.length], bk = M.boss[D.lv % M.boss.length][0], key = bk === 'p_idle' ? 'spawn1' : bk; spawnEnemy(ASSETS.DEM[key] ? bk : pick(['beast1', 'beast2', 'beast3', 'beast4', 'beast5']), 0, 1.45, st, true); bossIntro(DBOSS[D.k] || 'Le Gardien', `${dunName(D.k)} · Niveau ${D.lv}`); }""")
rep("function startDunWave() {", r"""const DBOSS = { sang: 'Le Seigneur de sang', os: 'Le Gardien de l\'Ossuaire', braise: 'Le Maître-forgeron', givre: 'La Sentinelle gelée', or: 'Le Roi des trésors', xp: 'Le Dévoreur d\'âmes', eclats: 'La Reine de cristal', ham: 'Le Voleur de clés', pages: 'Le Bibliothécaire maudit' }; // p27 donjons
const DCOL = { sang: '#ff2040', os: '#d8c890', braise: '#ff7a20', givre: '#8ad8ff', or: '#ffc23a', xp: '#7aff9a', eclats: '#b48aff', ham: '#e8dcc8', pages: '#ff9a6a' };
function startDunWave() {""")
# ambiance : halo coloré propre au donjon par-dessus le décor du biome
rep("\n  const bi = BIOMES.indexOf(biome()), BI =", "\n  const dunC = B.dun && !B.dun.raid && DCOL[B.dun.k];\n  const bi = BIOMES.indexOf(biome()), BI =")
rep("  for (let x = -off; x < BW; x += w) ctx.drawImage(BI, Math.floor(x), top, Math.ceil(w) + 1, VH);\n",
    "  for (let x = -off; x < BW; x += w) ctx.drawImage(BI, Math.floor(x), top, Math.ceil(w) + 1, VH);\n  if (dunC) { const g = ctx.createRadialGradient(BW * 0.62, YF - 60, 20, BW * 0.62, YF - 60, BW * 0.9); g.addColorStop(0, dunC + '38'); g.addColorStop(1, 'rgba(6,2,8,.55)'); ctx.fillStyle = g; ctx.fillRect(0, top, BW, VH); }\n")
s = s.replace('<style id="sv">', '<style id="sv">/* p27 donjons */', 1)
open(P, 'w').write(s); print('p27 donjons ok')
