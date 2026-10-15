// ================= tutoriel guidé (projecteur + bulles) =================
let CO = null;
const COACH = [
  { t: '#stageWrap', h: 'Bienvenue dans GRIMLOOM', p: 'Ton héros se bat <b>tout seul</b> : il avance vague après vague et abat les démons. Ton rôle : le rendre plus fort.' },
  { t: '#forgeBtn', h: 'La forge', p: 'Tout commence ici. Touche l\'<b>enclume</b> pour forger ton premier objet.', act: 'forge' },
  { t: '#mbox', h: 'Ton premier objet', p: 'L\'objet forgé est à gauche, ce que tu portes à droite. L\'emplacement est vide : touche <b>Équiper</b>.', act: 'close' },
  { t: '#forgeBtn', h: 'Encore une fois', p: 'Chaque forge te donne un objet au hasard : arme, armure, bottes… Forge-en un deuxième.', act: 'forge' },
  { t: '#mbox', h: 'Équiper ou recycler ?', p: 'S\'il est <b>plus puissant</b>, équipe-le. Sinon, <b>recycle-le</b> : tu gagnes de l\'or et des <b>éclats</b> pour améliorer ton équipement.', act: 'close' },
  { t: () => $('ham') && $('ham').closest('.res'), h: 'Les marteaux', p: 'Chaque forge coûte <b>1 marteau</b>. Ils se rechargent tout seuls avec le temps, et les quêtes en donnent.' },
  { t: '#bagBtn', h: 'L\'auto-forge', p: 'Active-la pour forger en boucle sans toucher à rien. Elle <b>s\'arrête</b> dès qu\'elle trouve un objet meilleur que le tien.' },
  { t: '#forgeLv', h: 'Le niveau de forge', p: 'Dépense ton or ici pour améliorer la forge : les objets <b>rares, épiques et légendaires</b> sortent plus souvent.' },
  { t: '#questBar', h: 'Les quêtes', p: 'Elles te guident pas à pas. Quand la barre est remplie, touche-la pour récupérer ta récompense.' },
  { t: '#stageBar', h: 'Les chapitres', p: 'Chaque chapitre compte <b>10 étapes</b> et se termine par un boss. Ta progression s\'affiche ici.' },
  { t: '#bossBtn', h: 'Défier le boss', p: 'Quand tu te sens prêt, lance le combat contre le boss. Trop fort ? Forge, monte de niveau et reviens.' },
  { t: '#nav [data-t="hero"]', h: 'Ton héros', p: 'Ses stats, ses <b>évolutions</b> aux niveaux 15, 30 et 60, ses ailes et son familier.' },
  { t: '#nav [data-t="talent"]', h: 'Les talents', p: 'Chaque niveau gagné te donne un <b>point de talent</b> à placer dans l\'arbre.' },
  { t: '#nav [data-t="skills"]', h: 'Les pouvoirs', p: 'Des sorts qui se lancent tout seuls pendant le combat. Équipe-les et améliore-les.' },
  { t: '#nav [data-t="dungeon"]', h: 'Les donjons', p: 'Farme de l\'or, de l\'XP et des pages avec tes tickets, et affronte le <b>raid</b> pour forger des ailes.' },
  { t: '#adminBtn', h: 'À toi de jouer !', p: 'Ce menu contient les options, et tu peux y <b>refaire ce tutoriel</b> quand tu veux. Bonne chasse !' },
];
const ARW = '<svg viewBox="0 0 24 24"><path d="M12 22 3 10h5V2h8v8h5z" fill="#ffd27a" stroke="#6a2a06" stroke-width="1.5" stroke-linejoin="round"/></svg>';
function coachStart(after) {
  if (CO) return; closeM && !$('modal').hidden && closeM();
  const nb = document.querySelector('#nav [data-t="forge"]'); if (nb) nb.click();
  S.auto.on = false; if (S.ham < 3) S.ham = 3; uiTop();
  const d = document.createElement('div'); d.id = 'coach';
  d.innerHTML = '<div class="cb"></div><div class="cb"></div><div class="cb"></div><div class="cb"></div><div class="cb cbh"></div><div class="ch"></div><div class="ca">' + ARW + '</div><div class="kg cbub"><div class="cst"></div><h4></h4><p></p><div class="crow"><button type="button" class="cskip">Passer le tutoriel</button><button type="button" class="btn gold cnext">Suivant</button></div></div>';
  document.body.appendChild(d);
  CO = { i: -1, el: d, after };
  d.querySelector('.cskip').onclick = () => coachEnd();
  d.querySelector('.cnext').onclick = () => coachStep(CO.i + 1);
  coachStep(0); requestAnimationFrame(coachLoop);
}
function coachTarget(st) { return typeof st.t === 'function' ? st.t() : document.querySelector(st.t); }
function coachStep(i) {
  if (!CO) return; if (i >= COACH.length) return coachEnd();
  const st = COACH[i], el = coachTarget(st); if (!el) return coachStep(i + 1);
  CO.i = i; CO.wait = st.act === 'forge' ? 'open' : st.act === 'close' ? 'close' : null; CO.t0 = performance.now();
  const d = CO.el; d.querySelector('.cst').textContent = `${i + 1} / ${COACH.length}`; d.querySelector('h4').textContent = st.h; d.querySelector('p').innerHTML = st.p;
  const last = i === COACH.length - 1; d.querySelector('.cnext').textContent = last ? 'C\'est parti !' : 'Suivant';
  d.querySelector('.cnext').hidden = !!st.act; d.querySelector('.cskip').hidden = last;
  d.querySelector('.cbh').style.display = st.act ? 'none' : 'block';
  coachPlace();
}
function coachPlace() {
  if (!CO) return; const st = COACH[CO.i], el = coachTarget(st); if (!el) return;
  const r = el.getBoundingClientRect(), W = innerWidth, Hh = innerHeight, pad = 6;
  const x0 = Math.max(0, r.left - pad), y0 = Math.max(0, r.top - pad), x1 = Math.min(W, r.right + pad), y1 = Math.min(Hh, r.bottom + pad);
  const d = CO.el, cb = d.querySelectorAll('.cb'), set = (e, l, t, w, h) => Object.assign(e.style, { left: l + 'px', top: t + 'px', width: Math.max(0, w) + 'px', height: Math.max(0, h) + 'px' });
  set(cb[0], 0, 0, W, y0); set(cb[1], 0, y1, W, Hh - y1); set(cb[2], 0, y0, x0, y1 - y0); set(cb[3], x1, y0, W - x1, y1 - y0); set(cb[4], x0, y0, x1 - x0, y1 - y0);
  set(d.querySelector('.ch'), x0, y0, x1 - x0, y1 - y0);
  const bub = d.querySelector('.cbub'), ar = d.querySelector('.ca'), bh = bub.offsetHeight, below = (y0 + y1) / 2 < Hh * 0.45, big = y1 - y0 > Hh * 0.38;
  ar.classList.toggle('up', below); ar.style.left = ((x0 + x1) / 2) + 'px';
  if (below) { ar.style.top = (y1 + 6) + 'px'; bub.style.top = Math.min(Hh - bh - 10, y1 + (big ? 10 : 48)) + 'px'; }
  else { ar.style.top = (y0 - 42) + 'px'; bub.style.top = Math.max(10, y0 - bh - (big ? 10 : 48)) + 'px'; }
  ar.style.display = big ? 'none' : 'block';
}
function coachLoop() {
  if (!CO) return; requestAnimationFrame(coachLoop);
  const open = !$('modal').hidden && !!$('eqB');
  if (CO.wait === 'open' && open) coachStep(CO.i + 1);
  else if (CO.wait === 'close' && $('modal').hidden && performance.now() - CO.t0 > 300) coachStep(CO.i + 1);
  coachPlace();
}
function coachEnd() { if (!CO) return; const a = CO.after; CO.el.remove(); CO = null; S.tutoDone = 1; save(); if (a) setTimeout(a, 300); }
