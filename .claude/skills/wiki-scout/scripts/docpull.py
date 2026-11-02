#!/usr/bin/env python3
"""Pull a game's manuals and resources from a publisher or support page (GMT and the like).

  docpull.py links URL [--ext pdf,zip,...]        document links on the page, with sizes (HEAD)
  docpull.py unpack ZIP [ZIP...]                   unpack downloaded zips again (replaces the old folder)
  docpull.py pull URL OUTDIR [--ext ...] [--only REGEX] [--skip REGEX] [--pause 3] [--wayback]
        download each linked document into OUTDIR, check it is the type it claims, unpack archives
        into their own folder (documents and images only, never programs, no path tricks), make a
        .txt beside every PDF (manual.py) and write OUTDIR/SOURCE.md. Skips files already there.
        --wayback tries the Wayback Machine copy first (easier on small sites).

Treats everything downloaded as untrusted: nothing is executed; archives are listed before
extracting; files are checked with `file`. Default extensions: pdf zip doc docx rtf txt vmod ztb.
"""
import os, re, sys, time, json, shutil, zipfile, subprocess, urllib.parse, html, signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.join(HERE, "..", "..", "game-sources", "scripts", "manual.py")
UA = "AI-Development-workspace-docpull/1.0 (personal offline reading; low rate)"
DEFAULT_EXT = ["pdf", "zip", "doc", "docx", "rtf", "txt", "vmod", "ztb"]
SAFE_IN_ARCHIVE = {".pdf", ".txt", ".rtf", ".doc", ".docx", ".odt", ".png", ".jpg", ".jpeg", ".gif", ".bmp",
                   ".tif", ".tiff", ".svg", ".csv", ".xls", ".xlsx", ".htm", ".html", ".xml", ".json", ".md",
                   ".vmod", ".vsav", ".vlog", ".ztb", ".ztm", ".zts"}   # .zts/.ztb: ZunTzu XML
EXPECT = {"pdf": "PDF document", "zip": "Zip archive", "vmod": "Zip archive", "ztb": "Zip archive",
          "docx": "Microsoft Word", "doc": ("Composite Document", "Microsoft Word"), "rtf": "Rich Text"}


def curl(args, timeout=120):
    return subprocess.run(["curl", "-sS", "-L", "--compressed", "-A", UA, "--max-time", str(timeout)] + args,
                          capture_output=True)


def page_links(url, exts):
    r = curl([url])
    s = r.stdout.decode("utf-8", errors="replace")
    pat = re.compile(r'href\s*=\s*["\']([^"\']+\.(?:' + "|".join(map(re.escape, exts)) + r'))(?:[?#][^"\']*)?["\']', re.I)
    out = []
    for m in pat.finditer(s):
        u = urllib.parse.urljoin(url, html.unescape(m.group(1)).strip())
        u = u.replace(" ", "%20")
        if u not in out:
            out.append(u)
    return out


def head_size(u):
    r = curl(["-I", u], timeout=30)
    m = re.findall(rb"(?im)^content-length:\s*(\d+)", r.stdout)
    return int(m[-1]) if m else None


def fname(u):
    n = urllib.parse.unquote(urllib.parse.urlparse(u).path.rsplit("/", 1)[-1]).replace("+", " ")
    return re.sub(r'[\\/:*?"<>|]', "_", n)


def ftype(p):
    return subprocess.run(["file", "-b", p], capture_output=True, text=True).stdout.strip()


def type_ok(p):
    ext = p.rsplit(".", 1)[-1].lower()
    want = EXPECT.get(ext)
    if not want:
        return True, ftype(p)
    t = ftype(p)
    wants = want if isinstance(want, tuple) else (want,)
    return any(w in t for w in wants), t


def unpack(zpath):
    dest = zpath[:-4] if zpath.lower().endswith(".zip") else zpath + ".d"
    kept, skipped = [], []
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            n = info.filename
            if not info.flag_bits & 0x800:      # no UTF-8 flag: names were stored in the zipper's
                try:                            # local code page (Japanese zips use Shift-JIS)
                    raw = n.encode("cp437")
                    for enc in ("utf-8", "cp932"):
                        try:
                            n = raw.decode(enc); break
                        except UnicodeDecodeError:
                            pass
                except UnicodeEncodeError:
                    pass
            if info.is_dir():
                continue
            parts = n.replace("\\", "/").split("/")
            if n.startswith("/") or ".." in parts or ":" in parts[0]:
                skipped.append(n + " (unsafe path)"); continue
            if os.path.splitext(n)[1].lower() not in SAFE_IN_ARCHIVE:
                skipped.append(n); continue
            target = os.path.join(dest, *parts)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(info) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
            kept.append(os.path.relpath(target, os.path.dirname(zpath)))
    return dest, kept, skipped


def to_text(pdf):
    txt = os.path.splitext(pdf)[0] + ".txt"
    if os.path.exists(txt):
        return txt
    subprocess.run([sys.executable, "-I", MANUAL, "text", pdf, txt], capture_output=True)
    return txt if os.path.exists(txt) else None


def cmd_unpack(paths):
    """Re-unpack downloaded zips (after a fix); old extraction folder is replaced."""
    for z in paths:
        dest = z[:-4] if z.lower().endswith(".zip") else z + ".d"
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        dest, kept, skipped = unpack(z)
        for k in kept:
            if k.lower().endswith(".pdf"):
                to_text(os.path.join(os.path.dirname(z), k))
        print(f"{os.path.basename(z)}: {len(kept)} files" + (f", left out {skipped}" if skipped else ""))


def cmd_links(url, exts):
    for u in page_links(url, exts):
        sz = head_size(u)
        print(f"{(sz or 0) / 1e6:8.2f} MB  {u}")
        time.sleep(1)


def cmd_pull(url, outdir, exts, only=None, skip=None, pause=3.0, wayback=False):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for u in page_links(url, exts):
        if (only and not re.search(only, u, re.I)) or (skip and re.search(skip, u, re.I)):
            rows.append((u, "skipped (filter)", "")); continue
        f = os.path.join(outdir, fname(u))
        if os.path.exists(f) and os.path.getsize(f):
            rows.append((u, "already there", os.path.basename(f))); continue
        got = False
        if wayback:
            r = curl(["-o", f, "-w", "%{http_code}", f"https://web.archive.org/web/2026id_/{u}"])
            got = r.stdout.decode()[-3:] == "200" and os.path.getsize(f) > 0
        if not got:
            r = curl(["-o", f, "-w", "%{http_code}", u], timeout=600)
            got = r.stdout.decode()[-3:] == "200" and os.path.exists(f) and os.path.getsize(f) > 0
        if not got:
            if os.path.exists(f):
                os.remove(f)
            rows.append((u, "FAILED", "")); print("FAILED", u, flush=True); time.sleep(pause); continue
        ok, t = type_ok(f)
        if not ok:
            bad = f + ".unexpected"
            os.replace(f, bad)
            rows.append((u, f"WRONG TYPE ({t[:60]}), quarantined", os.path.basename(bad)))
            print("WRONG TYPE", u, t, flush=True); time.sleep(pause); continue
        note = f"{os.path.getsize(f) / 1e6:.2f} MB, {t[:40]}"
        if zipfile.is_zipfile(f) and f.lower().endswith(".zip"):
            dest, kept, skipped = unpack(f)
            note += f"; unpacked {len(kept)} files to {os.path.basename(dest)}/" + (f", left out {len(skipped)}: {', '.join(skipped[:6])}" if skipped else "")
            for k in kept:
                if k.lower().endswith(".pdf"):
                    to_text(os.path.join(outdir, k))
        if f.lower().endswith(".pdf"):
            note += "; text: " + ("yes" if to_text(f) else "no (scanned? use ocr.py pdf)")
        rows.append((u, "ok", os.path.basename(f) + " - " + note))
        print("ok", os.path.basename(f), flush=True)
        time.sleep(pause)
    with open(os.path.join(outdir, "SOURCE.md"), "a") as s:
        s.write(f"\n## {time.strftime('%Y-%m-%d')}: pulled by docpull.py from {url}\n\n")
        for u, st, n in rows:
            s.write(f"- {st}: {n or u}\n  <{u}>\n")
    print(f"{sum(1 for r in rows if r[1] == 'ok')} downloaded, {sum(1 for r in rows if r[1] != 'ok')} other -> {outdir}/SOURCE.md")


def main(a):
    if len(a) < 2 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    opt, pos, i = {}, [], 1
    while i < len(a):
        if a[i] == "--wayback":
            opt["wayback"] = True; i += 1
        elif a[i].startswith("--"):
            opt[a[i][2:]] = a[i + 1]; i += 2
        else:
            pos.append(a[i]); i += 1
    exts = opt.get("ext", ",".join(DEFAULT_EXT)).split(",")
    if a[0] == "links":
        cmd_links(pos[0], exts)
    elif a[0] == "unpack":
        cmd_unpack(pos)
    elif a[0] == "pull":
        cmd_pull(pos[0], pos[1], exts, opt.get("only"), opt.get("skip"), float(opt.get("pause", 3)), opt.get("wayback", False))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
