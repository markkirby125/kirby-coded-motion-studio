# Module 02: Characters and Wardrobe

Every recurring character gets a sheet set and a wardrobe ledger row before it appears in a shot.

## Character sheet SOP (per character)

Directory `bible/characters/<id>/`:

| File | Content | Engine |
|---|---|---|
| `base.png` | Full body, neutral stance, signature wardrobe, plain dark-grey backdrop | MOSS text-to-image, seed-locked |
| `face.png` | Extreme close-up, collarbone up, neutral expression | MOSS img2img from base (denoise ≈ 0.4) |
| `turnaround.png` | Front / left profile / back, one sheet | MOSS img2img from base |
| `split.png` | base + face side by side (the review/anchor montage) | PIL, derived |
| `prompts.json` | Every prompt + seed + the phase-4 turntable prompt | text |

Rules (measured lessons, 2026-11-07):
- **Neutral expression invariant** in every base/face/turnaround prompt. Expressions bake into the model's notion of the character and corrupt scene takes.
- **No-text clause** in every prompt; negative-prompt the usual (photorealistic, text, watermark, extra fingers).
- **Face-identity policy is a project-layer decision**: some channels hide a character's face (record it as a canon constraint and enforce it in every prompt); others show it. Whatever the policy, it applies to the sheets too. If the policy changes, regenerate the affected sheets — do not patch prompts only.
- Review every sheet at full resolution against its LOOK string before first use (module 07).
- Volumetric turntable videos (`@master_video`) are **deferred**: they need an image-conditioned video route, which this skill's doctrine excludes from scene work. The turntable prompt is saved in `prompts.json` against a future decision to add reference-video conditioning.

## Wardrobe ledger (continuity across time)

Doctrine: **signature wardrobe is permanent**. Within one video, clothing is identical in
every shot. Across videos, only slight variations mark time passing (a different scarf, an
added jacket, sleeves rolled vs down). Special occasions (funeral, ceremony) may change the
outfit fully — logged with a reason so continuity never silently breaks.

Ledger row (template in `assets/wardrobe-ledger.template.json`):

```json
{
  "character": "example",
  "variant": "example-day1",
  "date_added": "2026-11-07",
  "video": "ep01",
  "delta": "signature parka, grey scarf",
  "reason": "baseline",
  "sheet_ref": "bible/characters/example/base.png"
}
```

Rules:
- A variant ID is `<character>-<marker>` (day number, episode, or occasion). One active variant per character per video.
- Shot rows in `@shot_list` carry the variant ID; generation prompts append the variant delta after the LOOK string — the LOOK itself never changes.
- Bumping a variant regenerates only shots that include the character; the base sheet is not redrawn.
- Retired variants stay in the ledger (never deleted) — pixel-consistency's dated-bump pattern.

## Review before use

Sheets are versioned assets: regenerate on constraint violations (face policy, invented traits, style drift), update `prompts.json`, and re-run the module-07 sheet review. Never edit a PNG by hand to fix a canon violation — regenerate (shadow/composite patches are for shot repair, not canon).
