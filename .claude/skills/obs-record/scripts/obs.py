"""Control OBS Studio through its WebSocket server (protocol v5), pure Python, no pip.

  python3 -I obs.py status               recording/streaming state, scene, sources, audio mutes,
                                         recording folder and format
  python3 -I obs.py start | stop | pause | resume       the recording (stop prints the file)
  python3 -I obs.py mute NAME | unmute NAME             an audio input (e.g. "Mic/Aux")
  python3 -I obs.py call REQUEST [JSON]                 any v5 request, e.g. GetVersion
  python3 -I obs.py begin | end          a gameplay session: begin starts the recording paused and
                                         sets a flag; while it is set, dom6-ui's session.run
                                         resumes the recording for each game action and pauses it
                                         afterwards, so the video holds only gameplay. end stops it.

Connects to localhost:4455; the password is read from OBS's own config (flatpak or native) and
never printed. OBS must be running with Tools > WebSocket Server Settings > Enable ticked.
"""
import base64
import hashlib
import json
import os
import socket
import struct
import sys

CONFIGS = ["~/.var/app/com.obsproject.Studio/config/obs-studio/plugin_config/obs-websocket/config.json",
           "~/.config/obs-studio/plugin_config/obs-websocket/config.json"]


def settings():
    for p in CONFIGS:
        p = os.path.expanduser(p)
        if os.path.exists(p):
            return json.load(open(p))
    sys.exit("no obs-websocket config found (has OBS run with the WebSocket server enabled?)")


class WS:
    def __init__(self, host="127.0.0.1", port=4455):
        self.s = socket.create_connection((host, port), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\n"
                        f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
                        "Sec-WebSocket-Protocol: obswebsocket.json\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            head += self.s.recv(1)
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise SystemExit("OBS refused the WebSocket upgrade: " + head.split(b"\r\n")[0].decode())

    def send(self, obj):
        data = json.dumps(obj).encode()
        mask = os.urandom(4)
        n = len(data)
        hdr = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack(">H", n)
                               if n < 65536 else bytes([0x80 | 127]) + struct.pack(">Q", n))
        self.s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _exact(self, n):
        b = b""
        while len(b) < n:
            c = self.s.recv(n - len(b))
            if not c:
                raise SystemExit("OBS closed the connection")
            b += c
        return b

    def recv(self):
        while True:
            b0, b1 = self._exact(2)
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._exact(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._exact(8))[0]
            data = self._exact(n)
            if b0 & 0x0F == 0x8:
                raise SystemExit("OBS closed the connection: " + data[2:].decode(errors="replace"))
            if b0 & 0x0F == 0x1:
                return json.loads(data)


class OBS:
    def __init__(self):
        cfg = settings()
        if not cfg.get("server_enabled"):
            sys.exit("the OBS WebSocket server is disabled (Tools > WebSocket Server Settings)")
        self.ws = WS(port=cfg.get("server_port", 4455))
        hello = self.ws.recv()["d"]
        ident = {"rpcVersion": 1, "eventSubscriptions": 0}
        auth = hello.get("authentication")
        if auth:
            secret = base64.b64encode(hashlib.sha256((cfg["server_password"] + auth["salt"]).encode()).digest())
            ident["authentication"] = base64.b64encode(
                hashlib.sha256(secret + auth["challenge"].encode()).digest()).decode()
        self.ws.send({"op": 1, "d": ident})
        msg = self.ws.recv()
        if msg["op"] != 2:
            sys.exit(f"OBS did not accept the identification: {msg}")
        self.n = 0

    def call(self, rtype, data=None):
        self.n += 1
        rid = str(self.n)
        self.ws.send({"op": 6, "d": {"requestType": rtype, "requestId": rid, "requestData": data or {}}})
        while True:
            m = self.ws.recv()
            if m["op"] == 7 and m["d"]["requestId"] == rid:
                st = m["d"]["requestStatus"]
                if not st["result"]:
                    raise SystemExit(f"{rtype} failed: {st.get('comment', st)}")
                return m["d"].get("responseData", {})


FLAG = os.path.expanduser("~/.cache/game-ui/recording")   # read by game-ui (gameui.FLAG)


def session_active():
    return os.path.exists(FLAG)


def hook(resume):
    """Called by dom6-ui's session.run around game input; never raises (a recording problem must
    not stop play)."""
    if not session_active():
        return
    try:
        o = OBS()
        st = o.call("GetRecordStatus")
        if not st["outputActive"]:
            return
        if resume and st.get("outputPaused"):
            o.call("ResumeRecord")
        elif not resume and not st.get("outputPaused"):
            o.call("PauseRecord")
    except BaseException as e:                     # SystemExit included
        print(f"(recording hook: {e})", file=sys.stderr)


def status(o):
    rec = o.call("GetRecordStatus")
    scene = o.call("GetCurrentProgramScene")
    name = scene.get("sceneName") or scene.get("currentProgramSceneName")
    items = o.call("GetSceneItemList", {"sceneName": name})["sceneItems"]
    print(f"recording: {rec['outputActive']} (paused {rec.get('outputPaused')}, {rec.get('outputTimecode')})")
    print(f"scene: {name}; sources: " + ", ".join(f"{i['sourceName']} ({i.get('inputKind')}, "
                                                     f"{'shown' if i['sceneItemEnabled'] else 'hidden'})" for i in items))
    for i in o.call("GetInputList")["inputs"]:
        try:
            muted = o.call("GetInputMute", {"inputName": i["inputName"]})["inputMuted"]
            print(f"audio: {i['inputName']} ({i['inputKind']}): {'MUTED' if muted else 'live'}")
        except SystemExit:
            pass                                   # not an audio input
    print("folder:", o.call("GetRecordDirectory")["recordDirectory"])
    prof = o.call("GetProfileParameter", {"parameterCategory": "SimpleOutput", "parameterName": "RecFormat2"})
    print("format (simple output):", prof.get("parameterValue"))


def main(a):
    if not a:
        print(__doc__)
        return
    o = OBS()
    c = a[0]
    if c == "status":
        status(o)
    elif c in ("start", "stop", "pause", "resume"):
        r = o.call({"start": "StartRecord", "stop": "StopRecord", "pause": "PauseRecord",
                    "resume": "ResumeRecord"}[c])
        print(c, "ok", r.get("outputPath", ""))
    elif c == "begin":
        if not o.call("GetRecordStatus")["outputActive"]:
            o.call("StartRecord")
        import time
        time.sleep(1.0)
        o.call("PauseRecord")
        os.makedirs(os.path.dirname(FLAG), exist_ok=True)
        open(FLAG, "w").close()
        print("recording session open (paused until the next game action)")
    elif c == "end":
        if os.path.exists(FLAG):
            os.remove(FLAG)
        st = o.call("GetRecordStatus")
        if st["outputActive"]:
            if st.get("outputPaused"):
                o.call("ResumeRecord")
            print("stopped:", o.call("StopRecord").get("outputPath", ""))
        else:
            print("no recording was running")
    elif c in ("mute", "unmute"):
        o.call("SetInputMute", {"inputName": a[1], "inputMuted": c == "mute"})
        print(a[1], "muted" if c == "mute" else "live")
    elif c == "call":
        print(json.dumps(o.call(a[1], json.loads(a[2]) if len(a) > 2 else None), indent=1))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
