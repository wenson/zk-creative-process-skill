# Troubleshooting

## FFmpeg Not Found

The scripts need both `ffmpeg` and `ffprobe`.

Install options:

```bash
brew install ffmpeg
```

```powershell
winget install Gyan.FFmpeg
```

```bash
sudo apt install ffmpeg
```

If FFmpeg is installed but not on PATH, pass explicit paths:

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/video.mp4" \
  --slug "test-video" \
  --name "test-video-测试视频" \
  --product-brief-path "./my-product-brief.md" \
  --ffmpeg-path "/opt/homebrew/bin/ffmpeg" \
  --ffprobe-path "/opt/homebrew/bin/ffprobe"
```

## PowerShell Script Execution Is Disabled

If Windows blocks script execution, run PowerShell as your normal user and set:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Or run one command with bypass on Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/check-environment.ps1
```

## Paths With Spaces Or Non-English Characters

Use quoted paths:

```bash
-VideoPath "/Users/me/Videos/test video.mp4"
```

The scripts use literal filesystem paths internally and should support spaces and non-English characters.

## Skill Validation Fails On Windows Encoding

If `quick_validate.py` fails with a `UnicodeDecodeError`, enable UTF-8 for that terminal session:

```bash
PYTHONUTF8=1 python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/zk-creative-process
```

This repository intentionally uses Chinese filenames in generated analysis files, so UTF-8 validation is expected.

## Source Video Disappeared

Current scripts copy source videos by default. Originals stay in their original folder.

If a source video was moved, check whether the command used `--move`. That flag deliberately moves originals into the generated material folder.

## Long Videos Are Slow

The default extracts 12 selected frames plus intermediate frames. For very long videos, first trim to the ad segment or lower the frame count:

```bash
--storyboard-frames 8
```

## Output Contains TODO

This is expected immediately after script setup. The script creates skeleton files. Codex should then fill:

- `product-brief-产品信息.md`
- `outputs/reference-video-storyboard-原视频场景变化分镜.md`
- `outputs/creative-script-directions-创意脚本方向.md`

For a `mix` folder, Codex should fill:

- `outputs/shared-analysis-同方向素材共性拆解.md`

## Product Mapping Looks Generic

Fill `product-brief-产品信息.md` or pass an existing file with `--product-brief-path`.

Without product context, Codex should only deconstruct the reference video and list missing product questions. It should not invent gameplay, assets, audience, or compliance constraints.

## Do Not Commit Generated Materials

Generated folders may include source videos and derived frames. Keep them out of git. This repository's `.gitignore` already ignores `creative-materials/`, `.tmp/`, and common video file extensions.
