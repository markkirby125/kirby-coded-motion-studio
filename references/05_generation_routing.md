# Module 05: Generation Routing (stills)

Stills are the only generated pixels in this studio, and they are generated locally. The
sibling skill's `@route_table` records the project's instantiation.

## Route

| Route | Engine | Limit (measured 2026-11-07) | Use for |
|---|---|---|---|
| local | MOSS MCP → SwarmUI/ComfyUI on the local GPU (`localhost:7801`) | unlimited, free | Every still |

There is no cloud route and no budget gate: the sibling skill's doctrine is local apps only.
A project whose spec still names a cloud image route must be migrated to the local route
before production.

## Local route operating rules (measured 2026-11-07)

- Endpoint `POST /API/GenerateText2Image` with a fresh `POST /API/GetNewSession` session id per call; payload keys `prompt`, `negativeprompt`, `model`, `width`, `height`, `steps`, `cfgscale`, `seed`, optional `init_image` (data-URI) + `denoise` for img2img.
- **The first call after idle loads the model**: the HTTP call may time out while generation continues. Never blind-retry — poll the reported output path under the SwarmUI Output dir (it appears within ~90 s). An immediate "file not found" on a 200 response is write-lag: poll, don't regenerate.
- Image dims in multiples of 64; 20 steps, cfg 3.5–5.0. Seed-lock per character/asset family so regenerations stay in-family.
- Verify with `ls -lh` (and a vision check at module 07) before reporting done.

## Prompt construction (every still)

```
<style prefix> <LOOK string verbatim>[ <wardrobe variant delta>].
Shot: <size>, <camera>. <action>. [Acting: <acting>.]
[<hard constraint lines: counts, positions, exclusions>]
No on-screen text... <no-text clause>
```

- The **style prefix** is the channel's locked style sentence, identical in every prompt (project layer).
- **LOOK verbatim** (module 01's rule); wardrobe delta from `@wardrobe_ledger`.
- Hard constraints name the failure modes you refuse: bed/prop counts, "exactly two", "open floor gap", "face policy". Learned from measured review rounds: models refill shelves, merge beds, expose hidden arms, and write stray text unless each is explicitly forbidden.
- Negative prompt: photorealistic, 3d render, text/letters/numbers, watermark, extra fingers (+ per-shot additions).
- Never name real people; never put invented traits into prompts without owner approval.

## Retake discipline

- A still retake is free (local): fix by **constraint addition**, not by re-rolling — add the specific prohibition for the observed failure, then regenerate. Two strikes on the same failure → escalate the constraint wording; three → rewrite the prompt structure or repair the frame (module 06 floor). There is no cloud route to escalate to.
- Repair vs regenerate: shadow patches, freeze-masks, punch-in crops and monitor overlays (module 06 floor) may repair an otherwise-good frame; canon violations (face policy, wrong scar side, invented marks) always regenerate.
- Every promotion is a one-line pointer change (`start_frame` / `kept`), reversible; the ledger (`@shot_list`) is the truth.
