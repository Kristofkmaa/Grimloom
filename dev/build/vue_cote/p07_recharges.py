# patch v26 : recharges des pouvoirs et de l'ultime jamais en pause (avance, changement d'étape…), sauf pendant le choix d'un objet
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'patch v26' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("  for (let i = 0; i < slotCount(); i++) { const id = S.slots[i]; if (!id || !S.spells[id]) continue; B.cd = B.cd || {}; B.cd[id] = (B.cd[id] === undefined ? SPELLS[id].cd * 0.5 : B.cd[id]) - dt; if (B.cd[id] <= 0) { B.cd[id] = SPELLS[id].cd; castSpell(id); } }", "")
rep("  if (!fighting) return;",
    "  { const pick = !!$('sellB'); // patch v26 : on ne met en pause que pendant le choix d'un objet\n"
    "    for (let i = 0; i < slotCount(); i++) { const id = S.slots[i]; if (!id || !S.spells[id]) continue; B.cd = B.cd || {}; if (B.cd[id] === undefined) B.cd[id] = SPELLS[id].cd * 0.5; if (!pick) B.cd[id] = Math.max(0, B.cd[id] - dt); if (B.cd[id] <= 0 && fighting) { B.cd[id] = SPELLS[id].cd; castSpell(id); } } }\n"
    "  if (!fighting) return;")
rep("if (!B.hero.dead && fighting) ultGain(100 / ULT_CD * dt);", "if (!B.hero.dead && !$('sellB')) ultGain(100 / ULT_CD * dt);")
s = s.replace('<style id="sv">', '<style id="sv">/* patch v26 */', 1)
open(P, 'w').write(s); print('patch v26 ok')
