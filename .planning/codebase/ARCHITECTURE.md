---
title: Architecture
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

<!-- refreshed: 2026-05-27 -->
# Architecture

**Analysis Date:** 2026-05-27

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 Codex Skill Package Layer                   │
├─────────────────────┬───────────────────┬───────────────────┤
│ Skill instructions  │ Agent metadata     │ Bundled scripts   │
│ `skills/zk-creative-process/SKILL.md`                       │
│ `skills/zk-creative-process/agents/openai.yaml`             │
│ `skills/zk-creative-process/scripts/*.ps1`                  │
└──────────┬──────────┴─────────┬─────────┴─────────┬─────────┘
           │                    │                   │
           ▼                    ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Repository Development Script Layer             │
│                    `scripts/*.ps1`                           │
│ Root copies mirror bundled script behavior for development,  │
│ installer entry points, environment checks, and tests.        │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                Generated Creative Material Output            │
│ `creative-materials/YYYY-MM-DD-slug-name/`                   │
│ Human markdown, copied videos, keyframe sheets, system JSON, │
│ and AI review packs. This output is ignored by git.          │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Skill contract | Defines trigger terms, single/mix routing, hard rules, output requirements, and completion checks for Codex usage. | `skills/zk-creative-process/SKILL.md` |
| Agent metadata | Provides display name, short description, and default prompt for the skill UI. | `skills/zk-creative-process/agents/openai.yaml` |
| Installer | Copies the self-contained skill into the user's `.codex\skills\zk-creative-process` folder and handles `-Backup`/`-Force`. | `scripts/install-skill.ps1` and `skills/zk-creative-process/scripts/install-skill.ps1` |
| Environment check | Verifies PowerShell, FFmpeg/FFprobe availability, and UTF-8 filesystem write/read support. | `scripts/check-environment.ps1` and `skills/zk-creative-process/scripts/check-environment.ps1` |
| Single wrapper | Runs material setup for one video, validates generated output, and returns JSON for the next AI step. | `scripts/process-reference-video-phase1.ps1` and `skills/zk-creative-process/scripts/process-reference-video-phase1.ps1` |
| Single material generator | Creates the single-video material folder, copies/moves video, probes metadata, extracts frames, writes skeleton markdown, and writes system review files. | `scripts/start-reference-video.ps1` and `skills/zk-creative-process/scripts/start-reference-video.ps1` |
| Mix material generator | Creates one direction-level folder for multiple same-direction videos, copies/moves all videos, writes per-video contact sheets, and writes shared analysis skeletons. | `scripts/process-reference-videos-mix.ps1` and `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1` |
| Material validator | Checks required root files, system files, contact sheets, source videos, outputs, and TODO placeholders. | `scripts/check-creative-material.ps1` and `skills/zk-creative-process/scripts/check-creative-material.ps1` |
| Installation smoke test | Generates or finds a sample video, runs the single workflow, validates output, and cleans `.tmp` unless `-KeepOutput` is passed. | `scripts/test-install.ps1` and `skills/zk-creative-process/scripts/test-install.ps1` |
| User documentation | Keeps entry usage in the README and extended explanations in docs. | `README.md`, `docs/creative-process-guide.md`, `docs/example-folder-structure.md`, `docs/troubleshooting.md` |

## Pattern Overview

**Overall:** Self-contained Codex skill package with mirrored repository scripts and generated-file pipeline.

**Key Characteristics:**
- Treat `skills/zk-creative-process/` as the installable artifact; it must include `SKILL.md`, `agents/openai.yaml`, and `scripts/*.ps1`.
- Keep `scripts/*.ps1` as root-level development and installer entry points; current root scripts are byte-identical to `skills/zk-creative-process/scripts/*.ps1`.
- Separate deterministic processing from AI judgment: scripts create folders, copied videos, metadata, keyframes, manifests, and skeleton markdown; Codex fills creative analysis afterward.
- Default source handling is copy. Moving originals requires explicit `-Move` in `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
- Generated work belongs under `creative-materials/` and `.tmp/`; both are ignored by `.gitignore`.

## Layers

**Skill Instruction Layer:**
- Purpose: Route user intent to `single` or `mix`, define hard rules, and describe AI output obligations.
- Location: `skills/zk-creative-process/SKILL.md`
- Contains: YAML frontmatter, command modes, routing rules, hard rules, workflows, product mapping requirements, completion checks.
- Depends on: Bundled scripts in `skills/zk-creative-process/scripts/`.
- Used by: Codex sessions invoking `$zk-creative-process`, `single`, or `mix`.

**Skill Metadata Layer:**
- Purpose: Expose skill display metadata and default prompt text.
- Location: `skills/zk-creative-process/agents/openai.yaml`
- Contains: `interface.display_name`, `interface.short_description`, `interface.default_prompt`.
- Depends on: Skill naming in `skills/zk-creative-process/SKILL.md`.
- Used by: Codex skill UI and agent metadata readers.

**Repository Script Layer:**
- Purpose: Provide development-time copies of bundled scripts and the primary installer entry point from the repository root.
- Location: `scripts/`
- Contains: PowerShell scripts for install, environment check, FFmpeg install, material generation, validation, and smoke testing.
- Depends on: PowerShell runtime, FFmpeg, FFprobe, filesystem access.
- Used by: Users running `.\scripts\install-skill.ps1`, maintainers testing scripts, and documentation examples in `README.md`.

**Bundled Script Layer:**
- Purpose: Make the installed skill self-contained after `skills/zk-creative-process/` is copied to `.codex\skills`.
- Location: `skills/zk-creative-process/scripts/`
- Contains: The same script set as `scripts/`.
- Depends on: Relative paths inside the installed skill folder.
- Used by: Codex when executing the installed skill's own scripts.

**Generated Material Layer:**
- Purpose: Store creative processing results and AI handoff artifacts.
- Location: `creative-materials/YYYY-MM-DD-slug-name/`
- Contains: Copied or moved videos, keyframe contact sheets, `brief.md`, `product-brief-产品信息.md`, `outputs/`, and `_system-review-系统复查资料/`.
- Depends on: Script output from `scripts/start-reference-video.ps1` or `scripts/process-reference-videos-mix.ps1`.
- Used by: Codex analysis and human creative review.

**Documentation Layer:**
- Purpose: Explain entry workflow, troubleshooting, and expected generated folder structures.
- Location: `README.md`, `docs/`, `examples/`
- Contains: Install and usage guide, detailed process guide, folder structure examples, troubleshooting notes, lightweight examples.
- Depends on: Current script parameters and generated output names.
- Used by: Non-programmer users and maintainers.

## Data Flow

### Single Reference Video Path

1. User invokes `$zk-creative-process single` or runs `.\scripts\process-reference-video-phase1.ps1` with `-VideoPath`, `-Slug`, and `-Name` (`scripts/process-reference-video-phase1.ps1:1`).
2. Wrapper resolves sibling scripts and calls `scripts/start-reference-video.ps1` with the provided arguments (`scripts/process-reference-video-phase1.ps1:35`).
3. `scripts/start-reference-video.ps1` validates filename-safe `Name`, resolves `ffmpeg` and `ffprobe`, creates `creative-materials/YYYY-MM-DD-slug-name/`, and copies the video by default (`scripts/start-reference-video.ps1:34`, `scripts/start-reference-video.ps1:53`, `scripts/start-reference-video.ps1:163`).
4. The script writes or copies `product-brief-产品信息.md`, probes video metadata, extracts selected frames, creates a contact sheet, and writes `frame-index.json` plus `video_metadata.json` (`scripts/start-reference-video.ps1:173`, `scripts/start-reference-video.ps1:220`, `scripts/start-reference-video.ps1:331`).
5. The script creates human-facing markdown skeletons in the material root and `outputs/`, then writes `_system-review-系统复查资料/ai-input-pack.md` and `run-manifest.json` (`scripts/start-reference-video.ps1:345`, `scripts/start-reference-video.ps1:369`, `scripts/start-reference-video.ps1:450`, `scripts/start-reference-video.ps1:483`).
6. The wrapper runs `scripts/check-creative-material.ps1 -Json`, returns a JSON payload with paths and validation status, and exits with the validator status (`scripts/process-reference-video-phase1.ps1:60`, `scripts/process-reference-video-phase1.ps1:65`, `scripts/process-reference-video-phase1.ps1:88`).

### Mix Reference Video Path

1. User invokes `$zk-creative-process mix` or runs `.\scripts\process-reference-videos-mix.ps1` with two or more video paths (`scripts/process-reference-videos-mix.ps1:1`, `scripts/process-reference-videos-mix.ps1:32`).
2. The script validates `-Copy`/`-Move`, `StoryboardFrames`, and filename-safe `Name`, then resolves `ffmpeg` and `ffprobe` (`scripts/process-reference-videos-mix.ps1:35`, `scripts/process-reference-videos-mix.ps1:39`, `scripts/process-reference-videos-mix.ps1:45`).
3. It creates one shared direction-level material folder, `outputs/`, `_system-review-系统复查资料/`, and temporary `keyframes-work/` (`scripts/process-reference-videos-mix.ps1:67`).
4. Each source video is copied by default or moved only with `-Move`; each video gets metadata, selected frames, and a per-video contact sheet in the material root (`scripts/process-reference-videos-mix.ps1:136`, `scripts/process-reference-videos-mix.ps1:143`, `scripts/process-reference-videos-mix.ps1:168`).
5. The script writes shared `video_metadata.json`, shared `frame-index.json`, `brief.md`, `outputs/shared-analysis-同方向素材共性拆解.md`, `ai-input-pack.md`, and `run-manifest.json` (`scripts/process-reference-videos-mix.ps1:205`, `scripts/process-reference-videos-mix.ps1:212`, `scripts/process-reference-videos-mix.ps1:214`, `scripts/process-reference-videos-mix.ps1:240`, `scripts/process-reference-videos-mix.ps1:265`, `scripts/process-reference-videos-mix.ps1:285`).
6. Temporary frame work is removed unless `-KeepWork` is used, with a path containment check before deletion (`scripts/process-reference-videos-mix.ps1:298`, `scripts/process-reference-videos-mix.ps1:303`).

### Installation Path

1. User runs `.\scripts\install-skill.ps1` from the repository root (`README.md`).
2. The installer detects whether it is running inside a self-contained skill folder or from the repository root (`scripts/install-skill.ps1:10`).
3. The source defaults to `skills\zk-creative-process` when running from the repository root (`scripts/install-skill.ps1:13`).
4. Destination defaults to `$HOME\.codex\skills\zk-creative-process` unless `-CodexSkillsDir` is passed (`scripts/install-skill.ps1:26`).
5. Existing installs stop unless `-Backup` or `-Force` is explicitly provided (`scripts/install-skill.ps1:50`).
6. The installer recursively copies the skill folder and ensures `scripts/` exists inside the destination (`scripts/install-skill.ps1:63`).

**State Management:**
- No long-lived application state exists. Scripts are process-local and write state to generated files under material folders.
- Generated state files are `_system-review-系统复查资料/video_metadata.json`, `_system-review-系统复查资料/frame-index.json`, `_system-review-系统复查资料/run-manifest.json`, and `_system-review-系统复查资料/ai-input-pack.md`.
- Human-editable state lives in `brief.md`, `product-brief-产品信息.md`, and `outputs/*.md`.

## Key Abstractions

**Skill Package:**
- Purpose: The copyable unit installed into Codex.
- Examples: `skills/zk-creative-process/SKILL.md`, `skills/zk-creative-process/agents/openai.yaml`, `skills/zk-creative-process/scripts/install-skill.ps1`
- Pattern: Self-contained folder with instructions, metadata, and bundled scripts.

**Material Folder:**
- Purpose: One creative-processing workspace for either one reference video or one same-direction batch.
- Examples: `creative-materials/YYYY-MM-DD-slug-name/brief.md`, `creative-materials/YYYY-MM-DD-slug-name/outputs/`, `creative-materials/YYYY-MM-DD-slug-name/_system-review-系统复查资料/`
- Pattern: Human root files plus machine-review subfolder.

**System Review Pack:**
- Purpose: Preserve deterministic inputs for AI review, reproducibility, and validation.
- Examples: `_system-review-系统复查资料/ai-input-pack.md`, `_system-review-系统复查资料/frame-index.json`, `_system-review-系统复查资料/run-manifest.json`, `_system-review-系统复查资料/video_metadata.json`
- Pattern: Generated metadata and paths, never primary human-facing analysis.

**Product Brief:**
- Purpose: Separates reference-video deconstruction from product-specific mapping.
- Examples: `product-brief-产品信息.md` generated by `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`
- Pattern: Template or copied user-provided markdown; if incomplete, product mapping stays pending.

**Validation Result:**
- Purpose: Standardizes material folder checks for required files and placeholder warnings.
- Examples: JSON from `scripts/check-creative-material.ps1 -Json`, wrapper fields in `scripts/process-reference-video-phase1.ps1`
- Pattern: Ordered JSON with `status`, `errors`, `warnings`, and `issues`.

## Entry Points

**Skill Invocation:**
- Location: `skills/zk-creative-process/SKILL.md`
- Triggers: `$zk-creative-process`, `single`, `mix`, reference video processing, game-ad hook analysis, story-direction pools.
- Responsibilities: Choose mode, run script setup before AI writing, preserve copy-by-default semantics, and enforce product-mapping boundaries.

**Repository Install Command:**
- Location: `scripts/install-skill.ps1`
- Triggers: Manual install from repository root.
- Responsibilities: Copy `skills/zk-creative-process/` to Codex skills directory without silently overwriting existing installs.

**Environment Check Command:**
- Location: `scripts/check-environment.ps1`
- Triggers: Manual preflight and troubleshooting.
- Responsibilities: Detect PowerShell version, `ffmpeg`, `ffprobe`, and UTF-8 filesystem support.

**Single Processing Command:**
- Location: `scripts/process-reference-video-phase1.ps1`
- Triggers: Single-video creative processing.
- Responsibilities: Call material generator, validate output, return AI handoff JSON.

**Low-Level Single Generator:**
- Location: `scripts/start-reference-video.ps1`
- Triggers: Called by `scripts/process-reference-video-phase1.ps1` or directly by advanced users.
- Responsibilities: Generate single-video folders and all deterministic artifacts.

**Mix Processing Command:**
- Location: `scripts/process-reference-videos-mix.ps1`
- Triggers: Same-direction batch processing.
- Responsibilities: Generate one shared folder for multiple videos and one shared analysis skeleton.

**Material Check Command:**
- Location: `scripts/check-creative-material.ps1`
- Triggers: Manual validation, wrapper validation, smoke test validation.
- Responsibilities: Verify material folder completeness and report placeholder TODO warnings.

**Smoke Test Command:**
- Location: `scripts/test-install.ps1`
- Triggers: Maintainer validation after script changes.
- Responsibilities: Generate or reuse a sample video, run the single workflow, validate output, and clean `.tmp`.

## Architectural Constraints

- **Threading:** Single-process PowerShell execution. FFmpeg/FFprobe are invoked as child processes; no background workers or concurrent job orchestration are present.
- **Global state:** No persistent global application state. Environment variables are read only indirectly through `$env:USERPROFILE` and `$HOME` in `scripts/install-skill.ps1`.
- **Circular imports:** Not applicable. Scripts invoke sibling scripts by path rather than module importing.
- **Script duplication:** Root `scripts/*.ps1` and bundled `skills/zk-creative-process/scripts/*.ps1` are intentionally mirrored. Keep them synchronized when changing script behavior.
- **Generated files:** `creative-materials/`, `.tmp/`, video files, and `keyframes-work/` are ignored by `.gitignore`; do not add generated user materials to git.
- **No silent destructive behavior:** Existing skill installs require `-Backup` or `-Force`; original videos are copied unless `-Move` is explicit; temporary deletion is guarded by path containment checks.
- **Encoding:** Generated markdown uses UTF-8 and includes Chinese filenames such as `product-brief-产品信息.md` and `_system-review-系统复查资料/`.

## Anti-Patterns

### Editing Only One Script Copy

**What happens:** A change is made in `scripts/start-reference-video.ps1` but not in `skills/zk-creative-process/scripts/start-reference-video.ps1`.
**Why it's wrong:** Installed skill users execute the bundled copy, while repository tests and README examples may execute the root copy.
**Do this instead:** Apply behavior changes to both `scripts/*.ps1` and `skills/zk-creative-process/scripts/*.ps1`, then compare them with `cmp` or equivalent.

### Writing AI Analysis Before Script Setup

**What happens:** Codex writes `outputs/*.md` before running `scripts/process-reference-video-phase1.ps1` or `scripts/process-reference-videos-mix.ps1`.
**Why it's wrong:** Required metadata, frame index, keyframe sheets, and material folders do not exist yet.
**Do this instead:** Run the deterministic setup first, then read `_system-review-系统复查资料/ai-input-pack.md`, `frame-index.json`, `video_metadata.json`, contact sheets, and `product-brief-产品信息.md`.

### Inventing Product Mapping Details

**What happens:** AI fills product-specific mapping while `product-brief-产品信息.md` still contains TODO or lacks product facts.
**Why it's wrong:** The skill contract explicitly separates reference analysis from product mapping and forbids invented product facts.
**Do this instead:** Keep reference-video deconstruction useful, list missing product questions, and mark product mapping pending in `outputs/creative-script-directions-创意脚本方向.md` or `outputs/shared-analysis-同方向素材共性拆解.md`.

### Creating Production Assets Too Early

**What happens:** A production storyboard, prompt folder, or `script-*` folder is created during first-stage processing.
**Why it's wrong:** The first stage must produce a story-direction pool only; production starts after a human selects a direction.
**Do this instead:** Fill only `brief.md`, `product-brief-产品信息.md`, and files under `outputs/` during the first stage.

## Error Handling

**Strategy:** Fail fast with PowerShell `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`, then return structured JSON where wrappers or validators need machine-readable output.

**Patterns:**
- Validate required command parameters with `param(...)`, `[Parameter(Mandatory = $true)]`, and `[ValidatePattern(...)]` in scripts such as `scripts/start-reference-video.ps1`.
- Throw explicit errors for missing files, missing executables, invalid copy/move combinations, out-of-range frame counts, and pre-existing material folders.
- Capture FFmpeg output into log files and throw log paths on non-zero exit in `Invoke-Logged`.
- Use `exit 1` for failed validation in `scripts/check-creative-material.ps1` and environment checks in `scripts/check-environment.ps1`.
- Guard cleanup with path containment checks before deleting temporary work directories in `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, and `scripts/test-install.ps1`.

## Cross-Cutting Concerns

**Logging:** FFmpeg/FFprobe processing logs are written to `keyframes-work/*.log` during generation. Human-facing progress is printed as plain strings or returned JSON, depending on the entry point.

**Validation:** Material validation lives in `scripts/check-creative-material.ps1`. Environment validation lives in `scripts/check-environment.ps1`. Skill metadata validation is documented in `README.md` through Codex `quick_validate.py`.

**Authentication:** Not applicable. The repository has no authentication layer or external API credentials.

**Privacy:** `.gitignore` excludes generated materials and common video formats. Keep private videos, ad data, filled product briefs, generated `creative-materials/`, and strategy notes out of git.

---

*Architecture analysis: 2026-05-27*
