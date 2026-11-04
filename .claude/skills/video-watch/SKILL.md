---
name: video-watch
description: Read and "watch" videos - YouTube (or any yt-dlp site) by URL, or a local video file - with video.py - info (title, channel, length, chapters, description), the transcript from the uploader's or automatic captions as clean timestamped text with chapter headings, grep the transcript, contact sheets of stamped frames (an hour in about six images; even spacing or scene cuts), full-size frames at chosen times, OCR of on-screen text, and short clips at higher quality. Method for an hour-long video - transcript first, sheets second, close frames only where the transcript points, the user fills in what can't be seen. Use when the user sends a YouTube link or a video file, asks Claude to watch, summarise or learn from a video (game guides, let's plays, lectures, tutorials), or wants a transcript.
---

# Watching videos (video.py)

The user (2026-11-03): "can you build an app to scrape and read youtube transcripts and watch videos?" He
offered to answer questions about what's on screen, so the video doesn't have to be watched frame by frame.

## Commands (`scripts/video.py`, run with `python3 -I`)
| Command | Does |
|---|---|
| `info SRC` | title, channel, length, captions available, chapters, description |
| `transcript SRC [--lang en] [--para 30]` | `transcript.md`: paragraphs stamped [mm:ss] every 30 s, chapter headings; prints word and token count |
| `grep SRC REGEX [--context 1]` | transcript lines that match, with times |
| `frames SRC [--count 96 \| --every 60 \| --scene 0.1] [--from T --to T]` | downloads a <=480p copy once, then contact sheets of 16 stamped frames (`sheets/sheet_NN.png`) |
| `at SRC T [T...] [--wide 1280]` | single frames at those times (12:34, 754, 1:02:03) |
| `ocr SRC` | Tesseract on the grabbed frames -> `frames_ocr.md` (noise dropped; weak at 480p) |
| `clip SRC FROM TO` | only that part, at <=720p, for a close look (then `at` on the clip file) |

SRC is a URL, an 11-character YouTube id, or a local file (no download; a sidecar `.vtt`/`.srt` or an
embedded subtitle track is used for the transcript). Everything is cached in
`~/.cache/video-watch/<id>/` (VIDEO_WATCH_CACHE changes it), so repeat calls are free.

## Method for a long video (an hour)
The video is downloaded ONCE as a small (<=480p) copy; after that every frame, sheet or time is local and
instant - look only at what's needed (the user, 2026-11-03: "you can download the video and only look at
what you need right?").
1. `info` - chapters and description often give the structure for free.
2. `transcript` - an hour of talk is ~9-10k words (~13k tokens): read it all, in parts with Read.
   Write notes with timestamps as you go.
3. `frames --count 96` - six sheets; look at them for what's on screen (game screens, slides, maps).
   Talk-heavy videos with a fixed camera: `--count 32` is plenty. Edited videos: `--scene 0.1`.
4. `grep` and `at` for the moments the transcript points to ("as you can see here", unit stats, a menu).
   Need it sharper: `clip FROM TO`, then `at` on the clip.
5. Ask the user about what can't be read (fast UI, small text, audio cues) instead of grinding frames.
6. Save the result where it belongs (a game's guide or skill), with the video URL and timestamps as the
   source - and the order of truth still holds: game > mod files > manual > video > wiki > what the user says (manual-first).

## Setup (once)
- Needs yt-dlp (current!), ffmpeg/ffprobe, Pillow; tesseract for `ocr`. All present except a current yt-dlp.
- **yt-dlp must be recent**: YouTube changes break old versions ("Precondition check failed", "No video
  formats found"). Ubuntu's apt copy (2024.04.09) is broken. The user runs, from the prompt:
  `! curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o "$HOME/Desktop/AI Development/.claude/skills/video-watch/bin/yt-dlp" && chmod +x "$HOME/Desktop/AI Development/.claude/skills/video-watch/bin/yt-dlp"`
  (Claude may not download and run outside code itself - the permission check refused it 2026-11-03.)
  Update the same way when it breaks again; `bin/yt-dlp -U` also works.
- New yt-dlp versions want a JavaScript runtime for YouTube (deno preferred; node 18 is present and may be too
  old). If yt-dlp says so: The user installs deno, or set `VIDEO_YTDLP_ARGS` to what yt-dlp asks for.
- Rules: no cookies, logins or bot-check evasion. If YouTube asks to sign in, stop and tell the user
  (he can download the video himself and give the file path).

## No captions (or YouTube refuses them)
YouTube answered 429 Too Many Requests to every caption request on 2026-11-03 (three tries over 15 minutes)
while the video and audio downloads worked. Then transcribe locally:
1. `video.py audio SRC` - audio only (an hour = ~65 MB m4a).
2. `video.py stt SRC [--model small]` - faster-whisper on the CPU (12 cores: roughly 10-20 min an hour with
   `small`, int8; `base` is faster and rougher, `medium` slower and better) -> `captions.en.srt`.
3. `video.py transcript SRC` - uses that file like any captions.
Setup (the user, once - Claude may not download packages itself):
`! python3 -m venv ~/.venvs/whisper && ~/.venvs/whisper/bin/pip install faster-whisper`
then fetch the model once:
`! ~/.venvs/whisper/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"`
(VIDEO_WHISPER_PY points at another Python with faster-whisper.)
Installed 2026-11-03: faster-whisper 1.2.1 in ~/.venvs/whisper, model `small` (484 MB) in ~/.cache/huggingface.
The venv has no pip of its own (Ubuntu lacks python3.12-venv): install into it with the system pip,
`python3 -m pip --python ~/.venvs/whisper/bin/python install X`. faster-whisper's audio reader breaks with
PyAV 19 ("metadata_errors"), so stt_worker.py decodes with ffmpeg itself. Speed: about 2x real time on the CPU.

## Status
Built and tested 2026-11-03 on a local file (the Troban battle replay mp4 with a sample rolling auto-caption
.vtt): info, transcript (rolling-caption de-duplication), grep, frames (count and scene), at, ocr all work.
YouTube tested 2026-11-03 with yt-dlp 2026.10.26 in bin/ (the user fetched it; no deno needed so far): info,
transcript (uploaded captions, json3), frames from the downloaded 480p copy all work. Auto-generated-only
captions not yet seen on a real video - check the first one's transcript for repeated lines.

## Related skills
game-sources (manuals and wikis), wiki-scout, learn-to-play, learn-from-tutorials (in-game tutorials),
manual-first (order of truth), game-ui (ocr.py).
