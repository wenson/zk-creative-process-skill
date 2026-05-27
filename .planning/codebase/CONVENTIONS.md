---
title: Coding Conventions
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

# Coding Conventions

**Analysis Date:** 2026-05-27

## Naming Patterns

**Files:**
- Use kebab-case for repository scripts: `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `scripts/check-creative-material.ps1`.
- Keep installable skill scripts mirrored under `skills/zk-creative-process/scripts/`; every file currently matches its root `scripts/` counterpart byte-for-byte.
- Use uppercase `SKILL.md` for the Codex skill entry point at `skills/zk-creative-process/SKILL.md`.
- Keep human documentation in Markdown under `README.md`, `docs/creative-process-guide.md`, `docs/example-folder-structure.md`, and `docs/troubleshooting.md`.
- Generated user-facing material filenames intentionally include Chinese names: `product-brief-产品信息.md`, `outputs/reference-video-storyboard-原视频场景变化分镜.md`, and `outputs/creative-script-directions-创意脚本方向.md`.

**Functions:**
- Use approved PowerShell verb-noun style where practical: `Resolve-Executable`, `Resolve-FilePath`, `Invoke-Logged`, `New-TileSheet`, `Add-Issue`, `Add-Check`.
- Keep small helper functions near the top of each script before the main execution path, as in `scripts/start-reference-video.ps1` and `scripts/check-environment.ps1`.
- Use imperative function names for validation helpers, such as `Assert-SafeFileNamePart` in `scripts/start-reference-video.ps1`.

**Variables:**
- Use lower camelCase for local variables: `$materialDir`, `$outputsDir`, `$systemDir`, `$productBriefOutputPath`, `$frameIndexPath`.
- Use PascalCase for public script parameters: `$VideoPath`, `$VideoPaths`, `$Slug`, `$Name`, `$BaseDir`, `$FfmpegPath`, `$FfprobePath`.
- Use boolean switches for behavior changes: `$Copy`, `$Move`, `$KeepWork`, `$StrictCheck`, `$Json`, `$PrintOnly`.
- Use ordered hashtables for structured JSON output: `[ordered]@{ ... } | ConvertTo-Json` in `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, and `scripts/process-reference-video-phase1.ps1`.

**Types:**
- Scripts are plain PowerShell `.ps1`; no module `.psm1` or class files are present.
- Parameter types are explicit where behavior matters: `[string]`, `[string[]]`, `[int]`, `[double]`, and `[switch]`.
- Use `[System.Collections.Generic.List[object]]::new()` when accumulating validation checks or issues, as in `scripts/check-creative-material.ps1` and `scripts/check-environment.ps1`.

## Code Style

**Formatting:**
- No formatter configuration file is present; use the existing PowerShell style in `scripts/*.ps1`.
- Put one parameter per line in top-level `param(...)` blocks.
- Use four-space indentation inside functions, conditionals, loops, and hashtables.
- Prefer backtick line continuation only for long command invocations in docs and script calls, as in `README.md` and `scripts/process-reference-video-phase1.ps1`.
- Keep generated Markdown skeletons as here-strings with `Set-Content -Encoding UTF8`, as in `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.

**Linting:**
- No `PSScriptAnalyzerSettings.psd1`, `.editorconfig`, ESLint, Prettier, or Biome configuration is present.
- Validate PowerShell syntax after script changes using the PowerShell parser before runtime tests.
- Keep scripts compatible with PowerShell 5.1+ where possible, while `README.md` recommends PowerShell 7+.

## Import Organization

**Order:**
1. Top-level `param(...)` block with mandatory and optional parameters.
2. `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
3. Helper functions such as `Resolve-Executable`, `Invoke-Logged`, or validation accumulators.
4. Input validation and default resolution.
5. Main file processing, FFmpeg calls, JSON/Markdown generation, cleanup, and final structured output.

**Path Aliases:**
- Not detected. Scripts resolve paths through `$PSScriptRoot`, `$PSCommandPath`, `Resolve-Path -LiteralPath`, and `Join-Path`.
- Use `-LiteralPath` for filesystem operations that may include spaces or non-English characters, as documented in `docs/troubleshooting.md`.

## Error Handling

**Patterns:**
- Set strict execution in every root script with `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
- Use `throw` for invalid inputs, missing executables, failed external commands, unsafe cleanup boundaries, and existing material folders.
- Check `$LASTEXITCODE` immediately after FFmpeg, FFprobe, or child-script calls.
- Log FFmpeg output to files under temporary work directories, then throw with the log path using `Invoke-Logged` in `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
- Prevent accidental destructive cleanup by resolving paths and checking that work directories start inside the intended parent before `Remove-Item`, as in `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, and `scripts/test-install.ps1`.
- Do not overwrite generated material folders; `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1` throw when `$materialDir` already exists.
- Preserve source videos by default. Use `Copy-Item` unless the user explicitly passes `-Move`; both single and mix scripts reject simultaneous `-Copy` and `-Move`.

## Logging

**Framework:** console output and FFmpeg log files.

**Patterns:**
- External command stdout/stderr is redirected to log files with `*> $LogPath`.
- Validation scripts print readable status lines, for example `scripts/check-environment.ps1` outputs `[OK]` and `[FAIL]` checks.
- Processing scripts return JSON for machine-readable orchestration, especially `scripts/process-reference-video-phase1.ps1`, `scripts/start-reference-video.ps1`, and `scripts/process-reference-videos-mix.ps1`.
- `scripts/check-creative-material.ps1` supports both human-readable output and JSON via `-Json`.

## Comments

**When to Comment:**
- Use comments sparingly for non-obvious behavior only; most scripts rely on clear function names and explicit errors.
- Keep user-facing explanations in `README.md` and `docs/`, not inline script comments.
- Preserve the existing non-fatal cleanup comment style, such as `# Non-fatal cleanup failure.` in `scripts/check-environment.ps1`.

**JSDoc/TSDoc:**
- Not applicable. This is a PowerShell and Markdown repository.

## Function Design

**Size:** Keep reusable helpers small and local to the script that needs them. Larger workflow scripts such as `scripts/start-reference-video.ps1` can be linear because they generate a full material folder in one pass.

**Parameters:** Use explicit mandatory parameters for required user inputs. Apply `ValidatePattern('^[a-z0-9][a-z0-9-]*$')` to slug parameters in `scripts/start-reference-video.ps1`, `scripts/process-reference-video-phase1.ps1`, and `scripts/process-reference-videos-mix.ps1`.

**Return Values:** Return final machine-readable `[ordered]` JSON from processing scripts. Return exit code `1` for failed validation or environment checks.

## Module Design

**Exports:** Not applicable. There are no PowerShell modules or exported functions.

**Barrel Files:** Not applicable.

**Repository Duplication Rule:** Keep `scripts/*.ps1` and `skills/zk-creative-process/scripts/*.ps1` synchronized. When changing a script, update both copies or use a sync step, then compare with `cmp` or `git diff --no-index`.

## Documentation Conventions

**Entry Guide:** Keep quick install and usage in `README.md`.

**Longer Notes:** Put troubleshooting and workflow details in `docs/troubleshooting.md`, `docs/creative-process-guide.md`, and `docs/example-folder-structure.md`.

**Examples:** Keep examples lightweight in `examples/single/README.md` and `examples/mix/README.md`; do not include private videos, private ad data, or generated `creative-materials/`.

## Generated File Conventions

**Material Root:** Human-facing files belong in the generated material root: source video copy, contact sheet, `brief.md`, and `product-brief-产品信息.md`.

**Automation Folder:** Machine-review artifacts belong in `_system-review-系统复查资料/`: `ai-input-pack.md`, `frame-index.json`, `run-manifest.json`, and `video_metadata.json`.

**Outputs:** AI-fillable analysis goes in `outputs/`.

**Privacy:** Do not commit source videos, generated `creative-materials/`, private ad data, filled strategy notes, or product briefs with confidential data. `.gitignore` ignores `creative-materials/`, `.tmp/`, common video extensions, and `keyframes-work/`.

---

*Convention analysis: 2026-05-27*
