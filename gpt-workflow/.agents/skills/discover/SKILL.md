---
name: discover
description: Research discovery, frontier literature, data assessment, and evidence-based brainstorming for economics. Supports interview, lit, data, ideate, brainstorm, and frontier.
---

# Discover

根据当前请求中的目标、材料和参数执行。从问题和机制出发，帮助研究者判断值得研究什么、现有证据支持什么，以及下一步如何区分解释。默认中文，保留必要英文术语。

先读已有 `research/PROJECT_BRIEF.md` 和相关输入；按需读 [研究协作](../../../references/research-collaboration.md) 与 [领域资料](../../../references/domain-profile.md)。没有项目事实就标明未知，不把领域资料中的例子当成研究设定。

## 路由

| 用法 | 工作 | 产物 |
|---|---|---|
| `$discover [topic]` | 根据上下文进入 brainstorm；信息不足时只补最关键的问题 | 讨论及必要的 brief 更新 |
| `$discover interview [topic]` | 对话澄清问题、机制、证据资源和最值得验证的未知 | `research/PROJECT_BRIEF.md` |
| `$discover lit [topic]` | `librarian` 搜索综合；重要贡献或覆盖结论交 `librarian-critic` 复核 | `research/literature.md`，核实的 bibliography 条目 |
| `$discover frontier [topic]` | 本次按检索日期核验最近相关版本、直接竞争论文、反证及相邻文献 | 文献地图与前沿变化说明 |
| `$discover data [requirements]` | `data-explorer` 查数据；关键可行性判断交 `explorer-critic` | `research/data-assessment.md` |
| `$discover ideate [topic]` | 兼容模式，执行 brainstorm | 候选及最小检验 |
| `$discover brainstorm [topic]` | 前沿证据、竞争机制、跨领域连接及下一步建议 | 讨论；必要时链接专题笔记 |

独立文献和数据子任务可以并行，依赖结果的综合顺序完成。小范围问题直接处理即可；没有子 agent 工具时明确做串行复核，不声称已完成独立审查。审查路径统一为 `quality_reports/reviews/YYYY-MM-DD_<task>.md`。

## 对话与研究设定

先利用现有上下文，不逐条做问卷。需要时围绕一个具体缺口提问：现象是什么、为何重要、什么机制、什么会使我们改变看法、已有何种证据资源。不要求每个新项目预先给出识别策略或期待显著的方向。

将已知事实、研究者判断和自己的候选分开。只有经研究者确认的重大研究选择写为 `research/DECISIONS.md` 的 `approved`；AI 推荐写 `proposed`。初期可以先交付可讨论的 brief，不因缺数据/文献就虚构设定，也不等待所有信息齐备才开始检索。

## 文献与前沿

优先读取提供的论文、项目已有 bibliography（检查实际文件名），再查论文原文、作者/机构页面、期刊与工作论文平台。沿关键论文向前/向后追引，同时搜索不同机制、相反结果和相邻领域。按相关性和证据质量选择；期刊层次、作者名气和 working paper 比例不作筛除规则。

每篇重要文献记录题名、作者、版本与日期、稳定链接、检索日期、读取范围（全文/指定章节/摘要/二手提及/未核实）、问题/机制、数据与识别、相关发现和局限。关系类别统一为：`direct`（直接竞争）、`adjacent`（相邻问题）、`mechanism`（机制基础）、`method`（方法）、`context`（制度/背景）；可多选，不用方向易混的数字。

对同一研究的工作论文和期刊版去重，说明实质差异；原则上引用实际支撑当前主张的版本。无法核实的文献留在待核实清单，不猜作者、DOI、系数或 BibTeX。只读摘要不声称理解全文识别或写作风格。新颖性写“在本次检索范围内未找到……”，给出范围和遗漏风险；无法联网时标 `NOT_RUN`，不要声称前沿已核验。

## 数据与创新

数据评估按测量、选择、外推、识别兼容性、实际访问与处理成本展开，明确“目录可见”和“已获得可用数据”的差别。保留未选数据及重开条件，不用字母等级代替说明。

每轮实质 brainstorm 根据讨论给出首选探索，必要时增加替代或远距离连接：机制、新意所依据的文献、可能推翻它的证据、数据需求与最小检验。创新不限于增加异质性或换数据；可以来自市场边界、组织安排、动态调整、信息摩擦或测量对象的变化。候选保持候选，执行仍围绕已授权主线。

交付时说清刚学到什么、主要未知和下一步为何值得做。陌生理论/方法给直觉与学习入口，可转 `$learn`；重要发现更新证据账，输入变化使旧判断标 `STALE`。详细状态规则见研究协作，不打综合分、不因模板自动推进到下一阶段。
