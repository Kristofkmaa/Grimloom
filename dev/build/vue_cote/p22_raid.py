# p22 : raid de l'Archidémon refait : planche HD (ASSETS.DEMHD.raid_arch), salle du trône (ASSETS.raidBg), illustration de la carte (ASSETS.raidArt)
#  il entre en rage (rugit, ailes déployées) à chaque palier de dégâts franchi
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p22 raid' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

# illustration de la carte du raid
i = s.index('const DUNART = {'); j = s.index('\n', i)
s = s[:j + 1] + "if (ASSETS.raidArt) DUNART.raid = ASSETS.raidArt; // p22 raid\n" + s[j + 1:]
# le boss
rep("spawnEnemy('beast4', 0, 0.3, st, true, 'void'); B.en[0].raid = 1;",
    "spawnEnemy(ASSETS.DEM.raid_arch ? 'raid_arch' : 'beast4', 0, 0.3, st, true, ASSETS.DEM.raid_arch ? null : 'void'); B.en[0].raid = 1; B.en[0].tierN = 0;")
# rage à chaque palier
rep("e.z += e.kz; e.kz *= 0.8; if (e.raid) { e.z = 0.3; e.X = 0; e.kz = 0; }",
    "e.z += e.kz; e.kz *= 0.8; if (e.raid) { e.z = 0.3; e.X = 0; e.kz = 0; const tN = raidTier(B.waveDmg); if (tN > (e.tierN || 0)) { e.tierN = tN; if (ASSETS.DEM[e.key].anims.rage_S) { e.aName = 'rage'; e.aT = 0; e.aDur = 1.1; e.hitDone = 1; e.cd = Math.max(e.cd, 1.3); } B.shake = Math.max(B.shake, 7); B.banner = { a: `Palier ${tN}`, b: 'L\\'Archidémon enrage !', t: 1.4 }; } }")
# le Chevalier peut frapper l'Archidémon (il se tient un peu au-delà de la portée de l'épée)
rep("inMelee = () => B.en.some(e => !e.dead && e.spawn <= 0 && e.z < MELEE);", "inMelee = () => B.en.some(e => !e.dead && e.spawn <= 0 && (e.z < MELEE || e.raid));")
# décor : la salle du trône, le trône derrière le boss, sans teinte de biome
rep("function drawSideBg(VH) { const top = -OFFY;",
    """const RBG = new Image(); if (ASSETS.raidBg) RBG.src = ASSETS.raidBg.src;
function drawSideBg(VH) { const top = -OFFY;
  if (B.dun && B.dun.raid && RBG.complete && RBG.naturalWidth) { const s3 = VH / RBG.naturalHeight, w = RBG.naturalWidth * s3, x0 = clamp(sx(0, 0.3) + 40 - ASSETS.raidBg.tx * s3, BW - w, 0); ctx.imageSmoothingEnabled = true; ctx.drawImage(RBG, x0, top, w, VH); const gd = ctx.createLinearGradient(0, top, 0, top + VH); gd.addColorStop(0, 'rgba(8,2,6,.55)'); gd.addColorStop(0.62, 'rgba(8,2,6,.42)'); gd.addColorStop(1, 'rgba(8,2,6,.2)'); ctx.fillStyle = gd; ctx.fillRect(0, top, BW, VH); return; }""")
s = s.replace('<style id="sv">', '<style id="sv">/* p22 raid */', 1)
open(P, 'w').write(s); print('p22 raid ok')
