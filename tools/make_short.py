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
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--images", help="folder of images, used in filename order")
    src.add_argument("--frames", help="folder of pre-rendered 1080x1920 JPEG frames 00000.jpg... (tools/render_frames.js)")
    ap.add_argument("--fps", type=int, default=FPS, help="frame rate of --frames (default 30)")
    ap.add_argument("--audio", required=True, help="voiceover file (mp3/wav)")
    ap.add_argument("--srt", help="optional subtitle file burned in as big centred captions")
    ap.add_argument("--music", help="optional background music (YouTube Audio Library etc.)")
    ap.add_argument("--music-db", type=float, default=-26.0, help="music level in dB (default -26)")
    ap.add_argument("--durations", help="comma-separated seconds per image (e.g. from voiceover line timings); "
                    "the last image is stretched to the end of the audio. Default: equal split")
    ap.add_argument("--caption-pos", choices=["center", "bottom"], default="center",
                    help="caption position; bottom sits just above the YouTube Shorts UI")
    ap.add_argument("--caption-size", type=int, default=20, help="caption font size (ASS units, default 20)")
    ap.add_argument("--caption-margin", type=int, default=62, help="bottom margin for --caption-pos bottom (default 62)")
    ap.add_argument("--caption-style", choices=["paper", "neon"], default="paper",
                    help="paper = cream text, navy outline; neon = white text, magenta glow outline")
    ap.add_argument("--out", required=True, help="output .mp4")
    a = ap.parse_args()

    total = duration(Path(a.audio)) + 0.3
    if a.frames:
        images = []
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-framerate", str(a.fps), "-i", str(Path(a.frames) / "%05d.jpg"), "-i", a.audio]
        if a.music:
            cmd += ["-stream_loop", "-1", "-i", a.music]
        audio_idx = 1
        parts = [f"[0:v]scale={W}:{H},setsar=1,format=yuv420p[vc]"]
        return finish(a, cmd, parts, audio_idx, total, "frames")
    images = sorted(p for p in Path(a.images).iterdir() if p.suffix.lower() in IMG_EXT)
    if not images:
        sys.exit(f"No images found in {a.images}")
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
    finish(a, cmd, parts, audio_idx, total, f"{len(images)} images")


def finish(a, cmd, parts, audio_idx, total, what):

    vlast = "vc"
    if a.srt:
        srt = str(Path(a.srt).resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        pos = f"Alignment=2,MarginV={a.caption_margin}" if a.caption_pos == "bottom" else "Alignment=10,MarginV=0"
        look = {"paper": "FontName=Montserrat ExtraBold,PrimaryColour=&H00E1EDF4,OutlineColour=&H003D2114,Outline=3,Shadow=1",
                "neon": "FontName=Inter Black,PrimaryColour=&H00FFFFFF,OutlineColour=&H00B56FFF,Outline=2.5,Shadow=0"}
        style = f"{look[a.caption_style]},Fontsize={a.caption_size},Bold=1,BorderStyle=1,{pos}"
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
    print(f"✅ {a.out}  ({total:.1f}s, {what})")


if __name__ == "__main__":
    main()
