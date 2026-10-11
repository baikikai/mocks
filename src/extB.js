
/* ---- rev18 Pigment ---- */
/* mega menu */
(function () {
  var mega = document.getElementById('mega'); if (!mega) return;
  var nv = function () { return document.querySelector('.nv'); };
  var t = null;
  function wide() { return window.matchMedia('(min-width:901px)').matches; }
  function open(sec) {
    if (!wide()) return;
    var g = mega.querySelector('.mg[data-g="' + sec + '"]'); if (!g) { close(0); return; }
    clearTimeout(t);
    [].forEach.call(mega.querySelectorAll('.mg'), function (x) { x.classList.toggle('on', x === g); });
    mega.style.top = nv().getBoundingClientRect().bottom + 'px';
    mega.classList.add('open');
  }
  function close(d) { clearTimeout(t); t = setTimeout(function () { mega.classList.remove('open'); }, d === undefined ? 140 : d); }
  [].forEach.call(document.querySelectorAll('.nv nav .nl,.nv nav .don'), function (a) {
    var sec = a.getAttribute('data-sec');
    a.addEventListener('mouseenter', function () { open(sec); });
    a.addEventListener('focus', function () { open(sec); });
    a.addEventListener('mouseleave', function () { close(); });
  });
  mega.addEventListener('mouseenter', function () { clearTimeout(t); });
  mega.addEventListener('mouseleave', function () { close(); });
  [].forEach.call(mega.querySelectorAll('li a'), function (a) {
    function th() { mega.querySelector('.mg.on .mth').setAttribute('data-p', a.getAttribute('data-p')); }
    a.addEventListener('mouseenter', th); a.addEventListener('focus', th);
    a.addEventListener('click', function () { close(0); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(0); });
  window.addEventListener('scroll', function () { if (mega.classList.contains('open')) close(0); }, { passive: true });
})();

/* anchors: the sections of the current page, with scroll-spy */
(function () {
  var mn = document.querySelector('.mn'), anc = document.querySelector('nav.sub.anc'); if (!mn || !anc) return;
  var sj = anc.querySelector('.sj'), secs = [], links = [], queued = false;
  function offset() { var ah = document.querySelector('.ah'); return (ah ? ah.offsetHeight : 0) + anc.offsetHeight; }
  function build() {
    var pg = document.querySelector('.pg:not([hidden])'); secs = []; links = []; sj.innerHTML = '';
    var hs = pg ? [].slice.call(pg.querySelectorAll('.sec .lab h2')).filter(function (h) { return h.textContent.trim(); }) : [];
    if (hs.length < 3) { anc.hidden = true; mn.classList.remove('has-sub'); return; }
    hs.forEach(function (h) {
      var s = h.closest('.sec'), a = document.createElement('a');
      a.className = 'lk'; a.href = '#'; a.textContent = h.textContent.trim();
      a.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo(0, s.getBoundingClientRect().top + window.pageYOffset - offset() + 1); });
      sj.appendChild(a); secs.push(s); links.push(a);
    });
    anc.hidden = false; mn.classList.add('has-sub'); spy();
  }
  function spy() {
    var y = offset() + 40, cur = -1;
    secs.forEach(function (s, i) { if (s.getBoundingClientRect().top <= y) cur = i; });
    links.forEach(function (a, i) { var on = i === cur; a.classList.toggle('on', on); if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    var on = links[cur];
    if (on && sj.scrollWidth > sj.clientWidth) sj.scrollTo({ left: on.offsetLeft - (sj.clientWidth - on.offsetWidth) / 2, behavior: 'smooth' });
  }
  var qt = null;
  function q(d) { clearTimeout(qt); qt = setTimeout(build, d || 0); }
  window.addEventListener('scroll', function () { if (!anc.hidden) spy(); }, { passive: true });
  window.addEventListener('resize', function () { q(0); });
  window.addEventListener('hashchange', function () { q(500); });
  document.addEventListener('click', function (e) { if (e.target.closest && (e.target.closest('[data-go]') || e.target.closest('.ll button'))) q(650); });
  window.addEventListener('load', function () { q(300); });
  q(0);
})();

/* hero lines: the words slide in line by line */
(function () {
  var h = document.querySelector('.hr .hh h1'); if (!h) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function wrap(node) {
    [].slice.call(node.childNodes).forEach(function (c) {
      if (c.nodeType === 3) {
        var frag = document.createDocumentFragment();
        c.nodeValue.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) frag.appendChild(document.createTextNode(w));
          else { var s = document.createElement('span'); s.className = 'wd'; s.textContent = w; frag.appendChild(s); }
        });
        node.replaceChild(frag, c);
      } else if (c.nodeType === 1 && c.tagName !== 'BR') wrap(c);
    });
  }
  function lines() {
    var tops = [], ws = [].slice.call(h.querySelectorAll('.wd'));
    ws.forEach(function (w) { var t = Math.round(w.offsetTop); if (tops.indexOf(t) < 0) tops.push(t); w.style.setProperty('--ln', tops.indexOf(Math.round(w.offsetTop))); });
  }
  var busy = false;
  function run() {
    if (busy || reduce) return; busy = true;
    h.setAttribute('data-sp', h.textContent); wrap(h); lines(); busy = false;
  }
  new MutationObserver(function () { if (busy) return; if (h.getAttribute('data-sp') === h.textContent && h.querySelector('.wd')) return; run(); }).observe(h, { childList: true, characterData: true, subtree: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (h.querySelector('.wd')) lines(); });
  run();
})();

/* section labels slide in once, the first time they enter */
(function () {
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: 0.2 });
  [].forEach.call(document.querySelectorAll('.lab h2'), function (h) { io.observe(h); });
  document.documentElement.classList.add('io-h');
})();
