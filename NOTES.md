# Working notes

Background on how this site is put together and why. `README.md` covers layout
and building; `TODO.md` tracks what's still open. This file is the reasoning.

Built August 2026 by adapting the DWV (Data Wrangling & Visualization) course
site as a template, then replacing all its content with PST 315 material drawn
from the syllabus PDF and the Word/PowerPoint files in `Prior Assignments/`.

---

## The rule that matters most

**The GitHub repo is public.** `github.com/jacklreilly/pst315_f26` returns HTTP
200 anonymously. That means committing a file publishes it, whether or not the
site links to it.

`Prior Assignments/` is gitignored for exactly this reason. It contains the
original course documents, and those hold real client data. None of this was ever committed. Keep it that way. If the folder needs to move
or be renamed, update `.gitignore` in the same commit.

## Anonymization of the worked examples

Every example image on the site is **regenerated with fabricated data**, not
redacted. The originals were deleted. Source of truth is
`tools/swco_data.py`; `build_pages.py` typesets report pages with xelatex,
`build_graphs.py` draws graphs to the PST 315 graphing rules, and
`build_annotated.py` rebuilds the annotated executive-summary header by reading
text positions back out of the PDF.

**SWCO (Skills Win Coaching Organization) is a real Syracuse program** — it is
fine to name, but its *data* must not appear publicly. Every generated example
therefore carries a visible callout saying the numbers are invented. If you
edit `swco_data.py`, keep that true.

Two exceptions kept as real screenshots, both cleaned by `tools/redact_ui.py`:
`codebook-7.png` (cropped to the Excel context menu — it had respondent-level
gender/race columns behind it, plus the author's device name) and
`codebook-8.png` (real workbook filename painted over).

Also removed: three business-casual infographics from Reader's Digest and The
Balance — third-party copyrighted images with visible branding, fine on
Blackboard but not on an open site. Replaced with a CC BY-SA 3.0 illustration
from Wikimedia, attributed in the caption on the Initial Client Meeting guide.

`bare-essentials.pdf` summarizes Coplin & Dwyer, *Does Your Government Measure
Up?* chapter by chapter. Coplin is a colleague, collaborator and rights holder,
so this is a decided non-issue — noted only so it isn't rediscovered as alarming.

## Document metadata

Every file in `assignments/files/` originally carried real names in
`docProps/core.xml` and `app.xml` — invisible in the document, one click away in
Word's Properties pane. Ten people's names in total. `clean_office_metadata.py`
scrubs them.

Gotcha that cost a pass: Word writes these tags **with or without a namespace
prefix** depending on which version saved the file (`<lastModifiedBy>` vs
`<cp:lastModifiedBy>`). The scrubber is now prefix-agnostic. Any new matcher
should be too.

Scrubbing only touches `docProps/`. Verified on the report shell: 34 of 35 zip
parts stay byte-identical, including `document.xml`, headers, footers and the
embedded logo. Files do get smaller after scrubbing — that is recompression, not
lost content.

## Structure decisions

**Guidelines are a top-level section, not sub-sections of assignments.** They
started embedded under the assignment where each was first applicable, then were
pulled out to `guidelines/` with their own navbar entry and docked sidebar. Each
assignment links to the guidelines it needs under a `## Guidelines` heading, and
`guidelines/index.qmd` lists all twelve. Guide images moved to
`guidelines/images/` and the `tools/` scripts point there.

Placement of each guide (which assignment it belongs to) was decided
deliberately — see the mapping table on `guidelines/index.qmd`. Do not shuffle
without a reason.

**Downloads are only things students fill in or build from.** Anything that was
just prose duplicating a webpage was deleted, since Quarto already offers
PDF/Word/RTF of every page. Nine files remain. The Organizational Assessment
worksheet and grade sheet are *generated* by `build_org_assessment.py` (the
original was 4.6 MB of embedded fonts; these are 36 KB).

One shared `formatted-report-shell.docx` serves both the Practice Report and the
Formatted Report Shell assignments — the two originals differed only in a
placeholder month in the footer.

**Terminology:** "UCA" everywhere (the source guides said "TA"). Submission is
"By Project" / "By Individual". American spellings.

## The Fall 2026 calendar

First day of classes Mon Aug 24. Fall Break Oct 12–13 lands inside Week 8;
Thanksgiving Nov 22–29 is **not** a course week, so Week 14 is the week *after*
it. That makes the 15 weeks land exactly on the Dec 8 last day of classes.

Week *n* Friday deadlines: Aug 28, Sep 4, 11, 18, 25, Oct 2, 9, 16, 23, 30,
Nov 6, 13, 20, then Dec 4, Dec 11. The Final Presentation is the one exception —
submitted Monday Nov 30, presented in class Tuesday Dec 1.

**Due dates are duplicated** in each assignment page and in
`tools/build_calendar.py`, with nothing keeping them in sync. This is the main
known fragility. Options discussed: a Quarto `pre-render` hook, having the
script parse dates out of the `.qmd` files, or a check that fails on mismatch.
Recommended combination is the last two.

## Verification habits that caught real bugs

- Link/anchor checker over rendered `_site/` — caught every dead link after the
  guidelines restructure
- iCalendar parser on the `.ics` rather than eyeballing it — confirmed all timed
  events land Tuesday 15:30–18:15
- Rendering *before* and *after* a whitespace-only change and diffing the HTML
  to prove nothing moved
- Computed-style contrast measurement in a browser, not by inspecting CSS
- Deep scan of every XML part inside every `.docx`, not just the visible text

The browser preview pane intermittently returns blank screenshots. Programmatic
measurement via `javascript_tool` is reliable; fall back to that.

**Do not run two renders at once.** Quarto writes each page next to its source
and then moves it into `_site/`; a second concurrent render moves files out from
under the first, which dies with a confusing `NotFound ... rename` error and
leaves a scatter of `.html`/`.pdf`/`.docx`/`.rtf` beside the `.qmd` files.
`.gitignore` now catches those in the root, `assignments/` and `guidelines/`,
scoped so `assignments/files/` is untouched. A clean re-render tidies them up.

## Small things easily rediscovered as bugs

- The navbar blue `#1A5490` needs the overrides in `styles.css`. Bootstrap's
  default translucent navbar text measures 4.28:1 against it, under the 4.5:1
  AA floor; forcing solid white gives 7.74:1.
- `assignments/index.qmd` emits unused `.pdf`/`.docx`/`.rtf`. Quarto rejects
  `pdf: false`, and `format: html` merges with `_metadata.yml` rather than
  replacing it. Harmless; `format-links: false` hides them.
- SVG in a page that also renders to PDF needs `rsvg-convert`, which is not
  installed locally or in CI. Use PNG.
- `%` in interpolated strings breaks xelatex (it is a comment character) —
  `build_pages.py` has a `pct()` helper for this.
