"""Sprite Studio: a local editor for Dominions 6 sprites.

  python3 server.py [--port 8765] [--no-open] [--data DIR] [--mods DIR] [--app]

Then use the page that opens (http://127.0.0.1:8765). Everything stays on this machine:
models are saved in DATA/models/, renders go to DATA/output/<model>/, and Export copies
the TGAs into a folder under the mods directory (default: the folder above DATA).
DATA defaults to this folder. --app (used by the built SpriteStudio file) quits when no
page has been open for a few minutes.
"""
import base64
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

CODE = os.path.dirname(os.path.abspath(__file__))  # engine/ and web/
DATA = CODE                                        # models/ and output/ (set_dirs)
MODS = os.path.dirname(DATA)                       # export root: the Dominions folder
MODELS, OUTPUT = os.path.join(DATA, "models"), os.path.join(DATA, "output")
WEB = os.path.join(CODE, "web")
NAME = re.compile(r"^[a-z0-9_\-]{1,64}$")
RENDER_LOCK = threading.Lock()
LATEST = {}                                        # sprite file -> newest render request for it
LATEST_LOCK = threading.Lock()
LAST_SEEN = [time.time()]                          # last request from a page (for --app)
QUIT_AFTER = 180                                   # seconds without a page before --app quits
BUILD = ["source"]                                 # build id of the built app (--build), "source" for server.py


def set_dirs(data, mods=None):
    global DATA, MODS, MODELS, OUTPUT
    DATA = os.path.abspath(data)
    MODS = os.path.abspath(mods) if mods else os.path.dirname(DATA)
    MODELS, OUTPUT = os.path.join(DATA, "models"), os.path.join(DATA, "output")


def model_path(name):
    if not NAME.match(name or ""):
        raise ValueError("model names use lowercase letters, digits, - and _")
    return os.path.join(MODELS, name + ".json")


def frame_ok(key):
    if not re.match(r"^[a-z0-9_]{0,16}$", key):
        raise ValueError("bad frame key")
    return key


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=CODE, **kw)

    def translate_path(self, path):
        """/web/... comes from the code folder, /output/... from the data folder."""
        path = posixpath.normpath(urlparse(path).path)
        base, rest = (WEB, path[5:]) if path.startswith("/web/") else (OUTPUT, path[8:])
        parts = [p for p in rest.split("/") if p not in ("", ".", "..")]
        return os.path.join(base, *parts)

    def log_message(self, fmt, *args):
        if "/api/" in str(args[0] if args else "") and sys.stderr:   # no stderr under pythonw
            sys.stderr.write("%s\n" % (fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        LAST_SEEN[0] = time.time()
        try:
            if u.path == "/api/ping":
                self.send_json({"app": "sprite-studio", "build": BUILD[0]})
            elif u.path == "/":
                self.send_response(302)
                self.send_header("Location", "/web/index.html")
                self.end_headers()
            elif u.path == "/api/wait":                       # test hook: lets screenshots wait for the page
                time.sleep(min(int(q.get("ms", "0")), 30000) / 1000)
                self.send_response(204)
                self.end_headers()
            elif u.path == "/api/models":
                names = sorted(f[:-5] for f in os.listdir(MODELS) if f.endswith(".json"))
                self.send_json({"models": names, "mods": os.path.basename(MODS) or MODS})
            elif u.path == "/api/model":
                with open(model_path(q.get("name"))) as f:
                    self.send_json(json.load(f))
            elif posixpath.normpath(u.path).startswith(("/web/", "/output/")):
                super().do_GET()
            else:
                self.send_error(404)
        except (ValueError, OSError) as e:
            self.send_json({"error": str(e)}, 400)

    def do_POST(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            data = self.body()
            LAST_SEEN[0] = time.time()
            if u.path == "/api/quit":
                self.send_json({"quit": True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            elif u.path == "/api/model":
                path = model_path(q.get("name"))
                if os.path.exists(path):                    # keep the previous version
                    hist = os.path.join(MODELS, ".history")
                    os.makedirs(hist, exist_ok=True)
                    shutil.copy(path, os.path.join(hist, f"{q['name']}-{time.strftime('%Y%m%d-%H%M%S')}.json"))
                data["name"] = q["name"]
                with open(path, "w") as f:
                    json.dump(data, f, indent=1)
                self.send_json({"saved": q["name"]})
            elif u.path == "/api/render":
                self.send_json(render(data["model"], frame_ok(str(data.get("frame", "1"))), data.get("ss"),
                                      data.get("tag")))
            elif u.path == "/api/export":
                self.send_json(export(data))
            elif u.path == "/api/decode":
                self.send_json(decode(data))
            elif u.path == "/api/sprite":
                self.send_json(save_sprite(data))
            else:
                self.send_error(404)
        except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
            self.send_json({"error": str(e)}, 400)


def render(model, frame, ss, tag=None):
    """Render one frame. A tag (e.g. "yaw45") renders a preview into output/<model>/preview/
    without touching the real frame files."""
    name = model.get("name") or "untitled"
    if not NAME.match(name):
        raise ValueError("bad model name")
    if tag is not None and not re.match(r"^[a-z0-9_\-]{1,32}$", tag):
        raise ValueError("bad preview tag")
    out = os.path.join(OUTPUT, name, "preview") if tag else os.path.join(OUTPUT, name)
    os.makedirs(out, exist_ok=True)
    file = re.sub(r"[^a-z0-9_\-]", "", model.get("render", {}).get("file") or name)
    stem = f"{file}{frame}" + (f"_{tag}" if tag else "")
    tga, png = os.path.join(out, f"{stem}.tga"), os.path.join(out, f"{stem}.png")
    me = object()
    with LATEST_LOCK:
        LATEST[tga] = me
    # each request has its own model file: requests for the same frame (e.g. while dragging)
    # used to share one, and the first to finish deleted it under the others
    fd, src = tempfile.mkstemp(prefix=f".render-{stem}-", suffix=".json", dir=out)
    with os.fdopen(fd, "w") as f:
        json.dump(model, f)
    cmd = [sys.executable, "-I", *(["-X", "utf8"] if sys.flags.utf8_mode else []),
           os.path.join(CODE, "engine", "render.py"), src, frame, tga, f"--png={png}"]
    if ss:
        cmd.append(f"--ss={int(ss)}")
    try:
        with RENDER_LOCK:
            if tag is None and LATEST.get(tga) is not me:
                return {"skipped": True}           # a newer request for this sprite is waiting
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    finally:
        try:
            os.remove(src)
        except OSError:
            pass
    if p.returncode:
        raise ValueError("render failed:\n" + p.stderr[-2000:])
    info = json.loads(p.stdout.strip().splitlines()[-1])
    rel = os.path.relpath(png, OUTPUT).replace(os.sep, "/")
    return {"png": "/output/" + rel + f"?t={time.time():.0f}", "tga": os.path.relpath(tga, MODS), **info}


MAX_SIDE = 512


def decode(data):
    """An imported image (TGA, PNG, ...) -> PNG data URL with Dominions colours: anything
    see-through becomes black (transparent in the game)."""
    from PIL import Image
    raw = base64.b64decode(data["data"])
    if len(raw) > 16 << 20:
        raise ValueError("image file too big")
    try:
        im = Image.open(io.BytesIO(raw))
    except OSError:
        raise ValueError("not an image Sprite Studio can read (use .tga or .png)") from None
    if max(im.size) > MAX_SIDE:
        raise ValueError(f"image is {im.size[0]}x{im.size[1]}; sprites can be at most {MAX_SIDE} px")
    im.load()
    if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        out = Image.new("RGB", im.size, (0, 0, 0))
        out.paste(rgba.convert("RGB"), mask=rgba.getchannel("A").point(lambda a: 255 if a >= 128 else 0))
    else:
        out = im.convert("RGB")
    px = out.load()                                # off-magenta shadow (e.g. 248,0,248) -> exact magenta
    for y in range(out.height):
        for x in range(out.width):
            r, g, b = px[x, y]
            if r >= 230 and b >= 230 and g <= 30 and (r, g, b) != (255, 0, 255):
                px[x, y] = (255, 0, 255)
    buf = io.BytesIO()
    out.save(buf, "PNG")
    return {"png": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), "w": out.width, "h": out.height}


def save_sprite(data):
    """Write a sprite drawn in the page (2D cut-out projects) as <file><frame>.tga + .png."""
    from PIL import Image
    name, frame = data["name"], frame_ok(str(data["frame"]))
    if not NAME.match(name):
        raise ValueError("bad model name")
    file = re.sub(r"[^a-z0-9_\-]", "", data.get("file") or name) or name
    w, h = int(data["w"]), int(data["h"])
    rgb = base64.b64decode(data["rgb"])
    if not (0 < w <= MAX_SIDE and 0 < h <= MAX_SIDE) or len(rgb) != w * h * 3:
        raise ValueError("bad sprite size")
    out = os.path.join(OUTPUT, name)
    os.makedirs(out, exist_ok=True)
    im = Image.frombytes("RGB", (w, h), rgb)
    tga, png = os.path.join(out, f"{file}{frame}.tga"), os.path.join(out, f"{file}{frame}.png")
    im.save(tga)
    im.save(png)
    rel = os.path.relpath(png, OUTPUT).replace(os.sep, "/")
    return {"png": "/output/" + rel + f"?t={time.time():.0f}", "tga": os.path.relpath(tga, MODS), "seconds": 0, "size": [w, h]}


def export(data):
    """Copy rendered TGAs into a folder under the Dominions directory."""
    name = data["name"]
    if not NAME.match(name):
        raise ValueError("bad model name")
    dest = os.path.realpath(os.path.join(MODS, data["dir"]))
    inside = lambda d: dest == os.path.realpath(d) or dest.startswith(os.path.realpath(d) + os.sep)
    if not dest.startswith(os.path.realpath(MODS) + os.sep) or inside(DATA) or inside(CODE):
        raise ValueError(f"the export folder must be inside {os.path.basename(MODS)}/ (and not Sprite Studio's own folder)")
    for f in data["files"]:
        if not re.match(r"^[a-z0-9_\-]+\.tga$", f):
            raise ValueError(f"bad file {f}")
    os.makedirs(dest, exist_ok=True)
    src = os.path.join(OUTPUT, name)
    copied = []
    for f in data["files"]:
        shutil.copy(os.path.join(src, f), os.path.join(dest, f))
        copied.append(os.path.relpath(os.path.join(dest, f), MODS))
    return {"copied": copied}


class Server(ThreadingHTTPServer):
    # on Windows SO_REUSEADDR lets two servers share a port, so a busy port would not be noticed
    allow_reuse_address = os.name != "nt"


def running_here(port):
    """The build id of a Sprite Studio answering on this port ("" if it is older than build ids),
    or None if no Sprite Studio is there."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/ping", timeout=1.5) as r:
            j = json.load(r)
            return j.get("build", "") if j.get("app") == "sprite-studio" else None
    except (OSError, ValueError):
        return None


def take_over(port):
    """Ask an older Sprite Studio on this port to quit and wait until the port is free."""
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/api/quit", data=b"{}"), timeout=3).read()
    except OSError:
        pass
    for _ in range(50):
        if running_here(port) is None:
            return True
        time.sleep(0.1)
    return False


def watchdog(srv):
    """--app: quit once no page has talked to the server for QUIT_AFTER seconds."""
    while True:
        time.sleep(10)
        if time.time() - LAST_SEEN[0] > QUIT_AFTER and not RENDER_LOCK.locked():
            srv.shutdown()
            return


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    arg = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    if arg("--data"):
        set_dirs(arg("--data"), arg("--mods"))
    BUILD[0] = arg("--build", BUILD[0])
    port = int(arg("--port", 8765))
    open_page = "--no-open" not in argv
    for d in (MODELS, OUTPUT):
        os.makedirs(d, exist_ok=True)
    seed = os.path.join(CODE, "seed")             # starter models bundled with the built app
    if os.path.isdir(seed) and not any(f.endswith(".json") for f in os.listdir(MODELS)):
        for f in os.listdir(seed):
            shutil.copy(os.path.join(seed, f), MODELS)
    for p in range(port, port + 10):              # reuse a running copy, else take a free port
        other = running_here(p)
        if other is not None and "--app" in argv and other != BUILD[0]:
            print(f"replacing an older Sprite Studio ({other or 'old build'}) on port {p}")
            take_over(p)
        elif other is not None:
            print(f"Sprite Studio is already running on port {p}")
            if open_page:
                webbrowser.open(f"http://127.0.0.1:{p}/web/index.html")
            return
        try:
            srv = Server(("127.0.0.1", p), Handler)
            break
        except OSError:
            continue
    else:
        raise SystemExit(f"no free port in {port}-{port + 9}")
    url = f"http://127.0.0.1:{p}/web/index.html"
    print(f"Sprite Studio running at {url}  (Ctrl+C to stop)\nmodels: {MODELS}")
    if open_page:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    if "--app" in argv:
        threading.Thread(target=watchdog, args=(srv,), daemon=True).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()


if __name__ == "__main__":
    main()
