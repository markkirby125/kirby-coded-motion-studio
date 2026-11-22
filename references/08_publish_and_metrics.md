# Module 08: Publish and Metrics

Delivery is measured, packaged, and logged. Nothing is "done" until the checks pass and the
pack exists.

## Delivery checks (blocking)

| Check | Target |
|---|---|
| Loudness | −14 LUFS integrated, true peak ≤ −1.0 dBTP (`ebur128` verify, not the filter's say-so) |
| Duration match | video vs audio ≤ 0.1 s; length in the version's band (Short 60–75 s default) |
| Streams | exactly one video + one audio stream; pixel format/container per platform norm |
| Subtitles | burnt-in `.ass` + upload `.srt`, same text |
| Poster/thumbnail | the clip's own frame (`-frames:v 1`), not a re-encode |

## Upload pack (`publish.md` per video)

Per version: unique title following the channel's title rule (never the outcome),
description (premise line, episode number, playlist link, "new here" line, AI-disclosure
line per the channel's policy), tags/entity list, pinned-comment question, thumbnail
moment, related-video links per the channel's linking map. Tick-boxes before upload; the
altered/synthetic box is ticked wherever the platform requires it.

## Metrics and go/no-go

- Log at 48 h and 7 days per version into `metrics.csv` (the channel's column set — e.g.
  views, swipe-through, avg % viewed, link clicks, subs, comment signals; add per-channel
  columns as decided).
- **Go/no-go gate**: don't start generating the next series until the current series' Ep 1
  has 48 h of numbers. Judge rates, not totals.
- The continuity/Stage-10 log line is written the same day the episode publishes (module 01).

## House rules (from the sibling collection)

- Commits: text only; media stays outside git (or force-added deliberately, one-time, per
  project convention); no attribution/co-author lines in commit messages.
- Handoffs: after each session, update the project's handoff/TASKS docs — state, decisions
  waiting, next steps — so any future session resumes without archaeology.
