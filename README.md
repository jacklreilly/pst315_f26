# pst315_f26

Course website for **PST 315: Methods of Policy Analysis and Presentation**,
Policy Studies, Syracuse University, Fall 2026.

🔗 <https://jacklreilly.github.io/pst315_f26/>

## Layout

| Path | What's there |
|------|--------------|
| `index.qmd`, `about.qmd` | Landing page and about page |
| `overview.qmd` | Course information, description, objectives, materials |
| `logistics.qmd` | Schedule, assignment structure, evaluation, grading |
| `policies.qmd` | Campus academic policies |
| `syllabus.qmd` | Overview + logistics + policies on one page |
| `assignments/` | 17 assignment pages, plus `files/` (templates students download) |
| `guidelines/` | 12 how-to guides, plus `images/` (worked examples) |
| `tools/` | Python scripts that generate the calendar, example images, and templates |
| `pst315_schedule.ics` | Subscribable course calendar |
| `Prior Assignments/` | Original Word/PowerPoint source. **Gitignored — never commit.** |

## Building

The site is plain [Quarto](https://quarto.org). Render everything with:

```bash
quarto render
```

Output goes to `_site/`. Pushing to `main` triggers
`.github/workflows/publish.yml`, which renders and deploys to `gh-pages`.

Pages render to HTML, PDF, Word, and RTF, so a full render needs LaTeX
(the Action installs TinyTeX).

## Regenerating assets

Nothing in `tools/` runs automatically — run it by hand, then re-render.

```bash
python3 tools/build_calendar.py
```

- `build_calendar.py` — rebuilds `pst315_schedule.ics` from its `CLASSES` and `DUE` tables
- `build_graphs.py`, `build_pages.py`, `build_annotated.py` — regenerate the worked-example images from `swco_data.py`
- `build_org_assessment.py` — regenerates the Organizational Assessment worksheet and grade sheet
- `clean_office_metadata.py` — strips author names from everything in `assignments/files/`

⚠️ Editing any file in `assignments/files/` with Word re-stamps your name into
its metadata. Re-run `clean_office_metadata.py` afterward.

See `NOTES.md` for background on how things are set up and why, and `TODO.md`
for what's still open.
