# Baseline

Rev 16 as it stands on October 11, 2026. Nothing is added to it without being asked for. Anything experimental stays behind an opt-in flag and is not built by default.

## In the baseline

- Rev 16 shell: utility bar, hero with the nav, jump nav, sections, footer, event drawer, Spanish and Chinese.
- Heroes keep their fixed heights: 620px on desktop, 380px on phones (`--hero-h`). Nothing is sized from the viewport.
- Hero parallax: the hero stays put and the page slides over it. No gap above the footer.
- The returning nav (headroom) fades in and out. It lives outside the pinned hero while it is a bar.
- A new page always opens at its top.
- Weekday headers on the schedule stay under the nav while the week scrolls.
- Section labels stick only when their section is tall enough to need it (desktop).
- Revisions pill in every comp.
- Title Case on headings, labels, nav, buttons and chips.

## Not in the baseline

- Any hero height from `vh`, `svh`, `dvh` or a measured visible height.
- A hero that fills the screen with the jump nav on its bottom edge. The experiment is kept in `src/fullheight.css`; to build it anyway: `MOCKS_FULLHEIGHT=1 python3 make.py`.

## Rule

Change one thing at a time, say what changed, and rebuild all of `dist/` before publishing.
