#!/usr/bin/env python3
"""Build every mock into dist/. Python 3.12 or newer, standard library only.

    python3 make.py          build everything
    python3 make.py rev16    build one (rev16, rev16-baseline, rev17, rev18, rev19, technique)
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

def rev16_viewport(m):
    BA.REV16_NAME = 'rev16 Viewport'
    return BA.build(m)

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
}

def write(rel, text):
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
