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
    root.classList.toggle('hs', showSub);
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
      // a new page always opens at its top (the hero is pinned, so its offset follows the reader and cannot be used here)
      if (started) {
        var top0 = function () { window.scrollTo(0, 0); root.scrollTop = 0; document.body.scrollTop = 0; if (window.__navReset) window.__navReset(); };
        top0(); requestAnimationFrame(top0); setTimeout(top0, 120);
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
  function closeSheet(pre) {
    if (!sheet || sheet.hidden || sheet.classList.contains('closing') || sheet._leaving) return;
    sheet._leaving = true;
    setTimeout(function () {
      sheet.classList.add('closing');
      setTimeout(function () {
        sheet.classList.remove('open', 'closing'); root.style.overflow = ''; root.classList.remove('sheet-on');
        [].forEach.call(sheet.querySelectorAll('.chosen'), function (c) { c.classList.remove('chosen'); });
        sheet._leaving = false;
        setTimeout(function () { sheet.hidden = true; }, 650);
        if (opener && opener.focus) opener.focus({ preventScroll: true });
      }, 520);
    }, pre || 0);
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
      if (sheet && !sheet.hidden) { if (g.closest('#sheet')) g.classList.add('chosen'); closeSheet(g.closest('#sheet') ? 260 : 0); }
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

/* main nav. It stays where it is until the page (the jump nav) arrives and carries it off the top.
   Scrolling up brings it back as a bar; its black background fades to transparent as the scroll reaches the top. */
(function () {
  var nv = document.querySelector('.nv'); if (!nv) return;
  var root = document.documentElement, site = document.querySelector('.site'), home = nv.parentNode;
  var hero = nv.closest('.hr'), mn = document.querySelector('.mn');
  var last = window.pageYOffset, thr = 0;
  function isBar() { return nv.classList.contains('fx'); }
  function measure() { if (!isBar()) thr = nv.getBoundingClientRect().bottom + window.pageYOffset; }
  function show(on) {
    nv.classList.toggle('in', on);
    root.style.setProperty('--nvo', on ? nv.offsetHeight + 'px' : '0px');
  }
  window.__navReset = function () { if (window.pageYOffset <= 0.5 && isBar()) toHero(); };
  function toHero() {
    nv.classList.remove('fx', 'in'); nv.style.transform = ''; nv.style.removeProperty('--bar-a');
    root.style.setProperty('--nvo', '0px');
    if (nv.parentNode !== home) { var hh = home.querySelector('.hh'); home.insertBefore(nv, hh && hh.parentNode === home ? hh : null); }
  }
  function toBar() {
    if (isBar()) return;
    nv.classList.add('fx'); nv.style.transform = '';
    void nv.offsetWidth;
    if (site) site.insertBefore(nv, site.firstChild);
  }
  function tick() {
    var y = window.pageYOffset, dy = y - last; last = y;
    if (!isBar() && getComputedStyle(nv).position === 'fixed') return;            // a fixed rail never moves
    var sticky = hero && getComputedStyle(hero).position === 'sticky';
    if (!sticky) {                                                                  // reduced motion: the old rule
      if (y <= thr) toHero();
      else { toBar(); nv.style.setProperty('--bar-a', 1); if (dy < -4) show(true); else if (dy > 4) show(false); }
      return;
    }
    var navH = nv.offsetHeight, navBottom = hero.getBoundingClientRect().top + navH;
    var mnTop = mn && mn.offsetParent !== null ? mn.getBoundingClientRect().top : Infinity;
    var d = mnTop - navBottom;                                                      // >= 0 while the nav is clear of the page
    if (isBar()) {
      if (y <= 0.5) { toHero(); return; }                                           // at the very top: the transparent hero nav
      if (d >= -0.5 && dy > 4) { toHero(); return; }                                // heading back down over the hero: it rides with the hero again
      nv.style.setProperty('--bar-a', Math.max(0, Math.min(1, y / 160)).toFixed(3)); // the black fades to transparent over the last 160px to the top
      if (dy < -4) show(true); else if (dy > 4) show(false);
    } else {
      var push = Math.max(0, Math.min(navH, -d));
      if (push >= navH - 0.5) { toBar(); nv.style.setProperty('--bar-a', 1); show(dy < -4); }   // carried off the top
      else nv.style.transform = push ? 'translateY(' + (-push) + 'px)' : '';
    }
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


/* iOS only applies :active (and ignores :hover) for touch if a touch handler exists; this gives every pressable the same pressed state */
(function () {
  var cur = null;
  function on(e) {
    var t = e.target.closest && e.target.closest('.si,.pc.v,.cb,.sdon,.sm a,.sj a,.nv a,.ft a,.lb,.mb,.tg,button,a');
    if (t) { cur = t; t.classList.add('pr'); }
  }
  function off() { if (cur) { cur.classList.remove('pr'); cur = null; } }
  document.addEventListener('touchstart', on, { passive: true });
  ['touchend', 'touchcancel', 'touchmove'].forEach(function (n) { document.addEventListener(n, off, { passive: true }); });
})();
