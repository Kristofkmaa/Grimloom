P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v28.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
rep('      <button id="mapBtn" type="button"', '      <button id="helpBtn" type="button" aria-label="Aide : les ressources"><b style="font:400 19px var(--n);color:var(--gold2)">?</b></button>\n      <button id="mapBtn" type="button"')
rep("$('adminBtn').onclick = showAdmin;", r"""$('adminBtn').onclick = showAdmin; $('helpBtn').onclick = showHelp;""")
rep("function showForge() {", r"""// ---------- aide : à quoi servent les ressources ----------
const HELP = [
  ['#ffc23a', '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="9"/></svg>', 'Or', 'Démons tués, recyclage d\'objets, quêtes.', 'Niveau de la forge, amélioration des objets, compagnons, réinitialiser les talents.'],
  ['#d8dee8', IC.ham, 'Marteaux', '1 toutes les 15 s (jusqu\'à 99), boss, quêtes, connexion du jour.', 'Forger un objet (1 marteau par forge).'],
  ['#b48aff', IC.gem, 'Éclats', 'Recycler les objets dont tu ne veux pas. Plus l\'objet est rare, plus il en donne.', 'Améliorer l\'équipement que tu portes (avec de l\'or).'],
  ['#ff9a6a', '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h7a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-5a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h5z"/></svg>', 'Pages de grimoire', 'Chaque vague, boss, donjons, quêtes.', 'Invoquer des pouvoirs (10 pages par invocation), onglet Pouvoirs.'],
  ['#f0c46a', '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M8 3a5 5 0 1 0 1.9 9.6L19 21.7l2-2-1.5-1.5 1.5-1.5-2-2-1.5 1.5-4.9-4.9A5 5 0 0 0 8 3zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/></svg>', 'Clés', '3 par jour, +1 par boss de chapitre, certaines quêtes.', 'Entrer dans un donjon (la clé n\'est perdue qu\'en cas de victoire).'],
  ['#ff4a5a', IC.shield, 'Sceaux', 'Réussir les donjons des sets.', 'Graver un set (Sang, Os, Braises, Givre) sur une pièce que tu portes.'],
  ['#7aff9a', IC.star, 'Expérience et niveaux', 'Tuer des démons.', 'Chaque niveau donne 1 point de talent pour l\'arbre (onglet Talents).'],
  ['#ffe3a0', IC.sword, 'Puissance', 'Calculée à partir de ton équipement, talents et compagnons.', 'Indique ta force : compare-la à la difficulté des étapes.'],
];
function showHelp() {
  sheet(`<h3>Les ressources <button class="x" type="button" aria-label="Fermer">✕</button></h3><div class="help">${HELP.map(([c, ic, n, get, use]) => `<div class="hl" style="--hc:${c}"><div class="hi">${ic}</div><div><b>${n}</b><p><em>Gagner :</em> ${get}</p><p><em>Sert à :</em> ${use}</p></div></div>`).join('')}</div>`);
  $('mbox').querySelector('.x').onclick = closeM;
}
function showForge() {""")
s = s.replace("</style>", r"""
.help{display:grid;gap:8px;max-height:62vh;overflow:auto}
.hl{display:grid;grid-template-columns:40px 1fr;gap:10px;align-items:start;padding:9px 10px;border-radius:12px;background:#ffffff06;border:1px solid #ffffff10}
.hi{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;font-size:21px;color:var(--hc);background:color-mix(in srgb,var(--hc) 14%,#140a0f);border:1.5px solid color-mix(in srgb,var(--hc) 50%,transparent)}
.hl b{display:block;font:900 14px var(--t);color:var(--hc);margin-bottom:2px}
.hl p{margin:2px 0 0;font:700 12px/1.4 var(--b);color:var(--txt)}.hl em{font-style:normal;color:var(--dim)}
</style>""", 1)
open(P, 'w').write(s); print('ok')
