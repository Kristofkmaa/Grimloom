P = '/home/claude/grimloom/src.html'
s = open(P).read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
a = s.index("function recolorStep() {"); b = s.index("function queueBiome")
s = s[:a] + r"""let DVJ = null; // recoloration découpée en tranches pour ne jamais bloquer une image
function recolorStep() {
  const t0 = performance.now();
  while (performance.now() - t0 < 5) {
    if (!DVJ) { const k = DVQ.shift(); if (!k) return; if (DV[k]) continue; const [key, v] = k.split('@'), im = IMG['D_' + key]; if (!im || !im.complete) { DVQ.push(k); return; }
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0); DVJ = { k, c, g, P: VARS[v], y: 0 }; }
    const J = DVJ, W = J.c.width, rows = Math.max(1, Math.floor(60000 / W)), h = Math.min(rows, J.c.height - J.y), id = J.g.getImageData(0, 0 + J.y, W, h), d = id.data, [h0, sm, lm] = J.P;
    for (let i = 0; i < d.length; i += 4) {
      if (!d[i + 3]) continue; const r = d[i] / 255, gg = d[i + 1] / 255, b = d[i + 2] / 255, mx = Math.max(r, gg, b), mn = Math.min(r, gg, b), dl = mx - mn; if (dl <= 0) continue;
      const l = (mx + mn) / 2, sat = dl / (1 - Math.abs(2 * l - 1) + 1e-6); if (sat <= 0.18) continue;
      let hh = mx === r ? ((gg - b) / dl) % 6 : mx === gg ? (b - r) / dl + 2 : (r - gg) / dl + 4; hh *= 60; const dh = ((hh + 540) % 360) - 180; if (Math.abs(dh) >= 50) continue;
      const nh = ((h0 + dh * 0.6) % 360 + 360) % 360, ns = Math.min(1, sat * sm), nl = Math.min(1, l * lm), C = (1 - Math.abs(2 * nl - 1)) * ns, X = C * (1 - Math.abs((nh / 60) % 2 - 1)), m = nl - C / 2, q = Math.floor(nh / 60);
      const R = q === 0 || q === 5 ? C : q === 1 || q === 4 ? X : 0, G = q === 1 || q === 2 ? C : q === 0 || q === 3 ? X : 0, Bq = q === 3 || q === 4 ? C : q === 2 || q === 5 ? X : 0;
      d[i] = (R + m) * 255; d[i + 1] = (G + m) * 255; d[i + 2] = (Bq + m) * 255;
    }
    J.g.putImageData(id, 0, J.y); J.y += h; if (J.y >= J.c.height) { DV[J.k] = J.c; DVJ = null; }
  }
}
""" + s[b:]
rep("if (DVQ.length) recolorStep();", "if (DVQ.length || DVJ) recolorStep();")
rep("B.hero.psD = Math.max(B.hero.psD && B.hero.psT > 0 ? B.hero.psD : 0, d * 0.15);", "B.hero.psD = Math.max(B.hero.psD && B.hero.psT > 0 ? B.hero.psD : 0, d * 0.1);")
open(P, 'w').write(s); print('ok')
