"""Technique database v14 (font set D): the v13 prototype as a real page on rev16's utility bar and footer."""
import re, os, sys, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build_all as BA
B = BA.B
SRC = 'technique-entry-prototype-v13.html'
REV16 = {'desktop': '/rev16/', 'mobile': '/rev16/mobile/'}

# ---------------- tiny css parser
def strip_comments(c): return re.sub(r'/\*.*?\*/', '', c, flags=re.S)
def parse(css):
    out = []; i = 0; n = len(css)
    while i < n:
        j = i; depth_paren = 0
        while j < n and css[j] not in '{;':
            j += 1
        if j >= n: out.append(('raw', css[i:].strip())); break
        pre = css[i:j].strip()
        if css[j] == ';': out.append(('raw', pre + ';')); i = j + 1; continue
        k = j + 1; d = 1
        while k < n and d:
            ch = css[k]
            if ch in '"\'':
                q = ch; k += 1
                while k < n and css[k] != q: k += 1
            elif ch == '{': d += 1
            elif ch == '}': d -= 1
            k += 1
        body = css[j + 1:k - 1]
        if pre.startswith(('@media', '@supports')): out.append(('at', pre, parse(body)))
        else: out.append(('rule', pre, body))
        i = k
    return out
def split_sel(s):
    parts = []; d = 0; cur = ''
    for ch in s:
        if ch in '([': d += 1
        if ch in ')]': d -= 1
        if ch == ',' and d == 0: parts.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): parts.append(cur.strip())
    return parts
def filt(nodes, keep):
    res = []
    for nd in nodes:
        if nd[0] == 'rule':
            if nd[1].startswith('@'):
                if keep(nd[1], True): res.append(nd)
                continue
            sels = [s for s in split_sel(nd[1]) if keep(s, False)]
            if sels: res.append(('rule', ', '.join(sels), nd[2]))
        elif nd[0] == 'at':
            ch = filt(nd[2], keep)
            if ch: res.append(('at', nd[1], ch))
        else: res.append(nd)
    return res
def emit(nodes):
    o = ''
    for nd in nodes:
        if nd[0] == 'rule': o += nd[1] + '{' + nd[2] + '}\n'
        elif nd[0] == 'at': o += nd[1] + '{\n' + emit(nd[2]) + '}\n'
        else: o += nd[1] + '\n'
    return o

CHROME = re.compile(r'^(?:\.ah|\.th|\.tg|\.ic|\.lang|\.lb|\.ll|\.arl|\.chev|\.sr|\.ft|\.lk|\.dead|:root|html\[lang|\*|a$|button|:focus-visible)(?![\w-])')
def chrome_keep(sel, at):
    if at: return False
    if sel.startswith('button') and sel != 'button' and not sel.startswith('button,'): return False
    return bool(CHROME.match(sel))

def css16(mobile):
    s2 = open('system2.css').read()
    tail = s2 + BA.HOMECSS
    if mobile:
        css = (B.CSS + open('ext.css').read() + open('mobile.css').read() + open('rev16.css').read() + open('rev16-m.css').read() + BA.FIX + B.SYS(True) + tail)
    else:
        narrow = open('mobile.css').read() + open('rev16-m.css').read()
        css = (B.CSS + open('ext.css').read() + open('desktop.css').read() + open('sheet.css').read() + open('rev16.css').read() + open('rev16-d.css').read()
               + '@media (max-width:900px){\n' + narrow + '\n}\n' + BA.FIX + B.SYS(False) + tail)
    css = re.sub(r'url\(data:[^)]*\)', 'none', strip_comments(css))
    return emit(filt(parse(css), chrome_keep))

# ---------------- source pieces
S = open(SRC).read()
def between(a, b, s=S):
    i = s.index(a); return s[i + len(a):s.index(b, i + len(a))]
PROTO_CSS = strip_comments(between('<style>', '</style>'))
JS1 = between('<script>\n(function () {\n  var DATA', '</script>')
JS1 = '(function () {\n  var DATA' + JS1

def proto_keep(sel, at):
    if at: return True
    bad = ('.sh', '.sf', '#dbar', '#dsw', '#vp', '#stage', '.zc', 'html[data-k', 'html,html[data-k', 'html[lang', 'html[data-eff', 'html{--K', '.lsel', '.app>.sh', ':root', 'html, body', 'html,body', 'body')
    return not any(sel.startswith(b) for b in bad)
def proto_nodes():
    nodes = filt(parse(PROTO_CSS), proto_keep)
    res = []
    for nd in nodes:
        if nd[0] == 'rule' and nd[1].startswith('@keyframes shin'): continue
        res.append(nd)
    return emit(res)
APP_CSS = proto_nodes()

THEME = '''
:root{--ink:#14171C;--ink2:#1D2128;--paper:#ECEDE8;--stone:#C4C8C0;--indigo:#2C3E72;--lilac:#9AA7D4;--muted-d:#4B5058;--rule-d:#3A3F47;--hov:#DADCD5;--display:'Shippori Mincho','Hiragino Mincho ProN',serif;--body:'Zen Kaku Gothic New','Hiragino Sans',system-ui,sans-serif;--K:'Zen Kaku Gothic New','Hiragino Sans',sans-serif}
@media (prefers-color-scheme: light){:root:not([data-site="dark"]):not([data-theme="dark"]){--ink:#ECEDE8;--ink2:#E2E4DD;--paper:#14171C;--stone:#4B5058;--muted-d:#B5B9B1;--rule-d:#C4C8C0;--lilac:#2C3E72;--indigo:#9AA7D4;--hov:#232830}}
:root[data-site="light"],:root[data-theme="light"]{--ink:#ECEDE8;--ink2:#E2E4DD;--paper:#14171C;--stone:#4B5058;--muted-d:#B5B9B1;--rule-d:#C4C8C0;--lilac:#2C3E72;--indigo:#9AA7D4;--hov:#232830}
:root[data-site="dark"],:root[data-theme="dark"]{--ink:#14171C;--ink2:#1D2128;--paper:#ECEDE8;--stone:#C4C8C0;--indigo:#2C3E72;--lilac:#9AA7D4;--muted-d:#4B5058;--rule-d:#3A3F47;--hov:#DADCD5}
.ecum{flex-wrap:wrap;gap:6px 14px}.ecum button{white-space:nowrap}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:normal}
html[lang="zh-Hans"]{--display:'Shippori Mincho','PingFang SC','Songti SC',serif;--body:'Zen Kaku Gothic New','PingFang SC','Microsoft YaHei',sans-serif}
.app{min-height:100%;display:flex;flex-direction:column}
.app>.sh,.app>.crumbs,.app>.ft{flex:none}
.sh{view-transition-name:site-header}
.sh .ah{position:relative;top:auto}
.sh .ah{height:64px;min-height:64px;border-bottom:1px solid var(--barline)}
.ah .arl.ttl{font-family:var(--display);font-size:22px;line-height:1.2;letter-spacing:-.01em;white-space:nowrap;max-width:none;overflow:visible;display:flex;gap:10px}
.ah .arl.ttl span:last-child{color:var(--barmut)}
.ah .arl.ttl:hover span{color:var(--gt)}
/* detail: the video leads, the rest is a narrow side column */
.split.dt{grid-template-columns:minmax(0,1fr) 340px}
.dt .left .video{min-height:260px}
.dt .left .big{font-size:clamp(30px,3.6vw,48px);line-height:1.05}
.dt .rbody{padding:20px 24px;gap:16px}
.dt .left .seg{margin:4px 0 6px}
.dt .left .seg button{border-color:var(--paper)}
.dt .left .seg button.on{background:var(--paper);color:var(--ink)}
.split.dt.solo{grid-template-columns:minmax(0,1fr)}
.dt .others .row{min-height:44px}
.onone{color:var(--stone);font-family:var(--body);font-size:15px;padding:12px 0}
.dt .others .rl{font-size:17px}
/* demonstration modal */
.left .video[data-act=demo]{cursor:pointer}
.left .video[data-act=demo]:hover .play{background:var(--paper);color:var(--ink)}
.dm{position:fixed;inset:0;z-index:100;visibility:hidden;pointer-events:none;background:rgba(8,10,13,0);transition:background-color .35s cubic-bezier(.2,.7,.2,1),visibility 0s linear .35s}
.dm.open{visibility:visible;pointer-events:auto;background:rgba(8,10,13,.72);transition:background-color .35s cubic-bezier(.2,.7,.2,1),visibility 0s}
.dm-card{position:absolute;inset:5vmin;display:flex;flex-direction:column;gap:16px;padding:24px;background:var(--ink2);color:var(--paper);border:1px solid var(--rule-d);opacity:0;transform:translateY(40px);transition:opacity .35s cubic-bezier(.2,.7,.2,1),transform .35s cubic-bezier(.2,.7,.2,1);overflow:auto}
.dm.open .dm-card{opacity:1;transform:none}
.dm.out .dm-card{transform:translateY(-40px)}
.dm-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}
.dm-head .big{font-family:var(--display);font-size:clamp(26px,3.2vw,40px);line-height:1.1}
.dm-x{flex:none;border:1px solid var(--paper);padding:8px 16px;font-size:13px;font-family:var(--body);color:var(--paper);background:transparent}
.dm-x:hover{background:var(--paper);color:var(--ink)}
.dm-card .seg{margin:0}
.dm-card .seg button{border-color:var(--paper)}
.dm-card .seg button.on{background:var(--paper);color:var(--ink)}
.dm-card .video{flex:1;min-height:0;aspect-ratio:auto}
@media (max-width:900px){.dm-card{padding:16px;gap:12px}.dm-card .video{flex:none;aspect-ratio:16/9}}
@media (prefers-reduced-motion:reduce){.dm,.dm-card{transition:none}}
.crumbs{padding-inline:var(--pad)}
.ft{view-transition-name:site-footer;margin-top:0}
#view{flex:1;min-height:620px;display:flex;background:var(--ink2)}
.label,.link,.play,.seg button,.otitle,.steps span,.group,.ecum,.pill b,.pin span{font-family:var(--body)}
@media (max-width:900px){
  html,body{height:auto}
  .app{min-height:100svh}
  .ah .arl.ttl{flex-direction:column;align-items:center;gap:0;font-size:17px;line-height:1.25;text-align:center}
  .split.dt{grid-template-columns:none}
  .dt .left .video{min-height:0}
  .dt .left .big{font-size:clamp(30px,9vw,40px)}
  .dt .rbody{padding:20px var(--pad)}
  .crumbs{padding:12px var(--pad)}
  #view{flex:none;display:block;min-height:0}
  .ent,.cols{display:block}
  .col{border-right:0;border-bottom:1px solid var(--rule-d);padding:18px 0 0}
  .col .head{padding:0 var(--pad) 12px}
  .col h2{font-size:28px}
  .col .list{display:flex;flex-wrap:wrap;gap:8px;padding:12px var(--pad) 18px;overflow:visible}
  .item,.item:hover,.cols .item.sel:hover,.cols .item.off:hover{width:auto;padding:9px 14px;border:1px solid var(--rule-d);border-radius:999px;font-size:17px;gap:8px}
  .item:hover{background:transparent}
  .cols .item.sel{border-color:var(--indigo)}
  .split{display:flex;flex-direction:column}
  .left{padding:24px var(--pad);overflow:visible;border-right:0;border-bottom:1px solid var(--rule-d)}
  .left .big{font-size:clamp(34px,11vw,56px)}
  .left .video{flex:none;min-height:0;aspect-ratio:16/9}
  .right,.rscroll{overflow:visible}
  .rhead{padding:20px var(--pad) 12px}
  .rhead h3{font-size:24px}
  .row,.row:hover{padding-left:var(--pad);padding-right:var(--pad);min-height:56px}
  .row.all{padding-right:var(--pad)}
  .dock{display:none;position:sticky;bottom:0;z-index:5;grid-template-columns:minmax(0,1fr)}
  .dock.on{display:grid;height:auto;max-height:55svh;overflow-y:auto}
  .dock .dl{padding:18px var(--pad);border-right:0;border-bottom:1px solid var(--rule-d)}
  .dock .dl .link{margin-top:6px}
}
'''

# ---------------- app js edits
def P(js, a, b, count=1):
    assert a in js, a[:70]
    return js.replace(a, b, count)
WAZA_JS = '''  function wazaView() {
    var w = state.waza;
    var back = '<button type="button" class="link" data-act="back">Back to Results</button>';
    if (w.weapon) {
      $view.innerHTML = '<div class="split dt solo"><div class="left"><span class="label" style="color:var(--lilac)">Introduced at ' + RANKS[w.rank] + '</span><div class="big">' + esc(w.name) + '</div><div class="video" data-act="demo"><button type="button" class="play">View Demonstration</button></div><button type="button" class="link" data-act="back">Back</button></div></div>';
      return;
    }
    var others = R.filter(function (x) { return x.t === w.t && x.s === w.s && x.id !== w.id; });
    var oh = others.slice(0, 6).map(function (x, i) {
      return '<button type="button" class="row" style="--i:' + i + '" data-act="open" data-id="' + x.id + '"><span class="rl">' + esc(ATK[x.a] + (x.v ? ' ' + x.v : '')) + '</span><span class="rm">' + RANKS[x.r] + ' \\u2192</span></button>';
    }).join('');
    var lp2 = '<div class="left"><span class="label" style="color:var(--lilac)">Introduced at ' + RANKS[w.r] + '</span><div class="big">' + esc(wazaName(w)) + '</div>' +
      '<div class="seg"><button type="button" data-act="omote" data-v="Omote" class="' + (state.omote === 'Omote' ? 'on' : '') + '">Omote</button><button type="button" data-act="omote" data-v="Ura" class="' + (state.omote === 'Ura' ? 'on' : '') + '">Ura</button></div>' +
      '<div class="video" data-act="demo"><button type="button" class="play">View Demonstration</button></div>' + back + '</div>';
    var rt = '<div class="right"><div class="rbody"><div class="others"><div class="otitle">Other Attacks, ' + esc(TECH[w.t][0]) + ' from ' + esc(ST[w.s][0]) + '</div>' + (others.length ? oh : '<div class="onone">None Recorded</div>') + '</div></div></div>';
    $view.innerHTML = '<div class="split dt">' + lp2 + rt + '</div>';
  }
'''


DEMO_JS = '''
(function () {
  var dm = null, last = null, om = 'Omote';
  function build(name) {
    dm = document.createElement('div'); dm.className = 'dm'; dm.setAttribute('role', 'dialog'); dm.setAttribute('aria-modal', 'true');
    dm.innerHTML = '<div class="dm-card"><div class="dm-head"><div class="big"></div><button type="button" class="dm-x" data-dm="close">Close</button></div>' +
      '<div class="seg"><button type="button" data-dm="Omote">Omote</button><button type="button" data-dm="Ura">Ura</button></div>' +
      '<div class="video"><button type="button" class="play">Play Demonstration</button></div></div>';
    document.body.appendChild(dm);
    dm.addEventListener('click', function (e) {
      var b = e.target.closest('[data-dm]');
      if (e.target === dm || (b && b.getAttribute('data-dm') === 'close')) { close(); return; }
      if (b) { om = b.getAttribute('data-dm'); mark(); }
    });
  }
  function mark() { [].forEach.call(dm.querySelectorAll('.seg button'), function (b) { b.classList.toggle('on', b.getAttribute('data-dm') === om); }); }
  function open(from) {
    last = from; if (!dm) build();
    var big = document.querySelector('#view .left .big');
    dm.querySelector('.big').textContent = big ? big.textContent : '';
    dm.classList.remove('out'); mark();
    if (window.__xl) window.__xl(dm);
    void dm.offsetWidth; dm.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    dm.querySelector('.dm-x').focus();
  }
  function close() {
    if (!dm || !dm.classList.contains('open')) return;
    dm.classList.add('out'); dm.classList.remove('open');
    document.documentElement.style.overflow = '';
    if (last && document.contains(last)) last.focus();
  }
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-act="demo"]'); if (b) open(b.querySelector('button') || b); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
'''

def app_js():
    j = JS1
    # roman numerals without dots
    for r in ('IV', 'II', 'III', 'I'):
        j = j.replace("roman: '%s.'" % r, "roman: '%s'" % r)
    j = P(j, "var roman = ['I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.', 'VIII.', 'IX.', 'X.', 'XI.', 'XII.', 'XIII.', 'XIV.', 'XV.', 'XVI.', 'XVII.', 'XVIII.', 'XIX.', 'XX.', 'XXI.'];",
          "var roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI'];")
    j = P(j, '<span class="num">V.</span>', '<span class="num">V</span>')
    j = P(j, "if (facet === 'technique') return TECH[value];", "if (facet === 'technique') return [TECH[value][0], ''];")
    j = P(j, "if (facet === 'stance') return ST[value];", "if (facet === 'stance') return [ST[value][0], ''];")
    # no small text under the column titles
    j = P(j, "<h2>' + f.title + '</h2><div class=\"sub\">' + subs[facet] + '</div>' + (extra || '')", "<h2>' + f.title + '</h2>' + (extra || '')")
    j = P(j, "<h2>Weapons</h2><div class=\"sub\">Buki-waza 武器技</div>", "<h2>Weapons</h2>")
    # title case on interface text
    for a, b in (("'Choose a technique'", "'Choose a Technique'"), ("'Choose a stance'", "'Choose a Stance'"), ("'Choose an attack'", "'Choose an Attack'"),
                 ("'Choose a variant'", "'Choose a Variant'"), ("'Choose a rank'", "'Choose a Rank'"), ('>Start over<', '>Start Over<'), ('>Back to results<', '>Back to Results<'),
                 ('>Play demonstration<', '>Play Demonstration<'), ('>New at rank<', '>New at Rank<'), ('>Up to rank<', '>Up to Rank<'), ("'Entry points'", "'Entry Points'"),
                 ('>Entry points<', '>Entry Points<'), ("'All waza'", "'All Waza'"), ("All ' + all.length + ' waza", "All ' + all.length + ' Waza"), ("'Any ' + FAC[f].title.toLowerCase()", "'Any ' + FAC[f].title"),
                 ("'Other attacks, '", "'Other Attacks, '"), ('Other attacks, ', 'Other Attacks, ')):
        j = j.replace(a, b)
    j = j.replace('>Back to Results<', '>Back to Results<')
    k0 = j.index('  function wazaView() {'); k1 = j.index('  function render() {', k0)
    j = j[:k0] + WAZA_JS + '\n' + j[k1:]
    # the dock hint: no inline link
    j = P(j, '''right = '<div class="dr"><div class="hint">' + m.length + ' waza match. Keep choosing to reach one, or <button type="button" class="link" data-act="eresolve" style="display:inline">open the list</button>.</div></div>';''',
          '''right = '<div class="dr"><div class="hint">' + m.length + ' waza match. Keep choosing to reach one.<br><button type="button" class="link" data-act="eresolve" style="margin:12px auto 0">Open the List</button></div></div>';''')
    # a robust view transition: if the browser never runs the callback, apply the change anyway
    k = j.index('  function go(update, fromEl, toSel) {'); e = j.index('  document.addEventListener(\'click\', function (e) {', k)
    new_go = '''  function go(update, fromEl, toSel) {
    var before = DEPTH[state.view] || 0;
    if (!fromEl && !toSel) { update(); render(); return; }
    if (!document.startViewTransition || reduce) { update(); render(); return; }
    var done = false;
    function nameAll(on) {
      var els = document.querySelectorAll('.left, .right, .col');
      for (var i = 0; i < els.length; i++) {
        var n = els[i].classList.contains('left') ? 'pl' : els[i].classList.contains('right') ? 'pr' : 'c' + i;
        els[i].style.viewTransitionName = on ? n : '';
      }
    }
    function step() {
      if (done) return; done = true;
      update();
      document.documentElement.setAttribute('data-dir', (DEPTH[state.view] || 0) < before ? 'back' : 'fwd');
      render();
    }
    nameAll(true);
    var t;
    try {
      t = document.startViewTransition(function () { nameAll(false); step(); nameAll(true); });
    } catch (err) { nameAll(false); step(); return; }
    t.finished.then(function () { nameAll(false); }, function () { nameAll(false); });
    document.documentElement.setAttribute('data-dir', 'fwd');
    setTimeout(function () { if (!done) { nameAll(false); step(); } }, 900);
  }

'''
    j = j[:k] + new_go + j[e:]
    # translate after every paint
    j = P(j, "    $crumbs.innerHTML = h;\n  }", "    $crumbs.innerHTML = h;\n  }")
    j = P(j, "    else wazaView();\n  }", "    else wazaView();\n    if (window.__xl) window.__xl(document.getElementById('crumbs')), window.__xl($view);\n  }")
    j = P(j, "      el.classList.add('on');\n    } else el.classList.remove('on');", "      el.classList.add('on');\n      if (window.__xl) window.__xl(el);\n    } else el.classList.remove('on');")
    j = j.replace("  render();\n})();", "  window.__render = function () { var d = document.querySelector('.dock'); if (d) d.removeAttribute('data-sig'); render(); if (state.view === 'entry') epaint(false); };\n  render();\n})();")
    return j

LANGSEL = between('(function () {\n  function closeAll(except) {', '})();\n', open('app.js').read())
LANGJS = '(function () {\n  function closeAll(except) {' + LANGSEL + '})();\n'

def i18n_dicts():
    js = open('i18n.js').read(); a = js.index('var D=') + 6; b = js.index('\nvar orig'); D = json.loads(js[a:b])
    keep = ['Our Commitment to Anti-Racism', 'Contact', 'Accessibility', 'Instagram', 'Site Credits', 'Brooklyn Aikikai is a 501(c)(3)', 'EIN: 26-1693436', '@aria-label:Toggle light and dark mode', '@aria-label:Language']
    return {k: D[k] for k in keep if k in D}
HDR = i18n_dicts()
TECHD = {
 'Entry Points': ('Puntos de Entrada', '入口'), 'Rank': ('Rango', '级别'), 'Stance': ('Postura', '姿势'), 'Attack': ('Ataque', '攻击'), 'Technique': ('Técnica', '技法'),
 'Weapons': ('Armas', '武器'), 'Variant': ('Variante', '变体'), 'Chain': ('Cadena', '组合'), 'Clear': ('Borrar', '清除'), 'New at Rank': ('Nuevo en el Rango', '该级别新增'),
 'Up to Rank': ('Hasta el Rango', '截至该级别'), 'Choose a Technique': ('Elige una Técnica', '选择技法'), 'Choose a Stance': ('Elige una Postura', '选择姿势'),
 'Choose an Attack': ('Elige un Ataque', '选择攻击'), 'Choose a Rank': ('Elige un Rango', '选择级别'), 'Choose a Variant': ('Elige una Variante', '选择变体'),
 'Start Over': ('Empezar de Nuevo', '重新开始'), 'Back': ('Atrás', '返回'), 'Back to Results': ('Volver a los Resultados', '返回结果'), 'Play Demonstration': ('Ver Demostración', '播放示范'),
 'All Waza': ('Todos los Waza', '全部技法'), 'Weapon': ('Arma', '武器'), 'Standard': ('Estándar', '标准'), 'Grouped by rank': ('Agrupado por rango', '按级别分组'),
 'Open the List': ('Abrir la Lista', '打开列表'), 'Any Stance': ('Cualquier Postura', '任意姿势'), 'Any Attack': ('Cualquier Ataque', '任意攻击'), 'Any Technique': ('Cualquier Técnica', '任意技法'),
 'Any Rank': ('Cualquier Rango', '任意级别'), 'Any Variant': ('Cualquier Variante', '任意变体'), 'Technique Database': ('Base de Datos de Técnicas', '技法数据库'),
 'View Demonstration': ('Ver Demostración', '观看演示'), 'Close': ('Cerrar', '关闭'), 'None Recorded': ('Ninguno Registrado', '暂无记录'), 'Omote': ('Omote', '表'), 'Ura': ('Ura', '裏'),
 '5th kyu': ('5.º kyu', '5级'), '4th kyu': ('4.º kyu', '4级'), '3rd kyu': ('3.º kyu', '3级'), '2nd kyu': ('2.º kyu', '2级'), '1st kyu': ('1.º kyu', '1级'),
 'Shodan': ('Shodan', '初段'), 'Nidan': ('Nidan', '二段'), 'Sandan': ('Sandan', '三段'),
}
XL = {'es': {}, 'zh': {}}
for k, v in HDR.items():
    for l in ('es', 'zh'): XL[l][k] = v[l]
for k, (e, z) in TECHD.items(): XL['es'][k] = e; XL['zh'][k] = z
XLR = {  # [regex, es, zh] for dynamic strings
 'es': [[r'^(\d+) waza match\. Keep choosing to reach one\.$', r'\1 waza coinciden. Sigue eligiendo para llegar a uno.'], [r'^Introduced at (.+)$', r'Introducido en \1']],
 'zh': [[r'^(\d+) waza match\. Keep choosing to reach one\.$', r'\1 个技法匹配。继续选择以缩小范围。'], [r'^Introduced at (.+)$', r'首次出现于 \1']],
}

TECH_JS = '''
(function () {
  var root = document.documentElement, XL = %s, XR = %s, lang = 'en', orig = new WeakMap();
  function tr(s) {
    var t = s.trim(); if (!t || lang === 'en') return null;
    var d = XL[lang][t]; if (d) return s.replace(t, d);
    var rr = XR[lang];
    for (var i = 0; i < rr.length; i++) { var re = new RegExp(rr[i][0]); if (re.test(t)) return s.replace(t, t.replace(re, rr[i][1])); }
    return null;
  }
  function xl(el) {
    if (!el) return;
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n, list = [];
    while ((n = w.nextNode())) list.push(n);
    list.forEach(function (n) {
      if (!orig.has(n)) orig.set(n, n.nodeValue);
      var o = orig.get(n), t = tr(o);
      if (lang === 'en') { if (n.nodeValue !== o) n.nodeValue = o; } else if (t !== null) n.nodeValue = t; else if (n.nodeValue !== o && !/^\\s*$/.test(o)) { /* keep dynamic text */ }
    });
    [].forEach.call(el.querySelectorAll('[aria-label]'), function (e) {
      var k = '@aria-label:' + (e.getAttribute('data-al') || e.getAttribute('aria-label'));
      if (!e.getAttribute('data-al')) e.setAttribute('data-al', e.getAttribute('aria-label'));
      var d = XL[lang] && XL[lang][k]; e.setAttribute('aria-label', lang === 'en' || !d ? e.getAttribute('data-al') : d);
    });
  }
  window.__xl = function (el) { if (lang !== 'en') xl(el); };
  function setLang(l) {
    lang = l; root.lang = l === 'zh' ? 'zh-Hans' : l;
    xl(document.querySelector('.sh')); xl(document.querySelector('.ft'));
    if (window.__render) window.__render();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.ll button[data-lang]');
    if (b) setLang(b.getAttribute('data-lang'));
  });
  /* theme */
  function eff() { var t = root.getAttribute('data-site') || root.getAttribute('data-theme'); if (t) return t; return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'; }
  try { var saved = localStorage.getItem('site-theme'); if (saved === 'light' || saved === 'dark') root.setAttribute('data-site', saved); } catch (x) {}
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('[data-tg]')) return;
    var t = eff() === 'light' ? 'dark' : 'light'; root.setAttribute('data-site', t);
    try { localStorage.setItem('site-theme', t); } catch (x) {}
  });
  document.addEventListener('click', function (e) { var d = e.target.closest && e.target.closest('[data-dead]'); if (d) e.preventDefault(); });
})();
''' % (json.dumps(XL, ensure_ascii=False), json.dumps(XLR, ensure_ascii=False))

def markup(mobile):
    ah = B.chrome_ah(mobile)
    home = REV16['mobile' if mobile else 'desktop']
    ah = re.sub(r'<a class="lk arl"[^>]*>.*?</a>', '<a class="lk arl ttl" href="%s" target="_blank" rel="noopener"><span>Brooklyn Aikikai</span> <span>Technique Database</span></a>' % home, ah, flags=re.S)
    foot = B.FOOT
    return (f'<div class="app"><div class="sh" id="sh">{ah}</div>'
            f'<nav class="crumbs" id="crumbs" aria-label="Breadcrumb"></nav><div id="view"></div>{foot}</div>')

def build(mobile):
    title = 'Technique Database v14 ' + ('Mobile' if mobile else 'Desktop')
    css = css16(mobile)
    appcss = APP_CSS
    page_css = appcss + THEME + css
    if mobile: page_css = page_css.replace('@media (max-width:900px){', '@media all{')
    html_ = (f'<meta charset="utf-8">\n<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
             f'<style>\n{page_css}\n</style>\n{markup(mobile)}\n<script>\n{app_js()}\n</script>\n<script>\n{DEMO_JS}\n</script>\n<script>\n{LANGJS}\n{TECH_JS}\n</script>\n')
    return B.finish(html_)

if __name__ == '__main__':
    for m in (False, True):
        n = 'tech-%s.html' % ('mobile' if m else 'desktop'); open(n, 'w').write(build(m)); print(n, os.path.getsize(n))
