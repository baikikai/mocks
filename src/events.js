(function () {
  var st = { cat: '', loc: '', mo: '' };
  var mos = [].slice.call(document.querySelectorAll('.mo'));
  function apply() {
    var shown = 0;
    mos.forEach(function (m) {
      var any = 0;
      [].forEach.call(m.querySelectorAll('.ev'), function (e) {
        var ok = (!st.cat || e.getAttribute('data-cat') === st.cat) && (!st.loc || e.getAttribute('data-loc') === st.loc);
        e.hidden = !ok; if (ok) any++;
      });
      m.hidden = any === 0 || (st.mo !== '' && m.getAttribute('data-m') !== st.mo);
      if (!m.hidden) shown++;
    });
    var z = document.querySelector('.zero');
    z.hidden = shown > 0;
    z.textContent = st.mo !== '' ? 'No events this month.' : 'No events match these filters.';
  }
  [].forEach.call(document.querySelectorAll('.chip'), function (c) {
    c.addEventListener('click', function () {
      var g = c.getAttribute('data-g');
      st[g] = c.getAttribute('data-v');
      [].forEach.call(document.querySelectorAll('.chip[data-g="' + g + '"]'), function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      apply();
    });
  });
  document.querySelector('#mosel .ll').addEventListener('click', function (e) { var o = e.target.closest('button'); if (!o) return; st.mo = o.getAttribute('data-v'); apply(); });
  var f = document.querySelector('.reg'); if (f) f.addEventListener('submit', function (e) { e.preventDefault(); });
  apply();
})();
