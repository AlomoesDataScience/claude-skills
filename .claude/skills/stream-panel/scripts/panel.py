#!/usr/bin/env python3
"""Stream panel: one window for the right-hand column of a recording - a tracker on top (game,
mode, status, fields, goals, recent events, session timer) and Claude's live terminal log below
(what Claude says, each tool call with its description, full results, the user's messages).

  panel.py [--fresh] [--transcript FILE.jsonl] [--geometry WxH+X+Y] [--hide-user] [--font 11]

- Default place: the right third of the screen, full height minus the taskbar (--geometry to
  change). --fresh starts with an empty log (only what happens from now on - use it for
  recordings, so earlier parts of the session never show); otherwise the last ~60 entries.

- Log source: the newest Claude Code transcript under ~/.claude/projects (re-checked every 10 s),
  or --transcript. Thinking and subagent (sidechain) entries are left out.
- Tracker source: tracker.py's JSON (~/.cache/game-ui/tracker.json), redrawn when it changes.
- Window class "claude-panel" (title "Claude stream panel"): OBS window capture picks it by that.
- Paths are shortened for the screen (home -> ~, the workspace -> AI/, bgplay calls -> bgplay).
- Keys in the window: Space pauses/resumes the log scroll, +/- font size, h hides, q quits.
- It never takes focus: on opening it hands focus back to the window that had it (the user may be
  typing). The tracker text re-wraps to the window's real size; an off-screen start is pulled back.

  panel.py hide | show | toggle | stop        control the running panel (show keeps focus put)
"""
import glob
import json
import os
import re
import sys
import time
import subprocess
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracker as T                                    # noqa: E402

HOME = os.path.expanduser("~")
WORKSPACE = os.path.join(HOME, "Desktop", "AI Development")

# flat colours (art direction: no gradients, no 3D)
BG, PANEL, LINE = "#101317", "#191e25", "#2a313b"
TEXT, DIM, ACCENT = "#e8e8e8", "#8a93a0", "#f0a840"
TOOL, OK, USER, BAD = "#6cc4ff", "#9be38a", "#c9a0ff", "#ff6b6b"


def opt(a, name, default=None):
    if name in a:
        i = a.index(name)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    return default


def newest_transcript():
    files = glob.glob(os.path.join(HOME, ".claude", "projects", "*", "*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


TITLE = "Claude stream panel"


def active_window():
    out = subprocess.run(["xprop", "-root", "_NET_ACTIVE_WINDOW"], capture_output=True, text=True).stdout
    m = re.search(r"(0x[0-9a-f]+)", out)
    return m.group(1) if m and m.group(1) != "0x0" else None


def panel_window():
    out = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.endswith(TITLE):
            return line.split()[0]
    return None


def control(cmd):
    """hide / show / toggle / stop an already running panel without touching focus."""
    wid = panel_window()
    if not wid:
        sys.exit("no stream panel running (start it with: panel.py [--fresh])")
    if cmd == "toggle":
        st = subprocess.run(["xprop", "-id", wid, "_NET_WM_STATE"], capture_output=True, text=True).stdout
        cmd = "show" if "HIDDEN" in st else "hide"
    if cmd == "hide":
        subprocess.run(["python3", "-I", "-c", ICONIFY, wid], capture_output=True)
    elif cmd == "show":
        prev = active_window()
        subprocess.run(["wmctrl", "-i", "-R", wid], capture_output=True)
        if prev:
            subprocess.run(["wmctrl", "-i", "-a", prev], capture_output=True)   # visible, focus stays put
    elif cmd == "stop":
        subprocess.run(["wmctrl", "-i", "-c", wid], capture_output=True)
    print(f"panel {cmd}")


ICONIFY = """
import sys, ctypes, ctypes.util
X = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11"))
X.XOpenDisplay.restype = ctypes.c_void_p
d = X.XOpenDisplay(None)
X.XIconifyWindow.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int]
X.XDefaultScreen.argtypes = [ctypes.c_void_p]
X.XIconifyWindow(d, int(sys.argv[1], 16), X.XDefaultScreen(d))
X.XFlush.argtypes = [ctypes.c_void_p]; X.XFlush(d)
"""


def shorten(s):
    s = re.sub(r'cd "[^"]*" && ', "", s)
    s = re.sub(r'cd \S+ && ', "", s)
    for q in (r'"[^"]*/', r'[^"\s]*/'):                      # quoted (spaces) or bare script path
        s = re.sub(r'python3 -I ' + q + r'bgplay\.py"?', "bgplay", s)
        s = re.sub(r'python3 -I ' + q + r'([\w-]+\.py)"?', r"\1", s)
    s = re.sub(r'/tmp/claude-\d+/[^/\s"]+/[^/\s"]+/', "scratch/", s)
    s = s.replace(WORKSPACE, "AI").replace(HOME, "~")
    return s


def result_text(c):
    if isinstance(c, list):
        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    return str(c or "")


def entries(d, hide_user):
    """One transcript line -> list of (kind, text) for the log."""
    if d.get("type") == "queue-operation" and d.get("operation") == "enqueue":
        txt = str(d.get("content") or "").strip()        # typed while Claude works: shown at Enter
        if not txt or hide_user or txt.startswith("<"):   # system notices (task done etc.) aren't the user
            return []
        return [("user", txt)]
    if d.get("isSidechain") or d.get("type") not in ("assistant", "user"):
        return []
    c = (d.get("message") or {}).get("content")
    out = []
    if isinstance(c, str):
        if d["type"] == "user" and not hide_user and not c.startswith("<"):
            out.append(("user", c.strip()))
        return out
    for x in c or []:
        t = x.get("type")
        if t == "text" and x.get("text", "").strip():
            if d["type"] == "assistant":
                out.append(("say", x["text"].strip()))
            elif not hide_user and not x["text"].lstrip().startswith("<"):
                out.append(("user", x["text"].strip()))
        elif t == "tool_use":
            inp = x.get("input") or {}
            desc = inp.get("description") or ""
            cmd = inp.get("command") or inp.get("file_path") or inp.get("pattern") or inp.get("skill") or ""
            out.append(("tool", (x.get("name", "tool"), shorten(desc), shorten(str(cmd)))))
        elif t == "tool_result":
            txt = shorten(result_text(x.get("content"))).strip()
            out.append(("bad" if x.get("is_error") else "result", txt))
    return out


class Panel:
    def __init__(self, transcript, geometry, hide_user, size, fresh=False):
        self.fixed = transcript
        self.path = transcript or newest_transcript()
        self.pos = 0
        self.hide_user = hide_user
        self.size = size
        self.paused = False
        self.track_mtime = 0
        self.calls = 0
        self.seen_user = []
        self.last_kind = None
        self.last_t = time.time()
        self.prev = active_window()             # the user may be typing: hand focus back after mapping
        self.root = tk.Tk(className="claude-panel")
        self.root.title(TITLE)
        if not geometry:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            geometry = f"{sw // 3}x{sh - 80}+{sw - sw // 3}+0"
        self.root.geometry(geometry)
        self.root.configure(bg=BG)
        self.build()
        for k, f in (("<space>", self.toggle), ("q", lambda e: self.root.destroy()),
                     ("<plus>", lambda e: self.resize(1)), ("<minus>", lambda e: self.resize(-1)),
                     ("<equal>", lambda e: self.resize(1)), ("h", lambda e: self.root.iconify())):
            self.root.bind(k, f)
        self.root.bind("<Configure>", self.on_resize)
        self.root.after(400, self.settle)
        if self.path:
            if fresh:
                self.pos = os.path.getsize(self.path)
            else:
                self.prime()
        self.tick()

    # ---------- layout
    def fonts(self):
        s = self.size
        return {"title": ("DejaVu Sans", s + 9, "bold"), "big": ("DejaVu Sans", s + 2, "bold"),
                "mono": ("DejaVu Sans Mono", s), "small": ("DejaVu Sans Mono", s - 1), "tiny": ("DejaVu Sans Mono", max(7, s - 2)),
                "label": ("DejaVu Sans", s - 1, "bold")}

    def build(self):
        F = self.fonts()
        top = tk.Frame(self.root, bg=PANEL, padx=14, pady=10)
        top.pack(fill="x")
        self.w_game = tk.Label(top, text="", font=F["title"], fg=ACCENT, bg=PANEL, anchor="w", justify="left",
                               wraplength=600)
        self.w_game.pack(fill="x")
        row = tk.Frame(top, bg=PANEL)
        row.pack(fill="x")
        self.w_mode = tk.Label(row, text="", font=F["big"], fg=TEXT, bg=PANEL, anchor="w", justify="left",
                               wraplength=480)
        self.w_mode.pack(side="left")
        self.w_timer = tk.Label(row, text="0:00:00", font=F["big"], fg=DIM, bg=PANEL)
        self.w_timer.pack(side="right")
        self.w_status = tk.Label(top, text="", font=F["mono"], fg=OK, bg=PANEL, anchor="w",
                                 justify="left", wraplength=600)
        self.w_status.pack(fill="x", pady=(4, 0))
        self.w_fields = tk.Frame(top, bg=PANEL)
        self.w_fields.pack(fill="x", pady=(8, 0))
        self.w_goals = tk.Label(top, text="", font=F["mono"], fg=TEXT, bg=PANEL, anchor="w",
                                justify="left", wraplength=600)
        self.w_goals.pack(fill="x", pady=(8, 0))
        self.w_notes = tk.Label(top, text="", font=F["small"], fg=DIM, bg=PANEL, anchor="w",
                                justify="left", wraplength=600)
        self.w_notes.pack(fill="x", pady=(6, 0))
        tk.Frame(self.root, bg=LINE, height=2).pack(fill="x")
        head = tk.Frame(self.root, bg=BG, padx=14, pady=4)
        head.pack(fill="x")
        tk.Label(head, text="TERMINAL", font=F["label"], fg=DIM, bg=BG).pack(side="left")
        self.w_live = tk.Label(head, text="", font=F["label"], fg=DIM, bg=BG)
        self.w_live.pack(side="right")
        self.log = tk.Text(self.root, bg=BG, fg=TEXT, font=F["mono"], wrap="word", bd=0,
                           highlightthickness=0, padx=14, pady=6, spacing1=1, spacing3=3)
        self.log.pack(fill="both", expand=True)
        self.tags()
        self.log.configure(state="disabled")

    def tags(self):
        F = self.fonts()
        L = self.log
        L.tag_configure("say", foreground=TEXT, font=F["mono"], spacing1=6)
        L.tag_configure("toolname", foreground=TOOL, font=(F["mono"][0], F["mono"][1], "bold"), spacing1=6)
        L.tag_configure("desc", foreground=TOOL)
        L.tag_configure("cmd", foreground=DIM, font=F["tiny"], lmargin1=18, lmargin2=18)
        L.tag_configure("result", foreground="#b5bcc6", font=F["tiny"], lmargin1=18, lmargin2=18)
        L.tag_configure("bad", foreground=BAD, font=F["tiny"], lmargin1=18, lmargin2=18)
        L.tag_configure("user", foreground=USER, font=F["mono"], spacing1=8)

    def resize(self, d):
        self.size = max(7, min(20, self.size + d))
        F = self.fonts()
        self.w_game.configure(font=F["title"])
        for w in (self.w_mode, self.w_timer):
            w.configure(font=F["big"])
        for w in (self.w_status, self.w_goals):
            w.configure(font=F["mono"])
        self.w_notes.configure(font=F["small"])
        self.log.configure(font=F["mono"])
        self.tags()
        self.track_mtime = 0

    def settle(self):
        """After mapping: give focus back, and pull the window on-screen if it landed off it."""
        if self.prev:
            subprocess.run(["wmctrl", "-i", "-a", self.prev], capture_output=True)
        r = self.root
        r.update_idletasks()
        sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
        w, h = min(r.winfo_width(), sw), min(r.winfo_height(), sh)
        x, y = min(max(r.winfo_x(), 0), sw - w), min(max(r.winfo_y(), 0), sh - h)
        if (x, y, w, h) != (r.winfo_x(), r.winfo_y(), r.winfo_width(), r.winfo_height()):
            r.geometry(f"{w}x{h}+{x}+{y}")

    def on_resize(self, e):
        """Re-wrap the tracker text to the window's real width wherever it is moved or resized."""
        if e.widget is self.root:
            wrap = max(200, e.width - 40)
            for w in (self.w_status, self.w_goals, self.w_notes, self.w_game):
                w.configure(wraplength=wrap)
            self.w_mode.configure(wraplength=max(150, wrap - 130))
            if abs(getattr(self, "last_w", 0) - e.width) > 20:
                self.last_w, self.track_mtime = e.width, 0      # redraw fields for the new width

    def toggle(self, e=None):
        self.paused = not self.paused
        if not self.paused:
            self.log.see("end")

    # ---------- log
    def add(self, kind, payload):
        L = self.log
        L.configure(state="normal")
        if kind == "tool":
            name, desc, cmd = payload
            self.calls += 1
            L.insert("end", f"▸ {name}  ", "toolname")
            L.insert("end", (desc or "") + "\n", "desc")
            if cmd:
                L.insert("end", cmd + "\n", "cmd")
        elif kind in ("result", "bad"):
            lines = [x for x in payload.splitlines() if x.strip()]
            txt = "\n".join(lines)                 # everything, wrapped - never cut (the user)
            if txt:
                L.insert("end", txt + "\n", kind)
        elif kind == "user":
            L.insert("end", "⮞ " + payload + "\n", "user")
        else:
            L.insert("end", payload + "\n", "say")
        n = int(L.index("end-1c").split(".")[0])
        if n > 3000:
            L.delete("1.0", f"{n - 2500}.0")
        L.configure(state="disabled")
        if not self.paused:
            L.see("end")
        self.last_kind, self.last_t = kind, time.time()

    def prime(self):
        """Start with the last ~60 log entries."""
        try:
            with open(self.path, "rb") as f:
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - 400_000))
                data = f.read().decode("utf-8", "replace")
                self.pos = size
        except OSError:
            return
        items = []
        for line in data.splitlines()[1:]:
            try:
                items += entries(json.loads(line), self.hide_user)
            except ValueError:
                pass
        for k, p in items[-60:]:
            self.add(k, p)

    def read_new(self):
        if not self.fixed and int(time.time()) % 10 == 0:
            p = newest_transcript()
            if p and p != self.path:
                self.path, self.pos = p, 0
                self.prime()
                return
        try:
            if os.path.getsize(self.path) < self.pos:
                self.pos = 0
            with open(self.path, "rb") as f:
                f.seek(self.pos)
                chunk = f.read()
        except (OSError, TypeError):
            return
        if not chunk:
            return
        end = chunk.rfind(b"\n")
        if end < 0:
            return
        self.pos += end + 1
        for line in chunk[:end].decode("utf-8", "replace").splitlines():
            try:
                for k, p in entries(json.loads(line), self.hide_user):
                    self.add(k, p)
            except ValueError:
                pass

    # ---------- tracker
    def draw_tracker(self):
        try:
            m = os.path.getmtime(T.FILE)
        except OSError:
            m = -1
        if m == self.track_mtime:
            return
        self.track_mtime = m
        d = T.load() if m > 0 else dict(T.EMPTY, started=time.time())
        self.started = d.get("started") or time.time()
        self.w_game.configure(text=d.get("game") or "Claude plays")
        self.w_mode.configure(text=d.get("mode") or "")
        self.w_status.configure(text=d.get("status") or "")
        for w in self.w_fields.winfo_children():
            w.destroy()
        F = self.fonts()
        width = max(200, self.root.winfo_width() - 40)
        longest = max([len(k) + len(v) for k, v in d["fields"].items()] or [0])
        cols = 2 if longest * (self.size + 2) * 0.8 < width / 2 - 40 else 1
        self.field_wrap = width // cols - 120
        for i, (k, v) in enumerate(d["fields"].items()):
            r, c = divmod(i, cols)
            tk.Label(self.w_fields, text=k.upper(), font=F["label"], fg=DIM, bg=PANEL, anchor="w") \
                .grid(row=r, column=c * 2, sticky="w", padx=(0, 8))
            tk.Label(self.w_fields, text=v, font=F["big"], fg=TEXT, bg=PANEL, anchor="w", justify="left",
                     wraplength=max(120, self.field_wrap)) \
                .grid(row=r, column=c * 2 + 1, sticky="w", padx=(0, 28))
        goals = d.get("goals") or []
        self.w_goals.configure(text="\n".join(("☑ " if g.get("done") else "☐ ") + g.get("text", "")
                                              for g in goals))
        notes = (d.get("notes") or [])[-6:]
        self.w_notes.configure(text="\n".join(time.strftime("%H:%M ", time.localtime(n["t"])) + n["text"]
                                              for n in notes))

    def tick(self):
        if self.path:
            self.read_new()
        self.draw_tracker()
        el = int(time.time() - getattr(self, "started", time.time()))
        self.w_timer.configure(text=f"{el // 3600}:{el % 3600 // 60:02d}:{el % 60:02d}")
        idle = time.time() - self.last_t
        state = "acting" if self.last_kind == "tool" else ("thinking" if idle < 300 else "idle")
        self.w_live.configure(text=f"{'PAUSED  ' if self.paused else ''}{state}  ·  {self.calls} actions",
                              fg=ACCENT if self.paused else (OK if state == "acting" else DIM))
        self.root.after(300, self.tick)


def main(a):
    if a and a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a and a[0] in ("hide", "show", "toggle", "stop"):
        return control(a[0])
    if panel_window():
        control("show")
        sys.exit("a stream panel is already running: shown it (panel.py stop to close it)")
    tr = opt(a, "--transcript")
    geo = opt(a, "--geometry")
    size = int(opt(a, "--font", "11"))
    Panel(tr, geo, "--hide-user" in a, size, fresh="--fresh" in a).root.mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])
