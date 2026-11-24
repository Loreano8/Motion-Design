"""Musique synthétisée à partir de timing.js (l'horloge maître). Aucun sample.
Chaque son tombe 1 image (1/60 s) après l'événement visuel correspondant.
Usage : python3 score.py  ->  score.wav (48 kHz, stéréo)
"""
import json, re, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
T = json.loads(re.search(r"\{.*\}", (HERE / "timing.js").read_text(), re.S).group(0))
SR, DUR = 48000, T["duration"]
LAG = 1 / T["fps"]
BEAT = 60 / T["bpm"]
out = np.zeros(int(SR * DUR))
rng = np.random.default_rng(7)  # seeded: same file every run

def place(sig, t, gain=1.0):
    i = int(round((t + LAG) * SR))
    n = min(len(sig), len(out) - i)
    if n > 0:
        out[i:i + n] += gain * sig[:n]

def env(n, a=0.002, d=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)

def hat():
    n = int(0.06 * SR)
    x = np.diff(rng.standard_normal(n + 1))  # crude high-pass
    return x * env(n, 0.0005, 0.015) * 0.5

def pluck(freq, d=0.35):
    n = int(1.2 * SR); t = np.arange(n) / SR
    tone = sum(np.sin(2 * np.pi * freq * h * t) / h ** 1.6 for h in (1, 2, 3, 4))
    return tone * env(n, 0.002, d)

def chord(freqs, length, a=0.4, r=0.6):
    n = int(length * SR); t = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.003 * f * t) for f in freqs)
    shape = np.minimum(1, t / a) * np.minimum(1, (length - t) / r).clip(0)
    return sig * shape / len(freqs)

def boom():
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 38 + 60 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.35)

N = lambda m: 440 * 2 ** ((m - 69) / 12)  # MIDI -> Hz

# rhythm
m = T["music"]
for t in np.arange(m["kick_from"], m["kick_to"] + 1e-6, BEAT):
    place(kick(), t, 0.9)
for t in np.arange(m["hat_from"] + BEAT / 2, m["hat_to"], BEAT):
    place(hat(), t, 0.35)

# blocks land: C5 E5 G5 C6
for t, note in zip(T["blocks"], (72, 76, 79, 84)):
    place(pluck(N(note)), t, 0.45)
# title words: G4 A4 C5
for (word, t), note in zip(T["words"].items(), (67, 69, 72)):
    place(pluck(N(note), 0.5), t, 0.35)
# dates: boom + C chord stab
for t in (T["dates"]["28"], T["dates"]["29"]):
    place(boom(), t, 0.8)
    place(chord([N(48), N(55), N(60)], 0.5, 0.005, 0.3), t, 0.35)
place(pluck(N(84), 0.2), T["dates"]["NOVEMBER 2026"], 0.25)
# place: A minor lift
place(chord([N(57), N(60), N(64)], 0.6, 0.005, 0.4), T["place"]["BANGKOK"], 0.4)
place(pluck(N(88), 0.25), T["place"]["VENUE"], 0.2)
# pad under the whole hold, gone before the loop point
place(chord([N(48), N(55), N(64), N(71)], 7.3, 1.0, 1.2), 2.0, 0.18)
# exit: descending plucks on the stagger
for i, note in enumerate((84, 79, 76, 72, 67)):
    place(pluck(N(note), 0.25), T["exit"]["start"] + i * 0.1, 0.25)

# stereo: tiny Haas widening on everything but the low end is fine for a 10 s loop
out /= np.abs(out).max() * 1.12
left, right = out, np.concatenate([np.zeros(int(0.008 * SR)), out[:-int(0.008 * SR)]]) * 0.97
pcm = (np.stack([left, right], 1) * 32767).astype("<i2")
with wave.open(str(HERE / "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score.wav", len(out) / SR, "s")
