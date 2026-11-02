"""Build the double-clickable Sprite Studio app.

  python3 tools/build.py

Writes, in the spritestudio folder:
  SpriteStudio            one executable file (a Python zip app: server, engine, web page,
                          and the killbot as a starter model). Needs python3 and Pillow.
  Sprite Studio.desktop   desktop launcher with an icon (double-click it, or copy it to
                          ~/.local/share/applications/ to get a menu entry)
  icon.png                the launcher icon (the killbot sprite, enlarged)

Run it again after changing the code; the app unpacks each new build automatically.
"""
import hashlib
import io
import os
import stat
import sys
import zipfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "SpriteStudio")
FILES = ["server.py", "engine", "web"]
SEED = ["models/killbot.json"]


def collect():
    """(path inside the app, bytes) for every file the app needs."""
    items = []
    for top in FILES:
        src = os.path.join(ROOT, top)
        if os.path.isfile(src):
            items.append((top, src))
            continue
        for d, dirs, files in os.walk(src):
            dirs[:] = sorted(x for x in dirs if x != "__pycache__")
            for f in sorted(files):
                if not f.endswith(".pyc"):
                    p = os.path.join(d, f)
                    items.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), p))
    for s in SEED:
        items.append(("seed/" + os.path.basename(s), os.path.join(ROOT, s)))
    return [(n, open(p, "rb").read()) for n, p in items]


def icon():
    """Killbot idle sprite on a transparent square, scaled up with hard pixels."""
    spr = Image.open(os.path.join(ROOT, "output", "killbot", "killbot1.tga")).convert("RGB")
    rgba = Image.new("RGBA", spr.size, (0, 0, 0, 0))
    px, out = spr.load(), rgba.load()
    for y in range(spr.height):
        for x in range(spr.width):
            if px[x, y] not in ((0, 0, 0), (255, 0, 255)):
                out[x, y] = px[x, y] + (255,)
    box = rgba.getbbox()
    side = max(box[2] - box[0], box[3] - box[1]) + 4
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(rgba.crop(box), ((side - (box[2] - box[0])) // 2, (side - (box[3] - box[1])) // 2))
    sq.resize((side * 6, side * 6), Image.NEAREST).save(os.path.join(ROOT, "icon.png"))


def main():
    files = collect()
    build = hashlib.sha256(b"".join(n.encode() + b for n, b in files)).hexdigest()[:12]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("__main__.py", open(os.path.join(ROOT, "tools", "launcher.py"), "rb").read())
        z.writestr("app/BUILD", build)
        for n, b in files:
            z.writestr("app/" + n, b)
    tmp = OUT + ".tmp"
    with open(tmp, "wb") as f:
        f.write(b"#!/usr/bin/env python3\n")
        f.write(buf.getvalue())
    os.chmod(tmp, os.stat(tmp).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    os.replace(tmp, OUT)
    icon()
    desk = os.path.join(ROOT, "Sprite Studio.desktop")
    with open(desk, "w") as f:
        f.write("[Desktop Entry]\nType=Application\nName=Sprite Studio\n"
                "Comment=Dominions 6 sprite editor\n"
                f'Exec="{OUT}"\nIcon={os.path.join(ROOT, "icon.png")}\n'
                f"Path={ROOT}\nTerminal=false\nCategories=Graphics;Game;\n")
    os.chmod(desk, 0o755)
    print(f"built {OUT}  ({os.path.getsize(OUT) // 1024} KB, {len(files)} files, build {build})")


if __name__ == "__main__":
    sys.exit(main())
