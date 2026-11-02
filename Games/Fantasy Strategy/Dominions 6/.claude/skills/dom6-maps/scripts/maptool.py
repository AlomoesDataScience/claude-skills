"""Check and install Dominions 6 maps (from MapNuke or anywhere else).

  python3 -I maptool.py check PATH            PATH = a .map file or the folder holding it
  python3 -I maptool.py install PATH [--force]   copy into ~/.dominions6/maps/<Name>/ (checks first)
  python3 -I maptool.py list                  maps installed in ~/.dominions6/maps

check: #dom2title first, image files present and as big as #mapsize, one pure white pixel per
province (#terrain lines), neighbours point at real provinces, nobody is cut off, starts and
allowed players, thrones, cave gates, extra planes (_plane2...), the name rules. Rules are from
Illwinter's Dom6 Map Making Manual (dom6mapman.pdf).
"""
import os
import re
import shutil
import sys
from collections import Counter

from PIL import Image

MAPS = os.path.expanduser("~/.dominions6/maps")
# terrain mask bits (manual, Terrain Types table)
TERRAIN = [(1, "small"), (2, "large"), (4, "sea"), (8, "freshwater"), (16, "highland"),
           (32, "swamp"), (64, "waste"), (128, "forest"), (256, "farm"), (512, "nostart"),
           (1024, "manysites"), (2048, "deep"), (4096, "cave"), (8388608, "mountains"),
           (33554432, "good throne"), (67108864, "good start"), (134217728, "bad throne"),
           (2 ** 30, "warmer"), (2 ** 31, "colder"), (68719476736, "cave wall")]
SPEC = {1: "mountain pass", 2: "river", 4: "impassable", 8: "road"}
# terrain-look images the game reads next to the main one (manual, The Map Image File)
LOOKS = ("winter", "forest", "waste", "farm", "swamp", "highland", "plain", "kelp", "water")


def find_map(path):
    if os.path.isdir(path):
        maps = sorted(f for f in os.listdir(path) if f.endswith(".map") and "_plane" not in f)
        if len(maps) != 1:
            sys.exit(f"{path}: expected one main .map file, found {maps}")
        return os.path.join(path, maps[0])
    return path


def plane_maps(main):
    """The main .map and its extra planes (name_plane2.map ... name_plane8.map)."""
    base = main[:-4]
    return [main] + [f"{base}_plane{n}.map" for n in range(2, 9) if os.path.exists(f"{base}_plane{n}.map")]


def images_for(mapfile):
    """Every image file the game may read for this .map: #imagefile, #winterimagefile and the
    terrain looks (name_forest.tga, name_forestw.tga, ...), .tga or .rgb."""
    folder, base = os.path.split(mapfile[:-4])
    text = open(mapfile, encoding="latin-1").read()
    named = re.findall(r"^#(?:imagefile|winterimagefile)\s+(\S+)", text, re.M)
    looks = [f for f in os.listdir(folder)
             if re.fullmatch(re.escape(base) + r"_(%s)w?\.(tga|rgb)" % "|".join(LOOKS), f)]
    return sorted(set(named) | set(looks))


def check_plane(mapfile, problems, notes):
    name = os.path.basename(mapfile)
    folder = os.path.dirname(mapfile)
    text = open(mapfile, encoding="latin-1").read()
    cmds = [l.split()[0] for l in text.splitlines() if l.startswith("#")]
    if "_plane" not in name and (not cmds or cmds[0] != "#dom2title"):
        problems.append(f"{name}: #dom2title must be the first command (found {cmds[:1]})")
    m = re.search(r"^#imagefile\s+(\S+)", text, re.M)
    size = re.search(r"^#mapsize\s+(\d+)\s+(\d+)", text, re.M)
    if not m or not size:
        problems.append(f"{name}: needs #imagefile and #mapsize")
        return
    img = os.path.join(folder, m.group(1))
    if not os.path.exists(img):
        problems.append(f"{name}: image {m.group(1)} is missing")
        return
    im = Image.open(img).convert("RGB")
    w, h = im.size
    if (w, h) != (int(size.group(1)), int(size.group(2))):
        problems.append(f"{name}: #mapsize {size.group(1)}x{size.group(2)} but the image is {w}x{h}")
    for f in images_for(mapfile):
        p = os.path.join(folder, f)
        if not os.path.exists(p):
            problems.append(f"{name}: {f} is named but missing")
        elif Image.open(p).size != (w, h):
            problems.append(f"{name}: {f} is {Image.open(p).size}, not {w}x{h}")
    px = im.tobytes()
    white = sum(1 for i in range(0, len(px), 3) if px[i:i + 3] == b"\xff\xff\xff")

    terr = {int(a): int(b) for a, b in re.findall(r"^#terrain\s+(\d+)\s+(\d+)", text, re.M)}
    if white != len(terr):
        problems.append(f"{name}: {white} white province pixels but {len(terr)} #terrain lines")
    if terr and sorted(terr) != list(range(1, len(terr) + 1)):
        problems.append(f"{name}: province numbers are not 1..{len(terr)}")
    nb = [(int(a), int(b)) for a, b in re.findall(r"^#neighbour\s+(\d+)\s+(\d+)", text, re.M)]
    bad = [p for p in nb if p[0] not in terr or p[1] not in terr]
    if bad:
        problems.append(f"{name}: {len(bad)} #neighbour lines name unknown provinces, e.g. {bad[:3]}")
    # a border may be listed once or both ways: count unordered pairs
    borders = {tuple(sorted(p)) for p in nb if p[0] != p[1]}
    deg = Counter(x for b in borders for x in b)
    lonely = [p for p in terr if deg[p] == 0]
    if lonely:
        problems.append(f"{name}: provinces with no neighbours: {lonely[:10]}")
    specs = {}
    for a, b, k in re.findall(r"^#neighbourspec\s+(\d+)\s+(\d+)\s+(\d+)", text, re.M):
        pair = tuple(sorted((int(a), int(b))))
        if pair not in borders:
            problems.append(f"{name}: #neighbourspec {a} {b} is not a #neighbour pair")
        specs[pair] = SPEC.get(int(k), k)
    spec = Counter(specs.values())
    kinds = Counter()
    for v in terr.values():
        for bit, label in TERRAIN:
            if v & bit:
                kinds[label] += 1
        if not v & (4 | 4096 | 68719476736 | 0x1F0):
            kinds["plains"] += 1
    starts = re.findall(r"^#specstart\s+(\d+)\s+(\d+)", text, re.M)
    for nat, prov in starts:
        if int(prov) not in terr:
            problems.append(f"{name}: #specstart {nat} {prov} names an unknown province")
    gates = re.findall(r"^#gate\s+(\d+)\s+(\d+)", text, re.M)
    notes.append(f"{name}: {w}x{h}, {len(terr)} provinces, {len(borders)} borders "
                 f"({', '.join(f'{n} {k}' for k, n in spec.most_common()) or 'no special borders'})")
    notes.append(f"  terrain: {', '.join(f'{n} {k}' for k, n in kinds.most_common())}")
    if starts:
        notes.append(f"  #specstart (nation province): {', '.join(' '.join(s) for s in starts)}")
    ap = re.findall(r"^#allowedplayer\s+(\d+)", text, re.M)
    if ap:
        notes.append(f"  #allowedplayer: {', '.join(ap)}")
    if gates:
        notes.append(f"  cave gates: {len(gates)}")
    for flag in ("#wraparound", "#hwraparound", "#vwraparound", "#nodeepcaves", "#nodeepchoice", "#mapnohide"):
        if re.search(rf"^{flag}\b", text, re.M):
            notes.append(f"  {flag}")


def check(path):
    main = find_map(path)
    problems, notes = [], []
    base = os.path.basename(main)[:-4]
    folder = os.path.basename(os.path.dirname(os.path.abspath(main)))
    if not re.fullmatch(r"[A-Za-z_]+", base):
        problems.append(f"map name {base!r}: use only a-z, A-Z and _")
    if folder != base and os.path.dirname(os.path.abspath(main)).startswith(MAPS):
        problems.append(f"installed in folder {folder!r}: the folder must be named {base!r}")
    for pm in plane_maps(main):
        check_plane(pm, problems, notes)
    print("\n".join(notes))
    print("\n".join(f"PROBLEM: {p}" for p in problems) if problems else "OK: no problems found")
    return main, problems


def install(path, force=False):
    main, problems = check(path)
    if problems:
        sys.exit("not installed: fix the problems first")
    base = os.path.basename(main)[:-4]
    dest = os.path.join(MAPS, base)
    if os.path.exists(dest) and not force:
        sys.exit(f"{dest} exists; --force replaces its files (a map in an ongoing game only changes its look)")
    os.makedirs(dest, exist_ok=True)
    src = os.path.dirname(os.path.abspath(main))
    files = []
    for pm in plane_maps(main):
        files += [os.path.basename(pm)] + images_for(pm)
    for f in sorted(set(files)):
        shutil.copy2(os.path.join(src, f), os.path.join(dest, f))
    print(f"installed {len(set(files))} files to {dest}: {', '.join(sorted(set(files)))}")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, a = argv[0], argv[1:]
    if cmd == "check" and a:
        check(a[0])
    elif cmd == "install" and a:
        install(a[0], "--force" in a)
    elif cmd == "list":
        for d in sorted(os.listdir(MAPS)) if os.path.isdir(MAPS) else []:
            print(d)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
