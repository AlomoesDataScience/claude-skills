"""Fetch the Dominions 6 Pretenders Calculator's data (zollqir.github.io/pretenders-dom6) into ../data.

  python3 -I update.py [--work DIR]

Clones or pulls github.com/zollqir/pretenders-dom6 (default work dir <tmp>/pretenders-dom6-build),
copies its data files and reads the data kept in its JavaScript (bless list, per-nation pretender
removals and scale fixes) as plain literals, without running any of the site's code. Needs git.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
REPO_URL = "https://github.com/zollqir/pretenders-dom6"
FILES = ["pretenders.json", "pretender_costs.json", "nations.json", "nations_pretenders.json"]
JS = {  # output file: (module, the literal starts after this text)
    "blesses.json": ("src/App/BlessEffects/getBlessEffects.js", "const blessData ="),
    "pretenders_to_remove.json": ("src/getNations/pretendersToRemove.js", "const pretendersToRemove ="),
    "nation_scales_to_fix.json": ("src/getNations/nationScalesToFix.js", "const nationScalesToFix ="),
}


def js_literal(text, start):
    """The JavaScript object/array literal after START in TEXT, as Python data (comments dropped,
    bare keys quoted, trailing commas removed). Raises if it is not a plain literal."""
    i = text.index(start) + len(start)
    while text[i] in " \t\r\n":
        i += 1
    out, depth, j = [], 0, i
    while True:
        c = text[j]
        if c in "\"'":                                   # string: copy as a JSON string
            k = j + 1
            while text[k] != c:
                k += 2 if text[k] == "\\" else 1
            out.append(json.dumps(text[j + 1:k].replace("\\" + c, c)))
            j = k + 1
            continue
        if text.startswith("//", j):
            j = text.index("\n", j)
            continue
        if text.startswith("/*", j):
            j = text.index("*/", j) + 2
            continue
        m = re.match(r"[A-Za-z_$][\w$]*", text[j:])
        if m:
            word = m.group(0)
            if word in ("true", "false", "null"):
                out.append(word)
            elif re.match(r"\s*:", text[j + len(word):]):
                out.append(json.dumps(word))
            else:
                raise ValueError(f"not a plain literal near {text[j:j + 40]!r}")
            j += len(word)
            continue
        out.append(c)
        if c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    s = re.sub(r",(\s*[\]}])", r"\1", "".join(out))
    return json.loads(s)


def main():
    a = sys.argv[1:]
    work = a[a.index("--work") + 1] if "--work" in a else os.path.join(tempfile.gettempdir(), "pretenders-dom6-build")
    os.makedirs(work, exist_ok=True)
    repo = os.path.join(work, "repo")
    if os.path.isdir(os.path.join(repo, ".git")):
        subprocess.run(["git", "-C", repo, "pull", "-q", "--ff-only"], check=True)
    else:
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO_URL, repo], check=True)
    os.makedirs(DATA, exist_ok=True)
    for fn in FILES:
        shutil.copy(os.path.join(repo, "src", "data", fn), os.path.join(DATA, fn))
    for out, (mod, start) in JS.items():
        data = js_literal(open(os.path.join(repo, mod), encoding="utf-8").read(), start)
        json.dump(data, open(os.path.join(DATA, out), "w"), indent=0)
    commit = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%H %ci"], capture_output=True, text=True).stdout.strip()
    version = open(os.path.join(repo, "src", "version.js")).read().split('"')[1]
    with open(os.path.join(DATA, "VERSION"), "w") as f:
        f.write(f"source: {REPO_URL} (site version {version})\ncommit: {commit}\nfetched: {time.strftime('%Y-%m-%d')}\n")
    print(f"wrote {DATA}: site version {version}, commit {commit}")


if __name__ == "__main__":
    main()
