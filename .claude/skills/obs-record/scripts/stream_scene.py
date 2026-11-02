#!/usr/bin/env python3
"""Build the streamer-style OBS scene "Claude Stream": the bgplay game screen on the left 2/3,
the stream panel (stream-panel skill) on the right third. Re-running it refreshes the window
choices and the layout. Canvas 1920x1080.

  stream_scene.py [--game-title "Claude game screen"] [--panel-title "Claude stream panel"]
"""
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import obs as O                                    # noqa: E402

SCENE = "Claude Stream"


def opt(a, k, d):
    if k in a:
        i = a.index(k)
        return a[i + 1]
    return d


def safe(o, req, data=None):
    try:
        return o.call(req, data)
    except SystemExit as e:                         # obs.py exits on a failed request
        return {"error": str(e)}


def window_value(title):
    """xcomposite's capture_window value: decimal window id, title, class (from wmctrl -lx)."""
    out = subprocess.run(["wmctrl", "-lx"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.split(None, 4)
        if len(parts) == 5 and parts[4].endswith(title):
            cls = parts[2].split(".")[0]
            return f"{int(parts[0], 16)}\r\n{title}\r\n{cls}"
    sys.exit(f"no window titled {title!r} on the desktop")


def capture(o, name, title):
    # OBS 33 crashes ("basic_string: construction from null") if an xcomposite input is created
    # with empty settings or its window list is queried over the WebSocket: always create it
    # with capture_window already filled in, and never call GetInputPropertiesListPropertyItems.
    settings = {"capture_window": window_value(title), "include_border": False, "exclude_alpha": False,
                "show_cursor": False}            # the user: hide the mouse
    if "error" in safe(o, "GetInputSettings", {"inputName": name}):
        safe(o, "CreateInput", {"sceneName": SCENE, "inputName": name, "inputKind": "xcomposite_input",
                                "inputSettings": settings})
    else:
        safe(o, "SetInputSettings", {"inputName": name, "inputSettings": settings})
        items = safe(o, "GetSceneItemList", {"sceneName": SCENE}).get("sceneItems", [])
        if not any(i["sourceName"] == name for i in items):
            safe(o, "CreateSceneItem", {"sceneName": SCENE, "sourceName": name})
    return safe(o, "GetSceneItemId", {"sceneName": SCENE, "sourceName": name})["sceneItemId"]


def place(o, item, x, y, box_w, box_h):
    """Scale the source to fit the box (keep aspect), centred in it."""
    for _ in range(20):
        t = safe(o, "GetSceneItemTransform", {"sceneName": SCENE, "sceneItemId": item})["sceneItemTransform"]
        if t["sourceWidth"] > 0:
            break
        time.sleep(0.3)
    sw, sh = t["sourceWidth"] or box_w, t["sourceHeight"] or box_h
    s = min(box_w / sw, box_h / sh)
    safe(o, "SetSceneItemTransform", {"sceneName": SCENE, "sceneItemId": item, "sceneItemTransform": {
        "positionX": x + (box_w - sw * s) / 2, "positionY": y + (box_h - sh * s) / 2,
        "scaleX": s, "scaleY": s, "boundsType": "OBS_BOUNDS_NONE"}})
    print(f"  {sw}x{sh} -> scale {s:.3f} at box {x},{y} {box_w}x{box_h}")


def main(a):
    o = O.OBS()
    safe(o, "CreateScene", {"sceneName": SCENE})
    if "error" in safe(o, "GetInputSettings", {"inputName": "Stream background"}):
        safe(o, "CreateInput", {"sceneName": SCENE, "inputName": "Stream background", "inputKind": "color_source_v3",
                                "inputSettings": {"color": 0xFF171310, "width": 1920, "height": 1080}})
    bg = safe(o, "GetSceneItemId", {"sceneName": SCENE, "sourceName": "Stream background"})["sceneItemId"]
    safe(o, "SetSceneItemIndex", {"sceneName": SCENE, "sceneItemId": bg, "sceneItemIndex": 0})
    g = capture(o, "Game screen", opt(a, "--game-title", "Claude game screen"))
    p = capture(o, "Stream panel", opt(a, "--panel-title", "Claude stream panel"))
    print("game:"); place(o, g, 0, 0, 1280, 1080)
    print("panel:"); place(o, p, 1280, 0, 640, 1080)
    safe(o, "SetCurrentProgramScene", {"sceneName": SCENE})
    print(f"scene {SCENE!r} is live")


if __name__ == "__main__":
    main(sys.argv[1:])
