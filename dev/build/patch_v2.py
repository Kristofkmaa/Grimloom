import re
P = '/home/claude/grimloom/src.html'
s = open('/home/claude/grimloom/src.v1.html').read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------------- CSS ----------------
a = s.index('/*FONT*/') + len('/*FONT*/'); b = s.index('</style>')
s = s[:a] + r'''
:root{--bg:#0b0609;--paper:#ffce70;--paper2:#f5b94e;--cream:#fff1c8;--ink:#411d31;--red:#cc1e48;--gold:#ffc46a;--dim:#b8a0a8;--line:#3a1a26}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--bg);color:#f3e6e2;font-family:Dungeon,monospace;overflow:hidden;touch-action:manipulation;-webkit-user-select:none;user-select:none}
button{font-family:Dungeon,monospace}
#app{position:fixed;inset:0;margin:0 auto;max-width:480px;display:flex;flex-direction:column;background:#0b0609;box-shadow:0 0 60px #000}
#stageWrap{position:relative;flex:none;overflow:hidden;background:#000}
#bt{display:block;width:100%;height:100%;image-rendering:pixelated}
#hud{position:absolute;left:0;right:0;top:0;padding:calc(6px + env(safe-area-inset-top)) 8px 0;display:grid;grid-template-columns:1fr auto auto;gap:6px;align-items:center;pointer-events:none}
.pill{display:flex;align-items:center;gap:6px;height:28px;padding:0 10px;background:#0b0609d0;border:2px solid #5a2a3a;border-radius:14px;font-size:12px;white-space:nowrap}
.pill b{font-weight:400;color:var(--gold)}
#stagePill{justify-self:start;color:#ffd0d6}
#waveBox{grid-column:1/-1;position:relative;height:16px;background:#0b0609d0;border:2px solid #5a2a3a;border-radius:8px;overflow:hidden}
#waveBar{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(#ffd88a,#d88a2a);transition:width .2s}
#waveBox.boss #waveBar{background:linear-gradient(#ff6070,#a8142a)}
#waveTxt{position:absolute;inset:0;text-align:center;font-size:8px;line-height:12px;color:#fff;text-shadow:1px 1px 0 #000}
#powerTag{position:absolute;left:8px;bottom:8px;pointer-events:none;color:#ffd0d6}
#powerTag b{color:#ff8a9a}
.coin{width:12px;height:12px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff0a0,#f0a020 60%,#a05a10);border:1px solid #5a2a00;flex:none}
.ico{width:14px;height:14px;flex:none;image-rendering:pixelated}
#panel{flex:1;min-height:0;overflow:auto;padding:10px 10px 12px;background:linear-gradient(#170b11,#0b0609);overscroll-behavior:contain}
.paper{background:var(--paper);color:var(--ink);border:3px solid var(--ink);border-radius:4px;box-shadow:inset 0 -3px 0 #0002,0 3px 0 #000}
.row{display:flex;gap:8px;align-items:center}
.sec{display:flex;justify-content:space-between;align-items:baseline;margin:2px 2px 8px;font-size:12px;color:var(--dim)}
.sec b{font-weight:400;font-size:16px;color:#ffd0d6}
#equip{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.slot{aspect-ratio:1;position:relative;border:3px solid var(--ink);border-radius:6px;background:#3a2028;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;box-shadow:inset 0 -4px 0 #0004,0 2px 0 #000;padding:0}
.slot.empty{background:#21121a;border-color:#4a2a36;border-style:dashed}
.slot canvas{width:48px;height:48px;image-rendering:pixelated}
.slot .nm{font-size:8px;color:#fff;text-shadow:1px 1px 0 #000;line-height:9px}
.slot.empty .nm{color:#8a6a76;text-shadow:none}
.slot .lv{position:absolute;left:3px;top:2px;font-size:8px;color:#fff;text-shadow:1px 1px 0 #000}
.slot:active{transform:translateY(2px)}
#odds{display:flex;flex-wrap:wrap;gap:4px;margin-top:10px}
#odds span{font-size:8px;padding:4px 6px;border-radius:4px;background:#1e1016;border:1px solid #3a1a26}
#dock{flex:none;display:grid;grid-template-columns:72px 1fr 72px;gap:8px;padding:8px 10px;background:linear-gradient(#1c0d14,#12080d);border-top:2px solid var(--line)}
.dk{position:relative;height:60px;border:3px solid var(--ink);border-radius:6px;background:var(--paper2);color:var(--ink);font-size:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;box-shadow:inset 0 -4px 0 #0003;padding:0}
.dk b{font-weight:400;font-size:16px}
.dk:active,#forgeBtn:active{transform:translateY(2px);box-shadow:inset 0 -2px 0 #0003}
.dk .dot{position:absolute;right:-5px;top:-5px;width:14px;height:14px;border-radius:50%;background:#3ad05a;border:2px solid var(--ink)}
.dk.red{background:var(--red);color:#fff3d8}
.dk.off{visibility:hidden}
#forgeBtn{height:60px;border:3px solid var(--ink);border-radius:6px;background:linear-gradient(#ff5a6a,#a8142a);color:#fff3d8;font-size:16px;cursor:pointer;box-shadow:inset 0 -6px 0 #0004;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:0}
#forgeBtn small{font-size:8px;color:#ffd8b0;display:flex;align-items:center;gap:4px}
#forgeBtn.empty{filter:grayscale(.7) brightness(.8)}
.btn{font-size:12px;min-height:48px;border:3px solid var(--ink);border-radius:6px;background:var(--paper2);color:var(--ink);padding:8px 10px;cursor:pointer;box-shadow:inset 0 -4px 0 #0003}
.btn.red{background:var(--red);color:#fff3d8}
.btn:disabled{opacity:.45}
.btn:active{transform:translateY(2px)}
.btn small{display:block;font-size:8px;margin-top:3px;opacity:.85}
.small{font-size:8px;color:var(--ink)}
#nav{display:grid;grid-template-columns:repeat(4,1fr);flex:none;border-top:2px solid var(--line);background:#12080d;padding-bottom:env(safe-area-inset-bottom)}
#nav button{font-size:12px;background:none;border:0;color:var(--dim);height:50px;cursor:pointer;position:relative}
#nav button.on{color:#ffd0d6;background:#2a0f1a}
#nav button.on::after{content:'';position:absolute;left:25%;right:25%;top:0;height:3px;background:var(--red)}
#modal{position:fixed;inset:0;background:#000b;display:flex;align-items:flex-end;justify-content:center;z-index:9}
#modal[hidden]{display:none}
#mbox{width:100%;max-width:480px;max-height:88%;overflow:auto;padding:14px 12px calc(14px + env(safe-area-inset-bottom));border-radius:14px 14px 0 0;border-bottom:0;animation:up .18s ease-out}
@keyframes up{from{transform:translateY(40px);opacity:.3}}
#mbox h3{display:flex;justify-content:space-between;align-items:center}
.x{font-size:16px;background:none;border:0;color:var(--ink);width:40px;height:40px;cursor:pointer}
.card{border:3px solid var(--ink);border-radius:6px;padding:10px;background:var(--cream)}
.card + .card{margin-top:8px}
.card.cur{background:#f3dfb0;opacity:.95}
.card .hd{display:flex;gap:10px;align-items:center;margin-bottom:6px}
.card canvas{width:56px;height:56px;image-rendering:pixelated;border:3px solid var(--ink);border-radius:4px;flex:none}
.card h4{margin:0 0 4px;font-weight:400;font-size:16px}
.card .tag{font-size:8px;color:var(--ink);opacity:.7;margin-bottom:4px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:2px 10px}
.stat{font-size:8px;line-height:14px;display:flex;justify-content:space-between;gap:6px}
.stat em{font-style:normal}
.up{color:#1a8a3a}.down{color:#c8142a}
.pw{display:flex;justify-content:space-between;align-items:center;margin-top:6px;padding-top:6px;border-top:2px dashed #41193133;font-size:12px}
.rar{font-size:8px}
h3{margin:2px 0 10px;font-weight:400;font-size:16px;color:var(--red)}
.list{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.list div{display:flex;flex-direction:column;gap:4px;background:var(--cream);border:2px solid #41193144;border-radius:4px;padding:6px 8px;font-size:8px}
.list b{font-weight:400;font-size:12px;color:var(--red)}
.heroes{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.heroes button{font-size:8px;border:3px solid var(--ink);border-radius:6px;background:var(--cream);color:var(--ink);padding:4px 2px 8px;cursor:pointer;min-height:100px}
.heroes button.on{background:var(--red);color:#fff}
.heroes canvas{width:72px;height:72px;image-rendering:pixelated;display:block;margin:0 auto 2px}
#heroHead{display:flex;align-items:center;gap:10px;margin-bottom:10px}
#heroHead canvas{width:80px;height:100px;image-rendering:pixelated;background:#0002;border:2px solid #41193144;border-radius:6px}
#heroHead div{font-size:8px;line-height:14px}
#heroHead h4{margin:0 0 4px;font-weight:400;font-size:16px;color:var(--red)}
#toast{position:fixed;left:50%;top:84px;transform:translateX(-50%);z-index:10;pointer-events:none;display:flex;flex-direction:column;align-items:center}
#toast div{background:var(--paper);color:var(--ink);border:3px solid var(--ink);border-radius:6px;padding:8px 12px;font-size:12px;margin-bottom:4px;white-space:nowrap;animation:up .15s}
.soon{padding:14px;font-size:12px;line-height:20px}
''' + s[b:]

# ---------------- HTML ----------------
a = s.index('<div id="app">'); b = s.index('<div id="modal"')
s = s[:a] + '''<div id="app">
  <div id="stageWrap">
    <canvas id="bt" width="720" height="840" aria-label="Combat"></canvas>
    <div id="hud">
      <div class="pill" id="stagePill"><span id="stage">1-1</span></div>
      <div class="pill"><i class="coin"></i><b id="gold">0</b></div>
      <div class="pill"><svg class="ico" viewBox="0 0 8 8" shape-rendering="crispEdges"><rect x="1" y="1" width="5" height="2" fill="#c8c8d8"/><rect x="1" y="1" width="1" height="3" fill="#8888a0"/><rect x="3" y="3" width="1" height="5" fill="#a0602a"/></svg><b id="ham">0</b></div>
      <div id="waveBox"><i id="waveBar"></i><span id="waveTxt"></span></div>
    </div>
    <div class="pill" id="powerTag">Puissance <b id="pow">0</b></div>
  </div>
  <div id="panel"></div>
  <div id="dock">
    <button class="dk" id="forgeLv" type="button">Forge<b id="flv">1</b><i class="dot" id="fdot" hidden></i></button>
    <button id="forgeBtn" type="button">FORGER<small><svg class="ico" viewBox="0 0 8 8" shape-rendering="crispEdges"><rect x="1" y="1" width="5" height="2" fill="#fff"/><rect x="3" y="3" width="1" height="5" fill="#ffd8b0"/></svg><span id="hamN">0</span> marteaux</small></button>
    <button class="dk red" id="bossBtn" type="button">Boss<b>!</b></button>
  </div>
  <nav id="nav"><button data-t="forge" class="on" type="button">Équipement</button><button data-t="hero" type="button">Héros</button><button data-t="skills" type="button">Pouvoirs</button><button data-t="dungeon" type="button">Donjons</button></nav>
</div>
''' + s[b:]

# ---------------- chargement des démons animés ----------------
rep("for (const k in ASSETS) if (ASSETS[k].src) { const im = new Image(); im.src = ASSETS[k].src; IMG[k] = im; }",
    "for (const k in ASSETS) if (ASSETS[k].src) { const im = new Image(); im.src = ASSETS[k].src; IMG[k] = im; }\nfor (const k in ASSETS.DEM) { const im = new Image(); im.src = ASSETS.DEM[k].src; IMG['D_' + k] = im; }")

# ---------------- vue : canvas adapté à l'écran ----------------
rep("let FLOOR = null;", '''let FLOOR = null, OFFY = 0;
function fit() {
  const wrap = $('stageWrap'), w = wrap.clientWidth || 360, nat = w * BH / BW, h = Math.round(Math.min(nat, Math.max(280, innerHeight * 0.5)));
  wrap.style.height = h + 'px'; const dpr = Math.min(2, devicePixelRatio || 1); cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
  OFFY = (h * BW / w - BH) * 0.72; // on rogne surtout le haut du mur du fond
}
addEventListener('resize', fit);''')
rep("const k = cv.width / BW; ctx.setTransform(k, 0, 0, k, 0, 0);", "const k = cv.width / BW; ctx.setTransform(k, 0, 0, k, 0, OFFY * k); ctx.fillStyle = '#000'; ctx.fillRect(0, -40, BW, BH + 80);")
# barre de vague -> HUD DOM
a = s.index("  // progression de la vague\n"); b = s.index("  if (B.banner)")
s = s[:a] + s[b:]

# ---------------- ennemis animés ----------------
rep("""function spawnEnemy(img, X, z, st, boss) {
  const ranged = !!RANGED[img], elite = /elite/.test(img);""", """function spawnEnemy(img, X, z, st, boss) {
  const ranged = !!RANGED[img], elite = /elite/.test(img), key = img === 'p_idle' ? 'spawn1' : img, D = ASSETS.DEM[key].anims;
  const intro = boss && D.taunt_S ? { aName: 'taunt', aT: 0, aDur: D.taunt_S[1] / 10, hitDone: 1 } : {};""")
rep("spawn: 0.5, flip: false, chill: 0, dead: 0 });", "spawn: 0.5, flip: false, chill: 0, dead: 0, key, dir: 'S', hitT: 0, aName: null, ...intro });")
rep("""    e.cd -= dt;
    if (e.cd <= 0 && !h.dead) { if (e.z <= stop + 0.02) { e.cd = e.boss ? 1.6 : rand(1.2, 1.8); e.atkT = 0.3; if (e.ranged || e.boss && Math.random() < 0.5) B.es.push({ X: e.X, z: e.z, h: 30, dmg: e.atk, t: 0, fx: e.boss ? 'pfeu' : pick(['pfeu', 'pmort', 'pglace']) }); else hurtHero(e.atk); } }
    e.atkT = (e.atkT || 0) - dt;""", """    e.cd -= dt; e.hitT -= dt;
    // direction écran vers le héros : S, SE/SO, E/O
    { const dx = CX - sx(e.X, e.z), dy = Math.max(1, YF - py(e.z)), r = Math.abs(dx) / dy; e.dir = r < 0.42 ? 'S' : (dx > 0 ? (r < 1.7 ? 'SE' : 'E') : (r < 1.7 ? 'SW' : 'W')); }
    if (e.cd <= 0 && !h.dead && !e.aName && e.z <= stop + 0.02) {
      const D = ASSETS.DEM[e.key].anims, opts = ['atk', 'atk2', 'atk3', 'atk4', 'atk5', 'atk6'].filter(a => D[a + '_S']);
      e.aName = e.boss ? opts[(e.atkN = (e.atkN || 0) + 1) % opts.length] : e.elite ? pick(opts) : 'atk';
      e.aT = 0; e.aDur = D[e.aName + '_S'][1] / 13; e.hitDone = 0; e.shoot = e.ranged || (e.boss && Math.random() < 0.5); e.cd = (e.boss ? 1.0 : rand(0.8, 1.3)) + e.aDur;
    }
    if (e.aName) { e.aT += dt; if (!e.hitDone && e.aT >= e.aDur * 0.55) { e.hitDone = 1; if (!h.dead) { if (e.shoot) B.es.push({ X: e.X, z: e.z, h: 30, dmg: e.atk, t: 0, fx: e.boss ? 'pfeu' : pick(['pfeu', 'pmort', 'pglace']) }); else hurtHero(e.atk); } } if (e.aT >= e.aDur) e.aName = null; }""")
rep("""    if (e.z > stop) { e.z -= sp * dt;""", """    if (e.z > stop && !e.aName) { e.z -= sp * dt;""")
rep("B.en = B.en.filter(e => !e.dead || e.deadT < 0.7);", "B.en = B.en.filter(e => !e.dead || e.deadT < 1.1);")
rep("if (e.dead) return; e.hp -= dmg; e.flash = 0.1;", "if (e.dead) return; e.hp -= dmg; e.flash = 0.1; if (!e.aName && !e.boss) e.hitT = 0.25;")

a = s.index("function demon(img"); b = s.index("\n", a)
s = s[:a] + r'''const SCR = document.createElement('canvas'), SG = SCR.getContext('2d');
function dem(key, anim, dir, fr, x, y, sc, o) {
  const A = ASSETS.DEM[key], im = IMG['D_' + key]; if (!A || !im.complete) return; o = o || {};
  const flip = dir === 'W' || dir === 'SW', base = dir === 'W' ? 'E' : dir === 'SW' ? 'SE' : dir;
  const R = A.anims[anim + '_' + base] || A.anims[anim + '_S'] || A.anims.walk_S, n = R[1], i = o.loop === false ? clamp(Math.floor(fr), 0, n - 1) : ((Math.floor(fr) % n) + n) % n;
  let src = im, sx0 = i * A.cw, sy0 = R[0] * A.ch;
  if (o.tint) { if (SCR.width < A.cw || SCR.height < A.ch) { SCR.width = Math.max(SCR.width, A.cw); SCR.height = Math.max(SCR.height, A.ch); } SG.globalCompositeOperation = 'copy'; SG.drawImage(im, sx0, sy0, A.cw, A.ch, 0, 0, A.cw, A.ch); SG.globalCompositeOperation = 'source-in'; SG.fillStyle = o.tint; SG.fillRect(0, 0, A.cw, A.ch); src = SCR; sx0 = 0; sy0 = 0; }
  ctx.save(); ctx.imageSmoothingEnabled = false; if (o.alpha !== undefined) ctx.globalAlpha = o.alpha;
  ctx.translate(Math.round(x), Math.round(y)); ctx.scale((flip ? -1 : 1) * sc, sc * (o.sy || 1));
  ctx.drawImage(src, sx0, sy0, A.cw, A.ch, -A.ax, -(A.ch - A.foot), A.cw, A.ch); ctx.restore();
}''' + s[b:]

a = s.index("function drawEnemy(e, time) {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r'''function drawEnemy(e, time) {
  const s = sOf(e.z), x = sx(e.X, e.z), y = py(e.z), A = ASSETS.DEM[e.key], sc = (e.boss ? 2.3 : e.elite ? 1.75 : 1.55) * s;
  const al = e.dead ? clamp((1.1 - e.deadT) / 0.35, 0, 1) : e.spawn > 0 ? 1 - e.spawn / 0.5 : 1;
  ctx.fillStyle = `rgba(0,0,0,${0.35 * al})`; ctx.beginPath(); ctx.ellipse(x, y, Math.min(30, A.bh * 0.32) * sc, 5 * sc, 0, 0, TAU); ctx.fill();
  let anim = 'walk', fr = e.t * 12, loop = true;
  if (e.dead) { anim = 'die'; fr = e.deadT * 13; loop = false; }
  else if (e.aName) { anim = e.aName; fr = e.aT * 13; loop = false; }
  else if (e.hitT > 0) { anim = 'hit'; fr = (0.25 - e.hitT) * 30; loop = false; }
  else if (!e.moving && A.anims.idle_S) { anim = 'idle'; fr = e.t * 9; }
  else if (!e.moving) fr = e.t * 7;
  const o = { alpha: al, loop };
  if (e.boss || e.elite) { ctx.globalCompositeOperation = 'lighter'; glow(x, y - A.bh * 0.5 * sc, 46 * sc, e.boss ? 'rgba(255,30,50,1)' : 'rgba(255,190,80,1)', 0.3 * al); ctx.globalCompositeOperation = 'source-over'; }
  dem(e.key, anim, e.dir, fr, x, y, sc, o);
  if (e.flash > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.75 * al, loop, tint: '#ffffff' });
  if (e.chill > 0) dem(e.key, anim, e.dir, fr, x, y, sc, { alpha: 0.35 * al, loop, tint: '#7ae8ff' });
  if (!e.dead && e.spawn <= 0 && !e.boss) { const w = 26 * Math.max(0.6, s), hy = y - A.bh * sc - 6; ctx.fillStyle = 'rgba(0,0,0,.7)'; ctx.fillRect(x - w / 2 - 1, hy - 1, w + 2, 4); ctx.fillStyle = e.elite ? '#ffc46a' : '#e0283c'; ctx.fillRect(x - w / 2, hy, w * clamp(e.hp / e.max, 0, 1), 2); }
}
''' + s[b:]

# ---------------- interface ----------------
a = s.index("function slotHTML(sl)"); b = s.index("function heroPortrait(time)")
s = s[:a] + r'''function slotHTML(sl) { const it = S.eq[sl.id]; return `<button type="button" class="slot${it ? '' : ' empty'}" data-s="${sl.id}" style="${it ? `background:linear-gradient(${RAR[it.r].c}cc,${RAR[it.r].c}66);border-color:${RAR[it.r].c}` : ''}"><canvas data-ic="${sl.id}"></canvas><span class="nm">${sl.n}</span>${it ? `<span class="lv">${it.L}</span>` : ''}</button>`; }
let tab = 'forge';
function ui() {
  uiTop(); const st = heroStats();
  $('dock').style.display = tab === 'forge' ? '' : 'none';
  if (tab === 'forge') {
    $('panel').innerHTML = `<div class="sec"><span>${HEROES[S.hero].n}</span><span>ATQ <b>${fmt(st.atk)}</b> · PV <b>${fmt(st.pv)}</b></span></div>
    <div id="equip">${SLOTS.map(slotHTML).join('')}</div>
    <div class="sec" style="margin-top:12px"><span>Chances de la forge (niveau ${S.forge})</span></div><div id="odds">${odds()}</div>`;
    document.querySelectorAll('[data-ic]').forEach(c => eqIcon(c, S.eq[c.dataset.ic], c.dataset.ic));
    document.querySelectorAll('[data-s]').forEach(el => el.onclick = () => { const it = S.eq[el.dataset.s]; if (it) showItem(it, null); else toast('Forge pour trouver : ' + SLOTS.find(x => x.id === el.dataset.s).n); });
  } else if (tab === 'hero') {
    const H = HEROES[S.hero];
    $('panel').innerHTML = `<div class="paper" style="padding:10px"><div id="heroHead"><canvas id="heroC" width="80" height="100"></canvas><div><h4>${H.n}</h4>Attaque ×${H.atk} · Vie ×${H.hp}<br>Cadence ×${H.spd}${H.splash ? '<br>Tirs explosifs' : ''}${H.chill ? '<br>Ralentit les démons' : ''}${H.leech ? '<br>Vole la vie' : ''}</div></div>
    <div class="list">${[['Puissance', fmt(power(st))], ['Attaque', fmt(st.atk)], ['Points de vie', fmt(st.pv)], ['Défense', fmt(st.def)], ['Attaques / s', st.rate.toFixed(2)], ['Critique', st.crit.toFixed(1) + ' %'], ['Dégâts critiques', Math.round(st.cdmg) + ' %'], ['Vol de vie', st.vol.toFixed(1) + ' %'], ['Régénération', st.regen.toFixed(1) + ' %/s'], ['Esquive', st.esq.toFixed(1) + ' %'], ['Meilleure étape', `${Math.floor((S.best - 1) / 10) + 1}-${(S.best - 1) % 10 + 1}`], ['Démons tués', fmt(S.kills)]].map(([a, b]) => `<div><span>${a}</span><b>${b}</b></div>`).join('')}</div>
    <h3 style="margin-top:14px">Choisir le héros</h3><div class="heroes">${Object.entries(HEROES).map(([id, h]) => `<button type="button" data-h="${id}" class="${S.hero === id ? 'on' : ''}"><canvas data-hc="${id}" width="72" height="72"></canvas>${h.n.replace(/^(Le|La|L') ?/, '')}</button>`).join('')}</div></div>`;
    document.querySelectorAll('[data-hc]').forEach(c => { const H = HEROES[c.dataset.hc]; const g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, 72, 72); sprH(H.key, 'idle_6', performance.now() / 80, 36, 70, 0.75, 1, g); requestAnimationFrame(draw); }; draw(); });
    document.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { S.hero = b.dataset.h; save(); B.hero.hpMax = heroStats().pv; B.hero.hp = Math.min(B.hero.hp, B.hero.hpMax); ui(); });
  } else {
    $('panel').innerHTML = `<div class="paper soon"><h3>${tab === 'skills' ? 'Pouvoirs' : 'Donjons'}</h3>${tab === 'skills' ? 'Bientôt : des pouvoirs qui se déclenchent seuls en combat (pluie de feu, nova, blizzard…), à débloquer et améliorer.' : 'Bientôt : des donjons quotidiens qui rapportent des marteaux, de l\'or et des matériaux.'}<br><br>On le construit ensemble à la prochaine étape.</div>`;
  }
}
function odds() { const w = rarityWeights(S.forge), t = w.reduce((a, b) => a + b, 0); return w.map((x, i) => [RAR[i], x / t * 100]).filter(([, p]) => p >= 0.05).map(([r, p]) => `<span style="color:${r.c}">${r.n} ${p < 1 ? p.toFixed(1) : Math.round(p)} %</span>`).join(''); }
function uiTop() {
  hamTick(); $('stage').textContent = S.farm ? `Chapitre ${S.c} · entraînement` : `Chapitre ${S.c} · ${S.s}/10`; $('gold').textContent = fmt(S.gold); $('ham').textContent = S.ham; $('hamN').textContent = S.ham;
  $('pow').textContent = fmt(power()); $('flv').textContent = S.forge; $('fdot').hidden = S.gold < forgeCost(); $('forgeBtn').classList.toggle('empty', S.ham <= 0);
  $('bossBtn').classList.toggle('off', !S.farm);
}
function uiWave() {
  const w = B.wave; if (!w) return; const boss = w.boss && B.en[0], pr = boss ? Math.max(0, B.en[0].hp) / B.en[0].max : w.killed / Math.max(1, w.total);
  $('waveBox').classList.toggle('boss', !!boss); $('waveBar').style.width = (pr * 100).toFixed(1) + '%';
  $('waveTxt').textContent = boss ? `Boss · ${fmt(Math.max(0, B.en[0].hp))}` : S.farm ? `Entraînement · ${w.killed}/${w.total}` : `Vague ${S.s}/10 · ${w.killed}/${w.total}`;
}
function statLines(it, other) {
  const a = itemStats(it), b = other ? itemStats(other) : {}, keys = new Set([...Object.keys(a), ...(other ? Object.keys(b) : [])]);
  return [...keys].map(k => { const va = a[k] || 0, vb = b[k] || 0, d = va - vb, unit = PCT[k] || k === 'atkp' || k === 'pvp' ? ' %' : ''; return `<div class="stat"><span>${STATN[k]}${k === 'atkp' || k === 'pvp' ? ' %' : ''}</span><em>${round2(va)}${unit}${other && d ? ` <span class="${d > 0 ? 'up' : 'down'}">${d > 0 ? '▲' : '▼'}${round2(Math.abs(d))}</span>` : ''}</em></div>`; }).join('');
}
function cardHTML(it, label, other, cls) {
  const sl = SLOTS.find(s => s.id === it.slot), dp = other ? itemPower(it) - itemPower(other) : 0;
  return `<div class="card ${cls || ''}" style="border-color:${RAR[it.r].c}"><div class="tag">${label}</div><div class="hd"><canvas data-ci="${label}"></canvas><div><h4 style="color:${RAR[it.r].c};text-shadow:1px 1px 0 #0005">${sl.n}</h4><div class="rar">${RAR[it.r].n} · niveau ${it.L}</div></div></div><div class="stats">${statLines(it, other)}</div><div class="pw"><span>Puissance</span><span>${fmt(itemPower(it))}${other ? ` <span class="${dp >= 0 ? 'up' : 'down'}">${dp >= 0 ? '▲' : '▼'}${fmt(Math.abs(dp))}</span>` : ''}</span></div></div>`;
}
function sheet(html) { $('mbox').innerHTML = html; $('modal').hidden = false; const x = $('mbox').querySelector('.x'); if (x) x.onclick = closeM; }
function showItem(it, isNew) {
  const cur = S.eq[it.slot];
  if (isNew) {
    const better = !cur || itemPower(it) > itemPower(cur);
    sheet(`<h3>Nouvel objet <button class="x" type="button" aria-label="Fermer">×</button></h3>${cardHTML(it, 'Forgé', cur)}${cur ? cardHTML(cur, 'Équipé actuellement', null, 'cur') : ''}
    <div class="row" style="margin-top:12px"><button class="btn" id="sellB" type="button" style="flex:1">Vendre<small>+${fmt(it.v)} or</small></button><button class="btn ${better ? 'red' : ''}" id="eqB" type="button" style="flex:1.3">Équiper<small>${cur ? `l'ancien est vendu +${fmt(cur.v)} or` : 'emplacement vide'}</small></button></div>`);
    $('mbox').querySelector('.x').onclick = () => { S.gold += it.v; closeM(); };
  } else sheet(`<h3>${SLOTS.find(s => s.id === it.slot).n} <button class="x" type="button" aria-label="Fermer">×</button></h3>${cardHTML(it, 'Équipé', null)}<button class="btn" id="clB" type="button" style="width:100%;margin-top:12px">Fermer</button>`);
  $('mbox').querySelectorAll('[data-ci]').forEach(c => eqIcon(c, c.dataset.ci === 'Forgé' ? it : isNew ? cur : it));
  if (isNew) { $('eqB').onclick = () => { if (cur) S.gold += cur.v; S.eq[it.slot] = it; closeM(); toast(`${SLOTS.find(s => s.id === it.slot).n} équipé`); }; $('sellB').onclick = () => { S.gold += it.v; closeM(); }; }
  else $('clB').onclick = closeM;
}
function showForge() {
  const c = forgeCost();
  sheet(`<h3>Forge niveau ${S.forge} <button class="x" type="button" aria-label="Fermer">×</button></h3><p class="small" style="font-size:12px;line-height:18px;margin:0 0 10px">Chaque niveau augmente les chances d'obtenir des objets rares et leur niveau.</p>
  <div class="list">${(() => { const w = rarityWeights(S.forge), t = w.reduce((a, b) => a + b, 0), w2 = rarityWeights(S.forge + 1), t2 = w2.reduce((a, b) => a + b, 0); return w.map((x, i) => [RAR[i], x / t * 100, w2[i] / t2 * 100]).filter(([, p, q]) => q >= 0.05).map(([r, p, q]) => `<div><span style="color:${r.c};text-shadow:1px 1px 0 #0004">${r.n}</span><b>${p < 1 ? p.toFixed(2) : p.toFixed(1)} % <span class="up" style="font-size:8px">→ ${q < 1 ? q.toFixed(2) : q.toFixed(1)}</span></b></div>`).join(''); })()}</div>
  <button class="btn red" id="upB" type="button" style="width:100%;margin-top:12px" ${S.gold < c ? 'disabled' : ''}>Améliorer la forge<small>${fmt(c)} or · tu as ${fmt(S.gold)}</small></button>`);
  $('upB').onclick = () => { upForge(); showForge(); };
}
function closeM() { $('modal').hidden = true; save(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = Math.min(B.hero.hp, st.pv); ui(); }
function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }
  S.ham--; S.forged++; const it = makeItem(); save();
  sfx('epee', CX, YF - 30, 120, 0.3, -Math.PI / 2); if (it.r >= 3) { burst(CX, YF - 40, RAR[it.r].c, 30, 200); B.shake = 5; }
  showItem(it, true);
}
function upForge() { const c = forgeCost(); if (S.gold < c) return; S.gold -= c; S.forge++; save(); toast(`Forge niveau ${S.forge}`); uiTop(); }
function toast(t) { const d = document.createElement('div'); d.textContent = t; $('toast').appendChild(d); setTimeout(() => d.remove(), 2200); }
document.querySelectorAll('#nav button').forEach(b => b.onclick = () => { tab = b.dataset.t; document.querySelectorAll('#nav button').forEach(x => x.classList.toggle('on', x === b)); ui(); });
$('modal').addEventListener('click', e => { if (e.target.id === 'modal') { if ($('sellB')) return; closeM(); } });
$('forgeBtn').onclick = forge; $('forgeLv').onclick = showForge; $('bossBtn').onclick = () => { S.farm = false; S.s = 10; save(); startWave(); };
''' + s[b:]

rep("function heroPortrait(time) { const c = $('heroC'); if (!c) return; const g = c.getContext('2d'); g.clearRect(0, 0, 120, 150); const H = HEROES[S.hero]; g.fillStyle = 'rgba(65,29,49,.18)'; g.beginPath(); g.ellipse(60, 140, 34, 8, 0, 0, TAU); g.fill(); sprH(H.key, 'idle_6', time * 10, 60, 142, 1.25, 1, g); }",
    "function heroPortrait(time) { const c = $('heroC'); if (!c) return; const g = c.getContext('2d'); g.clearRect(0, 0, 80, 100); const H = HEROES[S.hero]; sprH(H.key, 'idle_6', time * 10, 40, 94, 0.85, 1, g); }")
rep("if (uiT <= 0) { uiT = 0.5; uiTop(); }", "if (uiT <= 0) { uiT = 0.5; uiTop(); } uiWave();")
rep("(function boot() { if (!ready()) return setTimeout(boot, 50); hamTick();", "(function boot() { if (!ready()) return setTimeout(boot, 50); fit(); hamTick();")
rep("window.__G = () => ({ S, B, heroStats, makeItem, power });", "window.__G = () => ({ S, B, heroStats, makeItem, power, startWave, ui, fit });")
open(P, 'w').write(s)
print('ok', len(s))
