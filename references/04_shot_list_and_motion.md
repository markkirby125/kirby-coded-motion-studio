# Module 04: Shot List and Coded Motion

The heart of the no-video-model doctrine: **a shot is a still plus a coded move, or a
rendered insert**. Author the **text-only `shots.json` pass** (`id`, `engine`, `template` for inserts, canonical `dialogue[*].line`, `sub`, and `insert` `text`, plus optional `tts_text` override if phonetic respelling is needed) **first — before Module 03 voice synthesis** so [`07_qa_and_review.md`](./07_qa_and_review.md) can verify `bible/claims.md` and `bible/pronunciation.md` against concrete canonical lines; then fill `seconds` and `at` offsets from Module 03's measured audio. Motion is authored in `@shot_list` and executed by ffmpeg/Python —
deterministic, free, and frame-exact.

## `@shot_list` (`shots.json`) — one row per shot

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable; `s*` Short spine, `b*`/`a*` extensions, `i*` inserts |
| `engine` | `still` \| `insert` | `still` = generated frame + `@motion_spec`; `insert` = rendered graphic |
| `seconds` | number | From measured voice audio (module 03), rounded to the channel's norm |
| `start_short` / `start_full` | number | Computed after timing; contiguous per version |
| `in` | `short`/`full`/`short+full` | Version membership |
| `size` / `camera` / `action` / `acting` | strings | The visual script; `action` is prose, never drawn text |
| `characters` | list | Cast IDs; drives wardrobe variant lookup |
| `wardrobe` | string | Active variant ID from `@wardrobe_ledger` |
| `motion` | object | The `@motion_spec` (below); default `{"type":"push","rate":0.0075}` |
| `dialogue` | list | `{character, line, sub, tts_text?, at}` — `tts_text` optional (respelling for TTS only; `line` stays canonical); `at` from measured audio |
| `start_frame` | string | stills only: source PNG path for the coded move |
| `place` | object | inserts only: overlay position `{x, y, w}` |
| `template` | string | inserts only: which renderer/template |
| `text` | list | inserts only: verbatim drawn lines |

## Shot grammar (rules that make coded motion work)

1. **Never a visible talking mouth.** Lines land over the shoulder, on the listener's face, on hands, on objects, or off-screen. Insert text speaks exposition.
2. Default mix (a heuristic, not measured; the project layer may retune): roughly half close-ups, a third mediums, the rest wide "small figure in big space" — cheap to generate, strong to push-in on.
3. Every `still` gets exactly one coded move; every insert is a full-frame card or a placed overlay.
4. Nothing in frame is *required* to move for the story; the move supplies the life.

## The coded motion vocabulary (`@motion_spec`)

| Type | Parameters | Effect |
|---|---|---|
| `push` | `rate` (zoom/s, ≤0.05) | Centre zoom-in; the default (0.75%/s) |
| `hold` | — | Static (locked-off feel); `{"type":"hold"}` for establishing frames |
| `pan` | `dx`,`dy` (px/s) | Slow drift across an oversized frame |
| `parallax` | `layers`, `factor` | Foreground/background offset drift (two stills) |
| `shake` | `amp`,`hz`,`hit_at` | fx-shake style jolt + dust overlay (one loud moment per series max) |
| `drift` | `rate`,`angle` | Very slow de-centred float (unease) |
| `xfade` | `dur` | Crossfade into the next part (montage) |

Implementation notes (all measured/proven):
- Push/hold/pan are one ffmpeg/Python pass per part (zoompan on an oversized render, sub-pixel smooth; a 9:16 frame is scaled to fill and cropped — a few edge rows/cols).
- `shake` composites a pre-rendered fx clip over the still (amp ≤ 24 px; low hz reads smoother).
- Parts are video-only 1080×1920 (or the channel's norm) 30 fps, exactly `seconds` long, normalised to the same codec/pixel-format before concat — then one final re-encode adds audio and subtitles (module 08).

## Inserts (code-rendered, no model credits, intended deterministic)

Rendered graphics — captions, comms/readouts, notes, end cards, Previously — are **code-rendered**, never generated: headless-Chromium HTML→PNG frames (intended to be deterministic, with byte-identical re-renders reported but not independently verified here; one-line cards may use ffmpeg `drawtext`), assembled to film and either joined as opaque cut-aways or alpha-composited as overlays at their `start_<v>` times. On-screen text obeys the project layer's language policy (e.g. invented-language station text, English cards). A length change to any insert is a timing change: recompute starts, `at`s and captions downstream.

## Assembly (per version)

1. Build every part (still+motion, insert) → `parts/<id>.mp4`.
2. Concat video-only (`-f concat -c copy`) in `start_<v>` order → `joined-<v>.mp4`.
3. Voice: each line at `start + at` (`adelay=<ms>:all=1`, `amix normalize=0`).
4. Sfx/room bed from the shot's sound column (supplied by the project layer; not in the base `@shot_list` schema), engine `moss-sfx-v2` only (policy in the [`kirby-local-first-video-pipeline` dispatcher](../../kirby-local-first-video-pipeline/references/00_dispatcher.md)); one loud moment cap.
5. Final pass — single re-encode: overlays → subtitles burn-in → audio `apad=whole_dur=$DUR,atrim=end=$DUR` **then** `loudnorm I=-14:TP=-1.0:LRA=11` → `export/<v>.mp4` (libass-enabled ffmpeg). Measured lesson (2026-11-07 dry run): loudnorm without a preceding pad/trim truncated the padded tail by ~3 s — always pad→trim→loudnorm, in that order.
6. `bin/assembly_check.py` asserts durations (video vs audio ≤0.1 s), length band, stream count — exit 1 on any failure.
