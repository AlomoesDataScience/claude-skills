#!/usr/bin/env python3
"""Read and "watch" videos (YouTube or a local file): transcript text, frames, contact sheets, OCR.

  python3 -I video.py info SRC                 title, channel, length, chapters, description
  python3 -I video.py transcript SRC [--lang en] [--para 30]
        captions (uploaded first, auto-generated second) as clean text with [mm:ss] stamps every
        --para seconds and chapter headings -> OUT/transcript.md; prints where it went and the size
  python3 -I video.py grep SRC REGEX [--context 1]   transcript lines matching, with timestamps
  python3 -I video.py frames SRC [--every 60 | --count 96 | --scene 0.3] [--from T] [--to T]
        downloads a small copy (<=480p) once, grabs frames and writes contact sheets of 16 stamped
        frames each (OUT/sheets/sheet_01.png ...) - an hour in ~6 images; look at those
  python3 -I video.py at SRC T [T ...] [--wide 1280]  full-size frames at those times (12:34, 754, 1:02:03)
  python3 -I video.py ocr SRC                   Tesseract text of every grabbed frame -> OUT/frames_ocr.md
  python3 -I video.py clip SRC FROM TO          only that part, downloaded at <=720p (for a closer look)
  python3 -I video.py audio SRC                 audio only (m4a/opus), for speech-to-text
  python3 -I video.py stt SRC [--model small]   speech-to-text on the audio (faster-whisper in a venv:
        VIDEO_WHISPER_PY, else ~/.venvs/whisper/bin/python) -> captions.stt.srt; then `transcript` uses it

SRC = a YouTube (or other yt-dlp site) URL or id, or a local video file (no download then).
OUT = ~/.cache/video-watch/<id>/ (VIDEO_WATCH_CACHE to change). Captions need nothing but yt-dlp;
frames need ffmpeg; contact sheets need Pillow; ocr needs tesseract.
yt-dlp: VIDEO_YTDLP, else this skill's bin/yt-dlp, else /usr/local/bin, ~/.local/bin, then PATH;
VIDEO_YTDLP_ARGS adds options to every yt-dlp call.
YouTube changes often: a yt-dlp older than a few months fails with "Precondition check failed" /
"No video formats found" - update it (SKILL.md). No cookies, no logins, no bot-check evasion.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("VIDEO_WATCH_CACHE", os.path.expanduser("~/.cache/video-watch"))


# ---------- helpers ----------
def ytdlp():
    for p in (os.environ.get("VIDEO_YTDLP"), os.path.join(HERE, "..", "bin", "yt-dlp"),
              "/usr/local/bin/yt-dlp", os.path.expanduser("~/.local/bin/yt-dlp"), shutil.which("yt-dlp")):
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return os.path.abspath(p)
    sys.exit("yt-dlp not found (see SKILL.md, 'Setup')")


def is_local(src):
    return os.path.isfile(src)


def vid_id(src):
    if is_local(src):
        return "local_" + re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.splitext(os.path.basename(src))[0])[:60]
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/|embed/)([A-Za-z0-9_-]{11})", src)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", src):
        return src
    return re.sub(r"[^A-Za-z0-9_.-]", "_", src)[-60:]


def url_of(src):
    return "https://www.youtube.com/watch?v=" + src if re.fullmatch(r"[A-Za-z0-9_-]{11}", src) else src


def outdir(src):
    d = os.path.join(CACHE, vid_id(src))
    os.makedirs(d, exist_ok=True)
    return d


def run_ytdlp(args, soft=False):
    extra = os.environ.get("VIDEO_YTDLP_ARGS", "").split()   # e.g. "--js-runtimes deno" if a new yt-dlp asks
    cmd = [ytdlp(), "--no-warnings", "--no-playlist"] + extra + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if soft:                                            # caller checks the files; give it the messages
        return r.stdout + r.stderr
    if r.returncode:
        err = (r.stderr or r.stdout).strip().splitlines()
        msg = "\n".join(err[-4:])
        if "Precondition" in r.stderr or "No video formats" in r.stderr or "Sign in to confirm" in r.stderr:
            msg += "\n-> yt-dlp is too old or YouTube blocked this request: update yt-dlp (SKILL.md 'Setup')"
        sys.exit("yt-dlp failed:\n" + msg)
    return r.stdout


def secs(t):
    """'1:02:03' / '12:34' / '754' / '754.5' -> seconds"""
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(p) for p in str(t).split(":")]
    s = 0.0
    for p in parts:
        s = s * 60 + p
    return s


def stamp(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def opt(name, default=None, cast=str):
    if name in sys.argv:
        i = sys.argv.index(name)
        v = sys.argv[i + 1]
        del sys.argv[i:i + 2]
        return cast(v)
    return default


# ---------- info ----------
def info(src):
    d = outdir(src)
    f = os.path.join(d, "info.json")
    if os.path.exists(f):
        return json.load(open(f))
    if is_local(src):
        r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_chapters",
                            src], capture_output=True, text=True, check=True)
        p = json.loads(r.stdout)
        j = {"id": vid_id(src), "title": os.path.basename(src), "duration": float(p["format"].get("duration", 0)),
             "channel": "(local file)", "chapters": [{"start_time": float(c["start_time"]),
                                                     "title": c.get("tags", {}).get("title", "")}
                                                    for c in p.get("chapters", [])], "description": "",
             "local": os.path.abspath(src)}
    else:
        j = json.loads(run_ytdlp(["--skip-download", "--dump-json", url_of(src)]))
        keep = ("id", "title", "channel", "uploader", "upload_date", "duration", "chapters", "description",
                "webpage_url", "view_count", "subtitles", "automatic_captions", "language")
        j = {k: j.get(k) for k in keep}
        j["subtitles"] = sorted((j.get("subtitles") or {}).keys())
        j["automatic_captions"] = sorted(k for k in (j.get("automatic_captions") or {}) if k.startswith("en"))[:12]
    json.dump(j, open(f, "w"), indent=1)
    return j


def cmd_info(src):
    j = info(src)
    print(f"{j.get('title')}\n{j.get('channel')} | {stamp(j.get('duration') or 0)} | {j.get('upload_date') or ''}"
          f" | {j.get('webpage_url') or j.get('local')}")
    if j.get("subtitles") is not None and not is_local(src):
        print("uploaded captions:", ", ".join(j["subtitles"]) or "none",
              "| auto (en):", ", ".join(j.get("automatic_captions") or []) or "none")
    for c in j.get("chapters") or []:
        print(f"  [{stamp(c['start_time'])}] {c['title']}")
    if j.get("description"):
        print("\n" + j["description"][:2500])
    print("\ncache:", outdir(src))


# ---------- transcript ----------
def parse_json3(path):
    """YouTube json3 captions -> [(start_s, text)]"""
    j = json.load(open(path, encoding="utf-8"))
    out = []
    for e in j.get("events", []):
        segs = e.get("segs")
        if not segs:
            continue
        t = "".join(s.get("utf8", "") for s in segs).replace("\n", " ").strip()
        if t:
            out.append((e.get("tStartMs", 0) / 1000, t))
    return out


TS = re.compile(r"(\d+:)?(\d\d):(\d\d)[.,](\d{3})\s+-->")


def parse_vtt(path):
    """WebVTT/SRT (also YouTube's rolling auto-captions, which repeat the previous line) -> [(start_s, text)]"""
    out, last, start, lines = [], [], None, []

    def flush():
        for ln in lines:
            if ln and ln not in last:
                out.append((start, ln))
                last.append(ln)
                del last[:-3]

    for raw in open(path, encoding="utf-8", errors="replace"):
        line = raw.strip()
        m = TS.match(line)
        if m:
            flush()
            h = int(m.group(1)[:-1]) if m.group(1) else 0
            start, lines = h * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000, []
        elif start is not None and line and not line.isdigit() and not line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            t = re.sub(r"<[^>]+>", "", line)
            t = re.sub(r"&nbsp;", " ", t).replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").strip()
            if t:
                lines.append(t)
    flush()
    return out


def get_captions(src, lang):
    d = outdir(src)
    have = glob.glob(os.path.join(d, "captions.*.json3")) + glob.glob(os.path.join(d, "captions.*.vtt")) \
        + glob.glob(os.path.join(d, "captions.*.srt"))
    if have:
        return have[0]
    if is_local(src):                                   # embedded subtitle track, or a sidecar .vtt/.srt
        base = os.path.splitext(src)[0]
        for ext in (".vtt", ".srt", "." + lang + ".vtt", "." + lang + ".srt"):
            if os.path.exists(base + ext):
                dst = os.path.join(d, f"captions.{lang}.{ext.split('.')[-1]}")
                shutil.copy(base + ext, dst)
                return dst
        o = os.path.join(d, "captions.embedded.vtt")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:s:0", o], capture_output=True)
        if r.returncode == 0 and os.path.getsize(o) > 50:
            return o
        sys.exit("no captions in this file (no sidecar .vtt/.srt, no subtitle track) - needs speech-to-text "
                 "(SKILL.md 'No captions')")
    tmpl = os.path.join(d, "captions.%(ext)s")
    j = info(src)                                       # ask only for what the video has: fewer requests
    up = [k for k in j.get("subtitles") or [] if k == lang or k.startswith(lang + "-")]
    auto = [k for k in j.get("automatic_captions") or [] if k in (lang, lang + "-orig")]
    tries = ([("--write-subs", up[0])] if up else []) + ([("--write-auto-subs", auto[0])] if auto else [])
    if not tries:
        sys.exit(f"no '{lang}' captions on this video (uploaded or automatic) - see SKILL.md 'No captions'")
    for kind, code in tries:                            # the uploader's own captions first
        for wait in (0, 60, 180):                       # YouTube rate limit (429): wait, then ask again
            if wait:
                print(f"YouTube said 429 Too Many Requests - waiting {wait} s", file=sys.stderr)
                time.sleep(wait)
            r = run_ytdlp(["--skip-download", kind, "--sub-langs", code, "--sub-format", "json3/vtt/best",
                           "-o", tmpl, url_of(src)], soft=True)
            got = sorted(glob.glob(os.path.join(d, "captions.*.json3")) + glob.glob(os.path.join(d, "captions.*.vtt")))
            if got:
                return got[0]
            if "429" not in r:
                break
        else:
            sys.exit("YouTube kept refusing the captions (429 Too Many Requests) - try again later (an hour), or use "
                     "speech-to-text on the downloaded audio (SKILL.md 'No captions')")
    sys.exit(f"no '{lang}' captions on this video (uploaded or automatic) - see SKILL.md 'No captions'")


def transcript(src, lang="en"):
    f = get_captions(src, lang)
    return parse_json3(f) if f.endswith(".json3") else parse_vtt(f)


def cmd_transcript(src, lang, para):
    j = info(src)
    lines = transcript(src, lang)
    chapters = sorted(j.get("chapters") or [], key=lambda c: c["start_time"])
    ci, out, cur, cur_t = 0, [f"# {j.get('title')}\n", f"{j.get('channel')} | {stamp(j.get('duration') or 0)} | "
                                f"{j.get('webpage_url') or j.get('local')}\n"], [], None
    for t, text in lines:
        while ci < len(chapters) and t >= chapters[ci]["start_time"]:
            if cur:
                out.append(f"[{stamp(cur_t)}] " + " ".join(cur) + "\n")
                cur = []
            out.append(f"\n## [{stamp(chapters[ci]['start_time'])}] {chapters[ci]['title']}\n")
            ci += 1
        if cur and t - cur_t >= para:
            out.append(f"[{stamp(cur_t)}] " + " ".join(cur) + "\n")
            cur = []
        if not cur:
            cur_t = t
        cur.append(text)
    if cur:
        out.append(f"[{stamp(cur_t)}] " + " ".join(cur) + "\n")
    p = os.path.join(outdir(src), "transcript.md")
    open(p, "w", encoding="utf-8").write("\n".join(out))
    words = sum(len(x.split()) for _, x in lines)
    print(f"{p}\n{len(lines)} caption lines, {words} words (~{words * 4 // 3} tokens), "
          f"source {os.path.basename(get_captions(src, lang))}")


def cmd_grep(src, rx, ctx):
    lines = transcript(src)
    r = re.compile(rx, re.I)
    hits = [i for i, (_, x) in enumerate(lines) if r.search(x)]
    shown = set()
    for i in hits:
        for k in range(max(0, i - ctx), min(len(lines), i + ctx + 1)):
            if k not in shown:
                shown.add(k)
                print(f"[{stamp(lines[k][0])}] {'>' if k == i else ' '} {lines[k][1]}")
        print("--")
    print(f"{len(hits)} matches")


# ---------- video ----------
def video_file(src, small=True):
    if is_local(src):
        return os.path.abspath(src)
    d = outdir(src)
    got = glob.glob(os.path.join(d, "video_small.*"))
    if got:
        return got[0]
    run_ytdlp(["-f", "bv*[height<=480][ext=mp4]/bv*[height<=480]/b[height<=480]/w", "-o",
               os.path.join(d, "video_small.%(ext)s"), url_of(src)])
    return glob.glob(os.path.join(d, "video_small.*"))[0]


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def grab(path, t, out, width=480):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                    "-vf", f"scale={width}:-2", out], check=True)


def sheets(frames, d, cols=4, rows=4, title=""):
    from PIL import Image, ImageDraw
    os.makedirs(os.path.join(d, "sheets"), exist_ok=True)
    for f in glob.glob(os.path.join(d, "sheets", "*.png")):
        os.remove(f)
    per, made = cols * rows, []
    for n in range(0, len(frames), per):
        chunk = frames[n:n + per]
        ims = [Image.open(p).convert("RGB") for _, p in chunk]
        w, h = ims[0].size
        sheet = Image.new("RGB", (cols * w, rows * h + 22), "black")
        dr = ImageDraw.Draw(sheet)
        dr.text((6, 4), f"{title}  frames {n + 1}-{n + len(chunk)} of {len(frames)}", fill="white")
        for k, (im, (t, _)) in enumerate(zip(ims, chunk)):
            x, y = k % cols * w, 22 + k // cols * h
            sheet.paste(im.resize((w, h)), (x, y))
            dr.rectangle([x, y, x + 62, y + 16], fill="black")
            dr.text((x + 4, y + 2), stamp(t), fill="yellow")
        p = os.path.join(d, "sheets", f"sheet_{n // per + 1:02d}.png")
        sheet.save(p)
        made.append(p)
    return made


def cmd_frames(src, every, count, scene, t0, t1):
    path = video_file(src)
    d = outdir(src)
    fd = os.path.join(d, "frames.new")                 # the old frames stay until the new set worked
    shutil.rmtree(fd, ignore_errors=True)
    os.makedirs(fd)
    dur = duration(path)
    a, b = secs(t0) if t0 else 0.0, min(secs(t1), dur) if t1 else dur
    if scene:                                           # cuts: frames where the picture changes a lot
        r = subprocess.run(["ffmpeg", "-v", "info", "-ss", str(a), "-to", str(b), "-i", path, "-vf",
                            f"select='gt(scene,{scene})',showinfo,scale=480:-2", "-vsync", "vfr",
                            os.path.join(fd, "s_%04d.png")], capture_output=True, text=True)
        ts = [a + float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
        files = sorted(glob.glob(os.path.join(fd, "s_*.png")))
        frames = list(zip(ts, files))
    else:
        step = float(every) if every else max(1.0, (b - a) / (count or 96))
        frames, t, k = [], a, 0
        while t < b:
            p = os.path.join(fd, f"f_{k:04d}_{int(t)}.png")
            grab(path, t, p)
            frames.append((t, p))
            t, k = t + step, k + 1
    frames = [(t, p) for t, p in frames if os.path.exists(p) and os.path.getsize(p) > 0]   # past the last frame: none
    if not frames:
        shutil.rmtree(fd, ignore_errors=True)
        sys.exit("no frames (scene threshold too high? try --scene 0.1, or --every 30)")
    final = os.path.join(d, "frames")
    shutil.rmtree(final, ignore_errors=True)
    os.rename(fd, final)
    frames = [(t, os.path.join(final, os.path.basename(p))) for t, p in frames]
    json.dump([[t, p] for t, p in frames], open(os.path.join(d, "frames.json"), "w"))
    made = sheets(frames, d, title=info(src).get("title", "")[:80])
    print(f"{len(frames)} frames from {stamp(a)} to {stamp(b)} -> {len(made)} contact sheets:")
    for p in made:
        print(" ", p)


def cmd_at(src, times, wide):
    path = video_file(src)
    d = os.path.join(outdir(src), "at")
    os.makedirs(d, exist_ok=True)
    for t in times:
        s = secs(t)
        p = os.path.join(d, f"at_{int(s)}.png")
        grab(path, s, p, wide)
        print(p)


def cmd_ocr(src):
    d = outdir(src)
    fr = json.load(open(os.path.join(d, "frames.json")))
    out = []
    for t, p in fr:
        if not os.path.exists(p):
            continue
        r = subprocess.run(["tesseract", p, "-", "--psm", "11"], capture_output=True, text=True)
        words = [w for w in r.stdout.split() if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9'.,:%/+-]*", w)
                 and sum(ch.isalpha() for ch in w) >= 2 and not re.fullmatch(r"(.)\1+", w.lower())]
        txt = " ".join(words)
        if len(words) >= 3:                             # drop frames whose "text" is noise
            out.append(f"[{stamp(t)}] {txt}")
    p = os.path.join(d, "frames_ocr.md")
    open(p, "w").write("\n".join(out) + "\n")
    print(p, f"({len(out)} frames with text)")


def audio_file(src):
    if is_local(src):
        return os.path.abspath(src)
    d = outdir(src)
    got = glob.glob(os.path.join(d, "audio.*"))
    if got:
        return got[0]
    run_ytdlp(["-f", "ba[ext=m4a]/ba/b", "-o", os.path.join(d, "audio.%(ext)s"), url_of(src)])
    return glob.glob(os.path.join(d, "audio.*"))[0]


def cmd_stt(src, model, lang):
    py = os.environ.get("VIDEO_WHISPER_PY", os.path.expanduser("~/.venvs/whisper/bin/python"))
    if not os.path.exists(py):
        sys.exit(f"no speech-to-text Python at {py} - see SKILL.md 'No captions' (faster-whisper venv)")
    a = audio_file(src)
    out = os.path.join(outdir(src), f"captions.{lang}.srt")
    subprocess.run([py, os.path.join(HERE, "stt_worker.py"), a, out + ".part", model, lang], check=True)
    os.replace(out + ".part", out)
    print(out, "- now run: video.py transcript", src)


def cmd_clip(src, a, b):
    if is_local(src):
        sys.exit("local file: use 'at' or 'frames --from --to' directly")
    d = outdir(src)
    o = os.path.join(d, f"clip_{int(secs(a))}_{int(secs(b))}.%(ext)s")
    run_ytdlp(["-f", "bv*[height<=720]+ba/b[height<=720]/b", "--download-sections", f"*{a}-{b}", "-o", o, url_of(src)])
    print(glob.glob(o.replace("%(ext)s", "*"))[0])


def main():
    global opt_model
    lang = opt("--lang", "en")
    opt_model = opt("--model", "small")
    para = opt("--para", 30.0, float)
    ctx = opt("--context", 1, int)
    every, count, scene = opt("--every"), opt("--count", None, int), opt("--scene")
    t0, t1, wide = opt("--from"), opt("--to"), opt("--wide", 1280, int)
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    c, src = a[0], a[1]
    if c == "info":
        cmd_info(src)
    elif c == "transcript":
        cmd_transcript(src, lang, para)
    elif c == "grep":
        cmd_grep(src, a[2], ctx)
    elif c == "frames":
        cmd_frames(src, every, count, scene, t0, t1)
    elif c == "at":
        cmd_at(src, a[2:], wide)
    elif c == "ocr":
        cmd_ocr(src)
    elif c == "audio":
        print(audio_file(src))
    elif c == "stt":
        cmd_stt(src, opt_model, lang)
    elif c == "clip":
        cmd_clip(src, a[2], a[3])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
