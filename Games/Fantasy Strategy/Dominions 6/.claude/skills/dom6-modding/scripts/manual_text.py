"""Turn dom6modman.pdf into one searchable text file with one column per page.

  python3 -I manual_text.py [PDF] [OUT]

The manual is laid out in two columns. pdftotext -layout keeps each page's columns side by
side, so this script finds the gap between them on every page and writes the left column
followed by the right column. Then grep for a command, e.g. grep -n -A4 '^#noheal' OUT.
Defaults: ../../../../Manuals/ (the Dominions 6 folder)/dom6modman.pdf and /tmp/dom6modman.txt.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../../Manuals/dom6modman.pdf")
out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dom6modman.txt"

raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
lines_out = []
for page in raw.split("\f"):
    lines = page.split("\n")
    best, best_score = 70, None
    for c in range(55, 95):                      # the column gap: blank in most long lines
        blank = sum(1 for l in lines if len(l) > c + 2 and l[c] == " " and l[c - 1] == " ")
        long_ = sum(1 for l in lines if len(l) > c)
        score = blank - 3 * (long_ - blank)
        if best_score is None or score > best_score:
            best, best_score = c, score
    left = [l[:best].strip() for l in lines]
    right = [l[best:].strip() for l in lines]
    lines_out += [l for l in left if l] + [l for l in right if l]
open(out, "w").write("\n".join(lines_out))
print("wrote", out, len(lines_out), "lines")
