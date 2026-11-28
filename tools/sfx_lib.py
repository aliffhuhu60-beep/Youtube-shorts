"""Procedural (synthesised) music + sound effects — 100% original, no samples, no copyright.

Every sound is generated from sine waves and noise with numpy, so the channel owns all of it.
Used by each episode's sound.py:  from sfx_lib import *
"""
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.01, r=0.3):
    e = np.ones(n)
    na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lowpass(x, cutoff):
    """One-pole low-pass, cutoff in Hz (scalar or per-sample array)."""
    c = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    a = np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # small, fine for short SFX
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def lowpass_fast(x, cutoff):
    """FFT low-pass for long signals (fixed cutoff)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[f > cutoff] *= 0
    return np.fft.irfft(X, len(x))


def drone(d, root=55.0, dark=True):
    """Dark ambient pad: detuned sines + slow LFO + filtered wind noise."""
    t = t_(d)
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
    ratios = [1, 1.5, 2.0, 2.4 if dark else 2.52, 3.0]
    x = sum(np.sin(2 * np.pi * root * r * t + 0.3 * np.sin(2 * np.pi * 0.11 * (i + 1) * t)) / (i + 1.5)
            for i, r in enumerate(ratios))
    x = x + 0.5 * sum(np.sin(2 * np.pi * root * r * 1.004 * t) / (i + 2) for i, r in enumerate(ratios[:3]))
    wind = lowpass_fast(rng.standard_normal(len(t)), 400) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + 1))
    out = (x * lfo * 0.25 + wind * 0.6)
    return out * env(len(t), 2.0, 2.0)


def boom(d=1.6, f0=70):
    t = t_(d)
    f = f0 * np.exp(-t * 2.5) + 30
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3)
    x += lowpass_fast(rng.standard_normal(len(t)), 300) * np.exp(-t * 8) * 0.5
    return x


def whoosh(d=0.6, up=True):
    t = t_(d)
    n = rng.standard_normal(len(t))
    sweep = np.linspace(300, 4000, len(t)) if up else np.linspace(4000, 300, len(t))
    x = lowpass(n, sweep) - lowpass(n, sweep * 0.3)
    return x * np.sin(np.pi * t / d) ** 2 * 2.5


def heartbeat(d=0.6):
    t = t_(d)
    def thump(dt, amp):
        tt = np.clip(t - dt, 0, None)
        return amp * np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 18) * (t >= dt)
    return thump(0, 1.0) + thump(0.18, 0.7)


def bell(d=2.2, f=2100):
    t = t_(d)
    parts = [(1, 1.0, 2.2), (2.76, 0.5, 3.5), (5.4, 0.25, 5), (8.93, 0.12, 7)]
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dec) for r, a, dec in parts)
    return x * env(len(t), 0.002, 0.2) * 0.5


def groan(d=2.2, f0=95, dist=0.0):
    """Zombie groan: vibrato saw through a formant-ish low-pass. dist (0..1) = far away (darker, quieter)."""
    t = t_(d)
    f = f0 * (1 + 0.06 * np.sin(2 * np.pi * 5.5 * t)) * (1 - 0.15 * t / d)
    ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1) - 1
    x = lowpass(saw + 0.3 * rng.standard_normal(len(t)), 700 * (1 - 0.6 * dist) + 200 * np.sin(np.pi * t / d))
    return x * np.sin(np.pi * t / d) ** 1.5 * (1 - 0.6 * dist)


def creak(d=0.9):
    t = t_(d)
    f = 180 + 120 * np.sin(2 * np.pi * 1.3 * t)
    pulses = (np.sin(2 * np.pi * np.cumsum(f) / SR) > 0.97).astype(float)
    return lowpass(pulses, 2500) * env(len(t), 0.05, 0.3) * 3


def chime(d=1.2):
    t = t_(d)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 4) * a for f, a in [(880, .5), (1320, .35), (1760, .2)])


def sting(d=2.5):
    """Dissonant reveal hit (cluster chord + boom)."""
    t = t_(d)
    x = sum(np.sin(2 * np.pi * f * t) for f in [110, 116.5, 164.8, 233.1]) * np.exp(-t * 1.2) * 0.3
    return x + boom(d, 90) * 0.8


class Mix:
    def __init__(self, seconds):
        self.buf = np.zeros(int(seconds * SR) + SR)

    def add(self, x, at, gain_db=0.0):
        i = int(at * SR)
        x = x[: max(0, len(self.buf) - i)]
        self.buf[i:i + len(x)] += x * 10 ** (gain_db / 20)

    def duck(self, start, end, depth_db=-30, fade=0.25):
        g = np.ones(len(self.buf))
        a, b, f = int(start * SR), int(end * SR), int(fade * SR)
        low = 10 ** (depth_db / 20)
        g[a:b] = low
        g[max(0, a - f):a] = np.linspace(1, low, a - max(0, a - f))
        g[b:b + f] = np.linspace(low, 1, len(g[b:b + f]))
        return g
