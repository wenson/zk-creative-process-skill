# ZK Creative Process Skill

`zk-creative-process` 是一个 Codex skill，用来把游戏广告参考视频整理成可复查、可继续创作的素材文件夹。

核心流程：

```text
参考视频拆解 -> product-brief-产品信息.md -> 映射到自己的产品 -> 产出创意方向池
```

脚本只负责确定性的素材处理。创意判断、产品映射和脚本方向由 Codex 在生成文件后继续完成。

## 会生成什么

单视频 `single` 模式会生成：

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

多视频 `mix` 模式会把同方向视频放进一个方向级文件夹，并生成：

```text
outputs/shared-analysis-同方向素材共性拆解.md
```

`product-brief-产品信息.md` 是从参考素材映射到自己产品的桥。它为空或仍有 `TODO` 时，Codex 只能拆解参考视频，并列出缺失问题，不能编造产品事实。

## 安装

在仓库根目录运行：

```bash
./scripts/install-skill.sh
```

如果已经安装过，安装器会停止。需要明确选择：

```bash
./scripts/install-skill.sh --backup
./scripts/install-skill.sh --force
```

`--backup` 会备份旧 skill。`--force` 会替换旧 skill。

Windows 用户可以运行同名 PowerShell 脚本：

```powershell
./scripts/install-skill.ps1
```

## 使用方式

先检查环境：

```bash
./scripts/check-environment.sh
```

单个参考视频：

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/reference.mp4" \
  --slug "dragon-flight" \
  --name "dragon-flight-飞龙换场景" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

同方向多视频：

```bash
./scripts/process-reference-videos-mix.sh \
  --video-paths "/Users/me/Videos/hook-1.mp4" "/Users/me/Videos/hook-2.mp4" \
  --slug "animal-hooks" \
  --name "animal-hooks-动物钩子" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` 可选。不传时，脚本会生成空的 `product-brief-产品信息.md` 模板。

脚本默认复制源视频，原文件会留在原位置。只有明确传 `--move` 时，才会移动原视频。

## 在 Codex 里调用

单视频：

```text
用 $zk-creative-process single 处理这个视频：/Users/me/Videos/reference.mp4
```

同方向多视频：

```text
用 $zk-creative-process mix 把这几个同方向视频合并分析：/Users/me/Videos/hook-1.mp4, /Users/me/Videos/hook-2.mp4
```

如果已经先跑过脚本，也可以把生成的素材文件夹给 Codex：

```text
$zk-creative-process single ./creative-materials/2026-05-23-dragon-flight-飞龙换场景
```

## 要求

- Python 3.10+。
- `ffmpeg` 和 `ffprobe` 在 PATH 中可用，或通过 `--ffmpeg-path`、`--ffprobe-path` 传入完整路径。

验证生成的素材文件夹：

```bash
./scripts/check-creative-material.sh --material-dir "./creative-materials/YYYY-MM-DD-slug-name"
```

验证 skill 元数据：

```bash
PYTHONUTF8=1 python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/zk-creative-process
```

端到端安装测试：

```bash
./scripts/test-install.sh
```

## 文档

- [创意流程说明](docs/creative-process-guide.md)
- [文件夹结构示例](docs/example-folder-structure.md)
- [常见问题](docs/troubleshooting.md)
- [单视频示例](examples/single/README.md)
- [多视频示例](examples/mix/README.md)

## 致谢

感谢原作者 [ZK-JackUltra/zk-creative-process-skill](https://github.com/ZK-JackUltra/zk-creative-process-skill) 提供的创意流程基础。

## 隐私与提交边界

- 不要提交客户视频、竞品视频、广告数据、产品策略、已填写的产品 brief 或生成的 `creative-materials/`。
- `.gitignore` 默认忽略常见视频格式、`.tmp/` 和生成目录。
- 仓库脚本是通用工具，不依赖任何私有项目目录。
