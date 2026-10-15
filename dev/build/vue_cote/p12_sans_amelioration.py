# p12 : plus d'amélioration d'objet ; on progresse uniquement en trouvant mieux dans le coffre
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p12 sans amelioration' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("""    const ok = S.gold >= upCost(it);
    sheet(`<h3>${nm} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Équipé', null)}
    <button class="btn gold" id="upI" type="button" style="width:100%;margin-top:12px" ${ok ? '' : 'disabled'}>Améliorer au niveau ${it.L + 1}<small>${fmt(upCost(it))} or — tu as ${fmt(S.gold)} or</small></button>
`);
    $('upI').onclick = () => { if (upgradeItem(it)) { B.gear = gear(); showItem(it, null); } };""",
"""    sheet(`<h3>${nm} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Équipé', null)}
    <p style="margin:12px 4px 0;text-align:center;font:700 12.5px/1.4 var(--b);color:var(--dim)">Ouvre des coffres pour trouver mieux : un meilleur objet le remplace et l'ancien est recyclé en or.</p>`); // p12 sans amelioration""")
rep("['upgrade', n => `Améliorer ${n} objets`, 3]", "['kill', n => `Tuer ${n} démons`, 120]")
rep("a_up: ['Économe', 5, 'drop', r => `Améliorations ${5 * r} % moins chères`]", "a_up: ['Économe', 5, 'drop', r => `Niveau du coffre ${5 * r} % moins cher`]")
rep("function forgeCost() { return Math.round(400 * Math.pow(2.6, S.forge - 1)); }", "function forgeCost() { return Math.round(400 * Math.pow(2.6, S.forge - 1) * (1 - 0.05 * tr('a_up'))); }")
rep("'Niveau du coffre, amélioration des objets, compagnons, réinitialiser les talents.'", "'Niveau du coffre, compagnons, réinitialiser les talents.'")
rep("Sinon, recycle-le en <b>or</b> pour améliorer ton stuff.", "Sinon, recycle-le en <b>or</b> pour améliorer ton coffre.")
rep("tu gagnes de l\\'<b>or</b> pour améliorer ton équipement.", "tu gagnes de l\\'<b>or</b> pour monter le niveau du coffre.")
rep("Touche une pièce équipée pour l\\'<b>améliorer</b> avec de l\\'or : elle garde sa rareté et gagne en puissance.", "Pour progresser, trouve de <b>meilleurs objets</b> dans le coffre.")
s = s.replace('<style id="sv">', '<style id="sv">/* p12 sans amelioration */', 1)
open(P, 'w').write(s); print('p12 sans amelioration ok')
