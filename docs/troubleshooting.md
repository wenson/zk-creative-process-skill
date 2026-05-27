# Troubleshooting

## 找不到 FFmpeg

脚本需要同时找到 `ffmpeg` 和 `ffprobe`。

安装方式：

```bash
brew install ffmpeg
```

```powershell
winget install Gyan.FFmpeg
```

```bash
sudo apt install ffmpeg
```

如果已经安装，但不在 PATH 里，可以传完整路径：

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/video.mp4" \
  --slug "test-video" \
  --name "test-video-测试视频" \
  --product-brief-path "./my-product-brief.md" \
  --ffmpeg-path "/opt/homebrew/bin/ffmpeg" \
  --ffprobe-path "/opt/homebrew/bin/ffprobe"
```

## Windows 禁止执行脚本

如果 Windows 阻止执行 PowerShell 脚本，用普通用户打开 PowerShell，然后运行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

也可以只对单次命令绕过执行策略：

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/check-environment.ps1
```

## 路径里有空格或中文

路径要加引号：

```bash
--video-path "/Users/me/Videos/test video 中文.mp4"
```

脚本内部使用真实文件路径，应该支持空格和中文路径。

## skill 校验遇到编码错误

如果 `quick_validate.py` 报 `UnicodeDecodeError`，在当前终端启用 UTF-8：

```bash
PYTHONUTF8=1 python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/zk-creative-process
```

本仓库会生成中文文件名，所以校验时使用 UTF-8 是正常要求。

## 源视频不见了

当前脚本默认复制源视频。原视频会留在原文件夹。

只有命令里用了 `--move`，脚本才会把原视频移动到生成的素材文件夹。

## 长视频处理很慢

默认会抽取一组均匀分布的关键帧。长视频可以先剪到广告片段，或降低帧数：

```bash
--storyboard-frames 8
```

`single` 默认 12 帧，`mix` 默认每个视频 8 帧。可设置范围是 4 到 30。

## 输出里还有 TODO

这是脚本刚生成后的正常状态。脚本只创建骨架文件，后续要由 Codex 填写。

`single` 需要填写：

- `brief.md`
- `outputs/reference-video-storyboard-原视频场景变化分镜.md`
- `outputs/creative-script-directions-创意脚本方向.md`

`mix` 需要填写：

- `brief.md`
- `outputs/shared-analysis-同方向素材共性拆解.md`

如果 `product-brief-产品信息.md` 仍有 `TODO`，产品映射必须标记为待补充。

## 产品映射看起来很泛

先填写 `product-brief-产品信息.md`，或通过 `--product-brief-path` 传入已有产品 brief。

没有产品上下文时，Codex 只能拆解参考视频并列出缺失问题。它不应该编造玩法、资产、受众或合规限制。

## 不要提交生成素材

生成目录可能包含源视频和派生图片，不要提交到 git。

仓库的 `.gitignore` 已经忽略：

- `creative-materials/`
- `.tmp/`
- 常见视频文件格式
