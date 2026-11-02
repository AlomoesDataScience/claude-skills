"""Download the Dominions 6 Mod Inspector (larzm42.github.io/dom6inspector) and store everything
it shows as local files in ../data.

  python3 -I build.py [--work DIR] [--no-images]

Needs git and firefox (headless). Steps:
  1. clone (or update) github.com/larzm42/dom6inspector into WORK/repo
  2. serve it locally with dump.js injected; headless firefox runs the site's own code, which
     prepares the data exactly as the site does (gold costs, recruit lists, spell effects...) and
     posts every object's detail page and computed fields back to this script
  3. write data/pages/<kind>.txt (each object's page as text, descriptions included),
     data/records/<kind>.jsonl (computed fields), data/gamedata/*.csv (the site's raw tables),
     data/images/ (unit sprites, item and site icons) and data/VERSION
"""
import html as htmlmod
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REPO_URL = "https://github.com/larzm42/dom6inspector.git"
KINDS = ["units", "spells", "items", "weapons", "armor", "sites", "mercs", "events", "nations"]


# ------------------------------------------------------------------ html page -> text
class PageText(HTMLParser):
    """Turns an inspector overlay into lines: one per table row ("label: value [key]  (breakdown)"),
    with the internal key rows folded into the row above."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.cur, self.cells, self.cell = [], [], None, None
        self.row_title, self.skip = None, 0

    def text(self, s):
        if self.skip:
            return
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.cur.append(s)

    def flush(self):
        t = " ".join("".join(self.cur).split())
        if t:
            self.lines.append(t)
        self.cur = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        cls = a.get("class") or ""
        if tag in ("script", "style"):
            self.skip += 1
        elif tag == "tr":
            if self.cells is not None:                   # the site sometimes opens a row without closing the last
                self.end_row()
            self.flush()
            self.cells, self.row_title = [], a.get("title")
        elif tag in ("td", "th") and self.cells is not None:
            self.cell = []
        elif tag in ("p", "div", "br", "h2", "h3", "h4", "table", "li"):
            if self.cells is None:
                self.flush()
        elif tag == "span" and "abilityicon" in cls and a.get("title"):
            self.text(f"({a['title']})")
        elif tag == "img" and a.get("src", "").startswith("images/") and "Pin" not in a.get("src", ""):
            if "sprites/" in a["src"] or "items/" in a["src"] or "sites/" in a["src"]:
                self.flush()
                self.lines.append(f"image: {a['src']}")
            elif a.get("title") or a.get("alt"):
                self.text(a.get("title") or a.get("alt"))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        elif tag in ("td", "th") and self.cell is not None:
            self.cells.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.cells is not None:
            self.end_row()
        elif tag in ("p", "div", "h2", "h3", "h4", "table", "li") and self.cells is None:
            self.flush()

    def end_row(self):
        raw, self.cells = self.cells, None
        cells = [c for c in raw if c]
        if not cells:
            return
        if tag_only(cells) and self.lines:              # "[key]" row: belongs to the row above
            self.lines[-1] += " " + cells[0]
            return
        if raw[0].endswith(":"):                         # "label: value"
            line = " ".join(cells)
        else:                                            # a table row: keep empty cells so columns line up
            while raw and not raw[-1]:
                raw.pop()
            line = " | ".join(raw)
        if self.row_title and self.row_title.strip() and not self.row_title.strip().isdigit():
            line += "   (" + " ".join(self.row_title.split()) + ")"
        self.lines.append(line)

    def handle_data(self, d):
        self.text(d)

    def close(self):
        super().close()
        if self.cells is not None:
            self.end_row()
        self.flush()


def tag_only(cells):
    return len(cells) == 1 and re.fullmatch(r"\[[^\]]+\]", cells[0])


def page_text(h):
    p = PageText()
    p.feed(h)
    p.close()
    out = []
    for l in p.lines:
        l = l.replace("\xa0", " ").strip()
        if re.fullmatch(r"Modded \[modded\] \S Modded \[modded\] \S", l):    # the site's show/hide toggle
            l = "mod lines [modded]:"
        if l:
            out.append(l)
    return "\n".join(out)


def descr_name(name):
    return re.sub(r"[^a-zA-Z0-9\-]", "", name) + ".txt"


def read_descr(repo, sub, fname):
    p = os.path.join(repo, "gamedata", sub, fname)
    if os.path.exists(p):
        return " ".join(open(p, encoding="utf-8", errors="replace").read().split())
    return ""


# ------------------------------------------------------------------ dump via headless firefox
def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


HOLD = 300          # seconds the page may take to load, prepare and post everything


def dump(repo, out, query="loadEvents=1"):
    """Render the site in headless firefox and save what dump.js posts into OUT. QUERY is the
    page's query string; add mod=<file>.dm (repeatable, files in REPO/mods/) to load mods."""
    page = open(os.path.join(repo, "index.html"), encoding="utf-8").read()
    page = re.sub(r"<script[^>]*googletagmanager[^<]*</script>", "", page)
    page = re.sub(r"<script>\s*window.dataLayer.*?</script>", "", page, flags=re.S)
    page, n = re.subn(r'(<script[^>]*src="scripts/main\.js[^"]*"></script>)', r'\1\n<script src="dump.js"></script>', page)
    if not n:
        sys.exit("index.html no longer loads scripts/main.js: dump.js needs a new hook")
    page = page.replace("</body>", '<img src="/hold" style="display:none"></body>')
    open(os.path.join(repo, "index_dump.html"), "w", encoding="utf-8").write(page)
    shutil.copy(os.path.join(HERE, "dump.js"), os.path.join(repo, "dump.js"))

    done = threading.Event()

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=repo, **k)

        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path.startswith("/hold"):             # keeps the page "loading" until the dump is in
                done.wait(HOLD)
                self.send_response(204)
                self.end_headers()
                return
            return super().do_GET()

        def do_POST(self):
            kind = self.path.rsplit("/", 1)[-1]
            body = self.rfile.read(int(self.headers["Content-Length"]))
            open(os.path.join(out, kind + ".json"), "wb").write(body)
            print(f"  got {kind} ({len(body) // 1000} KB)", flush=True)
            self.send_response(204)
            self.end_headers()
            if kind in ("done", "error"):
                done.set()

    port = free_port()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = tempfile.mkdtemp(prefix="ffprof-")
    shot = os.path.join(out, "shot.png")
    subprocess.run(["firefox", "--headless", "--no-remote", "--profile", prof, "--window-size", "1400,900",
                    "--screenshot", shot, f"http://127.0.0.1:{port}/index_dump.html?{query}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=HOLD + 120)
    srv.shutdown()
    shutil.rmtree(prof, ignore_errors=True)
    if os.path.exists(os.path.join(out, "error.json")):
        sys.exit("dump.js failed: " + open(os.path.join(out, "error.json")).read())
    if not os.path.exists(os.path.join(out, "done.json")):
        sys.exit(f"the page never finished within {HOLD} s and reported no error (a mod may stop the site's "
                 "parser silently; try the mods one at a time)")


# ------------------------------------------------------------------ write the data folder
def header(kind, d):
    name = d.get("fullname") or d.get("name") or d.get("nationname") or ""
    if kind == "nations":
        name = f"{d.get('eracode', '')} {d.get('name', '')}, {d.get('epithet', '')}".strip()
    return f"=== {kind[:-1] if kind.endswith('s') else kind} {d.get('id')}: {name}"


def descriptions(repo, kind, d):
    out = []
    if kind == "units":
        t = d.get("descr") or read_descr(repo, "unitdescr", "%04d.txt" % int(d["id"]))
        if t:
            out.append("description: " + t)
    elif kind == "spells":
        for pre, lab in (("", "description"), ("details", "details"), ("portent", "portent"), ("cure", "cure")):
            t = read_descr(repo, "spelldescr", descr_name(pre + d.get("name", "")))
            if t:
                out.append(f"{lab}: {t}")
    elif kind == "items":
        t = d.get("descr") or read_descr(repo, "itemdescr", descr_name(d.get("name", "")))
        if t:
            out.append("description: " + t)
    elif d.get("description") or d.get("descr"):
        out.append("description: " + " ".join(str(d.get("description") or d.get("descr")).split()))
    return out


NATION_LISTS = [("commanders", "commanders"), ("units", "units"), ("capcommanders", "capital-only commanders"),
                ("capunits", "capital-only units"), ("foreigncommanders", "foreign commanders"),
                ("foreignunits", "foreign units"), ("landcom", "land commanders (water nations)"),
                ("landunit", "land units (water nations)"), ("uwcom", "underwater commanders"), ("uwunit", "underwater units"),
                ("coastcom", "coast commanders"), ("coastrec", "coast units"), ("forestcom", "forest commanders"),
                ("forestrec", "forest units"), ("mountaincom", "mountain commanders"), ("mountainrec", "mountain units"),
                ("swampcom", "swamp commanders"), ("swamprec", "swamp units"), ("wastecom", "waste commanders"),
                ("wasterec", "waste units"), ("cavecom", "cave commanders"), ("caverec", "cave units"),
                ("plainscom", "plains commanders"), ("plainsrec", "plains units"), ("futurecapcommanders", "future capital commanders"),
                ("futurecapunits", "future capital units"), ("heroes", "heroes"), ("multiheroes", "multiheroes"),
                ("pretenders", "pretenders"), ("addgod", "extra pretenders"), ("delgod", "removed pretenders"),
                ("sites", "start sites"), ("futuresites", "future sites")]


def nation_lists(d, names):
    """The nation's recruit lists, heroes, pretenders and sites, which the site shows in its grid."""
    out = []
    for key, label in NATION_LISTS:
        ids = [x["id"] if isinstance(x, dict) else x for x in d.get(key) or [] if x is not None]
        if ids:
            book = names["sites"] if "sites" in key else names["units"]
            byname = {str(v).lower(): k for k, v in book.items()}
            parts = []
            for i in ids:
                if str(i) in book:
                    parts.append(f"#{i} {book[str(i)]}")
                elif str(i).lower() in byname:              # mods give start sites by name
                    parts.append(f"#{byname[str(i).lower()]} {book[byname[str(i).lower()]]}")
                else:
                    parts.append(f"{i} (not found)")
            out.append(f"{label}: " + ", ".join(parts))
    if d.get("spells"):
        out.append("national spells: " + ", ".join(f"#{x['id']} {x['name']}" for x in d["spells"] if x))
    if d.get("homerealm"):
        out.append("home realms: " + ", ".join(sorted(set(map(str, d["homerealm"])))))
    return out


def write_data(repo, dumpdir, images, data=DATA, note="", raw=True):
    """Write pages/, records/, gamedata/ (raw) and images/ (images) into DATA from a dump."""
    DATA = data
    for sub in ("pages", "records") + (("gamedata",) if raw else ()):
        shutil.rmtree(os.path.join(DATA, sub), ignore_errors=True)
        os.makedirs(os.path.join(DATA, sub))
    counts, names = {}, {}
    for kind in KINDS:
        objs = json.load(open(os.path.join(dumpdir, kind + ".json")))
        names[kind] = {str(o["data"].get("id")): o["data"].get("fullname") or o["data"].get("name") for o in objs}
        counts[kind] = len(objs)
        with open(os.path.join(DATA, "pages", kind + ".txt"), "w", encoding="utf-8") as f, \
             open(os.path.join(DATA, "records", kind + ".jsonl"), "w", encoding="utf-8") as g:
            for o in objs:
                d = o["data"]
                body = page_text(o["html"])
                f.write(header(kind, d) + "\n" + body + "\n")
                if kind == "nations":
                    f.write("".join(l + "\n" for l in nation_lists(d, names)))
                for line in descriptions(repo, kind, d):
                    f.write(line + "\n")
                f.write("\n")
                g.write(json.dumps(d, ensure_ascii=False) + "\n")
    for fn in os.listdir(os.path.join(repo, "gamedata")) if raw else []:
        if fn.endswith(".csv"):
            shutil.copy(os.path.join(repo, "gamedata", fn), os.path.join(DATA, "gamedata", fn))
    if images:
        shutil.rmtree(os.path.join(DATA, "images"), ignore_errors=True)
        for sub in ("sprites", "items", "sites"):
            shutil.copytree(os.path.join(repo, "images", sub), os.path.join(DATA, "images", sub))
    rev = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%H %ci %s"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(DATA, "VERSION"), "w") as f:
        f.write(f"source: {REPO_URL}\ncommit: {rev}\n")
        f.write("counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + "\n" + note)
    print("wrote", os.path.abspath(DATA), counts)


WORK = os.path.join(tempfile.gettempdir(), "dom6inspector-build")


def ensure_repo(work, update=True):
    """Clone the site into WORK/repo, or update it; returns the repo path."""
    os.makedirs(work, exist_ok=True)
    repo = os.path.join(work, "repo")
    if os.path.isdir(os.path.join(repo, ".git")):
        if update:
            subprocess.run(["git", "-C", repo, "pull", "-q", "--ff-only"], check=True)
    else:
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO_URL, repo], check=True)
    return repo


def main():
    args = sys.argv[1:]
    work = args[args.index("--work") + 1] if "--work" in args else WORK
    repo = ensure_repo(work)
    dumpdir = os.path.join(work, "dump")
    shutil.rmtree(dumpdir, ignore_errors=True)
    os.makedirs(dumpdir)
    print("rendering the site headless...")
    dump(repo, dumpdir)
    write_data(repo, dumpdir, "--no-images" not in args)


if __name__ == "__main__":
    main()
