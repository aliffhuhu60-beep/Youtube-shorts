#!/usr/bin/env python3
"""Assemble a vertical 1080x1920 YouTube Short from images + voiceover (+ optional .srt captions).

Each image gets an equal slice of the audio length with a slow zoom (Ken Burns).
Requires: ffmpeg on PATH. No Python packages needed.

Example:
  python3 tools/make_short.py --images shorts/ep01/img --audio shorts/ep01/voice.mp3 \
      --srt shorts/ep01/subs.srt --music music.mp3 --out shorts/ep01/final.mp4
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

W, H, FPS = 1080, 1920, 30
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--images", required=True, help="folder of images, used in filename order")
    ap.add_argument("--audio", required=True, help="voiceover file (mp3/wav)")
    ap.add_argument("--srt", help="optional subtitle file burned in as big centred captions")
    ap.add_argument("--music", help="optional background music (YouTube Audio Library etc.)")
    ap.add_argument("--music-db", type=float, default=-26.0, help="music level in dB (default -26)")
    ap.add_argument("--durations", help="comma-separated seconds per image (e.g. from voiceover line timings); "
                    "the last image is stretched to the end of the audio. Default: equal split")
    ap.add_argument("--caption-pos", choices=["center", "bottom"], default="center",
                    help="caption position; bottom sits just above the YouTube Shorts UI")
    ap.add_argument("--out", required=True, help="output .mp4")
    a = ap.parse_args()

    images = sorted(p for p in Path(a.images).iterdir() if p.suffix.lower() in IMG_EXT)
    if not images:
        sys.exit(f"No images found in {a.images}")
    total = duration(Path(a.audio)) + 0.3
    if a.durations:
        durs = [float(x) for x in a.durations.split(",")]
        if len(durs) != len(images):
            sys.exit(f"--durations has {len(durs)} values but there are {len(images)} images")
        durs[-1] = max(0.5, total - sum(durs[:-1]))
    else:
        durs = [total / len(images)] * len(images)

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for img in images:  # one frame per image; zoompan below expands it to the right length
        cmd += ["-i", str(img)]
    cmd += ["-i", a.audio]
    audio_idx = len(images)
    if a.music:
        cmd += ["-stream_loop", "-1", "-i", a.music]

    parts = []
    for i in range(len(images)):
        frames = max(1, round(durs[i] * FPS))
        zoom_in = i % 2 == 0  # alternate zoom direction for variety
        z = "min(1+0.0015*on,1.15)" if zoom_in else "max(1.15-0.0015*on,1)"
        parts.append(
            f"[{i}:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
            f"setsar=1,format=yuv420p[v{i}]"
        )
    concat_in = "".join(f"[v{i}]" for i in range(len(images)))
    parts.append(f"{concat_in}concat=n={len(images)}:v=1:a=0[vc]")

    vlast = "vc"
    if a.srt:
        srt = str(Path(a.srt).resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        pos = "Alignment=2,MarginV=62" if a.caption_pos == "bottom" else "Alignment=10,MarginV=0"
        style = ("FontName=Montserrat ExtraBold,Fontsize=20,Bold=1,PrimaryColour=&H00E1EDF4,"
                 f"OutlineColour=&H003D2114,BorderStyle=1,Outline=3,Shadow=1,{pos}")
        parts.append(f"[vc]subtitles='{srt}':force_style='{style}'[vs]")
        vlast = "vs"

    if a.music:
        parts.append(f"[{audio_idx + 1}:a]volume={a.music_db}dB[m];"
                     f"[{audio_idx}:a][m]amix=inputs=2:duration=first:dropout_transition=0[aout]")
        amap = "[aout]"
    else:
        amap = f"{audio_idx}:a"

    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{vlast}]", "-map", amap,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print(f"✅ {a.out}  ({total:.1f}s, {len(images)} images)")


if __name__ == "__main__":
    main()
