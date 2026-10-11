import html, io, re, contextlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
    import build_sched as S
src = open('gen.py').read().split("out={}")[0]
ns = {}
exec(src, ns)
os.chdir('.')
items = ns['parse']('events')

MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
ABBR = {m: m[:3] for m in MONTHS}
DOW = {d: d for d in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')}

# ---- parse: poster, then per year the month blocks (the site lays months out column by column)
poster = next(i for i in items if i['type'] == 'img')
years = {}; cur = None; month = None; past = False
gallery = [i for i in items if i['type'] == 'img' and i is not poster]
for it in items:
    if it['type'] == 'h3' and 'Events' in it['text']:
        cur = it['text']; years[cur] = {}; month = None; continue
    if it['type'] == 'h2' and 'Past Events' in it['text']:
        past = True; cur = None; continue
    if cur is None or it['type'] != 'p': continue
    t = it['text'].strip()
    name = t.rstrip('.').strip()
    if name in MONTHS:
        month = name; years[cur].setdefault(month, []); continue
    if t == 'Thanks for submitting!' or month is None: continue
    years[cur][month].append(t)

DATE = re.compile(r'^(\w+day), (\w+) (\d+)\w*(?: - (\w+day), (\w+) (\d+)\w*)?, (.*)$')

def esc(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\[([^\]]*?)(\s*)\]\(([^)]+)\)', r'<a class="lk" href="\3" target="_blank" rel="noopener">\1</a>\2', t)

def date_block(m, group):
    d1, mo1, n1, d2, mo2, n2, _ = m.groups()
    if d2 is None:
        return f'<span>{DOW[d1]}</span><b>{n1}</b>'
    days = f'{DOW[d1]}\u2013{DOW[d2]}'
    if mo1 == mo2:
        return f'<span>{days}</span><b>{n1}\u2013{n2}</b>'
    start = f'{ABBR[mo1]}&nbsp;{n1}' if mo1 != group else n1
    return f'<span>{days}</span><b class="x">{start}\u2013{ABBR[mo2]}&nbsp;{n2}</b>'

def classify(t):
    low = t.lower()
    if 'sesshin' in low or 'zazenkai' in low: cat = 'zen'
    elif 'misogi' in low: cat = 'misogi'
    elif any(k in low for k in ('seminar', 'camp', 'testing', 'shihan')) and 'self defense' not in low: cat = 'aikido'
    else: cat = ''
    if 'Brooklyn Aikikai' in t: loc = 'at'
    elif '](' in t or re.search(r'\b(?:at|in) [A-Z]', t): loc = 'away'
    else: loc = 'at'
    return cat, loc

def year_body(blocks):
    out = ''
    for mi, mo in enumerate(MONTHS):
        rows = ''
        for t in blocks.get(mo, []):
            m = DATE.match(t)
            if m:
                cat, loc = classify(m.group(7))
                body = m.group(7).rstrip()
                if body.endswith('.') and not re.search(r'\.\s', body): body = body[:-1]   # one short phrase, no full stop
                rows += f'<li class="ev" data-cat="{cat}" data-loc="{loc}"><div class="dt">{date_block(m, mo)}</div><p>{esc(body)}</p></li>'
            else:
                note = t.strip('*').strip()
                rows += f'<li class="nt"><p>{esc(note)}</p></li>'
        has = bool(blocks.get(mo))
        out += f'<div class="mo" data-m="{mi}"{"" if has else " data-empty"}><h3>{mo}</h3><ul>{rows}</ul></div>'
    return out

def poster_fig(label, ratio='11/17'):
    return f'<figure class="ph post" style="aspect-ratio:{ratio}"><figcaption>{html.escape(label)}</figcaption></figure>'

def field(i, label, kind='text', req=False):
    return f'<div class="f"><label for="{i}">{label}{" *" if req else ""}</label><input id="{i}" name="{i}" type="{kind}"{" required" if req else ""}></div>'

POSTER = 'data:image/jpeg;base64,' + __import__('base64').b64encode(open('poster_toko.jpg', 'rb').read()).decode()
BIO = ['Toko J. Flower Sensei began her training in Norwich, England in 1989 before moving to San Diego two years later to train under T. K. Chiba Shihan for three years in the Kenshusei program living for one year as Uchideshi (live in student) at San Diego Aikikai. During this time she was also fortunate to train extensively under M. Murashige Shihan who she considers to be an important teacher for her. In 1997 she moved to Greece and established Athens Aikikai which she ran for ten years before establishing Athens Aikido in 2008. She currently holds the rank of 6th degree black belt and is a Birankai International certified instructor (Shihan). Regularly invited to teach at international seminars, she has taught extensively in the United States, UK, France, Poland and Switzerland. She is Chairman of the Hellenic Birankai Teaching Committee.',
       'In addition to her work in Aikido she has been a dedicated Zen practitioner since the early 90s and continues her studies under the guidance of Canadian teacher Rev. Komyo Seido of Chisoku-an Zendo.']
DOJO = ('Athens Aikido', 'https://www.athensaikido.gr/')

import datetime
TODAY = datetime.date.today()

def pick_featured():
    """The next seminar hosted at the dojo: first dated row on or after today that is at Brooklyn Aikikai and is an aikido event."""
    for title, blocks in years.items():
        y = re.search(r'20\d\d', title).group(0)
        for mo in MONTHS:
            for t in blocks.get(mo, []):
                m = DATE.match(t)
                if m and classify(m.group(7)) == ('aikido', 'at'):
                    d1, mo1, n1, d2, mo2, n2, rest = m.groups()
                    if datetime.date(int(y), MONTHS.index(mo1) + 1, int(n1)) < TODAY: continue
                    name = re.sub(r'\s+at Brooklyn Aikikai\.?$', '', rest).strip(' .')
                    if d2 is None: dates = f'{d1}, {mo1} {n1}, {y}'
                    elif mo1 == mo2: dates = f'{d1}\u2013{d2}, {mo1} {n1}\u2013{n2}, {y}'
                    else: dates = f'{d1}\u2013{d2}, {mo1} {n1} \u2013 {mo2} {n2}, {y}'
                    return name, dates
    return None, None

NAME, DATES = pick_featured()

def featured(mobile):
    facts = ('<dl class="du"><div><dt>Saturday</dt><dd>1:00 pm to 5:15 pm, potluck to follow</dd></div>'
             '<div><dt>Sunday</dt><dd>10 am to 1:15 pm</dd></div>'
             '<div><dt>One day</dt><dd>$85</dd></div><div><dt>Both days</dt><dd>$160</dd></div>'
             '<div><dt>Bring</dt><dd>Bokken and jyo</dd></div></dl>')
    poster = (f'<button type="button" class="pstr" data-drawer="reg" aria-label="Open details and registration for {html.escape(NAME)}">'
              f'<img src="{POSTER}" alt="Poster: {html.escape(NAME)}, {html.escape(DATES)}" width="648" height="1000"></button>')
    body = (f'<h3 class="sh">{html.escape(NAME)}</h3><p class="ld">{html.escape(DATES)}</p><p class="fine">At Brooklyn Aikikai</p>'
            + facts + '<div class="cta"><button type="button" class="cb" data-drawer="reg">Register</button></div>')
    return f'<section class="sec feat"><div class="lab-wrap"><div class="lab"><h2>This Month</h2></div>{poster}</div><div class="bd">{body}</div></section>'

def drawer():
    form = ('<form class="reg" novalidate><h3 class="sh">Seminar registration</h3>'
            + field('fn', 'First Name', 'text', True) + field('ln', 'Last Name', 'text', True)
            + field('em', 'Email Address', 'email', True) + field('ph', 'Phone', 'tel', True)
            + field('dj', 'Home Dojo') + field('rk', 'Rank')
            + '<fieldset class="f days"><legend>Select day(s) attending ($) *</legend>'
              '<label class="opt"><input type="radio" name="days" value="sat"><span>Saturday Only - $85</span></label>'
              '<label class="opt"><input type="radio" name="days" value="sun"><span>Sunday Only - $85</span></label>'
              '<label class="opt"><input type="radio" name="days" value="both"><span>Both Days - $160</span></label></fieldset>'
              '<label class="opt"><input type="checkbox" name="potluck"><span>Please check here if you will be joining the Saturday potluck</span></label>'
              '<button type="submit" class="cb">Submit Registration</button></form>')
    bio = ''.join(f'<p>{html.escape(t)}</p>' for t in BIO)
    dojo = f'<dl class="du"><div><dt>Dojo</dt><dd><a class="lk" href="{DOJO[1]}" target="_blank" rel="noopener">{DOJO[0]}</a></dd></div></dl>'
    return (f'<div id="drawer" role="dialog" aria-modal="true" aria-labelledby="dr-t" hidden><div class="dr-in">'
            f'<button type="button" class="dr-x" aria-label="Close"><i></i><i></i></button>'
            f'<img class="dr-img" src="{POSTER}" alt="Poster: {html.escape(NAME)}, {html.escape(DATES)}" width="648" height="1000">'
            f'<h2 id="dr-t" class="dr-h">{html.escape(NAME)}</h2><p class="dr-d">{html.escape(DATES)}</p>'
            f'<div class="dr-bio">{bio}</div>{dojo}{form}'
            '<div class="info"><h3 class="sh">Seminar information</h3><p>Bring bokken and jyo.</p>'
            '<p>Saturday: 1:00 pm to 5:15 pm. Potluck to follow<br>Sunday: 10 am to 1:15 pm.</p></div></div></div>')

CHEV = '<svg class="chev" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5"/></svg>'

def filters():
    opts = '<li><button type="button" role="option" data-v="" aria-selected="true">All months</button></li>' + ''.join(f'<li><button type="button" role="option" data-v="{i}" aria-selected="false">{m}</button></li>' for i, m in enumerate(MONTHS))
    cat = ''.join(f'<button type="button" class="chip{" on" if v == "" else ""}" data-g="cat" data-v="{v}" aria-pressed="{"true" if v == "" else "false"}">{l}</button>' for v, l in (('', 'All'), ('aikido', 'Aikido'), ('zen', 'Zen'), ('misogi', 'Misogi')))
    loc = ''.join(f'<button type="button" class="chip{" on" if v == "" else ""}" data-g="loc" data-v="{v}" aria-pressed="{"true" if v == "" else "false"}">{l}</button>' for v, l in (('', 'All'), ('at', 'At Brooklyn Aikikai'), ('away', 'Away')))
    yopts = ''.join(f'<li><button type="button" role="option" data-v="{v}" aria-selected="{"true" if v == "" else "false"}">{l}</button></li>' for v, l in (('', 'All years'), ('2026', '2026'), ('2027', '2027')))
    return (f'<div class="filt"><div class="fg"><span class="fl" id="fyr">Year</span><div class="dd" id="yrsel"><button type="button" class="lb" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="fyr"><span>All years</span>{CHEV}</button><ul class="ll" role="listbox" hidden>{yopts}</ul></div></div>'
            f'<div class="fg"><span class="fl" id="fmo">Month</span><div class="dd" id="mosel"><button type="button" class="lb" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="fmo"><span>All months</span>{CHEV}</button><ul class="ll" role="listbox" hidden>{opts}</ul></div></div>'
            f'<div class="fg"><span class="fl" id="fcat">Practice</span><div class="chips" role="group" aria-labelledby="fcat">{cat}</div></div>'
            f'<div class="fg"><span class="fl" id="floc">Where</span><div class="chips" role="group" aria-labelledby="floc">{loc}</div></div></div>')

def year_section(title, blocks):
    y = re.search(r'20\d\d', title).group(0)
    title = f'{y} Events'
    return f'<section class="sec yr" data-y="{y}"><div class="lab-wrap"><div class="lab"><h2>{html.escape(title)}</h2></div></div><div class="bd evs">{year_body(blocks)}<p class="zero yz" hidden></p></div></section>'

def card(g):
    cap = g['file'] if ' ' in g['file'] else ''
    if not cap:
        return '<div class="pc" tabindex="0"><div class="pi"><b>Placeholder</b><span>2012</span></div></div>'
    m = re.search(r'([A-Z][a-z]+ \d+ ?- ?\d+, \d{4})', cap)
    if m:
        date = m.group(1).replace(' - ', '\u2013').replace('-', '\u2013'); rest = re.sub(r',?\s*' + re.escape(m.group(1)), '', cap).strip(' ,')
    else:
        y = re.search(r'\b(20\d\d)\b', cap); date = y.group(1) if y else ''; rest = cap
    return f'<div class="pc" tabindex="0"><div class="pi"><b>{html.escape(date)}</b><span>{html.escape(rest)}</span></div></div>'

def past_section():
    figs = ''.join(card(g) for g in gallery)
    return f'<section class="sec"><div class="lab-wrap"><div class="lab"><h2>Past Events</h2></div></div><div class="bd"><div class="gal">{figs}</div></div></section>'

def bna():
    return '<a class="lnkrow" href="https://birankai.org/events/" target="_blank" rel="noopener"><span>Birankai North America Events</span></a>'

def subnav():
    return ('<nav class="sub" aria-label="Schedule"><span class="lk dead" aria-disabled="true">Classes</span>'
            '<a class="lk on" href="#events" aria-current="page">Events</a></nav>')

def page(mobile):
    secs = featured(mobile) + filters() + '<p class="zero" hidden></p>'
    for title, blocks in years.items():
        secs += year_section(title, blocks)
    secs += past_section() + bna()
    return (f'<article class="pg" data-page="events">{B.chrome_ah(mobile)}<header class="hr">{S.nav(mobile)}<div class="hh"><h1>Events</h1></div><span class="pl">Hero image placeholder</span></header>'
            f'<main class="mn">{subnav()}{secs}</main></article>')

CSS_E = open('events.css').read()
def build(mobile):
    title = 'Brooklyn Aikikai Website rev15 ' + ('Mobile' if mobile else 'Desktop')
    css = B.CSS + open('ext.css').read() + (open('mobile.css').read() if mobile else open('desktop.css').read() + open('sheet.css').read()) + CSS_E + (open('events-m.css').read() if mobile else open('events-d.css').read()) + B.SYS(mobile)
    sheet = B.SHEET.replace('data-go=mission', 'data-dead').replace('class="slogo" href="#mission" data-go="mission"', 'class="slogo" href="#" data-dead')
    return (f'<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
            f'<style>\n{css}\n</style>\n<div class="site">{page(mobile)}{B.FOOT}</div>\n{sheet}\n<script>\n{B.JS}\n{open('events.js').read()}\n</script>\n')

open('events-desktop.html', 'w').write(B.finish(build(False)))
open('events-mobile.html', 'w').write(B.finish(build(True)))
for y, b in years.items(): print(y, {m: len(v) for m, v in b.items() if v})
print(len(gallery), 'gallery images')
