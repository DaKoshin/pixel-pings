#!/usr/bin/env python3
"""Synthesizes the 8-bit notification sounds into ../sounds. Uses no audio samples.

Run: python3 scripts/generate.py
To change a sound, edit SOUNDS below and run the script again.
"""
import array
import math
import wave
from pathlib import Path

RATE = 22050
FRAME = RATE / 60  # like old consoles, pitch and volume change 60 times a second
BIT_LEVELS = 31  # 5-bit resolution gives the sound its grain
LOUDNESS_DB = -23.5  # average loudness; +6 dB doubles the amplitude
OUT_DIR = Path(__file__).resolve().parent.parent / "sounds"

# Share of each cycle a pulse wave stays high: smaller sounds thinner.
DUTY = {"pulse12": 0.125, "pulse25": 0.25, "pulse50": 0.5}

# A note is (start frame, length in frames, wave, pitch, volume, decay, slide),
# where slide is in semitones per frame. The last three fields are optional.
SOUNDS = {
    # Finished: a quick rising D major arpeggio with an echo and a bass line.
    "done": [
        (0, 4, "pulse25", "D5", 0.8),
        (4, 4, "pulse25", "F#5", 0.8),
        (8, 4, "pulse25", "A5", 0.8),
        (12, 20, "pulse25", "D6", 0.9, True),
        (3, 4, "pulse12", "D5", 0.3),
        (7, 4, "pulse12", "F#5", 0.3),
        (11, 4, "pulse12", "A5", 0.3),
        (15, 20, "pulse12", "D6", 0.3, True),
        (0, 12, "triangle", "D3"),
        (12, 20, "triangle", "A3", 1.0, True),
    ],
    # Needs you: a double beep, then a higher tone that sounds like a question.
    "attention": [
        (0, 3, "pulse12", "F#5", 0.9),
        (5, 3, "pulse12", "F#5", 0.9),
        (10, 10, "pulse12", "C#6", 1.0, True),
        (13, 8, "pulse12", "C#6", 0.3, True),
    ],
    # Rate limit: a falling phrase that ends in a pitch drop and a noise hit.
    "limit": [
        (0, 5, "pulse50", "E4", 0.7),
        (5, 5, "pulse50", "C4", 0.7),
        (10, 5, "pulse50", "A3", 0.7),
        (15, 18, "pulse50", "F3", 0.8, True, -0.25),
        (15, 18, "triangle", "F2", 1.0, True, -0.1),
        (15, 8, "noise", "A6", 0.5, True),
    ],
}


def hz(pitch):
    semitone = "C D EF G A B".index(pitch[0]) + ("#" in pitch)
    midi = semitone + 12 * (int(pitch[-1]) + 1)
    return 440 * 2 ** ((midi - 69) / 12)


def oscillator(kind, phase, lfsr):
    if kind == "triangle":
        return (abs(int(phase * 32) - 15.5) - 7.75) / 7.75
    if kind == "noise":
        return 1.0 if lfsr & 1 else -1.0
    duty = DUTY[kind]
    # Removing the DC offset keeps notes from clicking at the start and end.
    return (1.0 if phase < duty else -1.0) - (2 * duty - 1)


def add_note(buf, start, frames, kind, pitch, volume=1.0, decay=False, slide=0.0):
    first = int(start * FRAME)
    phase = 0.0
    lfsr = 1
    for i in range(min(int(frames * FRAME), len(buf) - first)):
        frame = int(i / FRAME)
        level = volume * (1 - frame / frames) if decay else volume
        level = round(level * 15) / 15  # 16 volume steps
        phase += hz(pitch) * 2 ** (slide * frame / 12) / RATE
        if phase >= 1:
            phase -= 1
            lfsr = (lfsr >> 1) | (((lfsr ^ (lfsr >> 1)) & 1) << 14)
        buf[first + i] += level * oscillator(kind, phase, lfsr)


def render(notes):
    total = max(note[0] + note[1] for note in notes)
    buf = [0.0] * int(total * FRAME)
    for note in notes:
        add_note(buf, *note)
    peak = max(abs(s) for s in buf)
    crushed = [round(s / peak * BIT_LEVELS) / BIT_LEVELS for s in buf]
    rms = math.sqrt(sum(s * s for s in crushed) / len(crushed))
    scale = 10 ** (LOUDNESS_DB / 20) / rms
    return array.array("h", (int(s * scale * 32767) for s in crushed))


def main():
    for name, notes in SOUNDS.items():
        path = OUT_DIR / f"{name}.wav"
        with wave.open(str(path), "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(RATE)
            out.writeframes(render(notes).tobytes())
        print(path)


if __name__ == "__main__":
    main()
