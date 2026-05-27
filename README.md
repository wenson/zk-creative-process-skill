# ZK Creative Process Skill

A Codex skill and cross-platform toolkit for processing game-ad reference videos into clean creative-analysis folders.

Core workflow:

```text
reference-video deconstruction -> product-brief-产品信息.md -> map into your own product
```

## What It Creates

```text
creative-materials/YYYY-MM-DD-slug-name/
  original-name.mp4
  keyframes-reference-storyboard-contact-sheet-name.jpg
  brief.md
  product-brief-产品信息.md
  outputs/
    reference-video-storyboard-原视频场景变化分镜.md
    creative-script-directions-创意脚本方向.md
  _system-review-系统复查资料/
    ai-input-pack.md
    frame-index.json
    run-manifest.json
    video_metadata.json
```

`product-brief-产品信息.md` is the bridge from reference analysis to your own product. If it is empty, Codex should not invent product facts; mapping stays pending.

## Install

Run from this repository root:

```bash
./scripts/install-skill.sh
```

If the skill already exists, the installer stops. Choose explicitly:

```bash
./scripts/install-skill.sh --backup
./scripts/install-skill.sh --force
```

`--backup` keeps the old installed skill. `--force` replaces it.

## Use In Codex

Single reference video:

```text
用 $zk-creative-process single 处理这个视频：/Users/me/Videos/video.mp4
```

Same-direction batch:

```text
用 $zk-creative-process mix 把这几个同方向视频合并分析：/Users/me/Videos/video-1.mp4, /Users/me/Videos/video-2.mp4
```

The scripts copy source videos by default. Originals stay where they are. Use `--move` only when you deliberately want originals moved into the material folder.

## Requirements

- Python 3.10+.
- FFmpeg and FFprobe available on PATH, or pass `--ffmpeg-path` and `--ffprobe-path`.

Check environment:

```bash
./scripts/check-environment.sh
```

Validate generated material:

```bash
./scripts/check-creative-material.sh --material-dir "./creative-materials/YYYY-MM-DD-slug-name"
```

Validate skill metadata:

```bash
PYTHONUTF8=1 python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/zk-creative-process
```

## Docs

- [Creative process guide](docs/creative-process-guide.md)
- [Folder structure](docs/example-folder-structure.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Single example](examples/single/README.md)
- [Mix example](examples/mix/README.md)

## Privacy

- Do not commit customer videos, competitor videos, ad data, product strategy, filled product briefs, or generated `creative-materials/`.
- `.gitignore` ignores common video formats, `.tmp/`, and generated folders by default, except the bundled public sample `shower.mp4`.
- The included scripts are generic and do not depend on a private project folder.
