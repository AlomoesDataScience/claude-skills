"""Look at a unit's model large, before it is shrunk to a 64 px sprite.

    python3 -I inspect_pose.py GEN.py UNIT OUT.png [--zoom 4] [--poses 1,2] [--views sprite,front,side]

GEN.py is a standalone generator from build.sh (or a nation's <nation>_sprites.py). For every pose
it renders the same model at ZOOM x resolution through the sprite camera, face-on (yaw 0) and in
profile (yaw -90), with the usual cel shading and ink, and lays them out on one labelled sheet,
next to the real 64 px sprite. Use it to see hidden limbs, props lost behind the body or a pose
that reads wrong, then fix the pose and check the small sprite again.
"""
import importlib.util
import sys

from PIL import Image, ImageDraw

VIEWS = {"sprite": None, "front": 0.0, "side": -90.0, "back": 150.0}


def load(path):
    spec = importlib.util.spec_from_file_location("gen", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen"] = mod              # the render pool pickles functions by module name
    spec.loader.exec_module(mod)
    return mod


def zoomed(gen, unit, z, yaw):
    """Register a copy of UNIT drawn z times larger (optionally from another yaw)."""
    U = dict(gen.UNITS[unit])
    r = U.get("res", 64)
    rw, rh = (r, r) if isinstance(r, int) else r
    U["res"] = (rw * z, rh * z)
    U["scale"] = U.get("scale", 1.0) * z
    U["cx"] = U.get("cx", rw / 2) * z
    U["y0"] = U.get("y0", rh - 2.4) * z
    sh = U.get("shadow", (23, 41))
    U["shadow"] = (sh[0] * z, sh[1] * z) if sh else None
    U["free_rows"] = False
    if yaw is not None:
        U["yaw"] = yaw
    key = f"{unit}@{z}@{yaw}"
    gen.UNITS[key] = U
    return key


def main():
    a = sys.argv[1:]
    opt = {"--zoom": "4", "--poses": "", "--views": "sprite,front,side"}
    pos = []
    while a:
        x = a.pop(0)
        if x in opt:
            opt[x] = a.pop(0)
        else:
            pos.append(x)
    gen_path, unit, out = pos
    gen = load(gen_path)
    z = int(opt["--zoom"])
    poses = opt["--poses"].split(",") if opt["--poses"] else list(gen.UNITS[unit]["poses"])
    views = opt["--views"].split(",")
    cells = []
    for p in poses:
        row = [("64 px " + p, gen.sprite(unit, p).resize((64 * z, 64 * z), Image.NEAREST))]
        for v in views:
            key = zoomed(gen, unit, z, VIEWS[v])
            row.append((f"{v} {p}", gen.sprite(key, p, ss=2)))
        cells.append(row)
    w = max(sum(im.width for _, im in row) + 6 * len(row) for row in cells)
    h = sum(max(im.height for _, im in row) + 18 for row in cells)
    sheet = Image.new("RGB", (w, h), (52, 84, 52))
    d = ImageDraw.Draw(sheet)
    y = 0
    for row in cells:
        x = 0
        for label, im in row:
            d.text((x + 2, y + 2), label, fill=(255, 255, 0))
            sheet.paste(im, (x, y + 16))
            x += im.width + 6
        y += max(im.height for _, im in row) + 18
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
