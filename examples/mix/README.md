# Mix Example

Use `mix` when several videos share the same creative direction.

Run:

```bash
./scripts/process-reference-videos-mix.sh \
  --video-paths "/Users/me/Videos/hook-1.mp4" "/Users/me/Videos/hook-2.mp4" "/Users/me/Videos/hook-3.mp4" \
  --slug "animal-hooks" \
  --name "animal-hooks-动物钩子" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` is optional. If omitted, fill the generated `product-brief-产品信息.md` before asking Codex to map the shared direction into your own product.

Then ask Codex:

```text
$zk-creative-process mix ./creative-materials/2026-05-23-animal-hooks-动物钩子
```

The output should be one direction-level folder, not three independent single-video folders.
