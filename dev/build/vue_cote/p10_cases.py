# p10 : cases d'équipement plus grandes (coffre plus compact, combat un peu moins haut, icônes qui remplissent la case)
import sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p10 cases' not in s
def rep(old, new, cnt=1):
    global s; assert s.count(old) == cnt, (s.count(old), old[:100]); s = s.replace(old, new)
rep("room = H0 - st - 56 - nav - 128 - 16;\n  const ss = Math.max(42, Math.min(64, Math.floor((W - 16 - 5 * 6 - 14) / 6), Math.floor((room - 12) / 3)));",
    "room = H0 - st - 56 - nav - DOCKH - 10;\n  const ss = Math.max(42, Math.min(72, Math.floor((W - 10 - 5 * 5 - 12) / 6), Math.floor((room - 10) / 3)));")
rep("function eqSize() {", "const DOCKH = 108; // p10 : hauteur de la zone du coffre\nfunction eqSize() {")
s = s.replace('</style>\n<div id="app">', r'''
/* p10 cases : équipement plus grand */
body:not(.full) #panel{padding:6px 5px 0!important;display:flex!important;flex-direction:column!important;justify-content:center!important}
#eqg{gap:4px!important}#eqg .gl,#eqg .gr{gap:5px!important}#eqg .sep{margin:2px 1px!important}
#eqg .slot canvas{width:calc(var(--ss,56px) * .84)!important;height:calc(var(--ss,56px) * .84)!important}
#eqg .slot .lv{font-size:11px!important;left:3px!important;bottom:1px!important}
#app #dock{height:108px!important;padding-bottom:4px!important}
#app #dock #forgeBtn{height:104px!important;width:110px!important}
#app #forgeBtn .chest{width:92px!important;height:104px!important;margin-left:-46px!important;bottom:12px!important}
#app #dock .dk{width:54px!important;height:54px!important;margin-bottom:8px!important}
</style>
<div id="app">''', 1)
assert 'p10 cases' in s
open(P, 'w').write(s); print('p10 cases ok')
