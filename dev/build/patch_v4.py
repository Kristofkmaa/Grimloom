P = '/home/claude/grimloom/src.html'
s = open(P).read()
open('/home/claude/grimloom/src.v3.html', 'w').write(s)

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)

# =================== CSS ===================
a = s.index('/*FONT*/') + len('/*FONT*/'); b = s.index('</style>')
s = s[:a] + r'''
:root{--bg:#0c0610;--p1:#2c1722;--p2:#170b11;--gold:#f0c46a;--gold2:#ffe3a0;--goldd:#8a5a24;--ink:#2a0f18;--red:#d8264a;--red2:#ff5a72;--txt:#f6e9e4;--dim:#b49aa4;--line:#4a2532;
  --t:'Cinzel',serif;--n:'Lilita',system-ui,sans-serif;--b:'Nunito',system-ui,sans-serif}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--bg);color:var(--txt);font:800 14px/1.3 var(--b);overflow:hidden;touch-action:manipulation;-webkit-user-select:none;user-select:none}
button{font:inherit;color:inherit;cursor:pointer}
svg.i{width:1em;height:1em;flex:none;vertical-align:-.12em}
#app{position:fixed;inset:0;margin:0 auto;max-width:480px;display:flex;flex-direction:column;background:radial-gradient(120% 60% at 50% 100%,#2a0f1c,#0c0610 70%);box-shadow:0 0 60px #000}
/* ---------- scène ---------- */
#stageWrap{position:relative;flex:none;overflow:hidden;background:#000}
#stageWrap::after{content:'';position:absolute;left:0;right:0;bottom:0;height:28px;background:linear-gradient(transparent,#12070d);pointer-events:none}
#bt{display:block;width:100%;height:100%;image-rendering:pixelated}
#hud{position:absolute;left:0;right:0;top:0;padding:calc(8px + env(safe-area-inset-top)) 8px 0;display:flex;gap:6px;align-items:center;z-index:2}
#heroChip{display:flex;align-items:center;gap:6px;padding:3px 12px 3px 3px;border-radius:24px;background:linear-gradient(#2d1520ee,#14080ded);border:2px solid var(--goldd);box-shadow:0 2px 8px #000a;margin-right:auto}
#avatar{width:36px;height:36px;border-radius:50%;background:radial-gradient(#5a2a3a,#1a0b10);border:2px solid var(--gold);image-rendering:pixelated}
#heroChip .lbl{display:block;font:800 9px var(--b);color:var(--dim);letter-spacing:.06em;text-transform:uppercase}
#heroChip b{font:400 17px var(--n);color:var(--gold2);letter-spacing:.02em;text-shadow:0 2px 0 #000}
.res{display:flex;align-items:center;gap:5px;height:30px;padding:0 10px 0 4px;border-radius:16px;background:linear-gradient(#1c0c13ee,#0e0609ee);border:1.5px solid #5a3040;box-shadow:inset 0 1px 0 #ffffff12,0 2px 6px #0008}
.res b{font:400 16px var(--n);color:#fff;text-shadow:0 2px 0 #000;min-width:22px}
.res .ico{width:22px;height:22px}
#adminBtn{width:32px;height:32px;border-radius:50%;border:1.5px solid #5a3040;background:linear-gradient(#2a1520,#12080d);color:var(--gold);display:grid;place-items:center;font-size:16px;padding:0}
#stageBar{position:absolute;left:50%;transform:translateX(-50%);top:calc(50px + env(safe-area-inset-top));width:min(300px,78%);z-index:2;pointer-events:none;text-align:center}
#ribbon{display:inline-flex;flex-direction:column;align-items:center;padding:3px 22px 4px;background:linear-gradient(#8a1a32,#4a0a1a);border:1.5px solid var(--gold);border-radius:4px;box-shadow:0 3px 10px #000a;clip-path:polygon(0 0,100% 0,96% 50%,100% 100%,0 100%,4% 50%)}
#ribbon b{font:900 13px var(--t);color:var(--gold2);letter-spacing:.08em;text-shadow:0 1px 0 #000}
#ribbon small{font:800 10px var(--b);color:#ffd8de;letter-spacing:.04em}
#pips{display:flex;justify-content:center;gap:4px;margin-top:5px}
#pips i{width:12px;height:12px;transform:rotate(45deg) scale(.8);background:#1a0b10;border:1.5px solid #6a3a48;border-radius:2px}
#pips i.done{background:linear-gradient(135deg,var(--gold2),#c88a2a);border-color:var(--gold)}
#pips i.cur{background:var(--red2);border-color:#fff;box-shadow:0 0 8px var(--red2);transform:rotate(45deg) scale(1)}
#pips i.boss{width:15px;height:15px;border-color:var(--red)}
#waveBox{position:relative;height:12px;margin:6px auto 0;width:100%;background:#0b0508d8;border:1.5px solid #6a3a48;border-radius:7px;overflow:hidden}
#waveBar{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(#ffe39a,#d8902a);transition:width .25s;border-radius:6px}
#waveBox.boss{height:16px;border-color:var(--red)}
#waveBox.boss #waveBar{background:linear-gradient(#ff7088,#a8142a)}
#waveTxt{position:absolute;inset:0;font:800 9px/11px var(--b);color:#fff;text-shadow:0 1px 2px #000;letter-spacing:.03em}
#waveBox.boss #waveTxt{font-size:11px;line-height:14px}
/* ---------- panneau ---------- */
#panel{flex:1;min-height:0;overflow:auto;padding:8px 10px 10px;overscroll-behavior:contain;position:relative}
.frame{background:linear-gradient(#2a1620,#160a10);border:1.5px solid #6b3a2e;border-radius:14px;box-shadow:inset 0 0 0 1.5px #12060a,inset 0 2px 0 #ffffff10,0 6px 16px #0009}
h3{margin:0 0 8px;font:900 16px var(--t);color:var(--gold2);letter-spacing:.06em;text-shadow:0 2px 0 #000;display:flex;align-items:center;justify-content:space-between}
#equip{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:stretch;padding:10px 8px}
.col{display:grid;gap:7px;align-content:center}
.slot{width:62px;height:62px;position:relative;border-radius:12px;border:2px solid #4a2a36;background:radial-gradient(circle at 50% 40%,#3a2030,#170b11);display:grid;place-items:center;padding:0;box-shadow:inset 0 -3px 0 #0006,0 3px 6px #0008}
.slot canvas{width:44px;height:44px;image-rendering:pixelated}
.slot.empty canvas{opacity:.28}
.slot .nm{position:absolute;bottom:3px;left:0;right:0;font:800 8px var(--b);color:#8a6a76;text-transform:uppercase;letter-spacing:.05em}
.slot .lv{position:absolute;right:-4px;bottom:-5px;font:400 11px var(--n);padding:1px 5px;border-radius:7px;background:#14080d;border:1.5px solid currentColor;text-shadow:0 1px 0 #000}
.slot .gem{position:absolute;left:4px;top:4px;width:7px;height:7px;transform:rotate(45deg);background:currentColor;box-shadow:0 0 6px currentColor}
.slot:active{transform:scale(.95)}
#heroStage{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;border-radius:12px;overflow:hidden;background:radial-gradient(70% 45% at 50% 82%,var(--aura,#5a2a3a) 0,transparent 70%)}
#heroC{width:132px;height:156px;image-rendering:pixelated}
#heroStage .pname{font:900 12px var(--t);color:var(--gold2);letter-spacing:.06em;margin-top:-4px;text-align:center}
.pstats{display:flex;gap:10px;font:400 15px var(--n);margin-top:2px}
.pstats span{display:flex;align-items:center;gap:3px}
/* ---------- barre de forge ---------- */
#dock{flex:none;display:flex;gap:8px;padding:8px 10px;align-items:center}
.dk{position:relative;width:64px;height:62px;border-radius:14px;border:2px solid var(--goldd);background:linear-gradient(#3a2230,#1a0c12);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;padding:0;box-shadow:inset 0 2px 0 #ffffff14,0 4px 0 #07020480}
.dk small{font:800 9px var(--b);color:var(--dim);text-transform:uppercase;letter-spacing:.05em}
.dk b{font:400 18px var(--n);color:var(--gold2);line-height:1}
.dk svg{font-size:20px;color:var(--gold)}
.dk .dot{position:absolute;right:-4px;top:-4px;width:18px;height:18px;border-radius:50%;background:#3ad05a;border:2px solid #0c0610;display:grid;place-items:center;color:#fff;font:400 12px var(--n)}
.dk.red{border-color:#ff8a9a;background:linear-gradient(#e8344e,#86102a)}
.dk.red b,.dk.red svg{color:#fff}
#forgeBtn{flex:1;height:66px;border-radius:16px;border:2px solid #ffd27a;background:linear-gradient(#ffcf6a 0,#f0a030 45%,#c46a10 100%);color:#3a1404;display:flex;align-items:center;justify-content:center;gap:12px;padding:0;box-shadow:inset 0 3px 0 #fff6,inset 0 -5px 0 #0003,0 5px 0 #6a2a06,0 8px 18px #f0a03040;position:relative;overflow:hidden}
#forgeBtn::before{content:'';position:absolute;inset:0;background:linear-gradient(105deg,transparent 30%,#fff7 45%,transparent 60%);transform:translateX(-120%);animation:shine 3.2s infinite}
@keyframes shine{60%,100%{transform:translateX(120%)}}
#forgeBtn svg{font-size:30px;filter:drop-shadow(0 2px 0 #fff6)}
#forgeBtn .ft{display:flex;flex-direction:column;align-items:flex-start;line-height:1}
#forgeBtn .ft b{font:900 22px var(--t);letter-spacing:.08em}
#forgeBtn .ft small{font:800 11px var(--b);opacity:.85;margin-top:3px}
#forgeBtn:active{transform:translateY(3px);box-shadow:inset 0 3px 0 #fff6,inset 0 -3px 0 #0003,0 2px 0 #6a2a06}
#forgeBtn.empty{filter:grayscale(.8) brightness(.7)}
#forgeBtn.empty::before{display:none}
/* ---------- navigation ---------- */
#nav{display:grid;grid-template-columns:repeat(4,1fr);flex:none;background:linear-gradient(#1c0c13,#0b0508);border-top:1.5px solid #4a2532;padding:4px 6px calc(4px + env(safe-area-inset-bottom))}
#nav button{background:none;border:0;color:var(--dim);height:54px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;border-radius:12px;font:800 11px var(--b);position:relative}
#nav button svg{font-size:22px;opacity:.75}
#nav button.on{color:var(--gold2);background:radial-gradient(80% 90% at 50% 100%,#6a1a2e,transparent)}
#nav button.on svg{opacity:1;filter:drop-shadow(0 0 6px #ffb04a90)}
#nav button.on::before{content:'';position:absolute;top:-5px;left:30%;right:30%;height:3px;border-radius:2px;background:var(--gold);box-shadow:0 0 8px var(--gold)}
/* ---------- fenêtres ---------- */
#modal{position:fixed;inset:0;background:#000c;display:flex;align-items:flex-end;justify-content:center;z-index:9;backdrop-filter:blur(2px)}
#modal[hidden]{display:none}
#mbox{width:100%;max-width:480px;max-height:90%;overflow:auto;padding:16px 14px calc(16px + env(safe-area-inset-bottom));border-radius:22px 22px 0 0;background:linear-gradient(#2e1823,#140910);border:1.5px solid #7a4434;border-bottom:0;box-shadow:0 -10px 30px #000;animation:up .2s ease-out}
@keyframes up{from{transform:translateY(60px);opacity:.2}}
.x{width:36px;height:36px;border-radius:50%;border:1.5px solid #6a3a48;background:#12070c;color:var(--dim);font:400 18px var(--n);padding:0;display:grid;place-items:center}
.btn{min-height:52px;border-radius:14px;border:2px solid #6a3a48;background:linear-gradient(#3a2230,#1c0e15);color:var(--txt);font:400 17px var(--n);letter-spacing:.02em;padding:6px 12px;box-shadow:inset 0 2px 0 #ffffff14,0 4px 0 #07020480}
.btn small{display:block;font:800 11px var(--b);opacity:.8;margin-top:1px}
.btn.gold{border-color:#ffd27a;background:linear-gradient(#ffcf6a,#d8801a);color:#3a1404;box-shadow:inset 0 2px 0 #fff6,0 4px 0 #6a2a06}
.btn.red{border-color:#ff8a9a;background:linear-gradient(#ec3a54,#8a1028);color:#fff}
.btn:disabled{opacity:.4}
.btn:active{transform:translateY(2px)}
.row{display:flex;gap:10px}
.card{border-radius:16px;padding:12px;background:linear-gradient(#24121b,#12080d);border:2px solid var(--rc,#6a3a48);box-shadow:0 0 0 1px #000,0 0 22px -6px var(--rc,transparent)}
.card + .card{margin-top:10px}
.card.cur{opacity:.8;transform:scale(.97)}
.card .tag{font:800 10px var(--b);color:var(--dim);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.card .hd{display:flex;gap:12px;align-items:center;margin-bottom:10px}
.icon-big{position:relative;width:64px;height:64px;border-radius:14px;display:grid;place-items:center;background:radial-gradient(circle,var(--rc) -40%,#14080d 75%);border:2px solid var(--rc);flex:none}
.icon-big canvas{width:48px;height:48px;image-rendering:pixelated}
.card h4{margin:0;font:900 18px var(--t);letter-spacing:.04em;color:var(--rc);text-shadow:0 2px 0 #000}
.rar{font:800 12px var(--b);color:var(--dim);margin-top:2px}
.rar b{color:var(--rc);font-weight:900}
.stats{display:grid;gap:5px}
.stat{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:6px 10px;border-radius:9px;background:#ffffff08;font:800 13px var(--b)}
.stat.sub{background:#ffffff04;color:#e6d4da}
.stat em{font:400 15px var(--n);font-style:normal}
.up{color:#5ae07a}.down{color:#ff5a6a}
.pw{display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding:8px 10px;border-radius:10px;background:linear-gradient(90deg,#00000060,#ffffff0a);font:900 12px var(--t);letter-spacing:.06em;color:var(--gold2)}
.pw em{font:400 20px var(--n);font-style:normal;color:#fff}
.list{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.list div{display:flex;align-items:center;gap:8px;background:#ffffff08;border:1px solid #ffffff10;border-radius:10px;padding:8px 10px;font:800 11px var(--b);color:var(--dim)}
.list div svg{font-size:18px;color:var(--gold)}
.list b{display:block;font:400 17px var(--n);color:#fff;font-weight:400}
.heroes{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.heroes button{border-radius:14px;border:2px solid #4a2a36;background:radial-gradient(circle at 50% 35%,#3a2030,#160a10);padding:6px 4px 8px;font:800 11px var(--b);color:var(--txt);min-height:112px}
.heroes button.on{border-color:var(--gold);box-shadow:0 0 14px -2px var(--gold);color:var(--gold2)}
.heroes canvas{width:76px;height:76px;image-rendering:pixelated;display:block;margin:0 auto 2px}
#heroHead{display:flex;align-items:center;gap:12px;margin-bottom:12px}
#heroHead canvas{width:96px;height:112px;image-rendering:pixelated;border-radius:12px;background:radial-gradient(60% 40% at 50% 85%,var(--aura,#5a2a3a),#14080d 80%);border:2px solid var(--goldd)}
#heroHead h4{margin:0 0 6px;font:900 19px var(--t);color:var(--gold2);letter-spacing:.04em}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chips span{font:800 11px var(--b);padding:3px 8px;border-radius:8px;background:#ffffff0c;border:1px solid #ffffff14}
.odds{display:grid;gap:6px}
.odd{display:grid;grid-template-columns:90px 1fr 72px;gap:8px;align-items:center;font:800 12px var(--b)}
.odd .bar{height:10px;border-radius:5px;background:#ffffff0c;overflow:hidden}
.odd .bar i{display:block;height:100%;border-radius:5px;background:currentColor;min-width:3px}
.odd em{font:400 14px var(--n);font-style:normal;text-align:right;color:#fff}
.odd em small{color:#5ae07a;font-size:11px;display:block}
.soon{padding:22px 16px;text-align:center}
.soon svg{font-size:52px;color:var(--gold);opacity:.8;filter:drop-shadow(0 0 12px #f0a03060)}
.soon p{font:700 14px/1.5 var(--b);color:var(--dim);margin:8px 0 0}
.lockgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}
.lockgrid div{padding:12px 8px;border-radius:12px;background:#ffffff06;border:1.5px dashed #5a3040;font:800 12px var(--b);color:var(--dim)}
.adm{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.adm .btn{font-size:14px;min-height:46px}
.adm .full{grid-column:1/-1}
.seg{display:flex;gap:6px;margin:6px 0 10px}
.seg button{flex:1;height:40px;border-radius:10px;border:1.5px solid #5a3040;background:#14080d;color:var(--dim);font:400 15px var(--n)}
.seg button.on{background:var(--red);border-color:#ff8a9a;color:#fff}
.lbl2{font:800 11px var(--b);color:var(--dim);text-transform:uppercase;letter-spacing:.08em;margin:10px 2px 4px}
#toast{position:fixed;left:50%;top:132px;transform:translateX(-50%);z-index:10;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:6px;width:max-content;max-width:92vw}
#toast div{background:linear-gradient(#2e1823,#170b11);color:var(--gold2);border:1.5px solid var(--gold);border-radius:22px;padding:8px 16px;font:800 13px var(--b);box-shadow:0 6px 16px #000a;animation:up .2s}
''' + s[b:]

# =================== HTML ===================
a = s.index('<div id="app">'); b = s.index('<div id="modal"')
s = s[:a] + '''<div id="app">
  <div id="stageWrap">
    <canvas id="bt" width="720" height="840" aria-label="Combat"></canvas>
    <div id="hud">
      <div id="heroChip"><canvas id="avatar" width="40" height="40"></canvas><div><span class="lbl">Puissance</span><b id="pow">0</b></div></div>
      <div class="res"><svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#c87a18"/><circle cx="12" cy="11" r="8.5" fill="#ffc94a"/><circle cx="12" cy="11" r="5.5" fill="none" stroke="#c87a18" stroke-width="1.6"/><path d="M8 7.5a5 5 0 0 1 4-2" stroke="#fff6c0" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg><b id="gold">0</b></div>
      <div class="res"><svg class="ico" viewBox="0 0 24 24"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z" fill="#a8622a"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z" fill="#d6d8e6"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-3V6.5H8z" fill="#fff" opacity=".5"/></svg><b id="ham">0</b></div>
      <button id="adminBtn" type="button" aria-label="Panneau admin"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3.3h-4l-.4 2.6a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1a7.4 7.4 0 0 0 1.7 1l.4 2.6h4l.4-2.6a7.4 7.4 0 0 0 1.7-1l2.5 1 2-3.5zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z" transform="translate(-1 0)"/></svg></button>
    </div>
    <div id="stageBar"><div id="ribbon"><b id="stage">CHAPITRE 1</b><small id="biomeN">Les Catacombes</small></div><div id="pips"></div><div id="waveBox"><i id="waveBar"></i><span id="waveTxt"></span></div></div>
  </div>
  <div id="panel"></div>
  <div id="dock">
    <button class="dk" id="forgeLv" type="button"><small>Forge</small><b id="flv">1</b><small>niveau</small><i class="dot" id="fdot" hidden>!</i></button>
    <button id="forgeBtn" type="button"><svg class="i" viewBox="0 0 24 24"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z" fill="#6a2a06"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z" fill="#3a1404"/></svg><span class="ft"><b>FORGER</b><small><span id="hamN">0</span> marteaux</small></span></button>
    <button class="dk red" id="bossBtn" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 3 5.8 3 10.5c0 2.8 1.3 4.6 3 5.6V19a1 1 0 0 0 1 1h1.5v-2h1.5v2h4v-2h1.5v2H17a1 1 0 0 0 1-1v-2.9c1.7-1 3-2.8 3-5.6C21 5.8 17.5 2 12 2zM8.5 14a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zm7 0a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4z"/></svg><b style="font-size:14px">Boss</b></button>
  </div>
  <nav id="nav">
    <button data-t="forge" class="on" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5zm0 3.2 5 1.9V11c0 3.4-2.1 6.6-5 7.9z"/></svg>Équipement</button>
    <button data-t="hero" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="7" r="4.2"/><path d="M3.5 21c.6-4.6 4-7.5 8.5-7.5s7.9 2.9 8.5 7.5z"/></svg>Héros</button>
    <button data-t="skills" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.5c1 4 4.8 5.7 4.8 10.4A4.8 4.8 0 0 1 12 16.8a4.8 4.8 0 0 1-4.8-4.9c0-2 .9-3.3 1.8-4.4.2 1.4 1 2.4 2 2.7C10.2 7 11 4 12 1.5zM5 18h14v3.5H5z"/></svg>Pouvoirs</button>
    <button data-t="dungeon" type="button"><svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M3 21V9l3-2V4h3v1.5L12 3l3 2.5V4h3v3l3 2v12h-6v-5a3 3 0 0 0-6 0v5z"/></svg>Donjons</button>
  </nav>
</div>
''' + s[b:]

# =================== polices dans le canvas ===================
s = s.replace("ctx.font = (n.k > 1.1 ? 16 : 8) + 'px Dungeon, monospace'", "ctx.font = (n.k > 1.1 ? 17 : 12) + 'px Lilita, sans-serif'")
s = s.replace("ctx.font = '32px Dungeon, monospace'", "ctx.font = '900 28px Cinzel, serif'")
s = s.replace("ctx.font = '16px Dungeon, monospace'", "ctx.font = '800 14px Nunito, sans-serif'")
assert 'Dungeon' not in s.split('<script>')[1], 'Dungeon reste'

# =================== décor de l'arène qui défile avec la salle ===================
rep("function placeDeco() { DECO = B.scene === 'arena' ? DECO_A : DECO_C; if (DECO === DECO_C) for (const d of DECO) d.z = ((d.wz - B.scroll + 0.15) % SEG + SEG) % SEG - 0.15; }",
    "for (const d of DECO_A) d.wz = d.z;\nfunction placeDeco() { DECO = B.scene === 'arena' ? DECO_A : DECO_C; if (DECO === DECO_C) for (const d of DECO) d.z = ((d.wz - B.scroll + 0.15) % SEG + SEG) % SEG - 0.15; else for (const d of DECO) d.z = d.wz - B.scroll; }")
rep("  if (B.scene === 'corridor') placeDeco();", "  placeDeco();")
rep("glow(CX, py(0.5), 110, biome().light, 0.12 + Math.sin(time * 2.5) * 0.05)", "if (0.5 - B.scroll > 0.02) glow(CX, py(0.5 - B.scroll), 110 * sOf(0.5 - B.scroll) / sOf(0.5), biome().light, 0.12 + Math.sin(time * 2.5) * 0.05)")

# =================== effet d'équipement (plus d'effet d'attaque) ===================
rep("  sfx('epee', CX, YF - 30, 120, 0.3, -Math.PI / 2); if (it.r >= 3) { burst(CX, YF - 40, RAR[it.r].c, 30, 200); B.shake = 5; }\n", "")
s = s.replace("function makeItem() {\n  const sl = pick(SLOTS), r = rollRarity(),", "function makeItem(r0, sl0) {\n  const sl = sl0 || pick(SLOTS), r = r0 === undefined ? rollRarity() : r0,")

# =================== interface (réécrite) ===================
a = s.index("function slotHTML(sl)"); b = s.index("let last = performance.now()")
s = s[:a] + r'''const IC = {
  sword: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 2 21.9 3.5 11.5 13.9l-1.4-1.4zM9.4 13.2l1.4 1.4-1.6 1.6 2.1 2.1-1.4 1.4-1.8-1.8-3 3L3 19.8l3-3-1.8-1.8 1.4-1.4 2.1 2.1z"/></svg>',
  heart: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-8.5-5.3-8.5-11.2A4.8 4.8 0 0 1 12 6.6a4.8 4.8 0 0 1 8.5 3.2C20.5 15.7 12 21 12 21z"/></svg>',
  shield: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/></svg>',
  bolt: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>',
  star: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 3 6.6 7 .7-5.3 4.8 1.6 7L12 17.5 5.7 21l1.6-7L2 9.3l7-.7z"/></svg>',
  drop: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2s7 7.6 7 12.5a7 7 0 0 1-14 0C5 9.6 12 2 12 2z"/></svg>',
  wind: '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7"/></svg>',
  skull: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 3 5.8 3 10.5c0 2.8 1.3 4.6 3 5.6V19a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-2.9c1.7-1 3-2.8 3-5.6C21 5.8 17.5 2 12 2zM8.5 14a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zm7 0a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4z"/></svg>',
  lock: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10V7a5 5 0 0 1 10 0v3h1.5a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 20.5v-9A1.5 1.5 0 0 1 5.5 10zm2.5 0h5V7a2.5 2.5 0 0 0-5 0z"/></svg>',
  flame: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.5c1 4 4.8 5.7 4.8 10.4A4.8 4.8 0 0 1 12 16.8a4.8 4.8 0 0 1-4.8-4.9c0-2 .9-3.3 1.8-4.4.2 1.4 1 2.4 2 2.7C10.2 7 11 4 12 1.5zM5 18h14v3.5H5z"/></svg>',
  gate: '<svg class="i" viewBox="0 0 24 24" fill="currentColor"><path d="M3 21V9l3-2V4h3v1.5L12 3l3 2.5V4h3v3l3 2v12h-6v-5a3 3 0 0 0-6 0v5z"/></svg>',
};
const STATI = { atk: 'sword', atkp: 'sword', pv: 'heart', pvp: 'heart', def: 'shield', crit: 'star', cdmg: 'star', vit: 'wind', vol: 'drop', regen: 'heart', esq: 'wind' };
const bestRar = () => Math.max(-1, ...SLOTS.map(sl => S.eq[sl.id] ? S.eq[sl.id].r : -1));
function slotHTML(sl) { const it = S.eq[sl.id], c = it ? RAR[it.r].c : ''; return `<button type="button" class="slot${it ? '' : ' empty'}" data-s="${sl.id}" style="${it ? `color:${c};border-color:${c};background:radial-gradient(circle at 50% 38%,${c}88,${c}22 60%,#170b11);box-shadow:inset 0 -3px 0 #0006,0 0 12px -3px ${c}` : ''}"><canvas data-ic="${sl.id}"></canvas>${it ? `<i class="gem"></i><span class="lv">${it.L}</span>` : `<span class="nm">${sl.n}</span>`}</button>`; }
let tab = 'forge';
function ui() {
  uiTop(); const st = heroStats(), br = bestRar();
  $('dock').style.display = tab === 'forge' ? '' : 'none';
  if (tab === 'forge') {
    $('panel').innerHTML = `<div id="equip" class="frame" style="--aura:${br >= 0 ? RAR[br].c + '77' : '#5a2a3a'}"><div class="col">${SLOTS.slice(0, 4).map(slotHTML).join('')}</div>
      <div id="heroStage"><canvas id="heroC" width="132" height="156"></canvas><div class="pname">${HEROES[S.hero].n}</div><div class="pstats"><span style="color:#ff9a6a">${IC.sword}${fmt(st.atk)}</span><span style="color:#ff6a7a">${IC.heart}${fmt(st.pv)}</span></div></div>
      <div class="col">${SLOTS.slice(4).map(slotHTML).join('')}</div></div>`;
    document.querySelectorAll('[data-ic]').forEach(c => eqIcon(c, S.eq[c.dataset.ic], c.dataset.ic));
    document.querySelectorAll('[data-s]').forEach(el => el.onclick = () => { const it = S.eq[el.dataset.s]; if (it) showItem(it, null); else toast('Forge pour trouver : ' + SLOTS.find(x => x.id === el.dataset.s).n); });
  } else if (tab === 'hero') {
    const H = HEROES[S.hero];
    $('panel').innerHTML = `<div class="frame" style="padding:12px;--aura:${br >= 0 ? RAR[br].c + '88' : '#5a2a3a'}"><div id="heroHead"><canvas id="heroC" width="96" height="112"></canvas><div><h4>${H.n}</h4><div class="chips"><span>Attaque ×${H.atk}</span><span>Vie ×${H.hp}</span><span>Cadence ×${H.spd}</span>${H.splash ? '<span>Tirs explosifs</span>' : ''}${H.chill ? '<span>Ralentit</span>' : ''}${H.leech ? '<span>Vol de vie</span>' : ''}</div></div></div>
    <div class="list">${[['star', 'Puissance', fmt(power(st))], ['sword', 'Attaque', fmt(st.atk)], ['heart', 'Points de vie', fmt(st.pv)], ['shield', 'Défense', fmt(st.def)], ['wind', 'Attaques / s', st.rate.toFixed(2)], ['star', 'Critique', st.crit.toFixed(1) + ' %'], ['star', 'Dégâts critiques', Math.round(st.cdmg) + ' %'], ['drop', 'Vol de vie', st.vol.toFixed(1) + ' %'], ['heart', 'Régénération', st.regen.toFixed(1) + ' %/s'], ['wind', 'Esquive', st.esq.toFixed(1) + ' %'], ['gate', 'Meilleure étape', `${Math.floor((S.best - 1) / 10) + 1}-${(S.best - 1) % 10 + 1}`], ['skull', 'Démons tués', fmt(S.kills)]].map(([i, a, b]) => `<div>${IC[i]}<span>${a}<b>${b}</b></span></div>`).join('')}</div>
    <h3 style="margin-top:16px">Choisir le héros</h3><div class="heroes">${Object.entries(HEROES).map(([id, h]) => `<button type="button" data-h="${id}" class="${S.hero === id ? 'on' : ''}"><canvas data-hc="${id}" width="76" height="76"></canvas>${h.n.replace(/^(Le|La|L') ?/, '')}</button>`).join('')}</div></div>`;
    document.querySelectorAll('[data-hc]').forEach(c => { const H = HEROES[c.dataset.hc]; const g = c.getContext('2d'); const draw = () => { if (!c.isConnected) return; g.clearRect(0, 0, 76, 76); sprH(H.key, 'idle_6', performance.now() / 80, 38, 74, 0.8, 1, g); requestAnimationFrame(draw); }; draw(); });
    document.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { S.hero = b.dataset.h; save(); B.hero.hpMax = heroStats().pv; B.hero.hp = Math.min(B.hero.hp, B.hero.hpMax); ui(); });
  } else {
    const sk = tab === 'skills';
    $('panel').innerHTML = `<div class="frame soon">${sk ? IC.flame : IC.gate}<h3 style="justify-content:center;margin-top:6px">${sk ? 'Pouvoirs' : 'Donjons'}</h3><p>${sk ? 'Des pouvoirs qui se déclenchent seuls en combat, à débloquer et améliorer.' : 'Des donjons quotidiens qui rapportent marteaux, or et matériaux.'}</p>
    <div class="lockgrid">${(sk ? ['Pluie de feu', 'Nova de givre', 'Lames d\'ombre', 'Blizzard'] : ['Mine de marteaux', 'Crypte d\'or', 'Tour des âmes', 'Arène sanglante']).map(n => `<div>${IC.lock} ${n}</div>`).join('')}</div></div>`;
  }
}
function uiTop() {
  hamTick(); $('stage').textContent = `CHAPITRE ${S.c}`; $('biomeN').textContent = S.farm ? biome().n + ' · entraînement' : biome().n;
  $('gold').textContent = fmt(S.gold); $('ham').textContent = S.ham; $('hamN').textContent = S.ham; $('pow').textContent = fmt(power());
  $('flv').textContent = S.forge; $('fdot').hidden = S.gold < forgeCost(); $('forgeBtn').classList.toggle('empty', S.ham <= 0);
  $('bossBtn').style.display = S.farm ? '' : 'none';
  $('pips').innerHTML = Array.from({ length: 10 }, (_, i) => `<i class="${i + 1 < S.s || (S.farm && i < 9) ? 'done' : ''} ${i + 1 === S.s && !S.farm ? 'cur' : ''} ${i === 9 ? 'boss' : ''}"></i>`).join('');
}
function uiWave() {
  const w = B.wave;
  if (!w) { $('waveTxt').textContent = sceneFor() === 'arena' ? 'Vers l\'arène du boss…' : B.scene === 'arena' ? 'Vers un nouveau biome…' : 'En avant…'; $('waveBar').style.width = '0%'; $('waveBox').classList.remove('boss'); return; }
  const boss = w.boss && B.en[0], pr = boss ? Math.max(0, B.en[0].hp) / B.en[0].max : w.killed / Math.max(1, w.total);
  $('waveBox').classList.toggle('boss', !!boss); $('waveBar').style.width = (pr * 100).toFixed(1) + '%';
  $('waveTxt').textContent = boss ? `${fmt(Math.max(0, B.en[0].hp))} / ${fmt(B.en[0].max)}` : `${w.killed} / ${w.total} démons`;
}
function statLines(it, other) {
  const a = itemStats(it), b = other ? itemStats(other) : {}, keys = [...new Set([...Object.keys(a), ...(other ? Object.keys(b) : [])])], mainK = it.main.map(m => m[0]);
  return keys.map(k => { const va = a[k] || 0, vb = b[k] || 0, d = va - vb, unit = PCT[k] || k === 'atkp' || k === 'pvp' ? ' %' : ''; return `<div class="stat ${mainK.includes(k) ? '' : 'sub'}"><span style="display:flex;align-items:center;gap:6px"><span style="color:var(--gold)">${IC[STATI[k]] || ''}</span>${STATN[k]}</span><em>${round2(va)}${unit}${other && d ? ` <span class="${d > 0 ? 'up' : 'down'}" style="font-size:12px">${d > 0 ? '▲' : '▼'}${round2(Math.abs(d))}</span>` : ''}</em></div>`; }).join('');
}
function cardHTML(it, label, other, cls) {
  const sl = SLOTS.find(s => s.id === it.slot), dp = other ? itemPower(it) - itemPower(other) : 0, c = RAR[it.r].c;
  return `<div class="card ${cls || ''}" style="--rc:${c}"><div class="tag">${label}</div><div class="hd"><div class="icon-big"><canvas data-ci="${label}"></canvas></div><div><h4>${sl.n}</h4><div class="rar"><b>${RAR[it.r].n}</b> · niveau ${it.L}</div></div></div><div class="stats">${statLines(it, other)}</div><div class="pw"><span>PUISSANCE</span><em>${fmt(itemPower(it))}${other ? ` <span class="${dp >= 0 ? 'up' : 'down'}" style="font-size:14px">${dp >= 0 ? '▲' : '▼'}${fmt(Math.abs(dp))}</span>` : ''}</em></div></div>`;
}
function sheet(html) { $('mbox').innerHTML = html; $('modal').hidden = false; const x = $('mbox').querySelector('.x'); if (x) x.onclick = closeM; }
function showItem(it, isNew) {
  const cur = S.eq[it.slot];
  if (isNew) {
    const better = !cur || itemPower(it) > itemPower(cur);
    sheet(`<h3>Nouvel objet <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Forgé', cur)}${cur ? cardHTML(cur, 'Équipé actuellement', null, 'cur') : ''}
    <div class="row" style="margin-top:14px"><button class="btn" id="sellB" type="button" style="flex:1">Vendre<small>+${fmt(it.v)} or</small></button><button class="btn ${better ? 'gold' : ''}" id="eqB" type="button" style="flex:1.4">Équiper<small>${cur ? `l'ancien vendu +${fmt(cur.v)} or` : 'emplacement vide'}</small></button></div>`);
    $('mbox').querySelector('.x').onclick = () => { S.gold += it.v; closeM(); };
  } else sheet(`<h3>${SLOTS.find(s => s.id === it.slot).n} <button class="x" type="button" aria-label="Fermer">✕</button></h3>${cardHTML(it, 'Équipé', null)}<button class="btn" id="clB" type="button" style="width:100%;margin-top:14px">Fermer</button>`);
  $('mbox').querySelectorAll('[data-ci]').forEach(c => eqIcon(c, c.dataset.ci === 'Forgé' ? it : isNew ? cur : it));
  if (isNew) { $('eqB').onclick = () => { if (cur) S.gold += cur.v; S.eq[it.slot] = it; closeM(); equipFx(it); toast(`${SLOTS.find(s => s.id === it.slot).n} ${RAR[it.r].n.toLowerCase()} équipé`); }; $('sellB').onclick = () => { S.gold += it.v; closeM(); }; }
  else $('clB').onclick = closeM;
}
function equipFx(it) { // petites étincelles de la couleur de la rareté qui montent du héros
  const c = RAR[it.r].c, n = 10 + it.r * 5;
  for (let i = 0; i < n; i++) B.fx.push({ k: 'p', x: CX + rand(-22, 22), y: YF - rand(0, 50), vx: rand(-6, 6), vy: rand(-60, -25), g: -10, c: Math.random() < 0.3 ? '#fff' : c, t: 0, d: rand(0.7, 1.3), r: rand(0.8, 1.6) });
}
function showForge() {
  const c = forgeCost(), w = rarityWeights(S.forge), t = w.reduce((a, b) => a + b, 0), w2 = rarityWeights(S.forge + 1), t2 = w2.reduce((a, b) => a + b, 0);
  const rows = w.map((x, i) => [RAR[i], x / t * 100, w2[i] / t2 * 100]).filter(([, p, q]) => q >= 0.01);
  const f = v => v < 0.1 ? v.toFixed(2) : v < 10 ? v.toFixed(1) : Math.round(v);
  sheet(`<h3>Forge · niveau ${S.forge} <button class="x" type="button" aria-label="Fermer">✕</button></h3><p style="margin:0 0 12px;color:var(--dim);font:700 13px/1.4 var(--b)">Chaque niveau augmente les chances d'objets rares.</p>
  <div class="odds">${rows.map(([r, p, q]) => `<div class="odd" style="color:${r.c}"><span>${r.n}</span><div class="bar"><i style="width:${Math.max(1, Math.sqrt(p / 100) * 100)}%"></i></div><em>${f(p)} %<small>→ ${f(q)} %</small></em></div>`).join('')}</div>
  <button class="btn gold" id="upB" type="button" style="width:100%;margin-top:16px" ${S.gold < c ? 'disabled' : ''}>Améliorer la forge<small>${fmt(c)} or · tu as ${fmt(S.gold)}</small></button>`);
  $('upB').onclick = () => { upForge(); showForge(); };
}
// ---------- panneau admin ----------
let SPEED = 1;
function showAdmin() {
  const rb = (i, r) => `<button class="btn" type="button" data-give="${i}" style="border-color:${r.c};color:${r.c}">${r.n}</button>`;
  sheet(`<h3>Panneau admin <button class="x" type="button" aria-label="Fermer">✕</button></h3>
  <div class="lbl2">Ressources</div><div class="adm"><button class="btn gold" data-a="gold" type="button">+1 M or</button><button class="btn gold" data-a="ham" type="button">+100 marteaux</button><button class="btn" data-a="forge" type="button">Forge +1</button><button class="btn" data-a="forge5" type="button">Forge +5</button></div>
  <div class="lbl2">Progression</div><div class="adm"><button class="btn" data-a="cm" type="button">Chapitre −1</button><button class="btn" data-a="cp" type="button">Chapitre +1</button><button class="btn" data-a="boss" type="button">Aller au boss</button><button class="btn red" data-a="kill" type="button">Tuer la vague</button></div>
  <div class="lbl2">Combat</div><div class="adm"><button class="btn ${B.god ? 'red' : ''}" data-a="god" type="button">Invincible : ${B.god ? 'oui' : 'non'}</button><button class="btn ${B.oneshot ? 'red' : ''}" data-a="one" type="button">Tue en 1 coup : ${B.oneshot ? 'oui' : 'non'}</button></div>
  <div class="lbl2">Vitesse du jeu</div><div class="seg">${[1, 2, 4, 8].map(v => `<button type="button" data-sp="${v}" class="${SPEED === v ? 'on' : ''}">×${v}</button>`).join('')}</div>
  <div class="lbl2">Équiper tout le stuff en</div><div class="adm">${RAR.map((r, i) => rb(i, r)).join('')}<button class="btn" data-a="strip" type="button">Tout retirer</button></div>
  <div class="lbl2">Sauvegarde</div><div class="adm"><button class="btn red full" data-a="reset" type="button">Réinitialiser la partie</button></div>`);
  const A = {
    gold: () => S.gold += 1e6, ham: () => S.ham += 100, forge: () => S.forge++, forge5: () => S.forge += 5,
    cp: () => { S.c++; S.s = 1; S.farm = false; B.fade = 1; startWave(); }, cm: () => { S.c = Math.max(1, S.c - 1); S.s = 1; S.farm = false; B.fade = 1; startWave(); },
    boss: () => { S.s = 10; S.farm = false; startWave(); }, kill: () => { for (const e of B.en) if (!e.dead) { e.spawn = 0; hitEnemy(e, e.hp + 1); } if (B.wave) B.wave.left = 0; },
    god: () => B.god = !B.god, one: () => B.oneshot = !B.oneshot, strip: () => S.eq = {},
    reset: () => { if (confirm('Effacer toute la progression ?')) { try { localStorage.removeItem(KEY); } catch (e) { } location.reload(); } },
  };
  $('mbox').querySelectorAll('[data-a]').forEach(b => b.onclick = () => { A[b.dataset.a](); save(); uiTop(); if (b.dataset.a !== 'reset') { showAdmin(); toast('Fait'); } });
  $('mbox').querySelectorAll('[data-sp]').forEach(b => b.onclick = () => { SPEED = +b.dataset.sp; showAdmin(); });
  $('mbox').querySelectorAll('[data-give]').forEach(b => b.onclick = () => { const r = +b.dataset.give; for (const sl of SLOTS) S.eq[sl.id] = makeItem(r, sl); save(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = st.pv; equipFx({ r }); showAdmin(); toast(`Stuff ${RAR[r].n.toLowerCase()} équipé`); });
}
function closeM() { $('modal').hidden = true; save(); const st = heroStats(); B.hero.hpMax = st.pv; B.hero.hp = Math.min(B.hero.hp, st.pv); ui(); }
function forge() {
  hamTick(); if (S.ham <= 0) { toast('Plus de marteaux : ils reviennent avec le temps'); return; }
  S.ham--; S.forged++; const it = makeItem(); save();
  showItem(it, true);
}
function upForge() { const c = forgeCost(); if (S.gold < c) return; S.gold -= c; S.forge++; save(); toast(`Forge niveau ${S.forge}`); uiTop(); }
function toast(t) { const d = document.createElement('div'); d.textContent = t; $('toast').appendChild(d); setTimeout(() => d.remove(), 2200); }
document.querySelectorAll('#nav button').forEach(b => b.onclick = () => { tab = b.dataset.t; document.querySelectorAll('#nav button').forEach(x => x.classList.toggle('on', x === b)); ui(); });
$('modal').addEventListener('click', e => { if (e.target.id === 'modal') { if ($('sellB')) return; closeM(); } });
$('forgeBtn').onclick = forge; $('forgeLv').onclick = showForge; $('adminBtn').onclick = showAdmin;
$('bossBtn').onclick = () => { if (B.walk) return; S.farm = false; S.s = 10; save(); B.en = []; B.es = []; beginWalk(); };
// portrait animé du héros (panneau + pastille du HUD)
function heroPortrait(time) {
  const H = HEROES[S.hero], c = $('heroC');
  if (c) { const g = c.getContext('2d'); g.clearRect(0, 0, c.width, c.height); const big = c.width > 100; sprH(H.key, 'idle_6', time * 10, c.width / 2, c.height - (big ? 10 : 8), big ? 1.15 : 0.85, 1, g); }
  const a = $('avatar'), g = a.getContext('2d'); g.clearRect(0, 0, 40, 40); g.save(); g.beginPath(); g.arc(20, 20, 20, 0, TAU); g.clip(); sprH(H.key, 'idle_6', time * 10, 20, 66, 1.05, 1, g); g.restore();
}
''' + s[b:]
rep("function heroPortrait(time) { const c = $('heroC'); if (!c) return; const g = c.getContext('2d'); g.clearRect(0, 0, 80, 100); const H = HEROES[S.hero]; sprH(H.key, 'idle_6', time * 10, 40, 94, 0.85, 1, g); }\n", "", 1) if "function heroPortrait(time) { const c = $('heroC'); if (!c) return;" in s else None

# vitesse ×N, invincible, tue en 1 coup
rep("try { if ($('modal').hidden) update(dt);", "try { if ($('modal').hidden) for (let i = 0; i < SPEED; i++) update(dt);")
rep("const st = heroStats(); if (B.hero.dead || B.walk) return;", "const st = heroStats(); if (B.hero.dead || B.walk || B.god) return;")
rep("if (e.dead) return; e.hp -= dmg;", "if (e.dead) return; if (B.oneshot) dmg = Math.max(dmg, e.hp + 1); e.hp -= dmg;")

open(P, 'w').write(s)
print('ok', len(s))
