"""Enable and disable Dominions 6 mods in the running game (main menu > Mods), and read which
mods are enabled.

  python3 -I mods.py status                  enabled mods, from ~/.dominions6/dom6config (no input)
  python3 -I mods.py installed [TEXT]        every mod the game lists, from disk (no input)
  python3 -I mods.py list                    read the game's Mods screen: every row and its tick
  python3 -I mods.py enable NAME [NAME...]   tick these mods
  python3 -I mods.py disable NAME [NAME...]  untick these mods
  python3 -I mods.py only NAME [NAME...]     exactly these mods enabled
  python3 -I mods.py none                    "Disable all mods"

NAME is the name the game lists (the .dm's #modname; mods in ~/.dominions6/mods get "(local)"),
or the .dm file or folder name, or a part of the name that only one mod has. Several mods share
a name ("One Age vSCBM (6.30 Zemaitia)"): add #2, #3 for the 2nd, 3rd row of that name.

The game must be on the main menu. The script opens Mods, ticks and unticks rows (clicking on
the name's text), checks every tick, presses Escape back to the main menu (that is when the game
writes dom6config) and prints the enabled mods from the file. Uses the dom6ui guard: waits for
the user to be idle and works only while the game is focused.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import textmatch as T  # noqa: E402
import vision as V  # noqa: E402
from session import Stop, on_text, run, same, says  # noqa: E402

CONFIG = os.path.expanduser("~/.dominions6/dom6config")
LOCAL = os.path.expanduser("~/.dominions6/mods")
WORKSHOP = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/2511500")
TEXT_X = (775, 1205)          # the name column of the Mods list
TICK_X = (1212, 1255)         # the green tick of an enabled mod
ROWS_Y = (56, 974)
KEY = 0x4F                    # dom6config strings are XORed with 0x4F


# ---------------------------------------------------------------- dom6config

def _xstr(d, i):
    j = d.index(KEY, i)                       # the NUL terminator, XORed
    return bytes(b ^ KEY for b in d[i:j]).decode("latin-1"), j + 1


def read_config(path=CONFIG):
    """(workshop folder, [(dm file, folder), ...] enabled). The file holds a few ints, the
    workshop path, a count, and per enabled mod its .dm name and folder, all strings XOR 0x4F."""
    d = open(path, "rb").read()
    i = d.index(bytes(c ^ KEY for c in b"/"))
    workshop, i = _xstr(d, i)
    n = int.from_bytes(d[i:i + 4], "little")
    i += 4
    mods = []
    for _ in range(n):
        f, i = _xstr(d, i)
        folder, i = _xstr(d, i)
        mods.append((f, folder))
    return workshop, mods


# ---------------------------------------------------------------- mods on disk

def modname(path):
    try:
        with open(path, encoding="latin-1") as fh:
            for line in fh:
                m = re.match(r'\s*#modname\s+"([^"]*)"', line.lstrip("\u00ef\u00bb\u00bf"))   # skip a UTF-8 BOM
                if m:
                    return m.group(1)
    except OSError:
        pass
    return os.path.basename(path)


def installed():
    """[{name, shown, file, folder, path, local}] in the game's list order: by #modname, ignoring
    case, a local copy before a workshop copy of the same name."""
    out = []
    for p in sorted(glob.glob(os.path.join(LOCAL, "*", "*.dm"))):
        n = modname(p)
        out.append(dict(name=n, shown=n + "  (local)", file=os.path.basename(p),
                        folder=os.path.basename(os.path.dirname(p)), path=p, local=True))
    try:
        ws = read_config()[0] or WORKSHOP
    except (OSError, ValueError):
        ws = WORKSHOP
    for p in sorted(glob.glob(os.path.join(ws, "*", "*.dm"))):
        n = modname(p)
        out.append(dict(name=n, shown=n, file=os.path.basename(p),
                        folder=os.path.dirname(p), path=p, local=False))
    return sorted(out, key=lambda m: (m["name"].lower(), not m["local"]))


def describe(f, folder, mods):
    for m in mods:
        if m["file"] == f and (m["folder"] == folder or os.path.basename(m["folder"]) == os.path.basename(folder)):
            return f'{m["shown"]}   [{m["path"]}]'
    return f"{f}  (folder {folder}; not found on disk)"


def resolve(names, mods):
    """User NAMEs -> indexes into MODS (the game's row order)."""
    shown = [m["shown"] for m in mods]
    out = []
    for raw in names:
        name, nth = raw, None
        m = re.match(r"(.*)#(\d+)$", raw)
        if m:
            name, nth = m.group(1).rstrip(), int(m.group(2))
        if name in shown:
            rows = [i for i, x in enumerate(shown) if x == name]
        else:
            low = name.lower()
            rows = [i for i, x in enumerate(mods)
                    if low in (x["file"].lower(), x["file"].lower()[:-3], os.path.basename(x["folder"]).lower())]
            if not rows:
                rows = [i for i, x in enumerate(mods) if low in x["shown"].lower()]
            if len({shown[i] for i in rows}) > 1:
                sys.exit(f"{raw!r} matches several mods: " + "; ".join(sorted({shown[i] for i in rows})))
            if rows and nth is None and len(rows) == 1:
                out.append(rows[0])
                continue
            rows = [i for i, x in enumerate(shown) if rows and x == shown[rows[0]]]
        if not rows:
            sys.exit(f"no installed mod matches {raw!r} (mods.py installed lists them)")
        if nth is None and len(rows) > 1:
            sys.exit(f"{len(rows)} mods are called {shown[rows[0]]!r}: say which with #1..#{len(rows)} "
                     f"or give the .dm file name; rows: " + ", ".join(mods[i]["path"] for i in rows))
        if nth is not None and not 1 <= nth <= len(rows):
            sys.exit(f"there are {len(rows)} mods called {shown[rows[0]]!r}, not {nth}")
        out.append(rows[(nth or 1) - 1])
    return out


# ---------------------------------------------------------------- the Mods screen

def ticked(im, y):
    n = 0
    for x in range(*TICK_X):
        for yy in range(y - 9, y + 10, 2):
            r, g, b = im.getpixel((x, yy))[:3]
            if g > 120 and g > r + 50 and g > b + 50:
                n += 1
    return n >= 6


class Screen:
    """The Mods list. Rows are placed in the known list order (MODS) by voting: every row read
    clearly gives the page's offset, so a row whose name is too close to another one (v1.08 /
    v1.09) still gets its place."""

    def __init__(self, g, mods):
        self.g, self.mods = g, mods
        self.shown = [m["shown"] for m in mods]
        self.names = sorted(set(self.shown) | {"Exit"})
        self.size = None

    def box(self, y):
        return (TEXT_X[0], y - 13, TEXT_X[1], y + 13)

    def read(self, im):
        """[(y, name or None, ticked)] of the visible rows."""
        ys = T.lines(im, TEXT_X[0], TEXT_X[1] - 10, *ROWS_Y)
        if V.tesseract_ok():                                # all rows in one OCR call
            reads = V.ocr(im, [self.box(y) for y in ys], [True] * len(ys))
            return [(y, V.closest(r["text"], self.names, limit=0.85, margin=0.03), ticked(im, y))
                    for y, r in zip(ys, reads)]
        out = []
        for y in ys:
            sizes = None if self.size is None else (self.size - 0.25, self.size, self.size + 0.25)
            r = T.match(im, self.box(y), self.names, sizes=sizes)
            name = None
            if r and r[0][0] <= 0.3 and (len(r) == 1 or r[1][0] - r[0][0] >= 0.04):
                name = r[0][1]
                if self.size is None:
                    self.size = r[0][2]
            out.append((y, name, ticked(im, y)))
        return out

    def place(self, rows):
        """{row number on the page: index in MODS} by the offset most clear rows agree on."""
        votes = {}
        for i, (y, name, _) in enumerate(rows):
            for j, s in enumerate(self.shown):
                if s == name:
                    votes[j - i] = votes.get(j - i, 0) + 1
        if not votes:
            return {}
        off, n = max(votes.items(), key=lambda kv: kv[1])
        if n < 2:
            return {}
        return {i: off + i for i in range(len(rows)) if 0 <= off + i < len(self.mods)
                and rows[i][1] != "Exit"}

    def is_row(self, im, y, j):
        r = T.match(im, self.box(y), [self.shown[j]])
        return bool(r) and r[0][0] <= 0.32

    def open(self):
        g = self.g
        im = g.grab()
        if not says(im, (780, 392, 960, 414), "Create World", light=False):
            g.grab("not_main_menu")
            raise Stop("the game is not on the main menu; bring it there first")
        g.key("m", wait=1.5)
        g.scroll(False, 80, wait=0.8)
        g.hover(200, 1000, wait=0.3)
        if not any(n for _, n, _ in self.read(g.grab())):
            g.grab("no_mod_list")
            raise Stop("the Mods screen did not open")

    def walk(self, visit):
        """Page through the list from the top; VISIT(im, rows, placed) on each page (it returns
        True to stop early). Returns the set of MODS indexes seen."""
        g, seen, prev = self.g, set(), None
        for _ in range(40):
            g.hover(200, 1000, wait=0.25)
            im = g.grab()
            rows = self.read(im)
            placed = self.place(rows)
            if not placed:
                g.grab("lost")
                raise Stop("could not tell which mods this page of the list shows")
            seen.update(placed.values())
            if visit(im, rows, placed):
                break
            if prev is not None and same(prev, im, (650, 50, 1270, 975)):
                break
            prev = im
            g.scroll(True, 10)
        return seen

    def close(self):
        self.g.key("Escape", wait=1.5)
        if not says(self.g.grab(), (780, 392, 960, 414), "Create World", light=False):
            self.g.grab("not_back")
            raise Stop("Escape did not go back to the main menu")


def toggle(g, im, y, want):
    x, _ = on_text(im, (TEXT_X[0], y - 13, TEXT_X[1], y + 13))
    for dx in (0, 12):
        g.click(x + dx, y, wait=0.8)
        g.hover(200, 1000, wait=0.3)
        now = g.grab()
        if ticked(now, y) == want:
            return now
    g.grab("tick_failed")
    raise Stop("the click did not change the mod's tick")


def change(g, mods, on, off, only=False):
    """Tick the MODS indexes ON, untick OFF (with ONLY: untick every other one)."""
    on, off = set(on), set(off)
    sc = Screen(g, mods)
    sc.open()
    done = set()

    def visit(im, rows, placed):
        for i, j in placed.items():
            y, _, t = rows[i]
            want = True if j in on else False if (j in off or only) else None
            if want is None or j in done:
                continue
            if t != want:
                if not sc.is_row(im, y, j):
                    g.grab("row_mismatch")
                    raise Stop(f"the row at y {y} should be {sc.shown[j]!r} but does not read so")
                im = toggle(g, im, y, want)
            done.add(j)
        return not only and (on | off) <= done

    seen = sc.walk(visit)
    sc.close()
    missing = (on | off) - seen
    if missing:
        print("NOT FOUND in the game's list: " + ", ".join(mods[j]["shown"] for j in sorted(missing)))
    if only and len(seen) != len(mods):
        print(f"  note: the game lists {len(seen)} rows here, {len(mods)} mods are on disk")


def disable_all(g, mods):
    sc = Screen(g, mods)
    sc.open()
    g.scroll(True, 80, wait=0.8)
    g.hover(200, 1000, wait=0.3)
    im = g.grab()
    btn = [y for y in T.lines(im, TEXT_X[0], TEXT_X[1] - 10, 860, ROWS_Y[1])        # "Disable all mods (N enabled)"
           if (lambda r: r and r[0][0] <= 0.3)(T.match(im, (790, y - 13, 1130, y + 13), ["Disable all mods"], prefix=True))]
    if not btn:
        g.grab("no_disable_all")
        raise Stop("could not find 'Disable all mods'")
    g.click(*on_text(im, (790, btn[0] - 13, 1130, btn[0] + 13)), wait=1.0)
    sc.close()


# ---------------------------------------------------------------- main

def print_status(mods):
    ws, en = read_config()
    print(f"{len(en)} mods enabled (dom6config):" if en else "no mods enabled (dom6config)")
    for f, folder in en:
        print("  " + describe(f, folder, mods))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    mods, cmd, names = installed(), a[0], a[1:]
    if cmd == "status":
        print_status(mods)
    elif cmd == "installed":
        en = {(f, os.path.basename(d)) for f, d in read_config()[1]}
        for m in mods:
            if not names or names[0].lower() in m["shown"].lower():
                on = (m["file"], os.path.basename(m["folder"])) in en
                print(f'{"*" if on else " "} {m["shown"]:<52} {m["path"]}')
        print("(* = enabled)")
    elif cmd == "list":
        def work(g):
            sc = Screen(g, mods)
            sc.open()
            state = {}

            def visit(im, rows, placed):
                for i, j in placed.items():
                    state[j] = (rows[i][2], rows[i][1] == sc.shown[j])
            sc.walk(visit)
            sc.close()
            for j, m in enumerate(mods):
                t, read = state.get(j, (None, False))
                mark = "?" if t is None else "*" if t else " "
                print(f'{mark} {m["shown"]:<52}{"" if read else "  (placed by order)"}')
            print("(* = ticked, ? = not seen)")
        run(work, "mods")
    elif cmd in ("enable", "disable", "only"):
        if not names:
            sys.exit(f"{cmd}: name at least one mod")
        targets = resolve(names, mods)
        run(lambda g: change(g, mods, targets if cmd != "disable" else [],
                             targets if cmd == "disable" else [], only=cmd == "only"), "mods")
        print_status(mods)
    elif cmd == "none":
        run(lambda g: disable_all(g, mods), "mods")
        print_status(mods)
    else:
        sys.exit(f"unknown command {cmd!r}; see --help")


if __name__ == "__main__":
    main()
