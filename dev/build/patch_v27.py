P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v27.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
a = s.index("function smokeFx(it) {"); b = s.index("\n}\n", a) + 3
s = s[:a] + r"""function smokeFx(it) { // l'objet sort du coffre, brûle, puis éclate en éclats qui filent vers le compteur
  const btn = $('forgeBtn'); if (!btn || !btn.offsetParent) return; const c = document.createElement('canvas'); c.className = 'smk'; eqIcon(c, it, it.slot);
  c.style.setProperty('--rc', RAR[it.r].c); c.style.left = '50%'; btn.appendChild(c);
  for (let i = 0; i < 12; i++) { const f = document.createElement('i'); f.className = 'fl'; f.style.left = `calc(50% + ${rand(-20, 20)}px)`; btn.appendChild(f);
    f.animate([{ transform: 'translate(0,0) scale(.5)', opacity: 0 }, { opacity: 1, offset: 0.25 }, { transform: `translate(${rand(-8, 8)}px,${-rand(28, 52)}px) scale(.15)`, opacity: 0 }], { duration: rand(360, 500), delay: 300 + i * 28, easing: 'ease-out', fill: 'both' }).onfinish = () => f.remove(); }
  setTimeout(() => {
    if (!c.isConnected) return; const br = btn.getBoundingClientRect(), cr = c.getBoundingClientRect(), ox = cr.left + cr.width / 2 - br.left, oy = cr.top + cr.height / 2 - br.top;
    const tg = document.querySelector('.shardp'); let tx = ox, ty = oy - 160; if (tg && tg.offsetParent) { const q = tg.getBoundingClientRect(); tx = q.left + 10 - br.left; ty = q.top + q.height / 2 - br.top; }
    const n = Math.min(14, 5 + it.r * 2);
    for (let i = 0; i < n; i++) { const p = document.createElement('i'); p.className = 'shd'; p.style.left = ox + 'px'; p.style.top = oy + 'px'; btn.appendChild(p); const a = rand(0, TAU), r = rand(22, 48), mx = Math.cos(a) * r, my = Math.sin(a) * r - 8;
      p.animate([{ transform: 'translate(-50%,-50%) scale(.3) rotate(45deg)', opacity: 1 }, { transform: `translate(calc(-50% + ${mx}px),calc(-50% + ${my}px)) scale(1) rotate(${45 + rand(-120, 120)}deg)`, opacity: 1, offset: 0.35 }, { transform: `translate(calc(-50% + ${tx - ox}px),calc(-50% + ${ty - oy}px)) scale(.45) rotate(45deg)`, opacity: 0.9 }], { duration: rand(640, 820), easing: 'cubic-bezier(.35,.05,.45,1)', fill: 'both' }).onfinish = () => { p.remove(); const t2 = document.querySelector('.shardp'); if (i === 0 && t2) { t2.classList.remove('pop'); void t2.offsetWidth; t2.classList.add('pop'); } }; }
    for (let i = 0; i < 6; i++) { const e = document.createElement('i'); e.className = 'emb'; e.style.left = ox + 'px'; e.style.top = oy + 'px'; btn.appendChild(e);
      e.animate([{ transform: 'translate(0,0)', opacity: 1 }, { transform: `translate(${rand(-30, 30)}px,${rand(40, 80)}px)`, opacity: 0 }], { duration: rand(500, 800), easing: 'ease-in', fill: 'both' }).onfinish = () => e.remove(); }
  }, 680);
  setTimeout(() => c.remove(), 780);
}
""" + s[b:]
rep("animation:smk 1.1s ease-out forwards", "animation:smk .78s linear forwards")
a = s.index("@keyframes smk{"); b = s.index("}}", a) + 2
s = s[:a] + "@keyframes smk{0%{transform:translateY(0) scale(.3);opacity:0;filter:none}18%{transform:translateY(-86px) scale(1.25);opacity:1;filter:none}26%{transform:translateY(-86px) scale(1);filter:none}42%{transform:translateY(-87px) scale(1);filter:none}80%{transform:translateY(-89px) scale(1.05) rotate(-4deg);filter:sepia(1) saturate(3) hue-rotate(-25deg) brightness(.6);background:radial-gradient(circle,#ff8a2a99,transparent 70%)}88%{transform:translateY(-89px) scale(1.3);filter:brightness(2.4) saturate(0);opacity:1}100%{transform:translateY(-89px) scale(1.6);filter:brightness(3) saturate(0);opacity:0}}" + s[b:]
s = s.replace("</style>", r"""
#forgeBtn .fl{position:absolute;bottom:242px;width:9px;height:13px;margin-left:-4px;border-radius:50% 50% 45% 45%/62% 62% 38% 38%;background:radial-gradient(circle at 50% 70%,#fff7b0,#ffa020 45%,#ff3a1000 75%);z-index:5;pointer-events:none;mix-blend-mode:screen}
#forgeBtn .shd{position:absolute;width:9px;height:9px;background:linear-gradient(135deg,#f0e4ff,#a070ff 60%,#5a2ad0);box-shadow:0 0 8px #b48aff;z-index:6;pointer-events:none}
#forgeBtn .emb{position:absolute;width:3px;height:3px;background:#ff9a30;box-shadow:0 0 4px #ff7a20;z-index:5;pointer-events:none}
.shardp.pop{animation:spop .35s ease-out}
@keyframes spop{40%{transform:scale(1.25);color:#e8d8ff;text-shadow:0 0 10px #b48aff}}
</style>""", 1)
open(P, 'w').write(s); print('ok')
