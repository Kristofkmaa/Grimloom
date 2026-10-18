# Assemble dev/src.html + polices + assets_*.js -> dev/out/grimloom.html
import base64, os
D = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = D + 'out/'; os.makedirs(OUT, exist_ok=True)
s = open(D + 'src.html').read()
F = D + 'fonts/'
def ff(fam, file, w): return "@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%s;font-display:block}" % (fam, base64.b64encode(open(F + file, 'rb').read()).decode(), w)
fonts = ''.join([ff('Cinzel', 'cinzel-latin-700-normal.woff2', 700), ff('Cinzel', 'cinzel-latin-900-normal.woff2', 900), ff('Lilita', 'lilita-one-latin-400-normal.woff2', 400), ff('Nunito', 'nunito-latin-700-normal.woff2', 700), ff('Nunito', 'nunito-latin-800-normal.woff2', 800), ff('Nunito', 'nunito-latin-900-normal.woff2', 900)])
s = s.replace('/*FONT*/', fonts)
assets = '\n'.join(open(D + f).read() for f in ['lune_assets2.js', 'crypte_assets_cata.js', 'assets_dem.js', 'assets_equip.js', 'assets_icons.js', 'assets_audio.js', 'assets_side.js', 'assets_wings.js', 'assets_enemy.js', 'assets_raid.js', 'assets_biomes.js', 'assets_pass.js', 'assets_dun.js'])
s = s.replace('/*ASSETS*/', assets)
open(OUT + 'grimloom.html', 'w').write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">' + s + '</body></html>')
print('ok', os.path.getsize(OUT + 'grimloom.html') // 1024, 'Ko')
