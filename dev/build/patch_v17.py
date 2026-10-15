P = '/home/claude/grimloom/src.html'
s = open(P).read()
#open('/home/claude/grimloom/src.v17.html', 'w').write(s)
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:100])
    s = s.replace(old, new)
rep('<span class="ft"><b>FORGER</b><small><span id="hamN">0</span> marteaux</small></span>',
    '<span class="plq"><svg class="i" viewBox="0 0 24 24"><path d="M10.5 9.5 4 20.5a1.6 1.6 0 0 0 2.6 1.5l7-10.5z" fill="#c8884a"/><path d="M8 3.5h9.5a3 3 0 0 1 3 3V9h-5l-1.5 2.5L9.5 9 8 9.2z" fill="#d8dee8"/></svg><b id="hamN">0</b></span>')
rep("@keyframes zbob{", """#forgeBtn{background:none!important;border:0!important;box-shadow:none!important;height:100px;align-self:flex-end;justify-content:center;padding:0}
#forgeBtn::before{display:none!important}
#forgeBtn:active{transform:scale(.96)}
#forgeBtn .zc{position:absolute;left:50%;bottom:16px;width:96px;height:162px;margin:0;transform:translateX(-38%);pointer-events:none}
#forgeBtn .zc::after{left:0;bottom:0;width:96px;height:162px}
#forgeBtn .plq{position:absolute;left:50%;bottom:0;transform:translateX(-50%);display:flex;align-items:center;gap:5px;padding:3px 14px 3px 10px;border-radius:12px;background:linear-gradient(#5a3420,#2a160c);border:2px solid #f0c46a;box-shadow:0 3px 0 #0008,inset 0 1px 0 #fff3;z-index:2}
#forgeBtn .plq svg{font-size:17px}
#forgeBtn .plq b{font:400 17px var(--n);color:#ffe3a0;text-shadow:0 2px 0 #000;letter-spacing:.02em}
#forgeBtn.empty{filter:none}
#forgeBtn.empty .plq b{color:#ff8a8a}
#forgeBtn .autob{top:auto;bottom:4px;right:auto;left:calc(50% + 46px)}
#dock{overflow:visible;align-items:flex-end}
@keyframes zbob{""")
open(P, 'w').write(s); print('ok')
s = open(P).read()
rep("#dock{overflow:visible;align-items:flex-end}", "#dock{overflow:visible;align-items:flex-end;padding-top:0}\n#forgeBtn{height:150px!important}\n#forgeBtn .zc{bottom:14px;width:100px;height:168px}\n#forgeBtn .zc::after{width:100px;height:168px}\n#panel > #equip{min-height:280px}")
open(P, 'w').write(s); print('ok2')
