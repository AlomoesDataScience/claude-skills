#!/usr/bin/env python3
"""Read a game manual (PDF) as text: pages, chapter outline, search.

  manual.py text PDF [OUT.txt]        whole manual as text, each page starting "=== page N"
                                      (default OUT: next to the PDF, same name .txt; layout kept so
                                      table rows stay on one line)
  manual.py outline PDF [--depth N]   chapter outline: the PDF's bookmarks, or, when it has none,
                                      headings found by font size (bigger than the body text)
  manual.py toc TXT [--pages N]       the printed table of contents: "title ..... page" lines of the
                                      first N pages (default 15) - for manuals without bookmarks
  manual.py grep TXT REGEX [-C N]     matching lines with their page (case-insensitive)
  manual.py page TXT N [M]            pages N..M of the text
  manual.py info PDF                  pages, title, bookmarks or not, text or scanned
  manual.py doc FILE [OUT.txt]        a Word/RTF/ODT rulebook (.doc .docx .rtf .odt) as plain text,
                                      through LibreOffice headless with its own throwaway profile
                                      (never touches the user's LibreOffice settings)

Needs poppler's pdftotext / pdftohtml / pdfinfo. A scanned manual (no text layer) gives empty
pages: `info` says so; read those pages as images instead (pdftoppm, or Read the PDF pages).
"""
import collections
import html
import os
import re
import subprocess
import sys


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def text(pdf, out=None):
    out = out or os.path.splitext(pdf)[0] + ".txt"
    raw = run("pdftotext", "-layout", pdf, "-")
    pages = raw.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    with open(out, "w") as f:
        for i, p in enumerate(pages, 1):
            f.write(f"=== page {i}\n{p.rstrip()}\n\n")
    empty = sum(1 for p in pages if len(p.strip()) < 20)
    print(f"{len(pages)} pages -> {out}" + (f"  ({empty} pages without text: scanned?)" if empty else ""))
    return out


def xml(pdf):
    return run("pdftohtml", "-xml", "-i", "-stdout", "-q", pdf)


def outline(pdf, depth=3):
    x = xml(pdf)
    items = []

    top = re.search(r"<outline>(.*)</outline>", x, re.S)
    if top:
        # nested outlines: indent by how many <outline> tags are open before each item
        lvl = 0
        for tok in re.finditer(r'<outline>|</outline>|<item page="(\d+)">(.*?)</item>', top.group(0), re.S):
            t = tok.group(0)
            if t == "<outline>":
                lvl += 1
            elif t == "</outline>":
                lvl -= 1
            elif lvl <= depth:
                items.append((lvl, int(tok.group(1)), html.unescape(re.sub(r"<[^>]+>", "", tok.group(2))).strip()))
        for lvl, page, title in items:
            print(f"{'  ' * (lvl - 1)}{title}  (p{page})")
        return
    # no bookmarks: headings = text lines in fonts bigger than the body font
    fonts = {m.group(1): float(m.group(2)) for m in re.finditer(r'<fontspec id="(\d+)" size="([\d.]+)"', x)}
    lines = []
    page = 0
    use = collections.Counter()
    for m in re.finditer(r'<page number="(\d+)"|<text [^>]*font="(\d+)"[^>]*>(.*?)</text>', x, re.S):
        if m.group(1):
            page = int(m.group(1))
            continue
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
        if t:
            size = fonts.get(m.group(2), 0)
            use[size] += len(t)
            lines.append((page, size, t))
    if not lines:
        print("no text layer (scanned manual?)")
        return
    body = use.most_common(1)[0][0]
    sizes = sorted({s for s in use if s > body * 1.15}, reverse=True)[:depth]
    rank = {s: i for i, s in enumerate(sizes)}
    last = None
    for page, size, t in lines:
        if size in rank and len(t) > 2 and not t.isdigit():
            key = (page, t)
            if key != last:
                print(f"{'  ' * rank[size]}{t}  (p{page})")
            last = key


def pages_of(txt):
    cur, out = 0, collections.defaultdict(list)
    for line in open(txt, errors="replace"):
        m = re.match(r"=== page (\d+)$", line.rstrip())
        if m:
            cur = int(m.group(1))
        else:
            out[cur].append(line.rstrip("\n"))
    return out


def toc(txt, first=15):
    rx = re.compile(r"^(\s*)(\S.*?\S)\s*(?:\.{2,}|\s{2,}|\s\.\s)\s*(\d{1,3}|[ivxlc]{1,6})\s*$")
    for page, lines in sorted(pages_of(txt).items()):
        if page > first:
            break
        for l in lines:
            m = rx.match(l.replace("\t", "    "))
            if m and not re.search(r"\s{6,}", m.group(2)) and len(m.group(2)) > 2:
                print(f"{' ' * min(8, len(m.group(1)) // 2)}{re.sub(chr(32) + '{2,}', ' ', m.group(2))}  {m.group(3)}")


def grep(txt, rx, ctx=0):
    r = re.compile(rx, re.I)
    for page, lines in sorted(pages_of(txt).items()):
        for i, l in enumerate(lines):
            if r.search(l):
                lo, hi = max(0, i - ctx), min(len(lines), i + ctx + 1)
                for j in range(lo, hi):
                    print(f"p{page}:{j + 1}{':' if j == i else '-'} {lines[j].strip()}")
                if ctx:
                    print("--")


def page(txt, a, b=None):
    P = pages_of(txt)
    for n in range(a, (b or a) + 1):
        print(f"=== page {n}")
        print("\n".join(P.get(n, [])))


def info(pdf):
    print(run("pdfinfo", pdf).strip())
    x = xml(pdf)
    print("bookmarks:", "yes" if "<outline>" in x else "no")
    chars = len(re.sub(r"\s", "", run("pdftotext", "-l", "5", pdf, "-")))
    print("text layer:", "yes" if chars > 200 else f"little or none ({chars} chars on the first 5 pages)")


def doc(path, out=None):
    import shutil
    import tempfile
    out = out or os.path.splitext(path)[0] + ".txt"
    tmp = tempfile.mkdtemp(prefix="manualdoc-")
    try:
        prof = "file://" + os.path.join(tmp, "profile")
        r = subprocess.run(["soffice", f"-env:UserInstallation={prof}", "--headless",
                            "--convert-to", "txt:Text (encoded):UTF8", "--outdir", tmp, path],
                           capture_output=True, text=True, timeout=300)
        made = os.path.join(tmp, os.path.splitext(os.path.basename(path))[0] + ".txt")
        if not os.path.exists(made):
            sys.exit(f"conversion failed: {r.stderr.strip() or r.stdout.strip()}")
        shutil.move(made, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{len(open(out, encoding='utf-8', errors='replace').read().split())} words -> {out}")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "text":
        text(a[1], a[2] if len(a) > 2 else None)
    elif cmd == "outline":
        outline(a[1], int(a[a.index("--depth") + 1]) if "--depth" in a else 3)
    elif cmd == "toc":
        toc(a[1], int(a[a.index("--pages") + 1]) if "--pages" in a else 15)
    elif cmd == "grep":
        grep(a[1], a[2], int(a[a.index("-C") + 1]) if "-C" in a else 0)
    elif cmd == "page":
        page(a[1], int(a[2]), int(a[3]) if len(a) > 3 else None)
    elif cmd == "doc":
        doc(a[1], a[2] if len(a) > 2 else None)
    elif cmd == "info":
        info(a[1])
    else:
        sys.exit(f"unknown command {cmd}\n{__doc__}")


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # quiet when piped into head
    main(sys.argv[1:])
