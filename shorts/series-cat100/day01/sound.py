"""Day 1 sound design: synthesised music + SFX timed to the voice lines, mixed with the narration."""
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from sfx_lib import SR, Mix, bell, boom, chime, creak, drone, groan, heartbeat, sting, whoosh  # noqa: E402

durs = [float(x) for x in (HERE / "durations.txt").read_text().split(",")]
starts = np.concatenate([[0], np.cumsum(durs)[:-1]])
total = sum(durs) + 0.5
L = lambda i, dt=0.0: starts[i] + dt  # noqa: E731

music = Mix(total)
music.add(drone(total, root=49.0), 0, -4)
# silence before the bell (line 7 end -> line 8), then music returns tense at the end card
gate = music.duck(L(7, 1.6), L(9, 0.2), depth_db=-40, fade=0.6)
music.buf *= gate

fx = Mix(total)
fx.add(boom(1.8, 60), L(0, 0.0), -2)                 # title stamp
fx.add(whoosh(0.5, up=True), L(2, -0.25), -6)          # whip-pan to Biscuit
fx.add(groan(2.4, 85, dist=0.8), L(3, 1.1), -6)        # distant sound in the garden
fx.add(chime(1.4), L(4, 0.05), -10)                    # CAT FACT badge
fx.add(creak(1.0), L(5, 0.1), -8)                      # window pushed open
fx.add(whoosh(0.4, up=False), L(6, -0.2), -4)          # snap zoom
fx.add(sting(2.6), L(6, 0.0), -3)                      # reveal
for k in range(5):                                     # heartbeat through the stare-down
    fx.add(heartbeat(), L(6, 0.6 + k * 0.72), -2)
fx.add(bell(2.4), L(8, 0.15), -1)                      # DING
fx.add(bell(1.6, 2180), L(8, 0.75), -9)
fx.add(groan(2.6, 78, dist=0.0), L(10, 0.05), -2)      # the shambler turns
fx.add(boom(2.0, 50), L(11, 0.0), -5)                  # end card hit

voice, vsr = sf.read(HERE / "voice.mp3")
if voice.ndim > 1:
    voice = voice.mean(axis=1)
voice = np.interp(np.arange(int(len(voice) * SR / vsr)) / SR, np.arange(len(voice)) / vsr, voice)

n = len(music.buf)
v = np.zeros(n)
v[:min(n, len(voice))] = voice[:n]
# duck music under narration (sidechain-style)
env = np.convolve(np.abs(v), np.ones(int(.15 * SR)) / int(.15 * SR), mode="same")
duck = 1 - 0.55 * np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
mix = v * 1.0 + music.buf / (np.abs(music.buf).max() + 1e-9) * 0.16 * duck + fx.buf / (np.abs(fx.buf).max() + 1e-9) * 0.55
mix = np.tanh(mix * 1.1) * 0.9
sf.write(HERE / "mix.wav", mix.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(HERE / "mix.wav"), "-af", "loudnorm=I=-14:TP=-1.5",
                "-b:a", "192k", str(HERE / "mix.mp3")], check=True)
(HERE / "mix.wav").unlink()
print(f"✅ mix.mp3 ({total:.1f}s)")
