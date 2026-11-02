"""Find town dots and capital stars on a printed map: small very dark blobs; a ring around = capital."""
from PIL import Image


def find_cities(im, dark=45, max_px=30, max_box=7):
    L = im.convert("L")
    W, H = L.size
    px = L.load()
    seen = set()
    out = []
    for y in range(6, H - 6):
        for x in range(6, W - 6):
            if px[x, y] >= dark or (x, y) in seen:
                continue
            comp, q = [], [(x, y)]
            seen.add((x, y))
            while q and len(comp) <= max_px:
                a, b = q.pop()
                comp.append((a, b))
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        p = (a + i, b + j)
                        if p not in seen and 0 <= p[0] < W and 0 <= p[1] < H and px[p] < dark:
                            seen.add(p)
                            q.append(p)
            if len(comp) > max_px or len(comp) < 3:
                continue
            xs = [p[0] for p in comp]
            ys = [p[1] for p in comp]
            if max(xs) - min(xs) >= max_box or max(ys) - min(ys) >= max_box:
                continue
            cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
            ring = [px[int(cx + 5 * dx), int(cy + 5 * dy)] for dx, dy in
                    ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))
                    if 0 <= cx + 5 * dx < W and 0 <= cy + 5 * dy < H]
            darkring = sum(1 for v in ring if v < 140)
            out.append((round(cx), round(cy), "capital" if darkring >= 4 else "town"))
    return out


if __name__ == "__main__":
    import sys
    from PIL import ImageDraw
    im = Image.open(sys.argv[1]).convert("RGB")
    cs = find_cities(im)
    d = ImageDraw.Draw(im)
    for x, y, k in cs:
        r = 7 if k == "capital" else 5
        d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 0, 0) if k == "capital" else (255, 0, 255), width=2)
    im.save(sys.argv[2])
    print(len(cs), "found:", sum(k == "capital" for *_, k in cs), "capitals")
