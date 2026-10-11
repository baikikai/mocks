(function () {
  var pages = [].slice.call(document.querySelectorAll('.pg'));
  var sheet = document.getElementById('sheet');
  var opener = null;
  var root = document.documentElement;
  var started = false;
  function feather(s) {
    s.style.setProperty('--fl', s.scrollLeft > 2 ? '32px' : '0px');
    s.style.setProperty('--fr', s.scrollLeft + s.clientWidth < s.scrollWidth - 2 ? '32px' : '0px');
  }
  [].forEach.call(document.querySelectorAll('.sj'), function (s) { s.addEventListener('scroll', function () { feather(s); }, { passive: true }); });
  window.addEventListener('resize', function () { [].forEach.call(document.querySelectorAll('.sub:not([hidden]) .sj'), feather); });
  function show(k) {
    var page = null;
    pages.forEach(function (p) { if (p.getAttribute('data-page') === k) page = p; });
    if (!page) page = pages[0];
    k = page.getAttribute('data-page');
    root.setAttribute('data-pg', k);
    pages.forEach(function (p) { p.hidden = p !== page; });
    var group = page.getAttribute('data-group') || '';
    var section = page.getAttribute('data-section') || '';
    var main = document.querySelector('.mn');
    var hero = document.querySelector('.hr');
    // the jump nav of the page's group stays; the other groups' navs are hidden
    var showSub = false;
    [].forEach.call(document.querySelectorAll('.sub'), function (s) {
      var mine = s.getAttribute('data-group') === group;
      s.hidden = !mine; if (mine) showSub = true;
      [].forEach.call(s.querySelectorAll('[data-go]'), function (a) {
        var on = a.getAttribute('data-go') === (page.getAttribute('data-nav') || k);
        a.classList.toggle('on', on);
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
    });
    if (main) main.classList.toggle('has-sub', showSub);
    [].forEach.call(document.querySelectorAll('.sub:not([hidden]) .sj'), function (s) {
      var on = s.querySelector('.on');
      if (on && s.scrollWidth > s.clientWidth) s.scrollTo({ left: on.offsetLeft - (s.clientWidth - on.offsetWidth) / 2, behavior: started ? 'smooth' : 'auto' });
      feather(s);
    });
    // primary nav and hero follow the page
    [].forEach.call(document.querySelectorAll('.nv [data-sec]'), function (a) { a.classList.toggle('on', a.getAttribute('data-sec') === section); });
    if (hero) {
      hero.setAttribute('data-hero', page.getAttribute('data-hero') || 'plain');
      var h1 = hero.querySelector('h1');
      if (h1 && h1.getAttribute('data-k') !== k) {
        var rich = page.getAttribute('data-h1html');
        if (rich) h1.innerHTML = rich; else h1.textContent = page.getAttribute('data-title');
        h1.setAttribute('data-k', k);
        h1.classList.remove('sw'); void h1.offsetWidth; h1.classList.add('sw');
      }
      hero.setAttribute('data-img', page.getAttribute('data-img') || '');
      var au = hero.querySelector('.hh .au');
      if (au) au.textContent = page.getAttribute('data-author') || '';
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches, kind = page.getAttribute('data-hero');
      [].forEach.call(hero.querySelectorAll('.hv'), function (v) {
        var mine = (kind === 'home') === v.classList.contains('hvh') && (kind === 'video' || kind === 'home');
        if (mine && !reduce) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else v.pause();
      });
      // keep the reader where they are; only bring the new content to the top of the screen when they are below the hero
      if (started) {
        var top = hero.offsetTop + hero.offsetHeight;
        if (window.scrollY > top) window.scrollTo(0, top);
      }
    }
    started = true;
  }
  var leaving = false;
  function toSection(sec) {
    if (!sec) return;
    var hs = [].slice.call(document.querySelectorAll('.pg:not([hidden]) .lab h2')).filter(function (h) { return h.textContent.trim() === sec; });
    if (!hs[0]) return;
    var s = hs[0].closest('.sec'), sub = document.querySelector('.sub:not([hidden])');
    var off = (document.querySelector('.ah').offsetHeight) + (sub ? sub.offsetHeight : 0);
    window.scrollTo(0, s.getBoundingClientRect().top + window.pageYOffset - off);
  }
  function go(k, sec) {
    var cur = document.querySelector('.pg:not([hidden])');
    var same = cur && cur.getAttribute('data-page') === k;
    var mn = document.querySelector('.mn');
    if (same || leaving || !started || !mn || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { if (!leaving) { show(k); toSection(sec); } return; }
    leaving = true; mn.classList.add('out');
    setTimeout(function () { show(k); mn.classList.remove('out'); leaving = false; toSection(sec); }, 260);
  }
  function eff() {
    var t = root.getAttribute('data-site') || root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  function setTheme(t) {
    root.setAttribute('data-site', t);
    try { localStorage.setItem('site-theme', t); } catch (x) {}
  }
  try { var saved = localStorage.getItem('site-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-site', saved); } catch (x) {}
  function openSheet(btn) {
    opener = btn; sheet.hidden = false; root.style.overflow = 'hidden'; root.classList.add('sheet-on');
    requestAnimationFrame(function () { sheet.classList.add('open'); var x = sheet.querySelector('.sx'); if (x) x.focus({ preventScroll: true }); });
  }
  function closeSheet() {
    if (!sheet || sheet.hidden) return;
    sheet.classList.remove('open'); root.style.overflow = ''; root.classList.remove('sheet-on');
    setTimeout(function () { sheet.hidden = true; }, 650);
    if (opener && opener.focus) opener.focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('[data-tg]')) { setTheme(eff() === 'light' ? 'dark' : 'light'); return; }
    if (t.closest('[data-open]')) { openSheet(t.closest('[data-open]')); return; }
    if (t.closest('[data-close]')) { closeSheet(); return; }
    var g = t.closest('[data-go]');
    if (g) {
      e.preventDefault();
      var k = g.getAttribute('data-go');
      go(k, g.getAttribute('data-sec'));
      try { history.replaceState(null, '', '#' + k); } catch (x) {}
      if (sheet && !sheet.hidden) closeSheet();
      return;
    }
    var d = t.closest('[data-dead]');
    if (d) { e.preventDefault(); if (sheet && !sheet.hidden) closeSheet(); return; }
    if (t.closest('#sheet [data-go]')) closeSheet();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSheet();
    if (e.key === 'Tab' && sheet && !sheet.hidden) {
      var f = [].slice.call(sheet.querySelectorAll('a,button')); var a = document.activeElement;
      if (e.shiftKey && a === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && a === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  window.addEventListener('hashchange', function () { show(location.hash.slice(1)); });
  show(location.hash ? location.hash.slice(1) : '');
})();

(function () {
  function closeAll(except) {
    [].forEach.call(document.querySelectorAll('.lb[aria-expanded="true"]'), function (b) {
      if (b === except) return;
      b.setAttribute('aria-expanded', 'false'); b.nextElementSibling.hidden = true;
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.lb');
    if (b) {
      var open = b.getAttribute('aria-expanded') === 'true';
      closeAll(b);
      b.setAttribute('aria-expanded', open ? 'false' : 'true'); b.nextElementSibling.hidden = open;
      return;
    }
    var o = e.target.closest('.ll button');
    if (o && !o.disabled) {
      var lb = o.closest('.lang,.dd').querySelector('.lb');
      [].forEach.call(o.closest('.ll').querySelectorAll('button'), function (x) { x.setAttribute('aria-selected', x === o ? 'true' : 'false'); });
      var lf = lb.querySelector('.lf');
      if (lf) { lf.textContent = o.textContent; lb.querySelector('.ls').textContent = o.getAttribute('data-code') || o.textContent; }
      else lb.querySelector('span').textContent = o.textContent;
      if (o.closest('.lang')) [].forEach.call(o.closest('.ll').querySelectorAll('li'), function (li) { li.hidden = li.contains(o); });
    }
    closeAll(null);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { var open = document.querySelector('.lb[aria-expanded="true"]'); if (open) { closeAll(null); open.focus(); } }
  });
})();

/* main nav: leaves with the page, comes back as soon as the reader scrolls up.
   While it is the returning bar it lives outside the pinned hero, so the page cannot cover it. */
(function () {
  var nv = document.querySelector('.nv'); if (!nv) return;
  var root = document.documentElement, site = document.querySelector('.site'), home = nv.parentNode, last = window.pageYOffset, thr = 0;
  function measure() { if (!nv.classList.contains('fx')) thr = nv.getBoundingClientRect().bottom + window.pageYOffset; }
  function set(on) {
    nv.classList.toggle('in', on);
    root.style.setProperty('--nvo', on ? nv.offsetHeight + 'px' : '0px');
  }
  function tick() {
    var y = window.pageYOffset, dy = y - last;
    if (y <= thr) {
      nv.classList.remove('fx', 'in'); root.style.setProperty('--nvo', '0px');
      if (nv.parentNode !== home) { var hh = home.querySelector('.hh'); home.insertBefore(nv, hh && hh.parentNode === home ? hh : null); }
    } else {
      if (!nv.classList.contains('fx')) { nv.classList.add('fx'); if (site) site.insertBefore(nv, site.firstChild); }
      if (dy < -4) set(true); else if (dy > 4) set(false);
    }
    last = y;
  }
  measure(); window.addEventListener('resize', measure);
  window.addEventListener('scroll', tick, { passive: true });
})();

/* margin notes appear as they scroll into view; on narrow screens the highlighted word opens a centred card */
(function () {
  var root = document.documentElement, card = document.getElementById('ncard');
  if ('IntersectionObserver' in window) {
    root.classList.add('io');
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: 0.3 });
    [].forEach.call(document.querySelectorAll('.sn'), function (n) { io.observe(n); });
  }
  function note(k) { return document.querySelector('.pg:not([hidden]) .sn[data-k="' + k + '"]'); }
  function open(t) {
    if (!card || window.matchMedia('(min-width:1280px)').matches) return;
    var n = note(t.getAttribute('data-k')); if (!n) return;
    card.querySelector('.nc-body').innerHTML = n.innerHTML;
    card.hidden = false; requestAnimationFrame(function () { card.classList.add('open'); card.querySelector('.nc-x').focus({ preventScroll: true }); });
    card._from = t;
  }
  function close() {
    if (!card || card.hidden) return;
    card.classList.remove('open'); setTimeout(function () { card.hidden = true; }, 250);
    if (card._from && card._from.focus) card._from.focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('.tm');
    if (t) { open(t); return; }
    if (e.target.closest && (e.target.closest('.nc-x') || e.target === card)) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
    var t = e.target.closest && e.target.closest('.tm');
    if (t && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); open(t); }
  });
  document.addEventListener('mouseover', function (e) {
    var t = e.target.closest && e.target.closest('.tm'); if (!t) return;
    var n = note(t.getAttribute('data-k')); if (!n) return;
    n.classList.add('hl'); t.addEventListener('mouseleave', function () { n.classList.remove('hl'); }, { once: true });
  });
})();

/* home: video progress along the bottom edge, and the footer height the hero leaves room for */
(function () {
  var v = document.querySelector('.hvh'), bar = document.querySelector('.hp'), root = document.documentElement;
  if (v && bar) v.addEventListener('timeupdate', function () { if (v.duration) bar.style.width = (v.currentTime / v.duration * 100) + '%'; });
  function ft() { var f = document.querySelector('.ft'); if (f) root.style.setProperty('--ft-h', f.offsetHeight + 'px'); }
  ft(); window.addEventListener('resize', ft); window.addEventListener('load', ft);
})();
