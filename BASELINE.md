# Baseline

`/rev16-baseline/` is the rollback point: rev 16 exactly as it was just before the viewport work began. Its CSS and JS are frozen snapshots in `src/baseline/`.

It has: the rev 16 shell, the pinned-hero parallax, the sticky weekday headers, the event drawer, Spanish and Chinese. Heroes are 620px on desktop and 380px on mobile.

It does not have anything from after that point: no full-height hero, no fade on the returning nav, no scroll-to-top on page change, no footer gap fix. Those live in `/rev16/` (Rev 16 Viewport).

One exception, on request: the new glossary layout (`src/glossary.css`, `build_join.py`) is applied to the baseline as well. The frozen files in `src/baseline/` are untouched.

Do not edit `src/baseline/`.
