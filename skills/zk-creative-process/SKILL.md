---
name: zk-creative-process
description: >
  Generic creative material processing for game ad reference videos. Use when
  the user invokes $zk-creative-process, single, or mix to process new
  reference videos, generate keyframe contact sheets, create material folders,
  create product-brief-产品信息.md, analyze game-ad hooks, map reference
  structures into the user's own product, or build story-direction pools.
  Supports single for one reference video and mix for multiple same-direction
  videos analyzed in one folder.
---

# ZK Creative Process

这个 skill 用来把游戏广告参考视频整理成清晰的素材文件夹，然后基于素材做参考视频拆解、产品映射和创意方向池。

先跑脚本，再写分析。脚本负责视频复制、元数据、关键帧、文件夹和骨架文档；AI 负责理解画面、拆解结构、判断可迁移点和生成方向池。

## 模式选择

- `single`：一个参考视频，一个素材文件夹。
- `mix`：多个同方向、同钩子或同批次视频，一个方向级素材文件夹。

用户只给一个视频，或没有明确说多个视频属于同方向时，默认用 `single`。

用户说多个视频是一个方向、一个 hook 类型、一批素材、需要合并分析时，用 `mix`。

## 硬规则

- 先运行代码生成素材结构，再做 AI 分析。
- 默认复制源视频。只有用户明确要求移动原文件时，才使用 `--move`。
- 参考视频和关键帧联系表放在素材文件夹根目录。
- 产品信息放在 `product-brief-产品信息.md`。
- 元数据、帧索引、运行清单和 AI 输入包放在 `_system-review-系统复查资料/`。
- 产品映射必须基于 `product-brief-产品信息.md`。如果产品信息缺失或仍有 `TODO`，不要编造产品事实，只列出缺失问题，并标记产品映射待补充。
- 第一阶段只产出故事方向池。用户选定方向前，不创建生产分镜、prompt 或 `script-*` 文件夹。
- 区分选择和完成：选择只记录选中的方向；完成才归档和清理最终生产资产。
- 人读的文件结论和优先级在前，细节在后。

## single 工作流

在仓库根目录，或安装后的 skill `scripts/` 目录运行：

```bash
./scripts/process-reference-video-phase1.sh \
  --video-path "/Users/me/Videos/reference.mp4" \
  --slug "short-slug" \
  --name "english-name-中文说明" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`--product-brief-path` 可选。不传时，脚本会生成空的 `product-brief-产品信息.md` 模板。

然后读取：

- `_system-review-系统复查资料/ai-input-pack.md`
- `_system-review-系统复查资料/frame-index.json`
- `_system-review-系统复查资料/video_metadata.json`
- `keyframes-reference-storyboard-contact-sheet-*.jpg`
- `product-brief-产品信息.md`

需要填写：

- `brief.md`
- `outputs/reference-video-storyboard-原视频场景变化分镜.md`
- `outputs/creative-script-directions-创意脚本方向.md`

## mix 工作流

多个同方向视频要创建一个方向级文件夹，不要拆成多个单视频文件夹：

```bash
./scripts/process-reference-videos-mix.sh \
  --video-paths "/Users/me/Videos/video-1.mp4" "/Users/me/Videos/video-2.mp4" \
  --slug "shared-direction" \
  --name "shared-direction-同方向说明" \
  --base-dir "./creative-materials" \
  --product-brief-path "./my-product-brief.md"
```

`brief.md` 应该说明所有视频、共性主题、差异点、可迁移结构和统一测试目标。

需要填写：

- `brief.md`
- `product-brief-产品信息.md`
- `outputs/shared-analysis-同方向素材共性拆解.md`

## 产品映射要求

把参考结构转成用户自己产品的脚本前，先检查 `product-brief-产品信息.md`。

必需产品信息：

- 产品或游戏品类、受众、市场、平台和投放渠道
- 核心玩法循环和前 30 秒真实体验
- 能真实连接 hook 与玩法的机制
- 可用视觉资产和制作限制
- 必须展示、必须避免、合规限制和成功指标

如果这些信息缺失，输出简短的缺失信息清单。参考视频拆解可以继续完成，但不要声称产品映射已完成。

## 输出要求

两种模式都要分析：

- 场景推进
- 开头 hook
- 冲突和压力来源
- 视觉语言和剪辑节奏
- BGM、音效、旁白和字幕
- 可迁移结构与不可照搬的表层风格
- 如何桥接到真实玩法或产品价值

每个故事方向应包含：

- 核心假设
- hook
- 故事前提
- 冲突和触发机制
- 产品桥接
- 产品映射适配度和缺失信息
- 可扩展变体
- 测试指标
- 风险
- 需要人决策的问题

## 收尾检查

回复前确认：

- 使用的是 `single` 还是 `mix`。
- 已先运行代码生成素材结构，再做 AI 写作。
- 素材文件夹路径明确。
- `_system-review-系统复查资料/` 包含元数据、帧索引、运行清单和 AI 输入包。
- 根目录包含参考视频、关键帧联系表、`brief.md`、产品 brief 和 `outputs/`。
- 产品映射是已完成，还是因为产品信息缺失而待补充。
- 用户选方向前，没有创建生产文件夹。
