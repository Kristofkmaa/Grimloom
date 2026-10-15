P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v14.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# ---------- couloir sans fin : sol et murs jusqu'au haut de l'écran ----------
rep("  for (let y = YH; y < BH; y++) { const q = (y - YH) / (YF - YH),", "  const yTop = scene === 'arena' ? YH : 0, sMin = scene === 'arena' ? S1 : 0.12;\n  for (let y = yTop; y < BH; y++) { const q = (y - YH) / (YF - YH),")
rep("if (s < S1 || s > 1.25) continue; const z = (1 / s - 1) / K, base = py(z), top = base - WALLH * s,", "if (s < sMin || s > 1.25) continue; const z = (1 / s - 1) / K, base = py(z), top = base - WALLH * s,")
rep("g.fillStyle = `rgba(0,0,0,${0.25 + (1 - s) * 0.5})`; g.fillRect(x, top, 1, base - top); }", "g.fillStyle = `rgba(0,0,0,${Math.min(0.85, 0.25 + (1 - s) * 0.5)})`; g.fillRect(x, top, 1, base - top); }")
# portes latérales sur toute la longueur visible
rep("for (let k = -1; k < 2; k++) { const dz = 0.55 - scroll + Math.round(scroll / SEG) * SEG + k * SEG; if (dz < 0.12 || dz > 0.98) continue;",
    "for (let k = -1; k < 4; k++) { const dz = 0.55 - scroll + Math.round(scroll / SEG) * SEG + k * SEG; if (dz < 0.12 || dz > 3.4) continue;")
# brume de profondeur au lieu du noir
rep("const gr = g.createLinearGradient(0, YH - 70, 0, YH + (scene === 'arena' ? 90 : 150)); gr.addColorStop(0, 'rgba(0,0,0,.95)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, BW, YH + 150);",
    "if (scene === 'arena') { const gr = g.createLinearGradient(0, YH - 70, 0, YH + 90); gr.addColorStop(0, 'rgba(0,0,0,.95)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, BW, YH + 150); }\n  else { const gr = g.createLinearGradient(0, 0, 0, YH + 130); gr.addColorStop(0, 'rgba(6,3,6,.82)'); gr.addColorStop(0.45, 'rgba(6,3,6,.45)'); gr.addColorStop(1, 'rgba(6,3,6,0)'); g.fillStyle = gr; g.fillRect(0, 0, BW, YH + 130); }")

# ---------- décor répété sur toute la profondeur ----------
rep("function placeDeco() { DECO = B.scene === 'arena' ? DECO_A : DECO_C; if (DECO === DECO_C) for (const d of DECO) d.z = ((d.wz - B.scroll + 0.15) % SEG + SEG) % SEG - 0.15; else for (const d of DECO) d.z = d.wz - B.scroll; }",
    """function placeDeco() {
  if (B.scene === 'arena') { DECO = DECO_A; for (const d of DECO) d.z = d.wz - B.scroll; return; }
  const out = [], gz = B.gate ? B.gate.z : 99; for (const d of DECO_C) { const z0 = ((d.wz - B.scroll + 0.15) % SEG + SEG) % SEG - 0.15; for (let k = 0; k < 3; k++) { const z = z0 + k * SEG; if (z < 3.3 && z < gz - 0.05) out.push({ k: d.k, X: d.X, v: d.v, z }); } } DECO = out;
}""")
rep("for (const d of DECO) if (d.z > -0.12 && d.z < 1.06) L.push({ z: d.z, f: () => drawDeco(d, time) });", "for (const d of DECO) if (d.z > -0.12 && d.z < 3.4) L.push({ z: d.z, f: () => drawDeco(d, time) });\n  if (B.gate && B.scene === 'corridor') L.push({ z: B.gate.z, f: () => drawGate(B.gate.z, B.gate.open, time) });")
rep("&& d.z > -0.12 && d.z < 1.06) hole(", "&& d.z > -0.12 && d.z < 3.4) hole(")

# ---------- démons qui arrivent du fond du couloir ----------
rep("if (from < 0.5) spawnEnemy(img, rand(-0.12, 0.12), 1.02, st);", "if (from < 0.5) spawnEnemy(img, rand(-0.12, 0.12), B.scene === 'corridor' ? rand(1.6, 2.0) : 1.02, st);")
rep("if (e.z > stop && !e.aName) { e.z -= sp * dt;", "if (e.z > stop && !e.aName) { e.z -= sp * dt * (e.z > 1 ? 2.4 : 1);")

# ---------- porte du boss au fond du couloir ----------
rep("function beginWalk() { // le héros avance vers le fond : couloir suivant, ou porte de l'arène\n  const change = sceneFor() !== B.scene;\n  B.walk = { t: 0, dur: change ? 2.0 : 1.5, d0: B.scroll, dist: SEG, change };",
    "function beginWalk() { // le héros avance vers le fond : couloir suivant, ou porte de l'arène\n  const change = sceneFor() !== B.scene, toBoss = change && sceneFor() === 'arena' && B.scene === 'corridor';\n  B.walk = toBoss ? { t: 0, dur: 3.4, d0: B.scroll, dist: 2.0, change, boss: true, gz0: B.gate ? B.gate.z : 2.6 } : { t: 0, dur: change ? 2.0 : 1.5, d0: B.scroll, dist: SEG, change };")
rep("    const w = B.walk; w.t += dt; const q = Math.min(1, w.t / w.dur), e = q < 0.5 ? 2 * q * q : 1 - Math.pow(-2 * q + 2, 2) / 2, ns = w.d0 + w.dist * e, ds = ns - B.scroll; B.scroll = ns;\n    for (const en of B.en) en.z -= ds; // les cadavres restent au sol\n    if (w.change) B.fade = clamp((w.t - (w.dur - 0.6)) / 0.6, 0, 1);",
    """    const w = B.walk; w.t += dt; const q = Math.min(1, w.t / w.dur), qa = w.boss ? Math.min(1, w.t / 2.3) : q, e = qa < 0.5 ? 2 * qa * qa : 1 - Math.pow(-2 * qa + 2, 2) / 2, ns = w.d0 + w.dist * e, ds = ns - B.scroll; B.scroll = ns;
    for (const en of B.en) en.z -= ds; // les cadavres restent au sol
    if (w.boss) { B.gate = { z: w.gz0 - w.dist * e, open: clamp((w.t - 2.35) / 0.6, 0, 1) }; if (w.t > 2.35 && !w.creak) { w.creak = 1; B.shake = 5; } B.fade = clamp((w.t - 2.9) / 0.5, 0, 1); }
    else if (w.change) B.fade = clamp((w.t - (w.dur - 0.6)) / 0.6, 0, 1);""")
# la porte est visible au fond pendant l'étape 9 (et disparaît dans l'arène)
rep("  placeDeco();\n  combatTick(dt);", "  if (!(B.walk && B.walk.boss)) B.gate = B.scene === 'corridor' && !S.farm && !B.dun && S.s === 9 ? { z: 2.6, open: 0 } : null;\n  placeDeco();\n  combatTick(dt);")
rep("function drawDeco(d, time) {", r"""function drawGate(z, open, time) { // grand mur du fond avec la porte du boss
  const s = sOf(z), y0 = py(z), xl = sx(-1, z), xr = sx(1, z), W = xr - xl, hw = WALLH * s * 1.7, bi = biome();
  const th = hw, tw = 204 * th / 78; ctx.save(); ctx.beginPath(); ctx.rect(xl, -60, W, y0 + 60); ctx.clip();
  for (let yy = y0 - th; yy > -60 - th; yy -= th) for (let x = xl - tw * 0.25; x < xr; x += tw) ctx.drawImage(IMG.tiles, 58, bi.awall, 204, 78, x, yy, tw, th);
  ctx.fillStyle = `rgba(0,0,0,${0.35 + (1 - s) * 0.3})`; ctx.fillRect(xl, -60, W, y0 + 60); ctx.restore();
  // ouverture en arche
  const dw = W * 0.44, dh = hw * 0.92, dx = CX - dw / 2, dy = y0 - dh, r = dw / 2;
  const arch = () => { ctx.beginPath(); ctx.moveTo(dx, y0); ctx.lineTo(dx, dy + r); ctx.arc(CX, dy + r, r, Math.PI, 0); ctx.lineTo(dx + dw, y0); ctx.closePath(); };
  ctx.save(); arch(); ctx.clip();
  const g2 = ctx.createRadialGradient(CX, y0 - dh * 0.35, 4, CX, y0 - dh * 0.35, dh); g2.addColorStop(0, `rgba(255,70,60,${0.25 + open * 0.75})`); g2.addColorStop(1, 'rgba(30,0,6,1)'); ctx.fillStyle = g2; ctx.fillRect(dx, dy, dw, dh);
  // battants : charnières sur les côtés, ils pivotent vers l'intérieur de la salle
  for (const side of [-1, 1]) {
    const lw = dw / 2 * (1 - open * 0.92), x0 = side < 0 ? dx : dx + dw - lw;
    const wg = ctx.createLinearGradient(x0, 0, x0 + lw, 0); wg.addColorStop(0, '#2a170e'); wg.addColorStop(0.5, '#4a2c18'); wg.addColorStop(1, '#22120a'); ctx.fillStyle = wg; ctx.fillRect(x0, dy, lw, dh);
    ctx.fillStyle = 'rgba(0,0,0,.35)'; for (let i = 1; i < 4; i++) ctx.fillRect(x0 + lw * i / 4, dy, Math.max(1, s * 2), dh);
    ctx.fillStyle = '#5c5a66'; for (const f of [0.22, 0.55, 0.85]) ctx.fillRect(x0, dy + dh * f, lw, Math.max(2, 5 * s));
    ctx.fillStyle = '#9a98a8'; for (const f of [0.22, 0.55, 0.85]) for (let i = 0; i < 3; i++) ctx.fillRect(x0 + lw * (0.2 + i * 0.3), dy + dh * f + 1, Math.max(1, 2.5 * s), Math.max(1, 2.5 * s));
    if (open < 0.5) { ctx.strokeStyle = '#b8902a'; ctx.lineWidth = Math.max(1, 3 * s); ctx.beginPath(); ctx.arc(side < 0 ? x0 + lw - 10 * s : x0 + 10 * s, dy + dh * 0.62, 7 * s, 0, TAU); ctx.stroke(); }
  }
  ctx.restore();
  // encadrement de pierre + lueur rouge
  ctx.strokeStyle = '#2a1a1e'; ctx.lineWidth = Math.max(3, 10 * s); arch(); ctx.stroke(); ctx.strokeStyle = '#8a6a5a'; ctx.lineWidth = Math.max(1, 3 * s); arch(); ctx.stroke();
  ctx.globalCompositeOperation = 'lighter'; glow(CX, y0 - dh * 0.5, dw * (0.6 + open * 0.8), 'rgba(255,40,50,1)', 0.18 + open * 0.45 + Math.sin(time * 3) * 0.04); ctx.globalCompositeOperation = 'source-over';
  // crâne au-dessus de la porte
  const ky = dy - 10 * s; ctx.fillStyle = '#d8cfc0'; ctx.beginPath(); ctx.arc(CX, ky, 9 * s, 0, TAU); ctx.fill(); ctx.fillStyle = '#ff3040'; ctx.fillRect(CX - 5 * s, ky - 2 * s, 3 * s, 3 * s); ctx.fillRect(CX + 2 * s, ky - 2 * s, 3 * s, 3 * s);
}
function drawDeco(d, time) {""")
# lumière de la porte dans le calque d'ombre
rep("  for (const s of B.shots) if (!s.solid) hole(", "  if (B.gate && B.scene === 'corridor') hole(CX, py(B.gate.z) - WALLH * sOf(B.gate.z) * 0.8, 160 * sOf(B.gate.z) + 40 + B.gate.open * 80, 0.6 + B.gate.open * 0.35);\n  for (const s of B.shots) if (!s.solid) hole(")

open(P, 'w').write(s)
print('ok')
