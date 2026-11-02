"""Turn dom6manual.pdf (the game manual, not the modding manual) into two searchable text files.

  python3 -I game_manual_text.py [PDF] [OUTDIR]

Writes, with a "=== page N" line before every page (PDF page numbers match the printed ones):
  OUTDIR/rules.txt   pages 1-98, the two-column rules chapters, one column after the other
  OUTDIR/tables.txt  every page in layout form, so wide tables keep each row on one line:
                     scales (p35, 86), magic items (99-117), battle spells (118-140),
                     summoning rituals (141-207), global enchantments (208-216),
                     other rituals (217-240), nation index with every unit's stats (241-429),
                     launch options (430-433), word index (434-449)
Defaults: ../../../../Manuals/ (the Dominions 6 folder)/dom6manual.pdf and /tmp/dom6manual/.
Then e.g. grep -n -A2 '^Mystic ' OUTDIR/tables.txt, or scripts/lookup.py NAME.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../../Manuals/dom6manual.pdf")
out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dom6manual"
RULES_LAST = 98                                  # page 99 starts the single-column appendix tables

raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
pages = raw.split("\f")


def split_columns(lines):
    """Left column then right column: find the gap that is blank in most long lines."""
    best, best_score = 70, None
    for c in range(55, 95):
        blank = sum(1 for l in lines if len(l) > c + 2 and l[c] == " " and l[c - 1] == " ")
        long_ = sum(1 for l in lines if len(l) > c)
        score = blank - 3 * (long_ - blank)
        if best_score is None or score > best_score:
            best, best_score = c, score
    left = [l[:best].strip() for l in lines]
    right = [l[best:].strip() for l in lines]
    return [l for l in left if l] + [l for l in right if l]


os.makedirs(out, exist_ok=True)
rules, tables = [], []
for n, page in enumerate(pages, 1):
    lines = page.split("\n")
    if n <= RULES_LAST:
        rules += [f"=== page {n}"] + split_columns(lines)
    tables += [f"=== page {n}"] + [l.rstrip() for l in lines if l.strip()]
open(os.path.join(out, "rules.txt"), "w").write("\n".join(rules))
open(os.path.join(out, "tables.txt"), "w").write("\n".join(tables))
print("wrote", os.path.join(out, "rules.txt"), len(rules), "lines and", os.path.join(out, "tables.txt"),
      len(tables), "lines")
