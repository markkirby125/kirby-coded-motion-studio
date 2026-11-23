# Module 07: QA and Independent Review

Nothing ships on the author's say-so. Every asset, every code change, every cut gets an
**independent** check: a reviewer that is not the author (a fresh subagent/session with no
shared state), mechanical evidence over impressions, and a recorded verdict.

## Vision QA (frames and clips)

1. **Contact sheets**: every animated part → an 8-frame tile sheet; stills → the frame itself. Build with `bin/contact_sheet.py`.
2. **Named-pattern rubric** — flag only genuine artifacts, each with its name:
   `MERGE/GEOMETRY` (objects fused/overlapping), `COUNT` (vs the spec), `PHYSICS/MOTION`
   (morphing, churning, impossible cloth), `ANATOMY` (fingers, limbs), `SPEC VIOLATION`
   (contradicts its own shot row), `GARBLED TEXT` (smeared writing). The locked style
   (grain, uneven ink, stylised faces) is never a finding.
3. Severity ladder: blocker / major / minor / nit. Blockers and majors are re-verified at
   full resolution with evidence crops before any action.
4. Report format: one line per shot (`<id>: SIGN-OFF` or `FINDING [severity] <pattern> — <sentence>`), then a batch verdict `SIGN-OFF (n/n)` or `HOLD (n/n) — <reason>`.
5. Findings become **constraint additions** in the retake prompt (module 05), not vibes.

## Mechanical checks (always, before eyes)

- Frame hashes: join frame at index N must equal part frame 0 (raw rgb24 md5) at every part boundary — proves starts and ordering.
- `ffprobe -count_frames` on every join; duration vs `seconds` sums within 0.05 s/part.
- `bin/assembly_check.py` on exports (durations, bands, stream counts).
- Audio QA per module 03 (per-second RMS) and loudness verify (`ebur128` target −14 LUFS, ≤ −1.0 dBTP).

## Independent review protocol

- **Reviewer ≠ author**, always. Code review: parallel read-only reviewers with distinct lenses (correctness, edge cases, project-rule compliance). Vision: fresh reviewer subagents with the rubric above and each shot's spec inline.
- The reviewer gets acceptance conditions and reports pass / fail / unavailable / blocked — verify-and-stop style. Don't ask for opinions; ask for evidence against conditions.
- Fidelity tiers for motion (when comparing against an intended move): motion-faithful ±80 ms; pixel-faithful ≤2% frame mismatch (starting thresholds, not measured; the project layer may retune); evidence sheets side-by-side.
- Verdicts are recorded in the project's review doc with accepted residuals listed — "signed off with nits" is a valid, final state.
- Review-of-reviews: work done under delegation gets one closing independent pass before install/publish.

## Canon checks (channel-level)

Face policy, scar/side/attribute rules, wardrobe variant match, faces-met table — checked
per shot by the reviewer against the project layer, not just visual slop.

## Pre-production / Pre-TTS & Post-synthesis Gates (Canonical Studio Checkpoints)

* Authoritative sibling gate sections: [`kirby-local-first-video-pipeline`](../../kirby-local-first-video-pipeline/SKILL.md) (`Pre-production / Pre-TTS Gate` & `Post-synthesis / pre-accept moss-transcribe proper-noun check` in [`04_qa_and_delivery.md`](../../kirby-local-first-video-pipeline/references/04_qa_and_delivery.md), and ledger logging in [`02_tts_budget.md`](../../kirby-local-first-video-pipeline/references/02_tts_budget.md)).
* Studio enforcement checkpoints:
  1. **Pre-synthesis (on text-only `shots.json` drafted before voice synthesis):** Every respelling needs an `approved_by` (a human or named independent reviewer) before any TTS call; if none is available, put `PENDING` in `approved_by`, stop TTS synthesis for the affected lines, and report to the operator, per the **Pre-production / Pre-TTS Gate** in [`04_qa_and_delivery.md`](../../kirby-local-first-video-pipeline/references/04_qa_and_delivery.md). Confirm the voice-clone consent record (`03_voice.md`) before any `-r` clip of a real or unknown-origin voice is used. Log documented respelling heuristics for proper nouns in `bible/pronunciation.md` (flagged by `moss-transcribe`, confirmed only by human listen-back; distinct from the ≤200-char character dialect/delivery style note in `bible/voices.md`). Keep `dialogue[*].line`, `dialogue[*].sub`, and `insert` `text` canonical (put phonetic respellings only in optional `tts_text` or `-t`/`--text` input — keeping `-i`/`--instruction` strictly for voice/tone style and never using raw IPA). Verify all verifiable stats and factual claims (excluding common knowledge and diegetic fictional dialogue) across canonical `dialogue[*].line`, `dialogue[*].sub`, and `insert` `text` against primary sources recorded in `bible/claims.md` (ungrounded AI-generated summaries are not valid primary sources). Unverified stats/claims or missing phonetic entries block TTS synthesis and final assembly **for the affected lines** (verified lines may proceed; reduces ungrounded AI-podcast hallucination and mispronunciation risk — residual misreads are caught by checkpoint 2; directional, single-source anecdote from Edward Sturm Ep. 1,233 `eEQP8D3R7i4`).
  2. **Post-synthesis / pre-accept:** run `bin/audio_qa.py`, then verify rendered proper nouns and spot-check spoken numbers/factual claims with `moss-transcribe` (comparing spoken stats/numbers against `bible/claims.md`; escalating ASR ambiguity to human listen-back; a human-confirmed misread or spoken-claim mismatch rejects the take and triggers a retake or `tts_text`/input correction) before logging every take (pass or fail) via the sibling skill's `bin/tts_budget.py ... log` against project `@tts_ledger` (`tts-ledger.json`) with `result` and `rms_qa` recorded (refuses cloud engines; per [`04_qa_and_delivery.md`](../../kirby-local-first-video-pipeline/references/04_qa_and_delivery.md) and [`02_tts_budget.md`](../../kirby-local-first-video-pipeline/references/02_tts_budget.md)).
  3. **Pre-mix / pre-lock:** re-check that canonical `dialogue[*].line` / `dialogue[*].sub` / `insert` `text` in final `shots.json` match `bible/claims.md`, and spoken proper nouns match `bible/pronunciation.md`, before mixing audio or locking final renders.
