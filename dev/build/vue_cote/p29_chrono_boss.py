# p29 : combat de boss chronométré (60 s, comme dans Mushroom) : si le temps est écoulé, le héros se replie et farme
#  (avant : un boss trop résistant pouvait durer plusieurs minutes sans que rien ne se passe)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p29 chrono boss' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("spawnEnemy(bo.key, 0, 1.45, st, true); bossIntro(", "spawnEnemy(bo.key, 0, 1.45, st, true); B.bossT = BOSS_T; bossIntro(")
rep("function bossIntro(n, sub) {", "const BOSS_T = 60; // p29 chrono boss\nfunction bossIntro(n, sub) {")
rep("  if (B.bossIn) B.bossIn.t += dt;", """  if (B.bossIn) B.bossIn.t += dt;
  if (B.bossT > 0 && !B.dun && !B.hero.dead && !B.walk) { const bo = B.en.find(e => e.boss && !e.dead); if (!bo) B.bossT = 0; else if (!B.bossIn && bo.spawn <= 0) { B.bossT -= dt; if (B.bossT <= 0) { B.bossT = 0; B.hero.hp = 0; B.hero.dead = 1; B.hero.deadT = 0; B.banner = { a: 'Temps écoulé !', b: 'Renforce-toi puis défie-le à nouveau', t: 2.2 }; } } }""")
rep("$('waveTxt').textContent = boss ? `${fmt(Math.max(0, B.en[0].hp))} / ${fmt(B.en[0].max)}` :",
    "$('waveTxt').textContent = boss ? `${fmt(Math.max(0, B.en[0].hp))} / ${fmt(B.en[0].max)}${B.bossT > 0 ? ' · ' + Math.ceil(B.bossT) + ' s' : ''}` :")
s = s.replace('<style id="sv">', '<style id="sv">/* p29 chrono boss */', 1)
open(P, 'w').write(s); print('p29 chrono boss ok')
