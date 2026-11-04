"""Run by video.py under the speech-to-text Python (a venv with faster-whisper): audio file -> .srt.
  python stt_worker.py AUDIO OUT.srt [MODEL] [LANG]"""
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path):
    """ffmpeg -> 16 kHz mono float32 (faster-whisper's own reader breaks with PyAV 19: 'metadata_errors')."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def ts(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


audio, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "small"
lang = sys.argv[4] if len(sys.argv) > 4 else "en"
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, info = m.transcribe(load_audio(audio), language=lang, vad_filter=True, beam_size=1)
with open(out, "w", encoding="utf-8") as f:
    for i, s in enumerate(segs, 1):
        f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
        if i % 50 == 0:
            print(f"  {ts(s.end)[:8]} transcribed", flush=True)
print("done", out)
