"""Blog: an index and post pages. Posts reuse the editorial template of the Tendokan page."""
import html, json, re, datetime
import build as B
import build_tend as T

POSTS = {p['slug']: p for p in json.load(open('blog.json'))}
SLUGS = ['thoughts-on-sesshin-by-k-bloom', 'the-sangha', 'on-giving', 'seminar-with-juba-nour-sensei']  # newest first
LIVE = sorted((POSTS[s] for s in SLUGS), key=lambda p: p['date'], reverse=True)

META = json.load(open('blog-meta.json'))
def key(p): return 'post-' + p['slug']
def title(p): return META[p['slug']]['title']
def author(p): return META[p['slug']]['author']
def summary(p): return META[p['slug']]['summary']
def when(p):
    d = datetime.date.fromisoformat(p['date'][:10]); return f'{d:%B} {d.day}, {d.year}'

def md(t):
    t = B.esc(t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*([^*]+)\*(?!\w)', r'<em>\1</em>', t)
    return t.replace('\n', '<br>')

def plain(t): return re.sub(r'^[A-Z][a-z]+ \d{1,2}, \d{4}', '', re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', re.sub(r'\*+', '', t)).replace('\xa0', ' ')).strip()

def index():
    cards = ''.join(
        f'<a class="bc" href="#{key(p)}" data-go="{key(p)}"><figure class="ph" style="aspect-ratio:3/2"></figure>'
        f'<time datetime="{p["date"][:10]}">{when(p)}</time><h3>{html.escape(title(p))}</h3>{('<span class="au">' + html.escape(author(p)) + '</span>') if author(p) else ''}<p>{html.escape(summary(p))}</p></a>' for p in LIVE)
    return B.sec('Blog', f'<div class="bl">{cards}</div>')

def post(p):
    out = T.byline([when(p)])
    blocks = p['blocks']; i = 0; first = True
    while i < len(blocks):
        b = blocks[i]; t = b['type']
        if t == 'img':
            run = []
            while i < len(blocks) and blocks[i]['type'] == 'img': run.append(blocks[i]); i += 1
            if len(run) == 1: out += T.figure('', '21/9')
            else:
                for k in range(0, len(run) - 1, 2): out += T.pair('', '')
                if len(run) % 2: out += T.figure('', '21/9')
            continue
        i += 1
        if t in ('h2', 'h3', 'h4'): out += f'<h2 class="edh">{md(b["text"])}</h2>'
        elif t == 'quote': out += f'<blockquote class="q sm"><p class="hq">{md(b["text"])}</p></blockquote>'
        elif t in ('ul', 'ol'): out += '<ol class="stp">' + ''.join(f'<li><span class="dash" aria-hidden="true"></span><span>{md(x)}</span></li>' for x in b['items']) + '</ol>'
        elif t == 'p':
            drop = ' drop' if first else ''; first = False
            out += f'<div class="pn{drop}"><p>{md(b["text"])}</p></div>'
    out += '<p class="edby"><a class="lk" href="#blog" data-go="blog">Blog</a></p>'
    return f'<div class="ed">{out}</div>'
