---
name: talk
description: Create, audit, or compile economics presentations in Beamer or Quarto RevealJS, matching audience and time while preserving evidence and uncertainty.
---

# Talk

保留现有三种模式、四类场合及 Beamer／Quarto 支持。已有幻灯主稿或指定格式优先；新稿默认 Beamer。报告语言、听众和时长可从任务推断，只有实际缺失且影响交付时才澄清。

## Create

读取主稿、`research/PROJECT_BRIEF.md` 和涉及结果的 `research/EVIDENCE_LEDGER.md` 及真实图表。研究尚早也可做 idea talk，明确假说、拟设计和未完成证据；不得把计划包装成发现。稿件与输出有冲突时先标出，不把旧主稿当作数值真值。

| 场合 | 组织重点 |
|---|---|
| `job-market` | 核心贡献、经济理解和证据可信度；预留讨论，技术细节有可到达的 backup |
| `seminar` | 让听众理解问题、机制和关键判别证据；围绕主线组织讨论 |
| `short` | 集中一个问题及最有信息的结果或命题，简要说明其成立条件 |
| `lightning` | 听众能复述问题、核心洞见及下一步；不把未做的研究讲成结果 |

上述不是强制页数或时长。按实际演讲时间、预期提问和复杂图表安排内容，必要时估算讲述时间，标明尚未排练。

通过 当前可用的子 agent 能力 按需委派 `storyteller`。每页有清楚的中心问题或判断；具体数字、方向和限制可追溯到证据。表格能帮助判断时可以放正文，不机械地全部藏到 backup。新证据尚未写入论文时可以使用，但标明其状态和来源，并记录与主稿待同步事项。

沿用项目主题、引用及输出路径。新稿无约定时，Beamer 用 `paper/talks/<format>_talk.tex`，Quarto 用 `paper/quarto/<format>_talk.qmd`。大改按 `references/protocols/revision.md` 另存并提供差异。speaker notes 可存讲解、限定和预期问题；核心条件不能只藏在备注中。

## Compile 与 Audit

使用项目现有构建设置；无设置时先确认可用引擎与中文字体，再选择命令。例如在文件所在目录运行：

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error seminar_talk.tex
quarto render seminar_talk.qmd
```

命令只用于对应格式，中文 Beamer 可按已配置引擎使用 `-xelatex` 或 `-lualatex`。保留实际退出码和完整日志；不能用 `| tail` 的成功掩盖编译失败。工具缺失为 `NOT_RUN`，不要擅自声称已生成 PDF。

`audit` 先分清能否查看渲染结果。有 PDF／截图或浏览器预览时检查真实页面；只有源文件时仅做静态审查并标记视觉检查 `NOT_RUN`。检查溢出、投影可读性、图例与轴、颜色／灰度、叠层与导航，以及数字和口径；编译成功不代表版面可读。

大幅新建、重要演讲或用户要求审查时委派 `storyteller-critic` 独立评议。critic 不改稿；由 creator 修正证实的问题，再验证受影响部分。不为每个小改动机械调用完整审查链。

## 交付

提供源文件、实际生成的 PDF／HTML、页数与用途、编译和视觉检查的 `PASS / FAIL / NOT_RUN / NOT_APPLICABLE`、未解决内容。审查报告保存 `quality_reports/reviews/YYYY-MM-DD_<task>.md`；需要后缀时追加，保留历史。`STALE` 的旧结果不得当作当前已核验证据。
