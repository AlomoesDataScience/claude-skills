#!/usr/bin/env python3
"""Draw a movement plan over several turns on a game board - as ONE picture (all turns, arrows coloured
and numbered by turn) and/or ONE PICTURE PER TURN. Uses draw-map's drawmap.py.

  turnplan.py PLAN.txt [--mode one|turns|both] [--cell 34]

PLAN.txt:
  board: setup.txt            draw-map board file to take the terrain grid from (relative to PLAN.txt)
  view: C0 C1 R0 R1           map columns C0..C1 and rows R0..R1 to show (inclusive); default whole board
  units:                      ID COLOUR COL ROW [FACING]   start positions in MAP coordinates
  turn TITLE...               a turn: following lines are moves  ID COL ROW  (destination, map coords)
  marks:                      COL ROW text   (map coords; shown in every picture)
Output next to PLAN.txt: NAME_one.png and/or NAME_t1.png, NAME_t2.png ... (+ the .txt boards)."""
import os
import subprocess
import sys

DRAW = os.path.expanduser("~/Desktop/AI Development/.claude/skills/draw-map/scripts/drawmap.py")
TURN_COLOURS = ["#d01010", "#e07b00", "#1a8f1a", "#7b2fbf", "#0060c0", "#c0187a", "#6b4f00", "#008080"]


def parse(path):
    base = os.path.dirname(os.path.abspath(path))
    board, view, units, turns, marks, sec = None, None, {}, [], [], None
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        if p[0] == "board:":
            board = os.path.join(base, p[1]); continue
        if p[0] == "view:":
            view = tuple(int(x) for x in p[1:5]); continue
        if line in ("units:", "marks:"):
            sec = line[:-1]; continue
        if p[0] == "turn":
            turns.append((" ".join(p[1:]), [])); sec = "turn"; continue
        if sec == "units":
            units[p[0]] = [p[1], int(p[2]), int(p[3]), p[4] if len(p) > 4 else "E"]
        elif sec == "turn":
            turns[-1][1].append((p[0], int(p[1]), int(p[2])))
        elif sec == "marks":
            marks.append((int(p[0]), int(p[1]), " ".join(p[2:])))
    g = open(board).read().split("grid:\n")[1]
    grid = []
    for l in g.split("\n"):
        if l.strip() in ("units:", "moves:", "marks:", "colour:"):
            break
        if l.strip():
            grid.append(l.strip())
    if view is None:
        view = (0, max(len(r) for r in grid) - 1, 0, len(grid) - 1)
    return grid, view, units, turns, marks


def write_board(path, title, grid, view, units, moves, marks):
    c0, c1, r0, r1 = view
    out = [f"# {title}", "grid:"] + [row[c0:c1 + 1] for row in grid[r0:r1 + 1]] + ["units:"]
    out += [f"{u} {col} {c - c0} {r - r0} {face}" for u, (col, c, r, face) in units.items()
            if c0 <= c <= c1 and r0 <= r <= r1]
    out += ["moves:"] + [f"{u} {a - c0} {b - r0} -> {c - c0} {d - r0} c={colr} {lab}".rstrip()
                         for u, a, b, c, d, colr, lab in moves]
    out += ["marks:", f"0 0 map c{c0} r{r0}"] + [f"{c - c0} {r - r0} {t}" for c, r, t in marks
                                                 if c0 <= c <= c1 and r0 <= r <= r1]
    open(path, "w").write("\n".join(out) + "\n")


def main(a):
    if not a:
        sys.exit(__doc__)
    mode = a[a.index("--mode") + 1] if "--mode" in a else "both"
    cell = a[a.index("--cell") + 1] if "--cell" in a else "34"
    src = a[0]
    name = os.path.splitext(src)[0]
    grid, view, units, turns, marks = parse(src)
    pos = {u: list(v) for u, v in units.items()}
    allmoves = []
    for i, (title, mv) in enumerate(turns):
        colr = TURN_COLOURS[i % len(TURN_COLOURS)]
        moves = []
        for u, c, r in mv:
            moves.append((u, pos[u][1], pos[u][2], c, r, colr, f"T{i + 1}"))
            pos[u][1], pos[u][2] = c, r
        allmoves += moves
        if mode in ("turns", "both"):
            f = f"{name}_t{i + 1}.txt"
            write_board(f, f"Turn {i + 1}: {title}", grid, view, pos, moves, marks)
            subprocess.run([sys.executable, "-I", DRAW, f, f[:-4] + ".png", "--cell", cell,
                            "--origin", str(view[0]), str(view[2])], check=True)
    if mode in ("one", "both"):
        f = f"{name}_one.txt"
        legend = "; ".join(f"T{i + 1} {t}" for i, (t, _) in enumerate(turns))
        write_board(f, "All turns: " + legend, grid, view, pos, allmoves, marks)
        subprocess.run([sys.executable, "-I", DRAW, f, f[:-4] + ".png", "--cell", cell,
                       "--origin", str(view[0]), str(view[2])], check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
