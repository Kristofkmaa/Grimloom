import base64
s=open('/home/claude/grimloom/src.html').read()
F='/home/claude/grimloom/fonts/'
def ff(fam,file,w): return "@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%s;font-display:block}"%(fam,base64.b64encode(open(F+file,'rb').read()).decode(),w)
fonts=''.join([ff('Cinzel','cinzel-latin-700-normal.woff2',700),ff('Cinzel','cinzel-latin-900-normal.woff2',900),ff('Lilita','lilita-one-latin-400-normal.woff2',400),ff('Nunito','nunito-latin-700-normal.woff2',700),ff('Nunito','nunito-latin-800-normal.woff2',800),ff('Nunito','nunito-latin-900-normal.woff2',900)])
s=s.replace('/*FONT*/',fonts)
assets='\n'.join(open(f).read() for f in ['/home/claude/lune/assets2.js','/home/claude/crypte/assets_cata.js','/home/claude/grimloom/assets_dem.js','/home/claude/grimloom/assets_equip.js','/home/claude/grimloom/assets_icons.js','/home/claude/grimloom/assets_audio.js'])
s=s.replace('/*ASSETS*/',assets)
open('/home/claude/grimloom.html','w').write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">'+s+'</body></html>')
