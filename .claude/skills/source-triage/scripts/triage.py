#!/usr/bin/env python3
"""Rate the documents in a game folder (and its install) by what they are good for.

  triage.py GAME_FOLDER [--install DIR ...] [--md]     table of every document with a guessed ROLE
  --md prints a SOURCES.md skeleton (Claude finishes the judgement column by reading each doc).

Roles (guessed from name, size, pages, version and readability - always check by opening the doc):
  CORE       the main rules manual (most pages, current version)
  UPDATE     what's new / readme / patch notes - OVERRIDE the manual where they differ; newest wins
  KEYS       hotkey / command lists - read FIRST (learn-to-play)
  GUIDE      primers, tutorials, how-tos for play
  EDITOR     modding / editor / database guides (learn-to-mod)
  DATA       big tables or lists (equipment, units) - look-up only
  OLDER      a previous game version's manual - only where the new one is silent; mark as old
  DUPLICATE  same document in another format (keep the best readable one)
  BROKEN     cannot be opened / no text (fix or ignore)
  ADVERT     catalogues, marketing - ignore
  OTHER      look at it
Pure standard library + pdfinfo/pdftotext if installed."""
import os, re, subprocess, sys

DOC = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".chm", ".hlp", ".htm", ".html", ".md", ".odt", ".epub"}
SKIP = {"__pycache__", ".git", ".claude", "redist", "Graphics", "Sound", "Languages", "Old Languages", "My Fonts",
        "Scenarios", "Graphics Override", "AutoPlay", "pfx"}


def pdf_pages(p):
    try:
        out = subprocess.run(["pdfinfo", p], capture_output=True, text=True, timeout=20)
        m = re.search(r"^Pages:\s+(\d+)", out.stdout, re.M)
        return int(m.group(1)) if m else -1          # -1 = pdfinfo failed: damaged
    except Exception:
        return None


def role(name, ext, pages, size):
    n = name.lower()
    if pages == -1:
        return "BROKEN"
    if re.search(r"catalog|catalogue|brochure", n):
        return "ADVERT"
    if re.search(r"key ?commands|hotkey|keys|shortcut|quick ?ref", n):
        return "KEYS"
    if re.search(r"what'?s ?new|whatsnew|readme|read ?me|changelog|patch|update|czytaj", n):
        return "UPDATE"
    if re.search(r"\bedit|editor|modding|recolou?r|bmp|scenario ?design|database|how ?to", n):
        return "EDITOR"
    if re.search(r"primer|tutorial|guide|walkthrough|hints|tips", n):
        return "GUIDE"
    if re.search(r"list|table|scenario descriptions", n) or (ext in (".rtf", ".txt") and size > 3_000_000):
        return "DATA"
    if re.search(r"manual|rules|rulebook", n) or (pages or 0) >= 80:
        return "CORE"
    return "OTHER"


def scan(dirs):
    rows = []
    for top in dirs:
        for dp, dn, fn in os.walk(top):
            dn[:] = [d for d in dn if d not in SKIP and not d.startswith(".")]
            for f in fn:
                ext = os.path.splitext(f)[1].lower()
                if ext not in DOC or f.startswith("~$"):
                    continue
                p = os.path.join(dp, f)
                size = os.path.getsize(p)
                pages = pdf_pages(p) if ext == ".pdf" else None
                rows.append(dict(path=p, top=top, name=f, ext=ext, size=size, pages=pages,
                                 role=role(f, ext, pages, size)))
    # version tags: an older major version of the game -> OLDER
    vers = [int(m.group(1)) for r in rows for m in [re.search(r"toaw ?(\d)|v(\d)\b|(\d)\.\d", r["name"].lower())] if m and m.group(1)]
    for r in rows:
        m = re.search(r"toaw ?(\d)", r["name"].lower())
        if m and vers and int(m.group(1)) < max(vers + [4]) and r["role"] in ("CORE", "OTHER", "DATA"):
            r["role"] = "OLDER"
    # duplicates: same stem, other format or other folder - keep pdf with text > docx > doc > rest
    pref = {".pdf": 0, ".docx": 1, ".txt": 2, ".doc": 3, ".rtf": 4}
    by = {}
    for r in rows:
        by.setdefault(re.sub(r"[^a-z0-9]", "", os.path.splitext(r["name"].lower())[0]), []).append(r)
    for stem, rs in by.items():
        if len(rs) > 1:
            rs.sort(key=lambda r: (r["role"] == "BROKEN", pref.get(r["ext"], 9), -r["size"]))
            for r in rs[1:]:
                if r["role"] not in ("BROKEN", "ADVERT") and not (r["ext"] == ".txt" and r["top"] == rs[0]["top"]):
                    r["role"] = "DUPLICATE"
                    r["of"] = os.path.relpath(rs[0]["path"], rs[0]["top"])
    return rows


ORDER = ["KEYS", "UPDATE", "CORE", "GUIDE", "EDITOR", "DATA", "OLDER", "OTHER", "DUPLICATE", "BROKEN", "ADVERT"]


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    dirs = [a[0]] + [a[i + 1] for i, x in enumerate(a) if x == "--install"]
    rows = sorted(scan(dirs), key=lambda r: (ORDER.index(r["role"]), r["name"]))
    if "--md" in a:
        print("# Sources - what each document is good for\n")
        print("Made with source-triage (`triage.py`); roles checked by opening each document. Read order: KEYS, UPDATE,")
        print("CORE (by chapter as needed), GUIDE; EDITOR for modding; OLDER only where the current manual is silent.\n")
        print("| Role | Document | Where | Pages/size | Verdict (Claude, after opening it) |")
        print("|---|---|---|---|---|")
    for r in rows:
        where = "install" if r["top"] != dirs[0] else os.path.relpath(os.path.dirname(r["path"]), dirs[0])
        ps = f"{r['pages']} p" if r["pages"] and r["pages"] > 0 else f"{r['size'] // 1024} KB"
        extra = f" (copy of {r['of']})" if r.get("of") else ""
        if "--md" in a:
            print(f"| {r['role']} | {r['name']}{extra} | {where} | {ps} | |")
        else:
            print(f"{r['role']:9} {ps:>9}  {where:20.20} {r['name']}{extra}")


if __name__ == "__main__":
    main()
