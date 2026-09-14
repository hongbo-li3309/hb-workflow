---
name: write
description: Draft, diagnose, and revise economics writing in Chinese or English, adapting academic papers and policy reports to readers, evidence, and field exemplars.
---

# Write

保留 `$write` 及 `humanize`、`style-guide` 等原入口。自然语言参数同样有效；从任务或现稿推断语言、体例和章节，避免不必要访谈。默认中文交流，稿件语言按目标读者决定。

## 先确定稿件与证据

1. 读取用户指定主稿和相关部分；没有指定时按项目已确认的主稿路径查找。不要把所有项目都改为 `paper/main.tex`。
2. 有则读取 `research/PROJECT_BRIEF.md` 及与本段有关的 `research/EVIDENCE_LEDGER.md` 条目；再按需读 `research/literature.md`、`research/theory.md`、`research/strategy.md` 和实际输出，不预装全目录。
3. 从 `references/writing-guide.md` 选中英论文或政策体例，读取 `personal-style-guide.md` 的已确认偏好。领域写法从 `writing-exemplars.md` 选合适样本，新领域或体例补查真实原文。
4. 辨认研究类型：因果实证、描述／测量、结构／量化模型、纯理论／方法、理论与实证结合。无代码、无数据或未完成证明都可以起草相应部分，清晰标记缺口。

## 模式

| 入口 | 行为 |
|---|---|
| `intro / data / strategy / model / results / conclusion / abstract` | 起草相应部分；结构随研究问题和研究类型调整 |
| `full` | 在已授权范围完成连贯初稿，汇总待判断项；不为每节强制暂停 |
| `outline` | 给出主线、各节要解决的问题、已有证据和缺口；替代组织方式仅在有判断价值时提供 |
| `edit / humanize [file]` | 先修逻辑与重复，再修句子；保留必要术语和限定，不用禁词替换改变研究含义 |
| `diagnose [file]` | 只诊断结构、主张与证据、读者障碍；给定位、理由和建议，不修改主稿 |
| `style-guide [file/dir]` | 从用户指定满意样稿或修改提炼候选观察，更新个人风格参考，不编造偏好 |

摘要可以根据已有研究计划起草，但须标明是拟稿且结论待定。不能把未来预期结果写成已完成发现。`model` 对纯理论开放，不要求先有实证结果。

## 起草与修订

小任务直接完成；大篇幅起草或需要独立角色时通过 当前可用的子 agent 能力 委派 `writer`，交代主稿路径、输出路径、语言体例、目标读者、证据范围和授权范围。重大改稿可追加 `writer-critic` 的独立审查；critic 返回报告，由主会话保存，不能改稿。

写作顺序：读者要理解什么 → 主张与证据 → 章节段落作用 → 句子节奏和用词 → 格式。借鉴 exemplar 的论证动作，并说明实际读取范围；不用固定句长、词数比例或作者名气决定质量。

编辑按 `references/protocols/revision.md` 处理指定主稿、另存版本和 diff。沿用 Word、LaTeX、Markdown 等已有格式；工具无法保留格式或修订记录时，先交付可审阅的文字修改及定位，明确未完成的格式工作，不能声称格式已保留。

新稿按项目约定存放；没有约定可用 `paper/`。占位直接写 `[RESULT PENDING: 需要的输出]`、`[SOURCE UNVERIFIED: 待核主张]` 或 `[PROOF PENDING: 缺失步骤]`，不填示意数字伪装结果。已有数据、模型或代码变化后，将相关旧证据标 `STALE`，不能直接复用为当前主张。

## 核验与交付

核对本次变更涉及的数字、单位、基准组、样本、引用和证据强度。参考文献“存在”与“支持这句话”分别核对；前趋势不显著不能证实平行趋势，相关性不能因润色变成因果。

检查状态仅用 `PASS / FAIL / NOT_RUN / NOT_APPLICABLE`，说明证据与适用范围。编译由有执行权限的 writer 或 verifier 运行；未运行就标 `NOT_RUN`，文本静态审查不能替代编译或视觉检查。

交付稿件链接、修改理由、保留的未决项和核验范围。正式审查保存 `quality_reports/reviews/YYYY-MM-DD_<task>.md`，同日重名加后缀。必要时用少量改句解释写作判断，让 Hongbo 能继续介入；不自动更换核心研究问题或把建议记成作者决定。
