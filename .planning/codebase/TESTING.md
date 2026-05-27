---
title: Testing Patterns
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

# Testing Patterns

**Analysis Date:** 2026-05-27

## Test Framework

**Runner:**
- No formal unit-test runner is configured.
- Functional validation is script-based through `scripts/check-environment.ps1`, `scripts/test-install.ps1`, and `scripts/check-creative-material.ps1`.
- The installable skill contains identical validation scripts under `skills/zk-creative-process/scripts/`.

**Assertion Library:**
- Native PowerShell checks, `throw`, `$LASTEXITCODE`, and exit codes.
- Validation issue objects are accumulated in `scripts/check-creative-material.ps1` and emitted as human-readable lines or JSON.

**Run Commands:**
```bash
pwsh -NoProfile -File scripts/check-environment.ps1
pwsh -NoProfile -File scripts/test-install.ps1
pwsh -NoProfile -File scripts/check-creative-material.ps1 -MaterialDir "./creative-materials/YYYY-MM-DD-slug-name"
```

**Syntax Validation:**
```bash
pwsh -NoProfile -Command '$ErrorActionPreference="Stop"; Get-ChildItem -Path scripts,skills/zk-creative-process/scripts -Filter *.ps1 -Recurse | ForEach-Object { $tokens=$null; $errors=$null; [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) > $null; if ($errors.Count -gt 0) { throw "$($_.FullName): $($errors[0].Message)" } }'
```

**Skill Metadata Validation:**
```bash
PYTHONUTF8=1 python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/zk-creative-process
```

On Windows PowerShell:
```powershell
$env:PYTHONUTF8='1'
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skills\zk-creative-process
```

## Test File Organization

**Location:**
- Script tests are in `scripts/test-install.ps1`.
- Environment checks are in `scripts/check-environment.ps1`.
- Generated material checks are in `scripts/check-creative-material.ps1`.
- Installed-skill copies are in `skills/zk-creative-process/scripts/test-install.ps1`, `skills/zk-creative-process/scripts/check-environment.ps1`, and `skills/zk-creative-process/scripts/check-creative-material.ps1`.

**Naming:**
- Use verb-focused script names: `test-install.ps1`, `check-environment.ps1`, and `check-creative-material.ps1`.
- No `*.test.*` or `*.spec.*` files are present.

**Structure:**
```text
scripts/
  check-environment.ps1          # prerequisites and filesystem UTF-8 smoke check
  test-install.ps1               # end-to-end generated-video workflow test
  check-creative-material.ps1    # validates generated material folders
skills/zk-creative-process/scripts/
  same validation scripts bundled with the installable skill
```

## Test Structure

**Suite Organization:**
```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$resultJson = & (Join-Path $PSScriptRoot 'process-reference-video-phase1.ps1') `
    -VideoPath $videoPath `
    -Slug 'test-install' `
    -Name 'test-install-测试安装' `
    -BaseDir $outputDir `
    -FfmpegPath $ffmpeg `
    -FfprobePath $ffprobe `
    -Copy `
    -StoryboardFrames 6 | Out-String

if ($LASTEXITCODE -ne 0) {
    throw 'process-reference-video-phase1.ps1 failed.'
}
$result = $resultJson | ConvertFrom-Json
```

**Patterns:**
- Resolve prerequisites first using `Resolve-Executable`.
- Generate a synthetic vertical MP4 with FFmpeg when no local `shower.*` sample exists.
- Run the real single-video pipeline through `scripts/process-reference-video-phase1.ps1`.
- Parse JSON output with `ConvertFrom-Json`.
- Validate the generated folder with `scripts/check-creative-material.ps1`.
- Clean `.tmp/test-install` by default; keep output only with `-KeepOutput`.

## Mocking

**Framework:** Not used.

**Patterns:**
```powershell
& $ffmpeg -hide_banner -y -f lavfi -i testsrc=size=720x1280:rate=30 -t 3 -pix_fmt yuv420p $videoPath *> (Join-Path $tmpRoot 'ffmpeg-generate.log')
if ($LASTEXITCODE -ne 0) {
    throw "Failed to generate test video. See: $(Join-Path $tmpRoot 'ffmpeg-generate.log')"
}
```

**What to Mock:**
- Do not mock FFmpeg or FFprobe in the current test style; use a generated synthetic video for realistic pipeline coverage.
- Use explicit `-FfmpegPath` and `-FfprobePath` parameters to test non-PATH installations.

**What NOT to Mock:**
- Do not mock filesystem writes, path resolution, JSON generation, or cleanup safety checks. These are core behavior for non-programmer install reliability.
- Do not mock `Copy-Item` versus `Move-Item` semantics when testing source-video preservation.

## Fixtures and Factories

**Test Data:**
```powershell
$sample = Get-ChildItem -LiteralPath $repoRoot.Path -File -Filter 'shower.*' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($sample) {
    $videoPath = $sample.FullName
} else {
    $videoPath = Join-Path $tmpRoot 'generated-test-video.mp4'
    & $ffmpeg -hide_banner -y -f lavfi -i testsrc=size=720x1280:rate=30 -t 3 -pix_fmt yuv420p $videoPath *> (Join-Path $tmpRoot 'ffmpeg-generate.log')
}
```

**Location:**
- Synthetic video output is created under `.tmp/test-install`.
- Generated material output is created under `.tmp/test-install/creative-materials`.
- Real source videos and generated `creative-materials/` are ignored by `.gitignore`.

## Coverage

**Requirements:** No numeric coverage target is enforced.

**View Coverage:**
```bash
# Not applicable; no coverage tool is configured.
```

**Current Validation Coverage:**
- `scripts/check-environment.ps1` verifies PowerShell version, FFmpeg, FFprobe, and UTF-8 filesystem write/read.
- `scripts/test-install.ps1` exercises the single-video path, generated video fallback, JSON parsing, material validation, and cleanup boundary.
- `scripts/check-creative-material.ps1` checks required root files, `_system-review-系统复查资料/` files, contact sheets, reference videos, output files, and TODO placeholders.
- `README.md` documents Codex skill validation with `quick_validate.py`.

## Test Types

**Unit Tests:**
- Not used. Helper functions such as `Resolve-Executable`, `Parse-Fps`, `Invoke-Logged`, and `Assert-SafeFileNamePart` are tested only through script-level execution.

**Integration Tests:**
- `scripts/test-install.ps1` is the main integration test. It runs FFmpeg, creates a material folder, runs `scripts/process-reference-video-phase1.ps1`, then validates the result.
- `scripts/check-creative-material.ps1 -Json` can be used by automation to assert folder validity without parsing human text.

**E2E Tests:**
- Manual E2E path is documented in `README.md`: install via `scripts/install-skill.ps1`, process a video, then use `$zk-creative-process single` or `$zk-creative-process mix` in Codex.
- Skill validation uses `quick_validate.py` against `skills/zk-creative-process`.

## Common Patterns

**Async Testing:**
```powershell
# Not applicable. Scripts are synchronous and check $LASTEXITCODE after external commands.
```

**Error Testing:**
```powershell
if ($Copy -and $Move) {
    throw 'Use either -Copy or -Move, not both. Copy is the default.'
}
if ($StoryboardFrames -lt 4 -or $StoryboardFrames -gt 30) {
    throw 'StoryboardFrames must be between 4 and 30.'
}
```

**Validation Object Pattern:**
```powershell
$checks = [System.Collections.Generic.List[object]]::new()
Add-Check -Checks $checks -Name 'ffmpeg available' -Passed (-not [string]::IsNullOrWhiteSpace($ffmpeg)) -Detail $detail -Fix $fix
$failed = @($checks | Where-Object { -not $_.passed })
exit $(if ($failed.Count -eq 0) { 0 } else { 1 })
```

## Manual Checks

**After Script Changes:**
- Run PowerShell parser syntax validation over both `scripts/` and `skills/zk-creative-process/scripts/`.
- Compare root and bundled script copies with `cmp scripts/<name>.ps1 skills/zk-creative-process/scripts/<name>.ps1`.
- Run `scripts/check-environment.ps1`.
- Run `scripts/test-install.ps1`; use `-KeepOutput` when inspecting generated files.
- Run `scripts/check-creative-material.ps1 -MaterialDir <generated-folder> -Strict` after filling output Markdown.

**After Skill Metadata Changes:**
- Run `quick_validate.py` against `skills/zk-creative-process`.
- Confirm `skills/zk-creative-process/SKILL.md` keeps command modes `single` and `mix`, copy-by-default behavior, product-brief requirements, and completion checks.

**After Documentation Changes:**
- Keep `README.md` as the short entry guide.
- Put longer setup, troubleshooting, and folder explanation in `docs/`.
- Keep `examples/` lightweight and free of private creative material.

## Coverage Gaps

**Mix Workflow:**
- `scripts/process-reference-videos-mix.ps1` has no automated end-to-end test equivalent to `scripts/test-install.ps1`.
- Add a generated two-video smoke test that validates `outputs/shared-analysis-同方向素材共性拆解.md`, per-video contact sheets, and mix `frame-index.json`.

**Installer Behavior:**
- `scripts/install-skill.ps1` is not covered by an automated temp-home install test.
- Add a test using a temporary `-CodexSkillsDir` to cover first install, existing destination error, `-Backup`, and `-Force`.

**Move Versus Copy:**
- Default copy behavior is covered indirectly by `scripts/test-install.ps1 -Copy`, but there is no explicit assertion that the original source remains after default execution.
- Add tests for default no-flag copy, explicit `-Copy`, explicit `-Move`, and rejected `-Copy -Move`.

**Failure Paths:**
- Missing FFmpeg, missing input video, invalid slug, invalid `Name`, existing material directory, and invalid `StoryboardFrames` are not covered by automated negative tests.

**PowerShell Versions:**
- `scripts/check-environment.ps1` supports PowerShell 5.1+, but local validation should be run on Windows PowerShell 5.1 and PowerShell 7 before release.

**Current Mapping Environment:**
- `pwsh`/`powershell` was not available in the current shell, so parser validation and script execution were not run during this mapping pass.

---

*Testing analysis: 2026-05-27*
