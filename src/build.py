import json, re, html, sys
D = json.load(open('web.json'))
pages = {p['id']: p for p in D['pages']}
people = D['people']

def esc(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a class="lk" href="\2" target="_blank" rel="noopener">\1</a>', t)

def para(t, cls=''):
    if t[:1] in ('"', '\u201c'): cls = (cls + ' hq').strip()
    attr = f' class="{cls}"' if cls else ''
    return f'<p{attr}>{esc(t)}</p>'

PLAY = '<svg class="play" width="56" height="56" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="27" fill="none" stroke="currentColor" stroke-width="2"/><path d="M23 18l15 10-15 10z" fill="currentColor"/></svg>'

def ph(label, ratio='16/9', video=False):
    if video:
        return f'<figure class="ph vid" style="aspect-ratio:{ratio}">{PLAY}<span class="bar" aria-hidden="true"><i></i></span><figcaption>{html.escape(label)}</figcaption></figure>'
    return f'<figure class="ph" style="aspect-ratio:{ratio}"><figcaption>{html.escape(label)}</figcaption></figure>'

def photo(name, alt, ratio, cls=''):
    import base64
    src = 'data:image/jpeg;base64,' + base64.b64encode(open('img/' + name, 'rb').read()).decode()
    return f'<figure class="ph pimg{(" " + cls) if cls else ""}" style="aspect-ratio:{ratio}"><img src="{src}" alt="{html.escape(alt)}" loading="lazy"></figure>'

def curly(t):
    out=[];o=True
    for ch in t:
        if ch=='"': out.append('\u201c' if o else '\u201d'); o=not o
        else: out.append(ch)
    return ''.join(out)

def quote(text, cite='', sm=False):
    text = curly(text)
    c = f'<cite>{esc(cite)}</cite>' if cite else ''
    return f'<blockquote class="q{" sm" if sm else ""}"><p class="hq">{esc(text)}</p>{c}</blockquote>'

def rows(pairs):
    return '<dl class="du">' + ''.join(f'<div><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in pairs) + '</dl>'

def sec(label, body, sub=''):
    s = f'<p class="by">{esc(sub)}</p>' if sub else ''
    return f'<section class="sec"><div class="lab"><h2>{html.escape(label)}</h2>{s}</div><div class="bd">{body}</div></section>'

KANA = ['い', 'ろ', 'は', 'に', 'ほ', 'へ']

# ---------- page bodies ----------
def mission():
    items = pages['seed-page-mission-vision']['body']
    out = []; cur = None; blocks = {}
    for it in items:
        if it['type'] == 'h2': cur = it['text']; blocks[cur] = []
        else: blocks[cur].append(it)
    m = blocks['Our Mission']
    ps = [i for i in m if i['type'] == 'p']
    lis = [i for i in m if i['type'] == 'li']
    lead = ps[0]['text']
    intro = ps[1]['text']
    rest = ps[2:]
    steps = '<ol class="stp">' + ''.join(f'<li><span class="dash" aria-hidden="true"></span><span>{esc(l["text"])}</span></li>' for i, l in enumerate(lis)) + '</ol>'
    ctas = [r for r in rest if r['text'].startswith('[aikido for')]
    prose = [r for r in rest if not r['text'].startswith('[aikido for')]
    nd = [r for r in prose if r['text'].startswith('Brooklyn Aikikai does not discriminate')]
    prose = [r for r in prose if r not in nd]
    mb = f'<p class="ld">{esc(lead)}</p>' + para(intro) + steps + ''.join(para(r['text']) for r in prose)
    mb += '<div class="cta">' + ''.join(f'<a class="cb" href="#" data-dead>{html.escape(re.sub(r"[\[\]]|\(.*\)", "", r["text"]).strip().capitalize())}</a>' for r in ctas) + '</div>'
    mb += ''.join(para(r['text'], 'fine') for r in nd)
    v = blocks['Our Vision']
    return sec('Our Mission', mb) + sec('Our Vision', ''.join(para(i['text']) for i in v if i['type'] == 'p'))

FACTS = {
 'Aikido': None,
 'Weapons': [('Begin after', 'Six months of training'), ('Permission', 'The chief instructor'), ('Equipment', 'Your own set, about $180')],
 'Iaido': [('Permission', 'The chief instructor'), ('Equipment', 'Extra equipment, bought by the student')],
 'Zen': [('Sessions', 'Several each week'), ('Open to', 'All students')],
 'Misogi': [('Sessions', 'Several times a week'), ('Permission', 'The chief instructor')],
}
def curriculum():
    items = pages['seed-page-classes']['content']
    groups = []; cur = None
    for it in items:
        if it['type'] == 'h2': cur = {'h': it['text'], 'items': []}; groups.append(cur)
        else: cur['items'].append(it)
    out = ''
    for g in groups:
        b = ''; q = ''
        for it in g['items']:
            if it['type'] == 'img':
                b += photo('koshi.jpg', it['alt'], '1960/1096') if it['alt'].startswith('A koshinage') else ph('Photo: ' + it['alt'], '16/9'); continue
            t = it['text']
            if g['h'] == 'Weapons' and t.startswith('"The sword'):
                b += quote(t, '', True); continue
            if g['h'] == 'Misogi' and t.startswith('"'):
                b += quote(t); continue
            if g['h'] == 'Misogi' and t.startswith('The above is an excerpt'):
                b += para(t, 'fine'); continue
            b += para(t)
        out += sec(g['h'], b)
    return out

def instructors():
    out = ''
    ranks = {
     'ryugan-savoca': [('Rank', 'Rokudan, 6th dan'), ('Title', 'Birankai North America Shihan'), ('Founded Brooklyn Aikikai', '2001')],
     'kate-savoca': [('Rank', 'Godan, 5th dan'), ('Began at Brooklyn Aikikai', '2002'), ('Certified by', 'Birankai North America')],
     'kaishin-kortney-bernard': [('Rank', 'Sandan, 3rd dan'), ('Certified', 'Fukushidoin, Birankai North America'), ('Also', 'Operations Manager')],
    }
    for p in people:
        bio = ''.join(para(i['text']) for i in p['bio'])
        body = ph('Video: ' + p['title'], '16/9', True) + bio
        lab = f'<div class="lab"><h2>{html.escape(p["title"])}</h2><p class="by">{html.escape(p["role"])}</p></div>'
        out += f'<section class="sec">{lab}<div class="bd">{body}</div></section>'
    return out

def history():
    items = pages['seed-page-history']['content']
    parts = []; cur = None
    for it in items:
        if it['type'] == 'h2': cur = {'h': it['text'], 'items': []}; parts.append(cur)
        else: cur['items'].append(it)
    dates = rows([
        ('Brooklyn Aikikai begins at the Albee School of Dance, Carroll Gardens', 'December 2001'),
        ('A mortgage on the old iron works building', 'May 2004'),
        ('First classes in the new dojo', 'November 2004'),
        ('Construction finished', 'March 2005'),
        ('Opening seminar with Chiba Sensei, over 100 on the mat', 'September 2005'),
    ])
    out = ''
    for pt in parts:
        b = ''; sub = ''
        imgs = [i for i in pt['items'] if i['type'] == 'img']
        txt = [i for i in pt['items'] if i['type'] != 'img']
        if pt['h'] == 'History of Aikido':
            b += ph('Photo: ' + imgs[0]['alt'], '4/3')
            for t in txt:
                m = re.search(r'^(.*?)\s*("The purpose of training,.*)$', t['text'])
                if m:
                    b += para(m.group(1)); b += quote(m.group(2))
                else: b += para(t['text'])
            out += sec('History of Aikido', b); continue
        continue  # the Tendokan essays live on their own page (build_tend.py)
        bylines = [t for t in txt if t['text'].startswith(('by ', 'from '))]
        body = [t for t in txt if t not in bylines]
        sub = ' · '.join(t['text'] for t in bylines)
        figs = [ph('Photo: ' + i['alt'], '16/9') for i in imgs] if pt['h'].endswith('Dojo') else []
        at = {round(len(body) * (k + 1) / (len(figs) + 1)): f for k, f in enumerate(figs)}
        for n, t in enumerate(body, 1):
            b += para(t['text'])
            if n in at: b += at[n]
        out += sec(pt['h'].replace('Tendokan Dojo- Part II', 'Tendokan Dojo, Part II'), b, sub)
    return out

PAGES = [
 ('mission', 'Our Mission', '', 'Our Mission', mission),
 ('curriculum', 'Curriculum', '', 'Curriculum', curriculum),
 ('instructors', 'Instructors', '', 'Instructors', instructors),
 ('history', 'History', '', 'History', history),
]
SUBNAV = [(k, lab) for k, _, _, lab, _ in PAGES]

def chrome_ah(mobile):
    sun = '<svg class="ic" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
    moon = '<svg class="ic moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/></svg>'
    tg = f'<button type="button" class="tg" data-tg aria-label="Toggle light and dark mode">{sun.replace("class=\"ic\"", "class=\"ic sun\"")}{moon}</button>'
    ar = '<a class="lk arl" href="#anti-racism" data-go="anti-racism">Our Commitment to Anti-Racism</a>'
    chev = '<svg class="chev" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5"/></svg>'
    lang = ('<div class="lang"><button type="button" class="lb" aria-haspopup="listbox" aria-expanded="false" aria-label="Language"><span class="lf">English</span><span class="ls" aria-hidden="true">EN</span>' + chev + '</button>'
            '<ul class="ll" role="listbox" hidden><li hidden><button type="button" role="option" data-lang="en" data-code="EN" aria-selected="true">English</button></li>'
            '<li><button type="button" role="option" data-lang="es" data-code="ES">Espa\u00f1ol</button></li><li><button type="button" role="option" data-lang="zh" data-code="\u4e2d\u6587">\u4e2d\u6587</button></li></ul></div>')
    return f'<div class="ah"><div class="th">{tg}</div>{ar}{lang}</div>'

NAV = [('About', True), ('Schedule', False), ('Join', False), ("Kids' Aikido", False), ('Dojo Members', False)]
def chrome_nav(mobile):
    if mobile:
        return '<div class="nv"><a class="logo" href="#mission" data-go="mission">Brooklyn Aikikai</a><button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button></div>'
    links = ''.join(f'<a class="nl{" on" if on else ""}" href="#{"mission" if on else ""}" {"data-go=mission" if on else "data-dead"}>{n}</a>' for n, on in NAV)
    return f'<div class="nv"><a class="logo" href="#mission" data-go="mission">Brooklyn Aikikai</a><nav aria-label="Primary">{links}<a class="don" href="#" data-dead>Donate</a></nav><button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button></div>'

def subnav(active):
    links = ''.join(f'<a class="lk{" on" if k == active else ""}" href="#{k}" data-go="{k}"{" aria-current=page" if k == active else ""}>{lab}</a>' for k, lab in SUBNAV)
    links += '<span class="lk dead" aria-disabled="true">Policies</span><span class="lk dead" aria-disabled="true">Blog</span>'
    return f'<nav class="sub" aria-label="About">{links}</nav>'

def subnav_join(active):
    items = (('join', 'Becoming a member'), ('testimonials', 'Member Testimonials'), ('etiquette', 'Etiquette/Glossary'), ('uchideshi', 'Uchideshi program'))
    links = ''.join(f'<a class="lk{" on" if k == active else ""}" href="#{k}" data-go="{k}"{" aria-current=page" if k == active else ""}>{lab}</a>' for k, lab in items)
    return f'<nav class="sub" aria-label="Join">{links}</nav>'

def article(mobile, key, title, subline, label, fn):
    return (f'<article class="pg" data-page="{key}"{"" if key == "mission" else " hidden"}>'
            f'{chrome_ah(mobile)}'
            f'<header class="hr">{chrome_nav(mobile)}<div class="hh"><h1>{html.escape(title)}</h1>{('<p>' + html.escape(subline) + '</p>') if subline else ''}</div><span class="pl">Hero image placeholder</span></header>'
            f'<main class="mn">{subnav(key)}{fn()}</main></article>')

FOOT = ('<footer class="ft"><nav aria-label="Footer"><a class="lk" href="#" data-dead>Contact</a><a class="lk" href="#" data-dead>Accessibility</a><a class="lk sc" href="#" data-dead>Site Credits</a>'
        '<a class="lk" href="https://www.instagram.com/baikikai/" target="_blank" rel="noopener">Instagram</a></nav>'
        '<div class="lg"><span>\u00a9 2026 Brooklyn Aikikai</span>'
        '<span>Brooklyn Aikikai is a 501(c)(3) <a class="lk" href="https://www.guidestar.org/profile/26-1693436" target="_blank" rel="noopener">EIN: 26-1693436</a></span></div></footer>')

SHEET = ('<div id="sheet" role="dialog" aria-modal="true" aria-label="Menu" hidden><div class="sbar"><a class="slogo" href="#mission" data-go="mission">Brooklyn Aikikai</a>'
         '<button type="button" class="mb sx" data-close aria-label="Close menu"><i></i><i></i></button></div><nav class="snav" aria-label="Menu">'
         + ''.join(f'<a class="si" href="#{"mission" if i == 0 else ""}" {"data-go=mission" if i == 0 else "data-dead"} style="--i:{i}"><span>{n}</span></a>' for i, (n, _) in enumerate(NAV))
         + '</nav><div class="sfoot"><a class="sdon" href="#" data-dead style="--i:5">Donate</a>'
         '<div class="slinks" style="--i:7"><a class="lk" href="#anti-racism" data-go="anti-racism">Our Commitment to Anti-Racism</a><a class="lk" href="#" data-dead>Contact</a><a class="lk" href="#" data-dead>Accessibility</a><a class="lk sc" href="#" data-dead>Site Credits</a><a class="lk" href="https://www.instagram.com/baikikai/" target="_blank" rel="noopener">Instagram</a></div></div></div>')

CSS = open('style.css').read()

def SYS(mobile):
    return open('system-m.css' if mobile else 'system-d.css').read() + open('system.css').read()

def finish(h):
    return re.sub(r'(<a [^>]*target="_blank"[^>]*>)([^<]+)(</a>)', r'\1\2<span class="sr"> (opens in a new tab)</span>\3', h)
JS = open('app.js').read()

def build(mobile):
    title = 'Brooklyn Aikikai Website rev13 ' + ('Mobile' if mobile else 'Desktop')
    arts = ''.join(article(mobile, *p) for p in PAGES)
    css = CSS + open('ext.css').read() + (open('mobile.css').read() if mobile else open('desktop.css').read() + open('sheet.css').read()) + SYS(mobile)
    return (f'<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
            f'<style>\n{css}\n</style>\n<div class="site">{arts}{FOOT}</div>\n{SHEET}\n<script>\n{JS}\n</script>\n')

open('desktop.html', 'w').write(finish(build(False)))
open('mobile.html', 'w').write(finish(build(True)))
print('ok')
