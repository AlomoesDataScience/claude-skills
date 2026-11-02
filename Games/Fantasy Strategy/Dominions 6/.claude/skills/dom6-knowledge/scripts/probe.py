"""Learn what things on an open game screen are: for each point, hover it and read the tooltip at
the bottom of the screen, then right-click it, read the popup that replaces the screen and close
that popup with its own Exit. Made for the unit stat screen (dom6-knowledge ui/unit-popups.md).

  python3 -I probe.py NAME=X,Y [NAME=X,Y ...] [--no-click] [--json OUT]
  python3 -I probe.py --icons [--gear] [--no-click] [--json OUT]
        the unit screen's icon rows (magic symbols, ability icons; the gear slots too with
        --gear) are swept with the mouse: every change of tooltip is a new icon, so icons that
        touch or overlap are still told apart. Each is then probed

The screen must show a window with an Exit button (unit screen). Stops when a popup does not
close back to the screen it came from. Popup shots go to ~/.cache/dom6ui/probe_<name>.png.
Uses dom6-ui's guard: waits for the user to be idle and works only while the game is focused.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dom6-ui", "scripts"))
import session                                    # noqa: E402
import dom6ui as U                                # noqa: E402
import vision as V                                # noqa: E402
from session import Stop                          # noqa: E402
from PIL import ImageChops, ImageStat             # noqa: E402

TIP_BAND = (0, 930, 1919, 1044)                   # bottom; centred on unit screens, follows the mouse x on the map
PARK = (1300, 110)                                # a blank spot for the mouse (no tooltip)


def diff(a, b, box):
    return ImageStat.Stat(ImageChops.difference(a.convert("L").crop(box), b.convert("L").crop(box))).mean[0]


_TIPS = {}


def tooltip(img):
    """Text of the tooltip box at the bottom centre ("" when there is none). Same box pixels,
    same text: OCR runs once per distinct tooltip."""
    box = tooltip_box(img)
    if not box or box[2] <= box[0] or box[3] <= box[1]:     # map art can fake a frame: no box
        return ""
    key = img.crop(box).tobytes()
    if key not in _TIPS:
        _TIPS[key] = clean_tip(V.ocr(img, [box], [True])[0]["text"])
    return _TIPS[key]


def clean_tip(text):
    """Drop stray 1-2 character tokens at the ends: a tooltip caught while fading in reads as
    "r air mage level 1 i '". Numbers and bracketed values stay."""
    w = text.strip(" |").split()
    keep = lambda t: len(t) > 2 or t.isdigit() or t.startswith("(")
    while w and not keep(w[-1]):
        w.pop()
    while w and not keep(w[0]):
        w.pop(0)
    return " ".join(w)


def tooltip_box(img):
    """The tooltip box: a dark box with a tan frame. Its top and bottom borders are the two
    longest horizontal runs of tan in the band, 25-105 rows apart (two-line tips are ~85)."""
    rgb = img.convert("RGB")
    x0, y0, x1, y1 = TIP_BAND
    px = rgb.load()

    def tan(p):
        return p[0] - p[2] >= 22 and 95 <= sum(p) / 3 <= 200

    runs = []
    for y in range(y0, min(y1, img.height - 3)):
        best, start = (0, 0), None
        for x in range(x0, x1 + 1):
            if x < x1 and tan(px[x, y]):
                if start is None:
                    start = x
            else:
                if start is not None and x - start > best[1] - best[0]:
                    best = (start, x)
                start = None
        if best[1] - best[0] >= 50:
            runs.append((y, best))
    pick = None
    for i, (ya, ra) in enumerate(runs):
        for yb, rb in runs[i + 1:]:
            if 25 <= yb - ya <= 105 and abs(ra[0] - rb[0]) <= 10 and abs(ra[1] - rb[1]) <= 10:
                score = (ra[1] - ra[0]) + (rb[1] - rb[0])
                if pick is None or score > pick[0]:
                    pick = (score, ya, yb, min(ra[0], rb[0]), max(ra[1], rb[1]))
    if not pick:
        return ""
    _, ya, yb, xa, xb = pick
    xm = (xa + xb) // 2                                     # the sides: frame met going out from
    side = lambda p: p[0] - p[2] >= 18 and sum(p) / 3 >= 70  # the middle (text is grey, not tan);
    los, his = [], []                                       # text or the map showing through can
    for ym in range(ya + 6, yb - 5, 3):                     # stop a row early, so take the median
        lo = xm                                             # edge over all rows
        while lo > x0 and not side(px[lo - 1, ym]):
            lo -= 1
        hi = xm
        while hi < x1 - 1 and not side(px[hi + 1, ym]):
            hi += 1
        los.append(lo)
        his.append(hi)
    left, right = sorted(los)[len(los) // 2], sorted(his)[len(his) // 2]
    return (left + 2, ya + 4, right - 1, yb - 3)


def screen_window(sc):
    for w in sc["windows"]:
        for t in w["text"]:
            if t["text"] == "Exit":
                return w, t["box"]
    return None, None


def lines_of(w):
    out = []
    for t in sorted(w["text"] + w["bars"], key=lambda t: (t["box"][1], t["box"][0])):
        if t.get("text") and t["text"] != "Exit":
            out.append(("## " if t in w["bars"] else "") + t["text"])
    return out


def icon_rows(img, sc):
    """The icon rows between the unit screen's stats and its weapon table, as (y0, y1, x0, x1)
    boxes around their ink. Rows are split at blank rows of the edge mask."""
    return [(ya, yb, min(b[0] for b in bs), max(b[2] for b in bs))
            for (ya, yb), bs in _rows_and_parts(img, sc)]


def icon_points(img, sc):
    """Rough icon centres from blank columns alone (gap >= 3 px). Touching icons merge and a
    path symbol's number counts as its own part, so prefer sweep() when the game is live."""
    return [((b[0] + b[2]) // 2, (ya + yb) // 2, b) for (ya, yb), bs in _rows_and_parts(img, sc) for b in bs]


def _rows_and_parts(img, sc):
    T = [t for w in sc["windows"] for t in w["text"]]
    stats = [t["box"][3] for t in T if any(V.closest(t["text"], [k], 0.8) for k in
             ("Morale", "Leadership", "Combat Speed", "XP", "Magic Ldr", "Undead Ldr"))]
    table = [t["box"][1] for t in T if "Len" in t["text"] or V.closest(t["text"], ["Weapon"], 0.8)]
    W, _ = screen_window(sc)
    if not stats or not table or not W:
        return []
    top, bot = max(stats) + 4, min(table) - 4
    x0, x1 = W["box"][0] + 18, W["box"][2] - 18
    E = V.edges(img)
    ep = E.load()
    rgb = img.convert("RGB").load()

    class Ink:                                              # an edge, or a strongly coloured pixel
        def __getitem__(self, xy):                          # (the dark Unhindered Researcher orb
            p = rgb[xy]                                     # has only its red cross)
            return ep[xy] or max(p) - min(p) >= 60
    px = Ink()
    rows, start = [], None
    for y in range(top, bot + 1):
        busy = y < bot and sum(1 for x in range(x0, x1, 2) if px[x, y]) >= 2
        if busy and start is None:
            start = y
        elif not busy and start is not None:
            if y - start >= 8:
                rows.append((start, y))
            start = None
    out = []
    for ya, yb in rows:
        parts = []
        cols = [any(px[x, y] for y in range(ya, yb)) for x in range(x0, x1)]
        x, n = 0, len(cols)
        while x < n:
            if not cols[x]:
                x += 1
                continue
            a = x
            gap = 0
            while x < n and gap < 3:
                gap = gap + 1 if not cols[x] else 0
                x += 1
            b = x - gap
            if b - a >= 6:
                parts.append((x0 + a, ya, x0 + b, yb))
        if parts:
            out.append(((ya, yb), parts))
    return out


def sweep(g, img, sc, step=5, wait=0.08, skip_gear=True):
    """Find the icons by hovering along each icon row every `step` px: each run of one tooltip
    is one icon (a path symbol and its number share a tooltip). Returns [(tooltip, (x, y))]
    with the point in the middle of the run. The gear-slot row is skipped when asked."""
    rows = icon_rows(img, sc)
    if skip_gear and len(rows) > 1:
        rows = rows[1:]
    found = []
    for ya, yb, xa, xb in rows:
        y, run, last = (ya + yb) // 2, None, (None, "")
        for x in range(xa + 2, xb + 1, step):
            g.hover(x, y, wait=wait)
            im = g.grab()
            band = im.crop(TIP_BAND).tobytes()          # unchanged band: same tooltip, no new search
            tip = last[1] if band == last[0] else tooltip(im)
            last = (band, tip)
            if run and tip and (tip in run[0] or run[0] in tip) and x - run[2] <= 4 * step:
                run[0] = min(run[0], tip, key=len)          # same icon (or its number)
                run[2] = x
            elif tip:
                run = [tip, x, x, y]
                found.append(run)
    g.hover(*PARK, wait=0.1)
    return [(t, ((a + b) // 2, y)) for t, a, b, y in found]


def probe(g, points, click=True):
    g.hover(*PARK, wait=0.6)
    base = g.grab()
    sc = V.scene(base)
    W, _ = screen_window(sc)
    if not W and click:
        raise Stop("no window with an Exit on screen")
    UW = W["box"] if W else (0, 0) + base.size                # hover only: any screen will do
    out = []
    for name, (x, y) in points:
        rec = {"name": name, "at": [x, y]}
        g.hover(x, y, wait=1.0)
        rec["tooltip"] = tooltip(g.grab())
        if click:
            g.click(x, y, right=True, wait=1.4)
            pop = g.grab()
            if diff(base, pop, UW) < 4:
                time.sleep(1.2)
                pop = g.grab()
            if diff(base, pop, UW) < 4:
                rec["popup"] = None
            else:
                ps = V.scene(pop)
                w, ex = screen_window(ps)
                if not w:
                    pop.save(os.path.join(U.OUT, "probe_stuck.png"))
                    raise Stop(f"{name}: screen changed but no popup with an Exit")
                safe = "".join(c if c.isalnum() else "_" for c in name.lower())
                pop.save(os.path.join(U.OUT, f"probe_{safe}.png"))
                rec["popup"] = lines_of(w)
                g.click((ex[0] + ex[2]) // 2, (ex[1] + ex[3]) // 2, wait=1.0)
                g.hover(*PARK, wait=0.5)
                if diff(base, g.grab(), UW) > 6:
                    time.sleep(1.0)
                    if diff(base, g.grab(), UW) > 6:
                        raise Stop(f"popup for {name} did not close back to the screen")
        print(f"{name}: tip={rec['tooltip']!r}" + (f"  popup={' | '.join(rec['popup'])[:240]}" if rec.get("popup") else
                                                   ("  popup=none" if click else "")), flush=True)
        out.append(rec)
    return out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    click = "--no-click" not in argv
    js = argv[argv.index("--json") + 1] if "--json" in argv else None
    pts = []
    for a in argv:
        if "=" in a and not a.startswith("--"):
            n, xy = a.rsplit("=", 1)
            x, y = xy.split(",")
            pts.append((n, (int(x), int(y))))
    os.makedirs(U.OUT, exist_ok=True)
    res = []

    def work(g):
        if "--icons" in argv:
            g.hover(*PARK, wait=0.6)
            img = g.grab()
            img.save(os.path.join(U.OUT, "probe_screen.png"))
            found = sweep(g, img, V.scene(img), skip_gear="--gear" not in argv)
            print(f"{len(found)} icons:", [t for t, _ in found], flush=True)
            pts.extend((f"icon{i + 1}@{x},{y}", (x, y)) for i, (_, (x, y)) in enumerate(found))
        res.extend(probe(g, pts, click))

    session.run(work, "probe")
    if js:
        with open(js, "w") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
