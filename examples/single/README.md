# Single Example

`single` 用于一个参考视频。它会生成一个素材文件夹，并准备两个 AI 要填写的输出文档。

运行：

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/reference.mp4" \
  --slug "dragon-flight" \
  --name "dragon-flight-飞龙换场景" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` 可选。不传时，先填写生成的 `product-brief-产品信息.md`，再让 Codex 做产品相关脚本方向。

然后让 Codex 继续：

```text
$zk-creative-process single ./creative-materials/2026-05-23-dragon-flight-飞龙换场景
```

预期输出重点：

- `outputs/reference-video-storyboard-原视频场景变化分镜.md`：拆解参考视频场景变化。
- `outputs/creative-script-directions-创意脚本方向.md`：给出可测试的故事方向池。

用户选定具体方向前，不创建生产分镜或 prompt 文件夹。
