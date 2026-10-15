P='/home/claude/grimloom/src.html'
s=open(P).read(); open('/home/claude/grimloom/src.v54.html','w').write(s)
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:140]); s=s.replace(old,new)
css=open('/home/claude/grimloom/build/title.css').read(); js=open('/home/claude/grimloom/build/title.js').read()
rep("</style>\n\n<div id=\"app\">","</style>\n<style>\n"+css+"</style>\n\n<div id=\"app\">")
rep('  <div id="panel"></div>','  <div id="panel"></div>\n  <div id="title" hidden><div id="tBg"></div><div id="tIn"></div></div>')
rep("(function boot() {",js+"\n(function boot() {")
rep("setTimeout(() => welcome(ham0), 400);","TAFTER_HAM = ham0; titleOpen('home');")
rep("try { if ($('modal').hidden || $('modal').classList.contains('dock')) for (let i = 0; i < SPEED; i++) update(dt); if (!document.body.classList.contains('full')) draw(clock);",
    "try { if (!TITLE && ($('modal').hidden || $('modal').classList.contains('dock'))) for (let i = 0; i < SPEED; i++) update(dt); if (!TITLE && !document.body.classList.contains('full')) draw(clock);")
rep("$('adminBtn').onclick = showAdmin;","$('adminBtn').onclick = () => titleOpen('home');")
rep("MUSG.gain.value = 0.3;","MUSG.gain.value = 0.3 * (S.vol === undefined ? 1 : S.vol);")
rep("MUSG.gain.setTargetAtTime(on ? 0.3 : 0,","MUSG.gain.setTargetAtTime(on ? 0.3 * (S.vol === undefined ? 1 : S.vol) : 0,")
rep('<button id="adminBtn" type="button" aria-label="Panneau admin">','<button id="adminBtn" type="button" aria-label="Menu">')
open(P,'w').write(s); print('ok')
