"""rev17 Rail, rev18 Pigment, rev19 Index: three builds on the rev16 content and shell."""
import re, html, io, contextlib, os, sys, json as _json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build_all as BA
B, E, R, TD, BL, TCm = BA.B, BA.E, BA.R, BA.TD, BA.BL, BA.TCm

VAR = {'A': dict(rev=17, name='Rail'), 'B': dict(rev=18, name='Pigment'), 'C': dict(rev=19, name='Index')}
FONTS = {
    'A': 'family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500',
    'B': 'family=Zen+Kaku+Gothic+New:wght@300;400;500',
    'C': 'family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500',
}
EXTRA_I18N = {
    'Read Full Story': {'es': 'Leer la historia completa', 'zh': '阅读全文'},
    'Upcoming': {'es': 'Próximamente', 'zh': '即将举行'},
    'Latest': {'es': 'Lo más reciente', 'zh': '最新'},
    'Today': {'es': 'Hoy', 'zh': '今天'},
    'Tomorrow': {'es': 'Mañana', 'zh': '明天'},
}

# ---------- motion: every duration and easing in the page becomes one of the direction's tokens
TIME = re.compile(r'(?<![\w.-])(\d*\.?\d+)s\b')
EASE = re.compile(r'\b(?:ease-in-out|ease-in|ease-out|ease)\b|cubic-bezier\([^)]*\)')
def _tok(m):
    v = float(m.group(1))
    if v > 2: return m.group(0)
    return 'var(--t-fast)' if v <= .25 else 'var(--t-base)' if v <= .35 else 'var(--t-move)'
def norm_motion(css):
    def decl(m):
        prop, val = m.group(1), m.group(2)
        if 'prog' in val and '14s' in val: return m.group(0)
        return prop + ':' + EASE.sub('var(--ease)', TIME.sub(_tok, val))
    return re.sub(r'(?<![\w-])((?:transition|animation)(?:-duration|-timing-function)?)\s*:\s*([^;{}]+)', decl, css)

# ---------- css
def sys2():
    s = open('system2.css').read()
    s = re.sub(r'\.hr\[data-img="ar"\]\{--himg:url\(data:image/jpeg;base64,[A-Za-z0-9+/=]+\)[^}]*\}', '', s)
    s = re.sub(r'@media \(max-width:900px\)\{\.hr\[data-img="ar"\]\{[^}]*\}\}', '', s)
    s = re.sub(r'\.hr\[data-img="join"\]\{--jimg:url\(data:image/jpeg;base64,[A-Za-z0-9+/=]+\)[^}]*\}', '', s)
    return s
S2 = sys2()

def css_for(var, mobile):
    tail = S2 + open('heroes2.css').read() + BA.HOMECSS + BA.GLOSS + open(f'dir{var}.css').read() + BA.FULLH
    if mobile:
        css = (B.CSS + open('ext.css').read() + open('mobile.css').read() + open('sched.css').read() + open('sched-m.css').read()
               + open('events.css').read() + open('events-m.css').read() + open('rev16.css').read() + open('rev16-m.css').read()
               + open('join.css').read() + open('join-m.css').read() + BA.FIX + B.SYS(True) + tail)
    else:
        narrow = (open('mobile.css').read() + open('sched-m.css').read() + open('events-m.css').read() + open('rev16-m.css').read() + open('join-m.css').read()
                  + '.wkd{display:none}.wkm{display:block}')
        css = (B.CSS + open('ext.css').read() + open('desktop.css').read() + open('sheet.css').read()
               + open('sched.css').read() + open('sched-d.css').read() + open('events.css').read() + open('events-d.css').read()
               + open('rev16.css').read() + open('rev16-d.css').read() + open('join.css').read() + '.wkm{display:none}\n'
               + '@media (max-width:900px){\n' + narrow + '\n}\n' + BA.FIX + B.SYS(False) + tail)
    return norm_motion(css)

# ---------- home content
def short_date(m):
    d1, mo1, n1, d2, mo2, n2, _ = m.groups()
    if d2 is None: return f'{mo1} {n1}'
    return f'{mo1} {n1}–{n2}' if mo1 == mo2 else f'{mo1} {n1} – {mo2} {n2}'

def upcoming(n=5):
    out = []
    for title, blocks in E.years.items():
        y = int(re.search(r'20\d\d', title).group(0))
        for mo in E.MONTHS:
            for t in blocks.get(mo, []):
                m = E.DATE.match(t)
                if not m: continue
                dt = datetime.date(y, E.MONTHS.index(m.group(2)) + 1, int(m.group(3)))
                if dt >= E.TODAY: out.append((dt, m))
    out.sort(key=lambda x: x[0])
    return out[:n]

def rel(dt):
    d = (dt - E.TODAY).days
    if d == 0: return 'Today'
    if d == 1: return 'Tomorrow'
    if d < 14: return f'In {d} days'
    if d < 60: return f'In {d // 7} weeks'
    return f'In {d // 30} months'

def blog_cards():
    return ''.join(
        f'<a class="bc" href="#{BL.key(p)}" data-go="{BL.key(p)}"><figure class="ph" style="aspect-ratio:3/2"></figure>'
        f'<time datetime="{p["date"][:10]}">{BL.when(p)}</time><h3>{html.escape(BL.title(p))}</h3>'
        f'{("<span class=\"au\">" + html.escape(BL.author(p)) + "</span>") if BL.author(p) else ""}<p>{html.escape(BL.summary(p))}</p></a>' for p in BL.LIVE)

def home_A():
    ev = (f'<button type="button" class="story" data-drawer="reg"><img class="poster" src="{E.POSTER}" alt="Poster: {html.escape(E.NAME)}, {html.escape(E.DATES)}" width="648" height="1000">'
          f'<div><p class="when">{html.escape(E.DATES)}</p><h3>{html.escape(E.NAME)}</h3><p>At Brooklyn Aikikai</p><span class="go">Read Full Story<i></i></span></div></button>')
    posts = ''.join(
        f'<a class="story" href="#{BL.key(p)}" data-go="{BL.key(p)}"><figure class="ph"></figure><div><p class="when">{BL.when(p)}</p>'
        f'<h3>{html.escape(BL.title(p))}</h3><p>{html.escape(BL.summary(p))}</p><span class="go">Read Full Story<i></i></span></div></a>' for p in BL.LIVE)
    return f'<div class="hm">{ev}{posts}</div>'

TILES = [('about', 'About', '--im-mission', ''), ('schedule', 'Schedule', '--im-classes', ''), ('join', 'Join', '--im-join', ''),
         ('kids', "Kids' Aikido", None, '#8E3B2B'), ('members', 'Dojo Members', None, '#3A4452')]
def home_B():
    t = ''
    for sec, label, im, col in TILES:
        go = BA.GO[sec]
        style = f'background-image:var({im})' if im else f'--p:{col}'
        t += f'<a class="tile" href="#{go}" data-go="{go}"><div class="im" style="{style}"></div><h3>{html.escape(label)}</h3><span class="go" aria-hidden="true"><i></i></span></a>'
    return f'<div class="tiles">{t}</div>'

def home_C():
    rows = ''
    for dt, m in upcoming(5):
        rest = re.sub(r'\[([^\]]*?)\]\([^)]+\)', r'\1', m.group(7)).strip().rstrip('.')
        cat, loc = E.classify(m.group(7))
        label = {'aikido': 'Aikido', 'zen': 'Zen', 'misogi': 'Misogi'}.get(cat, 'Event')
        rows += (f'<li><a href="#events" data-go="events"><span class="when">{rel(dt)}<br>{short_date(m)}</span>'
                 f'<span><span class="cat">{label}</span><span class="nm">{html.escape(rest[:1].upper() + rest[1:])}</span></span></a></li>')
    return (f'<div class="ix"><div class="sc-lab"><i></i><b>Upcoming</b></div><ul class="up">{rows}</ul></div>'
            f'<div class="ix"><div class="sc-lab"><i></i><b>Latest</b></div><div class="bl">{blog_cards()}</div></div>')

_body = BA.body
def make_body(var):
    home = {'A': home_A, 'B': home_B, 'C': home_C}[var]
    return lambda key, mobile: home() if key == 'home' else _body(key, mobile)

# ---------- header pieces
LANG = re.compile(r'<div class="lang">.*?</ul></div>', re.S)
TG = re.compile(r'<button type="button" class="tg".*?</button>', re.S)
def nav_html(var, mobile):
    if var == 'C':
        logo = '<a class="logo" href="#home" data-go="home">Brooklyn Aikikai</a>'
        ah = B.chrome_ah(mobile)
        cl = f'<div class="cl">{LANG.search(ah).group(0)}{TG.search(ah).group(0)}</div>'
        if mobile: return f'<div class="nv">{logo}{cl}{BA.BURGER}</div>'
        links = ''.join(f'<a class="nl{" on" if sec == BA.FIRST[2] else ""}" data-sec="{sec}" href="#{BA.GO[sec]}" data-go="{BA.GO[sec]}">{n}</a>' for n, sec in BA.NAVITEMS)
        return (f'<div class="nv">{logo}<nav aria-label="Primary">{links}<a class="don" data-sec="donate" href="#donate" data-go="donate">Donate</a></nav>{cl}{BA.BURGER}</div>')
    nv = BA.nav(mobile)
    if var == 'A' and not mobile:
        rail = ''.join(BA.subnav(g).replace('class="sub"', 'class="sub rs"', 1) for g in BA.GROUPS)
        nv = nv.replace('</nav>', '</nav>' + rail, 1)
    return nv

def hero_html(var, mobile):
    first = BA.FIRST
    vid = f'<video class="hv" muted loop playsinline aria-hidden="true" src="{R.VIDEO}"></video>'
    home_vid = f'<video class="hv hvh" muted loop playsinline aria-hidden="true" poster="{BA.HOMEPOSTER}" src="{BA.HOMEVID}"></video>'
    sl = ''
    if var == 'C':
        home_vid = ''
        pos = ('40% 65%', 'center', '50% 30%', '50% 40%')
        ims = ('--im-mission', '--hposter', '--im-join', '--im-uchideshi')
        g = 'linear-gradient(to bottom,rgba(10,12,16,.55) 0,rgba(10,12,16,0) 140px),linear-gradient(to top,rgba(10,12,16,.8) 0,rgba(10,12,16,.25) 55%,rgba(10,12,16,.1) 100%)'
        words = ('Aikido', 'Iaido', 'Zen', 'Misogi')
        slides = ''.join(f'<a class="sl-s{" on" if i == 0 else ""}" href="#curriculum" data-go="curriculum" data-sec="{w}"><i class="bg" style="background-image:{g},var({ims[i]});background-position:{pos[i]}"></i><span>{w}</span></a>' for i, w in enumerate(words))
        sl = f'<div class="sl" role="group" aria-roledescription="carousel" aria-label="Practices">{slides}<div class="sl-c"><i class="on"></i><i></i><i></i><i></i><button type="button">Pause</button></div></div>'
    return (f'<header class="hr" data-hero="{first[4]}">{vid}{home_vid}{sl}<i class="shade"></i><i class="hp"></i>'
            f'{nav_html(var, mobile)}<div class="hh"><span class="ey hero">Brooklyn Aikikai</span><h1>{html.escape(first[1])}</h1><p class="au"></p></div><span class="pl">Hero image placeholder</span></header>')

def mega():
    out = '<div id="mega">'
    for g, (label, items, dead) in BA.GROUPS.items():
        lis = ''.join(f'<li><a href="#{k}" data-go="{k}" data-p="{k}">{l}</a></li>' for k, l in items)
        out += f'<div class="mg" data-g="{g}"><ul>{lis}</ul><div class="mth" data-p="{items[0][0]}" aria-hidden="true"></div></div>'
    return out + '</div>'

def foot(var):
    f = B.FOOT
    if var == 'C':
        f = f.replace('<nav aria-label="Footer">', '<nav aria-label="Footer"><a class="lk" href="#anti-racism" data-go="anti-racism">Our Commitment to Anti-Racism</a>', 1)
    return f

def i18n():
    js = open('i18n.js').read()
    a = js.index('var D=') + 6; b = js.index('\nvar orig')
    D = _json.loads(js[a:b])
    for k in list(D):
        if not k.startswith('@'): D.setdefault(TCm.tc(k), D[k])
    D.update(EXTRA_I18N)
    return js[:a] + _json.dumps(D, ensure_ascii=False) + js[b:]
I18N = i18n()

def js_for(var, mobile):
    j = B.JS
    ex = open('extras.js').read()
    if var == 'A':
        j = j.replace("sub = document.querySelector('.sub:not([hidden])')", "sub = document.querySelector('.mn .sub:not([hidden])')")
        j = j.replace("var off = (document.querySelector('.ah').offsetHeight)", "var off = (window.innerWidth > 900 ? 0 : document.querySelector('.ah').offsetHeight)")
        ex = ex.replace("document.querySelector('.sub:not([hidden])')", "document.querySelector('.mn .sub:not([hidden])')").replace("(ah ? ah.offsetHeight : 0)", "(ah && window.innerWidth <= 900 ? ah.offsetHeight : 0)")
    ext = open(f'ext{var}.js').read() if os.path.exists(f'ext{var}.js') else ''
    return (j + '\n' + open('sched.scoped.js').read() + '\n' + open('events.scoped.js').read() + '\n' + I18N + '\n' + ex + '\n' + ext
            + "\n(function(){[].forEach.call(document.querySelectorAll('form'),function(f){f.addEventListener('submit',function(e){e.preventDefault();});});})();")

def build(var, mobile):
    V = VAR[var]
    BA.body = make_body(var)
    title = f'Brooklyn Aikikai Website rev{V["rev"]} {V["name"]} ' + ('Mobile' if mobile else 'Desktop')
    css = css_for(var, mobile)
    ah = '<div class="ah" hidden></div>' if var == 'C' else B.chrome_ah(mobile)
    subs = ''.join(BA.subnav(g) for g in BA.GROUPS)
    anc = ''
    if var == 'B':
        subs = ''
        anc = '<nav class="sub anc" aria-label="On This Page" hidden><div class="sj"></div></nav>'
    pages = ''.join(BA.page(mobile, *p_) for p_ in BA.PAGES)
    main = f'<main class="mn{" has-sub" if var != "B" else ""}">{anc}{subs}{pages}</main>'
    extra = mega() if (var == 'B' and not mobile) or var == 'B' else ''
    out = (f'<meta charset="utf-8">\n<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[var]}&display=swap">\n'
           f'<style>\n{css}\n</style>\n<div class="site">{ah}{hero_html(var, mobile)}{main}{foot(var)}</div>\n{extra}{BA.sheet()}\n{TD.card()}\n{E.drawer()}\n<script>\n{js_for(var, mobile)}\n</script>\n')
    out = BA._tc_html(out)
    if var == 'A':
        out = re.sub(r'(<a class="bc"[^>]*>.*?)(</a>)', lambda m: m.group(1) + '<span class="go">Read Full Story<i></i></span>' + m.group(2), out, flags=re.S)
    return B.finish(out)

if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for v in which:
        for mobile in (False, True):
            name = f'dir{v}-{"mobile" if mobile else "desktop"}.html'
            open(name, 'w').write(build(v, mobile)); print(name, os.path.getsize(name))
