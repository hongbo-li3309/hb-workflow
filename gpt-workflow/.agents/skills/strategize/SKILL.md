---
name: strategize
description: Build economic mechanisms, identification strategies, pre-analysis plans, formal theory, or a coherent research spine. Supports empirical, structural, descriptive, and theory projects.
---

# Strategize

根据当前请求中的目标、材料和参数执行。先说清经济问题与机制，再选择能回答问题的对象、假设、数据和方法。默认中文，公式与英文术语按需使用。

读取相关的 `research/PROJECT_BRIEF.md`、`research/EVIDENCE_LEDGER.md`、`research/DECISIONS.md` 及用户给定材料；不要求不存在的文件先齐备。按需读取 [研究协作](../../../references/research-collaboration.md)、[方法参考](../../../references/research-methods.md) 和领域资料。简短说明关键已知、未知和采用的假设，不写重复的“已读证明”。

## 模式

| 模式 | 执行与产物 |
|---|---|
| 默认 / `strategy` | `strategist` 制作 `research/strategy.md`；重要设计经 `strategist-critic` 审查 |
| `mechanism` | `theorist` 用最小模型解释机制、竞争解释和可检验预测，写 `research/theory.md` |
| `theory` | `theorist` 处理经济理论或计量理论，`theorist-critic` 审关键证明；按现有主稿格式交付 |
| `spine` / `focus` | 综合结果和反证，更新 brief 中的当前主线；提出需要研究者判断的重大转向 |
| `pap` | 基于已知设定制作 `research/pre-analysis-plan.md`，保留未定项与偏离记录 |
| `pap interactive` | 兼容原用法，仅就缺失的关键设定对话澄清，再起草 PAP |

没有可用子 agent 时串行处理并说明独立性限制。审查写 `quality_reports/reviews/YYYY-MM-DD_<task>.md`，按实际检查用 `PASS` / `FAIL` / `NOT_RUN` / `NOT_APPLICABLE`；输入改变旧结果为 `STALE`。

## 策略内容

围绕一个清楚问题比较有实质差别的路线，分别解释：目标对象、可用变化、关键识别假设、主要威胁、所需数据、实现与学习成本、最有价值的检验。推荐的理由可审阅，不让方法名或熟悉程度替研究者选择。

实证策略至少说明观测单位、主样本、处理和比较、时间结构、estimand、估计式/伪代码、推断方式及潜在失效情形。稳健性每项针对具体威胁；零结果和反常符号有解释位置。描述/测量研究不强加因果承诺；结构研究区分参数识别、估计、外部校准、预测与反事实，解释额外假设换来了什么。

重大主样本、主规格、estimand 或核心问题变化写入 `research/DECISIONS.md` 为 `proposed`，准备具体推荐供研究者判断；已有授权内的实现继续，不因新阶段重复确认。初稿缺条件时明确条件性建议，不能把假定政策、数据访问或变量可得性当事实。

## 机制、理论与学习

实证论文也可用 toy model，纯理论论文无需先有数据或代码。说明参与者、目标、选择、约束、时序与均衡/决策概念；从能澄清问题的最小模型开始，必要复杂度才加入。

推导应连接经济直觉、命题条件、比较静态和可观测含义。正式定理写清条件、证明和边界，数值检验不能替代证明。难点分层解释，主动提供可学习的新工具。模型解释与识别论证分别成立才可共同支持因果主张；一个拟合良好的模型不会自动验证机制。

`spine`（同义 `focus`）模式将每条主要结果归到支持、反驳或尚不能区分的机制，保留不方便的证据；优先建议最能改变判断的下一步。收敛是减少无信息分支，不能删反证来维护故事。

## PAP 与登记

PAP 覆盖问题与设计、干预/分配或识别来源、主/次结果与测量、样本/排除/流失、估计与推断、异质性、多重检验、功效/MDE 的假设与敏感性、数据/软件、时间及偏离记录。根据真实研究类型取舍，不机械填全模板。

区分 registry registration、平台认定的 preregistration、分析计划冻结时间以及研究者何时看过数据/结果。记录真实日期和已有知识；后验计划不能追溯写成预先承诺。AEA RCT Registry 允许登记，干预开始前登记才标为 pre-registered；字段和资格以当次官方规则为准。OSF/EGAP 等也先核验适用平台及当前规则，不宣称它们共享一套固定格式。依据见方法参考。

未决定项写 `[UNCONFIRMED]`；只有为展示推导而临时采用的值写 `[ASSUMED: 理由]`。功效参数无证据就展示情景，不编造基准统计量。正式登记前逐项解决实质未定内容、保留可审阅版本并确认外部提交授权；起草和核验无需额外许可。
