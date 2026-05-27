---
title: Technology Stack
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

# Technology Stack

**Analysis Date:** 2026-05-27

## Languages

**Primary:**
- PowerShell 5.1+ / 7+ recommended - all executable automation lives in `scripts/*.ps1` and duplicated installable copies live in `skills/zk-creative-process/scripts/*.ps1`.

**Secondary:**
- Markdown - user-facing docs, generated task skeletons, product briefs, and skill instructions in `README.md`, `docs/*.md`, `examples/*/README.md`, and `skills/zk-creative-process/SKILL.md`.
- YAML - Codex-facing interface metadata in `skills/zk-creative-process/agents/openai.yaml`.
- JSON - generated runtime artifacts such as `_system-review-系统复查资料/video_metadata.json`, `_system-review-系统复查资料/frame-index.json`, and `_system-review-系统复查资料/run-manifest.json` created by `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
- Python - not part of this repository, but README validation examples call Codex's external skill validator at `$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py` from `README.md`.

## Runtime

**Environment:**
- PowerShell is the script runtime. `scripts/check-environment.ps1` accepts PowerShell 5.1+ and recommends PowerShell 7+.
- Local shell execution is required. Scripts call native executables with `Get-Command`, `Resolve-Path`, `Copy-Item`, `Move-Item`, `Set-Content`, and external `ffmpeg` / `ffprobe`.
- Cross-platform support is explicit in `scripts/install-ffmpeg.ps1`: Windows uses `winget`, macOS uses `brew`, and Linux prints package-manager commands.

**Package Manager:**
- No application package manager manifest detected: no `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, or `go.mod`.
- PowerShell modules are not vendored. Scripts rely on built-in PowerShell cmdlets.
- System package managers are optional helpers for FFmpeg installation:
  - Windows: `winget install --id Gyan.FFmpeg -e` in `scripts/install-ffmpeg.ps1`.
  - macOS: `brew install ffmpeg` in `scripts/install-ffmpeg.ps1`.
  - Linux: `sudo apt install ffmpeg`, `sudo dnf install ffmpeg`, or `sudo pacman -S ffmpeg` suggested by `scripts/install-ffmpeg.ps1`.
- Lockfile: missing / not applicable.

## Frameworks

**Core:**
- Codex Skill package format - `skills/zk-creative-process/SKILL.md` defines the skill metadata, routing, hard rules, command modes, workflows, and completion checks.
- PowerShell script toolkit - `scripts/process-reference-video-phase1.ps1` orchestrates single-video setup and validation; `scripts/process-reference-videos-mix.ps1` handles same-direction multi-video batches.

**Testing:**
- Script-level smoke test - `scripts/test-install.ps1` generates or uses a local video, runs `scripts/process-reference-video-phase1.ps1`, validates output with `scripts/check-creative-material.ps1`, and cleans `.tmp/test-install` unless `-KeepOutput` is set.
- Material validation - `scripts/check-creative-material.ps1` checks generated folders for required root files, `_system-review-系统复查资料/` files, keyframe contact sheets, copied/moved reference videos, and output markdown.
- Skill metadata validation - documented in `README.md` and `docs/troubleshooting.md` via Codex's `quick_validate.py`; the validator is external to this repository.

**Build/Dev:**
- No compile/build step detected.
- Installer - `scripts/install-skill.ps1` copies `skills/zk-creative-process` into the user's Codex skills directory, defaulting to `$HOME/.codex/skills` or `$env:USERPROFILE\.codex\skills`.
- FFmpeg installer helper - `scripts/install-ffmpeg.ps1` checks for `ffmpeg` and `ffprobe`, then installs or prints platform-specific install guidance.

## Key Dependencies

**Critical:**
- FFmpeg executable - required for frame extraction, scaling, scene sampling, synthetic test video generation, and contact sheet creation in `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, and `scripts/test-install.ps1`.
- FFprobe executable - required for video/audio metadata extraction in `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
- Codex local skills directory - required for installation target in `scripts/install-skill.ps1`.

**Infrastructure:**
- Local filesystem - primary storage and output mechanism. Scripts create `creative-materials/YYYY-MM-DD-slug-name/`, `outputs/`, and `_system-review-系统复查资料/`.
- `.gitignore` - excludes generated `.tmp/`, `creative-materials/`, common video formats, and `keyframes-work/`; only the public `shower.mp4` exception is allowed by `.gitignore`.
- `skills/zk-creative-process/agents/openai.yaml` - exposes display metadata for the skill interface.

## Configuration

**Environment:**
- `scripts/check-environment.ps1` accepts `-FfmpegPath`, `-FfprobePath`, and `-TestDir` for explicit local configuration.
- `scripts/start-reference-video.ps1` and `scripts/process-reference-video-phase1.ps1` accept `-VideoPath`, `-Slug`, `-Name`, `-BaseDir`, `-FfmpegPath`, `-FfprobePath`, `-ProductBriefPath`, `-Copy`, `-Move`, `-KeepWork`, and frame-count options.
- `scripts/process-reference-videos-mix.ps1` accepts `-VideoPaths` for two or more same-direction inputs plus the same path and handling options.
- `scripts/install-skill.ps1` accepts `-CodexSkillsDir`, `-Force`, and `-Backup`.
- No `.env` or secret configuration files detected in the repository scan.

**Build:**
- Build config files: Not detected.
- Runtime config files:
  - `skills/zk-creative-process/SKILL.md`: skill metadata and workflow contract.
  - `skills/zk-creative-process/agents/openai.yaml`: interface label and default prompt.
  - `.gitignore`: generated-output and video-file hygiene.

## Platform Requirements

**Development:**
- Run from repository root for development copies in `scripts/`, or from installed skill folder for bundled copies in `skills/zk-creative-process/scripts/`.
- Use PowerShell with UTF-8-friendly terminal settings for Chinese file names such as `product-brief-产品信息.md` and `_system-review-系统复查资料/`.
- Validate PowerShell syntax after script changes, as required by `AGENTS.md`.
- Preserve the default copy behavior for source videos. Only use `-Move` when the user explicitly asks to move originals; this rule is enforced in `skills/zk-creative-process/SKILL.md` and implemented in `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.

**Production:**
- Deployment target is a local Codex skill installation under `.codex/skills/zk-creative-process`, created by `scripts/install-skill.ps1`.
- No server runtime, container runtime, hosted deployment, or cloud platform detected.
- Generated user materials are local files under `creative-materials/` and should not be committed.

---

*Stack analysis: 2026-05-27*
