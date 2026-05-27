# Mix Example

`mix` 用于多个同方向视频。它会生成一个方向级素材文件夹，用来分析共性、差异和统一测试目标。

运行：

```bash
./scripts/process-reference-videos-mix.sh \
  --video-paths "/Users/me/Videos/hook-1.mp4" "/Users/me/Videos/hook-2.mp4" "/Users/me/Videos/hook-3.mp4" \
  --slug "animal-hooks" \
  --name "animal-hooks-动物钩子" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` 可选。不传时，先填写生成的 `product-brief-产品信息.md`，再让 Codex 把共性方向映射到自己的产品。

然后让 Codex 继续：

```text
$zk-creative-process mix ./creative-materials/2026-05-23-animal-hooks-动物钩子
```

预期输出重点：

- 一个方向级文件夹。
- 每个视频一张关键帧联系表。
- `outputs/shared-analysis-同方向素材共性拆解.md` 作为共享分析。

不要把同方向素材拆成多个独立 `single` 文件夹。
