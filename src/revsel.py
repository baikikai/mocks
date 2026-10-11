"""The Revisions picker in every comp: a corner pill that lists the pages on this site (desktop or mobile to match the build)."""
import html

# key, label, path
ITEMS = [
    ('rev19', 'Rev 19 Index', '/rev19/'),
    ('rev18', 'Rev 18 Pigment', '/rev18/'),
    ('rev17', 'Rev 17 Rail', '/rev17/'),
    ('rev16v', 'Rev 16 Viewport', '/rev16/'),
    ('rev16', 'Rev 16 Baseline', '/rev16-baseline/'),
    ('tech', 'Technique Database v14', '/technique/'),
    ('coll', 'Collection Lacquer v2', '/collection/'),
    ('all', 'All Mocks', '/'),
]
CSS = '''#rv{position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:200;font:400 13px/1.2 'Zen Kaku Gothic New','Hiragino Sans',system-ui,sans-serif}
#rv *{box-sizing:border-box}
#rvb{display:block;background:rgba(12,14,18,.94);color:#ECEDE8;border:1px solid rgba(236,237,232,.3);border-radius:999px;padding:8px 14px;cursor:pointer;font:inherit;letter-spacing:.02em}
#rvb:hover,#rvb[aria-expanded="true"]{border-color:#E2B53F;color:#E2B53F}
#rvb:focus-visible,#rvl a:focus-visible{outline:2px solid #E2B53F;outline-offset:2px}
#rvl{position:absolute;left:0;bottom:calc(100% + 8px);width:max-content;min-width:220px;max-width:calc(100vw - 24px);max-height:min(70vh,520px);overflow-y:auto;background:rgba(12,14,18,.97);border:1px solid rgba(236,237,232,.3);padding:6px 0}
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
    out = '<div id="rv"><button type="button" id="rvb" aria-expanded="false" aria-controls="rvl">Revisions</button><div id="rvl" hidden>'
    for key, label, path in ITEMS:
        href = path + ('mobile/' if mobile and key != 'all' else '')
        cur = ' aria-current="page"' if key == current else ''
        out += f'<a href="{href}"{cur}>{html.escape(label)}</a>'
    return f'<style>{CSS}</style>{out}</div></div><script>{JS}</script>\n'
