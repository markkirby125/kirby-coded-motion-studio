#!/usr/bin/env python3
"""audio_qa.py <audio-file> [--threshold -38] [--min-speech-seconds 60%]

Per-second RMS audio QA. Fails (exit 1) if speech does not span the file:
- computes per-second RMS buckets (astats reset per ~1s of frames)
- a second is 'loud' if RMS > threshold (default -38 dB)
- PASS requires loud seconds >= min_share of total seconds
Overall volumedetect means are NOT acceptable QA (they hide tail-crammed takes).
"""
import argparse
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def per_second_rms(path: str, seconds: int) -> list[float]:
    """astats reset=1 emits one RMS entry per audio frame (~23 ms); pure-digital-silence
    frames report -inf. Bucket the frames into `seconds` even slices (a -inf frame counts
    as silence, never dropped — dropping it shifts every later window)."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
        meta = tf.name
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path,
         "-af", f"astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file={meta}",
         "-f", "null", "-"],
        check=True, capture_output=True)
    text = Path(meta).read_text()
    Path(meta).unlink(missing_ok=True)
    vals = []
    for m in re.findall(r"RMS_level=(-?(?:\d+\.?\d*|inf|nan))", text):
        v = float(m)
        vals.append(-120.0 if (math.isinf(v) or math.isnan(v)) else v)
    if not vals:
        return []
    per = len(vals) / seconds
    out = []
    for i in range(seconds):
        lo, hi = int(i * per), max(int((i + 1) * per), int(i * per) + 1)
        out.append(sum(vals[lo:hi]) / (hi - lo))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--threshold", type=float, default=-38.0)
    ap.add_argument("--min-share", type=float, default=0.5,
                    help="minimum fraction of seconds that must carry speech (0..1)")
    a = ap.parse_args()

    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", a.audio], capture_output=True, text=True).stdout.strip())
    secs = max(1, round(dur))
    sec_vals = per_second_rms(a.audio, secs)
    if not sec_vals:
        print("audio_qa: no RMS data (bad file?)"); return 1
    loud = [v for v in sec_vals if v > a.threshold]
    share = len(loud) / len(sec_vals)
    ok = share >= a.min_share and len(sec_vals) >= 1
    print(f"audio_qa: {'PASS' if ok else 'FAIL'} — {len(loud)}/{len(sec_vals)} loud seconds "
          f"({share:.0%}), duration {dur:.2f}s")
    for i, v in enumerate(sec_vals, 1):
        if v <= a.threshold:
            print(f"  quiet second {i}: {v:.1f} dB")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
