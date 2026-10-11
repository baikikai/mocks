
/* ---- rev19 Index: the turning hero ---- */
(function () {
  var sl = document.querySelector('.hr .sl'); if (!sl) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var slides = [].slice.call(sl.querySelectorAll('.sl-s')), dots = [].slice.call(sl.querySelectorAll('.sl-c i')), pb = sl.querySelector('.sl-c button');
  var i = 0, timer = null, paused = reduce;
  function show(n) { slides[i].classList.remove('on'); dots[i].classList.remove('on'); i = n; slides[i].classList.add('on'); dots[i].classList.add('on'); }
  function tick() { if (!paused) show((i + 1) % slides.length); }
  function start() { if (!timer) timer = setInterval(tick, 5000); }
  function stop() { clearInterval(timer); timer = null; }
  if (pb) { pb.textContent = paused ? 'Play' : 'Pause'; pb.addEventListener('click', function () { paused = !paused; pb.textContent = paused ? 'Play' : 'Pause'; }); }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) start(); else stop(); }); }, { threshold: 0.7 }).observe(sl);
  else start();
})();
