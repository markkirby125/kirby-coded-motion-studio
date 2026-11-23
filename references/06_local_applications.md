# Module 06: Local Applications (CLI-Anything)

CLI-Anything adapters are the standard wrapper for local applications. Active escalation ladder
for any local-app task: **adapter → real app CLI → Chromium (HTML→PNG inserts) → PIL/ffmpeg floor** (headless Chromium HTML→PNG inserts are reported in the **Verified behaviour table** below; Playwright WebGPU/GPU 3D spatial capture is an **unverified candidate route — not active; requires a dated verified entry in the Verified behaviour table below before use**).

## Verified behaviour table (tested 2026-11-07 on this machine)

| App | Adapter | Verified | Quirks / rules |
|---|---|---|---|
| Inkscape 1.4.4 | `cli-anything-inkscape` | full round-trip 0.086 s | Needs `-s` (auto-save) in one-shot mode. **First choice for vector/graphic assets.** |
| Blender 5.2.2 | `cli-anything-blender` | script gen 0.09 s; real render ~2 s | Adapter *plans* (writes a bpy script); **real Blender must execute it** (by design). Scene must contain a camera or render errors. |
| GIMP 3.2.6 (Flatpak) | `cli-anything-gimp` | correct output via 60 s Script-Fu wait → automatic Pillow fallback | GIMP 3 requires explicit `--batch-interpreter=plug-in-script-fu-eval` (local patch; upstream issue HKUDS/CLI-Anything#639). The Flatpak build hangs forever on any erroring batch script — so **native batch is not trusted**; the Pillow fallback is the working route. Use GIMP only when GIMP-specific processing is genuinely needed. |
| SwarmUI/ComfyUI | HTTP (module 05) | unlimited stills | model-load lag + write-lag: poll output paths. |
| Headless Chromium (HTML→PNG inserts) | `headless Chromium` (`render.mjs`) | reported deterministic output on 2026-11-07 tests (`<project>/templates/tools/render.mjs`); not re-measured here, so add a dated measured entry before relying on it | Project-local HTML→PNG insert path (`04_shot_list_and_motion.md` & `kirby-local-first-video-pipeline`). |
| ffmpeg + PIL | the floor | everything else | The default raster/composition path; skips GIMP's 60 s penalty entirely. |

### Candidate routes (unverified)

| App | Adapter | Verified | Quirks / rules |
|---|---|---|---|
| Playwright WebGPU / GPU 3D spatial capture | headless script | **not verified locally** | Candidate route only (see **Candidate (unverified) — Playwright GPU / Interactive Map & Spatial Scene Route (Nov 2026)** section below before any use). |

## Operational rules (measured lessons)

1. **Scratch files for long productions live in a project subfolder, never `/tmp`** — a suspend/reboot wipes `/tmp` (measured loss, 2026-11-07). `/tmp` is fine for one-command probes.
2. Adapter stateful projects (`--project <file>.json`) must be created *before* other commands reference them; `project new -o <path>` creates, then pass `--project` on every call.
3. A hung adapter shows near-zero CPU — it is *blocked*, not busy. Time-box every local-app call (`timeout`), and never extend a wait past the time-box twice without a new hypothesis.
4. Generation output "file not found" right after a success response is write-lag — poll (≤90 s) before retrying.
5. Health-check services before batches (SwarmUI: `ListBackends`/status; the sibling skill's tools).
6. Patches to the adapter venv are lost on reinstall — record them in the project layer or upstream them (see upstream issue #639, not verified here).

## The ffmpeg/PIL floor (what "code-only" falls back to)

Everything adapters do has a floor that always works: PIL for masks/montages/crops/unsharp,
ffmpeg for filters, concat, alphamerge overlays, `zoompan` motion, drawtext cards,
`loudnorm`, probes. Proven repair techniques from the 2026-11-06 rounds (keep in the
toolbox): alpha-mask shadow patches over faces/panels, flat-line monitor overlays,
punch-in crop re-frames (≤1.3× upscale), diff-mask freeze patches for churning props,
per-frame compositing passes re-encoded once.

## Candidate (unverified) — Playwright GPU / Interactive Map & Spatial Scene Route (Nov 2026)

* Source: Dossier entry around Video 09 (`ULvVvU0fWj8` — Edward Sturm Ep. 1,224 / Mike Hawley; `../../docs/yt_dossier_nov2026_mapping.md` recommends documenting overnight Playwright local-GPU 3D as a floor option, deliberately demoted here to unverified candidate-only pending local machine verification). Distinct from the HTML→PNG insert path (`04_shot_list_and_motion.md`), local-GPU 3D captures (interactive maps, overhead game-UI-style scenes, and data dashboards) may be rendered as local HTML/Canvas scenes and captured via headless Playwright WebGPU/GPU before ffmpeg assembly **only after recording a dated, measured verification entry in the Verified Behaviour table above (command, GPU/driver, resolution, flags/SwiftShader result)**. Once verified, captured plates enter `shots.json` as single PNG `start_frame` stills or `insert` (`template`/`text`) entries (`shots.json` schema in Module 04 uses `engine: still | insert` with no separate video-clip field).
