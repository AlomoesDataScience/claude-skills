
# ---------------------------------------------------------------- camera
YAW, PITCH = -30.0, 8.0   # three-quarter view facing left (the game reads this as the move direction)
RES = 64
K0 = 34.6 / 1.73          # sprite pixels per metre for a 1.73 m human: ~35 px tall
CX, Y0 = 32.0, 61.6       # sprite position of the model origin (feet on row 61)
K = K0


def cam_matrix(yaw=YAW, pitch=PITCH):
    a, b = math.radians(yaw), math.radians(pitch)
    ry = ((cos(a), 0, sin(a)), (0, 1, 0), (-sin(a), 0, cos(a)))
    rx = ((1, 0, 0), (0, cos(b), -sin(b)), (0, sin(b), cos(b)))
    return tuple(tuple(sum(rx[i][k] * ry[k][j] for k in range(3)) for j in range(3)) for i in range(3))


A = cam_matrix()


def to_model(v):
    return tuple(v[0] * A[0][j] + v[1] * A[1][j] + v[2] * A[2][j] for j in range(3))


def to_cam(v):
    return tuple(dot(A[i], v) for i in range(3))


DIR = to_model((0, 0, -1))
VIEW = mul(DIR, -1)
LIGHT = norm(to_model(norm((-0.65, 0.65, 0.4))))

SCENE = None


def sdf(x, y, z, groups):
    best, bm, bg = 1e9, 0, None
    for g in groups:
        c = g.c
        bd = sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2 + (z - c[2]) ** 2) - g.R
        if bd >= best:
            continue
        if bd > 0.02:
            best, bm = bd, 0
            continue
        d, m = g.eval(x, y, z)
        if d < best:
            best, bm, bg = d, m, g
    return best, bm, bg


def dist(p):
    return sdf(p[0], p[1], p[2], SCENE)[0]


def normal(p):
    e = 0.0006
    n = (0.0, 0.0, 0.0)
    for v in ((1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, 1, 1)):
        n = add(n, mul(v, dist(add(p, mul(v, e)))))
    return norm(n)


def hard_shadow(p, l):
    t = 0.015
    for _ in range(64):
        d = dist(add(p, mul(l, t)))
        if d < 0.0006:
            return 0.0
        t += max(min(d, 0.1), 0.004)
        if t > 2.0:
            break
    return 1.0


def shade(p, mat):
    n = normal(p)
    if mat in EMISSIVE:
        edge, core = EMISSIVE[mat]
        return lerp(edge, core, min(1.0, max(dot(n, VIEW), 0.0) ** 2 * 1.4))
    lit, mid, deep = PALETTE[mat]
    v = max(dot(n, LIGHT), 0.0)
    if v > 0.1:
        v *= hard_shadow(add(p, mul(n, 0.004)), LIGHT)
    # four painted tones: highlight, lit, shade, deep shade
    if v > 0.75:
        return lerp(lit, (255, 255, 255), 0.16)
    if v > 0.38:
        return lit
    if v > 0.1:
        return mid
    return deep


def trace(x_cam, y_cam):
    """Returns (rgb, material, depth) for one ray; material 0 is a miss."""
    o = to_model((x_cam, y_cam, 4.0))
    cands = []
    for g in SCENE:
        c = to_cam(g.c)
        if (c[0] - x_cam) ** 2 + (c[1] - y_cam) ** 2 <= g.R * g.R:
            cands.append(g)
    if not cands:
        return (0, 0, 0), 0, 1e9
    t = max(min(4.0 - to_cam(g.c)[2] - g.R for g in cands), 0.0)
    tend = max(4.0 - to_cam(g.c)[2] + g.R for g in cands)
    for _ in range(300):
        p = add(o, mul(DIR, t))
        d, m, g = sdf(p[0], p[1], p[2], cands)
        if d < 0.0004 and m:
            return shade(p, m), m, t
        t += max(d * 0.7, 0.0002)
        if t > tend:
            break
    return (0, 0, 0), 0, 1e9


def render_rows(args):
    rows, scale, w = args
    out = []
    for j in rows:
        line = []
        for i in range(w):
            u = (i + 0.5) / scale
            v = (j + 0.5) / scale
            line.append(trace((u - CX) / K, (Y0 - v) / K))
        out.append((j, line))
    return out


def setup(unit):
    """Canvas and camera for this unit. res: 64 (men), 128 (big units) or (w, h) such as
    (128, 64) for long beasts and vehicles; feet 2 px above the bottom. yaw/pitch re-aim the
    camera (e.g. yaw 0 for a face-on flag)."""
    global K, RW, RH, CX, Y0, A, DIR, VIEW, LIGHT
    U = UNITS[unit]
    r = U.get("res", 64)
    RW, RH = (r, r) if isinstance(r, int) else r
    K = K0 * U.get("scale", 1.0)
    CX, Y0 = U.get("cx", RW / 2), U.get("y0", RH - 2.4)
    A = cam_matrix(U.get("yaw", YAW), U.get("pitch", PITCH))
    DIR = to_model((0, 0, -1))
    VIEW = mul(DIR, -1)
    LIGHT = norm(to_model(norm((-0.65, 0.65, 0.4))))


def init(unit, pose):
    global SCENE
    setup(unit)
    SCENE = build(unit, pose)


def render(unit, pose, ss):
    nx, ny = RW * ss, RH * ss
    jobs = [(list(range(j, min(j + 4, ny))), ss, nx) for j in range(0, ny, 4)]
    with Pool(int(os.environ.get("SPRITE_WORKERS", os.cpu_count())), initializer=init, initargs=(unit, pose)) as pool:
        rows = {}
        for chunk in pool.imap_unordered(render_rows, jobs):
            for j, line in chunk:
                rows[j] = line
    return [rows[j] for j in range(ny)]


# ---------------------------------------------------------------- sprite output
INK = (30, 26, 32)


def sprite(unit, pose, ss=6):
    U = UNITS[unit]
    setup(unit)
    hi = render(unit, pose, ss)
    nx, ny = RW * ss, RH * ss
    # ink only where a nearer part overlaps a clearly farther one: at 35 px tall,
    # finer contour lines would turn to noise
    offs = [(dx, dy) for dx in range(-3, 4) for dy in range(-3, 4) if 0 < dx * dx + dy * dy <= 9]
    ink = [[False] * nx for _ in range(ny)]
    for j in range(ny):
        for i in range(nx):
            c, m, dep = hi[j][i]
            if not m or m in EMISSIVE:
                continue
            for di, dj in offs:
                ii, jj = i + di, j + dj
                if 0 <= ii < nx and 0 <= jj < ny:
                    c2, m2, d2 = hi[jj][ii]
                    if m2 and m2 not in EMISSIVE and d2 > dep + 0.07:
                        ink[j][i] = True
                        break

    out = Image.new("RGB", (RW, RH), (0, 0, 0))
    o = out.load()
    solid = [[0] * RW for _ in range(RH)]            # 0 empty, 1 body, else the glowing material
    col = [[None] * RW for _ in range(RH)]
    for y in range(RH):
        for x in range(RW):
            acc, cnt, glow = [0.0, 0.0, 0.0], 0, {}
            for j in range(ss):
                for i in range(ss):
                    c, m, _ = hi[y * ss + j][x * ss + i]
                    if m:
                        if ink[y * ss + j][x * ss + i]:
                            c = INK
                        cnt += 1
                        if m in EMISSIVE:
                            glow[m] = glow.get(m, 0) + 1
                        acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            if cnt / (ss * ss) >= 0.42:
                gm = max(glow, key=glow.get) if glow else 0
                solid[y][x] = gm if glow and glow[gm] * 2 > cnt else 1
                col[y][x] = tuple(int(v / cnt + 0.5) for v in acc)

    shadow = U.get("shadow", (23, 41))
    if shadow:                                             # shadow=None: no shadow (flags)
        x0, x1 = shadow
        sh = Image.new("L", (RW, RH), 0)
        ImageDraw.Draw(sh).ellipse([x0, RH - 4, x1, RH - 1], fill=255)
        shp = sh.load()
        for y in range(RH):
            for x in range(RW):
                if shp[x, y]:
                    o[x, y] = (255, 0, 255)
    nb4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for y in range(RH):
        for x in range(RW):
            if solid[y][x]:
                r, g, b = col[y][x]
                if (r, g, b) == (255, 0, 255):
                    r = 254
                o[x, y] = (max(r, 10), max(g, 10), max(b, 12))   # never pure black
                continue
            near = [solid[y + dy][x + dx] for dx, dy in nb4
                    if 0 <= x + dx < RW and 0 <= y + dy < RH and solid[y + dy][x + dx]]
            if near:
                if 1 in near:
                    o[x, y] = INK
                else:                                      # dark rim in the glow's own colour
                    e = EMISSIVE[near[0]][0]
                    o[x, y] = (max(e[0] // 2, 10), max(e[1] // 2, 10), max(e[2] // 2, 12))
    if U["poses"][pose].get("halo"):                       # soft glow around big lights
        for y in range(RH):
            for x in range(RW):
                if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                    continue
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        xx, yy = x + dx, y + dy
                        if dx * dx + dy * dy <= 4 and 0 <= xx < RW and 0 <= yy < RH and solid[yy][xx] > 1:
                            e = EMISSIVE[solid[yy][xx]][0]
                            o[x, y] = (max(int(e[0] * 0.62), 10), max(int(e[1] * 0.62), 10),
                                       max(int(e[2] * 0.62), 12))
                            break
                    else:
                        continue
                    break
    if U.get("free_rows", True):                           # 2px free below the feet
        for y in (RH - 2, RH - 1):
            for x in range(RW):
                if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                    o[x, y] = (255, 0, 255)
    return out


def build(unit, pose):
    R = Rig(UNITS[unit]["poses"][pose])
    UNITS[unit]["build"](R)
    return R.groups


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for unit in sys.argv[2:] or list(UNITS):
        for pose in UNITS[unit]["poses"]:
            name = UNITS[unit].get("file", unit)
            sprite(unit, pose).save(os.path.join(out, f"{name}{pose}.tga"))
