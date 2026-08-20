"""Strip identifying metadata from every downloadable Office file.

The originals carried real students' and staff members' full names in
docProps/core.xml and docProps/app.xml, which are invisible in the document body
but one click away in Word's Properties pane. Re-run after adding any new file.
"""
import zipfile, shutil, re, os, glob

# Tags appear with or without a namespace prefix (dc:, cp:, ap:) depending on
# which Word wrote the file, so every pattern is matched prefix-agnostically.
FIELDS_CORE = {"creator":"PST 315","lastModifiedBy":"PST 315","description":"",
               "keywords":"","category":"","contentStatus":"","subject":"",
               "lastPrinted":"","identifier":"","title":""}
FIELDS_APP  = {"Company":"Syracuse University","Manager":"","HyperlinkBase":""}

def scrub(path):
    z = zipfile.ZipFile(path); names = z.namelist()
    parts = {}
    for n in names:
        data = z.read(n)
        if n in ("docProps/core.xml","docProps/app.xml"):
            txt = data.decode("utf8","ignore")
            table = FIELDS_CORE if n.endswith("core.xml") else FIELDS_APP
            for tag, val in table.items():
                txt = re.sub(rf"(<(?:\w+:)?{tag}(?:\s[^>]*)?>)(.*?)(</(?:\w+:)?{tag}>)",
                             rf"\1{val}\3", txt, flags=re.S)
            data = txt.encode("utf8")
        parts[n] = data
    z.close()
    tmp = path + ".tmp"
    zo = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for n in names: zo.writestr(n, parts[n])
    zo.close(); shutil.move(tmp, path)

def report(path):
    z = zipfile.ZipFile(path)
    out = {}
    for n in ("docProps/core.xml","docProps/app.xml"):
        if n in z.namelist():
            t = z.read(n).decode("utf8","ignore")
            for tag in ("creator","lastModifiedBy","Company"):
                m = re.search(rf"<(?:\w+:)?{tag}(?:\s[^>]*)?>(.*?)</(?:\w+:)?{tag}>", t, re.S)
                if m: out[tag] = m.group(1).strip()
    return out

if __name__ == "__main__":
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assignments", "files")
    for f in sorted(glob.glob(os.path.join(d, "*"))):
        before = report(f); scrub(f); after = report(f)
        print(f"  {os.path.basename(f):<44} {str(before)[:56]:<58} -> {after}")
