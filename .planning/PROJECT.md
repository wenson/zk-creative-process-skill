# ZK Creative Process Skill

## What This Is

ZK Creative Process Skill is a Codex skill and PowerShell toolkit for turning game-ad reference videos into clean creative-analysis material folders. It is for creators and operators who need AI to deconstruct reference ads, preserve the evidence behind the analysis, and map the structure into their own product only when product facts are available.

The repository packages the installable skill under `skills/zk-creative-process/`, repository-level development scripts under `scripts/`, and documentation for non-programmer usage.

## Core Value

Make reference-video creative analysis stable, reviewable, and reusable without moving user originals by default or inventing missing product facts.

## Requirements

### Validated

- ✓ Installable Codex skill package exists under `skills/zk-creative-process/` with skill instructions, UI metadata, and bundled scripts — existing
- ✓ Single-video workflow creates a material folder, copies the source video by default, extracts keyframes, writes metadata, and returns validation JSON — existing
- ✓ Mix workflow creates one shared direction-level folder for multiple same-direction reference videos — existing
- ✓ Product context is separated into `product-brief-产品信息.md`, and skill instructions require product mapping to stay pending when product facts are missing — existing
- ✓ Generated system review artifacts are separated under `_system-review-系统复查资料/` while human-facing files stay at the material root and `outputs/` — existing
- ✓ Material folder validation exists through `scripts/check-creative-material.ps1` — existing
- ✓ Environment and install helper scripts exist for checking FFmpeg/FFprobe and installing the skill — existing

### Active

- [ ] Add a release preflight that catches tracked source videos, generated `creative-materials/`, private briefs, and strategy notes before commit or release
- [ ] Add a script-sync check so root `scripts/*.ps1` and bundled `skills/zk-creative-process/scripts/*.ps1` cannot drift silently
- [ ] Add or document one reliable validation command that runs PowerShell parser checks, smoke tests, material validation, and skill metadata validation
- [ ] Make destructive or surprising operations safer, especially installer overwrite, `-Move`, cleanup, and custom test directories
- [ ] Improve generated-material robustness by reducing partial folder leftovers when FFmpeg/FFprobe fails mid-run
- [ ] Align sample-video repository hygiene with `.gitignore`, README privacy rules, and `AGENTS.md`

### Out of Scope

- Full ad production automation before a story direction is selected — the skill intentionally creates a direction pool first
- Inventing product facts from reference videos — missing product information must produce questions and pending mapping
- Hosted backend, cloud service, database, or web UI — this project is a local Codex skill and script toolkit
- Committing generated creative materials, customer videos, competitor videos, private ad data, or filled strategy briefs — these belong outside git

## Context

The codebase is a brownfield repository. A codebase map already exists in `.planning/codebase/` and describes the current architecture, stack, testing patterns, and risk areas.

The core runtime is PowerShell with FFmpeg and FFprobe. The skill depends on local filesystem operations, copied source videos, generated contact sheets, JSON metadata, and Markdown analysis skeletons. There is no server runtime, package manifest, or formal unit test runner.

The repository intentionally has two script surfaces: root scripts in `scripts/` for development and installer entry points, and bundled scripts in `skills/zk-creative-process/scripts/` for the installed skill. Current behavior relies on keeping those copies synchronized.

The main product boundary is important: deterministic scripts prepare evidence and skeleton files; AI writes creative analysis afterward. Product mapping is only valid when `product-brief-产品信息.md` contains real product context.

Known risk from the current repository state: `video.mp4` is tracked even though `.gitignore`, README privacy guidance, and `AGENTS.md` say source videos should not be committed unless an explicit public sample exception is documented.

## Constraints

- **Safety**: Source videos are copied by default; moving originals requires explicit `-Move` — this prevents accidental loss of user material
- **Privacy**: Generated `creative-materials/`, filled product briefs, ad data, and strategy notes must not be committed — these files can contain private business context
- **Packaging**: `skills/zk-creative-process/` must remain self-contained — installed users should not need repository-only files
- **Script parity**: Root `scripts/` and bundled `skills/zk-creative-process/scripts/` should stay synchronized — otherwise installed behavior can differ from tested behavior
- **Runtime**: PowerShell plus FFmpeg/FFprobe are required — validation must account for machines where these are missing
- **User experience**: Install and troubleshooting should stay friendly for non-programmers — one clear command, clear next step, and no silent destructive behavior

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Treat the project as a reliable local skill package, not a video generation product | Existing code prepares material folders and analysis inputs; it does not produce final ads directly | — Pending |
| Keep product mapping gated by `product-brief-产品信息.md` | Prevents AI from inventing game/product facts from a reference ad | ✓ Good |
| Preserve copy-by-default source handling | Protects original user videos and matches `AGENTS.md` rules | ✓ Good |
| Focus v1 on release safety, validation, and non-programmer reliability | Current features exist, but codebase mapping found release hygiene and validation gaps | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-27 after initialization*
