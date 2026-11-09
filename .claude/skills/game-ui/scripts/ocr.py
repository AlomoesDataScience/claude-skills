#!/usr/bin/env python3
"""Read text from any image or scanned PDF with Tesseract 5 (the NormCap flatpak), any language.

  ocr.py image IMAGE [--box X0 Y0 X1 Y1] [--lang eng] [--psm 6] [--scale 3] [--dark] [--tsv]
        text in an image (a screenshot, a crop); --dark for light text on a dark background,
        --tsv for word boxes and confidence; --scale enlarges small game text first
  ocr.py pdf PDF [OUT.txt] [--lang eng] [--dpi 300] [--first N] [--last M]
        a scanned manual (no text layer) as text, each page starting "=== page N"
  ocr.py langs                          installed languages
  ocr.py getlang LANG [--fast]          download a language (tessdata_best; --fast = smaller)

Languages: eng, jpn (horizontal Japanese), jpn_vert (vertical), osd; join with + (eng+jpn).
Data lives in NormCap's own data folder (~/.var/app/com.github.dynobo.normcap/data/tessdata),
which the flatpak can read. Game text: crop to the text, --scale 3, --psm 7 for one line.
"""
import io
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageOps

APP = "com.github.dynobo.normcap"
DATA = os.path.expanduser(f"~/.var/app/{APP}/data/tessdata")
TESS = ["flatpak", "run", f"--env=TESSDATA_PREFIX={DATA}", "--command=tesseract", APP]


def prepare(img, box=None, scale=3, dark=False):
    img = img.convert("RGB")
    if box:
        img = img.crop(box)
    g = ImageOps.grayscale(img)
    if dark:
        g = ImageOps.invert(g)
    if scale and scale != 1:
        g = g.resize((g.width * scale, g.height * scale), Image.LANCZOS)
    return ImageOps.autocontrast(g)


def ocr(img, lang="eng", psm=6, tsv=False):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    cmd = TESS + ["stdin", "stdout", "-l", lang, "--psm", str(psm)] + (["-c", "tessedit_create_tsv=1"] if tsv else [])  # "tsv" config file is missing in the NormCap tessdata
    r = subprocess.run(cmd, input=buf.getvalue(), capture_output=True, timeout=300)
    if r.returncode:
        sys.exit(r.stderr.decode(errors="replace").strip())
    out = r.stdout.decode("utf-8", errors="replace")
    if "jpn" in lang and not tsv:                 # Tesseract spaces out CJK characters
        cjk = r"[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]"
        out = re.sub(rf"(?<={cjk}) +(?={cjk})", "", out)
    return out


def ocr_pdf(pdf, out=None, lang="eng", dpi=300, first=None, last=None):
    out = out or os.path.splitext(pdf)[0] + ".txt"
    with tempfile.TemporaryDirectory() as d:
        cmd = ["pdftoppm", "-r", str(dpi), "-gray", "-png"]
        if first:
            cmd += ["-f", str(first)]
        if last:
            cmd += ["-l", str(last)]
        subprocess.run(cmd + [pdf, os.path.join(d, "p")], check=True)
        pages = sorted(os.listdir(d), key=lambda f: int(f.split("-")[-1].split(".")[0]))
        with open(out, "w") as f:
            for p in pages:
                n = int(p.split("-")[-1].split(".")[0])
                txt = ocr(Image.open(os.path.join(d, p)), lang, psm=3)
                f.write(f"=== page {n}\n{txt.rstrip()}\n\n")
                print(f"page {n}: {len(txt.split())} words", flush=True)
    print(f"{len(pages)} pages -> {out}")


def opt(a, k, d, n=1):
    if k in a:
        i = a.index(k)
        v = a[i + 1:i + 1 + n]
        return v[0] if n == 1 else v
    return d


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "image":
        box = opt(a, "--box", None, 4)
        img = prepare(Image.open(a[1]), tuple(int(v) for v in box) if box else None,
                      int(opt(a, "--scale", 3)), "--dark" in a)
        print(ocr(img, opt(a, "--lang", "eng"), int(opt(a, "--psm", 6)), "--tsv" in a), end="")
    elif cmd == "pdf":
        out = a[2] if len(a) > 2 and not a[2].startswith("--") else None
        ocr_pdf(a[1], out, opt(a, "--lang", "eng"), int(opt(a, "--dpi", 300)),
                opt(a, "--first", None), opt(a, "--last", None))
    elif cmd == "langs":
        print(subprocess.run(TESS + ["--list-langs"], capture_output=True, text=True).stdout.strip())
    elif cmd == "getlang":
        os.makedirs(DATA, exist_ok=True)
        repo = "tessdata_fast" if "--fast" in a else "tessdata_best"
        url = f"https://github.com/tesseract-ocr/{repo}/raw/main/{a[1]}.traineddata"
        subprocess.run(["curl", "-sSLf", "-o", os.path.join(DATA, a[1] + ".traineddata"), url], check=True)
        print("saved", a[1], "from", repo)
    else:
        sys.exit(f"unknown command {cmd}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv[1:])
