#!/usr/bin/env python3
"""Build every mock into dist/. Python 3.12 or newer, standard library only.

    python3 make.py          build everything
    python3 make.py rev16    build one (rev16, rev16-baseline, rev17, rev18, rev19, technique, donate)
"""
import contextlib, io, os, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC, DIST = ROOT / 'src', ROOT / 'dist'
os.chdir(SRC)
sys.path.insert(0, str(SRC))
with contextlib.redirect_stdout(io.StringIO()):   # the legacy page builders print as they import
    import build_all as BA
    import build_dir as BD
    import build_tech as BT
    import build_donate as BDN

def splash():
    """The annual fundraiser poster, shown first and dismissible; the site is underneath."""
    import base64
    src = 'data:image/jpeg;base64,' + base64.b64encode(Path('img/poster.jpg').read_bytes()).decode()
    x = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>')
    arrow = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')
    alt = 'Brooklyn Aikikai Annual Fundraiser, Oct. 8 to Nov. 8, 2026. Celebration at Rodeo Bar, Nov. 8th, 5pm to 8pm. brooklynaikikai.com/donate'
    return f'''
<style>
#splash{{position:fixed;inset:0;z-index:200;background:rgba(8,10,13,.82);opacity:0;visibility:hidden;transition:opacity .45s cubic-bezier(.2,.7,.2,1),visibility 0s linear .45s}}
#splash.open{{opacity:1;visibility:visible;transition:opacity .45s cubic-bezier(.2,.7,.2,1),visibility 0s}}
#splash .sp-c{{position:absolute;inset:5vmin;display:flex;flex-direction:column;align-items:center;gap:20px;transform:translateY(48px);opacity:0;transition:transform .55s cubic-bezier(.2,.7,.2,1),opacity .45s cubic-bezier(.2,.7,.2,1)}}
#splash.open .sp-c{{transform:none;opacity:1}}
#splash.out .sp-c{{transform:translateY(-48px);opacity:0}}
#splash .sp-i{{position:relative;flex:1 1 0;min-height:0;width:100%}}
#splash img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}}
#splash .sp-go{{display:inline-flex;align-items:center;gap:12px;min-height:60px;padding:0 40px;background:#E2B53F;color:#14171C;font-family:var(--D);font-size:24px;transition:background .25s,transform .3s cubic-bezier(.2,.7,.2,1)}}
#splash .sp-go svg{{transition:transform .3s cubic-bezier(.2,.7,.2,1)}}
#splash .sp-go:hover{{background:#ECEDE8}}
#splash .sp-go:hover svg{{transform:translateX(6px)}}
#splash .sp-x{{position:absolute;top:0;right:0;width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:#14171C;color:#ECEDE8;border:1px solid rgba(236,237,232,.4);transition:background .2s,color .2s}}
#splash .sp-x:hover{{background:#ECEDE8;color:#14171C}}
@media (max-width:900px){{#splash .sp-c{{gap:14px}}#splash .sp-go{{width:100%;justify-content:center;min-height:56px}}#splash .sp-x{{top:8px;right:8px}}}}
@media (prefers-reduced-motion:reduce){{#splash,#splash .sp-c{{transition:none}}}}
</style>
<div id="splash" role="dialog" aria-modal="true" aria-label="Annual Fundraiser">
  <div class="sp-c"><div class="sp-i"><img src="{src}" alt="{alt}" decoding="sync"></div>
  <a class="sp-go" href="#donate" data-go="donate">Donate {arrow}</a>
  <button type="button" class="sp-x" aria-label="Close">{x}</button></div>
</div>
<script>(function(){{var s=document.getElementById('splash'),r=document.documentElement;
function show(){{s.classList.add('open');r.style.overflow='hidden';var b=s.querySelector('.sp-x');if(b)b.focus({{preventScroll:true}})}}
function hide(){{if(!s.classList.contains('open')||s.classList.contains('out'))return;s.classList.add('out');setTimeout(function(){{s.classList.remove('open','out');r.style.overflow=''}},450)}}
s.addEventListener('click',function(e){{if(e.target===s||e.target.closest('.sp-x')||e.target.closest('.sp-go'))hide()}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')hide()}});
requestAnimationFrame(function(){{requestAnimationFrame(show)}})}})();</script>
'''

def rev16_viewport(m):
    BA.REV16_NAME = 'rev16 Viewport'
    html = BA.build(m)
    return html.replace('</body>', splash() + '</body>', 1) if '</body>' in html else html + splash()

def rev16_baseline(m):
    """The rollback point: rev16 as it was before the viewport work. Snapshot CSS and JS, fixed hero heights, none of the later fixes."""
    saved = (BA.FULLH, BA.SYS2_FILE, BA.B.JS)
    BA.FULLH, BA.SYS2_FILE = '', 'baseline/system2.css'
    BA.B.JS = Path('baseline/app.js').read_text(encoding='utf-8')
    BA.REV16_NAME = 'rev16 Baseline'
    try:
        return BA.build(m)
    finally:
        BA.FULLH, BA.SYS2_FILE, BA.B.JS = saved

JOBS = {
    'rev16': rev16_viewport,
    'rev16-baseline': rev16_baseline,
    'rev17': lambda m: BD.build('A', m),
    'rev18': lambda m: BD.build('B', m),
    'rev19': lambda m: BD.build('C', m),
    'technique': lambda m: BT.build(m),
    'donate': lambda m: BDN.build(m),
    'donate2': lambda m: BDN.build(m, 2),
}

def with_viewport(rel, text):
    # without this, iOS lays the page out at 980px and shrinks it, so everything reads tiny
    if 'name="viewport"' in text[:3000]:
        return text
    content = 'width=device-width, initial-scale=1, viewport-fit=cover' if '/mobile/' in '/' + rel else 'width=1280'
    tag = f'<meta name="viewport" content="{content}">'
    if '<meta charset="utf-8">' in text[:3000]:
        return text.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + tag, 1)
    return tag + text

def write(rel, text):
    text = with_viewport(rel, text)
    p = DIST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    print(f'  {rel:<28} {p.stat().st_size / 1e6:5.1f} MB')

def main(only):
    if not only:
        shutil.rmtree(DIST, ignore_errors=True)
    for name, job in JOBS.items():
        if only and name not in only:
            continue
        print(name)
        # rev16 first: the other directions swap the shared home-page body when they build
        write(f'{name}/index.html', job(False))
        write(f'{name}/mobile/index.html', job(True))
    if not only:
        for f in ('desktop', 'mobile'):
            src = ROOT / 'static' / 'collection' / f'{f}.html'
            write(f'collection/{"mobile/" if f == "mobile" else ""}index.html', src.read_text(encoding='utf-8'))
        shutil.copy2(ROOT / 'index.html', DIST / 'index.html')
        shutil.copytree(ROOT / 'thumbs', DIST / 'thumbs')
        print('index, thumbs')

if __name__ == '__main__':
    main(set(sys.argv[1:]))
