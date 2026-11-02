"""Read nations' info screens in the running Dominions 6 and keep them in the knowledge base.

  python3 -I nations.py read ERA NATION [NATION...]   read these nations (part of the name is enough)
  python3 -I nations.py read ERA --all                every nation the game lists in that era
  python3 -I nations.py parse IMAGE [--era MA] [--name "Ulm, Forges of Ulm"]   parse a saved shot
  python3 -I nations.py overview                      rewrite nations/OVERVIEW.md from the files
  python3 -I nations.py list                          nations read so far

ERA: EA, MA or LA. The game must be on the main menu or Game Tools. The script goes Game Tools >
Create a Pretender God > era > Select Nation (this makes no game), right-clicks each nation (its
info window: description, National Features, commanders, units, sites), reads it with dom6-ui's
vision.py, closes it with Return, and goes back to where it started. Mod nations show when their
mod is enabled in game. Each nation is written to dom6-knowledge/nations/<ERA>/<slug>.md and .json
with a half-size picture of the info window (img/<slug>.jpg); vanilla nations get the
inspector's recruit lists, heroes and spells added. Uses the dom6-ui guard (waits until the user
is idle, only while the game is focused, gives focus back).
"""
import datetime
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(SKILLS, "dom6-ui", "scripts"))
sys.path.insert(0, os.path.join(SKILLS, "dom6-pretender-ingame", "scripts"))

from PIL import Image  # noqa: E402

import textmatch as T  # noqa: E402
import vision as V  # noqa: E402

KB = os.path.join(SKILLS, "dom6-knowledge", "nations")
INSPECTOR = os.path.join(SKILLS, "dom6-inspector", "scripts", "inspector.py")
ERA_Y = {"EA": 202, "MA": 373, "LA": 531}
ERA_NUM = {"EA": 1, "MA": 2, "LA": 3}
LIST = (780, 1180, 55, 915)                   # the Select Nation list: x0, x1, y0, y1
FEATURE_KEYS = ("Race", "Military", "Magic", "Priests", "Scales & Blesses", "Buildings")


def slug(name):
    base = name.split(",")[0]
    return re.sub(r"[^a-z0-9]+", "_", base.lower().replace("'", "")).strip("_") or "nation"


# ---------------------------------------------------------------- fixing the reading

def _vocab():
    words = set()
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english", "/usr/share/dict/british-english"):
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                words |= {w.strip().lower() for w in f}
        except OSError:
            pass
    return words


VOCAB = None


# ---------------------------------------------------------------- parsing the info window

def parse(im):
    """The nation info window in IM: {description, features, commanders, units, sites, ...}."""
    sc = V.scene(im)
    if not sc["windows"]:
        return None
    w = max(sc["windows"], key=lambda w: (w["box"][2] - w["box"][0]) * (w["box"][3] - w["box"][1]))
    lines = sorted(w["text"], key=lambda t: (t["box"][1], t["box"][0]))
    bar = next((b for b in w["bars"] if V.closest(b.get("text") or "", ["National Features"], 0.6)), None)
    bar_y = bar["box"][1] if bar else None
    labels = {}
    for t in lines:
        k = V.closest(t["text"], ["Commanders", "Units", "Sites"], 0.8)
        if k and k not in labels and len(t["text"]) <= 14:
            labels[k] = t["box"]
    feats_start = next((t["box"][1] for t in lines if re.match(r"(Race|Military)\s*:", t["text"])), None)
    if bar_y is None:
        bar_y = feats_start - 20 if feats_start else None
    if bar_y is None:
        return None
    first_label = min((b[1] for b in labels.values()), default=w["box"][3])
    _strays(lines)
    desc = [t["text"] for t in lines if t["box"][1] < bar_y and t["box"][1] > w["box"][1] + 40]
    feats, order = {}, []
    for t in lines:
        if not (bar_y < t["box"][1] < first_label):
            continue
        text = t["text"]
        m = re.match(r"([A-Z][\w &'-]{1,30}?)\s*:\s*(.*)", text)
        if m:
            key = V.closest(m.group(1), FEATURE_KEYS, 0.8) or m.group(1)
            feats[key] = m.group(2).strip()
            order.append(key)
        elif order:                                         # a feature running onto a second line
            feats[order[-1]] += " " + text
    feat_end = max((t["box"][3] for t in lines if bar_y < t["box"][1] < first_label), default=bar_y)
    ok_y = next((t["box"][1] for t in lines if t["text"].strip() in ("Ok", "OK")), w["box"][3] - 40)
    sprites = sorted((s_["box"] for s_ in w["sprites"] if s_["box"][1] > feat_end + 10
                      and s_["box"][3] < ok_y and s_["box"][3] - s_["box"][1] >= 10), key=lambda b: b[1])
    rows = []                                               # sprites grouped into rows by height
    for b in sprites:
        if rows and b[1] < rows[-1]["y1"] - 8:
            rows[-1]["boxes"].append(b)
            rows[-1]["y1"] = max(rows[-1]["y1"], b[3])
        else:
            rows.append({"y0": b[1], "y1": b[3], "boxes": [b]})
    for i in range(len(rows) - 2, -1, -1):                  # lance tips poking up from the next row
        r, n = rows[i], rows[i + 1]
        if r["y1"] - r["y0"] < 20 and n["y0"] - r["y1"] < 15:
            n["boxes"] += r["boxes"]                        # (the label stays above n's own top)
            del rows[i]
    x0 = w["box"][0] + 18
    heads = V.ocr(im, [(x0, max(0, r["y0"] - 34), x0 + 160, r["y0"] - 2) for r in rows]) if rows else []
    sections, current = {}, None
    for r, h in zip(rows, heads):
        k = V.closest(h["text"], ["Commanders", "Units", "Sites"], 0.7)
        mid = sorted(q[1] for q in r["boxes"])[len(r["boxes"]) // 2]    # a typical sprite top: a
        above = [(lb[1], name) for name, lb in labels.items()           # hydra can poke up past
                 if lb[3] <= mid + 6 and lb[1] > r["y0"] - 60]          # the row's own label
        if above:
            k = max(above)[1]
        if k:
            current = k.lower()
        elif current is None:
            current = "commanders"
        sections.setdefault(current, []).extend(r["boxes"])
    sections = {k: _merge_columns(v) for k, v in sections.items()}
    E = V.edges(im)
    for k in ("commanders", "units"):                       # touching lances join riders into one
        if k in sections:                                   # box: split it on the sprite grid
            sections[k] = [p for b in sections[k] for p in _split_wide(E, b)]
    if "sites" in sections:                                 # site icons are square and touch
        split = []
        for b in sections["sites"]:
            n = max(1, round((b[2] - b[0]) / max(1, b[3] - b[1])))
            wd = (b[2] - b[0]) / n
            split += [(round(b[0] + k * wd), b[1], round(b[0] + (k + 1) * wd), b[3]) for k in range(n)]
        sections["sites"] = split
    scores = [t.get("score", 1) for t in lines if t["box"][1] < feat_end + 1]
    return {"description": " ".join(desc).strip(), "features": feats,
            "commanders": len(sections.get("commanders", [])), "units": len(sections.get("units", [])),
            "sites": len(sections.get("sites", [])), "sprite_boxes": sections, "window": w["box"],
            "ocr_score": round(sum(scores) / len(scores), 3) if scores else None}


def _strays(lines):
    """Lines of a paragraph start at one left margin; a first word that starts left of it has a
    speck of the panel border read as a letter in front ("fits" for "its"): drop that letter."""
    starts = sorted(t["words"][0][2][0] for t in lines if t.get("words"))
    if len(starts) < 3:
        return
    global VOCAB
    if VOCAB is None:
        VOCAB = _vocab()
    margin = starts[len(starts) // 2]
    for t in lines:
        ws = t.get("words")
        if not ws:
            continue
        w0 = ws[0][0]
        core = re.sub(r"[^\w']+$", "", w0[1:])
        if ws[0][2][0] <= margin - 3 and len(w0) > 2 and w0[0] in "fli|j!" and core.lower() in VOCAB \
                and t["text"].startswith(w0):
            t["text"] = t["text"][1:]


PITCH = 61.3                     # sprites in the info window's rows sit this far apart


def _split_wide(E, b):
    """A box wider than one grid cell holds several sprites: cut at the emptiest column near each
    cell boundary."""
    n = round((b[2] - b[0]) / PITCH)
    if n < 2:
        return [b]
    px = E.load()
    ink = [sum(1 for y in range(b[1], b[3]) if px[x, y]) for x in range(b[0], b[2])]
    cuts, w = [], (b[2] - b[0]) / n
    for j in range(1, n):
        c = round(j * w)
        lo, hi = max(1, c - 15), min(len(ink) - 1, c + 15)
        cuts.append(min(range(lo, hi), key=lambda i: (ink[i], abs(i - c))))
    edges = [0] + cuts + [b[2] - b[0]]
    return [(b[0] + edges[i], b[1], b[0] + edges[i + 1], b[3]) for i in range(n)]


def _merge_columns(boxes):
    """One box per sprite: parts of a sprite (a lance above a knight) share its column."""
    out = []
    for b in sorted(boxes):
        a = out[-1] if out else None
        near = a and (0 <= b[1] - a[3] <= 14 or 0 <= a[1] - b[3] <= 14)   # a pike's tip, a plume
        wide = a and a[2] - b[0] >= 0.4 * min(a[2] - a[0], b[2] - b[0])   # a lance only grazes
        if a and ((wide and b[1] < a[3] and a[1] < b[3]) or (b[0] <= a[2] + 3 and near)):
            a = out[-1]
            out[-1] = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
        else:
            out.append(tuple(b))
    return out


# ---------------------------------------------------------------- what the nation is

def vanilla_id(name, era):
    try:
        import pretender as P
    except ImportError:
        sys.path.insert(0, os.path.join(SKILLS, "dom6-pretender", "scripts"))
        import pretender as P
    gm = P.Game()
    for n in gm.nations.values():
        full = f"{n['name']}, {n['epithet']}" if n.get("epithet") else n["name"]
        if n.get("era") == era and V.closest(name, [full], 0.9):
            return n["id"]
    return None


def mod_nation(name):
    """(nation number, .dm path) of a mod nation called NAME in an installed mod, or None."""
    paths = glob.glob(os.path.expanduser("~/.dominions6/mods/*/*.dm"))
    paths += glob.glob(os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/2511500/*/*.dm"))
    nm = name.split(",")[0].strip()
    for p in paths:
        try:
            with open(p, encoding="utf-8-sig", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        for m in re.finditer(r"#selectnation\s+(\d+)(.*?)#end", text, re.S):
            n = re.search(r'#name\s+"([^"]+)"', m.group(2))
            if n and n.group(1).strip().lower() == nm.lower():
                return int(m.group(1)), p
    return None


def inspector_page(nid):
    try:
        r = subprocess.run([sys.executable, "-I", INSPECTOR, "nation", str(nid)], capture_output=True,
                           text=True, timeout=120)
        return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


# ---------------------------------------------------------------- writing

def save(rec, im):
    era = rec["era"]
    d = os.path.join(KB, era)
    os.makedirs(os.path.join(d, "img"), exist_ok=True)
    s = slug(rec["name"])
    if im is not None and rec.get("window"):
        crop = im.convert("RGB").crop(rec["window"])
        crop.resize((crop.width // 2, crop.height // 2)).save(os.path.join(d, "img", s + ".jpg"), quality=85)
        rec["image"] = f"img/{s}.jpg"
    with open(os.path.join(d, s + ".json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
    with open(os.path.join(d, s + ".md"), "w", encoding="utf-8") as f:
        f.write(markdown(rec))
    return os.path.join(d, s + ".md")


def markdown(r):
    out = [f"# {r['name']} ({r['era']})", ""]
    src = f"nation {r['id']}" if r.get("id") is not None else "nation number unknown"
    if r.get("mod"):
        src += f", mod `{os.path.basename(os.path.dirname(r['mod']))}`"
    out += [f"*{src}; read from the game's nation info screen on {r['read']} (OCR, score "
            f"{r.get('ocr_score')}; small reading slips are possible)*", ""]
    if r.get("image"):
        out += [f"![info screen]({r['image']})", ""]
    out += ["## Description", "", r["description"] or "(not read)", "", "## National features", ""]
    for k, v in r["features"].items():
        out.append(f"- **{k}:** {v}")
    out += ["", "## On the info screen", "",
            f"- {r['commanders']} commanders, {r['units']} units, {r['sites']} start sites shown "
            "(right-click a sprite in game for its stats)"]
    if r.get("inspector"):
        out += ["", "## From the inspector (vanilla data)", "", "```", r["inspector"], "```"]
    return "\n".join(out) + "\n"


def overview():
    rows = []
    for p in sorted(glob.glob(os.path.join(KB, "*", "*.json"))):
        with open(p, encoding="utf-8") as f:
            r = json.load(f)
        rows.append(r)
    order = {"EA": 0, "MA": 1, "LA": 2}
    rows.sort(key=lambda r: (order.get(r["era"], 9), r["name"].lower()))
    out = ["# Nations overview", "",
           "Written by `dom6-nations/scripts/nations.py overview` from the nation files read in game. "
           "One file per nation in `<ERA>/`.", ""]
    for era in ("EA", "MA", "LA"):
        rs = [r for r in rows if r["era"] == era]
        if not rs:
            continue
        out += [f"## {era}", "", "| Nation | Race | Military | Magic | Priests | Scales & blesses |",
                "|---|---|---|---|---|---|"]
        for r in rs:
            f = r["features"]
            link = f"[{r['name']}]({era}/{slug(r['name'])}.md)" + (" *(mod)*" if r.get("mod") else "")
            cell = lambda k: (f.get(k) or "").replace("|", "/")
            out.append(f"| {link} | {cell('Race')} | {cell('Military')} | {cell('Magic')} | {cell('Priests')} "
                       f"| {cell('Scales & Blesses')} |")
        out.append("")
    p = os.path.join(KB, "OVERVIEW.md")
    os.makedirs(KB, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return p, len(rows)


def record(info, name, era):
    rec = dict(info, name=name, era=era, read=datetime.date.today().isoformat())
    rec["id"] = vanilla_id(name, era)
    if rec["id"] is None:
        m = mod_nation(name)
        if m:
            rec["id"], rec["mod"] = m
    elif rec["id"] is not None:
        rec["inspector"] = inspector_page(rec["id"])
    return rec


# ---------------------------------------------------------------- driving the game

def until(g, ok, most=3.0, settle=0.15):
    """Grab until OK(shot) holds (a window opened or closed), then once more after SETTLE seconds
    so it is fully drawn; after MOST seconds the last shot is returned as it is."""
    import time
    end = time.time() + most
    while True:
        im = g.grab()
        if ok(im) or time.time() > end:
            break
        time.sleep(0.05)
    time.sleep(settle)
    return g.grab()


def read_game(era, wanted, all_):
    import session
    import build_god as B
    from session import Stop, on_text, same, says

    done, saved = set(), []

    def work(g):
        im = g.grab()
        from_menu = not says(im, (741, 284, 1000, 307), "Create a Pretender God", light=False)
        B.to_game_tools(g)
        g.click(840, 294, wait=0.6)                         # Create a Pretender God
        if not says(g.grab(), (680, 188, 900, 216), "Early Ages", light=False):
            g.grab("no_era")
            raise Stop("the Select Era screen did not open")
        g.click(665, ERA_Y[era], wait=0.15)
        g.click(959, 689, wait=0.6)
        g.scroll(False, 40, wait=0.3)
        prev = None
        for _ in range(40):
            page = g.grab()
            ys = T.lines(page, *LIST)
            reads = V.ocr(page, [(LIST[0], y - 14, LIST[1], y + 14) for y in ys], [True] * len(ys))
            for y, r in zip(ys, reads):
                name = r["text"].strip()
                if not name or name in done:
                    continue
                if "," not in name or V.closest(name, ["Cancel", "Ok"], 0.8):   # buttons under the list:
                    continue                                                  # nations read "Name, Epithet"
                if not all_:
                    hit = [w for w in wanted if w.lower() in name.lower() or V.closest(w, [name], 0.85)]
                    if not hit:
                        continue
                done.add(name)
                x, _ = on_text(page, (LIST[0], y - 14, LIST[1], y + 14))
                g.click(x, y, right=True, wait=0.1)
                shot = until(g, lambda im: not same(page, im, (720, 50, 1200, 920)))
                os.makedirs(os.path.expanduser("~/.cache/dom6ui"), exist_ok=True)
                shot.save(os.path.expanduser(f"~/.cache/dom6ui/nation_{slug(name)}.png"))   # full size, to re-parse offline
                info = parse(shot)
                if not info or not info["features"]:
                    g.grab("not_info")
                    raise Stop(f"right-clicking {name!r} did not show its info window")
                rec = record(info, name, era)
                path = save(rec, shot)
                saved.append(path)
                print(f"  {name}: {len(info['features'])} features, {len(info['description'])} chars "
                      f"of description, {info['commanders']}/{info['units']}/{info['sites']} "
                      f"commanders/units/sites -> {os.path.relpath(path, SKILLS)}")
                g.key("Return", wait=0.05)                  # close the info window
                if not same(page, until(g, lambda im: same(page, im, (720, 50, 1200, 920))),
                            (720, 50, 1200, 920)):
                    g.grab("list_moved")
                    raise Stop("the nation list is not as it was after closing the info window")
            if not all_ and all(any(w.lower() in d.lower() or V.closest(w, [d], 0.85) for d in done)
                                for w in wanted):
                break
            if prev is not None and same(prev, page, (720, 50, 1200, 920)):
                break                                       # the list's end
            prev = page
            g.scroll(True, 3, wait=0.25)
        g.key("Escape", wait=0.6)                           # back to Game Tools
        im = g.grab()
        if not says(im, (741, 284, 1000, 307), "Create a Pretender God", light=False):
            g.grab("not_back")
            raise Stop("Escape did not go back to Game Tools")
        if from_menu:
            g.click(959, 662, wait=0.6)                     # Game Tools' Exit
        g.grab("end")

    session.run(work, "nations")
    missing = [w for w in wanted if not any(w.lower() in d.lower() or V.closest(w, [d], 0.85) for d in done)]
    return saved, missing


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("read")
    a.add_argument("era", choices=("EA", "MA", "LA"))
    a.add_argument("nations", nargs="*")
    a.add_argument("--all", action="store_true")
    a = sub.add_parser("parse")
    a.add_argument("image")
    a.add_argument("--era", default="MA")
    a.add_argument("--name", default="?")
    a.add_argument("--save", action="store_true")
    sub.add_parser("overview")
    sub.add_parser("list")
    o = ap.parse_args(argv)
    if o.cmd == "read":
        if not o.nations and not o.all:
            sys.exit("name nations or give --all")
        saved, missing = read_game(o.era, o.nations, o.all)
        p, n = overview()
        print(f"read {len(saved)} nations; overview of {n}: {p}")
        if missing:
            print("not found in the list:", ", ".join(missing))
    elif o.cmd == "parse":
        im = Image.open(o.image)
        info = parse(im)
        if not info:
            sys.exit("no nation info window found")
        rec = record(info, o.name, o.era) if o.name != "?" else dict(info)
        if o.save:
            rec.setdefault("read", datetime.date.today().isoformat())
            print(save(rec, im))
        else:
            rec.pop("inspector", None)
            print(json.dumps({k: v for k, v in rec.items() if k != "sprite_boxes"}, indent=1, ensure_ascii=False))
    elif o.cmd == "overview":
        print(*overview())
    elif o.cmd == "list":
        for p in sorted(glob.glob(os.path.join(KB, "*", "*.json"))):
            with open(p, encoding="utf-8") as f:
                r = json.load(f)
            print(f"{r['era']}  {r['name']:45} {r['read']}  {os.path.relpath(p[:-5] + '.md', KB)}")


if __name__ == "__main__":
    main(sys.argv[1:])
