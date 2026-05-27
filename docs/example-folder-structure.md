# Example Folder Structures

下面是脚本生成后的典型结构。日期来自运行当天，`slug` 和 `name` 来自命令参数。

## Single

一个参考视频对应一个素材文件夹：

```text
creative-materials/2026-05-23-dragon-flight-飞龙换场景/
  original-dragon-flight-飞龙换场景.mp4
  keyframes-reference-storyboard-contact-sheet-dragon-flight-飞龙换场景.jpg
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

根目录文件用途：

- `original-*.mp4`：复制进来的参考视频。
- `keyframes-reference-storyboard-contact-sheet-*.jpg`：关键帧联系表，供人和 AI 快速看场景变化。
- `brief.md`：素材任务入口。
- `product-brief-产品信息.md`：用户自己产品的信息。
- `outputs/`：AI 要填写的人读分析文档。

## Mix

多个同方向视频对应一个方向级素材文件夹：

```text
creative-materials/2026-05-23-animal-hooks-动物钩子/
  video-01-hook-a.mp4
  video-02-hook-b.mp4
  video-03-hook-c.mp4
  keyframes-reference-storyboard-contact-sheet-animal-hooks-动物钩子-video-01.jpg
  keyframes-reference-storyboard-contact-sheet-animal-hooks-动物钩子-video-02.jpg
  keyframes-reference-storyboard-contact-sheet-animal-hooks-动物钩子-video-03.jpg
  brief.md
  product-brief-产品信息.md
  outputs/
    shared-analysis-同方向素材共性拆解.md
  _system-review-系统复查资料/
    ai-input-pack.md
    frame-index.json
    run-manifest.json
    video_metadata.json
```

`mix` 不应该拆成多个独立 `single` 文件夹。它要回答的是：这些视频共同验证什么方向、有哪些差异、哪些结构可复用到自己的产品。
