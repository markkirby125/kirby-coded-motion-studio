# Module 01: Story and Series Bible

The story gate runs before any asset exists. It is cheap, text-only, and blocking.

## The 16-point story gate (blocking checklist)

Answer every point in one file (`bible/story-check.md`). Any unanswered point blocks generation:

1. Premise in one sentence (never the outcome).
2. Protagonist, antagonist force, and what each wants.
3. The grey dilemma — both options cost something real; no obvious right answer.
4. The compromise path taken, and its aftermath (gets screen time).
5. What is revealed, and what stays hidden.
6. Ending lands on a **choice**, not only a twist.
7. Episode/series structure: episode count, runtime band per version (Short 60–75 s; long-form per channel norm).
8. Clock or countdown that advances every episode.
9. Consequence rule: what happens in one series is mentioned in the next.
10. Speaker cap and line cap (defaults: ≤3 speaking characters per series, ≤2 lines per shot, ≤10 words per line — the project layer may retune).
11. Exposition route: intercom/screen/note, never a talking-head explain.
12. Tone lock: three adjectives the visuals must obey.
13. Style lock: the generation style prefix, copied verbatim into every prompt (see module 05).
14. Continuity file created (`bible/continuity.md`): who knows what, deaths, clocks, faces met.
15. Originality pass (sibling skill `kirby-yt-faceless-formula` module 04 if this is a formula-derived channel).
16. Owner sign-off on the story before the bible is built.

## Bible files

| File | Contents |
|---|---|
| `bible/world.md` | Setting, factions, rules, decided-by-owner rows |
| `bible/cast.md` | One row per character: age, role, personality, **LOOK string** (the only appearance canon) |
| `bible/continuity.md` | Current state; updated after every episode (address terms, secrets, clocks, faces met) |
| `bible/language.md` | Dialogue language rules (invented language, subtitles, on-screen text policy) |
| `bible/voices.md` | The `@voice_ledger` (module 03) |
| `bible/pronunciation.md` | Documented respelling heuristics for spoken proper nouns (pre-TTS; post-synthesis flagged by `moss-transcribe`, confirmed by human listen-back per `07_qa_and_review.md`) |
| `bible/claims.md` | Primary source notes backing verifiable stats and factual claims (excluding common knowledge and diegetic fictional dialogue) across spoken dialogue, `sub`, and insert `text` (`shots.json`), populated during story/script drafting before TTS |

**LOOK strings are canon.** A LOOK is `NAME, age: appearance description`. Prompts use it
verbatim; traits not in a LOOK are never invented into one without the owner's approval
(measured lesson, 2026-11-07: invented eye-colours and skin tones in sheet prompts caused a
review hold and a regeneration).

## Series continuity

Every episode ends with a Stage-10 log line appended to `continuity.md` (date, deaths,
secrets revealed, clock values). The next episode's Previously/opens read from that file,
never from memory. Sessions resume from the project's handoff/TASKS files — never re-derive
state from scratch.

## Pre-production / Pre-TTS & Post-synthesis Gates Pointer (Nov 2026)

* Factual claims (verifiable stats and claims, excluding common knowledge and diegetic fictional dialogue) across canonical spoken `dialogue[*].line` and displayed `dialogue[*].sub` / `insert` `text` (`shots.json`) must match primary sources recorded in `bible/claims.md` (populated at story/script stage), and all spoken proper nouns must have verified phonetic respellings in `bible/pronunciation.md` (flagged post-synthesis by `moss-transcribe` and confirmed only by human listen-back, using `tts_text` overrides or `-t`/`--text` CLI input rather than mutating canonical `dialogue[*].line`), enforced by the **Pre-production / Pre-TTS Gate** and **Post-synthesis proper-noun check** in [`07_qa_and_review.md`](./07_qa_and_review.md) (backed by sibling [`kirby-local-first-video-pipeline`](../../kirby-local-first-video-pipeline/SKILL.md) [`04_qa_and_delivery.md`](../../kirby-local-first-video-pipeline/SKILL.md)). For optional separate web-visualizer routing outside the video pipeline, see [`kirby-gemini-interactive-study-pages`](../../kirby-gemini-interactive-study-pages/SKILL.md) (listed in [`00_dispatcher.md`](./00_dispatcher.md); pending submodule registration in `.gitmodules`).
