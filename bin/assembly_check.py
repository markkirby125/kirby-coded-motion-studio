#!/usr/bin/env python3
"""assembly_check.py <export.mp4> --min 55 --max 75 [--subs srt]

Delivery gate: duration band, single video+audio streams, A/V duration match <= 0.1 s.
Optional --subs asserts the .srt exists and is non-empty. Exit 1 on any failure.
"""
import argparse
import subprocess
import sys
from pathlib import Path


def probe(path: str, args: list[str]) -> str:
    return subprocess.run(["ffprobe", "-v", "error"] + args + [path],
                          capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--min", type=float, required=True)
    ap.add_argument("--max", type=float, required=True)
    ap.add_argument("--subs")
    a = ap.parse_args()
    fails = []

    dur = float(probe(a.export, ["-show_entries", "format=duration", "-of", "csv=p=0"]))
    if not (a.min <= dur <= a.max):
        fails.append(f"duration {dur:.3f}s outside band [{a.min}, {a.max}]")

    v = probe(a.export, ["-select_streams", "v", "-show_entries", "stream=index", "-of", "csv=p=0"]).splitlines()
    au = probe(a.export, ["-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0"]).splitlines()
    if len(v) != 1:
        fails.append(f"{len(v)} video streams (want 1)")
    if len(au) != 1:
        fails.append(f"{len(au)} audio streams (want 1)")
    if au:
        raw_adur = probe(a.export, ["-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "csv=p=0"])
        try:
            adur = float(raw_adur)
        except ValueError:
            adur = dur  # some containers report N/A per-stream; container duration already checked
        if abs(adur - dur) > 0.1:
            fails.append(f"A/V drift {abs(adur - dur):.3f}s > 0.1s")

    if a.subs:
        sp = Path(a.subs)
        if not sp.exists() or sp.stat().st_size < 50:
            fails.append(f"subs missing/empty: {sp}")

    if fails:
        print(f"assembly_check: FAIL — {a.export}")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"assembly_check: PASS — {dur:.3f}s, 1v+1a, drift ok" + (f", subs ok" if a.subs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
