(function () {
  var R = document.querySelector('[data-page="classes"]'); if (!R) return;
  var f = 'all';
  var wk = R.querySelector('.wk');
  var chips = [].slice.call(R.querySelectorAll('.chip'));
  function match(el) { return f === 'all' || (' ' + el.getAttribute('data-p') + ' ').indexOf(' ' + f.split(' ')[0] + ' ') > -1; }
  function apply() {
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-f') === f); });
    if (wk) wk.setAttribute('data-f', f);
    [].forEach.call(R.querySelectorAll('.day li'), function (r) { var m = match(r); r.classList.toggle('dim', f !== 'all' && !m); r.classList.toggle('hit', f !== 'all' && m); });
  }
  chips.forEach(function (c) { c.addEventListener('click', function () { f = c.getAttribute('data-f'); apply(); }); });
})();
