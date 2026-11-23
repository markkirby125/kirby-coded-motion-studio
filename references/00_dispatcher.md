# Dispatcher: Coded-Motion Studio

Generalised, local-first production engine for narration-led YouTube video. One doctrine:
**every frame is either locally generated (stills), rendered by code (inserts, motion), or mixed by code (audio) — no generative video model is ever used.** Voice is local-only (cloud TTS left this pipeline's policy on 2026-11-07); stills are local too, so there are **no cloud routes inside this pipeline** and no budget gate. (Optional separate cloud web visualizers live outside this pipeline in `kirby-gemini-interactive-study-pages` — see Related Skills.)

This skill is **generalised**. It never hardcodes channel canon. Every project carries a
**project layer** — a "local-first production rules" section in its `CLAUDE.md`/`AGENTS.md`
(bible paths, language rules, cast constraints, credit conventions, insert templates).
**Read the project layer first; it overrides this skill wherever they differ.**

Sibling skill: `kirby-local-first-video-pipeline` owns the route-table/TTS-ledger doctrine and
the `@route_table`/`@tts_ledger` templates. This skill consumes them; it does not duplicate them.

## 🏷️ Canonical Asset Tag Register

| Asset Variable | Data Type | Role |
|---|---|---|
| `@project_layer` | Rules (per project) | The production-rules section of the project's CLAUDE.md/AGENTS.md. Read first, wins on conflict. |
| `@bible` | Docs (per project) | Story canon: world, cast (LOOK strings), continuity, language, claims (`claims.md`), and pronunciation (`pronunciation.md`) rules. |
| `@char_sheet` | Images (per character) | base / face / turnaround sheets; the look anchor for every generation. |
| `@wardrobe_ledger` | Data (committed) | One row per dated wardrobe variant per character. Template in `assets/wardrobe-ledger.template.json`. |
| `@voice_ledger` | Data (committed) | character → local engine/voice/style-note, locked per series. Template in `assets/voice-ledger.template.json`. |
| `@shot_list` | Data (`shots.json`) | One row per shot: `id`, `engine` (`still \| insert`), size, camera, action, wardrobe variant, canonical `dialogue` (`sub`) + optional `tts_text` override + `at`, `insert` `text`/`template`, motion spec. Template in `assets/shots.template.json`. |
| `@motion_spec` | Rule | The coded move applied to a still (push/pan/parallax/shake/drift/hold), with parameters. Vocabulary in module 04. |
| `@qa_gates` | Checklist | Contact-sheet vision gate on every asset; **Pre-production / Pre-TTS Gate & Post-synthesis proper-noun check** (`bible/claims.md` for stats & factual display text; `bible/pronunciation.md` for spoken proper nouns per `07_qa_and_review.md`); per-second RMS on every audio take; assembly checks on every export. |

## 🧭 Operational Routing Matrix

| Phase | Module | Output |
|---|---|---|
| Story and bible | `01_story_and_series_bible.md` | Approved story, series bible, continuity file, initial `bible/claims.md` |
| Characters and wardrobe | `02_characters_and_wardrobe.md` | `@char_sheet` set + `@wardrobe_ledger` |
| Shots text pass (before audio) | `04_shot_list_and_motion.md` | Drafted text-only `shots.json` (`id`, `engine`, `template`, canonical `dialogue[*].line` / `sub`, `insert` `text`) |
| Voice | `03_voice.md` | `@voice_ledger` + pre-TTS / post-TTS checks (`07_qa_and_review.md`) + generated lines + real timings |
| Shots timing & motion | `04_shot_list_and_motion.md` | Stills + timed `@shot_list` (`seconds` / `at`) + coded-motion parts + inserts |
| Generation routing | `05_generation_routing.md` | Stills via the local MOSS route (no cloud) |
| Local applications | `06_local_applications.md` | CLI-Anything adapter use, verified behaviours, escalation ladder |
| QA and review | `07_qa_and_review.md` | Pre-mix Pronunciation & Claim Ledger re-check (`bible/claims.md` & `bible/pronunciation.md`) + independent vision/code review verdicts |
| Publish and metrics | `08_publish_and_metrics.md` | Upload pack at −14 LUFS, metrics log, go/no-go |

## 🛑 When NOT to Use This Skill

* A one-off single still or poster — generate directly (MOSS) and skip the pipeline.
* A project that genuinely needs photoreal motion video — generative video models are out of policy here and in the sibling skill, so this is the wrong tool.
* The project layer says the channel runs a different pipeline — the project layer wins.

## 🔗 Related Skills in the Kirby Ecosystem

* `../../kirby-local-first-video-pipeline/SKILL.md` — route table, TTS ledger, audio QA bin. This skill's fallback spine.
* `../../kirby-volumetric-character-consistency/SKILL.md` — borrow the sheet structure only (base, face, turnaround, split; wardrobe is a ledger, not a sheet part); module 02's local MOSS engines are authoritative; the sibling's cloud still-image tooling and video route are out of policy.
* `../../kirby-pixel-character-consistency/SKILL.md` — deterministic-renderer character sheets and dated version bumps (the wardrobe ledger's pattern).
* `../../kirby-yt-faceless-formula/SKILL.md` — channel decoding and packaging; runs before this skill when a new channel is being designed.
* `../../kirby-ai-design-system/SKILL.md` — thumbnail station (never blocks production).
* `../../kirby-gemini-interactive-study-pages/SKILL.md` — standalone interactive HTML educational visualizers and click-to-reveal study pages (`risk: unverified`) when learner exploration beats linear rendered video — optional separate cloud web deliverable outside this local-first video pipeline (never used for video/TTS assets; registered as a submodule in `.gitmodules`).
