P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v12.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)

# ---------- un seul héros jouable : le Chevalier de la mort ----------
rep("  chevalier: { n: 'Le Chevalier de la mort', key: 'chevalier', fx: 'arc', atk: 1.15, hp: 1.2, spd: 1.0, sc: 1.55, leech: 0.03 },",
    "  chevalier: { n: 'Le Chevalier de la mort', key: 'chevalier', fx: 'arc', atk: 1.15, hp: 1.2, spd: 1.0, sc: 1.85, leech: 0.03 },")
rep("S.seals = Object.assign(", """S.hero = 'chevalier';
S.comps = S.comps || { archere: { lv: 1 } }; S.party = S.party || ['archere', null];
S.seals = Object.assign(""")

# ---------- compagnons ----------
rep("function power(st) {", r"""// ================= compagnons =================
const COMPS = {
  archere: { unlock: 1, rate: 1.5, pct: 28, d: 'Tirs rapides à l\'arc' },
  mage: { unlock: 2, rate: 0.9, pct: 38, chill: 1, d: 'Ses tirs de givre ralentissent' },
  sorcier: { unlock: 3, rate: 0.8, pct: 44, splash: 1, d: 'Boules de feu explosives' },
  paladin: { unlock: 4, rate: 0.7, pct: 55, heal: 1, d: 'Chaque coup soigne le héros de 1 % des PV' },
  seigneur: { unlock: 5, rate: 0.85, pct: 60, d: 'Projectiles d\'ombre dévastateurs' },
};
const compLv = id => (S.comps[id] || { lv: 0 }).lv;
const compDmgPct = id => COMPS[id].pct * (1 + 0.12 * (Math.max(1, compLv(id)) - 1));
const compRate = id => COMPS[id].rate * (1 + 0.03 * (Math.max(1, compLv(id)) - 1));
const compCost = id => Math.round(200 * Math.pow(1.6, compLv(id) - 1));
const PARTY_X = [-0.34, 0.34];
function compFire(id, i) {
  const L = B.en.filter(e => !e.dead && e.spawn <= 0 && e.z < 1.05); if (!L.length) return; const C = COMPS[id], H = HEROES[id], st = heroStats();
  const t = L.reduce((a, b) => (hyp((b.X - PARTY_X[i]) * 0.6, b.z) < hyp((a.X - PARTY_X[i]) * 0.6, a.z) ? b : a));
  const crit = Math.random() * 100 < st.crit * 0.5, dmg = st.atk * compDmgPct(id) / 100 * (crit ? st.cdmg / 100 : 1) * rand(0.9, 1.1);
  B.shots.push({ X: PARTY_X[i], z: 0.0, h: 30, tg: t, dmg, crit, t: 0, fx: H.fx, solid: H.solid, splash: !!C.splash, splashK: 0.35, chill: !!C.chill, wr: -1, comp: id });
  const cs = B.cs[i] = B.cs[i] || {}; cs.shootT = 0.3; cs.face = Math.atan2(-(py(t.z) - YF), sx(t.X, t.z) - (CX + PARTY_X[i] * HW));
}
function drawComp(i, time) {
  const id = S.party[i]; if (!id || !S.comps[id]) return; const H = HEROES[id], cs = (B.cs || [])[i] || {}, x = CX + PARTY_X[i] * HW, y = YF + 10, sc = H.sc * 0.66;
  let anim, fr, di = cs.shootT > 0 ? dirIdx(cs.face || Math.PI / 2) : 2;
  if (B.walk) { anim = 'course'; fr = time * 16 + i * 5; } else if (cs.shootT > 0) { anim = 'tir'; fr = (1 - cs.shootT / 0.3) * 14; } else { anim = 'idle'; fr = time * 12 + i * 7; }
  ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(x, y, 14, 4, 0, 0, TAU); ctx.fill();
  sprH(H.key, anim + '_' + di, fr, x, y, sc);
}
function power(st) {""")
rep("function power(st) { st = st || heroStats(); return Math.round(st.atk * st.rate * (1 + st.crit / 100 * (st.cdmg / 100 - 1)) * 12 + st.pv * 0.6 + st.def * 9 + st.regen * 20); }",
    "function power(st) { st = st || heroStats(); const cp = S.party.reduce((a, id) => a + (id && S.comps[id] ? st.atk * compDmgPct(id) / 100 * compRate(id) * 12 : 0), 0); return Math.round(st.atk * st.rate * (1 + st.crit / 100 * (st.cdmg / 100 - 1)) * 12 + cp + st.pv * 0.6 + st.def * 9 + st.regen * 20); }")
# tir des compagnons dans la boucle
rep("    if (!B.walk && h.cd <= 0 && B.en.some(e => !e.dead && e.spawn <= 0 && e.z < 1.05)) { heroFire(); h.cd = 1 / st.rate; }",
    """    if (!B.walk && h.cd <= 0 && B.en.some(e => !e.dead && e.spawn <= 0 && e.z < 1.05)) { heroFire(); h.cd = 1 / st.rate; }
    B.cs = B.cs || []; for (let i = 0; i < 2; i++) { const id = S.party[i]; if (!id || !S.comps[id]) continue; const cs = B.cs[i] = B.cs[i] || { cd: rand(0.2, 0.8) }; cs.cd -= dt; cs.shootT = (cs.shootT || 0) - dt; if (!B.walk && cs.cd <= 0) { compFire(id, i); cs.cd = 1 / compRate(id); } }""")
# soin du paladin
rep("if (crit && st.critFreeze && !e.boss) e.frozen = Math.max(e.frozen || 0, 1);", "if (crit && st.critFreeze && !e.boss) e.frozen = Math.max(e.frozen || 0, 1);")
rep("if (!e.dead) { hitEnemy(e, s.dmg, s.crit);", "if (!e.dead) { hitEnemy(e, s.dmg, s.crit); if (s.comp === 'paladin') B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + B.hero.hpMax * 0.01);")
# dessin : compagnons de part et d'autre, juste derrière le héros
rep("  L.push({ z: 0, f: () => drawHero(time) });", "  L.push({ z: 0, f: () => drawHero(time) });\n  L.push({ z: -0.02, f: () => { drawComp(0, time); drawComp(1, time); } });")

# ---------- onglet Héros : plus de choix de héros, place aux compagnons ----------
a = s.index('    <h3 style="margin-top:16px">Choisir le héros</h3>'); b = s.index("\n", s.index("document.querySelectorAll('[data-h]')", a))
s = s[:a] + r"""    <h3 style="margin-top:16px">Compagnons</h3><p style="margin:0 0 8px;color:var(--dim);font:700 12px/1.4 var(--b)">Ils se battent à tes côtés. 2 places : à gauche et à droite du chevalier.</p>
    <div class="party">${[0, 1].map(i => { const id = S.party[i]; return `<div class="pslot ${id ? '' : 'empty'}">${id ? `<canvas data-pc="${id}" width="64" height="64"></canvas><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><small>Nv ${compLv(id)}</small>` : `<b>+</b><small>${i ? 'Droite' : 'Gauche'}</small>`}</div>`; }).join('')}</div>
    <div class="comps">${Object.keys(COMPS).map(id => { const C = COMPS[id], o = S.comps[id], open = S.c >= C.unlock, inP = S.party.indexOf(id); return `<div class="comp ${o ? '' : 'lock'}"><canvas data-hc="${id}" width="72" height="72"></canvas><div class="ci"><b>${HEROES[id].n.replace(/^(Le|La|L') ?/, '')}</b><small>${C.d}</small><small>${o ? `Nv ${o.lv} · ${Math.round(compDmgPct(id))} % de ton attaque · ${compRate(id).toFixed(2)} tirs/s` : open ? 'Prêt à rejoindre ta troupe' : `Se débloque au chapitre ${C.unlock}`}</small></div><div class="cb">${o ? `<button class="btn gold" type="button" data-up="${id}" ${S.gold < compCost(id) ? 'disabled' : ''}>Niveau +1<small>${fmt(compCost(id))} or</small></button><button class="btn ${inP >= 0 ? 'red' : ''}" type="button" data-pt="${id}">${inP >= 0 ? 'Retirer' : 'Équiper'}</button>` : `<button class="btn gold" type="button" data-rc="${id}" ${open ? '' : 'disabled'}>Recruter</button>`}</div></div>`; }).join('')}</div></div>`;
    document.querySelectorAll('[data-hc],[data-pc]').forEach(c => { const id = c.dataset.hc || c.dataset.pc, H = HEROES[id], big = !!c.dataset.hc, W = c.width; const g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, W, W); sprH(H.key, 'idle_6', performance.now() / 80, W / 2, W - 2, H.sc * (big ? 0.62 : 0.55), 1, g); requestAnimationFrame(draw); }; draw(); });
    document.querySelectorAll('[data-rc]').forEach(b => b.onclick = () => { const id = b.dataset.rc; S.comps[id] = { lv: 1 }; const f = S.party.indexOf(null); if (f >= 0) S.party[f] = id; save(); toast(`${HEROES[id].n} rejoint ta troupe`); ui(); });
    document.querySelectorAll('[data-up]').forEach(b => b.onclick = () => { const id = b.dataset.up, c = compCost(id); if (S.gold < c) return; S.gold -= c; S.comps[id].lv++; save(); ui(); });
    document.querySelectorAll('[data-pt]').forEach(b => b.onclick = () => { const id = b.dataset.pt, i = S.party.indexOf(id); if (i >= 0) S.party[i] = null; else { const f = S.party.indexOf(null); S.party[f >= 0 ? f : 1] = id; } B.cs = []; save(); ui(); });""" + s[b:]

rep(".eveil{display:grid;gap:6px}", """.eveil{display:grid;gap:6px}
.party{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}
.pslot{display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:12px;border:2px solid var(--gold);background:radial-gradient(circle at 20% 50%,#4a2030,#160a10);font:800 12px var(--b)}
.pslot canvas{width:52px;height:52px;image-rendering:pixelated}.pslot small{display:block;color:var(--gold2);font:400 12px var(--n)}
.pslot.empty{border-style:dashed;border-color:#5a3040;color:var(--dim);justify-content:center;min-height:66px}.pslot.empty b{font:400 26px var(--n)}
.comps{display:grid;gap:8px}
.comp{display:grid;grid-template-columns:64px 1fr auto;gap:8px;align-items:center;padding:8px;border-radius:12px;background:#ffffff06;border:1.5px solid #ffffff12}
.comp canvas{width:64px;height:64px;image-rendering:pixelated;border-radius:10px;background:radial-gradient(circle at 50% 70%,#3a2030,#14080d)}
.comp.lock canvas{filter:grayscale(1) brightness(.5)}
.ci b{display:block;font:900 14px var(--t);color:var(--gold2)}.ci small{display:block;font:700 11px/1.35 var(--b);color:var(--dim)}
.cb{display:flex;flex-direction:column;gap:6px}.cb .btn{min-height:40px;font-size:13px;padding:4px 10px}""")

# admin : tout débloquer
rep('<button class="btn" data-a="allsp" type="button">Tous les sorts Nv 5</button>', '<button class="btn" data-a="allsp" type="button">Tous les sorts Nv 5</button><button class="btn" data-a="allcp" type="button">Tous les compagnons Nv 10</button>')
rep("allsp: () => {", "allcp: () => { Object.keys(COMPS).forEach(k => S.comps[k] = { lv: 10 }); },\n    allsp: () => {")

open(P, 'w').write(s)
print('ok')
