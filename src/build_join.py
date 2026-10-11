import html, io, re, contextlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
    import build_rev16 as R
src = open('gen.py').read().split("out={}")[0]
ns = {}; exec(src, ns); parse = ns['parse']
esc, p, sec, rows, ph = R.esc, R.p, R.sec, R.rows, R.ph

def cap(t): return t[:1].upper() + t[1:]
def money(t):
    a, _, b = t.partition(' = '); return (a.strip(), b.strip())

# ---------- Becoming a member ----------
def join():
    ps = [i['text'] for i in parse('join') if i['type'] == 'p']
    intro_html = p(ps[0], 'ld') + ''.join(p(t) for t in ps[1:10])
    levels = [money(t) for t in ps[11:17]]
    dues = ('<h3 class="sh">' + html.escape(cap(ps[10])) + '</h3>' + rows(levels)
            + '<h3 class="sh">' + html.escape(cap(ps[17])) + '</h3>' + p(ps[18])
            + p(ps[19]) + p(ps[20]) + p(ps[21])
            + '<h3 class="sh">Note</h3>' + p(ps[22]) + p(ps[23], 'fine'))
    def step(t, detail=''):
        t = re.sub(r'^\d\.\s*', '', t).replace(' .', '.')
        d = f'<br><span class="sub">{esc(detail)}</span>' if detail else ''
        return f'<li><span class="dash" aria-hidden="true"></span><span>{esc(t)}{d}</span></li>'
    li = step(ps[24], ps[25]) + ''.join(step(t) for t in ps[26:31])
    joining = '<h3 class="sh">New Adult Members</h3><ol class="stp">' + li + '</ol>'
    quote = f'<blockquote class="q box"><p class="hq">\u201c{html.escape(ps[33])}\u201d</p><cite>{html.escape(ps[32])}</cite></blockquote>'
    return (sec('', intro_html, cls='ctr') + sec('Dues', dues) + sec('Joining the dojo', joining) + sec('Testimonial', quote))

# ---------- Member Testimonials ----------
def testimonials():
    """A grid of video placeholders; the details show on hover like the event posters. Names and ranks are placeholders."""
    play = '<svg class="play" width="56" height="56" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="27" fill="none" stroke="currentColor" stroke-width="2"/><path d="M23 18l15 10-15 10z" fill="currentColor"/></svg>'
    tile = f'<div class="pc v" tabindex="0">{play}<div class="pi"><b>First Name Last Name</b><span>Shodan</span><span>Training since 2009</span></div></div>'
    return f'<div class="vg">{tile * 12}</div>'

# ---------- Etiquette and Glossary (two pages) ----------
def _gloss_source():
    it = parse('glossary')
    gloss_at = next(k for k, x in enumerate(it) if x['type'] == 'h2' and x['text'] == 'Aikido Glossary')
    return it, gloss_at

def etiquette():
    it, gloss_at = _gloss_source()
    TOPICS = ('Bowing', 'Training', 'Lateness', 'Cleanliness', 'In General')
    topics = {'intro': []}; order = ['intro']; cur = 'intro'
    for x in it[1:gloss_at]:
        if x['type'] == 'p' and x['text'] in TOPICS: cur = x['text']; topics[cur] = []; order.append(cur)
        elif x['type'] == 'p': topics[cur].append(x['text'])
    et = ''.join(p(t) for t in topics['intro'])
    return sec('Etiquette', et) + ''.join(sec(t, ''.join(p(x) for x in topics[t])) for t in order[1:])

def glossary():
    it, gloss_at = _gloss_source()
    letters = []; cur = None; rest = it[gloss_at + 1:]; k = 0
    while k < len(rest):
        x = rest[k]
        if x['type'] == 'h2': cur = [x['text'], []]; letters.append(cur); k += 1; continue
        if x['type'] == 'p' and k + 1 < len(rest) and rest[k + 1]['type'] == 'p': cur[1].append((x['text'], rest[k + 1]['text'])); k += 2; continue
        k += 1
    gl = ''.join(f'<div class="mo" data-m="{l}"><h3>{html.escape(l)}</h3><dl class="gl">' + ''.join(f'<div class="gr"><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in terms) + '</dl></div>' for l, terms in letters)
    return sec('Aikido Glossary', f'<div class="evs">{gl}</div>')

# ---------- Uchideshi program ----------
def uchideshi():
    it = [i for i in parse('uchideshi') if i['type'] != 'img']
    sections = []; cur = None
    for x in it:
        if x['type'] == 'h2': cur = [x['text'], []]; sections.append(cur)
        else: cur[1].append(x['text'])
    def dashlist(items): return '<ol class="stp">' + ''.join(f'<li><span class="dash" aria-hidden="true"></span><span>{esc(t)}</span></li>' for t in items) + '</ol>'
    req = sections[0][1]
    req_html = p(req[0]) + p(req[1]) + dashlist(req[2:6]) + p(req[6]) + p(req[7])
    app = sections[1][1]
    app_html = p(app[0]) + dashlist(app[1:5]) + p(app[5], 'fine')
    exp = sections[2][1]
    exp_html = ''.join(p(t, 'fine' if t.startswith('*') else '') for t in exp)
    add = sections[3][1]
    add_html = rows([tuple(t.split(': ', 1)) for t in add])
    return (sec(cap(sections[0][0]), req_html) + sec(cap(sections[1][0]), app_html)
            + sec(cap(sections[2][0]), exp_html) + sec(cap(sections[3][0]), add_html))
