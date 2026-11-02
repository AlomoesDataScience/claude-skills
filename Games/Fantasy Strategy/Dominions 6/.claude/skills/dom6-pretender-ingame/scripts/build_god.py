"""Build a pretender in the running Dominions 6 through Game Tools > Create a Pretender God, from a
design checked by the dom6-pretender calculator, and save it (it then shows in View Created
Pretenders and in every new game's pretender screen with Ctrl+L).

  python3 -I build_god.py NATION GOD [DESIGN] [--bless "Name,Name x2"] [--name "God name"]
                          [--mod DIR] [--cost ID=N] [--no-save] [--dry]
  python3 -I build_god.py --save-current [--name "God name"]   save the design open in the game

NATION, GOD and DESIGN (--paths --dom --scales --prison) are the dom6-pretender `build` options.
--name     the god's name (default: the game's random one)
--no-save  stop on the finished design screen without saving (the user can look, change, save)
--dry      check the design with the calculator and print the plan; no input to the game

Start with the game on the main menu or the Game Tools menu. Every step reads the screen back
(text matched against the game's own font) and stops if it does not see what it expects; the
screenshots of each stage go to ~/.cache/dom6ui/. Input goes through the dom6-ui skill's guard:
it waits until the user is idle, works only while the game window is focused, and gives focus and
the mouse pointer back at the end.
"""
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SKILLS, "dom6-ui", "scripts"))
sys.path.insert(0, os.path.join(SKILLS, "dom6-pretender", "scripts"))

from PIL import Image  # noqa: E402

import pretender as P  # noqa: E402
import textmatch as T  # noqa: E402
import vision as V  # noqa: E402
from session import Game6, Stop, on_text, run, same, says  # noqa: E402

INSPECTOR_SPRITES = os.path.join(SKILLS, "dom6-inspector", "data", "images", "sprites")
NEWLORDS = os.path.expanduser("~/.dominions6/savedgames/newlords")
ERA_Y = {"EA": 202, "MA": 373, "LA": 531}
PATH_X = dict(zip(P.PATHS, (711, 765, 817, 868, 920, 973, 1024, 1077, 1130)))   # magic icons
DOM_X = {"dom": 710, "order": 772, "productivity": 823, "heat": 877, "growth": 925, "fortune": 980, "magic": 1033}
HEADER = (50, 49, 49)            # design screen panel header bars
CELL_X = [403 + 122 * j for j in range(10)]


def on_sprite(im, cx, cy, half=48):
    """The sprite pixel nearest the centre of the form cell at CX,CY (hovering the cell's empty
    background shows no tooltip), or None for an empty cell."""
    from PIL import ImageChops, ImageFilter
    cell = im.crop((cx - half, cy - half, cx + half, cy + half)).convert("RGB")
    bg = tuple(sorted(cell.getdata(), key=sum)[len(cell.getdata()) // 2])     # the median pixel
    diff = ImageChops.difference(cell, Image.new("RGB", cell.size, bg)).convert("L")
    mask = diff.point(lambda v: 255 if v > 28 else 0)
    for f in (5, 3):
        core = mask.filter(ImageFilter.MinFilter(f))
        if core.getbbox():
            break
    else:
        return None
    px, W = core.load(), core.width
    best = min(((x - half) ** 2 + (y - half) ** 2, x, y) for y in range(W) for x in range(W) if px[x, y])
    return cx - half + best[1], cy - half + best[2]


def to_game_tools(g):
    im = g.grab()
    if says(im, (741, 284, 1000, 307), "Create a Pretender God", light=False):
        return
    if not says(im, (780, 392, 960, 414), "Create World", light=False):
        g.grab("not_main_menu")
        raise Stop("the game is not on the main menu or Game Tools; bring it there first")
    g.key("g", wait=1.2)
    if not says(g.grab(), (741, 284, 1000, 307), "Create a Pretender God", light=False):
        raise Stop("'g' did not open Game Tools")


def find_line(im, x0, x1, y0, y1, target, names, half=14):
    """The y of the list line that says TARGET (one of NAMES) in x0..x1, y0..y1, or None. Reads
    all lines in one OCR call when NormCap's Tesseract is there, else matches each line."""
    ys = T.lines(im, x0, x1, y0, y1)
    if V.tesseract_ok():
        reads = V.ocr(im, [(x0, y - half, x1, y + half) for y in ys], [True] * len(ys))
        for y, r in zip(ys, reads):
            if V.closest(r["text"], names, limit=0.8, margin=0.03) == target:
                return y
        return None
    for y in ys:
        r = T.match(im, (x0, y - half, x1, y + half), names)
        if r and r[0][1] == target and r[0][0] <= 0.35:
            return y
    return None


def read_tip(tip, box, names, god_name, lo, hi):
    """(name, points) from the form tooltip "Name - N points", or None."""
    if V.tesseract_ok():
        r = V.ocr(tip, [box], [True])[0]
        m = re.match(r"(.*?)\s*[-–—]\s*(\d+)\s*points", r["text"])
        if m and V.closest(m.group(1), names, limit=0.8, margin=0.03) == god_name:
            return god_name, int(m.group(2))
        return None
    pts = T.match(tip, box, ["points"], suffix=True)
    if not pts:
        return None
    s0 = pts[0][2]
    r = T.match(tip, box, names, prefix=True, sizes=(s0 - 0.25, s0, s0 + 0.25, s0 + 0.5))
    if not r or r[0][0] > 0.3 or r[0][1] != god_name:
        return None
    return god_name, T.number(tip, box, lo, hi, prefix=god_name + " -", after=" points")


def pick_nation(g, era, target, names):
    g.click(840, 294, wait=1.5)                                          # Create a Pretender God
    im = g.grab()
    if not says(im, (680, 188, 900, 216), "Early Ages", light=False):
        g.grab("no_era_screen")
        raise Stop("the Select Era screen did not open")
    g.click(665, ERA_Y[era], wait=0.4)
    g.click(959, 689, wait=1.5)                                          # Ok
    g.scroll(False, 40, wait=0.8)
    prev = None
    for _ in range(30):
        im = g.grab()
        y = find_line(im, 780, 1180, 55, 915, target, names)
        if y is not None:
            x, _ = on_text(im, (780, y - 14, 1180, y + 14))
            for dx in (0, 10, 30):                                       # retry if a click is ignored
                g.click(x + dx, y, wait=1.8)
                now = g.grab()
                if not same(im, now, (720, 50, 1200, 920)):
                    g.grab("nation_overview")
                    return
                g.hover(200, 500, wait=0.5)
            raise Stop(f"clicking {target!r} in the nation list did nothing")
        if prev is not None and same(prev, im, (720, 50, 1200, 920)):
            break
        prev = im
        g.scroll(True, 3)
    g.grab("nation_not_found")
    raise Stop(f"could not find {target!r} in the nation list (is a mod nation's mod enabled in game?)")


def headers(im, color=HEADER, xs=(660, 700, 1200, 1262), tol=3):
    """Centre y of each full-width bar of COLOR (a callable: a pixel test)."""
    px = im.load()
    test = color if callable(color) else (lambda p: max(abs(a - b) for a, b in zip(p[:3], color)) <= tol)
    rows = [y for y in range(im.height) if all(test(px[x, y]) for x in xs)]
    out, start, last = [], None, None
    for y in rows + [None]:
        if start is not None and (y is None or y - last > 2):
            if last - start >= 8:
                out.append((start + last) // 2)
            start = None
        if y is not None:
            if start is None:
                start = y
            last = y
    return out


def form_bar(p):
    """The form chooser's semi-transparent red-brown "Dominion N" bars."""
    r, g, b = p[:3]
    return 70 <= r <= 130 and 28 <= r - g <= 52 and 3 <= g - b <= 20


def layout(im):
    """Design screen positions from the four panel headers (the window re-centres as it grows)."""
    h = headers(im)
    if len(h) != 4:
        raise Stop(f"expected the four design panels, found {len(h)} header bars")
    magic, bless, dom, prison = h
    return {"magic": magic, "bless": bless, "dom": dom, "prison": prison, "paths_y": magic + 32,
            "dom_y": dom + 41, "points_y": magic - 108, "form_y": magic - 44,
            "prison_y": [prison + 34, prison + 63, prison + 91], "ok_y": prison + 177}


def design_screen(g, name="design"):
    for _ in range(6):
        im = g.grab()
        try:
            return im, layout(im)
        except Stop:
            time.sleep(0.6)
    g.grab(name + "_missing")
    raise Stop("not on the Design Pretender screen")


def read_digit(im, x, y, hi=10):
    return T.number(im, (x + 15, y - 14, x + 38, y + 15), 0, hi, light=False)


# ---------------------------------------------------------------- form

def tip_box(im, y=990):
    """The text area of the tooltip box at the bottom centre, or None when no tooltip shows."""
    px = im.convert("L").load()
    if px[960, y] > 90:
        return None
    left = right = 960
    while left > 0 and px[left - 1, y] < 90:
        left -= 1
    while right < im.width - 1 and px[right + 1, y] < 90:
        right += 1
    if right - left < 60 or right - left > 1400:
        return None
    return (left + 3, y + 2, right - 3, y + 36)


def sprite_colour(im):
    """Mean colour of a sprite's figure (not the black/magenta/transparent or grey cell background)."""
    px = (im if im.mode == "RGBA" else im.convert("RGB")).load()
    n, s = 0, [0, 0, 0]
    for yy in range(im.height):
        for xx in range(im.width):
            r, gg, b = px[xx, yy][:3]
            if len(px[xx, yy]) == 4 and px[xx, yy][3] < 128:
                continue
            if max(r, gg, b) < 40 or (r > 200 and b > 200 and gg < 60):
                continue
            if max(r, gg, b) - min(r, gg, b) < 12 and 45 < r < 75:      # the chooser's grey cell
                continue
            n += 1
            s[0] += r; s[1] += gg; s[2] += b
    return [v / n for v in s] if n else [0, 0, 0]


def pick_form(g, gm, nation, god):
    names = sorted({gm.pret[p]["name"] for p in nation["pretenders"] if p in gm.pret}, key=len, reverse=True)
    same_name = [p for p in nation["pretenders"] if p in gm.pret and gm.pret[p]["name"] == god["name"]]
    cost = god["pointcost"] - nation["cheap_gods"].get(god["id"], 0)
    group = god.get("startdom") or 1
    g.key("p", wait=1.5)
    g.scroll(False, 40, at=(960, 600), wait=0.8)
    prev, hits = None, []
    for _ in range(25):
        g.hover(960, 1030, wait=0.2)
        im = g.grab()
        bars = headers(im, form_bar, xs=(360, 500, 700, 1250, 1450))
        if not bars:
            g.grab("no_form_chooser")
            raise Stop("the Select Physical Form window did not open")
        labels = [T.number(im, (860, b - 12, 1060, b + 12), 1, 9, prefix="Dominion") for b in bars]
        if group in labels:
            i = labels.index(group)
            top = bars[i]
            end = bars[i + 1] if i + 1 < len(bars) else 965
            if i + 1 == len(bars):                             # the last group: on screen to its end
                for yc in T.lines(im, 900, 1020, top + 40, 1000):  # once the chooser's Cancel shows
                    if says(im, (880, yc - 14, 1040, yc + 14), "Cancel"):
                        end = min(end, yc - 20)
                        break
            if top <= 300 or end < 965:                        # the whole group is on screen
                rows = [y for y in range(top + 66, end - 40, 116)]
                for y in rows:
                    for cx in CELL_X:
                        pt = on_sprite(im, cx, y)
                        if pt is None:
                            continue
                        x, y2 = pt
                        g.hover(x, y2, wait=0.35)
                        tip = g.grab()
                        box = tip_box(tip)
                        if not box:
                            continue
                        got = read_tip(tip, box, names, god["name"], max(0, cost - 150), cost + 150)
                        if not got:
                            continue
                        n = got[1]
                        hits.append((x, y2, n, tip.crop((cx - 58, y - 55, cx + 58, y + 55))))
                break
        if prev is not None and same(prev, im, (340, 50, 1580, 960)):
            break
        prev = im
        g.scroll(True, 2, at=(960, 600))
    if not hits:
        g.grab("form_not_found")
        raise Stop(f"could not find {god['name']} among the Dominion {group} forms")
    if len(hits) > 1:
        exact = [h for h in hits if h[2] == cost]
        hits = exact or hits
    if len(hits) > 1 and len(same_name) > 1:
        # several forms share the name (the Dragons): compare the cell's colours with the sprites
        def dist(cell, pid):
            f = os.path.join(INSPECTOR_SPRITES, f"{int(pid):04d}_1.png")
            if not os.path.exists(f):
                return 1e9
            a, b = sprite_colour(cell), sprite_colour(Image.open(f).convert("RGBA"))
            return sum((u - v) ** 2 for u, v in zip(a, b))
        scored = sorted(((dist(h[3], god["id"]) - min(dist(h[3], o) for o in same_name if o != god["id"]), h) for h in hits),
                        key=lambda t: t[0])
        hits = [scored[0][1]]
        print(f"  {len(same_name)} forms are called {god['name']}: took the cell whose colours match sprite {god['id']} best")
    x, y, n, _ = hits[0]
    if n is not None and n != cost:
        print(f"  NOTE: the game prices {god['name']} at {n} points, the calculator at {cost}")
    g.click(x, y, wait=1.5)
    return n


# ---------------------------------------------------------------- design values

def set_paths(g, want, base):
    im, L = design_screen(g)
    for c in P.PATHS:
        x = PATH_X[c]
        cur = read_digit(im, x, L["paths_y"])
        if cur is None:
            raise Stop(f"could not read the {P.PATHNAME[c]} level")
        if cur != want[c]:
            g.click(x, L["paths_y"], right=cur > want[c], times=abs(cur - want[c]), wait=0.3)
            im, L = design_screen(g)
    bad = {c: read_digit(im, PATH_X[c], L["paths_y"]) for c in P.PATHS}
    bad = {c: v for c, v in bad.items() if v != want[c]}
    if bad:
        raise Stop("paths did not take: " + ", ".join(f"{P.PATHNAME[c]} is {v}, wanted {want[c]}" for c, v in bad.items()))


def set_dominion(g, dom):
    im, L = design_screen(g)
    cur = read_digit(im, DOM_X["dom"], L["dom_y"])
    if cur is None:
        raise Stop("could not read the dominion")
    if cur != dom:
        g.click(DOM_X["dom"], L["dom_y"], right=cur > dom, times=abs(cur - dom), wait=0.4)
        im, L = design_screen(g)
        got = read_digit(im, DOM_X["dom"], L["dom_y"])
        if got != dom:
            raise Stop(f"dominion is {got}, wanted {dom}")


def set_scales(g, sc):
    for s in P.SCALES:
        im, L = design_screen(g)
        x = DOM_X[s]
        cur = read_digit(im, x, L["dom_y"], 6)
        if cur == 0 and sc[s] == 0:
            continue
        g.click(x, L["dom_y"], right=True, times=7, wait=0.4)              # to the bottom of its range
        im, L = design_screen(g)
        low = -(read_digit(im, x, L["dom_y"], 6) or 0)
        if sc[s] - low:
            g.click(x, L["dom_y"], times=sc[s] - low, wait=0.4)
            im, L = design_screen(g)
        got = read_digit(im, x, L["dom_y"], 6)
        if got != abs(sc[s]):
            raise Stop(f"{s} shows {got}, wanted {sc[s]} (its range here starts at {low})")


def set_prison(g, prison):
    im, L = design_screen(g)
    g.click(665, L["prison_y"][prison], wait=0.5)


def add_blesses(g, blesses, all_names):
    for name in blesses:
        g.key("a", wait=1.3)
        g.scroll(False, 40, at=(960, 600), wait=0.6)
        found, prev = False, None
        for _ in range(12):
            g.hover(960, 1030, wait=0.15)
            im = g.grab()
            y = find_line(im, 840, 1085, 50, 940, name, all_names, half=15)
            if y is not None:
                g.click(*on_text(im, (840, y - 15, 1085, y + 15)), wait=1.2)
                found = True
            if found:
                break
            if prev is not None and same(prev, im, (640, 50, 1280, 940)):
                break
            prev = im
            g.scroll(True, 3, at=(960, 600))
        if not found:
            g.grab("bless_missing")
            raise Stop(f"bless {name!r} is not in the game's list (or not available)")
        if len(headers(g.grab())) != 4:
            g.grab("bless_not_taken")
            raise Stop(f"the game did not take {name!r} (greyed out: not enough paths or bless points?)")


def read_totals(g, expect):
    im, L = design_screen(g)
    pts = T.number(im, (650, L["points_y"] - 16, 1000, L["points_y"] + 16), expect - 250, expect + 250,
                   prefix="Design points:")
    bp = T.number(im, (700, L["bless"] - 14, 1220, L["bless"] + 14), 0, 99, prefix="Bless Effects (",
                  font="guifont_fancy.ttf", after=" bless points left)")
    return pts, bp


# ---------------------------------------------------------------- save

def save(g, name):
    """Ok on the design screen (if it is open), Yes to each "points left to spend" question, the
    god's name, and Ok on "All praise"."""
    im = g.grab()
    if len(headers(im)) == 4:
        g.click(959, layout(im)["ok_y"], wait=1.5)
        im = g.grab()
    for _ in range(3):                                                   # design points, bless points
        if not says(im, (900, 445, 1020, 475), "Yes"):
            break
        g.click(959, 459, wait=1.5)
        im = g.grab()
    if not (says(im, (900, 444, 1020, 472), "Ok") and says(im, (880, 476, 1040, 504), "Cancel")):
        g.grab("no_name_prompt")
        raise Stop("the name prompt did not appear")
    if name:
        g.key(*["BackSpace"] * 40, wait=0.2)
        g.type(name)
        time.sleep(0.4)
    g.grab("name")
    g.click(959, 458, wait=1.8)
    im = g.grab("saved")
    if not says(im, (900, 460, 1020, 488), "Ok"):
        raise Stop("no 'All praise' confirmation after the name")
    g.click(959, 474, wait=1.5)                                          # All praise ... Ok


# ---------------------------------------------------------------- main

def plan(a):
    o, rest = P.opts([x for x in a if x not in ("--no-save", "--dry")])
    mod, costs = o.pop("mod", None), {}
    for item in (o.pop("cost", "") or "").split(","):
        if "=" in item:
            k, v = item.split("=")
            costs[k.strip()] = int(v)
    name = o.pop("name", None)
    if len(rest) < 2:
        sys.exit(__doc__)
    gm = P.Game(mod, costs)
    nation, god = gm.nation(rest[0]), gm.god(" ".join(rest[1:]))
    paths, dom, sc, prison, _, left0 = P.setup(o, nation)
    if god["id"] not in nation["pretenders"]:
        sys.exit(f"{god['name']} ({god['id']}) is not in {nation['name']}'s pretender list")
    if (god.get("minprison") or 0) > prison:
        sys.exit(f"{god['name']} must sleep: use --prison {['awake', 'dormant', 'imprisoned'][god['minprison']]}")
    if not P.scale_ok(god, nation, sc):
        sys.exit("these scales are outside what this chassis and nation allow")
    eff = P.effective(god, paths)
    dom = max(god.get("startdom") or 1, dom)
    total = P.god_cost(god, nation, paths, dom)
    if total is None:
        sys.exit("no form cost known for this god: give --cost ID=N (read it in the game's form chooser)")
    left = left0 - total
    if left < 0:
        sys.exit(f"over budget by {-left} points")
    bl = {b["name"]: b for b in P.bless_list()}
    blesses = []
    for item in (o.get("bless") or "").split(","):
        m = re.match(r"\s*(.*?)\s*(?:x(\d+))?\s*$", item)
        if not m.group(1):
            continue
        b = next((v for k, v in bl.items() if k.lower() == m.group(1).lower()), None)
        if not b:
            sys.exit(f"unknown bless {m.group(1)!r}")
        if not P.bless_ok(b, eff, sc):
            sys.exit(f"{b['name']} needs more paths or scales than this design has")
        blesses += [b["name"]] * int(m.group(2) or 1)
    bp = P.bless_points(eff, nation["bless_bonus"])
    used = sum(bl[n]["cost"] for n in blesses)
    if used > bp:
        sys.exit(f"the blesses cost {used}, the design has {bp} bless points")
    return dict(gm=gm, nation=nation, god=god, paths=eff, dom=dom, sc=sc, prison=prison, left=left,
                blesses=blesses, bp_left=bp - used, name=name)


def report_new(before):
    new = sorted(set(os.listdir(NEWLORDS)) - before) if os.path.isdir(NEWLORDS) else []
    print("saved: " + (", ".join(os.path.join(NEWLORDS, f) for f in new) if new else
                       "(no new file in newlords: the game overwrote an older one of that nation, or did not save)"))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    before = set(os.listdir(NEWLORDS)) if os.path.isdir(NEWLORDS) else set()
    if a[0] == "--save-current":
        name = a[a.index("--name") + 1] if "--name" in a else None
        run(lambda g: save(g, name), "god")
        report_new(before)
        return
    d = plan(a)
    n, god = d["nation"], d["god"]
    era = n.get("era")
    if era not in ERA_Y:
        sys.exit(f"unknown era {era!r} for nation {n['id']}")
    print(f"{era} {n['name']}: {god['name']} ({god['id']}), {['awake', 'dormant', 'imprisoned'][d['prison']]}, "
          f"paths {P.paths_str(d['paths'])}, dominion {d['dom']}, scales {P.scales_str(d['sc'])}"
          + (f", blesses {', '.join(d['blesses'])}" if d["blesses"] else ""))
    print(f"calculator: {d['left']} design points left, {d['bp_left']} bless points left")
    if "--dry" in a:
        return

    def work(g):
        to_game_tools(g)
        print("- nation")
        names = [f"{x['name']}, {x['epithet']}" if x.get("epithet") else x["name"]
                 for x in d["gm"].nations.values() if x.get("era") == era]
        pick_nation(g, era, f"{n['name']}, {n['epithet']}" if n.get("epithet") else n["name"], names)
        g.key("Return", wait=1.8)                                        # nation overview: Ok
        design_screen(g)
        print("- form")
        pick_form(g, d["gm"], n, god)
        print("- sleep, paths, dominion, scales")
        set_prison(g, d["prison"])
        set_paths(g, d["paths"], god)
        set_dominion(g, d["dom"])
        set_scales(g, d["sc"])
        if d["blesses"]:
            print("- blesses")
            add_blesses(g, d["blesses"], [b["name"] for b in P.bless_list()])
        pts, bp = read_totals(g, d["left"])
        g.grab("design")
        print(f"game: {pts} design points left, {bp} bless points left")
        if pts != d["left"] or bp != d["bp_left"]:
            print(f"DIFFERENT from the calculator ({d['left']} / {d['bp_left']}): the game's numbers count; check the shot")
        if "--no-save" in a:
            print("not saved: the design is open in the game")
        else:
            save(g, d["name"])

    run(work, "god")
    if "--no-save" not in a:
        report_new(before)


if __name__ == "__main__":
    main()
