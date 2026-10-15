P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v39.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
HB = open('/home/claude/grimloom/heroart/hero.b64').read()
# nouvelle planche du chevalier : 5 lignes (repos dos, course, attaque, touché, repos face), vitesse d'animation propre
rep("for (const k in ASSETS) if (ASSETS[k].src) {", r"""{ const an = {}, k = { idle: 5 / 12, course: 0.5, tir: 4 / 14.5, touche: 2 / 12.5 };
  for (let d = 0; d < 8; d++) { const front = d >= 5 && d <= 7; an['idle_' + d] = { row: front ? 4 : 0, n: 4, k: k.idle }; an['course_' + d] = { row: 1, n: 4, k: k.course }; an['tir_' + d] = { row: 2, n: 4, k: k.tir }; an['touche_' + d] = { row: 3, n: 2, k: k.touche }; }
  ASSETS.knight = { src: 'data:image/png;base64,HEROB64', cw: 300, ch: 320, foot: 20, anims: an }; }
for (const k in ASSETS) if (ASSETS[k].src) {""".replace('HEROB64', HB))
rep("chevalier: { n: 'Le Chevalier de la mort', key: 'chevalier', fx: 'arc', atk: 1.15, hp: 1.2, spd: 1.0, sc: 1.5, leech: 0.03 },", "chevalier: { n: 'Le Chevalier de la mort', key: 'knight', fx: 'arc', atk: 1.15, hp: 1.2, spd: 1.0, sc: 0.484, leech: 0.03 },")
rep("const i = Math.max(0, Math.floor(fr)) % R.n, w = A.cw * sc, h = A.ch * sc; g.save();", "const i = Math.max(0, Math.floor(fr * (R.k || 1))) % R.n, w = A.cw * sc, h = A.ch * sc; g.save(); g.imageSmoothingEnabled = !!R.k && sc < 0.9 ? false : false;")
rep("const A = ASSETS[key], R = A.anims[anim]; if (!R) return; const i = Math.max(0, Math.floor(fr)) % R.n;", "const A = ASSETS[key], R = A.anims[anim]; if (!R) return; const i = Math.max(0, Math.floor(fr * (R.k || 1))) % R.n;")
# ailes calées sur la taille réelle du héros
rep("ws = 0.62 * sc / 1.5,", "ws = 0.62 * heroTop(H.key) * sc / 104,")
open(P, 'w').write(s); print('ok')
