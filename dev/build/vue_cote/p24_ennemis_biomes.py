# p24 : nouveaux ennemis HD par biome (planches build_enemy_hd.py, clés bN_*) : remplacent les anciens démons recolorés
#  un biome bascule quand toutes ses planches sont là ; les démons HD ne sont plus recolorés (le biome garde son effet de jeu)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p24 ennemis biomes' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("const bossOf = ch =>", r"""const BHD = { // p24 ennemis biomes : index du biome -> monstres HD
  1: { pool: ['b2_escargot', 'b2_escargot', 'b2_cercueil', 'b2_cercueil', 'b2_molosse', 'b2_champi', 'b2_sonneur'], elites: ['b2_gardien', 'b2_moine'], boss: [['b2_reine', 'La Reine Mycélienne'], ['b2_colosse', 'Le Colosse d\'ossuaire']], ranged: ['b2_champi', 'b2_sonneur', 'b2_moine'] },
};
for (const i in BHD) { const H = BHD[i], all = [...H.pool, ...H.elites, ...H.boss.map(b => b[0])]; if (all.every(k => ASSETS.DEM[k])) { Object.assign(BMOBS[i], { pool: H.pool, elites: H.elites, boss: H.boss }); } }
const bossOf = ch =>""")
rep("const RANGED = {", "const RANGED = { b2_champi: 1, b2_sonneur: 1, b2_moine: 1,")
rep("function demImg(key, v) { const im = IMG['D_' + key]; if (!v || !VARS[v]) return im;",
    "function demImg(key, v) { const im = IMG['D_' + key]; if (!v || !VARS[v] || (ASSETS.DEM[key] && ASSETS.DEM[key].hd)) return im;")
s = s.replace('<style id="sv">', '<style id="sv">/* p24 ennemis biomes */', 1)
open(P, 'w').write(s); print('p24 ennemis biomes ok')
