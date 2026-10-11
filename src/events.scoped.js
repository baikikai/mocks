(function () {
  var R = document.querySelector('[data-page="events"]'); if (!R) return;
  var st = { cat: '', loc: '', mo: '', yr: '' };
  var mos = [].slice.call(R.querySelectorAll('.mo'));
  var yrs = [].slice.call(R.querySelectorAll('.yr'));
  function apply() {
    yrs.forEach(function (y) {
      var shown = 0;
      y.hidden = st.yr !== '' && y.getAttribute('data-y') !== st.yr;
      [].forEach.call(y.querySelectorAll('.mo'), function (m) {
        var any = 0;
        [].forEach.call(m.querySelectorAll('.ev'), function (e) {
          var ok = (!st.cat || e.getAttribute('data-cat') === st.cat) && (!st.loc || e.getAttribute('data-loc') === st.loc);
          e.hidden = !ok; if (ok) any++;
        });
        m.hidden = any === 0 || (st.mo !== '' && m.getAttribute('data-m') !== st.mo);
        if (!m.hidden) shown++;
      });
      var z = y.querySelector('.zero');
      z.hidden = shown > 0;
      z.textContent = st.mo !== '' ? 'No events this month.' : 'No events match these filters.';
    });
  }
  [].forEach.call(R.querySelectorAll('.chip'), function (c) {
    c.addEventListener('click', function () {
      var g = c.getAttribute('data-g');
      st[g] = c.getAttribute('data-v');
      [].forEach.call(R.querySelectorAll('.chip[data-g="' + g + '"]'), function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      apply();
    });
  });
  R.querySelector('#mosel .ll').addEventListener('click', function (e) { var o = e.target.closest('button'); if (!o) return; st.mo = o.getAttribute('data-v'); apply(); });
  R.querySelector('#yrsel .ll').addEventListener('click', function (e) { var o = e.target.closest('button'); if (!o) return; st.yr = o.getAttribute('data-v'); apply(); });
  var f = R.querySelector('.reg'); if (f) f.addEventListener('submit', function (e) { e.preventDefault(); });
  apply();
})();
