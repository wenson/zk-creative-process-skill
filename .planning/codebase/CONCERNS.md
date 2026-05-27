---
title: Codebase Concerns
date: 2026-05-27
status: current
last_mapped_commit: 45bde0da596ed27b08f1bc632fed5716efdbd18d
---

# Codebase Concerns

**Analysis Date:** 2026-05-27

## Tech Debt

**Duplicated script surface:**
- Issue: Every helper script exists in both `scripts/` and `skills/zk-creative-process/scripts/`.
- Files: `scripts/start-reference-video.ps1`, `skills/zk-creative-process/scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1`, `scripts/check-environment.ps1`, `skills/zk-creative-process/scripts/check-environment.ps1`
- Impact: The repository currently keeps both copies identical, but future edits can drift and ship a different installed skill than the repo-level development scripts.
- Fix approach: Treat `skills/zk-creative-process/scripts/` as the packaged source of truth, or add a sync/check command that compares every `scripts/*.ps1` file to its bundled counterpart before release.

**No automated validation pipeline:**
- Issue: There is no detected `.github/workflows/` pipeline or local manifest that runs PowerShell syntax checks, `scripts/test-install.ps1`, or skill metadata validation automatically.
- Files: `README.md`, `scripts/test-install.ps1`, `skills/zk-creative-process/SKILL.md`
- Impact: Script syntax, cross-platform path behavior, and skill packaging can regress without being caught before commit.
- Fix approach: Add a CI workflow or documented release command that runs PowerShell parser validation for `scripts/*.ps1` and `skills/zk-creative-process/scripts/*.ps1`, then runs `scripts/test-install.ps1` where `pwsh`, `ffmpeg`, and `ffprobe` are available.

**Installer replacement lacks dry-run semantics:**
- Issue: `-Force` removes the existing installed skill directly.
- Files: `scripts/install-skill.ps1`, `skills/zk-creative-process/scripts/install-skill.ps1`
- Impact: The operation is explicit, but non-programmer users can lose local edits under `~/.codex/skills/zk-creative-process` without a preview or default backup.
- Fix approach: Prefer `-Backup` as the documented replacement path, add `SupportsShouldProcess`, and consider making `-Force` print the target path and require a second explicit confirmation flag for interactive users.

## Known Bugs

**Environment check can delete an existing custom test directory:**
- Symptoms: Passing `-TestDir` to `scripts/check-environment.ps1` creates a UTF-8 test file, then removes the entire `TestDir` with `Remove-Item -Recurse -Force`.
- Files: `scripts/check-environment.ps1`, `skills/zk-creative-process/scripts/check-environment.ps1`
- Trigger: Run `.\scripts\check-environment.ps1 -TestDir "C:\some-existing-folder"` or the equivalent on another platform.
- Workaround: Do not pass `-TestDir` unless it points to a disposable empty folder.
- Fix approach: Create a unique child folder under `TestDir` and delete only that child, or refuse to clean any user-provided directory unless it is under the repository `.tmp/` path.

**Tracked source video violates repository hygiene rules:**
- Symptoms: `video.mp4` is tracked even though `.gitignore` ignores `*.mp4` and `README.md` says not to commit customer videos, competitor videos, ad data, or generated materials.
- Files: `video.mp4`, `.gitignore`, `README.md`
- Trigger: `git ls-files '*.mp4'` lists `video.mp4`.
- Workaround: Treat `video.mp4` as public sample material only if intentionally allowed; otherwise remove it from Git history or replace it with a generated non-private sample.
- Fix approach: If a public sample is needed, align the filename with `.gitignore`'s `!shower.mp4` exception or update `.gitignore` and `README.md` to name the intended sample explicitly.

**Partial material folders remain after processing failure:**
- Symptoms: The scripts create the material folder and copy or move source videos before `ffprobe` and `ffmpeg` processing is complete.
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `skills/zk-creative-process/scripts/start-reference-video.ps1`, `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1`
- Trigger: Invalid video input, unsupported codec, missing write permission, or `ffmpeg` failure after folder creation.
- Workaround: Delete the failed material folder manually after confirming no original was moved unexpectedly.
- Fix approach: Build into a temporary staging folder, then rename to the final material folder only after metadata, contact sheets, manifest, and skeleton files are complete.

## Security Considerations

**Destructive cleanup path checks rely on string prefix matching:**
- Risk: Cleanup guards use `.StartsWith(...)` to decide whether `keyframes-work` is inside the material folder.
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `skills/zk-creative-process/scripts/start-reference-video.ps1`, `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1`
- Current mitigation: The work directory is constructed by the script under the generated material folder, so ordinary use is low risk.
- Recommendations: Replace string prefix checks with path-relative checks or parent-directory traversal using resolved `DirectoryInfo` objects so sibling prefixes cannot satisfy containment accidentally.

**Product brief may contain private business data:**
- Risk: Generated and copied `product-brief-产品信息.md` files can contain unreleased strategy, partner data, compliance limits, and ad hypotheses.
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `README.md`, `.gitignore`
- Current mitigation: Generated `creative-materials/` is ignored, and templates include a privacy reminder.
- Recommendations: Keep all filled product briefs under ignored `creative-materials/`; do not add example files containing real strategy under `examples/` or `docs/`.

**External package installer executes system package managers:**
- Risk: `scripts/install-ffmpeg.ps1` runs `winget install --id Gyan.FFmpeg -e` or `brew install ffmpeg`.
- Files: `scripts/install-ffmpeg.ps1`, `skills/zk-creative-process/scripts/install-ffmpeg.ps1`
- Current mitigation: Linux prints commands instead of auto-running distro-specific package managers; `-PrintOnly` previews Windows/macOS commands.
- Recommendations: Keep `-PrintOnly` visible in docs and avoid adding silent installers that change system state without a preview path.

## Performance Bottlenecks

**Single-video mode extracts unused intermediate frame sets:**
- Problem: `scripts/start-reference-video.ps1` extracts `fps=1` uniform frames and scene-change frames before selecting the final storyboard frames, but the final contact sheet uses only selected frames.
- Files: `scripts/start-reference-video.ps1`, `skills/zk-creative-process/scripts/start-reference-video.ps1`
- Cause: Intermediate frame counts are stored in the manifest, but generated images are deleted by default and are not part of the required AI input pack.
- Improvement path: Add a `-Fast` or `-SkipIntermediateFrames` mode, or make uniform/scene extraction opt-in when users need diagnostics.

**Long videos have linear processing cost:**
- Problem: Runtime and temporary disk usage scale with full source duration in single mode.
- Files: `scripts/start-reference-video.ps1`, `docs/troubleshooting.md`
- Cause: `fps=1` extraction scans the entire video, and scene detection also scans the entire video.
- Improvement path: Add `-StartTime` and `-Duration` parameters so users can process only the ad segment; document this as the preferred path for long recordings.

## Fragile Areas

**PowerShell availability is assumed by validation docs:**
- Files: `README.md`, `docs/troubleshooting.md`, `scripts/test-install.ps1`
- Why fragile: This mapping environment did not expose `pwsh` or `powershell`, so syntax and runtime validation cannot be performed everywhere the repository can be edited.
- Safe modification: After script edits, validate on a machine with PowerShell 7+, `ffmpeg`, and `ffprobe`; run `scripts/test-install.ps1` and compare root scripts against bundled scripts.
- Test coverage: No automated coverage detected.

**JSON orchestration depends on child scripts producing clean JSON:**
- Files: `scripts/process-reference-video-phase1.ps1`, `skills/zk-creative-process/scripts/process-reference-video-phase1.ps1`
- Why fragile: The wrapper captures child output with `Out-String` and immediately calls `ConvertFrom-Json`; any extra non-JSON output from `start-reference-video.ps1` or `check-creative-material.ps1 -Json` breaks orchestration.
- Safe modification: Keep setup scripts quiet in machine-readable paths, or add a `-Json` switch to `start-reference-video.ps1` and emit human logs to stderr or log files.
- Test coverage: `scripts/test-install.ps1` exercises the path, but there is no CI gate.

**User-facing filenames include free-form `Name`:**
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`
- Why fragile: Invalid filename characters are blocked, but very long names, reserved Windows device names, trailing dots/spaces, and shell-unfriendly names are not explicitly constrained.
- Safe modification: Keep `Slug` strict and consider deriving filesystem names primarily from `Slug`, with human-readable `Name` stored inside markdown metadata.
- Test coverage: No detected tests cover long, reserved, or platform-specific names.

## Scaling Limits

**Material folder storage grows quickly with copied source videos:**
- Current capacity: Each run copies one or more full source videos into `creative-materials/` by default.
- Limit: Local disk usage grows with every creative batch; mix mode multiplies this by video count.
- Scaling path: Keep copy-by-default for safety, but add documented cleanup guidance, optional compression, or a manifest-only reference mode for trusted local archives.

**Mix mode processes videos sequentially:**
- Current capacity: `scripts/process-reference-videos-mix.ps1` loops over every input video and extracts frames one video at a time.
- Limit: Large same-direction batches can be slow even when CPU has available parallel capacity.
- Scaling path: Keep sequential mode as default for clearer logs; add an advanced parallel option only after logging and failure behavior are well-defined.

## Dependencies at Risk

**FFmpeg and FFprobe are external runtime dependencies:**
- Risk: Version differences can change filter behavior, codec support, and deprecation warnings such as `-vsync`.
- Impact: Frame extraction, scene detection, and contact sheet generation can fail or produce different outputs across machines.
- Migration plan: Record `ffmpeg -version` and `ffprobe -version` into `run-manifest.json`; add compatibility guidance in `docs/troubleshooting.md`.

**Codex skill validator is referenced by user-local path:**
- Risk: README validation uses `$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py`, which may not exist on every machine.
- Impact: Non-programmer users may not be able to validate skill metadata with the documented command.
- Migration plan: Provide a repository-level validation wrapper that checks for the validator and prints a clear fallback when it is missing.

## Missing Critical Features

**No repository hygiene preflight:**
- Problem: There is no command that fails when tracked source videos, generated `creative-materials/`, private briefs, or ad strategy notes are present.
- Blocks: Safe release of a repository whose rules explicitly forbid committing source videos and generated creative materials.
- Files: `.gitignore`, `README.md`, `video.mp4`

**No release checklist for packaged skill sync:**
- Problem: The repo has both development scripts and packaged scripts, but no release checklist file or script that verifies they match.
- Blocks: Confident publishing of `skills/zk-creative-process/` after changes under `scripts/`.
- Files: `scripts/`, `skills/zk-creative-process/scripts/`

## Test Coverage Gaps

**PowerShell syntax and parser coverage:**
- What's not tested: Parser validation for all `.ps1` files.
- Files: `scripts/*.ps1`, `skills/zk-creative-process/scripts/*.ps1`
- Risk: Syntax errors ship into the installable skill.
- Priority: High

**Destructive behavior coverage:**
- What's not tested: `-Move`, `-Force`, `-Backup`, cleanup guards, and custom `-TestDir` behavior.
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `scripts/install-skill.ps1`, `scripts/check-environment.ps1`
- Risk: User files can be moved, replaced, or deleted in surprising ways.
- Priority: High

**Cross-platform path coverage:**
- What's not tested: Spaces, Chinese characters, reserved Windows names, long names, and custom executable paths across Windows/macOS/Linux.
- Files: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `scripts/check-environment.ps1`
- Risk: The install path is intended for non-programmers, so path failures directly break the main use case.
- Priority: Medium

**Generated material validation coverage:**
- What's not tested: Single and mix material folders after AI fills skeleton outputs, including strict TODO checks.
- Files: `scripts/check-creative-material.ps1`, `scripts/process-reference-video-phase1.ps1`, `scripts/process-reference-videos-mix.ps1`
- Risk: A generated folder can look complete while still containing placeholders or missing required system files.
- Priority: Medium

---

*Concerns audit: 2026-05-27*
