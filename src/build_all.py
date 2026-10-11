import html, io, contextlib, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
    import build_sched as S
    import build_events as E
    import build_rev16 as R
    import build_join as J
    import build_tend as TD
    import build_blog as BL
    import build_ar as AR
import tc as TCm
import revsel as REV
import json as _json

# key, hero title, nav section, jump-nav group, hero kind
PAGES = [
 ('home', 'Aikido, Iaido, Zen, Misogi', '', '', 'home'),
 ('mission', 'Our Mission', 'about', 'about', 'plain'), ('curriculum', 'Curriculum', 'about', 'about', 'plain'),
 ('instructors', 'Instructors', 'about', 'about', 'plain'), ('history', 'History', 'about', 'about', 'plain'),
 ('anti-racism', AR.TITLE, 'about', 'about', 'feature'),
 ('tendokan', 'Origins and History of Tendokan Dojo', 'about', 'about', 'feature'),
 ('blog', 'Blog', 'about', 'about', 'plain'),
] + [(BL.key(p), BL.title(p), 'about', 'about', 'feature') for p in BL.LIVE] + [
 ('classes', 'Schedule', 'schedule', 'schedule', 'plain'), ('events', 'Events', 'schedule', 'schedule', 'plain'),
 ('join', 'Becoming a member', 'join', 'join', 'plain'), ('testimonials', 'Member Testimonials', 'join', 'join', 'plain'),
 ('etiquette', 'Etiquette', 'join', 'join', 'plain'), ('glossary', 'Glossary', 'join', 'join', 'plain'), ('uchideshi', 'Uchideshi program', 'join', 'join', 'plain'),
 ('kids', "Kids' Aikido", 'kids', '', 'video'), ('members', 'Dojo Members', 'members', '', 'plain'), ('donate', '25 Years', 'donate', '', 'donate'),
]
GROUPS = {
 'about': ('About', [('mission', 'Our Mission'), ('curriculum', 'Curriculum'), ('instructors', 'Instructors'), ('history', 'History'), ('tendokan', 'Tendokan Dojo'), ('anti-racism', 'Anti-racism/DEI'), ('blog', 'Blog')], ['Policies']),
 'schedule': ('Schedule', [('classes', 'Classes'), ('events', 'Events')], []),
 'join': ('Join', [('join', 'Becoming a member'), ('testimonials', 'Member Testimonials'), ('etiquette', 'Etiquette'), ('glossary', 'Glossary'), ('uchideshi', 'Uchideshi program')], []),
}
GO = {'about': 'mission', 'schedule': 'classes', 'join': 'join', 'kids': 'kids', 'members': 'members', 'donate': 'donate'}
NAVITEMS = [('About', 'about'), ('Schedule', 'schedule'), ('Join', 'join'), ("Kids' Aikido", 'kids'), ('Dojo Members', 'members')]
BURGER = '<button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button>'
PAGES = [(k, TCm.tc(t) if k != 'home' else t, *rest) for k, t, *rest in PAGES]
GROUPS = {g: (TCm.tc(a), [(k, TCm.tc(l)) for k, l in items], [TCm.tc(x) for x in dead]) for g, (a, items, dead) in GROUPS.items()}
FIRST = PAGES[0]
HOME_H1 = ('<a class="w" href="#curriculum" data-go="curriculum" data-sec="Aikido">Aikido</a>, <a class="w" href="#curriculum" data-go="curriculum" data-sec="Iaido">Iaido</a>,<br>'
           '<a class="w" href="#curriculum" data-go="curriculum" data-sec="Zen">Zen</a>, <a class="w" href="#curriculum" data-go="curriculum" data-sec="Misogi">Misogi</a>')
import base64 as _b
HOMEVID = 'data:video/mp4;base64,' + _b.b64encode(open('homevid.mp4', 'rb').read()).decode()
HOMEPOSTER = 'data:image/jpeg;base64,' + _b.b64encode(open('rev12poster.jpg', 'rb').read()).decode()
SEC_FIRST = 'mission'

def nav(mobile):
    logo = '<a class="logo" href="#home" data-go="home">Brooklyn Aikikai</a>'
    if mobile: return f'<div class="nv">{logo}{BURGER}</div>'
    links = ''.join(f'<a class="nl{" on" if sec == FIRST[2] else ""}" data-sec="{sec}" href="#{GO[sec]}" data-go="{GO[sec]}">{n}</a>' for n, sec in NAVITEMS)
    return f'<div class="nv">{logo}<nav aria-label="Primary">{links}<a class="don" data-sec="donate" href="#donate" data-go="donate">Donate</a></nav>{BURGER}</div>'

def subnav(group):
    label, items, dead = GROUPS[group]
    links = ''.join(f'<a class="lk{" on" if k == FIRST[0] else ""}" href="#{k}" data-go="{k}"{" aria-current=page" if k == FIRST[0] else ""}>{l}</a>' for k, l in items)
    links += ''.join(f'<span class="lk dead" aria-disabled="true">{l}</span>' for l in dead)
    return f'<nav class="sub" data-group="{group}" aria-label="{label}"{"" if group == FIRST[3] else " hidden"}><div class="sj">{links}</div></nav>'

def body(key, mobile):
    if key == 'mission': return B.mission()
    if key == 'curriculum': return B.curriculum()
    if key == 'instructors': return B.instructors()
    if key == 'history': return B.history()
    if key == 'home': return ''
    if key == 'anti-racism': return AR.build()
    if key == 'tendokan': return TD.build()
    if key == 'blog': return BL.index()
    if key.startswith('post-'): return BL.post(next(p for p in BL.LIVE if BL.key(p) == key))
    if key == 'classes':
        views = S.weeklist() if mobile else f'<div class="wkd">{S.grid()}</div><div class="wkm">{S.weeklist()}</div>'
        return S.notes() + f'<section class="wkwrap">{S.chips(mobile)}{views}</section>'
    if key == 'events':
        secs = E.featured(mobile) + E.filters()
        yrs = {'2027 Events': {}}; yrs.update({k: v for k, v in E.years.items() if '2027' not in k})
        for title, blocks in sorted(yrs.items(), reverse=True): secs += E.year_section(title, blocks)
        return secs + E.past_section() + E.bna()
    if key == 'join': return J.join()
    if key == 'testimonials': return J.testimonials()
    if key == 'etiquette': return J.etiquette()
    if key == 'glossary': return J.glossary()
    if key == 'uchideshi': return J.uchideshi()
    if key == 'kids': return R.kids()
    if key == 'members': return R.members()
    if key == 'donate': return R.donate()

def page(mobile, key, title, section, group, hero):
    return (f'<section class="pg" data-page="{key}" data-title="{html.escape(title)}" data-section="{section}" data-group="{group}" data-hero="{hero}"{' data-nav="blog"' if key.startswith('post-') else ''}{' data-img="ar"' if key == 'anti-racism' else (' data-img="' + key + '"' if key in ('join', 'mission', 'uchideshi', 'classes') else '')}{(' data-h1html="' + html.escape(HOME_H1, quote=True) + '"') if key == 'home' else ''}{(' data-author="' + html.escape(BL.author(next(p for p in BL.LIVE if BL.key(p) == key))) + '"') if key.startswith('post-') else ''}'
            f'{"" if key == FIRST[0] else " hidden"}>{body(key, mobile)}</section>')

def sheet():
    s = B.SHEET.replace('class="slogo" href="#mission" data-go="mission"', 'class="slogo" href="#home" data-go="home"')
    s = s.replace('<a class="si" href="#mission" data-go=mission style="--i:0">', '<a class="si" href="#mission" data-go="mission" style="--i:0">')
    for i, k in ((1, 'classes'), (2, 'join'), (3, 'kids'), (4, 'members')):
        s = s.replace(f'<a class="si" href="#" data-dead style="--i:{i}">', f'<a class="si" href="#{k}" data-go="{k}" style="--i:{i}">')
    s = s.replace('<a class="sdon" href="#" data-dead', '<a class="sdon" href="#donate" data-go="donate"')
    return s

FIX = '''/* merged document: each page keeps its own spacing */
[data-page="classes"] .wkwrap{padding-top:0}
[data-page="members"] .wkwrap{padding-top:0}
'''

HOMECSS = f':root{{--hposter:url({HOMEPOSTER})}}\n'

def _tc_html(h):
    t = TCm.tc
    def inner(m):
        a, body, z = m.group(1), m.group(2), m.group(3)
        if '<' in body: return m.group(0)
        return a + html.escape(t(html.unescape(body)), quote=False) + z
    h = re.sub(r'(<h[23][^>]*>)([^<]*)(</h[23]>)', inner, h)
    h = re.sub(r'(<a class="lk[^"]*"[^>]*data-go[^>]*>)([^<]*)(</a>)', inner, h)
    h = re.sub(r'(<button[^>]*class="chip[^"]*"[^>]*>)([^<]*)(</button>)', inner, h)
    h = re.sub(r'(<(?:a|button)[^>]*class="cb[^"]*"[^>]*>)([^<]*)(</(?:a|button)>)', inner, h)
    h = re.sub(r'<dl class="du">.*?</dl>', lambda m: re.sub(r'(<dt>)([^<]*)(</dt>)', inner, m.group(0)), h, flags=re.S)
    return h

def _i18n():
    js = open('i18n.js').read()
    a = js.index('var D=') + 6; b = js.index('\nvar orig')
    D = _json.loads(js[a:b])
    for k in list(D):
        if not k.startswith('@'):
            D.setdefault(TCm.tc(k), D[k])
    return js[:a] + _json.dumps(D, ensure_ascii=False) + js[b:]

def build(mobile):
    title = 'Brooklyn Aikikai Website rev16 ' + ('Mobile' if mobile else 'Desktop')
    if mobile:
        css = (B.CSS + open('ext.css').read() + open('mobile.css').read() + open('sched.css').read() + open('sched-m.css').read()
               + open('events.css').read() + open('events-m.css').read() + open('rev16.css').read() + open('rev16-m.css').read()
               + open('join.css').read() + open('join-m.css').read() + FIX + B.SYS(True) + open('system2.css').read() + open('heroes.css').read() + HOMECSS)
    else:
        narrow = (open('mobile.css').read() + open('sched-m.css').read() + open('events-m.css').read() + open('rev16-m.css').read() + open('join-m.css').read()
                  + '.wkd{display:none}.wkm{display:block}')
        css = (B.CSS + open('ext.css').read() + open('desktop.css').read() + open('sheet.css').read()
               + open('sched.css').read() + open('sched-d.css').read() + open('events.css').read() + open('events-d.css').read()
               + open('rev16.css').read() + open('rev16-d.css').read() + open('join.css').read() + '.wkm{display:none}\n'
               + '@media (max-width:900px){\n' + narrow + '\n}\n' + FIX + B.SYS(False) + open('system2.css').read() + open('heroes.css').read() + HOMECSS)
    first = FIRST
    hero = (f'<header class="hr" data-hero="{first[4]}"><video class="hv" muted loop playsinline aria-hidden="true" src="{R.VIDEO}"></video><video class="hv hvh" muted loop playsinline aria-hidden="true" poster="{HOMEPOSTER}" src="{HOMEVID}"></video><i class="shade"></i><i class="hp"></i>'
            f'{nav(mobile)}<div class="hh"><span class="ey hero">Brooklyn Aikikai</span><h1>{html.escape(first[1])}</h1><p class="au"></p></div><span class="pl">Hero image placeholder</span></header>')
    subs = ''.join(subnav(g) for g in GROUPS)
    pages = ''.join(page(mobile, *p_) for p_ in PAGES)
    main = f'<main class="mn has-sub">{subs}{pages}</main>'
    js = (B.JS + '\n' + open('sched.scoped.js').read() + '\n' + open('events.scoped.js').read() + '\n' + _i18n() + '\n' + open('extras.js').read()
          + "\n(function(){[].forEach.call(document.querySelectorAll('form'),function(f){f.addEventListener('submit',function(e){e.preventDefault();});});})();")
    out = (f'<meta charset="utf-8">\n<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
           f'<style>\n{css}\n</style>\n<div class="site">{B.chrome_ah(mobile)}{hero}{main}{B.FOOT}</div>\n{sheet()}\n{TD.card()}\n{E.drawer()}\n<script>\n{js}\n</script>\n{REV.block(mobile, 'rev16')}')
    return B.finish(_tc_html(out))

if __name__ == '__main__':
    open('all-desktop.html', 'w').write(build(False))
    open('all-mobile.html', 'w').write(build(True))
    print('ok')
