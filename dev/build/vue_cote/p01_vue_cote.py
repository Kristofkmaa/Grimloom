# patch v18 : vue de côté façon Legend of Mushroom
#  - combat de côté : héros fixe à gauche, démons qui arrivent de la droite, décor extérieur qui défile
#  - disposition Mushroom : combat ~44 % + HUD en surimpression, barre de sorts ronde, grille 12 équipements + 6 artefacts
#  - coffre à clés à la place de la forge (marteaux -> clés, anciennes clés de donjon -> tickets)
# usage : python3 dev/build/patch_v18.py [src.html]   (modifie le fichier en place)
import re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read()
assert 'patch v18' not in s, 'déjà appliqué'

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (n, old[:120])
    s = s.replace(old, new)

def rex(pat, new, cnt=1):
    global s
    L = re.findall(pat, s, flags=re.S)
    assert len(L) == cnt, (len(L), pat[:120])
    s = re.sub(pat, lambda m: new, s, flags=re.S)

# ---------- images de la maquette (décor, Écuyer de profil, Diablotin de profil, coffre) ----------
M = open(D + 'maquette/maquette_vue_cote.html').read()
IMGS = {k: re.search(r'"%s": "(data:[a-z/]+;base64,[A-Za-z0-9+/=]+)"' % k, M).group(1) for k in ['bg', 'hero', 'walk', 'imp']}
CHEST = re.search(r"CI\.src='(data:image/png;base64,[A-Za-z0-9+/=]+)'", M).group(1)

KEY_SVG = '<svg class="ico" viewBox="0 0 24 24"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z" fill="#f0c04a" stroke="#6a3a08" stroke-width=".8"/></svg>'
KEY_I = '<svg class="i" viewBox="0 0 24 24"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z" fill="#f0c04a"/></svg>'

# =====================================================================
# A. moteur de combat : projection de côté
# =====================================================================
rep('const BW = 360, BH = 420, CX = 180, YF = 372,', 'const BW = 360, BH = 420, CX = 104, YF = 372,')
rep('const sOf = z => 1 / (1 + K * z), py = z => YH + (YF - YH) * (sOf(z) - S1) / (1 - S1), sx = (X, z) => CX + X * HW * sOf(z);',
    '// vue de côté : z = distance devant le héros (vers la droite), X = petit décalage de rangée (haut/bas)\nconst ZW = 180, LANE = 80, sOf = z => 0.62, py = z => YF, sx = (X, z) => CX + 30 + z * ZW;')
rex(r"function fit\(\) \{ appScale\(\);.*?\n\}\naddEventListener\('resize', fit\);", r'''function fit() { appScale(); // combat en haut (~44 % de l'écran), le reste pour les sorts, l'équipement et le coffre
  const wrap = $('stageWrap'), w = wrap.clientWidth || 360, H0 = $('app').clientHeight, h = Math.round(Math.max(250, Math.min(H0 * 0.44, w * 1.05)));
  wrap.style.height = h + 'px'; const dpr = Math.min(2, devicePixelRatio || 1); cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); CAMZ = 1; OFFY = 0; eqSize();
}
function eqSize() { // taille des cases : 6 colonnes en largeur, 3 rangées + le coffre en hauteur
  const a = $('app'); if (!a) return; const W = a.clientWidth, H0 = a.clientHeight, st = $('stageWrap').offsetHeight || H0 * 0.44, nav = $('nav').offsetHeight || 62, room = H0 - st - 56 - nav - 128 - 16;
  const ss = Math.max(42, Math.min(64, Math.floor((W - 16 - 5 * 6 - 14) / 6), Math.floor((room - 12) / 3)));
  document.documentElement.style.setProperty('--ss', ss + 'px'); }
addEventListener('resize', fit);''')
rep("const k = cv.width / BW * CAMZ, OX = CX - BW / 2 / CAMZ; ctx.setTransform(k, 0, 0, k, -OX * k, OFFY * k); ctx.fillStyle = '#000'; ctx.fillRect(0, -40, BW, BH + 80); ctx.imageSmoothingEnabled = false;",
    "const k = cv.width / BW, VH = cv.height / k; OFFY = VH * 0.845 - YF; ctx.setTransform(k, 0, 0, k, 0, OFFY * k); ctx.fillStyle = '#000'; ctx.fillRect(0, -OFFY - 2, BW, VH + 4); ctx.imageSmoothingEnabled = false;")
rep("  if (!IMG.tiles.complete) return; renderFloor(B.scene, biome(), B.scroll);\n", "")
rex(r"  const BGI = bgPaint\(\); if \(BGI && BGI\.complete\) \{.*?\} else ctx\.drawImage\(FLOOR, 0, 0, BW, BH\);", "  const BGI = 1; drawSideBg(VH);")
rep("  for (const e of B.en) L.push({ z: e.z, f: () => drawEnemy(e, time) });\n  L.push({ z: 0, f: () => drawHero(time) });\n  if (!B.walk && !B.dun) L.push({ z: -0.001, f: drawHeroHp });",
    "  for (const e of B.en) L.push({ z: e.z, y: YF + e.X * LANE, f: () => drawEnemy(e, time) });\n  L.push({ z: 0, y: YF, f: () => drawHero(time) });\n  if (!B.walk && !B.dun) L.push({ z: -0.001, y: YF + 60, f: drawHeroHp });")
rep("L.push({ z: 0.05, f: () => { const F = FAM[S.fam], im = IMG.fam_sp, bob = Math.sin(time * 2.4) * 5, x = CX + 54, y = YF - 86 + bob, sz = 58 + F.r * 4;",
    "L.push({ z: 0.05, y: YF - 1, f: () => { const F = FAM[S.fam], im = IMG.fam_sp, bob = Math.sin(time * 2.4) * 5, x = CX - 32, y = YF - 76 + bob, sz = 48 + F.r * 3;")
rep("  L.sort((a, b) => b.z - a.z).forEach(o => o.f());", "  L.sort((a, b) => ((a.y === undefined ? YF : a.y) - (b.y === undefined ? YF : b.y)) || (b.z - a.z)).forEach(o => o.f());")
rep("  drawLight(time);\n", "  drawSideLight(VH);\n")
rep("BW / 2, 205)", "BW / 2, YF - 150)", 2)
rep("BW / 2, 228)", "BW / 2, YF - 128)", 2)
rep("h: 40, tg: t", "h: 64, tg: t")
rep("X: (i ? -1 : 1) * 0.06, h: 34", "X: (i ? -1 : 1) * 0.06, h: 56")
rep("s.h += (26 - s.h) * dt * 3", "s.h += (40 - s.h) * dt * 3")
rep("B.es.push({ X: e.X, z: e.z, h: 30,", "B.es.push({ X: e.X, z: e.z, h: 50,")
rep("const s = sOf(e.z), x = sx(e.X, e.z), y = py(e.z), A = ASSETS.DEM[e.key], sc = (e.raid ? 2.7 : e.boss ? 2.3 : e.elite ? 1.75 : 1.55) * s * (A.k || 1);",
    "const s = 1, x = sx(e.X, e.z), y = py(e.z) + e.X * LANE, A = ASSETS.DEM[e.key], sc = (e.raid ? 2.2 : e.boss ? 1.9 : e.elite ? 1.4 : 1.2) * s * (A.k || 1);")
rep("const ex = e => sx(e.X, e.z), ey = e => py(e.z) - 24 * sOf(e.z);", "const ex = e => sx(e.X, e.z), ey = e => py(e.z) + e.X * LANE - 24 * sOf(e.z);")
rep("  if (from < 0.5) spawnEnemy(img, rand(-0.12, 0.12), B.scene === 'corridor' ? rand(1.6, 2.0) : 1.02, st); else { const side = from < 0.75 ? -1 : 1; spawnEnemy(img, side * 1.0, rand(0.5, 0.6), st); }",
    "  spawnEnemy(img, rand(-0.12, 0.12), rand(1.75, 2.15), st); // tous arrivent de la droite, hors de l'écran")
rep("spawnEnemy(bo.key, 0, 0.93, st, true);", "spawnEnemy(bo.key, 0, 1.45, st, true);")
rep("'beast5']), 0, 0.93, st, true);", "'beast5']), 0, 1.45, st, true);")
rep("const tx = e.ranged ? e.X * 0.6 : 0;", "const tx = e.X;")
rep("{ const dx = CX - sx(e.X, e.z), dy = Math.max(1, YF - py(e.z)), r = Math.abs(dx) / dy; e.dir = r < 0.42 ? 'S' : (dx > 0 ? (r < 1.7 ? 'SE' : 'E') : (r < 1.7 ? 'SW' : 'W')); }", "e.dir = 'S';")
rep("e.cd -= dt; e.hitT -= dt; if (e.v && e.v !== 'bone'", "e.X = clamp(e.X, -0.15, 0.15); e.cd -= dt; e.hitT -= dt; if (e.v && e.v !== 'bone'")
rep("B.shots.push({ X: 0.2, z: 0.04, h: 66, tg: t,", "B.shots.push({ X: 0, z: -0.34, h: 122, tg: t,")
rep("const sceneFor = () => PS() === 10 && !S.farm ? 'arena' : 'corridor';", "const sceneFor = () => 'corridor'; // vue de côté : plus d'arène, le boss attend qu'on le défie")
rep(": { t: 0, dur: change ? 2.0 : 1.5, d0: B.scroll, dist: SEG, change };", ": { t: 0, dur: 1.1, d0: B.scroll, dist: SEG, change }; // avance courte et rapide")
# boss : on farme la dernière vague tant qu'on n'a pas touché « Défier le boss »
rep("if (sc === 'corridor' && (prev === 'arena' || !B.started) && S.s === 1 && !S.farm)", "if ((B.lastC !== S.c || !B.started) && S.s === 1 && !S.farm)")
rep("  queueBiome(B.bi); if (PS() >= 8) queueBiome(B.bi + 1);", "  B.lastC = S.c; queueBiome(B.bi); if (PS() >= 8) queueBiome(B.bi + 1);")
rep("const n = stageIndex(), boss = PS() === 10 && !S.farm, ch = PC();", "const n = stageIndex(), boss = PS() === 10 && !S.farm && !!B.bossGo, ch = PC();")
rep("const boss = B.wave.boss; S.pages += boss ? 10 : 1;", "const boss = B.wave.boss; if (!boss && PS() === 10 && !S.farm) { S.pages += 1; S.st.stage++; save(); ui(); B.pend = 0.9; B.pendFn = beginWalk; return; } S.pages += boss ? 10 : 1;")
rep("else if (boss) { S.c++; S.s = 1;", "else if (boss) { B.bossGo = 0; S.c++; S.s = 1;")
rep("function heroDied() { if (B.dun) {", "function heroDied() { B.bossGo = 0; if (B.dun) {")
rep("if (!S.farm || B.dun) return; S.farm = false;", "if (B.dun) return; if (!S.farm && (PS() !== 10 || B.bossGo)) return; S.farm = false; if (S.s === 10) B.bossGo = 1;")
rep("$('challengeBtn').hidden = !S.farm || !!B.dun; $('challengeBtn').innerHTML = `${IC.sword} Défier ${label(S.c, S.s)}<small>${S.s === 10 ? 'Boss' : ''}</small>`;",
    "{ const bossReady = !S.farm && S.s === 10 && !B.bossGo; $('challengeBtn').hidden = !(S.farm || bossReady) || !!B.dun; const h = bossReady ? `${IC.skull} Défier le boss` : `${IC.sword} Défier ${label(S.c, S.s)}<small>${S.s === 10 ? 'Boss' : ''}</small>`; if ($('challengeBtn').innerHTML !== h) $('challengeBtn').innerHTML = h; }")
rep("'+' + hg + ' 🔨'", "'+' + hg + ' 🗝️'")
rep("function hamNewKill(e) { if (B.dun ||", "function hamNewKill(e) { if (PS() === 10 && !(B.wave && B.wave.boss)) return 0; if (B.dun ||")
rep("if ((B.ult || 0) >= 100 && B.ultFullT && B.t - B.ultFullT > 3 && !B.dun) castUlt();", "if ((B.ult || 0) >= 100 && B.ultFullT && S.ultAuto !== false && B.t - B.ultFullT > 0.4) castUlt(); // bouton AUTO de la barre de sorts")
rep("ctx.ellipse(CX, YF - 2, 70 * p + 10, (70 * p + 10) * 0.32, 0, 0, TAU);", "ctx.ellipse(CX, YF - 2, 46 * p + 8, (46 * p + 8) * 0.3, 0, 0, TAU);")
rep("ctx.ellipse(CX, YF - 2, 80, 26, 0, 0, TAU);", "ctx.ellipse(CX, YF - 2, 54, 16, 0, 0, TAU);")
# héros de profil (Écuyer) : attente, attaque, coup reçu, marche courte
rep("  if (ga >= 4) { ctx.globalCompositeOperation = 'lighter'; heroSil(H.key, key, fr, CX, YF, sc, gc, 0.55 + Math.sin(time * 4) * 0.15, 1.6); ctx.globalCompositeOperation = 'source-over'; }\n  sprH(H.key, key, fr, CX, YF + bobY, sc);\n  { const w = wEq(),",
    "  const SV = sideHero(); if (ga >= 4 && !SV) { ctx.globalCompositeOperation = 'lighter'; heroSil(H.key, key, fr, CX, YF, sc, gc, 0.55 + Math.sin(time * 4) * 0.15, 1.6); ctx.globalCompositeOperation = 'source-over'; }\n  if (SV) drawSideHero(time, anim); else sprH(H.key, key, fr, CX, YF + bobY, sc);\n  { const w = SV ? null : wEq(),")
SIDE_FN = r'''// ================= vue de côté (façon Legend of Mushroom) =================
const SBG = new Image(); SBG.src = '__BG__'; // cimetière à la lune rouge, bande raccordable
const SHI = new Image(); SHI.src = '__HERO__'; const SHW = new Image(); SHW.src = '__WALK__'; // Écuyer de profil (109 px par case)
const sideHero = () => S.cls === 'knight' && S.form === 'ecuyer';
function drawSideBg(VH) { const top = -OFFY; if (!SBG.complete || !SBG.naturalWidth) { ctx.fillStyle = '#1a1028'; ctx.fillRect(0, top, BW, VH); return; }
  const s2 = VH / SBG.naturalHeight, w = SBG.naturalWidth * s2, off = ((B.scroll * ZW) % w + w) % w; ctx.imageSmoothingEnabled = false;
  for (let x = -off; x < BW; x += w) ctx.drawImage(SBG, Math.floor(x), top, Math.ceil(w) + 1, VH);
  const bi = BIOMES.indexOf(biome()); if (bi > 0) { ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = BIOMES[bi].tint; ctx.fillRect(0, top, BW, VH); ctx.globalCompositeOperation = 'source-over'; } }
function drawSideLight(VH) { const top = -OFFY, g = ctx.createLinearGradient(0, top, 0, top + VH); g.addColorStop(0, 'rgba(6,2,8,.62)'); g.addColorStop(0.3, 'rgba(6,2,8,0)'); g.addColorStop(0.93, 'rgba(6,2,8,0)'); g.addColorStop(1, 'rgba(6,2,8,.5)'); ctx.fillStyle = g; ctx.fillRect(0, top, BW, VH); }
function drawSideHero(time, anim) { const h = B.hero, C = 109, sc = 0.7; let im = SHI, row = 2, f = Math.floor(time * 2.5) % 2 ? 2 : 0;
  if (anim === 'course') { im = SHW; row = 0; f = Math.floor(time * 16) % 8; }
  else if (anim === 'tir') { row = 1; f = clamp(Math.floor((1 - Math.max(0, h.shootT) / 0.3) * 4), 0, 3); }
  else if (anim === 'touche') { row = 2; f = 1; }
  const w = wEq(); if (w && WING_IMG.complete) { const fw = [0, 1, 2, 3, 2, 1][Math.floor(time * (B.walk ? 9 : 5)) % 6], ws = 0.5; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.translate(CX - 8, YF - 70); ctx.drawImage(WING_IMG, fw * 168, WINGS[w].row * 168, 168, 168, -84 * ws, -48 * ws, 168 * ws, 168 * ws); ctx.restore(); }
  if (!im.complete) return; ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(im, f * C, row * C, C, C, Math.round(CX - 50 * sc), Math.round(YF - 100 * sc), Math.round(C * sc), Math.round(C * sc)); ctx.restore(); }
'''.replace('__BG__', IMGS['bg']).replace('__HERO__', IMGS['hero']).replace('__WALK__', IMGS['walk'])
rep("function drawEnemy(e, time) {", SIDE_FN + "function drawEnemy(e, time) {")
# Diablotin d'os redessiné de profil (il regarde vers la gauche)
rex(r'ASSETS\.DEM\.n_imp = \{[^\n]*?\}; // Diablotin d\'os \(ChatGPT, à toi\)',
    'ASSETS.DEM.n_imp = {"cw": 109, "ch": 109, "foot": 9, "bh": 82, "k": 0.42, "spd": 0.6, "ax": 56, "side": 1, "anims": {"walk_S": [0, 4], "atk_S": [1, 4], "hit_S": [2, 1], "die_S": [2, 4], "idle_S": [0, 1]}, "src": "%s"}; // Diablotin d\'os de profil (ChatGPT, à toi)' % IMGS['imp'])
# l'ancien panneau rétractable n'existe plus
rep("function eqSet(min) { if (EQA ||", "function eqSet(min) { return; if (EQA ||")
rep("t.hidden = tab !== 'forge' || document.body.classList.contains('full');", "t.hidden = true;")
rep("const eqTogPlace = () => { document.body.classList.toggle('eqmin', !!S.eqMin);", "const eqTogPlace = () => { S.eqMin = false; document.body.classList.toggle('eqmin', false);")

# =====================================================================
# B. disposition façon Mushroom
# =====================================================================
# --- 12 emplacements : 3 nouvelles pièces (icônes provisoires en attendant les vraies) ---
rep("  { id: 'amulette', n: 'Amulette', ic: 15, main: [['cdmg', 8], ['pv', 15]] },\n];",
    "  { id: 'amulette', n: 'Amulette', ic: 15, main: [['cdmg', 8], ['pv', 15]] },\n  { id: 'epaulettes', n: 'Épaulettes', ic: 10, main: [['pv', 22], ['def', 1]] },\n  { id: 'ceinture', n: 'Ceinture', ic: 11, main: [['pv', 18], ['def', 1.5]] },\n  { id: 'bracelet', n: 'Bracelet', ic: 14, main: [['atk', 2], ['crit', 0.8]] },\n];")
rep("const $ = id => document.getElementById(id);",
    "const $ = id => document.getElementById(id);\nif (ASSETS.icons && ASSETS.icons.pool) { const P = ASSETS.icons.pool; P.epaulettes = P.epaulettes || P.plastron; P.ceinture = P.ceinture || P.jambieres; P.bracelet = P.bracelet || P.anneau; } // icônes provisoires des nouvelles pièces")

# --- HTML : HUD clés, barre de sorts, quête dans le combat, coffre ---
rep('<div class="res"><svg class="ico" viewBox="0 0 24 24"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z" fill="#a8622a"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z" fill="#d6d8e6"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-3V6.5H8z" fill="#fff" opacity=".5"/></svg><b id="ham">0</b></div>',
    '<div class="res">' + KEY_SVG + '<b id="ham">0</b></div>')
m = re.search(r'<button id="ultBtn".*?</button><div id="spellHud2"></div>', s, flags=re.S); assert m
ULTB = m.group(0); s = s.replace(ULTB, '')
ULTB = ULTB.replace('<div id="spellHud2"></div>', '')
m = re.search(r'  <button id="questBar" type="button">.*?</button>\n', s, flags=re.S); assert m
QB = m.group(0); s = s.replace(QB, '')
rep('  </div>\n  <div id="botBar">',
    '  ' + QB.strip() + '\n  </div>\n  <div id="skBar"><button type="button" id="autoU" aria-label="Ultime automatique"><b>AUTO</b><small>ON</small></button><div id="spellHud2"></div>' + ULTB + '</div>\n  <div id="botBar">')
rex(r'  <div id="dock">.*?\n  </div>\n  <nav id="nav">', '''  <div id="dock">
    <span class="shardp" id="shardP" title="Éclats : recycle des objets, sert à les améliorer"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 5 9l7 13 7-13zm0 3.2L16.4 9H7.6z"/></svg><b id="shardN">0</b></span>
    <button class="dk" id="forgeLv" type="button"><small>Coffre</small><b id="flv">1</b><small>niveau</small><i class="dot" id="fdot" hidden>!</i></button>
    <button id="forgeBtn" type="button" aria-label="Ouvrir le coffre"><i class="cglow"></i><canvas class="chest" width="304" height="344" aria-hidden="true"></canvas><span class="plq">''' + KEY_I + '''<b id="hamN">0</b></span></button>
    <button class="dk" id="bagBtn" type="button" aria-label="Ouverture auto"><small id="bagN">Auto</small></button>
    <button class="dk red" id="bossBtn" type="button" hidden></button>
  </div>
  <nav id="nav">''')

# --- page Équipement : grille 12 + 6 ---
FORGE_UI = r'''if (tab === 'forge') { // disposition Mushroom : 12 pièces à gauche, 6 artefacts à droite
    const GRID = ['arme', 'casque', 'epaulettes', 'plastron', 'gants', 'ceinture', 'jambieres', 'bottes', 'anneau', 'amulette', 'bracelet', null];
    const fam = S.fam && S.fams[S.fam], w = wEq(), nRel = S.relEq.filter(Boolean).length, nSp = S.slots.filter(Boolean).length;
    const art = (id, k, name, inner, on, rc) => !featOK(k) ? `<button type="button" id="${id}" class="slot art lockd" data-fk="${k}"><i class="flk">${IC.lock}</i><span class="nm">${name}</span><em class="stg">Étape ${stName(FEAT[k][0])}</em></button>` : `<button type="button" id="${id}" class="slot art ${on ? 'on' : 'empty'}" style="${on ? `--rc:${rc}` : ''}">${inner}<span class="nm">${name}</span></button>`;
    $('panel').innerHTML = `<div id="eqg"><div class="gl">${GRID.map(id => id ? slotHTML(SLOTS.find(q => q.id === id)) : `<button type="button" class="slot lockd" id="slot12"><i class="flk">${IC.lock}</i><span class="nm">${S.best >= 41 ? 'Bientôt' : 'Étape 5-1'}</span></button>`).join('')}</div><i class="sep"></i><div class="gr">${
      art('wingSlot', 'aile', 'Ailes', w ? `<canvas id="wingMini" width="84" height="54"></canvas><span class="lv">Nv ${wlv(w)}</span>` : '<i class="wplus">+</i>', !!w, w ? WINGS[w].c : '')}${
      art('famSlot', 'invoc', 'Familier', fam ? `<canvas id="famMini" width="64" height="64"></canvas><span class="lv">${famStar(S.fam)}★</span>` : '<i class="wplus">+</i>', !!fam, fam ? FRC[FAM[S.fam].r] : '')}${
      art('relSlot', 'rel', 'Reliques', nRel ? `<span class="rmini">${S.relEq.filter(Boolean).slice(0, 4).map(id => relSp(id)).join('')}</span><span class="lv">${nRel}/6</span>` : '<i class="wplus">+</i>', nRel > 0, '#ffc23a')}${
      art('spSlot', 'grim', 'Pouvoirs', nSp ? `<span class="spmini">${S.slots.filter(Boolean).slice(0, 3).map(id => spIcon(id, 16)).join('')}</span><span class="lv">${nSp}/${slotCount()}</span>` : '<i class="wplus">+</i>', nSp > 0, '#b48aff')}
      <button type="button" class="slot art lockd" data-soon="Monture"><i class="flk">${IC.lock}</i><span class="nm">Monture</span></button><button type="button" class="slot art lockd" data-soon="Artefact mystère"><i class="flk">${IC.lock}</i><span class="nm">???</span></button></div></div>`;
    const bind = (id, fn) => { const e = $(id); if (e && !e.dataset.fk) e.onclick = fn; }; bind('wingSlot', wingSheet); bind('famSlot', famSheet); bind('relSlot', relSheet); bind('spSlot', openSkills);
    document.querySelectorAll('#eqg [data-fk]').forEach(e => e.onclick = () => toast(featMsg(e.dataset.fk)));
    document.querySelectorAll('#eqg [data-soon]').forEach(e => e.onclick = () => toast(`${e.dataset.soon} : bientôt disponible`));
    $('slot12').onclick = () => toast(S.best >= 41 ? 'Nouvel emplacement : bientôt disponible' : 'Emplacement débloqué à l\'étape 5-1');
    { const c = $('famMini'); if (c && S.fam) { const g = c.getContext('2d'), im = IMG.fam_sp, F = FAM[S.fam]; const dr = () => { if (!im.complete) return setTimeout(dr, 100); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 64, 64); g.drawImage(im, F.i * 128, 0, 128, 128, 0, 0, 64, 64); }; dr(); } }
    { const c = $('wingMini'); if (c) { const w2 = wEq(), g = c.getContext('2d'); const draw = () => { if (!c.isConnected || !wEq()) return; g.clearRect(0, 0, 84, 54); if (WING_IMG.complete) { const f = [0, 1, 2, 3, 2, 1][Math.floor(performance.now() / 190) % 6]; g.imageSmoothingEnabled = false; g.drawImage(WING_IMG, f * 168, WINGS[w2].row * 168, 168, 108, 0, 0, 84, 54); } requestAnimationFrame(draw); }; draw(); } }
    document.querySelectorAll('#eqg [data-ic]').forEach(c => eqIcon(c, S.eq[c.dataset.ic], c.dataset.ic));
    document.querySelectorAll('#eqg [data-s]').forEach(el => el.onclick = () => { const it = S.eq[el.dataset.s]; if (it) showItem(it, null); else toast('Ouvre le coffre pour trouver : ' + SLOTS.find(x => x.id === el.dataset.s).n); });
    eqSize();
  } else if (tab === 'hero') {'''
rex(r"if \(tab === 'forge'\) \{\n    \$\('panel'\)\.innerHTML = `<div id=\"equip\" class=\"frame\">.*?\n  \} else if \(tab === 'hero'\) \{", FORGE_UI)
rep("{ const eb = $('eqBg'), on = tab === 'forge' && !document.body.classList.contains('full'); document.body.classList.toggle('eqmode', on); eb.hidden = !on; $('eqCols').hidden = !on; if (!on) $('eqCols').innerHTML = ''; }",
    "{ document.body.classList.remove('eqmode'); $('eqBg').hidden = true; $('eqCols').hidden = true; $('eqCols').innerHTML = ''; }")
# --- barre de sorts : 3 emplacements ronds (équipé / libre / verrouillé) ---
rex(r"function uiSpells\(\) \{.*?\n\}\nfunction uiCombat\(\)", r'''function uiSpells() {
  const n = slotCount(), el = $('spellHud2'), key = S.slots.slice(0, 3).map(id => id && S.spells[id] ? id : '').join(',') + '|' + n + '|' + featOK('grim');
  if (el.dataset.k !== key) { el.dataset.k = key; el.innerHTML = [0, 1, 2].map(i => { const id = S.slots[i]; if (i >= n || !featOK('grim')) return `<button type="button" class="sh2 lk" data-shl="${i}">${IC.lock}</button>`; if (!id || !S.spells[id]) return `<button type="button" class="sh2 em" data-she="1"><b>+</b></button>`; return `<button type="button" class="sh2" data-shs="${id}" style="--sc:${SPELLS[id].c}">${spIcon(id, 40)}<i class="cdm"></i><b class="cdt"></b></button>`; }).join('');
    el.querySelectorAll('[data-shl]').forEach(b => b.onclick = () => toast(!featOK('grim') ? featMsg('grim') : `Emplacement de pouvoir : chapitre ${b.dataset.shl === '1' ? 2 : 4}`));
    el.querySelectorAll('[data-she],[data-shs]').forEach(b => b.onclick = openSkills); }
  el.querySelectorAll('[data-shs]').forEach(d => { const id = d.dataset.shs, rem = B.cd && B.cd[id] !== undefined ? Math.max(0, B.cd[id]) : 0, cd = B.cd && B.cd[id] !== undefined ? rem / SPELLS[id].cd : 0.5; d.querySelector('.cdm').style.setProperty('--cd', (cd * 100).toFixed(0) + '%'); d.querySelector('.cdt').textContent = rem > 0.05 ? (rem >= 10 ? Math.ceil(rem) : rem.toFixed(1)) : ''; const fire = rem > SPELLS[id].cd - 0.35; if (fire !== d.classList.contains('cast')) d.classList.toggle('cast', fire); });
}
function uiCombat()''')
# --- bandeau d'étape et boutons ---
rep("$('stage').textContent = S.farm ? `FARM ${label(PC(), PS())}` : `CHAPITRE ${S.c} · ${S.s}/10`; $('biomeN').textContent = S.farm ? `${biome().n} · prochaine : ${label(S.c, S.s)}` : biome().n;",
    "$('stage').textContent = `${biome().n.replace(/^(Les |La |Le |L')/, '')} ${label(PC(), PS())}`; $('biomeN').textContent = S.farm ? `Repli · prochaine : ${label(S.c, S.s)}` : '';")
rep("$('flv').textContent = S.forge;", "$('flv').textContent = S.forge; { const e = $('shardN'); if (e) e.textContent = fmt(S.shards); const a = $('autoU'); if (a) { a.classList.toggle('off', S.ultAuto === false); a.querySelector('small').textContent = S.ultAuto === false ? 'OFF' : 'ON'; } }")
rep("$('ultBtn').onclick = castUlt;", "$('ultBtn').onclick = castUlt; $('autoU').onclick = () => { S.ultAuto = S.ultAuto === false; save(); uiTop(); toast(S.ultAuto ? 'Ultime automatique' : 'Ultime manuel : touche-le quand il est prêt'); };")

# =====================================================================
# C. le coffre remplace la forge
# =====================================================================
rex(r"const CHEST_IMG = new Image\(\); CHEST_IMG\.src = '[^']*';", "const CHEST_IMG = new Image(); CHEST_IMG.src = '%s'; // 6 images : cadenas, serrure, clé, entrouvert, ouvert, grand ouvert" % CHEST)
rex(r"let chestT = \[\], chestFr = 0;\n.*?\n\}\nlet zcT", r'''let chestT = [], chestFr = 1, chestGlow = 0, chestCol = '255,210,90', chestBusy = 0; const CW2 = 152, CH2 = 172;
const hexRgb = h => { const n = parseInt(h.slice(1), 16); return `${n >> 16 & 255},${n >> 8 & 255},${n & 255}`; };
function chestDraw() { const c = document.querySelector('#forgeBtn .chest'); if (!c || !c.offsetParent) return; const g = c.getContext('2d'); g.setTransform(2, 0, 0, 2, 0, 0); g.clearRect(0, 0, CW2, CH2);
  if (chestGlow > 0) { const gr = g.createRadialGradient(CW2 / 2, CH2 * 0.46, 4, CW2 / 2, CH2 * 0.46, CW2 * 0.49); gr.addColorStop(0, `rgba(${chestCol},${chestGlow})`); gr.addColorStop(1, `rgba(${chestCol},0)`); g.fillStyle = gr; g.fillRect(0, 0, CW2, CH2); }
  if (!CHEST_IMG.complete) return; g.imageSmoothingEnabled = false; const f = chestBusy ? chestFr : S.ham > 0 ? 1 : 0; g.drawImage(CHEST_IMG, f * CW2, 0, CW2, CH2, 0, 0, CW2, CH2);
  if (!chestBusy && S.ham > 0) { const p = (Math.sin(performance.now() / 400) + 1) / 2; g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.12 * p; g.drawImage(CHEST_IMG, f * CW2, 0, CW2, CH2, 0, 0, CW2, CH2); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; } }
(function chestLoop() { try { chestDraw(); } catch (e) { } requestAnimationFrame(chestLoop); })();
function chestOpen(r, cb, fast) { // la clé tourne, le couvercle s'ouvre, la lumière prend la couleur de la rareté
  fast = fast || autoBusy; const b = $('forgeBtn'); chestT.forEach(clearTimeout); chestT = []; chestBusy = 1; chestCol = hexRgb(RAR[r].c); const T = fast ? 0.55 : 1;
  const seq = [[2, 170], [3, 150], [4, 170], [5, r >= 3 ? 520 : 380], [1, 0]]; if (r >= 4 && !fast) { seq.unshift([1, 480]); b.classList.add('shake'); }
  let k = 0; const step = () => { const [f, d] = seq[k++]; if (f !== 1 || k > 1) b.classList.remove('shake'); chestFr = f; chestGlow = f >= 3 && f <= 5 ? (f === 5 ? 0.55 + 0.07 * r : 0.35 + 0.05 * r) : 0;
    if (f === 4) { if (r >= 4) B.shake = Math.max(B.shake, 5); if (cb) cb(); } if (k < seq.length) chestT.push(setTimeout(step, d * T)); else { chestBusy = 0; chestGlow = 0; } }; step(); }
function chestFly(it) { // l'objet file du coffre vers sa case
  const a = $('forgeBtn'), tg = document.querySelector(`#eqg [data-s="${it.slot}"]`); if (!a || !tg || !a.offsetParent || !tg.offsetParent) return;
  const ap = $('app').getBoundingClientRect(), r1 = a.getBoundingClientRect(), r2 = tg.getBoundingClientRect(), fl = document.createElement('canvas'); fl.className = 'cfly'; eqIcon(fl, it, it.slot); fl.style.setProperty('--rc', RAR[it.r].c);
  const x0 = (r1.left + r1.width / 2 - ap.left) / SCL - 16, y0 = (r1.top + 24 - ap.top) / SCL, x1 = (r2.left + r2.width / 2 - ap.left) / SCL - 16, y1 = (r2.top + r2.height / 2 - ap.top) / SCL - 16;
  $('app').appendChild(fl); fl.animate([{ transform: `translate(${x0}px,${y0}px) scale(.5)`, opacity: 0.3 }, { transform: `translate(${(x0 + x1) / 2}px,${Math.min(y0, y1) - 40}px) scale(1.4)`, opacity: 1, offset: 0.45 }, { transform: `translate(${x1}px,${y1}px) scale(1)`, opacity: 1 }], { duration: 480, easing: 'cubic-bezier(.3,.7,.3,1)', fill: 'both' }).onfinish = () => { fl.remove(); const t2 = document.querySelector(`#eqg [data-s="${it.slot}"]`); if (t2) t2.animate([{ transform: 'scale(1.25)' }, { transform: 'scale(1)' }], { duration: 260 }); }; }
let zcT''')
rep("if (!cur) { equipItem(it); save(); equipFx(it);", "if (!cur) { chestFly(it); equipItem(it); save(); equipFx(it);")
rep("let autoT = 0;\nlet autoBusy = false;", "let autoT = 0;\nvar autoBusy = false;")

# =====================================================================
# D. textes : marteaux -> clés, clés de donjon -> tickets, forge -> coffre
# =====================================================================
# icônes : le marteau devient une clé, l'ancienne clé devient un ticket
rep('''  key: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>',''',
    '''  key: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M3 6h18v4a2 2 0 0 0 0 4v4H3v-4a2 2 0 0 0 0-4zm5.5 1.5v9h1.6v-9z"/></svg>',''')
rep('''  ham: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z"/></svg>',''',
    '''  ham: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>',''')
T = [
 # anciennes clés (donjons de sets) -> tickets
 (r"""['#f0c46a', '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>', 'Clés', '2 par jour (remises à minuit), +1 par boss de chapitre, certaines quêtes.', 'Entrer dans un donjon (la clé n\'est perdue qu\'en cas de victoire).'],""",
  r"""['#f0c46a', IC.key, 'Tickets de set', '2 par jour (remis à minuit), +1 par boss de chapitre, certaines quêtes.', 'Entrer dans un donjon de set (le ticket n\'est perdu qu\'en cas de victoire).'],"""),
 ("donjons de sets (onglet Donjons), 2 clés par jour.", "donjons de sets (onglet Donjons), 2 tickets par jour."),
 ("keys: ['key', '#ffd890', 'clés']", "keys: ['key', '#ffd890', 'tickets']"),
 ("keys: v > 1 ? 'clés' : 'clé'", "keys: v > 1 ? 'tickets' : 'ticket'"),
 ("Plus de clés : 2 nouvelles dans", "Plus de tickets : 2 nouveaux dans"),
 ("<small>clé${S.keys > 1 ? 's' : ''}</small>", "<small>ticket${S.keys > 1 ? 's' : ''}</small>"),
 ("${KEY_MAX} clés max", "${KEY_MAX} tickets max"),
 ("B2('keys', '+10 clés')", "B2('keys', '+10 tickets')"),
 ("'Tickets, clés et raid pleins'", "'Tickets et raid pleins'"),
 # marteaux -> clés
 ("what: 'marteaux', d: 'Un démon voleur garde un trésor de marteaux'", "what: 'clés', d: 'Un démon voleur garde un trésor de clés'"),
 ("${fmt(r.ham)} marteaux", "${fmt(r.ham)} clés"),
 ("auto: [11, 'Auto-forge']", "auto: [11, 'Ouverture auto']"),
 ("or, XP, marteaux et pages", "or, XP, clés et pages"),
 ("Le bouton <b>Auto</b> à côté de la forge forge en boucle à ta place et te propose les objets meilleurs.", "Le bouton <b>Auto</b> à côté du coffre l\\'ouvre en boucle à ta place et te propose les objets meilleurs."),
 ("gagner marteaux, or, âmes ou Sceaux", "gagner clés, or, âmes ou Sceaux"),
 ("démons, forges, donjons, invocations…", "démons, coffres, donjons, invocations…"),
 (": forge et reviens défier", ": ouvre des coffres et reviens défier"),
 ("'Objets forgés'", "'Coffres ouverts'"),
 ("cur ? b : null, 'Forgé', true, 'new')", "cur ? b : null, 'Trouvé', true, 'new')"),
 ("'Niveau de la forge, amélioration", "'Niveau du coffre, amélioration"),
 ("IC.ham, 'Marteaux', '1 par démon", "IC.ham, 'Clés', '1 par démon"),
 ("'Forger un objet (1 marteau par forge).'", "'Ouvrir le coffre (1 clé par objet).'"),
 ("<h3>Forge · niveau ${S.forge}", "<h3>Coffre · niveau ${S.forge}"),
 ("XP gagnée par forge</b> et la vitesse de l'auto-forge.", "XP gagnée par coffre</b> et la vitesse de l'ouverture auto."),
 ("XP par forge : ", "XP par coffre : "),
 ("· auto-forge ×", "· ouverture auto ×"),
 ("Marteaux : 1 par démon vaincu", "Clés : 1 par démon vaincu"),
 ("Améliorer la forge<small>", "Améliorer le coffre<small>"),
 ("'Forge et butin'", "'Coffre et butin'"),
 ("'Forgeron infatigable'", "'Serrurier infatigable'"),
 ("qu'un nouveau démon donne un marteau en plus", "qu'un nouveau démon donne une clé en plus"),
 ("Chances de rareté comme une forge +", "Chances de rareté comme un coffre +"),
 (r"a_twin: ['Marteau béni', 1, 'ham', () => '10 % de chances qu\'une forge ne consomme pas de marteau']", r"a_twin: ['Clé bénie', 1, 'ham', () => '10 % de chances qu\'un coffre ne consomme pas de clé']"),
 ("['Forgeron', { a_ham: 2 }]", "['Serrurier', { a_ham: 2 }]"),
 ("cap: ['Marteau béni', { a_twin: 1 }]", "cap: ['Clé bénie', { a_twin: 1 }]"),
 ("ham: `${s.v} marteaux`", "ham: `${s.v} clés`"),
 ("ham: ['ham', '#d8dee8', 'marteaux']", "ham: ['ham', '#ffd27a', 'clés']"),
 ("+${r2.ham} marteaux", "+${r2.ham} clés"),
 ("étapes, boss, forges, donjons", "étapes, boss, coffres, donjons"),
 ("'Apprenti forgeron', 'Forger 50 objets'", "'Apprenti serrurier', 'Ouvrir 50 coffres'"),
 ("'Maître forgeron', 'Forger 500 objets'", "'Maître serrurier', 'Ouvrir 500 coffres'"),
 ("n => `Forger ${n} objets`", "n => `Ouvrir ${n} coffres`"),
 ("n => `Améliorer la forge ${n} fois`", "n => `Améliorer le coffre ${n} fois`"),
 ("ham: 'marteaux', gold: 'or'", "ham: 'clés', gold: 'or'"),
 (r"Il t\'attend à la forge", r"Il t\'attend au coffre"),
 ("Auto-forge en pause : plus de marteaux", "Ouverture auto en pause : plus de clés"),
 ("<span>Marteaux<b>", "<span>Clés<b>"),
 ("B2('ham', '+100 marteaux', 'gold')", "B2('ham', '+100 clés', 'gold')"),
 ("G('Forge', B2('forge', 'Forge +1') + B2('forge5', 'Forge +5'))", "G('Coffre', B2('forge', 'Coffre +1') + B2('forge5', 'Coffre +5'))"),
 ("chip('Forge', S.forge,", "chip('Coffre', S.forge,"),
 ("'Plus de marteaux : ils reviennent avec le temps'", "'Plus de clés : bats des démons sur de nouvelles étapes'"),
 ("'Marteau béni : forge gratuite !'", "'Clé bénie : coffre gratuit !'"),
 ("`Forge niveau ${S.forge}`", "`Coffre niveau ${S.forge}`"),
 ("'Auto-forge : bats le boss du chapitre 1 (étape 1-10) pour la débloquer'", "'Ouverture auto : bats le boss du chapitre 1 (étape 1-10) pour la débloquer'"),
 ("'Plus de marteaux : avance dans les étapes, ouvre le coffre hors ligne ou fais le Repaire du Voleur'", "'Plus de clés : avance dans les étapes, récolte le coffre hors ligne ou fais le Repaire du Voleur'"),
 ("'Auto-forge activée' : 'Auto-forge désactivée'", "'Ouverture auto activée' : 'Ouverture auto désactivée'"),
 (r"['ham', 'Forge ton équipement', 'Touche l\'<b>enclume</b> pour forger avec tes marteaux.", r"['ham', 'Ouvre le coffre', 'Touche le <b>coffre</b> pour l\'ouvrir avec tes clés."),
 (r"h: 'La forge', p: 'Tout commence ici. Touche l\'<b>enclume</b> pour forger ton premier objet.'", r"h: 'Le coffre', p: 'Tout commence ici. Touche le <b>coffre</b> pour trouver ton premier objet.'"),
 (r"L\'objet forgé est à gauche", r"L\'objet trouvé est à gauche"),
 ("'Chaque forge donne un objet au hasard : arme, casque, bottes… plus ou moins rare. Forge-en un deuxième.'", "'Chaque coffre donne un objet au hasard : arme, casque, bottes… plus ou moins rare. Ouvre-en un deuxième.'"),
 ("h: 'Les marteaux', p: 'Chaque forge coûte <b>1 marteau</b>.", "h: 'Les clés', p: 'Chaque coffre coûte <b>1 clé</b>."),
 (r"h: 'L\'auto-forge', p: 'Elle forge en boucle sans toucher", r"h: 'L\'ouverture auto', p: 'Elle ouvre le coffre en boucle sans toucher"),
 ("h: 'Le niveau de forge', p: 'Dépense ton or ici pour améliorer la forge :", "h: 'Le niveau du coffre', p: 'Dépense ton or ici pour améliorer le coffre :"),
 ("{ t: '#eqCols', h: 'Ton équipement', p: '8 emplacements autour de ton héros.", "{ t: '#eqg', h: 'Ton équipement', p: '11 emplacements à gauche (un 12e plus tard), tes artefacts à droite."),
 ("(sinon il part tout seul après 3 s)", "(ou laisse <b>AUTO</b> le lancer tout seul)"),
 ("${D.res ? 'le ticket' : 'la clé'} n'est pas consommé${D.res ? '' : 'e'}", "le ticket n'est pas consommé"),
 ("Quand il est trop fort, forge, monte de niveau", "Quand il est trop fort, ouvre des coffres, monte de niveau"),
 ("Trop fort ? Forge, monte de niveau et reviens.", "Trop fort ? Ouvre des coffres, monte de niveau et reviens."),
 ("Tuer des démons, forger, vaincre des boss", "Tuer des démons, ouvrir des coffres, vaincre des boss"),
 (">Avarice</b> (or, XP, forge).", ">Avarice</b> (or, XP, coffre)."),
 ("Le Repaire du Voleur donne des <b>marteaux</b>", "Le Repaire du Voleur donne des <b>clés</b>"),
 ("ouverts avec des <b>clés</b>", "ouverts avec des <b>tickets</b>"),
]
for a, b in T: rep(a, b)
rep("pour forger des ailes", "pour débloquer des ailes", 2)

# =====================================================================
# E. styles
# =====================================================================
CSS = r'''<style id="sv">
/* ===== patch v18 : disposition façon Legend of Mushroom, combat de côté, coffre ===== */
#app{background:radial-gradient(120% 60% at 50% 100%,#3a1a10,#140810 70%)!important}
#eqTog,#eqCols,#eqBg,#botBar,#hubTog{display:none!important}
body:not(.full) #topBar{position:absolute!important;left:0;right:0;top:0;z-index:6;background:none!important;border:0!important;box-shadow:none!important;padding:calc(6px + env(safe-area-inset-top)) 6px 0!important;pointer-events:none}
body:not(.full) #topBar>*,body:not(.full) #hud>*{pointer-events:auto}body:not(.full) #hud{pointer-events:none}
#stageBar{position:absolute!important;left:50%!important;top:calc(54px + env(safe-area-inset-top))!important;transform:translateX(-50%)!important;width:auto!important;margin:0!important;display:flex!important;flex-direction:column!important;align-items:center!important;gap:3px!important;pointer-events:none!important}
#stageBar .srow{flex:none!important;width:140px}#pips,#dpsChip,.srow1{display:none!important}
#ribbon{clip-path:none!important;flex-direction:column!important;align-items:center!important;gap:0!important;padding:2px 14px 3px!important;border-radius:12px!important;background:#000b!important;border:1px solid #6a4a2a!important;box-shadow:0 2px 6px #0008!important;pointer-events:auto;white-space:nowrap}
#ribbon b{font:400 15px/1.15 var(--n)!important;letter-spacing:.02em!important;color:var(--gold2)!important}
#ribbon small{font:800 9.5px var(--b)!important;color:#ffb0a0!important}#ribbon small:empty{display:none}
#waveBox{height:9px!important;border-width:1px!important;background:#000b!important}#waveTxt{font-size:7.5px!important;line-height:8px!important}#waveBox.boss{height:12px!important}#waveBox.boss #waveTxt{font-size:9px!important;line-height:11px!important}
#stageWrap{flex:none!important}
#hubCol{left:3px!important;top:calc(82px + env(safe-area-inset-top))!important;transform:none!important}
#hubCol .hcIn{gap:2px!important;opacity:1!important;pointer-events:auto!important;padding:0!important}
#hubCol .hb.big,#hubTop .hb{width:54px!important;height:52px!important}
#hubCol .hb.big img,#hubTop .hb img{width:42px!important;height:42px!important}
#hubCol .hb.big small,#hubTop .hb small{font-size:9px!important;padding:0 5px!important;margin-top:-5px!important}
#hubCol .hb.big .dot,#hubTop .hb .dot{width:14px!important;height:14px!important;font-size:8px!important;top:-1px!important;right:2px!important}
#hubAfk .afkF{top:36px!important;left:12px!important;right:12px!important;height:3px!important}
#sumBtn{position:relative;width:54px!important;height:54px!important;padding:0!important;margin:0!important;background:none!important;border:0!important;box-shadow:none!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important}
#sumBtn img.portal{width:46px!important;height:46px!important;margin:0!important;position:static!important;transform:none!important}
#sumBtn b{margin-top:-6px!important;position:relative;font:400 9px var(--n)!important;padding:0 5px!important;border-radius:7px!important;background:linear-gradient(#5a2a9a,#20083a)!important;border:1px solid #c8a0ff!important;color:#fff!important;white-space:nowrap}
#sumBtn .dot{top:-1px!important;right:2px!important;width:14px!important;height:14px!important;font-size:8px!important}
#hubTop{flex-direction:column!important;right:3px!important;left:auto!important;top:calc(86px + env(safe-area-inset-top))!important;gap:2px!important}
#challengeBtn{top:calc(100px + env(safe-area-inset-top))!important;padding:6px 16px!important;font-size:15px!important}
#stageWrap #questBar{position:absolute!important;right:6px;bottom:6px;z-index:4;max-width:62%;padding:3px 10px 3px 8px!important;border-radius:12px;background:#0d0609d8!important;border:1px solid #6a4a2a!important;gap:6px!important}
#stageWrap #questBar #qFill{border-radius:12px}#stageWrap #questBar b{font-size:10.5px!important}#stageWrap #questBar small{font-size:9px!important}#stageWrap #questBar em{font-size:12px!important}#stageWrap #questBar .qi{font-size:13px!important}
#skBar{flex:none;position:relative;z-index:4;height:56px;display:flex;justify-content:center;align-items:center;gap:9px;background:linear-gradient(#1a0b12,#100509);border-top:1.5px solid #6a4a2a;border-bottom:1.5px solid #6a4a2a}
body.full #skBar{display:none!important}
#autoU{width:44px;height:44px;border-radius:50%;border:2px solid #c8964a;background:radial-gradient(#5a3a10,#2a1404);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0;box-shadow:0 2px 4px #000;color:var(--gold2);gap:1px}
#autoU b{font:400 11px/1 var(--n)}#autoU small{font:400 11px/1 var(--n);color:#9affb0}#autoU.off{filter:grayscale(.5) brightness(.85)}#autoU.off small{color:#ff8a8a}
#skBar #spellHud2{position:static!important;display:flex!important;gap:9px!important;pointer-events:auto!important}
#skBar .sh2{position:relative;width:44px!important;height:44px!important;border-radius:50%;border:2px solid #c8964a;background:radial-gradient(#2a1418,#0a0406);padding:0;overflow:hidden;box-shadow:0 2px 4px #000;display:grid;place-items:center;color:#a08a78}
#skBar .sh2 .spIco{border-radius:50%}#skBar .sh2 .cdm{left:0!important;top:0!important;width:100%!important;height:100%!important}#skBar .sh2 .cdt{font-size:13px!important}
#skBar .sh2.em b{font:400 22px var(--n);color:#8a6a50}#skBar .sh2.lk{opacity:.5}#skBar .sh2.lk svg{width:16px;height:16px}
#skBar #ultBtn{position:relative!important;right:auto!important;bottom:auto!important;width:58px!important;height:58px!important;flex:none}
#skBar #ultBtn .uIc{width:31px!important;height:31px!important}#skBar #ultBtn b{bottom:-3px!important;font-size:10px!important}
body:not(.full) #panel{flex:1 1 auto!important;min-height:0!important;overflow:hidden!important;padding:10px 8px 0!important;background:none!important}
#eqg{display:flex;justify-content:center;align-items:flex-start;gap:6px}
#eqg .gl{display:grid;grid-template-columns:repeat(4,var(--ss,56px));gap:6px}#eqg .gr{display:grid;grid-template-columns:repeat(2,var(--ss,56px));gap:6px}
#eqg .sep{width:0;align-self:stretch;border-left:2px dashed #c8964a50;margin:2px 3px}
#eqg .slot{grid-column:auto!important;text-align:center;position:relative;width:var(--ss,56px)!important;height:var(--ss,56px)!important;border-radius:11px!important;border:2px solid #4a2a36!important;background:radial-gradient(circle at 50% 40%,#3a2030,#170b11)!important;box-shadow:inset 0 -3px 0 #0006,0 2px 4px #0008!important;padding:0!important;display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:1px;color:#a08a78;overflow:visible}
#eqg .slot:not(.empty):not(.lockd){border-color:var(--rc)!important;background:radial-gradient(70% 65% at 50% 42%,color-mix(in srgb,var(--rc) 38%,#1a0d14),#110a0d 85%)!important;box-shadow:inset 0 -3px 0 #0006,0 0 10px -3px var(--rc)!important}
#eqg .slot canvas{width:calc(var(--ss,56px) * .7)!important;height:calc(var(--ss,56px) * .7)!important;image-rendering:pixelated;opacity:1!important;margin:0!important}
#eqg .slot.empty canvas[data-ic]{display:none}
#eqg .slot .nm{position:static!important;font:800 7.5px var(--b)!important;color:#a08a78!important;letter-spacing:.04em!important;text-transform:uppercase;white-space:nowrap}
#eqg .slot:not(.empty):not(.lockd) .nm{display:none}#eqg .slot.art.on .nm{display:block;font-size:7px!important;color:#e8d0b0!important}
#eqg .slot .lv{position:absolute!important;left:4px!important;right:auto!important;top:auto!important;bottom:2px!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;font:400 10px var(--n)!important;color:#fff!important;text-shadow:0 1px 0 #000,0 0 3px #000}
#eqg .slot.art .lv{left:auto!important;right:4px!important;top:2px!important;bottom:auto!important}
#eqg .slot .gem,#eqg .slot .setdot{display:none}
#eqg .slot.lockd{opacity:.5;filter:grayscale(1)}#eqg .slot .flk{display:grid;place-items:center;color:#8a7a70}#eqg .slot .flk svg{width:17px;height:17px}#eqg .slot .stg{font:800 6.5px var(--b);font-style:normal;color:#8a7a70;white-space:nowrap}
#eqg .slot.art{border-color:#6a4a2a!important}#eqg .slot.art .wplus{font:400 20px/1 var(--n);font-style:normal;color:#8a6a50}
#eqg .slot.art canvas#wingMini{width:46px!important;height:30px!important}#eqg .slot.art canvas#famMini{width:34px!important;height:34px!important}
#eqg .rmini{display:grid;grid-template-columns:repeat(2,15px);gap:1px}#eqg .rmini .rsp{width:15px!important;height:15px!important;margin:0!important;animation:none!important}
#eqg .spmini{display:flex;gap:1px}
#app #dock{flex:none!important;position:relative!important;height:128px!important;min-height:0!important;display:flex!important;justify-content:center!important;align-items:flex-end!important;gap:30px!important;padding:0 0 8px!important;background:none!important;border:0!important;box-shadow:none!important;overflow:visible!important}
#app #dock::before,#app #dock::after{display:none!important}
#app #dock .dk{width:58px!important;height:58px!important;border-radius:50%!important;padding:0!important;margin:0 0 12px!important;align-self:flex-end!important;background:radial-gradient(circle at 50% 30%,#3a2028,#120609 70%)!important;border:2px solid #c8964a!important;box-shadow:0 3px 8px #000c!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:0!important}
#app #dock .dk small{font:800 7px/1 var(--b)!important;letter-spacing:.08em!important;color:#c8a878!important;text-transform:uppercase}
#app #dock .dk b{font:400 18px/1.05 var(--n)!important;color:#ffe2a8!important;margin:1px 0!important}
#app #dock #bagN{display:flex;flex-direction:column;align-items:center}#app #dock #bagN b{display:block}
#app #dock #bagBtn.on{border-color:#5ae07a!important;box-shadow:0 0 12px -2px #5ae07a,0 3px 8px #000c!important}#app #dock #bagBtn.on b{color:#9affb0!important}
#app #dock #bossBtn{display:none!important}#app #dock #forgeLv .dot{top:-2px!important;right:-2px!important}
#app #dock #forgeBtn{position:relative!important;flex:none!important;width:122px!important;height:124px!important;padding:0!important;margin:0!important;background:none!important;border:0!important;box-shadow:none!important;overflow:visible!important;filter:none!important;transform:none!important}
#app #forgeBtn .chest{position:absolute!important;left:50%!important;bottom:14px!important;width:106px!important;height:120px!important;margin-left:-53px!important;image-rendering:pixelated!important;animation:none!important;filter:drop-shadow(0 4px 6px #000)!important;z-index:1}
#app #forgeBtn:active .chest{transform:scale(.96)}
#app #forgeBtn.shake .chest{animation:chs .08s linear infinite!important}@keyframes chs{25%{transform:translate(-2px,0)}75%{transform:translate(2px,0)}}
#app #forgeBtn .cglow,#app #forgeBtn .zc{display:none!important}
#app #forgeBtn .plq{position:absolute!important;left:50%!important;bottom:0!important;transform:translateX(-50%)!important;z-index:2;display:flex;align-items:center;gap:5px;padding:1px 14px!important;border-radius:12px;background:linear-gradient(#5a3420,#2a160c)!important;border:2px solid #f0c46a!important}
#app #forgeBtn .plq svg{width:16px;height:16px}#app #forgeBtn .plq b{font:400 16px var(--n)!important;color:#ffe3a0!important}
#app #forgeBtn.empty .plq b{color:#ff8a8a!important}
#app #forgeBtn .smk{bottom:96px!important}#app #forgeBtn .fl{bottom:140px!important}#app #forgeBtn .puff{bottom:144px!important}
#app #dock .shardp{position:absolute!important;left:10px;top:2px;display:flex!important;align-items:center;gap:4px;margin:0!important;padding:2px 9px 2px 6px;border-radius:10px;background:#000a;border:1px solid #5a3a6a;color:#b8a0ff;font:800 11px var(--b)}
#app #dock .shardp svg{width:13px;height:13px}#app #dock .shardp b{font:400 14px var(--n);color:#d8c8ff}
.cfly{position:absolute;left:0;top:0;width:32px;height:32px;z-index:30;pointer-events:none;image-rendering:pixelated;filter:drop-shadow(0 0 6px var(--rc)) drop-shadow(0 0 2px #fff)}
body.full #app #dock{display:none!important}
#toast{top:200px!important}body.full #toast{top:110px!important}
</style>
'''
rep('<div id="app">', CSS + '<div id="app">')
open(P, 'w').write(s)
print('patch v18 ok', len(s) // 1024, 'Ko')
