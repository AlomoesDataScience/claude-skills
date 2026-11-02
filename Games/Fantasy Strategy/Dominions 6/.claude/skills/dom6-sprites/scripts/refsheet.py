"""Contact sheet of spr1/spr2 pairs from a Dominions Enhanced (or any mod) folder, for picking stances.

  python3 -I refsheet.py OUT.png ROOT [nation ...] [--size 64] [--max 72] [--seed 6]

Finds name/name2 and name1/name2 pairs of the given canvas size, shuffles them,
and labels each with its index and path so a stance can be cited ("venedia/admiral").
"""
import os
import random
import sys

from PIL import Image, ImageDraw

args = sys.argv[1:]
opt = {"--size": 64, "--max": 72, "--seed": 6}
for k in list(opt):
    if k in args:
        i = args.index(k)
        opt[k] = int(args[i + 1])
        del args[i:i + 2]
out, root, nations = args[0], args[1], args[2:] or sorted(
    n for n in os.listdir(args[1]) if os.path.isdir(os.path.join(args[1], n)))
pairs = []
for nat in nations:
    fs = set(os.listdir(os.path.join(root, nat)))
    for f in sorted(fs):
        if not f.endswith(".tga"):
            continue
        b = f[:-4]
        c = b[:-1] + "2" if b.endswith("1") else b + "2"
        if c == b or c + ".tga" not in fs:
            continue
        try:
            if Image.open(os.path.join(root, nat, f)).size == (opt["--size"],) * 2:
                pairs.append((nat, b, c))
        except Exception:
            pass
random.seed(opt["--seed"])
random.shuffle(pairs)
pairs = pairs[:opt["--max"]]
s, z, cols = opt["--size"], 2 if opt["--size"] <= 64 else 1, 6
cw, ch = 2 * s * z + 6, s * z + 12
W = Image.new("RGB", (cols * cw, ((len(pairs) + cols - 1) // cols) * ch), (40, 70, 40))
d = ImageDraw.Draw(W)
for k, (nat, a, c) in enumerate(pairs):
    x, y = (k % cols) * cw, (k // cols) * ch
    for i, n in enumerate((a, c)):
        im = Image.open(os.path.join(root, nat, n + ".tga")).convert("RGB").resize((s * z, s * z), Image.NEAREST)
        W.paste(im, (x + i * s * z, y + 10))
    d.text((x + 2, y), f"{k} {nat}/{a}", fill=(255, 255, 0))
W.save(out)
print("\n".join(f"{k} {n}/{a} {c}" for k, (n, a, c) in enumerate(pairs)))
