P='/home/claude/grimloom/src.html'; s=open(P).read()
def rep(a,b,c=1):
    global s
    assert s.count(a)==c,(s.count(a),a[:90]); s=s.replace(a,b)
rep('<button id="challengeBtn" type="button" hidden></button>','<button id="challengeBtn" type="button" hidden></button>\n    <button id="ultBtn" type="button" aria-label="Sort ultime"><i id="ultFill"></i><svg viewBox="0 0 24 24"><path d="m12 2 3 6.6 7 .7-5.3 4.8 1.6 7L12 17.5 5.7 21l1.6-7L2 9.3l7-.7z" fill="currentColor"/></svg><b id="ultTxt">0%</b></button>')
rep(".kcf{","""#ultBtn{position:absolute;right:10px;bottom:10px;z-index:4;width:62px;height:62px;border-radius:50%;border:2px solid #6a3a48;background:#14080d;padding:0;overflow:hidden;color:#8a6a74;display:grid;place-items:center}
#ultBtn i{position:absolute;left:0;right:0;bottom:0;height:0;background:linear-gradient(#ff9a3a,#b8201c);opacity:.55;transition:height .2s}
#ultBtn svg{position:relative;width:26px;height:26px;margin-top:-8px}
#ultBtn b{position:absolute;bottom:7px;left:0;right:0;font:400 12px var(--n);color:#f0d8c0;text-align:center}
#ultBtn.full{border-color:#ffd27a;color:#fff6c8;animation:ultP .8s ease-in-out infinite alternate;box-shadow:0 0 18px #ff9a3a}
#ultBtn.full i{opacity:.9}
@keyframes ultP{to{transform:scale(1.08);box-shadow:0 0 30px #ffb040}}
.kult{margin-top:6px;padding:6px 8px;border-radius:8px;background:#2a0f18;box-shadow:inset 0 0 0 1px #6a3a48;font:700 11.5px/1.35 var(--b);color:#e8d0d6}.kult b{color:#ffb040;font:900 12px var(--t)}
.kcf{""")
# définitions des ultimes
rep("function castSpell(id) {","""// ================= sorts ultimes (un par forme / voie) =================
const ULT = {
  base_k: ['Lame tournoyante', 'Une vague d\\'acier frappe tous les démons (400 %).'],
  mort: ['Faucheuse', 'Un vortex d\\'ombre frappe tout (500 %) et te soigne de 20 %.'],
  enfer: ['Déluge infernal', '10 météores s\\'abattent sur le champ de bataille (350 % chacun).'],
  givre: ['Hiver éternel', 'Gèle tous les démons 4 s et les frappe (400 %).'],
  base_h: ['Pluie de carreaux', '14 carreaux tombent du ciel (180 % chacun).'],
  ombre: ['Danse des ombres', 'Des lames frappent chaque démon 3 fois, toujours en critique.'],
  sang: ['Moisson sanglante', 'Brûle tous les démons (450 %) et te soigne de 30 %.'],
  argent: ['Jugement', 'Des piliers sacrés frappent tout (400 %, ×2 sur les boss et élites).'],
  base_m: ['Tempête de givre', 'Une nova glacée frappe tout (450 %) et ralentit les démons.'],
  feu: ['Apocalypse', '12 météores s\\'abattent sur le champ de bataille (380 % chacun).'],
  morts: ['Fléau des âmes', 'Des nuées de crânes frappent tout (500 %) et te soignent de 25 %.'],
  foudre: ['Orage', '6 éclairs frappent tous les démons (130 % chacun).'],
};
function ultKey() { const f = curForm(), E = EVO[f]; if (E.path) return E.path; return S.cls === 'hunter' ? 'base_h' : S.cls === 'mage' ? 'base_m' : 'base_k'; }
function ultGain(n) { B.ult = Math.min(100, (B.ult || 0) + n); if (B.ult >= 100 && !B.ultFullT) B.ultFullT = B.t; }
function castUlt() {
  if ((B.ult || 0) < 100 || B.hero.dead) return; const L0 = alive(); if (!L0.length) return;
  B.ult = 0; B.ultFullT = 0; const k = ultKey(), st = heroStats(), A = st.atk, U = ULT[k]; B.banner = { a: 'Ultime', b: U[0], t: 1.6 }; B.shake = Math.max(B.shake, 8); B.flash = { c: '255,200,120', t: 0.35, a: 0.4 };
  const each = (f, gap) => alive().forEach((e, i) => setTimeout(() => { if (!e.dead) f(e); }, (gap || 0) * i));
  const heal = p => { B.hero.hp = Math.min(B.hero.hpMax, B.hero.hp + B.hero.hpMax * p); num(CX, YF - 90, '+' + fmt(B.hero.hpMax * p), '#7aff9a', 1); };
  if (k === 'base_k') { gfx('imp', 0, CX, YF - 20, 360, 0.5); each(e => { gfx('imp', 0, ex(e), ey(e), 140 * sOf(e.z), 0.4); hitEnemy(e, A * 4, true); }, 40); }
  else if (k === 'mort') { each(e => { gfx('spl', 0, ex(e), ey(e), 170 * sOf(e.z), 0.6); hitEnemy(e, A * 5, true); }, 50); heal(0.2); }
  else if (k === 'enfer') meteorShower(A * 3.5, 10);
  else if (k === 'feu') meteorShower(A * 3.8, 12);
  else if (k === 'givre' || k === 'base_m') { gfx('spl', 3, CX, YF - 20, 460, 0.8); if (k === 'givre') freezeAll(4); each(e => { gfx('imp', 3, ex(e), ey(e), 120 * sOf(e.z), 0.45); hitEnemy(e, A * (k === 'givre' ? 4 : 4.5), true); if (k === 'base_m') e.chill = 4; }, 30); }
  else if (k === 'base_h') { for (let i = 0; i < 14; i++) setTimeout(() => { const L = alive(); if (!L.length) return; const e = pick(L); B.fx.push({ k: 'bolt2', x: ex(e), y: ey(e), s: sOf(e.z), t: 0, d: 0.5 }); setTimeout(() => { if (!e.dead) hitEnemy(e, A * 1.8, false); }, 160); }, i * 70); }
  else if (k === 'ombre') { for (let r = 0; r < 3; r++) setTimeout(() => each(e => { gfx('spl', 0, ex(e), ey(e), 120 * sOf(e.z), 0.4, { a: rand(0, TAU) }); hitEnemy(e, A * 1.6, true); }), r * 260); }
  else if (k === 'sang') { gfx('spl', 7, CX, YF - 22, 200, 0.7); each(e => { gfx('spl', 7, ex(e), ey(e) + 6 * sOf(e.z), 130 * sOf(e.z), 0.7); hitEnemy(e, A * 4.5, true); }, 40); heal(0.3); }
  else if (k === 'argent') each(e => { gfx('spl', 6, ex(e), py(e.z) - 50 * sOf(e.z), 200 * sOf(e.z), 0.8); hitEnemy(e, A * 4 * (e.boss || e.elite ? 2 : 1), true); }, 70);
  else if (k === 'morts') { each(e => { gfx('spl', 5, ex(e), ey(e) - 10 * sOf(e.z), 170 * sOf(e.z), 0.9); hitEnemy(e, A * 5, true); }, 40); heal(0.25); }
  else if (k === 'foudre') { for (let r = 0; r < 6; r++) setTimeout(() => { const L = alive(); if (!L.length) return; const pts = [[CX, YF - 60]].concat(L.map(e => [ex(e), ey(e)])); B.fx.push({ k: 'bolt', pts, t: 0, d: 0.3 }); L.forEach(e => { gfx('imp', 8, ex(e), ey(e), 100 * sOf(e.z), 0.3); hitEnemy(e, A * 1.3, false); }); B.flash = { c: '255,250,180', t: 0.12, a: 0.25 }; }, r * 180); }
  uiUlt();
}
function uiUlt() { const b = $('ultBtn'); if (!b) return; const v = Math.floor(B.ult || 0); $('ultFill').style.height = v + '%'; $('ultTxt').textContent = v >= 100 ? 'ULTIME' : v + '%'; b.classList.toggle('full', v >= 100); }
function castSpell(id) {""")
# carreaux qui tombent (Pluie de carreaux)
rep("if (f.k === 'met') {","""if (f.k === 'bolt2') { const q = Math.min(1, f.t / 0.16), sc = f.s; if (q < 1) drawG('prj', 4, 0, f.x + 30 * sc * (1 - q), f.y - 260 * sc * (1 - q) - 10, Math.max(70, 110 * sc), Math.PI / 2 + 0.12); else drawG('imp', 4, (f.t - 0.16) / (f.d - 0.16) * 6, f.x, f.y, 90 * sc, 0, 1 - (f.t - 0.16) / (f.d - 0.16)); continue; }
    if (f.k === 'met') {""")
# jauge : kills
rep("if (e.hp <= 0) { e.dead = 1; e.deadT = 0;","if (e.hp <= 0) { e.dead = 1; e.deadT = 0; ultGain(e.boss ? 35 : e.elite ? 15 : 7);")
# auto-lancement : 3 s après être pleine
rep("  if (B.plague) {","  if ((B.ult || 0) >= 100 && B.ultFullT && B.t - B.ultFullT > 3 && !B.dun) castUlt();\n  if (B.plague) {")
rep("uiWave(); uiCombat(); uiQuest();","uiWave(); uiCombat(); uiQuest(); uiUlt();")
rep("$('bossBtn').onclick = challenge;","$('ultBtn').onclick = castUlt; $('bossBtn').onclick = challenge;")
# fiche d'évolution : nom de l'ultime
rep("""<b style="font-size:16px">${cur.n}</b><small>${cur.d}</small>""","""<b style="font-size:16px">${cur.n}</b><small>${cur.d}</small><div class="kult">Ultime : <b>${ULT[ultKey()][0]}</b><br>${ULT[ultKey()][1]}</div>""")
# tuto
rep("  { t: '#nav [data-t=\"hero\"]', h: 'Ton héros',","  { t: '#ultBtn', h: 'Le sort ultime', p: 'Chaque démon tué remplit cette jauge. Pleine, touche-la pour lancer l\\'<b>ultime</b> de ton héros (sinon il part tout seul après 3 s). Chaque voie d\\'évolution a son propre ultime.' },\n  { t: '#nav [data-t=\"hero\"]', h: 'Ton héros',")
open(P,'w').write(s); print('ok')
