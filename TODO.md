# TODO

## Before the site goes live

- [ ] Push. The course URL currently serves the **old DWV site** — that stale
      content is public right now, and the first push replaces it.
- [ ] Watch the first GitHub Action run. Every render so far used the local
      toolchain (Quarto 1.4.555 + TeX Live); CI uses newer Quarto + TinyTeX.
      A PDF failure fails the whole publish.
- [ ] Once live: click 📡 Subscribe on a phone (webcal only works against the
      real URL), download one `.docx` and check Properties says "PST 315",
      spot-check a guideline page for images.

## Before Week 1 (class Tue Aug 25, first deadline Fri Aug 28)

- [ ] **Project Application page is an empty stub** and it's due Fri Aug 28.
      Needs its instructions and the Qualtrics link.
- [ ] Set up the Qualtrics form for the Project Application.
- [ ] Post to Blackboard the things the site now points at:
      - [ ] Practice report data (Excel) — deliberately not on the public site
      - [ ] UCA example reports — referenced from Practice Report and Rough Draft
      - [ ] Submission portals for each assignment

## During the semester

- [ ] **Excel Coding Workshop** (Wk 6) and **Excel Graphing Workshop** (Wk 7)
      are placeholders — "Coming later". Their guidelines are already written.
- [ ] Add the UCA roster to `overview.qmd` once UCAs consent to being listed on
      a public site. The section heading and intro are there; the table is not.

## Decisions still open

- [ ] Move `bare-essentials.pdf` to Blackboard instead of the public site?
- [ ] Sample Contract & Timeline still runs on a Spring 2023 timeline
      (Jan 25 – May 1). Updating means reworking the internal dates, not just
      swapping them.
- [ ] Practice Report still names the three real partner sites (ITC,
      PLSA@Fowler, Syracuse Police Cadets) and the real 432/457 attendance
      figures. Genericize, or leave as study metadata?
- [ ] Keep `Prior Assignments/` local-only forever, or archive it somewhere
      private but backed up? It is currently gitignored and exists nowhere else.

## Worth fixing when there's time

- [ ] Due dates live in both the assignment pages and
      `tools/build_calendar.py` with nothing syncing them. Change one, and
      subscribed students silently get the wrong date. Best fix: have the script
      read dates from the `.qmd` files, plus a check that fails on mismatch.
- [ ] Headshot is 5552×5536 / 3.7 MB and displays at 100px.
- [ ] `formatted-report-shell.docx` footer placeholder says "April 2026" —
      intentionally left for students to overwrite, but it is a spring month on
      a fall course.

## Next year

- [ ] Roll every date forward: `tools/build_calendar.py`, the `Due` lines in all
      17 assignment pages, `assignments/index.qmd` tables, the three
      Fall-2026-stamped templates in `assignments/files/`.
- [ ] Re-check that Fall Break and Thanksgiving still fall where the 15-week
      structure assumes.
