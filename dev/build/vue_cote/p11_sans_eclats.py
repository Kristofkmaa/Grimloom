# p11 : suppression des éclats -> tout passe par l'or
#  recycler donne plus d'or, améliorer un objet ne coûte que de l'or, les éclats possédés sont convertis en or
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p11 sans eclats' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)

# recyclage : or seulement (environ 2,5× la valeur d'avant, plus pour les objets rares)
rep("function recycle(it) { const sh = shardsOf(it); S.gold += it.v; S.shards += sh; smokeFx(it); return sh; }",
    "const recGold = it => Math.round(it.v * (2 + 0.5 * it.r) * (1 + 0.1 * tr('a_shard'))); // p11 sans eclats\nfunction recycle(it) { const g = recGold(it); S.gold += g; smokeFx(it); return g; }")
# conversion des éclats déjà gagnés
rep("if (!Array.isArray(S.bag)) S.bag = []; if (S.shards === undefined) S.shards = 0;",
    "if (!Array.isArray(S.bag)) S.bag = []; if (S.shards === undefined) S.shards = 0;\nif (S.shards > 0) { const g0 = Math.round(S.shards * 3 * Math.pow(1.11, Math.max(1, S.best || 1))); S.gold = (S.gold || 0) + g0; S.shards = 0; setTimeout(() => toast(`Les éclats disparaissent : +${fmt(g0)} or`), 2600); }")
# les éclats qui volaient vers le compteur volent maintenant vers l'or
rep("const tg = document.querySelector('.shardp');", "const tg = $('gold');")
rep("const t2 = document.querySelector('.shardp');", "const t2 = $('gold');")
# fiche d'objet
rep("const better = !cur || itemPower(it) > itemPower(cur), sh = shardsOf(it);", "const better = !cur || itemPower(it) > itemPower(cur), sh = recGold(it);")
rep("Recycler<small>+${fmt(it.v)} or · +${sh} éclats</small>", "Recycler<small>+${fmt(sh)} or</small>")
rep("const n = recycle(it); save(); toast(`Recyclé : +${fmt(it.v)} or · +${n} éclats`);", "const n = recycle(it); save(); toast(`Recyclé : +${fmt(n)} or`);")
rep("const cs = upShards(it), ok = S.gold >= upCost(it) && S.shards >= cs;", "const ok = S.gold >= upCost(it);")
rep("<small>${fmt(upCost(it))} or · ${fmt(cs)} éclats — tu as ${fmt(S.gold)} or · ${fmt(S.shards)} éclats</small>", "<small>${fmt(upCost(it))} or — tu as ${fmt(S.gold)} or</small>")
rep("const upCost = it => Math.round(30 * SCALE(it.L) * RMULT[it.r] * (1 - 0.05 * tr('a_up')));", "const upCost = it => Math.round(55 * SCALE(it.L) * RMULT[it.r] * (1 - 0.05 * tr('a_up')));")
rep("const c = upCost(it), cs = upShards(it); if (S.gold < c || S.shards < cs) { toast('Pas assez ' + (S.gold < c ? 'd\\'or' : 'd\\'éclats : recycle des objets'));", "const c = upCost(it), cs = 0; if (S.gold < c) { toast('Pas assez d\\'or : recycle des objets');")
rep("S.gold -= c; S.shards -= cs;", "S.gold -= c;")
# compteur d'éclats sous la grille
s = __import__('re').sub(r'    <span class="shardp" id="shardP".*?</span>\n', '', s, count=1, flags=__import__('re').S)
assert 'id="shardP"' not in s
# donjon Caveau de cristal : donne de l'or (joyaux) au lieu des éclats
rep("what: 'éclats', d: 'Des démons de givre chargés d\\'éclats' }", "what: 'or', d: 'Des démons de givre gorgés de joyaux' }")
rep("k === 'eclats' ? { shards: Math.round((20 + si * 1.5) * f) }", "k === 'eclats' ? { gold: Math.round(160 * Math.pow(1.11, si) * f) }")
# roue : la part « éclats » devient de l'or
rep("{ k: 'shards', v: 150, w: 15, c: '#2a2050' }", "{ k: 'gold', v: 1, w: 15, c: '#2a2050' }")
# talent Récupérateur
rep("a_shard: ['Récupérateur', 5, 'gem', r => `Éclats de recyclage +${10 * r} %`]", "a_shard: ['Récupérateur', 5, 'coin', r => `Or de recyclage +${10 * r} %`]")
# aide, textes, tutoriel
rep("  ['#b48aff', IC.gem, 'Éclats', 'Recycler les objets dont tu ne veux pas. Plus l\\'objet est rare, plus il en donne.', 'Améliorer l\\'équipement que tu portes (avec de l\\'or).'],\n", "")
rep("'Or', 'Démons tués, recyclage d\\'objets, quêtes.'", "'Or', 'Démons tués, recyclage d\\'objets (plus l\\'objet est rare, plus il rapporte), quêtes, donjons.'")
rep("te donnent or, XP, éclats et pages.", "te donnent or, XP, clés et pages.")
rep("Sinon, recycle-le en <b>éclats</b> pour améliorer ton stuff.", "Sinon, recycle-le en <b>or</b> pour améliorer ton stuff.")
rep("tu gagnes de l\\'or et des <b>éclats</b> pour améliorer ton équipement.", "tu gagnes de l\\'<b>or</b> pour améliorer ton équipement.")
rep("avec de l\\'or et des éclats : elle garde", "avec de l\\'or : elle garde")
rep("  { t: '.shardp', h: 'Les éclats', p: 'Ton stock d\\'éclats s\\'affiche ici. Recycle tout ce qui ne te sert pas pour en gagner.' },\n", "")
rep("p: 'Or, XP, éclats, pages :", "p: 'Or, XP, clés, pages :")
rep("B2('shards', '+1 000 éclats', 'gold') + ", "")
rep("${chip('Éclats', fmt(S.shards), '#b48aff')}", "")
s = s.replace('<style id="sv">', '<style id="sv">/* p11 sans eclats */\n#forgeBtn .shd{border-radius:50%!important;background:radial-gradient(circle at 35% 35%,#fff6c0,#ffc94a 45%,#c87a18)!important;box-shadow:0 0 8px #ffb040!important}\n', 1)
open(P, 'w').write(s); print('p11 sans eclats ok')
