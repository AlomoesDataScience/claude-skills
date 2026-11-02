"""Entry point of the Windows build (packed as app\\start.py by tools/release.py).

"Sprite Studio.bat" runs  python\\pythonw.exe -X utf8 app\\start.py  with the bundled Python
(no console window). Models and renders live in models\\ and output\\ next to app\\; Export
writes into the folder above that. pythonw has no console, so output goes to
sprite-studio.log and errors also pop up in a message box.
"""
import os
import sys
import traceback

APP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(APP)
LOG = os.path.join(ROOT, "sprite-studio.log")

if sys.stdout is None or sys.stderr is None:
    _log = open(LOG, "a", encoding="utf-8", buffering=1)
    sys.stdout = sys.stdout or _log
    sys.stderr = sys.stderr or _log


def fail(msg):
    print(msg, file=sys.stderr)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, msg, "Sprite Studio", 0x10)
    except (ImportError, AttributeError, OSError):
        pass
    sys.exit(1)


def main():
    try:
        import PIL  # noqa: F401  (the renderer needs Pillow; the Windows build bundles it)
    except ImportError:
        fail("Sprite Studio could not load Pillow. Unzip the whole folder again and start it from there.")
    sys.path.insert(0, APP)
    with open(os.path.join(APP, "BUILD")) as f:
        build = f.read().strip()
    import server
    try:
        server.main(sys.argv[1:] + ["--data", ROOT, "--app", "--build", build])
    except SystemExit:
        raise
    except Exception as e:                           # noqa: BLE001
        traceback.print_exc()
        fail(f"Sprite Studio stopped: {e}\n\nDetails are in {LOG}")


if __name__ == "__main__":
    main()
