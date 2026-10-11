# Brooklyn Aikikai Mocks

Static builds of the design mocks: the website (rev 16 and three directions, rev 17 to 19), the technique database and the collection prototype. Each has a real desktop layout and a real phone layout.

## Build

```sh
pnpm build        # or: python3 make.py
pnpm dev          # build, then serve dist/ on http://localhost:8080
python3 make.py rev18   # rebuild one: rev16, rev17, rev18, rev19, technique
```

Python 3.12 or newer, standard library only. Output goes to `dist/` (ignored). The page is large (about 12 MB each) because photos and video are embedded.

```
dist/
  index.html            the index
  rev16/ rev17/ rev18/ rev19/ technique/ collection/
    index.html          desktop
    mobile/index.html   phone
```

## Layout

| Path | What it is |
| --- | --- |
| `make.py` | builds everything into `dist/` |
| `index.html`, `thumbs/` | the index page and its thumbnails (static) |
| `static/collection/` | the collection prototype, copied as is |
| `src/build_all.py` | rev 16: the shell, every page, i18n |
| `src/build_dir.py` + `dirA.css`, `dirB.css`, `dirC.css`, `extB.js`, `extC.js` | rev 17 Rail, rev 18 Pigment, rev 19 Index |
| `src/build_tech.py` | technique database v14 (font set D) from `technique-entry-prototype-v13.html` |
| `src/revsel.py` | the Revisions picker in every comp |
| `src/system*.css`, `heroes*.css`, `app.js`, `extras.js` | shared styles and behaviour |
| `src/web.json`, `blog.json`, harvested `*.html` | the live site's copy, used as is |

Every duration and easing in a direction is rewritten to that direction's tokens in `build_dir.py` (`norm_motion`).

## Deploy

Netlify runs `python3 make.py` and publishes `dist/` (see `netlify.toml`, `PYTHON_VERSION = 3.12`). Pages are marked `noindex`.

Older revisions (1 to 15), the directions proposal and the earlier prototypes live on claude.ai; the index links to them.
