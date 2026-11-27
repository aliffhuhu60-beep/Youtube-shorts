#!/usr/bin/env python3
"""Free, local AI voiceover with Kokoro (Apache-2.0, commercial use OK) + timed captions.

Reads a script file (one narration line per row; write "spoken words || caption text" to speak
numbers as words but show them as digits), voices every line, joins them with a short
pause, and writes:
  voice.mp3      the narration
  durations.txt  seconds per line (pass to make_short.py --durations, one image per line)
  subs.srt       captions of 2-4 words, timed inside each line

Setup (once):
  python3 -m venv .venv && .venv/bin/pip install kokoro-onnx soundfile
  download kokoro-v1.0.onnx and voices-v1.0.bin from
  https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 into models/

Example:
  .venv/bin/python tools/voice_kokoro.py shorts/ep02-saturn/script.txt --out shorts/ep02-saturn
Brand voice: bm_george (British male storyteller), speed 0.95.
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

GAP = 0.12  # seconds of silence between lines


def chunk(line: str) -> list[str]:
    words, out, cur = line.split(), [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or (w[-1] in ".,?!;:" and len(cur) >= 2):
            out.append(" ".join(cur))
            cur = []
    if cur:
        if len(cur) == 1 and out:
            out[-1] += " " + cur[0]
        else:
            out.append(" ".join(cur))
    return out


def ts(s: float) -> str:
    return f"{int(s // 3600):02}:{int(s % 3600 // 60):02}:{s % 60:06.3f}".replace(".", ",")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", help="text file, one narration line per row")
    ap.add_argument("--out", required=True, help="output folder")
    ap.add_argument("--models", default="models", help="folder with kokoro-v1.0.onnx and voices-v1.0.bin")
    ap.add_argument("--voice", default="bm_george")
    ap.add_argument("--speed", type=float, default=0.95)
    a = ap.parse_args()

    lines = [l.strip() for l in Path(a.script).read_text().splitlines() if l.strip()]
    m = Path(a.models)
    tts = Kokoro(str(m / "kokoro-v1.0.onnx"), str(m / "voices-v1.0.bin"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    audio, durs, srt, n, t, sr = [], [], [], 1, 0.0, 24000
    for line in lines:
        # "spoken text || caption text" lets numbers be spoken as words but shown as digits
        spoken, _, caption = line.partition("||")
        spoken, caption = spoken.strip(), (caption.strip() or spoken.strip())
        samples, sr = tts.create(spoken, voice=a.voice, speed=a.speed, lang="en-gb")
        samples = np.concatenate([samples, np.zeros(int(GAP * sr), dtype=samples.dtype)])
        d = len(samples) / sr
        parts = chunk(caption)
        total_chars = sum(len(p) for p in parts)
        pt = t + 0.03
        for p in parts:
            pd = (d - GAP - 0.05) * len(p) / total_chars
            srt.append(f"{n}\n{ts(pt)} --> {ts(pt + pd)}\n{p.upper()}\n")
            n += 1
            pt += pd
        audio.append(samples)
        durs.append(d)
        t += d

    wav = out / "voice.wav"
    sf.write(wav, np.concatenate(audio), sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                    "-af", "loudnorm=I=-14:TP=-1.5", "-b:a", "192k", str(out / "voice.mp3")], check=True)
    wav.unlink()
    (out / "durations.txt").write_text(",".join(f"{d:.3f}" for d in durs))
    (out / "subs.srt").write_text("\n".join(srt))
    print(f"✅ {len(lines)} lines, {t:.1f}s -> {out}/voice.mp3, subs.srt, durations.txt")


if __name__ == "__main__":
    main()
