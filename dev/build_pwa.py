# Construit dev/out/pwa/ à partir de dev/out/grimloom.html (sortie d'assemble.py).
# Option --publish : copie aussi le résultat à la racine du dépôt (GitHub Pages).
import json, base64, io, re, time, zipfile, os, sys, shutil
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = D + 'out/pwa/'; os.makedirs(OUT, exist_ok=True)
s = open(D + 'out/grimloom.html').read()
ver = time.strftime('%Y%m%d%H%M')
head = ('<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#0c0610">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="GRIMLOOM">'
        '<link rel="apple-touch-icon" href="icon-192.png"><link rel="icon" href="icon-192.png"><title>GRIMLOOM</title>')
s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + head, 1)
s = s.replace('</body></html>', "<script>if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js'));</script></body></html>")
# images sorties du HTML en fichiers (a/xxxx.webp) : le jeu s'ouvre vite, les images arrivent ensuite (et se mettent en cache)
import hashlib
shutil.rmtree(OUT + 'a', ignore_errors=True); os.makedirs(OUT + 'a')
def ext_img(m):
    t, b = m.group(1), m.group(2); raw = base64.b64decode(b); n = hashlib.sha1(raw).hexdigest()[:12] + '.' + {'jpeg': 'jpg', 'svg+xml': 'svg'}.get(t, t)
    if not os.path.exists(OUT + 'a/' + n): open(OUT + 'a/' + n, 'wb').write(raw)
    return 'a/' + n
logo_src = s
s = re.sub(r'data:image/(png|webp|jpeg);base64,([A-Za-z0-9+/=]+)', ext_img, s)
open(OUT + 'index.html', 'w').write(s)
# icône : logo GRIMLOOM sur fond sombre
m = re.search(r'const TIA = (\{.*?\});\n', logo_src); T = json.loads(m.group(1))
logo = Image.open(io.BytesIO(base64.b64decode(T['logo'].split(',')[1]))).convert('RGBA')
for n in (192, 512):
    ic = Image.new('RGBA', (n, n), (12, 6, 16, 255))
    g = Image.new('RGBA', (n, n)); 
    for r in range(n // 2, 0, -2):
        a = int(70 * (1 - r / (n / 2)))
        Image.Image.paste(g, Image.new('RGBA', (2 * r, 2 * r), (120, 20, 30, a)), (n // 2 - r, n // 2 - r), Image.new('L', (2 * r, 2 * r), 0).point(lambda v: 0))
    w = int(n * 0.9); lg = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    ic.alpha_composite(lg, ((n - w) // 2, (n - lg.height) // 2)); ic.convert('RGB').save(OUT + f'icon-{n}.png')
json.dump({'name': 'GRIMLOOM', 'short_name': 'GRIMLOOM', 'start_url': './', 'scope': './', 'display': 'fullscreen', 'orientation': 'portrait',
           'background_color': '#0c0610', 'theme_color': '#0c0610',
           'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}]},
          open(OUT + 'manifest.webmanifest', 'w'), indent=1)
open(OUT + 'sw.js', 'w').write("""const V = 'grimloom-%s';
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png']))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
// réseau d'abord (pour recevoir les mises à jour), cache si hors ligne
self.addEventListener('fetch', e => { if (e.request.method !== 'GET') return; e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(V).then(k => k.put(e.request, c)); return r; }).catch(() => caches.match(e.request).then(r => r || caches.match('index.html')))); });
""" % ver)
z = D + 'out/grimloom_web.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
    for r, _, fs in os.walk(OUT):
        for n in fs: f.write(os.path.join(r, n), os.path.relpath(os.path.join(r, n), OUT))
print('ok', ver, os.path.getsize(z) // 1024, 'Ko')
if '--publish' in sys.argv:
    for n in os.listdir(OUT):
        if os.path.isdir(OUT + n): shutil.rmtree(D + '../' + n, ignore_errors=True); shutil.copytree(OUT + n, D + '../' + n)
        else: shutil.copy(OUT + n, D + '../' + n)
    print('copié à la racine du dépôt')
