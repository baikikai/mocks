
/* event drawer: details and registration slide in from the right */
(function () {
  var d = document.getElementById('drawer'); if (!d) return;
  var root = document.documentElement, opener = null;
  function open(btn) {
    opener = btn; d.hidden = false; root.style.overflow = 'hidden';
    void d.offsetWidth; setTimeout(function () { d.classList.add('open'); var x = d.querySelector('.dr-x'); if (x) x.focus({ preventScroll: true }); }, 30);
  }
  function close() {
    if (d.hidden) return;
    d.classList.remove('open'); root.style.overflow = '';
    setTimeout(function () { d.hidden = true; }, 380);
    if (opener && opener.focus) opener.focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var o = e.target.closest && e.target.closest('[data-drawer]');
    if (o) { e.preventDefault(); open(o); return; }
    if (e.target === d || (e.target.closest && e.target.closest('.dr-x'))) close();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();

/* section labels only stick when the section is long enough to need it; short ones, and the last ones on a page, stay beside their text */
(function () {
  var queued = false;
  function upd() {
    queued = false;
    var wide = window.innerWidth > 900;
    var ah = document.querySelector('.ah'), sub = document.querySelector('.sub:not([hidden])');
    var avail = window.innerHeight - ((ah ? ah.offsetHeight : 0) + (sub ? sub.offsetHeight : 0) + 32);
    [].forEach.call(document.querySelectorAll('.pg:not([hidden]) .sec'), function (s) {
      var bd = s.querySelector(':scope > .bd');
      if (!wide || !bd) { s.classList.remove('ns'); return; }
      var h = bd.offsetHeight; if (!h) return;
      s.classList.toggle('ns', h <= avail * 0.9);
    });
  }
  function q() { if (!queued) { queued = true; requestAnimationFrame(upd); } }
  window.addEventListener('resize', q);
  window.addEventListener('load', function () { q(); setTimeout(q, 600); });
  window.addEventListener('hashchange', function () { setTimeout(q, 350); });
  document.addEventListener('click', function () { setTimeout(q, 450); setTimeout(q, 1000); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(q);
  if ('ResizeObserver' in window) { var m = document.querySelector('.mn'); if (m) new ResizeObserver(q).observe(m); }
  q();
})();
