"""Look at a Dominions 6 game on Claude's virtual screen (bgplay) - READ ONLY.

The FoG II order.py pattern brought to Dominions (2026-11-03): one command = one checked action,
the result read back (OCR of named regions from Dominions' .claude/game-ui.json), and the screen left
readable for a human (mouse parked on a neutral panel). Nothing here gives orders, recruits, researches
or ends the turn - the user's MP game: "click around, just don't change anything".

  dom6bg.py look                      shot + read title, resources, province panel, scout report
  dom6bg.py read REGION [REGION...]   OCR named regions (title resources commanders province sites
                                      scout hovername dialog replaylog)
  dom6bg.py capital                   Home (camera to the capital), then look
  dom6bg.py zoom out|in N             mouse wheel over the map centre, N notches, then a shot
  dom6bg.py mapshot [N]               zoom out N notches (default 3), full shot, zoom back in N
  dom6bg.py messages                  open Messages (m), read the list, leave it open for `goto`
  dom6bg.py goto TEXT                 in the open Messages list, click "Goto province" on the row whose
                                      text contains TEXT (camera only), then look
  dom6bg.py exitdialog                click the dialog's "Exit" (found by OCR) - never Esc (Esc = Options)
  dom6bg.py battle NAME               record the open Battle Summary's replay (battle_review.py, detail 4)
  dom6bg.py park                      park the mouse on the neutral spot
  dom6bg.py pan DX DY                 move the camera DX, DY map pixels (arrow-key holds; 72 px per 100 ms
                                      measured with camcal.py at normal zoom; + = show what is right/below)
  dom6bg.py snap                      where is this view? resnap the current shot on the game's atlas
                                      (game-ui.json "atlas"): world point at the screen centre, scale, match
  dom6bg.py lookat WX WY              FoG II snapview: snap, pan so world point WX,WY is at the centre (wrap-
                                      aware), settle, snap again to check (world = atlas px, mod the period)
  dom6bg.py provsweep GRAPH.json OUT.jsonl [--views 3x3] [--redo]
                                      THE province sweep: provinces, not a grid. GRAPH = dom6-map provgraph.py
                                      (built + fitted). For each view (lookat, snap) right-click every province
                                      centre on screen, check the panel's number is that province, read panel +
                                      scout. Skips provinces already in OUT unless --redo. Ends at the capital.
  dom6bg.py labelshot GRAPH.json [OUT.png] [--key mark|world]
                                      fresh shot, snapped, every province number drawn at its marker (flag
                                      point) or centre - the Dominions "gridshot" (provinces, not squares)
  dom6bg.py flagsweep GRAPH.json OUTDIR [--views 3x3]
                                      camera only, no clicks: per view crop every province's flag (above its
                                      marker) -> OUTDIR/<num>.png + sheet.png (all flags, numbered) for owners
  dom6bg.py view NUM [--graph GRAPH.json]
                                      camera to province NUM (provgraph), right-click its centre = view it,
                                      panel number checked (default graph: game-ui.json "atlas" "graph")
  dom6bg.py sweep OUT.jsonl [--step 130] [--tag T]   (OLD click grid - only to seed provgraph's fit)
                                      RIGHT-click (= view, never an order) a grid of points over the map part
                                      of the CURRENT view, read each panel's title "Name (number)", terrain and
                                      scout report; one JSON line per new province (screen point, tag). Skips
                                      the scout-report corner. Points come from this view, never an old shot.

Start Dominions on the virtual screen first (dom6-ui SKILL.md: virtual screen recipe). Run with
python3 -I; the virtual screen is BG_DISPLAY (default :5).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
BG = os.path.join(ROOT, ".claude", "skills", "game-ui", "scripts", "bgplay.py")
GAME = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))      # the Dominions 6 folder
DISP = os.environ.get("BG_DISPLAY", ":5")
PARK = (1750, 820)                 # empty lower part of the province panel: no tooltip, no order
MAPC = (960, 520)                  # map centre for wheel zoom


def bg(*steps, quiet=False):
    r = subprocess.run(["python3", "-I", BG, *steps], cwd=GAME, capture_output=True, text=True,
                       env=dict(os.environ, BG_DISPLAY=DISP))
    out = (r.stdout + r.stderr).strip()
    if not quiet and out:
        print(out)
    return out


def seq(*steps):
    return bg("seq", *steps, quiet=True).splitlines()[-1:] or [""]


def shot():
    p = bg("shot", "--full", quiet=True).splitlines()[-1]
    print("shot:", p)
    return p


def read(*names):
    return bg("read", *names)


def park():
    seq(f"move {PARK[0]} {PARK[1]}", "wait 200")


def find_text(img, text):
    """Box centre of the first OCR'd line containing TEXT (dom6-ui vision.py)."""
    sys.path.insert(0, HERE)
    import vision as V
    from PIL import Image
    for w in V.scene(Image.open(img))["windows"]:
        for t in w["text"] + w["bars"]:
            if text.lower() in (t.get("text") or "").lower():
                x0, y0, x1, y1 = t["box"]
                return (x0 + x1) // 2, (y0 + y1) // 2, t["text"]
    return None


def look():
    shot()
    read("title", "resources", "province", "scout")
    park()


import json
import re
import time

RESNAP = os.path.join(ROOT, ".claude", "skills", "map-measure", "scripts", "resnap.py")
CENTRE = (930, 515)
MAP_BOX = (265, 95, 1595, 935)      # map part of the screen: commander list left, province panel right


def pan(dx, dy):
    steps = []
    for d, pos, neg in ((dx, "Right", "Left"), (dy, "Down", "Up")):
        if d:
            steps += [f"hold {pos if d > 0 else neg} {int(abs(d) / 72 * 100)}", "wait 500"]
    if steps:
        seq(*steps)


def atlas():
    d = json.load(open(os.path.join(GAME, ".claude", "game-ui.json")))["atlas"]
    return os.path.join(GAME, d["ref"]), d["period"]


def settle(limit=8.0):
    """Wait until the map stops moving (two shots in a row nearly the same)."""
    from PIL import Image, ImageChops
    prev, t0 = None, time.time()
    while time.time() - t0 < limit:
        cur = Image.open(bg("shot", "--full", quiet=True).splitlines()[-1]).convert("L").crop(MAP_BOX)
        if prev is not None and sum(ImageChops.difference(cur, prev).histogram()[12:]) < 2000:
            return
        prev = cur
        time.sleep(0.3)


LASTZ = []                          # scale found by the last good snap: later snaps search near it only


def snap(path=None):
    """(S, x0, y0, match): screen x = x0 + ax*S/100 for atlas px ax (resnap find)."""
    ref, _ = atlas()
    path = path or bg("shot", "--full", quiet=True).splitlines()[-1]
    z = ["%.3f" % (LASTZ[0] * 0.96), "%.3f" % (LASTZ[0] * 1.04)] if LASTZ else ["1.2", "6"]
    out = subprocess.run(["python3", "-I", RESNAP, "find", ref, path, "--zoom", *z,
                          "--area", *map(str, MAP_BOX)], capture_output=True, text=True).stdout.split()
    S, x0, y0, m = float(out[1]), float(out[3]), float(out[5]), float(out[7])
    if m >= 0.5:
        LASTZ[:] = [S / 100]
    elif LASTZ:                     # lost it: forget the scale and search the whole range once
        LASTZ[:] = []
        return snap(path)
    return S, x0, y0, m


def to_world(sx, sy, sn):
    S, x0, y0, _ = sn
    (pw, ph) = atlas()[1]
    return ((sx - x0) * 100 / S) % pw, ((sy - y0) * 100 / S) % ph


def lookat(wx, wy, tries=3):
    pw, ph = atlas()[1]
    for _ in range(tries):
        sn = snap()
        if sn[3] < 0.5:
            sys.exit(f"snap failed (match {sn[3]:.2f}) - look at the screen")
        cx, cy = to_world(*CENTRE, sn)
        dx = (wx - cx + pw / 2) % pw - pw / 2           # shortest way round the wrapping world
        dy = (wy - cy + ph / 2) % ph - ph / 2
        px, py = dx * sn[0] / 100, dy * sn[0] / 100     # in screen pixels
        print(f"  view centre at world ({cx:.0f},{cy:.0f}), match {sn[3]:.2f}; pan {px:+.0f},{py:+.0f} px")
        if abs(px) < 40 and abs(py) < 40:
            break
        pan(px, py)
        settle()
    park()


def read_prov(num_expected=None):
    txt = bg("read", "province", "scout", quiet=True)
    m = re.search(r"\[province\]\s*\n\s*(.+?)\s*\((\d+)\)", txt)
    if not m:
        return None, txt
    return (m.group(1).strip(" *|"), int(m.group(2))), txt


def panel_record(name, num, txt, pt, world, tag):
    def field(lbl):
        f = re.search(lbl + r":\s*([^|\n]+)", txt)
        return f.group(1).strip() if f else ""
    sc = txt.split("[scout]", 1)[1] if "[scout]" in txt else ""
    sc = " ".join(w for w in sc.split() if w != "|")
    i = sc.find("Scout Report")
    return {"num": num, "name": name, "terrain": field("Terrain"), "full": "Population" in txt,
            "population": field("Population"), "income": field("Income"), "defence": field("Defence"),
            "unrest": field("Unrest"), "scout": sc[i:i + 300] if i >= 0 else "", "pt": list(pt),
            "world": world, "tag": tag, "t": time.strftime("%Y-%m-%d %H:%M")}


PANEL_CROP = (0, 85, 1912, 410)     # covers the scout report (left) and the province panel (right)


def screen_points(graph, sn, key="mark_world"):
    """{num: (x, y)} on screen for every province whose point is in the map part of this view."""
    pw, ph = atlas()[1]
    S, ox, oy, _ = sn
    x0b, y0b, x1b, y1b = MAP_BOX
    out = {}
    for k, pr in graph["provinces"].items():
        w = pr.get(key) or pr.get("world")
        if not w:
            continue
        for kx in range(-1, 4):
            for ky in range(-1, 4):
                sx = ox + (w[0] + kx * pw) * S / 100; sy = oy + (w[1] + ky * ph) * S / 100
                if x0b < sx < x1b and y0b < sy < y1b:
                    out[int(k)] = (int(sx), int(sy))
    return out


def labelshot(graph_path, out=None, key="mark_world"):
    from PIL import Image, ImageDraw
    g = json.load(open(graph_path))
    path = bg("shot", "--full", quiet=True).splitlines()[-1]
    sn = snap(path)
    if sn[3] < 0.5:
        sys.exit(f"snap failed ({sn[3]:.2f})")
    im = Image.open(path).convert("RGB")
    dr = ImageDraw.Draw(im)
    for num, (x, y) in screen_points(g, sn, key).items():
        dr.ellipse((x - 4, y - 4, x + 4, y + 4), outline=(255, 0, 255), width=2)
        dr.text((x + 6, y - 6), str(num), fill=(255, 0, 255))
    out = out or path.replace(".png", "_labels.png")
    im.save(out)
    print(out)


FLAG_BOX = (-45, -95, 55, -5)       # flag crop around a province marker, screen px at the working zoom


def flagsweep(graph_path, outdir, views=(3, 3)):
    from PIL import Image, ImageDraw
    g = json.load(open(graph_path))
    pw, ph = atlas()[1]
    os.makedirs(outdir, exist_ok=True)
    got = {int(f[:-4]): 1 for f in os.listdir(outdir) if f[:-4].isdigit()}     # resume: keep earlier crops
    for j in range(views[1]):
        for i in range(views[0]):
            lookat((i + 0.5) * pw / views[0], (j + 0.5) * ph / views[1])
            path = bg("shot", "--full", quiet=True).splitlines()[-1]
            sn = snap(path)
            if sn[3] < 0.5:
                continue
            im = Image.open(path).convert("RGB")
            x0b, y0b, x1b, y1b = MAP_BOX
            for num, (x, y) in screen_points(g, sn).items():
                b = (x + FLAG_BOX[0], y + FLAG_BOX[1], x + FLAG_BOX[2], y + FLAG_BOX[3])
                if num in got or b[0] < x0b or b[1] < y0b or b[2] > x1b or b[3] > y1b or (b[0] < 590 and b[1] < 235):
                    continue
                im.crop(b).save(os.path.join(outdir, f"{num}.png"))
                got[num] = 1
            print(f"  view {i},{j}: {len(got)} flags", flush=True)
    seq("key Home", "wait 800")
    park()
    nums = sorted(got)
    cw, chh, per = 100, 108, 16
    sheet = Image.new("RGB", (cw * per, chh * ((len(nums) + per - 1) // per)), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for k, n in enumerate(nums):
        x, y = (k % per) * cw, (k // per) * chh
        sheet.paste(Image.open(os.path.join(outdir, f"{n}.png")), (x, y))
        d.text((x + 2, y + 92), str(n), fill=(255, 255, 0))
    sheet.save(os.path.join(outdir, "sheet.png"))
    print(f"{len(nums)} flags -> {outdir}/sheet.png; missing: {sorted(set(map(int, g['provinces'])) - set(nums))}")


def view(num, graph_path=None):
    if not graph_path:
        graph_path = os.path.join(GAME, json.load(open(os.path.join(GAME, ".claude", "game-ui.json")))["atlas"]["graph"])
    g = json.load(open(graph_path))
    w = g["provinces"][str(num)]["world"]
    lookat(*w)
    sn = snap()
    pt = screen_points({"provinces": {str(num): g["provinces"][str(num)]}}, sn, "world").get(num)
    if not pt:
        sys.exit(f"province {num} not on screen after lookat")
    seq(f"move {pt[0]} {pt[1]}", "wait 150", f"click {pt[0]} {pt[1]} --right", "wait 800")
    got, _ = read_prov()
    park()
    print(f"viewing {got}" if got and got[1] == num else f"WRONG province: panel says {got}, wanted {num}")
    return got and got[1] == num


def ocr_panel(path):
    """Panel + scout text of one saved full screenshot (same OCR as bgplay read)."""
    from PIL import Image
    sys.path.insert(0, os.path.dirname(BG))
    import ocr as O
    regions = json.load(open(os.path.join(GAME, ".claude", "game-ui.json")))["regions"]
    im = Image.open(path)
    dx, dy = PANEL_CROP[:2] if os.path.basename(path).startswith("crop_") else (0, 0)
    out = []
    for n in ("province", "scout"):
        r = regions[n]
        b = (r[0] - dx, r[1] - dy, r[2] - dx, r[3] - dy)
        out.append(f"[{n}]\n" + O.ocr(O.prepare(im, b, scale=2, dark="dark" in r[4:]), psm=6).strip())
    return "\n".join(out)


def provsweep(graph, out, views=(3, 3), redo=False, settle_ms=350):
    """Fast: per view ONE driver call right-clicks every province centre and photographs each panel;
    the OCR runs afterwards on the photos, in parallel, off the game. Wrong or unread panels get a
    second, slower pass."""
    from concurrent.futures import ThreadPoolExecutor
    g = json.load(open(graph))
    if "fit" not in g:
        sys.exit("graph not fitted: provgraph.py fit GRAPH SWEEP.jsonl first")
    pw, ph = atlas()[1]
    done = set()
    if os.path.exists(out) and not redo:
        for line in open(out):
            try:
                done.add(json.loads(line)["num"])
            except Exception:
                pass
    todo = {int(k): v["world"] for k, v in g["provinces"].items() if v.get("world") and int(k) not in done}
    print(f"{len(todo)} provinces to read ({len(done)} already in {out})", flush=True)
    t0 = time.time()
    vx, vy = views
    x0b, y0b, x1b, y1b = MAP_BOX
    m = 30
    for attempt, wait in ((1, settle_ms), (2, settle_ms * 3)):
        shots = []                                   # (num, pt, world, view, path)
        for j in range(vy):
            for i in range(vx):
                if not todo:
                    break
                wc = ((i + 0.5) * pw / vx, (j + 0.5) * ph / vy)
                if LASTZ:                            # skip a view with nothing left to read in it
                    hw = (x1b - x0b) / 2 / LASTZ[0] / 1.0 + 5; hh = (y1b - y0b) / 2 / LASTZ[0] + 5
                    inside = [n for n, (wx, wy) in todo.items() if n not in {h[0] for h in shots}
                              and abs((wx - wc[0] + pw / 2) % pw - pw / 2) < hw
                              and abs((wy - wc[1] + ph / 2) % ph - ph / 2) < hh]
                    if not inside:
                        continue
                lookat(*wc)
                sn = snap()
                if sn[3] < 0.5:
                    print(f"  view {i},{j}: snap failed ({sn[3]:.2f}), skipped", flush=True); continue
                S, ox, oy, _ = sn
                here, steps = [], []
                for num, (wx, wy) in sorted(todo.items()):
                    if any(num == h[0] for h in shots):
                        continue
                    pt = None
                    for kx in range(-1, 4):
                        for ky in range(-1, 4):
                            sx = ox + (wx + kx * pw) * S / 100; sy = oy + (wy + ky * ph) * S / 100
                            if x0b + m < sx < x1b - m and y0b + m < sy < y1b - m and not (sx < 590 and sy < 235):
                                pt = (int(sx), int(sy))
                    if pt:
                        here.append((num, pt, [wx, wy]))
                        steps += [f"move {pt[0]} {pt[1]}", f"click {pt[0]} {pt[1]} --right", f"wait {wait}", "shot --box " + " ".join(map(str, PANEL_CROP))]
                if not steps:
                    continue
                paths = [l for l in bg("seq", *steps, quiet=True).splitlines() if l.endswith(".png")]
                for (num, pt, w), path in zip(here, paths):
                    shots.append((num, pt, w, f"view{i}{j}", path))
                print(f"  view {i},{j}: {len(here)} provinces photographed ({time.time() - t0:.0f} s)", flush=True)
        with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as ex:
            texts = list(ex.map(lambda r: ocr_panel(r[4]), shots))
        bad = 0
        for (num, pt, w, tag, path), txt in zip(shots, texts):
            mm = re.search(r"\[province\]\s*\n\s*(.+?)\s*\((\d+)\)", txt)
            if not mm or int(mm.group(2)) != num:
                bad += 1; continue
            rec = panel_record(mm.group(1).strip(" *|"), num, txt, pt, w, tag)
            open(out, "a").write(json.dumps(rec) + "\n")
            todo.pop(num, None)
        print(f"pass {attempt}: {len(shots) - bad} read, {bad} wrong/unread ({time.time() - t0:.0f} s)", flush=True)
        if not todo:
            break
    seq("key Home", "wait 800")
    park()
    print(f"left unread: {sorted(todo)}" if todo else "every province read", flush=True)


def sweep(out, step=130, tag=""):
    seen = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                seen.add(json.loads(line)["num"])
            except Exception:
                pass
    new = 0
    sn = snap()
    print(f"  view snapped on the atlas, match {sn[3]:.2f}")
    x0, y0, x1, y1 = MAP_BOX
    for y in range(y0 + step // 2, y1, step):
        for x in range(x0 + step // 2, x1, step):
            if x < 590 and y < 235:             # the Scout Report box sits there when shown
                continue
            seq(f"move {x} {y}", "wait 150", f"click {x} {y} --right", "wait 700")
            txt = bg("read", "province", "scout", quiet=True)
            m = re.search(r"\[province\]\s*\n\s*(.+?)\s*\((\d+)\)", txt)
            if not m:
                continue
            num = int(m.group(2))
            if num in seen:
                continue
            seen.add(num)
            ter = re.search(r"Terrain:\s*([^|\n]+)", txt)
            sc = txt.split("[scout]", 1)[1] if "[scout]" in txt else ""
            sc = " ".join(w for w in sc.split() if w != "|")
            rec = {"num": num, "name": m.group(1).strip(" *|"), "terrain": ter.group(1).strip() if ter else "",
                   "full": "Population" in txt, "scout": sc[:300], "pt": [x, y], "tag": tag,
                   "world": [round(v) for v in to_world(x, y, sn)] if sn[3] >= 0.5 else None,
                   "t": time.strftime("%Y-%m-%d %H:%M")}
            open(out, "a").write(json.dumps(rec) + "\n")
            new += 1
            print(f"{num:4d} {rec['name'][:28]:28s} {rec['terrain'][:22]:22s} {'panel' if rec['full'] else '-':5s} {sc[:60]}")
    park()
    print(f"{new} new provinces, {len(seen)} known -> {out}")


def main(a):
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "look":
        look()
    elif c == "read":
        read(*a[1:])
    elif c == "park":
        park()
    elif c == "capital":
        seq("key Home", "wait 1200")
        look()
    elif c == "zoom":
        n = int(a[2]) if len(a) > 2 else 3
        seq(f"move {MAPC[0]} {MAPC[1]}", f"scroll {'down' if a[1] == 'out' else 'up'} {n} {MAPC[0]} {MAPC[1]}", "wait 1000")
        park()
        shot()
    elif c == "mapshot":
        n = int(a[1]) if len(a) > 1 else 3
        seq(f"move {MAPC[0]} {MAPC[1]}", f"scroll down {n} {MAPC[0]} {MAPC[1]}", "wait 1200")
        park()
        p = shot()
        seq(f"move {MAPC[0]} {MAPC[1]}", f"scroll up {n} {MAPC[0]} {MAPC[1]}", "wait 1000")
        park()
        print("map photo:", p)
    elif c == "messages":
        seq("key m", "wait 1500")
        shot()
        read("dialog")
    elif c == "goto":
        p = shot()
        row = find_text(p, a[1])
        if not row:
            sys.exit(f"no message row containing {a[1]!r}")
        hit = find_text(p, "Goto province")
        if not hit:
            sys.exit("no 'Goto province' on screen")
        # the Goto link on the same row as the message text
        sys.path.insert(0, HERE)
        x = hit[0]
        seq(f"move {x} {row[1]}", "wait 400", f"click {x} {row[1]}", "wait 1800")
        look()
    elif c == "exitdialog":
        p = shot()
        hit = find_text(p, "Exit")
        if not hit:
            sys.exit("no Exit on screen - not pressing Esc (Esc opens Options)")
        seq(f"move {hit[0]} {hit[1]}", "wait 300", f"click {hit[0]} {hit[1]}", "wait 1200")
        park()
        shot()
    elif c == "pan":
        pan(int(a[1]), int(a[2]))
        park()
        shot()
    elif c == "snap":
        sn = snap()
        print("view centre at world (%.0f,%.0f), scale %.1f, match %.2f" % (*to_world(*CENTRE, sn), sn[0], sn[3]))
    elif c == "lookat":
        lookat(float(a[1]), float(a[2]))
        shot()
    elif c == "flagsweep":
        v = a[a.index("--views") + 1].split("x") if "--views" in a else ("3", "3")
        flagsweep(a[1], a[2], (int(v[0]), int(v[1])))
    elif c == "view":
        gp = a[a.index("--graph") + 1] if "--graph" in a else None
        view(int(a[1]), gp)
    elif c == "labelshot":
        o = [x for x in a[2:] if not x.startswith("--") and x not in ("mark", "world")]
        labelshot(a[1], o[0] if o else None, "world" if "world" in a[2:] else "mark_world")
    elif c == "provsweep":
        v = a[a.index("--views") + 1].split("x") if "--views" in a else ("3", "3")
        provsweep(a[1], a[2], (int(v[0]), int(v[1])), "--redo" in a)
    elif c == "sweep":
        o = dict(zip(a[2::2], a[3::2]))
        sweep(a[1], int(o.get("--step", 130)), o.get("--tag", ""))
    elif c == "battle":
        br = os.path.join(GAME, ".claude", "skills", "dom6-battle-view", "scripts", "battle_review.py")
        subprocess.run(["python3", "-I", br, "record", a[1]], env=dict(os.environ, DISPLAY=DISP))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
