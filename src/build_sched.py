import html, json, re, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build as B

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# practice, start, end  (24h "H:MM")
S = {
 'Monday':   [('zazen','8:00','8:50'),('aikido','12:30','13:30'),('zazen','13:45','14:15'),('aikido','18:00','18:50'),('weapons','19:00','19:50'),('misogi','20:15','21:00')],
 'Tuesday':  [('weapons','8:00','8:50'),('aikido','12:30','13:30'),('aikido','18:00','18:50'),('aikido','19:00','19:50'),('zazen','20:00','20:45')],
 'Wednesday':[('aikido','7:00','7:50'),('zazen','8:00','8:45'),('aikido/weapons','12:00','13:30'),('iaido','17:30','18:45'),('aikido','19:00','19:50'),('misogi','20:00','20:45')],
 'Thursday': [('aikido','8:00','8:50'),('aikido','18:00','18:50'),('aikido','19:00','19:50'),('zazen','20:00','20:45')],
 'Friday':   [('iaido','7:30','8:45'),('zazen','9:00','9:45'),('aikido','12:30','13:30'),('misogi','17:30','18:00'),('weapons','18:15','19:15'),('aikido','19:30','20:30')],
 'Saturday': [('zazen','10:00','10:45'),('aikido','11:00','12:15')],
 'Sunday':   [('zazen','10:00','10:45'),('free practice','11:00','12:15')],
}
PRACTICES = ['aikido', 'weapons', 'iaido', 'zazen', 'misogi', 'free practice']

def mins(t):
    h, m = t.split(':'); return int(h) * 60 + int(m)
def f12(t):
    h, m = map(int, t.split(':')); ap = 'am' if h < 12 else 'pm'; h12 = h % 12 or 12
    return (f'{h12}' if m == 0 else f'{h12}:{m:02d}'), ap
def span(a, b):
    (ta, aa), (tb, ab) = f12(a), f12(b)
    return f'{ta}–{tb} {ab}' if aa == ab else f'{ta} {aa}–{tb} {ab}'
def tags(p): return ' '.join(p.split('/'))

SCALE = 1.05; T0 = 7 * 60; T1 = 21 * 60 + 15

def chips(mobile):
    out = '<div class="chips" role="group" aria-label="Filter by practice"><button type="button" class="chip on" data-f="all" aria-pressed="true">All</button>'
    out += ''.join(f'<button type="button" class="chip" data-f="{p}" aria-pressed="false">{p[0].upper()+p[1:]}</button>' for p in PRACTICES)
    return out + '</div>'

LONG = {'iaido', 'aikido/weapons'}   # the two tile sizes on the current site: regular, and long
def slot(m): return (m // 30) * 30
STARTS = sorted({slot(mins(a)) for d in DAYS for _, a, _ in S[d]})

def grid():
    n = len(STARTS)
    cols = ''
    for d in DAYS:
        blks = ''
        for i, (p, a, b) in enumerate(S[d]):
            r = STARTS.index(slot(mins(a))) + 1
            span_rows = 2 if p in LONG else 1
            name = p[0].upper() + p[1:]
            blks += (f'<div class="blk" data-p="{tags(p)}" style="grid-row:{r} / span {span_rows};--i:{i}">'
                     f'<b>{name}</b><span>{span(a, b)}</span></div>')
        cols += f'<div class="col" style="grid-template-rows:repeat({n},minmax(0,1fr))">{blks}</div>'
    heads = ''.join(f'<div class="dh"><span>{d}</span></div>' for d in DAYS)
    return f'<div class="wk" data-f="all"><div class="wkh">{heads}</div><div class="wkb">{cols}</div></div>'

def weeklist():
    out = ''
    for d in DAYS:
        rows = ''.join(f'<li data-p="{tags(p)}"><b>{p[0].upper()+p[1:]}</b><span>{span(a, b)}</span></li>' for p, a, b in S[d])
        out += f'<section class="day"><h3>{d}</h3><ul>{rows}</ul></section>'
    return f'<div class="week">{out}</div>'

def notes():
    items = ('<li>Thursday, October 8th, zazen 6 pm to 6:40 pm, aikido 7 pm to 8 pm.</li>'
             '<li>Monday, October 12th, there will be one class only, 7 pm to 8 pm.</li>'
             '<li class="fee">Mat fee for visiting students from other dojos is $20 per day</li>')
    return B.sec('Schedule notes', f'<ul class="notes">{items}</ul>')

def subnav():
    return ('<nav class="sub" aria-label="Schedule"><a class="lk on" href="#classes" aria-current="page">Classes</a>'
            '<span class="lk dead" aria-disabled="true">Events</span></nav>')

def nav(mobile):
    if mobile:
        return B.chrome_nav(True).replace('data-go="mission"', 'data-dead')
    links = ''.join(f'<a class="nl{" on" if n == "Schedule" else ""}" href="#" data-dead>{n}</a>' for n, _ in B.NAV)
    return f'<div class="nv"><a class="logo" href="#" data-dead>Brooklyn Aikikai</a><nav aria-label="Primary">{links}<a class="don" href="#" data-dead>Donate</a></nav><button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button></div>'

def page(mobile):
    ah = B.chrome_ah(mobile)
    classes = f'<section class="wkwrap">{chips(mobile)}{weeklist() if mobile else grid()}</section>'
    return (f'<article class="pg" data-page="classes">{ah}<header class="hr">{nav(mobile)}<div class="hh"><h1>Schedule</h1></div><span class="pl">Hero image placeholder</span></header>'
            f'<main class="mn">{subnav()}{notes()}{classes}</main></article>')

CSS_S = open('sched.css').read()
JS_S = open('sched.js').read()

def build(mobile):
    title = 'Brooklyn Aikikai Website rev14 ' + ('Mobile' if mobile else 'Desktop')
    css = B.CSS + open('ext.css').read() + (open('mobile.css').read() if mobile else open('desktop.css').read() + open('sheet.css').read()) + CSS_S + (open('sched-m.css').read() if mobile else open('sched-d.css').read()) + B.SYS(mobile)
    sheet = B.SHEET.replace('data-go=mission', 'data-dead').replace('class="slogo" href="#mission" data-go="mission"', 'class="slogo" href="#" data-dead')
    foot = B.FOOT
    return (f'<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
            f'<style>\n{css}\n</style>\n<div class="site">{page(mobile)}{foot}</div>\n{sheet}\n<script>\n{B.JS}\n{JS_S}\n</script>\n')

open('sched-desktop.html', 'w').write(B.finish(build(False)))
open('sched-mobile.html', 'w').write(B.finish(build(True)))
print('ok')
