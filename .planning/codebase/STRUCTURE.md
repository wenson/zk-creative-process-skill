---
title: Codebase Structure
date: 2026-05-27
status: current
last_mapped_commit: 45bde0d
---

# Codebase Structure

**Analysis Date:** 2026-05-27

## Directory Layout

```text
zk-creative-process-skill/
├── AGENTS.md                         # Repository rules and contribution boundaries
├── README.md                         # Entry guide for install, usage, requirements, docs, privacy
├── LICENSE                           # MIT license
├── .gitignore                        # Ignores generated materials, temp files, and videos
├── .planning/
│   └── codebase/                     # GSD codebase maps
├── docs/                             # Longer usage notes and troubleshooting
│   ├── creative-process-guide.md     # Deterministic processing vs AI judgment guide
│   ├── example-folder-structure.md   # Expected generated folder examples
│   └── troubleshooting.md            # FFmpeg, PowerShell, path, TODO, and privacy troubleshooting
├── examples/                         # Lightweight public examples only
│   ├── single/
│   │   └── README.md                 # Single-video example
│   └── mix/
│       └── README.md                 # Same-direction batch example
├── scripts/                          # Root-level development, test, and installer scripts
│   ├── check-creative-material.ps1
│   ├── check-environment.ps1
│   ├── install-ffmpeg.ps1
│   ├── install-skill.ps1
│   ├── process-reference-video-phase1.ps1
│   ├── process-reference-videos-mix.ps1
│   ├── start-reference-video.ps1
│   └── test-install.ps1
└── skills/
    └── zk-creative-process/          # Installable self-contained Codex skill
        ├── SKILL.md                  # Skill instructions and workflow contract
        ├── agents/
        │   └── openai.yaml           # Skill UI metadata and default prompt
        └── scripts/                  # Bundled scripts copied with the installed skill
            ├── check-creative-material.ps1
            ├── check-environment.ps1
            ├── install-ffmpeg.ps1
            ├── install-skill.ps1
            ├── process-reference-video-phase1.ps1
            ├── process-reference-videos-mix.ps1
            ├── start-reference-video.ps1
            └── test-install.ps1
```

## Directory Purposes

**Repository Root:**
- Purpose: Provide the entry guide, repo rules, license, ignore policy, install command, and root script entry points.
- Contains: `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `scripts/`, `skills/`, `docs/`, `examples/`, `.planning/`.
- Key files: `README.md`, `AGENTS.md`, `.gitignore`, `scripts/install-skill.ps1`.

**`skills/zk-creative-process/`:**
- Purpose: The installable, self-contained Codex skill package.
- Contains: `SKILL.md`, `agents/openai.yaml`, and bundled PowerShell scripts.
- Key files: `skills/zk-creative-process/SKILL.md`, `skills/zk-creative-process/agents/openai.yaml`, `skills/zk-creative-process/scripts/process-reference-video-phase1.ps1`.

**`skills/zk-creative-process/scripts/`:**
- Purpose: Scripts bundled with the skill for direct use after copying the skill folder.
- Contains: Mirrored copies of all root scripts.
- Key files: `skills/zk-creative-process/scripts/start-reference-video.ps1`, `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1`, `skills/zk-creative-process/scripts/check-creative-material.ps1`.

**`scripts/`:**
- Purpose: Repository-level copies and wrappers for development, testing, and installer entry points.
- Contains: PowerShell scripts for install, environment checks, video processing, material validation, FFmpeg install, and smoke tests.
- Key files: `scripts/install-skill.ps1`, `scripts/process-reference-video-phase1.ps1`, `scripts/start-reference-video.ps1`, `scripts/process-reference-videos-mix.ps1`, `scripts/test-install.ps1`.

**`docs/`:**
- Purpose: Hold troubleshooting and longer usage notes that should not crowd `README.md`.
- Contains: Workflow philosophy, generated folder examples, and operational troubleshooting.
- Key files: `docs/creative-process-guide.md`, `docs/example-folder-structure.md`, `docs/troubleshooting.md`.

**`examples/`:**
- Purpose: Provide lightweight examples only.
- Contains: Example READMEs for `single` and `mix`.
- Key files: `examples/single/README.md`, `examples/mix/README.md`.

**`.planning/codebase/`:**
- Purpose: Store GSD-generated codebase maps used by future planning and execution commands.
- Contains: `ARCHITECTURE.md`, `STRUCTURE.md`.
- Key files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`.

## Key File Locations

**Entry Points:**
- `README.md`: Human entry guide for install, usage, requirements, docs, and privacy.
- `skills/zk-creative-process/SKILL.md`: Codex skill trigger, routing, hard rules, workflows, and completion checks.
- `scripts/install-skill.ps1`: Main repository-root installer command.
- `scripts/process-reference-video-phase1.ps1`: Single-video workflow wrapper.
- `scripts/process-reference-videos-mix.ps1`: Same-direction multi-video workflow command.
- `scripts/check-environment.ps1`: Environment preflight command.
- `scripts/check-creative-material.ps1`: Generated material validation command.
- `scripts/test-install.ps1`: Smoke test command for script changes.

**Configuration:**
- `.gitignore`: Ignores `.tmp/`, `creative-materials/`, common video formats, and `keyframes-work/`.
- `AGENTS.md`: Repository rules, scope, structure, and required behavior.
- `skills/zk-creative-process/agents/openai.yaml`: UI metadata and default prompt for the skill.
- `skills/zk-creative-process/SKILL.md`: YAML frontmatter includes the skill `name` and `description`.

**Core Logic:**
- `scripts/start-reference-video.ps1`: Single-video deterministic generator and core processing logic.
- `scripts/process-reference-videos-mix.ps1`: Multi-video deterministic generator and shared-analysis skeleton writer.
- `scripts/process-reference-video-phase1.ps1`: Single workflow orchestration and validation wrapper.
- `scripts/check-creative-material.ps1`: Required output shape validation.
- `scripts/install-skill.ps1`: Self-contained package install logic.

**Testing:**
- `scripts/test-install.ps1`: End-to-end smoke test for single workflow generation and validation.
- `scripts/check-environment.ps1`: Preflight environment validation for PowerShell, FFmpeg, FFprobe, and UTF-8 filesystem support.
- `README.md`: Documents Windows skill metadata validation using `.codex\skills\.system\skill-creator\scripts\quick_validate.py`.

**Documentation:**
- `docs/creative-process-guide.md`: Explains script responsibilities, AI responsibilities, single/mix routing, product mapping, and first-stage-only rule.
- `docs/example-folder-structure.md`: Shows expected generated folders for single and mix workflows.
- `docs/troubleshooting.md`: Longer operational notes for FFmpeg, PowerShell execution policy, paths, validation, TODO output, and generated-material privacy.

## Naming Conventions

**Files:**
- PowerShell scripts use lower-kebab names ending in `.ps1`: `scripts/check-creative-material.ps1`, `scripts/process-reference-videos-mix.ps1`.
- Markdown docs use lower-kebab names ending in `.md`: `docs/creative-process-guide.md`, `docs/example-folder-structure.md`.
- Skill metadata uses standard Codex names: `skills/zk-creative-process/SKILL.md`, `skills/zk-creative-process/agents/openai.yaml`.
- Generated product and output files intentionally include Chinese names for user clarity: `product-brief-产品信息.md`, `outputs/reference-video-storyboard-原视频场景变化分镜.md`, `outputs/creative-script-directions-创意脚本方向.md`, `outputs/shared-analysis-同方向素材共性拆解.md`.

**Directories:**
- Skill packages live under `skills/<skill-name>/`: `skills/zk-creative-process/`.
- Bundled skill scripts live under `skills/<skill-name>/scripts/`: `skills/zk-creative-process/scripts/`.
- Repository scripts live under root `scripts/`.
- Long-form docs live under `docs/`.
- Examples are grouped by workflow mode: `examples/single/`, `examples/mix/`.
- Generated material folders use `YYYY-MM-DD-slug-name`: `creative-materials/2026-05-23-dragon-flight-飞龙换场景/`.

**Generated Material Names:**
- Single original video: `original-$Name$extension`.
- Mix copied videos: `video-01-source-name.mp4`, `video-02-source-name.mp4`.
- Contact sheets: `keyframes-reference-storyboard-contact-sheet-$Name.jpg` for single and `keyframes-reference-storyboard-contact-sheet-$Name-video-01.jpg` for mix.
- System folder: `_system-review-系统复查资料/`.
- Temporary frame folder: `keyframes-work/`.

## Where to Add New Code

**New Skill Behavior:**
- Primary contract: `skills/zk-creative-process/SKILL.md`.
- If behavior changes script usage or generated files, update `README.md` and relevant docs in `docs/`.
- If behavior changes script execution, update both `scripts/*.ps1` and matching files in `skills/zk-creative-process/scripts/*.ps1`.

**New PowerShell Script:**
- Development copy: `scripts/<lower-kebab-name>.ps1`.
- Bundled copy: `skills/zk-creative-process/scripts/<lower-kebab-name>.ps1`.
- Documentation: Add usage to `README.md` if it is an entry command; add longer details to `docs/`.

**New Single-Workflow Logic:**
- Wrapper behavior: `scripts/process-reference-video-phase1.ps1` and `skills/zk-creative-process/scripts/process-reference-video-phase1.ps1`.
- Core generation behavior: `scripts/start-reference-video.ps1` and `skills/zk-creative-process/scripts/start-reference-video.ps1`.
- Validation updates: `scripts/check-creative-material.ps1` and `skills/zk-creative-process/scripts/check-creative-material.ps1`.

**New Mix-Workflow Logic:**
- Primary code: `scripts/process-reference-videos-mix.ps1` and `skills/zk-creative-process/scripts/process-reference-videos-mix.ps1`.
- Shared output docs: `docs/example-folder-structure.md` and `docs/creative-process-guide.md`.
- Validation updates: `scripts/check-creative-material.ps1` and `skills/zk-creative-process/scripts/check-creative-material.ps1`.

**New Validation Rule:**
- Primary code: `scripts/check-creative-material.ps1`.
- Bundled copy: `skills/zk-creative-process/scripts/check-creative-material.ps1`.
- Troubleshooting docs: `docs/troubleshooting.md` if the rule can fail for users.

**New Installer Behavior:**
- Primary code: `scripts/install-skill.ps1`.
- Bundled copy: `skills/zk-creative-process/scripts/install-skill.ps1`.
- Entry docs: `README.md`.

**Utilities:**
- Shared helper functions are currently local to each `.ps1` file. Add new helpers locally unless a real cross-script abstraction is introduced in both root and bundled script sets.
- Avoid creating hidden helper dependencies outside `skills/zk-creative-process/`; installed skill users must be able to use the copied skill folder directly.

## Special Directories

**`skills/zk-creative-process/`:**
- Purpose: Installable skill package.
- Generated: No.
- Committed: Yes.

**`skills/zk-creative-process/scripts/`:**
- Purpose: Bundled scripts available after skill installation.
- Generated: No.
- Committed: Yes.

**`scripts/`:**
- Purpose: Repository-level development, testing, and installer entry points.
- Generated: No.
- Committed: Yes.

**`docs/`:**
- Purpose: Longer explanations and troubleshooting.
- Generated: No.
- Committed: Yes.

**`examples/`:**
- Purpose: Lightweight public examples only.
- Generated: No.
- Committed: Yes.

**`creative-materials/`:**
- Purpose: Generated user material folders containing copied videos, keyframes, briefs, outputs, and system review packs.
- Generated: Yes.
- Committed: No; ignored by `.gitignore`.

**`.tmp/`:**
- Purpose: Temporary output from smoke tests and environment checks.
- Generated: Yes.
- Committed: No; ignored by `.gitignore`.

**`keyframes-work/`:**
- Purpose: Temporary frame extraction workspace during script runs.
- Generated: Yes.
- Committed: No; ignored by `.gitignore`.

## Repository-Specific Placement Rules

- Keep `README.md` as the entry guide. Put longer usage explanations in `docs/`.
- Keep source examples lightweight under `examples/`; do not store private creative materials there.
- Keep user-generated videos, generated `creative-materials/`, private ad data, and strategy notes out of git.
- Keep install path friendly for non-programmers: prefer one command, clear next step, and explicit flags for destructive behavior.
- Validate PowerShell syntax after script changes.
- Preserve copy-by-default video handling. Any move behavior must require explicit `-Move`.
- Keep root `scripts/` and bundled `skills/zk-creative-process/scripts/` synchronized.

---

*Structure analysis: 2026-05-27*
