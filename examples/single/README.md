# Single Example

Run:

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/reference.mp4" \
  --slug "dragon-flight" \
  --name "dragon-flight-飞龙换场景" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` is optional. If omitted, fill the generated `product-brief-产品信息.md` before asking Codex for product-specific script directions.

Then ask Codex:

```text
$zk-creative-process single ./creative-materials/2026-05-23-dragon-flight-飞龙换场景
```
