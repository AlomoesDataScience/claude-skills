"""Entry point of the built SpriteStudio file (a Python zip app; build with tools/build.py).

Unpacks the editor into ~/.cache/sprite-studio/<build id>/ the first time it runs,
then starts the server in app mode. Models and renders live next to the SpriteStudio
file (models/, output/); Export writes into the folder above that.
"""
import os
import shutil
import subprocess
import sys
import zipfile

ARCHIVE = os.path.dirname(os.path.abspath(__file__))     # .../SpriteStudio (the zip itself)
HERE = os.path.dirname(ARCHIVE)                           # the folder holding it
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "sprite-studio")


def fail(msg):
    """No terminal when launched by double-click: also show the error on the desktop."""
    print(msg, file=sys.stderr)
    os.makedirs(CACHE, exist_ok=True)
    with open(os.path.join(CACHE, "error.log"), "a") as f:
        f.write(msg + "\n")
    for tool, args in (("zenity", ["--error", "--title=Sprite Studio", "--text=" + msg]),
                       ("notify-send", ["Sprite Studio", msg])):
        if shutil.which(tool):
            subprocess.run([tool, *args])
            break
    sys.exit(1)


def unpack():
    with zipfile.ZipFile(ARCHIVE) as z:
        build = z.read("app/BUILD").decode().strip()
        dest = os.path.join(CACHE, build)
        if not os.path.exists(os.path.join(dest, "server.py")):
            tmp = dest + f".tmp{os.getpid()}"
            shutil.rmtree(tmp, ignore_errors=True)
            for name in z.namelist():
                if name.startswith("app/") and not name.endswith("/"):
                    out = os.path.join(tmp, name[4:])
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "wb") as f:
                        f.write(z.read(name))
            try:
                os.rename(tmp, dest)
            except OSError:                          # another copy unpacked it first
                shutil.rmtree(tmp, ignore_errors=True)
    for old in os.listdir(CACHE):                     # drop unpacked older builds nobody is running
        path = os.path.join(CACHE, old)
        if old != build and os.path.isdir(path) and not in_use(path):
            shutil.rmtree(path, ignore_errors=True)
    return dest, build


def in_use(path):
    """A running copy leaves a .pid-<n> file in its unpacked folder."""
    for f in os.listdir(path):
        if f.startswith(".pid-"):
            try:
                os.kill(int(f[5:]), 0)
                return True
            except (ValueError, ProcessLookupError):
                os.remove(os.path.join(path, f))
            except PermissionError:
                return True
    return False


def main():
    if sys.version_info < (3, 8):
        fail("Sprite Studio needs Python 3.8 or newer.")
    try:
        import PIL  # noqa: F401  (the renderer needs Pillow)
    except ImportError:
        fail("Sprite Studio needs Pillow. Install it with:  sudo apt install python3-pil")
    code, build = unpack()
    mark = os.path.join(code, f".pid-{os.getpid()}")
    open(mark, "w").close()
    sys.path.insert(0, code)
    import server
    args = sys.argv[1:]
    if "--data" not in args:
        args += ["--data", HERE]
    try:
        server.main(args + ["--app", "--build", build])
    except SystemExit:
        raise
    except Exception as e:                           # noqa: BLE001
        fail(f"Sprite Studio stopped: {e}")
    finally:
        try:
            os.remove(mark)
        except OSError:
            pass


main()
