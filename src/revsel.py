"""One revision picker for every comp: a corner pill that lists real links, desktop or mobile to match the build."""
import html, os
A = 'https://claude.ai/artifact/'
LOCAL = os.environ.get('MOCKS_LOCAL') == '1'
PATH = {'rev19': '/rev19/', 'rev18': '/rev18/', 'rev17': '/rev17/', 'rev16': '/rev16/', 'tech': '/technique/', 'coll': '/collection/', 'all': '/'}
# key, label, desktop id, mobile id (same id twice when there is one build)
GROUPS = [
    ('Site', [
        ('rev19', 'Rev 19 Index', 'Qra9fjs2Cp7vNA1ZFTfzwY', 'Uiocn2dWvxt1KF3ram4jhb'),
        ('rev18', 'Rev 18 Pigment', 'Aj1EPpEfCDdThwDMXdUS7z', 'D8xffQfGVpHbHRDaBjZ2NH'),
        ('rev17', 'Rev 17 Rail', '9XEynkuFapEmqbZ4FUdSpX', 'Cwz8ufgJVeKLNDteBgy2Do'),
        ('rev16', 'Rev 16', 'AwzhgzHvDKXmCvg8kgRhEL', 'SC6hpbHabduJwd3XurMuzf'),
    ]),
    ('Technique and Collection', [
        ('tech', 'Technique Database v14', 'LijTjQqke4fJcLQAYLhep4', '6pGESxKtrDG7xp47WPq4bo'),
        ('coll', 'Collection Lacquer v2', '7FSfiqexNKefTqzCsha92Q', 'ELtQSdkDEzGGRK2W4cfhey'),
        ('tv13', 'Technique Entry v13', '4MecTXrkgpeiQAotckVeA6', 'MrddZW4jYBCjQYqvFzo7cc'),
    ]),
    ('Earlier Site Revisions', [
        ('rev15', 'Rev 15', 'AtkT2tijBzCrmnRth4MMiS', 'Jyh2Wc9whAWkM66iDB8y5e'),
        ('rev14', 'Rev 14', 'M9RkgvXE5sRprgrc7eXjRx', 'FSwqeNV7DVHDJzqH1CYVKN'),
        ('rev13', 'Rev 13', '1SjdYZYUcu6WKLoyxH1emT', 'QX8Tv1UFQyi9xwh2uB9sJ2'),
        ('rev12', 'Rev 12', 'TThWAefMpTkjP2Lr7zaZ6p', '5E4puez8Qe2yhrXgPdnUMq'),
    ]),
    ('More', [
        ('prop', 'Directions Proposal', 'DBcFENmfJY8ZYL1Nb29ToT', 'DBcFENmfJY8ZYL1Nb29ToT'),
        ('all', 'All Revisions', '3u52BvdQZHrZx4rnZGbc2B', '3u52BvdQZHrZx4rnZGbc2B'),
    ]),
]
CSS = '''#rv{position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:200;font:400 13px/1.2 'Zen Kaku Gothic New','Hiragino Sans',system-ui,sans-serif}
#rv *{box-sizing:border-box}
#rvb{display:block;background:rgba(12,14,18,.94);color:#ECEDE8;border:1px solid rgba(236,237,232,.3);border-radius:999px;padding:8px 14px;cursor:pointer;font:inherit;letter-spacing:.02em}
#rvb:hover,#rvb[aria-expanded="true"]{border-color:#E2B53F;color:#E2B53F}
#rvb:focus-visible,#rvl a:focus-visible{outline:2px solid #E2B53F;outline-offset:2px}
#rvl{position:absolute;left:0;bottom:calc(100% + 8px);width:max-content;min-width:220px;max-width:calc(100vw - 24px);max-height:min(70vh,520px);overflow-y:auto;background:rgba(12,14,18,.97);border:1px solid rgba(236,237,232,.3);padding:6px 0}
#rvl .g{padding:12px 16px 4px;color:#A5ABB3;font-size:12px}
#rvl a{display:block;padding:8px 16px;color:#ECEDE8;text-decoration:none;white-space:nowrap}
#rvl a:hover{background:rgba(236,237,232,.1)}
#rvl a[aria-current]{color:#E2B53F}
'''
JS = '''(function(){var b=document.getElementById('rvb'),l=document.getElementById('rvl');if(!b||!l)return;
function set(o){l.hidden=!o;b.setAttribute('aria-expanded',o?'true':'false')}
b.addEventListener('click',function(e){e.stopPropagation();set(l.hidden)});
document.addEventListener('click',function(e){if(!l.hidden&&!e.target.closest('#rv'))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!l.hidden){set(false);b.focus()}});})();'''
def block(mobile, current):
    i = 3 if mobile else 2
    out = '<div id="rv"><button type="button" id="rvb" aria-expanded="false" aria-controls="rvl">Revisions</button><div id="rvl" hidden>'
    for g, items in GROUPS:
        out += f'<div class="g">{html.escape(g)}</div>'
        for it in items:
            cur = ' aria-current="page"' if it[0] == current else ''
            if LOCAL and it[0] in PATH:
                href = PATH[it[0]] + ('mobile/' if mobile and it[0] != 'all' else '')
                out += f'<a href="{href}"{cur}>{html.escape(it[1])}</a>'
            else:
                out += f'<a href="{A}{it[i]}" target="_blank" rel="noopener"{cur}>{html.escape(it[1])}</a>'
    return f'<style>{CSS}</style>{out}</div></div><script>{JS}</script>\n'


# ---- the visible height: the frame the page runs in can be taller than what is on screen
import re as _re
VH_JS = """/* visible height: measure what is actually on screen, not the frame the page sits in */
(function () {
  var root = document.documentElement;
  if (!('IntersectionObserver' in window) || !document.body) return;
  var p = document.createElement('div');
  p.setAttribute('aria-hidden', 'true');
  p.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:100vh;pointer-events:none;visibility:hidden';
  document.body.appendChild(p);
  var thr = []; for (var i = 0; i <= 400; i++) thr.push(i / 400);
  var io = new IntersectionObserver(function (es) {
    var e = es[es.length - 1], h = e.boundingClientRect.height * e.intersectionRatio;
    if (h > 200) root.style.setProperty('--vh', Math.round(h) + 'px');
  }, { threshold: thr });
  io.observe(p);
  window.addEventListener('resize', function () { io.unobserve(p); io.observe(p); });
})();"""
_TOK = _re.compile(r'(?<![\w-])100(?:svh|dvh|vh)(?![\w-])')
def vh_css(page):
    """In every <style> block (outside data: urls) 100vh, 100svh and 100dvh become the measured visible height."""
    def block(m):
        parts = _re.split(r'(url\(data:[^)]*\))', m.group(2))
        parts = [x if x.startswith('url(data:') else _TOK.sub('var(--vh,100svh)', x) for x in parts]
        return m.group(1) + ''.join(parts) + m.group(3)
    return _re.sub(r'(<style>)(.*?)(</style>)', block, page, flags=_re.S)
