"""Typeset the worked-example report pages with xelatex and render them to PNG.

Content comes from tools/swco_data.py and is entirely fabricated. Re-run this
script after editing that file to regenerate the images.
"""
import sys, os, subprocess, shutil, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import swco_data as d
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.abspath(os.path.join(HERE, "..", "guidelines", "images"))
XELATEX = "/Library/TeX/texbin/xelatex"

PREAMBLE = r"""
\documentclass[12pt]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{setspace}
\usepackage[normalem]{ulem}
\usepackage{enumitem}
\usepackage{array}
\setlength{\parindent}{0pt}
\setlength{\parskip}{10pt}
\pagestyle{empty}
% report section header: rule / centered bold caps / rule
\newcommand{\secthead}[1]{%
  \par\noindent\rule{\textwidth}{1.2pt}\par\vspace{-6pt}
  \begin{center}\textbf{\MakeUppercase{#1}}\end{center}\vspace{-6pt}
  \noindent\rule{\textwidth}{1.2pt}\par\vspace{6pt}}
\begin{document}
"""
POSTAMBLE = r"\end{document}"

def pct(s):
    """Escape percent signs so LaTeX does not treat them as comments."""
    return str(s).replace("%", r"\%")

def tex_escape(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    return s

def render(body, name, crop=True, zoom=2.0):
    tmp = tempfile.mkdtemp()
    tex = os.path.join(tmp, "p.tex")
    open(tex, "w").write(PREAMBLE + body + POSTAMBLE)
    r = subprocess.run([XELATEX, "-interaction=nonstopmode", "-halt-on-error", "p.tex"],
                       cwd=tmp, capture_output=True, text=True)
    pdf = os.path.join(tmp, "p.pdf")
    if not os.path.exists(pdf):
        print(r.stdout[-2500:]); raise SystemExit(f"xelatex failed for {name}")
    doc = fitz.open(pdf)
    page = doc[0]
    if crop:
        # tighten to the inked area, then add a small white margin
        rect = page.get_bbox() if hasattr(page, "get_bbox") else None
        blocks = page.get_text("blocks") + [tuple(dr["rect"]) + (0,0,0)
                                            for dr in page.get_drawings()]
        if blocks:
            x0 = min(b[0] for b in blocks); y0 = min(b[1] for b in blocks)
            x1 = max(b[2] for b in blocks); y1 = max(b[3] for b in blocks)
            pad = 14
            page.set_cropbox(fitz.Rect(max(0,x0-pad), max(0,y0-pad),
                                       min(page.rect.x1,x1+pad), min(page.rect.y1,y1+pad)))
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    out = os.path.join(OUT, name)
    pix.save(out)
    doc.close(); shutil.rmtree(tmp, ignore_errors=True)
    print(f"  wrote {name}  ({pix.width}x{pix.height})")
    return out

# ---------------------------------------------------------------- content

TITLE_BLOCK = rf"""
\begin{{center}}
\textbf{{{tex_escape(d.AGENCY)} {tex_escape(d.PROJECT)}}}\\
\textbf{{{tex_escape(d.AGENCY)}}}\\
\textbf{{By {tex_escape(d.AUTHOR)}}}\\
\textbf{{{tex_escape(d.DATE)}}}
\end{{center}}
"""

ES_INTRO = (rf"\uline{{\textbf{{Introduction:}}}} This study reports the results of a student "
            rf"satisfaction survey for participants in the site sessions run by the "
            rf"{tex_escape(d.AGENCY)} (SWCO). The study will be presented to the SWCO program "
            rf"director and coaching staff.")

ES_METHODS = (rf"\uline{{\textbf{{Methods:}}}} Data were collected through an online survey "
              rf"distributed to students at the close of each site session. The target population "
              rf"was the {d.TARGET_POPULATION} students who attended a site session during the "
              rf"semester. The survey was distributed to the {d.SAMPLING_FRAME} students present "
              rf"on the day of the survey, and {d.SAMPLE} students responded, yielding a "
              rf"{pct(d.RESPONSE_RATE)} response rate. Because the survey was distributed at the very "
              rf"end of each session, some students may have rushed their responses.")

FINDINGS = [
 f"{d.F1['vals'][2]}\\% of respondents reported that the coaches were helpful. (n={d.F1['n']})",
 f"{d.F2['vals'][1]}\\% of respondents at Site B agreed that the exercises were engaging, "
 f"compared with {d.F2['vals'][0]}\\% at Site A. (n={d.F2['n']})",
 f"{d.F3['vals'][0]}\\% of respondents said more activities would improve the sessions. (n={d.F3['n']})",
 f"{d.F3['vals'][1]}\\% of respondents said the sessions needed more time. (n={d.F3['n']})",
 f"{d.F3['vals'][2]}\\% of respondents said the groups should be smaller. (n={d.F3['n']})",
 "62\\% of respondents reported attending three or more sessions. (n=214)",
 "84\\% of respondents said they would recommend the sessions to a friend. (n=214)",
]

def findings_block():
    items = "\n".join(rf"\item {f}" for f in FINDINGS)
    return (r"\uline{\textbf{Findings:}}" + "\n"
            r"\begin{enumerate}[leftmargin=*,itemsep=6pt,topsep=6pt]" + "\n"
            + items + "\n" + r"\end{enumerate}")

INTRO_PAGE = rf"""
\secthead{{Introduction}}
This study reports the results of a student satisfaction survey for participants in the
site sessions run by the {tex_escape(d.AGENCY)} (SWCO). SWCO is a Syracuse University
program whose mission is to enhance the professional skills of youth in the City of
Syracuse, paving the way for career and personal success. Each semester, SWCO delivers a
series of skill development sessions, known as site sessions, at partner high schools and
community organizations across the city.

The survey was created in collaboration with the SWCO program director. It was designed to
help SWCO understand how students experience the site sessions, which parts of the sessions
students find most valuable, and where students believe the program could improve. The
results of this survey and report will be used by SWCO to plan session content for future
semesters and to guide how coaches are trained and assigned to sites.
"""

METHODS_PAGE = rf"""
\secthead{{Methods}}
\uline{{\textbf{{How Data Were Collected}}}}

\textbf{{Instrument Design:}} The survey used in this study was designed by
{tex_escape(d.AUTHOR)}, a Syracuse University student in the Policy Studies Community Link
Project, in collaboration with the SWCO program director. The survey was created using an
online survey platform.

\textbf{{Data Collection Method:}} The survey link was distributed to students by their
site coaches at the close of each site session. Students accessed the survey by scanning a
QR code displayed at the end of the session. Responses were recorded automatically by the
survey platform and later exported for analysis.

\textbf{{Target Population and Sample:}} The target population includes all
{d.TARGET_POPULATION} students who attended at least one site session during the semester.
The survey was distributed to the {d.SAMPLING_FRAME} students present on the day of the
survey, making the sampling frame {d.SAMPLING_FRAME} students. The sample consists of
{d.SAMPLE} respondents, yielding a {pct(d.RESPONSE_RATE)} response rate.

\uline{{\textbf{{Quality of the Data}}}}

\textbf{{Representativeness:}} Representativeness may have been affected by the fact that
the survey was distributed only to students present on a single day. Students who attended
sessions earlier in the semester but were absent on the survey day had no opportunity to
respond, and attendance was not evenly distributed across the three sites.

\textbf{{Accuracy:}} Because the survey was distributed in the final minutes of each
session, some students may have rushed their answers. Students also completed the survey in
the presence of their coaches, which may have encouraged more positive responses than
students would have given anonymously.
"""

EXEC_PAGE = TITLE_BLOCK + "\n" + r"\begin{center}\textbf{EXECUTIVE SUMMARY}\end{center}" + "\n\n" \
            + ES_INTRO + "\n\n" + ES_METHODS + "\n\n" + findings_block()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render(TITLE_BLOCK + "\n" + r"\begin{center}\textbf{EXECUTIVE SUMMARY}\end{center}",
           "ex-execsum-header.png")
    render(ES_INTRO,   "ex-execsum-intro.png")
    render(ES_METHODS, "ex-execsum-methods.png")
    render(findings_block(), "ex-execsum-findings.png")
    render(EXEC_PAGE,  "ex-execsum-full.png", crop=False, zoom=1.6)
    render(INTRO_PAGE, "ex-intro-page.png",   crop=False, zoom=1.6)
    render(METHODS_PAGE, "ex-methods-page.png", crop=False, zoom=1.6)
