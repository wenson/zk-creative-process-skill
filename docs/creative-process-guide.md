# Creative Process Guide

这份文档说明 `zk-creative-process` 的工作边界。给新素材时，先用脚本把视频变成稳定的文件结构，再让 Codex 进行创意判断。

## 基本思路

流程分成两层：

- 脚本处理确定性的事情。
- AI 处理需要理解和判断的事情。

脚本负责：

- 创建素材文件夹
- 复制或移动源视频
- 提取视频元数据
- 提取关键帧
- 生成关键帧联系表
- 生成运行清单
- 创建 Markdown 骨架文件

AI 负责：

- 理解场景内容
- 拆解 opening hook
- 分析冲突、压力和节奏
- 提炼可迁移结构
- 根据产品 brief 做真实映射
- 生成创意方向池和测试假设

## 文件夹结构

```text
material-folder/
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

根目录给人阅读。`_system-review-系统复查资料/` 给自动化和未来 AI 复查使用。

`product-brief-产品信息.md` 是必须检查的产品信息入口。它为空或仍有 `TODO` 时，AI 应该拆解参考视频，并提出缺失问题，而不是编造玩法、受众或素材条件。

## single 和 mix

默认使用 `single`。只有用户明确说明多个视频属于同方向、同 hook 类型或同批素材时，才使用 `mix`。

`single` 的输出重点是一个参考视频的场景变化和多个可测试方向：

```text
outputs/reference-video-storyboard-原视频场景变化分镜.md
outputs/creative-script-directions-创意脚本方向.md
```

`mix` 的输出重点是同方向素材的共性、差异和统一测试目标：

```text
outputs/shared-analysis-同方向素材共性拆解.md
```

`mix` 文件夹应该包含所有源视频、每个视频对应的关键帧联系表、一个共享 `brief.md` 和一个共享分析文件。

## 产品映射

参考视频拆解和产品映射不是一回事。

产品 brief 应该覆盖：

- 产品品类、受众、市场、平台和投放渠道
- 核心玩法循环和前 30 秒真实体验
- 能把 hook 真实连接到玩法的机制
- 可用资产、制作限制和合规限制
- 创意测试目标和成功指标

产品信息不足时，产品映射保持待补充。可以完成参考视频拆解，但不能把参考视频里的表层元素直接说成用户产品里存在的功能。

## 第一阶段边界

第一阶段不创建生产分镜、生成图 prompt 或资产生成文件夹。

第一阶段只产出方向池，让人选择：

- 哪个 hook 值得测试
- 哪个冲突机制适合自己的产品
- 哪些素材或产品信息还缺失
- 哪些方向风险太高

只有用户选定方向后，才进入生产脚本、分镜 prompt 和素材生成阶段。
