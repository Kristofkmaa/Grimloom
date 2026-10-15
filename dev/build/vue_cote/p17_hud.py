# p17 : clés retirées du haut (elles sont déjà sur le coffre), or déplacé à côté du coffre, nom de la carte remonté en haut
import sys, os, re
D = os.path.dirname(os.path.abspath(__file__)) + '/../../'
P = sys.argv[1] if len(sys.argv) > 1 else D + 'src.html'
s = open(P).read(); assert 'p17 hud' not in s
m = re.search(r'      <div class="res"><svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#c87a18"/>.*?<b id="gold">0</b></div>\n', s, flags=re.S); assert m
gold = m.group(0).strip().replace('<div class="res">', '<div class="res" id="goldD">', 1); s = s.replace(m.group(0), '', 1)
m = re.search(r'      <div class="res"><svg class="ico"[^\n]*?<b id="ham">0</b></div>\n', s); assert m
s = s.replace(m.group(0), '      <div class="res" hidden><b id="ham">0</b></div>\n', 1)
assert s.count('  <div id="dock">\n') == 1
s = s.replace('  <div id="dock">\n', '  <div id="dock">\n    ' + gold + '\n', 1)
s = s.replace('<style id="sv">', r'''<style id="sv">/* p17 hud */
#hud .res[hidden]{display:none!important}
#app #topBar #stageBar{top:calc(12px + env(safe-area-inset-top))!important;left:calc(50% + 14px)!important}
#app #dock #goldD{position:absolute!important;left:10px;top:4px;height:28px;padding:0 10px 0 4px;z-index:3}
#app #dock #goldD b{font-size:15px}
''', 1)
open(P, 'w').write(s); print('p17 hud ok')
