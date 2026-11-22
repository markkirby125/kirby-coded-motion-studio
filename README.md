# kirby-coded-motion-studio

Generalised, local-first channel production engine. Story bible → character sheets with
wardrobe variants → local-TTS voice ledger → locally generated stills → **motion
entirely by code** (no video model, ever) → ffmpeg assembly → independent review →
publish and metrics.

- Routing doctrine and TTS ledger: `../kirby-local-first-video-pipeline`
- Character-sheet SOP: `../kirby-volumetric-character-consistency` (still-image parts only; its turntable video route is excluded by module 02)
- Start at `references/00_dispatcher.md`. Project-specific rules live in each project's
  `CLAUDE.md`/`AGENTS.md` and always override this skill.

Verified on this machine 2026-11-07: MOSS local stills (unlimited), Inkscape/Blender/GIMP
adapters (see module 06), ffmpeg motion vocabulary, and the full review protocol (vision
rubric + mechanical checks). Voice is local MOSS TTS only: cloud TTS left policy on
2026-11-07 and was removed from this skill's voice route (module 03). Stills are local
only too (module 05). The MOSS routes are verified in the sibling skill, not re-verified here.
