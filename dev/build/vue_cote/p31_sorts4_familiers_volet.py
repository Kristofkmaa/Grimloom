# p31 : 4 pouvoirs + ultime (4e emplacement au chapitre 6) ; emplacements de familiers plus tôt (1, 2-1, 3-1, 4-1, 5-1) ;
#  la petite flèche qui replie le volet de gauche (Invocation, Roue, Passe) revient
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p31 sorts4' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
# --- 4 pouvoirs ---
rep("const slotCount = () => S.c >= 4 ? 3 : S.c >= 2 ? 2 : 1;", "const slotCount = () => S.c >= 6 ? 4 : S.c >= 4 ? 3 : S.c >= 2 ? 2 : 1; while (S.slots.length < 4) S.slots.push(null); // p31 sorts4")
rep("[0, 1, 2].map(i => { const id = S.slots[i]; if (i >= n) return `<div class=\"spslot lock\"><i class=\"splk\">${IC.lock}</i><small>Chapitre ${i === 1 ? 2 : 4}</small></div>`;",
    "[0, 1, 2, 3].map(i => { const id = S.slots[i]; if (i >= n) return `<div class=\"spslot lock\"><i class=\"splk\">${IC.lock}</i><small>Chapitre ${[1, 2, 4, 6][i]}</small></div>`;", 2)
rep("el.innerHTML = [0, 1, 2].map(i =>", "el.innerHTML = [0, 1, 2, 3].map(i =>")
rep("S.slots.slice(0, 3).map(id => id && S.spells[id] ? id : '')", "S.slots.slice(0, 4).map(id => id && S.spells[id] ? id : '')")
rep("S.slots.filter(Boolean).slice(0, 3).map(id => spIcon(id, 16))", "S.slots.filter(Boolean).slice(0, 4).map(id => spIcon(id, 12))")
rep("S.slots = Object.keys(SPELLS).slice(0, 3); }", "S.slots = Object.keys(SPELLS).slice(0, 4); }")
# --- familiers : emplacements plus tôt ---
rep("const FAM_UNL = [0, 21, 31, 41, 51];", "const FAM_UNL = [0, 11, 21, 31, 41];")
# le tuto des Pouvoirs fermait la fiche qu'il présente
rep("  if (CO) return; if (!$('modal').hidden) closeM();", "  if (CO) return; if (!$('modal').hidden && !(steps && steps.some(st => typeof st.t === 'string' && st.t.includes('#mbox')))) closeM();")
rep("Équipe jusqu\\'à <b>3 pouvoirs</b>. Le premier est libre, les autres se débloquent aux chapitres 2 et 4.", "Équipe jusqu\\'à <b>4 pouvoirs</b>. Le premier est libre, les autres se débloquent aux chapitres 2, 4 et 6.")
# --- volet de gauche repliable ---
s = s.replace('<style id="sv">', '''<style id="sv">/* p31 sorts4 */
#skBar{gap:7px!important}#skBar #spellHud2{gap:7px!important}#skBar .sh2{width:42px!important;height:42px!important}
.spslots{grid-template-columns:repeat(4,1fr)!important}
#mbox .row:has(>[data-slot]){flex-wrap:wrap}#mbox .row>[data-slot]{flex:1 1 45%!important}
#app #hubTog{display:grid!important;position:absolute;left:100%;top:50%;margin:-15px 0 0 2px;width:22px;height:30px}
#app #hubTog img{width:22px;height:28px}#app #hubCol #hubTog .aR{display:none}#app #hubCol.shut #hubTog .aR{display:block}#app #hubCol.shut #hubTog .aL{display:none}
#app #hubCol{transition:transform .28s cubic-bezier(.3,.8,.3,1)!important}
#app #hubCol.shut{transform:translateX(calc(-100% - 3px))!important}
#app #hubCol.shut .hcIn{opacity:0!important;pointer-events:none!important}
''', 1)
open(P, 'w').write(s); print('p31 sorts4 ok')
