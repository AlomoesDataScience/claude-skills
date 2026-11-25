"""licensecheck.py - find and name the licences in a folder or a GitHub repo before we use or ship anything.

Usage:
  python3 -I licensecheck.py scan DIR              licence files + SPDX tags under DIR, a verdict per licence
  python3 -I licensecheck.py nuget PROJECT_DIR     licences of the NuGet packages the .csproj files under it use
                                                   (read from ~/.nuget/packages: local, no web)
  python3 -I licensecheck.py github OWNER/REPO     one API call for the repo's licence, one for .gitmodules,
                                                   one per GitHub submodule (each URL printed first)

It names licences by their wording (MIT, BSD, Apache, GPL, ...). It does not decide anything: the SKILL.md
table says what each one asks of a release, and the user rules on anything unclear. Run with no arguments
for this help.
"""
import json, os, re, sys, urllib.request, urllib.error
import xml.etree.ElementTree as ET

NAMES = re.compile(r"^(licen[sc]e|copying|notice|unlicense|copyright|third[-_ ]party)", re.I)
# wording -> SPDX id; the more specific first
SIGNS = [
    # 2026-11-22: the GNU family moved to gnu_name() below. These rows matched anywhere in the text, and every
    # GNU licence names its siblings (GPL-2's preamble and last paragraph name the "GNU Library General Public
    # License", GPL-3 names the Lesser GPL), so plain GPL-2 (EasyABC) came out as LGPL-2.1. Kept, not used:
    # ("AGPL-3.0", [r"GNU AFFERO GENERAL PUBLIC LICENSE"]),
    # ("LGPL-3.0", [r"GNU LESSER GENERAL PUBLIC LICENSE", r"Version 3"]),
    # ("LGPL-2.1", [r"GNU (LESSER|LIBRARY) GENERAL PUBLIC LICENSE"]),
    # ("GPL-3.0", [r"GNU GENERAL PUBLIC LICENSE", r"Version 3"]),
    # ("GPL-2.0", [r"GNU GENERAL PUBLIC LICENSE", r"Version 2"]),
    ("MPL-2.0", [r"Mozilla Public License,? (Version|v\.?) ?2\.0"]),
    ("Apache-2.0", [r"Apache License", r"Version 2\.0"]),
    ("BSD-3-Clause", [r"Redistribution and use in source and binary forms", r"(Neither the name|names of its contributors)"]),
    ("BSD-2-Clause", [r"Redistribution and use in source and binary forms"]),
    ("MIT", [r"Permission is hereby granted, free of charge"]),
    ("Zlib", [r"provided 'as-is', without any express or implied", r"altered source versions must be plainly marked"]),
    ("ISC", [r"Permission to use, copy, modify, and(/or)? distribute this software for any purpose"]),
    ("Unlicense", [r"This is free and unencumbered software released into the public domain"]),
    ("CC0-1.0", [r"CC0 1\.0|Creative Commons Zero"]),
    ("CC-BY-NC", [r"Attribution-NonCommercial|CC BY-NC"]),
    ("CC-BY-SA", [r"Attribution-ShareAlike|CC BY-SA"]),
    ("CC-BY", [r"Creative Commons Attribution|CC BY \d"]),
    ("MS-PL", [r"Microsoft Public License"]),
    ("BSL-1.0", [r"Boost Software License"]),
]
# short verdicts for an itch.io binary release; SKILL.md has the full table
VERDICT = {
    "MIT": "ok - ship the notice", "BSD-2-Clause": "ok - ship the notice", "BSD-3-Clause": "ok - ship the notice, no endorsement",
    "Zlib": "ok - mark changed source", "ISC": "ok - ship the notice", "BSL-1.0": "ok - notice with source copies",
    "Apache-2.0": "ok - ship LICENSE + NOTICE, mark changes", "MS-PL": "ok - ship the notice",
    "Unlicense": "ok - nothing required", "CC0-1.0": "ok - nothing required", "CC-BY": "ok - credit the author",
    "MPL-2.0": "care - changed MPL files stay MPL, source offered", "LGPL-2.1": "care - dynamic link only, relinkable, source offered",
    "LGPL-3.0": "care - dynamic link only, relinkable, source offered",
    "LGPL-2.0": "care - dynamic link only, relinkable, source offered", "LGPL-unknown": "care - LGPL, version unread; read it yourself",
    "GPL-1.0": "STOP - whole game would be GPL; ask the user", "GPL-unknown": "STOP - GPL, version unread; ask the user",
    "GPL-2.0": "STOP - whole game would be GPL; ask the user", "GPL-3.0": "STOP - whole game would be GPL; ask the user",
    "AGPL-3.0": "STOP - ask the user", "CC-BY-SA": "care - derived assets share-alike; ask the user",
    "CC-BY-NC": "STOP - no commercial use; ask the user", "unknown": "read it yourself", "none": "STOP - no licence = all rights reserved",
}
CODE_EXT = {".c", ".cc", ".cpp", ".h", ".hpp", ".cs", ".py", ".js", ".ts", ".rs", ".go", ".java", ".lua", ".mr", ".glsl", ".hlsl"}
UA = "AI-Development-workspace-licensecheck"


GNU_TITLE = re.compile(r"GNU\s+(AFFERO\s+|LESSER\s+|LIBRARY\s+)?GENERAL\s+PUBLIC\s+LICEN[SC]E", re.I)


def gnu_name(t):
    """A GNU licence by its title: the first GNU licence name in the text and the version right after it.
    The title comes before any mention of a sibling licence. None when no GNU title is found."""
    m = GNU_TITLE.search(t)
    if not m:
        return None
    kind = (m.group(1) or "").strip().upper()
    v = re.search(r"Version\s+(\d)(\.\d)?", t[m.end():m.end() + 200], re.I)
    ver = (v.group(1) + (v.group(2) or "")) if v else ""
    major = ver[:1]
    if kind == "AFFERO":
        return "AGPL-3.0"
    if kind in ("LESSER", "LIBRARY"):
        return "LGPL-3.0" if major == "3" else "LGPL-2.1" if ver == "2.1" else "LGPL-2.0" if major == "2" else "LGPL-unknown"
    return {"1": "GPL-1.0", "2": "GPL-2.0", "3": "GPL-3.0"}.get(major, "GPL-unknown")


def name_text(t):
    g = gnu_name(t)
    if g:
        return g
    for spdx, pats in SIGNS:
        if all(re.search(p, t, re.I) for p in pats):
            return spdx
    return "unknown"


def scan(root):
    found, spdx_tags, code_dirs = [], {}, set()
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in (".git", "node_modules", "bin", "obj", "__pycache__"))
        for f in sorted(files):
            p = os.path.join(d, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXT:
                code_dirs.add(os.path.relpath(d, root).split(os.sep)[0])
            if NAMES.match(f) and os.path.getsize(p) < 2_000_000:
                with open(p, errors="replace") as fh:
                    found.append((os.path.relpath(p, root), name_text(fh.read())))
            elif ext in CODE_EXT and os.path.getsize(p) < 1_000_000:
                with open(p, errors="replace") as fh:
                    head = fh.read(4000)
                m = re.search(r"SPDX-License-Identifier:\s*([\w.\-+ ()]+)", head)
                if m:
                    spdx_tags.setdefault(m.group(1).strip(), []).append(os.path.relpath(p, root))
    print(f"# licence files under {root}")
    for p, n in found:
        print(f"{n:14} {VERDICT.get(n, 'read it yourself'):48} {p}")
    if not found:
        print(f"none            {VERDICT['none']}")
    for tag, ps in sorted(spdx_tags.items()):
        print(f"SPDX {tag:9} {len(ps)} files, e.g. {ps[0]}")
    covered = {p.split(os.sep)[0] for p, _ in found}
    bare = sorted(x for x in code_dirs if x != "." and x not in covered and "." not in covered)
    if bare:
        print("# top-level folders with code and no licence file of their own (check what covers them):")
        for x in bare:
            print("  " + x)


def nuget(proj):
    cache = os.path.expanduser("~/.nuget/packages")
    refs = set()
    for d, dirs, files in os.walk(proj):
        dirs[:] = [x for x in dirs if x not in (".git", "bin", "obj")]
        for f in files:
            if f.endswith(".csproj"):
                for r in ET.parse(os.path.join(d, f)).getroot().iter("PackageReference"):
                    refs.add((r.get("Include"), r.get("Version")))
    print("# direct NuGet packages (their own dependencies come too: check the build output with scan)")
    for name, ver in sorted(refs):
        pdir = os.path.join(cache, name.lower(), ver or "")
        spec = os.path.join(pdir, name.lower() + ".nuspec")
        lic = "not in cache"
        if os.path.exists(spec):
            t = open(spec, errors="replace").read()
            m = re.search(r"<license type=\"(\w+)\"[^>]*>([^<]+)</license>", t)
            u = re.search(r"<licenseUrl>([^<]+)</licenseUrl>", t)
            lic = f"{m.group(2)} ({m.group(1)})" if m else (f"url {u.group(1)}" if u else "not stated")
        print(f"{name} {ver}: {lic}")


def get(url, raw=False):
    print("GET", url, flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def github(repo):
    def lic(rp):
        code, body = get(f"https://api.github.com/repos/{rp}/license")
        if code == 404:
            return "none"
        if code != 200:
            sys.exit(f"HTTP {code}: stopping (failure protocol: no resend)")
        return (json.loads(body).get("license") or {}).get("spdx_id") or "unknown"
    n = lic(repo)
    print(f"{repo}: {n} - {VERDICT.get(n, 'read it yourself')}")
    code, body = get(f"https://api.github.com/repos/{repo}/contents/.gitmodules", raw=True)
    if code not in (200, 404):
        sys.exit(f"HTTP {code}: stopping")
    for url in re.findall(r"url\s*=\s*(\S+)", body):
        m = re.match(r"https?://github\.com/([^/]+/[^/.]+)", url)
        if not m:
            print(f"  submodule {url}: not on GitHub, check by hand")
            continue
        s = lic(m.group(1))
        print(f"  submodule {m.group(1)}: {s} - {VERDICT.get(s, 'read it yourself')}")
    print("Note: the API reads only the root LICENSE. Clone the pinned commit and run scan on it before use.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "scan":
        scan(a[1])
    elif len(a) == 2 and a[0] == "nuget":
        nuget(a[1])
    elif len(a) == 2 and a[0] == "github" and re.fullmatch(r"[\w.-]+/[\w.-]+", a[1]):
        github(a[1])
    else:
        print(__doc__)
