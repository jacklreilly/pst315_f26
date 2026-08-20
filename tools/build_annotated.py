"""Rebuild the annotated executive-summary header example.

Renders the header with xelatex, reads back the exact position of each text line
from the PDF, then draws the instructional callout boxes and leader lines onto a
widened canvas so the labels always point at the right line.
"""
import sys, os, subprocess, tempfile, shutil
sys.path.insert(0, os.path.dirname(__file__))
import fitz
from PIL import Image, ImageDraw, ImageFont
import build_pages as bp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.abspath(os.path.join(HERE, "..", "guidelines", "images"))
BOX  = (58, 63, 42)         # dark olive, as in the original guide
TXT  = (255, 255, 255)
ZOOM = 2.4
PAD_X, PAD_Y = 330, 90

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def build():
    tmp = tempfile.mkdtemp()
    body = bp.TITLE_BLOCK + "\n" + r"\begin{center}\textbf{EXECUTIVE SUMMARY}\end{center}"
    open(os.path.join(tmp, "p.tex"), "w").write(bp.PREAMBLE + body + bp.POSTAMBLE)
    subprocess.run(["/Library/TeX/texbin/xelatex", "-interaction=nonstopmode", "p.tex"],
                   cwd=tmp, capture_output=True, text=True)
    doc = fitz.open(os.path.join(tmp, "p.pdf")); page = doc[0]

    lines = []
    for blk in page.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if txt: lines.append((txt, fitz.Rect(ln["bbox"])))
    lines.sort(key=lambda t: t[1].y0)

    x0 = min(r.x0 for _, r in lines); x1 = max(r.x1 for _, r in lines)
    y0 = min(r.y0 for _, r in lines); y1 = max(r.y1 for _, r in lines)
    pad = 10
    page.set_cropbox(fitz.Rect(x0-pad, y0-pad, x1+pad, y1+pad))
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), alpha=False)
    hdr = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close(); shutil.rmtree(tmp, ignore_errors=True)

    canvas = Image.new("RGB", (hdr.width + 2*PAD_X, hdr.height + 2*PAD_Y), "white")
    canvas.paste(hdr, (PAD_X, PAD_Y))
    dr = ImageDraw.Draw(canvas)
    f = font(19)

    def to_px(rect):
        return (PAD_X + (rect.x0-(x0-pad))*ZOOM, PAD_Y + (rect.y0-(y0-pad))*ZOOM,
                PAD_X + (rect.x1-(x0-pad))*ZOOM, PAD_Y + (rect.y1-(y0-pad))*ZOOM)

    def label(text, anchor_rect, side):
        ax0, ay0, ax1, ay1 = to_px(anchor_rect)
        ay = (ay0 + ay1) / 2
        tw = dr.textbbox((0,0), text, font=f); w = tw[2]-tw[0]; h = tw[3]-tw[1]
        bw, bh = w + 24, h + 18
        if side == "left":
            bx = PAD_X - bw - 34; anchor = (ax0 - 6, ay)
        elif side == "right":
            bx = PAD_X + hdr.width + 34; anchor = (ax1 + 6, ay)
        by = ay - bh/2
        bx = max(6, min(bx, canvas.width - bw - 6))
        dr.rounded_rectangle([bx, by, bx+bw, by+bh], radius=6, fill=BOX)
        dr.text((bx+12, by+9-tw[1]), text, font=f, fill=TXT)
        edge = (bx + bw, ay) if side == "left" else (bx, ay)
        dr.line([edge, anchor], fill=BOX, width=2)

    def label_above(text, anchor_rect, dy=52):
        ax0, ay0, ax1, ay1 = to_px(anchor_rect)
        cx = (ax0+ax1)/2
        tw = dr.textbbox((0,0), text, font=f); w = tw[2]-tw[0]; h = tw[3]-tw[1]
        bw, bh = w+24, h+18
        bx, by = cx-bw/2, ay0-dy-bh
        dr.rounded_rectangle([bx,by,bx+bw,by+bh], radius=6, fill=BOX)
        dr.text((bx+12, by+9-tw[1]), text, font=f, fill=TXT)
        dr.line([(cx, by+bh), (cx, ay0-6)], fill=BOX, width=2)

    def label_below(text, anchor_rect, dy=44):
        ax0, ay0, ax1, ay1 = to_px(anchor_rect)
        cx = (ax0+ax1)/2
        tw = dr.textbbox((0,0), text, font=f); w = tw[2]-tw[0]; h = tw[3]-tw[1]
        bw, bh = w+24, h+18
        bx, by = cx-bw/2, ay1+dy
        dr.rounded_rectangle([bx,by,bx+bw,by+bh], radius=6, fill=BOX)
        dr.text((bx+12, by+9-tw[1]), text, font=f, fill=TXT)
        dr.line([(cx, ay1+6), (cx, by)], fill=BOX, width=2)

    # lines: 0 title, 1 agency, 2 by-author, 3 date, 4 EXECUTIVE SUMMARY
    label_above("Bold heading", lines[0][1], dy=48)
    label("Title of project",  lines[0][1], "left")
    label("Agency name",       lines[1][1], "right")
    label("Your name",         lines[2][1], "left")
    label("Month and year your project is due", lines[3][1], "right")
    gap = fitz.Rect(lines[3][1].x0, lines[3][1].y1, lines[3][1].x1, lines[4][1].y0)
    label("One blank line",    gap, "left")
    label_below("All caps and bold", lines[4][1], dy=40)

    out = os.path.join(OUT, "ex-execsum-header-annotated.png")
    canvas.save(out)
    print(f"  wrote ex-execsum-header-annotated.png ({canvas.width}x{canvas.height})")
    for t, r in lines: print(f"      line: {t[:60]!r}")

if __name__ == "__main__":
    build()
