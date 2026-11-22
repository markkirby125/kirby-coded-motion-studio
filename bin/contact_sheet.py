#!/usr/bin/env python3
"""contact_sheet.py <media> <out.png> [--frames 8]

Vision-QA contact sheet: N evenly-spaced frames tiled 4x2 (or 3x2 for 6), scaled to
360px wide tiles. Works on any ffmpeg-readable video; for stills just copy the file.
"""
import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("out")
    ap.add_argument("--frames", type=int, default=8, choices=[6, 8])
    a = ap.parse_args()

    if Path(a.media).suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        Path(a.out).write_bytes(Path(a.media).read_bytes())
        print(f"contact_sheet: still copied -> {a.out}")
        return 0

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", a.media],
        capture_output=True, text=True, check=True)
    frames = int(probe.stdout.strip() or "240")
    k = max(1, frames // a.frames)
    tile = "4x2" if a.frames == 8 else "3x2"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.media,
           "-vf", f"select='not(mod(n\\,{k}))',scale=360:-1,tile={tile}",
           "-fps_mode", "passthrough", "-frames:v", "1", a.out]
    subprocess.run(cmd, check=True)
    print(f"contact_sheet: {a.out} ({a.frames} frames, every {k})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
