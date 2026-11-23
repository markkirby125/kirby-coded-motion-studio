# Module 03: Voice

Local TTS only for this pipeline's voice route. Cloud TTS (Gemini, ElevenLabs) is out of policy since 2026-11-07 and never called inside this production pipeline (the narration and voice-ledger steps it controls), for any reason: no quota, no budget gate, no cloud fallback. Third-party tools outside this pipeline (for example NotebookLM Audio Overviews, routed by [`kirby-off-page-seo`](../../kirby-off-page-seo/SKILL.md) Module 26) are for separate deliverables only; their audio is never used as narration, character voice or any other audio in this pipeline. The engine routes (`moss-nano-tts` for narration and host, `moss-voice` for characters) and the `@tts_ledger`, which refuses to record a cloud engine, live in the sibling skill (`kirby-local-first-video-pipeline`, module 02); this module adds the studio's character-voice machinery.

## Voice ledger (`bible/voices.md` + `assets/voice-ledger.template.json`)

One locked entry per speaking character, recorded **before** the first generated line:

| Field | Rule |
|---|---|
| character | Cast name |
| engine | `moss-voice` or `moss-nano-tts`. Columns follow the canonical schema in [`04_qa_and_delivery.md`](../../kirby-local-first-video-pipeline/references/04_qa_and_delivery.md); this module does not redefine them |
| voice_or_ref | The lock: `moss-voice` description string, or `moss-nano-tts` reference clip or preset; never mid-series changes |
| style_note | ≤200 chars; character dialect/delivery steering, a request to the engine that only the test sentence confirms (proper-noun phonetic spellings live separately in `bible/pronunciation.md`; follow `07_qa_and_review.md`) |
| locked_on | Date; after lock, changes are a logged owner decision (dated entry in `bible/voices.md` prose, outside the template) |
| test_sentence_result | The dialect test sentence pass/fail + QA numbers |

Dialect/invented-language steering goes in the style note (e.g. "pronounce like Dutch: doubled vowels long, hard g"). Do not assume the local engine honours it: the test sentence per dialect is generated and archived once per voice, and **the owner listens and picks** — a spoken read cannot be judged from text.

**Consent gate:** a `moss-nano-tts` reference clip of a real person's voice is used only after that person's written consent is on record; no real person is cloned without it. The full rule (where the record is kept, unknown-origin clips, `moss-voice` descriptions) lives in the sibling skill's [`02_tts_budget.md`](../../kirby-local-first-video-pipeline/references/02_tts_budget.md), under Voice locks, and applies here unchanged.

## Generation discipline

- **Pre-production / Pre-TTS & Post-synthesis Gates (follow [`07_qa_and_review.md`](./07_qa_and_review.md)):**
  - Before invoking TTS, draft the text-only `shots.json` pass (`04_shot_list_and_motion.md`) and run [`07_qa_and_review.md`](./07_qa_and_review.md) checkpoint 1: keep `dialogue[*].line`, `dialogue[*].sub`, and `insert` `text` canonical (passing phonetic respelling heuristics via `tts_text` or `-t`/`--text`, keeping `-i`/`--instruction` strictly for voice/tone style).
  - After generating each take, run `bin/audio_qa.py` (`## Audio QA` below) and [`07_qa_and_review.md`](./07_qa_and_review.md) checkpoint 2 (`moss-transcribe` proper-noun + numeric/claim spot-check with human listen-back) before logging `tts_budget.py ... log`.
- **1 take + 1 retake per line.** Local takes are free and unlimited, so the cap is a quality discipline, not a quota. A third attempt means changing the description string, reference clip, or the `tts_text` respelling (never canonical `dialogue[*].line`), not the policy. Log every take via the sibling skill's `bin/tts_budget.py ... log` against project `@tts_ledger` after `bin/audio_qa.py` and the `moss-transcribe` proper-noun check (07 checkpoint 2).
- Draft/scratch timing (mute pass, subtitle estimates) uses the same local engine as the finals (`moss-nano-tts` runs on CPU with zero VRAM, per the sibling skill's dispatcher), so timings carry over.
- Durations: **real audio is the timing source.** After generation, measure every take (`ffprobe`) and set shot lengths and `at` offsets from the measurements — never from word-count estimates (measured on the old Gemini route: invented-dialect reads ran ~2.2 words/s vs the 2.5 estimate, 2026-11-06; re-measure on MOSS).
- STATION/PA/broadcast voices get a radio filter at mix (module 08: `highpass`/`lowpass` + slight `aecho`), and a distinct ledger voice.

## Audio QA (every take)

1. `bin/audio_qa.py` (this skill's bin; the sibling kirby-local-first-video-pipeline ships an equivalent) — per-second RMS windows, ~−38 dB speech threshold; an overall `volumedetect` mean is **not** acceptable (it hides tail-crammed takes; measured lesson, 2026-11-06).
2. Duration within the shot's slot; trim or retime the shot, never speed the voice.
3. Playback rule: audition files in **wav or mpv** — VLC fails to decode some TTS m4a encodings and plays near-silence (root-caused 2026-11-06). Loudness-match audition copies into `wav/` for fair A/B listening.

## Failure ladder

A silent or truncated local take: re-run once and check the per-second RMS before judging the voice. If it repeats, treat it as an engine or setup fault and fix that. There is no cloud fallback: never switch a line to a cloud voice.
