import base64, html, io, re, contextlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
    import build_events as E

esc = E.esc
KANA = B.KANA
VIDEO = 'data:video/mp4;base64,' + base64.b64encode(open('hero.mp4', 'rb').read()).decode()
ZEN = 'https://brooklynaikikai.sites.zenplanner.com/login.cfm'

def ph(label, ratio='16/9'): return f'<figure class="ph" style="aspect-ratio:{ratio}"><figcaption>{html.escape(label)}</figcaption></figure>'
def p(t, cls=''): return f'<p{" class=%s" % chr(34)+cls+chr(34) if cls else ""}>{esc(t)}</p>'
def sec(label, body, sub='', cls='', left=''):
    s = f'<p class="by">{esc(sub)}</p>' if sub else ''
    h = f'<h2>{html.escape(label)}</h2>{s}' if label else ''
    return f'<section class="sec {cls}"><div class="lab-wrap"><div class="lab">{h}{left}</div></div><div class="bd">{body}</div></section>'
def rows(pairs): return '<dl class="du">' + ''.join(f'<div><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in pairs) + '</dl>'
def tile(a, b): return f'<div class="tl"><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>'
def play(label, ratio='16/9'):
    return f'<figure class="ph vid" style="aspect-ratio:{ratio}">{B.PLAY}<span class="bar" aria-hidden="true"><i></i></span><figcaption>{html.escape(label)}</figcaption></figure>'

# ---------------- Kids' Aikido ----------------
def kids():
    notes = (p('Our classes for Fall 2026 are now full. Please email Kate if you are interested in being placed on a waitlist for classes beginning in January 2027.')
             + p("Click [here](https://youtu.be/3byzot6okRU?si=DlJsi_ujug2k8HAZ) for a video on how to tie your child's belt."))
    cal = ('<div class="mo"><h3>Calendar</h3><ul>'
           '<li class="ev"><div class="dt"><b class="x">Nov 26–28</b></div><p>Thanksgiving Break</p></li>'
           '<li class="ev"><div class="dt"><b class="x">Dec 24–Jan 2</b></div><p>Winter Break</p></li>'
           '<li class="nt"><p>(January 5 - open for classes)</p></li>'
           '<li class="ev"><div class="dt"><b class="x">Jan 7–9</b></div><p>Closed due to meditation intensive</p></li></ul></div>')
    days = ''.join(f'<div class="kd"><h3>{d}</h3>{tile("Ages 6–9", a)}{tile("Ages 10–14", b)}</div>' for d, a, b in
                   (('Tuesday', '4:15–5:00 pm', '5:00–5:45 pm'), ('Thursday', '4:15–5:00 pm', '5:00–5:45 pm'), ('Saturday', '8:15–9:00 am', '9:00–9:45 am')))
    dues = (p('Monthly membership fees are based on a sliding scale. Please choose the rate that best reflects your ability to pay monthly and to support our nonprofit school. Regardless of which you choose, your child is invited to attend any and all of the classes for their age group.')
            + p('(Please note, as of September 2026, due to our increasing costs, we have had to raise our membership fees slightly.)', 'fine')
            + rows([('Gi (uniform)', '$25'), ('Community Rate', '$60 per month'), ('Standard Rate', '$85 per month'), ('Pay-it-forward level 1', '$110 per month'),
                    ('Pay-it-forward level 2', '$125 per month'), ('Pay-it-forward level 3', '$150 per month')]))
    inst = (ph('Photo: Kate Savoca, children’s instructor', '16/9')
            + p('Kate holds the rank of godan (5th degree black belt) and is certified to teach by Birankai North America. She has been teaching aikido to children for more than 20 years and has also been an elementary school teacher since 1995.'))
    phil = (p('There are no competitions in Aikido. Each of us is here to grow at our own pace. More experienced students are encouraged to help beginners so that everyone progresses together.', 'ld')
            + p('Through the practice of Aikido exercises and techniques in the setting of a traditional dojo, we strive to build each child\'s strength, flexibility, and attention. Learning "the moves" is all very nice, but what we are really working on here is bigger than that: looking someone in the eye, paying attention to details, practicing good posture, sustaining focus, persevering in the face of a challenge, and more ...'))
    steps = ['Choose a monthly membership rate (see above). Note: All students (regardless of payment) are welcome to come to any/all three classes a week for their age group.',
             'Email Kate at mail@brooklynaikikai.com to receive a link for registration and payment.',
             'Pay for your first month of dues and purchase a uniform for $25.']
    join = ('<div class="mo flat"><h3>New Child Members</h3></div>' + p("We register new students for our Children's classes twice a year: in January and September.")
            + '<ol class="stp">' + ''.join(f'<li><span class="dash" aria-hidden="true"></span><span>{html.escape(t)}</span></li>' for i, t in enumerate(steps)) + '</ol>')
    quote = ('<blockquote class="q box"><p class="hq">“Last week after class, I had my son stop and look at the outside of the dojo, and tell me what he observed and noticed. He mentioned the wooden sign that looked like it had hand-carved Japanese writing, the wooden doors, the handwritten sign on the door, and the rock with the salt offering. I asked him what these things told him about Brooklyn Aikikai. He said something like, “They put a lot of care and thought into what they do. They want to teach us the tradition, and aren\'t just about making money.” He got it. : ) Thank you for all you teach our children about discipline, practice, respect, and tradition.”</p><cite>Stacy R.</cite></blockquote>')
    return (sec('Schedule notes', notes + cal) + f'<section class="wkwrap"><div class="kgrid">{days}</div></section>'
            + sec('Dues and costs', dues) + sec('Kate Savoca', inst, "children's instructor") + sec('', phil, left=ph('Photo: Choice', '4/5'))
            + sec('Joining the dojo', join) + sec('Testimonials', quote))

# ---------------- Dojo Members ----------------
def members():
    cards = [
     ('La Conexión', 'LA CONEXIÓN', 'Member only forum / announcements', 'A place to connect with the dojo community online.', 'Photo: Blog image', None),
     ('Video Gallery', 'VIDEO GALLERY', '', 'This part is still under construction! Please visit again soon.', 'Photo: Screenshot, March 2025', None),
     ('Student Resources', 'STUDENT RESOURCES', 'Forms, procedures, and information', 'Study guides, scholarship forms, dan registration forms and guidelines...', 'Photo: Name tags', None),
     ('Dues', 'DUES', '', 'Link to ZenPlanner for due payments.', 'Photo: Jizo', ZEN),
    ]
    out = ''
    for label, _, tag, desc, cap, href in cards:
        body = f'<h2>{html.escape(label)}</h2>' + (f'<p class="tg">{html.escape(tag)}</p>' if tag else '') + f'<p>{html.escape(desc)}</p>'
        inner = ph(cap, '4/3') + f'<div class="mc-t">{body}</div>'
        if href: out += f'<a class="mcard" href="{href}" target="_blank" rel="noopener">{inner}</a>'
        else: out += f'<a class="mcard" href="#" data-dead>{inner}</a>'
    return f'<section class="wkwrap"><div class="mgrid">{out}</div></section>'

# ---------------- Donate ----------------
def donate():
    intro = (p('Through your continued support, we have been able to thrive and flourish, keeping our dojo space in New York City for over two decades! Your donations help us to cover our sliding scale for dues, the rising costs of material goods, utilities, and scholarships that enable travel year after year. We’ve put together a montage film of the last 25 years to show just how lucky we are to have a community like this! Thank you for your continued support!')
             + play('Video: 25 years of Brooklyn Aikikai'))
    give = (p('Brooklyn Aikikai is a nonprofit dedicated to rigorous training and personal transformation through aikido and other traditional Japanese arts.', 'ld')
            + p('Donations help us keep our doors open, fund need-based scholarships for adults and children, and host guest instructors who have dedicated their lives to aikido.')
            + p('This year, in honor of our 25th year, all donations from January 2026, to December 31st, 2026 will count towards our 2026 fundraiser.')
            + p('Thank you for your support!')
            + '<div class="cta"><a class="cb" href="#" data-dead>Donate</a></div>')
    shirts = (p('Check out our new t-shirts! Another excellent design from dojo member Diego Medina-Rosas and Sensei. Grab one today!')
              + '<div class="gal sh4"><figure class="ph big"></figure>' + ''.join('<figure class="ph" style="aspect-ratio:3/4"></figure>' for _ in range(16)) + '</div>')
    check = p('Donations by check can be made payable to Brooklyn Aikikai. Our mailing address is 408 3rd Avenue, Brooklyn, NY 11215.')
    mail = ('<form class="reg" novalidate>' + p('Join our mailing list for fundraising and incentive updates!')
            + '<div class="f"><label for="ml">Email Address</label><input id="ml" name="ml" type="email"></div>'
            + '<label class="opt"><input type="checkbox" name="sub"><span>I want to subscribe to your mailing list.</span></label>'
            + '<button type="submit" class="cb">Subscribe</button></form>')
    return (sec('', intro) + sec('', give) + sec('Here for Summer!', shirts) + sec('Donate by check', check) + sec('', mail))

PAGES = [
 ('kids', "Kids' Aikido", '', kids, True),
 ('members', 'Dojo Members', '', members, False),
 ('donate', 'Donate', '', donate, False),
]

NAVITEMS = [('About', None), ('Schedule', None), ('Join', None), ("Kids' Aikido", 'kids'), ('Dojo Members', 'members')]
def nav(mobile, active):
    if mobile:
        return '<div class="nv"><a class="logo" href="#kids" data-go="kids">Brooklyn Aikikai</a><button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button></div>'
    links = ''.join(f'<a class="nl{" on" if k == active else ""}" href="#{k or ""}" {"data-go=" + k if k else "data-dead"}>{n}</a>' for n, k in NAVITEMS)
    return f'<div class="nv"><a class="logo" href="#kids" data-go="kids">Brooklyn Aikikai</a><nav aria-label="Primary">{links}<a class="don{" on" if active == "donate" else ""}" href="#donate" data-go="donate">Donate</a></nav><button type="button" class="mb" data-open aria-label="Open menu" aria-controls="sheet"><i></i><i></i></button></div>'

def article(mobile, key, title, sub, fn, video):
    vid = f'<video class="hv" autoplay muted loop playsinline aria-hidden="true" src="{VIDEO}"></video><i class="shade"></i>' if video else ''
    return (f'<article class="pg" data-page="{key}"{"" if key == "kids" else " hidden"}>{B.chrome_ah(mobile)}'
            f'<header class="hr">{vid}{nav(mobile, key)}<div class="hh">'
            + ('<span class="ey hero">Brooklyn Aikikai</span>' if key == 'donate' else '')
            + f'<h1>{html.escape("25 Years" if key == "donate" else title)}</h1></div>'
            + ('' if video else '<span class="pl">Hero image placeholder</span>')
            + f'</header><main class="mn">{fn()}</main></article>')

def build(mobile):
    title = 'Brooklyn Aikikai Website rev16 ' + ('Mobile' if mobile else 'Desktop')
    css = B.CSS + open('ext.css').read() + (open('mobile.css').read() if mobile else open('desktop.css').read() + open('sheet.css').read()) + open('events.css').read() + (open('events-m.css').read() if mobile else open('events-d.css').read()) + open('rev16.css').read() + (open('rev16-m.css').read() if mobile else open('rev16-d.css').read()) + B.SYS(mobile)
    sheet = B.SHEET
    for k, n in (('mission', 'x'),): pass
    sheet = (sheet.replace('class="slogo" href="#mission" data-go="mission"', 'class="slogo" href="#kids" data-go="kids"')
             .replace('<a class="si" href="#mission" data-go=mission style="--i:0">', '<a class="si" href="#" data-dead style="--i:0">')
             .replace('<a class="si" href="#" data-dead style="--i:3">', '<a class="si" href="#kids" data-go="kids" style="--i:3">')
             .replace('<a class="si" href="#" data-dead style="--i:4">', '<a class="si" href="#members" data-go="members" style="--i:4">')
             .replace('<a class="sdon" href="#" data-dead', '<a class="sdon" href="#donate" data-go="donate"'))
    arts = ''.join(article(mobile, *p_) for p_ in PAGES)
    js = B.JS + "\n(function(){var v=document.querySelector('.hv');if(v&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause();}[].forEach.call(document.querySelectorAll('form'),function(f){f.addEventListener('submit',function(e){e.preventDefault();});});})();"
    return (f'<title>{title}</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">\n'
            f'<style>\n{css}\n</style>\n<div class="site">{arts}{B.FOOT}</div>\n{sheet}\n<script>\n{js}\n</script>\n')

open('rev16-desktop.html', 'w').write(B.finish(build(False)))
open('rev16-mobile.html', 'w').write(B.finish(build(True)))
print('ok')
