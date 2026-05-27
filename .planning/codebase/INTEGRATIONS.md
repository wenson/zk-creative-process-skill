---
title: External Integrations
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

# External Integrations

**Analysis Date:** 2026-05-27

## APIs & External Services

**Local Media Tooling:**
- FFmpeg - extracts frames, scales images, creates contact sheets, and generates synthetic test video.
  - SDK/Client: native `ffmpeg` executable invoked from PowerShell in `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, and `scripts/test-install.ps1`.
  - Auth: Not applicable.
- FFprobe - reads video/audio stream and format metadata.
  - SDK/Client: native `ffprobe` executable invoked from `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
  - Auth: Not applicable.

**Installer Package Sources:**
- Windows Package Manager (`winget`) - installs Gyan.FFmpeg on Windows through `scripts/install-ffmpeg.ps1`.
  - SDK/Client: `winget` CLI.
  - Auth: Not applicable.
- Homebrew - installs FFmpeg on macOS through `scripts/install-ffmpeg.ps1`.
  - SDK/Client: `brew` CLI.
  - Auth: Not applicable.
- Linux package managers - documented install options in `scripts/install-ffmpeg.ps1` and `docs/troubleshooting.md`.
  - SDK/Client: `apt`, `dnf`, or `pacman` command examples.
  - Auth: system-level package manager privileges, not application credentials.

**Codex Local Skill Runtime:**
- Codex skills directory - installation target for the self-contained skill.
  - SDK/Client: filesystem copy via `scripts/install-skill.ps1`.
  - Auth: local filesystem permissions only.
- Codex skill metadata - `skills/zk-creative-process/SKILL.md` and `skills/zk-creative-process/agents/openai.yaml` describe the skill to Codex.
  - SDK/Client: local Codex skill loader.
  - Auth: Not applicable.

**External Web APIs:**
- Not detected. Repository scripts do not call HTTP APIs, webhooks, SDK clients, `Invoke-WebRequest`, `Invoke-RestMethod`, or cloud service clients.

## Data Storage

**Databases:**
- Not detected.
  - Connection: Not applicable.
  - Client: Not applicable.

**File Storage:**
- Local filesystem only.
  - Source videos are copied by default into generated material folders by `scripts/start-reference-video.ps1` and `scripts/process-reference-videos-mix.ps1`.
  - Moving originals requires explicit `-Move`; `-Copy` and `-Move` are mutually exclusive in both single and mix processing scripts.
  - Generated files are created under `creative-materials/YYYY-MM-DD-slug-name/` unless `-BaseDir` overrides the target.
  - System review artifacts are written under `_system-review-系统复查资料/`.
  - Temporary frame work files are created under `keyframes-work/` and removed unless `-KeepWork` is used.

**Caching:**
- No persistent cache service detected.
- Temporary local working directories are used during frame extraction:
  - `scripts/start-reference-video.ps1` creates `keyframes-work/uniform`, `keyframes-work/scene`, and `keyframes-work/selected`.
  - `scripts/process-reference-videos-mix.ps1` creates `keyframes-work/selected-*` folders.
  - `scripts/test-install.ps1` uses `.tmp/test-install`.

## Authentication & Identity

**Auth Provider:**
- None.
  - Implementation: no login flow, token validation, session management, or identity provider integration detected.
  - Local permissions: scripts depend on current user permissions for reading videos, writing output folders, installing into `.codex/skills`, and optionally running system package managers.

## Monitoring & Observability

**Error Tracking:**
- None.

**Logs:**
- Local command logs only.
  - `scripts/start-reference-video.ps1` writes FFmpeg logs such as `ffmpeg-uniform.log`, `ffmpeg-scene.log`, `ffmpeg-selected-*.log`, and `ffmpeg-final-sheet.log` under `keyframes-work/`.
  - `scripts/process-reference-videos-mix.ps1` writes per-video FFmpeg logs under `keyframes-work/`.
  - `scripts/test-install.ps1` writes `.tmp/test-install/ffmpeg-generate.log` when it generates a synthetic test video.
  - Validation output is printed to stdout or JSON by `scripts/check-creative-material.ps1`.

## CI/CD & Deployment

**Hosting:**
- Not applicable. This repository ships a local Codex skill and scripts, not a hosted service.

**CI Pipeline:**
- Not detected. No `.github/`, build config, or CI workflow files were found in the repository scan.

**Deployment / Installation:**
- `scripts/install-skill.ps1` copies the skill into the local Codex skills directory.
- Existing installs are protected by default:
  - `-Backup` moves the existing destination to a timestamped backup.
  - `-Force` removes and replaces the existing destination.
  - Without either flag, the installer stops if the destination already exists.

## Environment Configuration

**Required env vars:**
- None required by repository scripts.
- `$env:USERPROFILE` and `$HOME` are read by `scripts/install-skill.ps1` only to infer the default Codex skills directory.
- `$env:OS` is read by `scripts/install-ffmpeg.ps1` only to detect Windows.
- `$env:PYTHONUTF8` is documented in `README.md` and `docs/troubleshooting.md` only for running the external Codex skill validator on Windows.

**Secrets location:**
- Not detected.
- No `.env`, credential, certificate, private key, or package-manager auth files were detected in the repository scan.
- Generated `product-brief-产品信息.md` templates explicitly warn users not to include API keys, unreleased financial data, personal information, or private partner data.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

## Integration Boundaries For Future Work

- Keep new functionality local-first unless a product requirement explicitly introduces a network dependency.
- Do not add API keys or cloud credentials to generated materials, `product-brief-产品信息.md`, examples, docs, or repository config.
- If adding external APIs, document the SDK package, required environment variables, failure modes, and privacy implications in this file.
- If changing video handling, preserve the current contract: copy by default, move only with explicit `-Move`, and never commit generated `creative-materials/` or private source videos.

---

*Integration audit: 2026-05-27*
