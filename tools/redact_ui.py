"""Clean the two Excel UI screenshots.

codebook-7 and codebook-8 are genuine macOS Excel screenshots, so they are kept
rather than recreated - but they leak real client data. codebook-7 shows
respondent-level gender/age/race columns behind the menu plus the author's device
name; codebook-8 shows a real client workbook filename. Both are cropped and
painted over here.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.abspath(os.path.join(HERE, "..", "guidelines", "images"))

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

# ---- codebook-7: crop away the data columns, cover the device name ----------
im = Image.open(os.path.join(IMG, "codebook-7.png")).convert("RGB")
im = im.crop((258, 20, 542, 740))                   # keep the context menu only
dr = ImageDraw.Draw(im)
dr.rectangle([2, 512, im.width-2, 550], fill=(246, 246, 246)) # "Sophie's iPhone" row
dr.text((16, 520), "iPhone", font=font(20), fill=(170, 170, 170))
im.save(os.path.join(IMG, "codebook-7.png"))
print(f"  codebook-7 cleaned -> {im.size}")

# ---- codebook-8: replace the real workbook name, trim the bleed-through -----
im = Image.open(os.path.join(IMG, "codebook-8.png")).convert("RGB")
im = im.crop((0, 0, 576, 728))                      # trim right-edge response text
dr = ImageDraw.Draw(im)
dr.rectangle([64, 152, 528, 188], fill=(255, 255, 255))       # filename field
dr.text((76, 160), "Survey Responses.xlsx", font=font(20), fill=(0, 0, 0))
im.save(os.path.join(IMG, "codebook-8.png"))
print(f"  codebook-8 cleaned -> {im.size}")
