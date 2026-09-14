# Claude Code 快速参考

在实际研究项目中工作；这个库用于维护模板。默认中文、Stata；用户指定工具和主稿优先。GPT版在独立的 `gpt-workflow/`，Claude任务不加载它。

| 命令 | 适用任务 |
|---|---|
| `/new-project [问题]` | 明确项目与下一阶段；不自动一路执行到投稿 |
| `/discover interview` | 聚焦问题与约束，信息充分则不重复问卷 |
| `/discover lit` / `data` | 文献和数据评估，记录版本、读取范围与可得性 |
| `/discover ideate` / `brainstorm` / `frontier` | 创新、竞争机制及近期文献变化 |
| `/strategize mechanism` / `theory` / `focus` / `pap` | 机制、识别、推导、主线整理和PAP |
| `/learn [概念]` | 学习经济学理论/方法，连接具体研究问题 |
| `/analyze [任务]` | 可读代码、实际执行与结果解释 |
| `/write [目标]` | 按语言/体例/领域起草、编辑或诊断 |
| `/review --code` / `--methods` / `--theory` / `--peer` | 选择所需审查，返回有证据的问题 |
| `/revise [意见]` | R&R范围、依赖、回应与另存修订 |
| `/talk [模式]` | 演讲结构与视觉核查 |
| `/submit target` / `package` / `audit` / `final` | 查要求、准备、核验；正式提交另按授权 |
| `/checkpoint` | 更新一页状态及必要交接，不重复写日志 |
| `/tools commit` / `compile` / `validate-bib` / `lint` | 轻量维护，Git动作按已授权范围 |
| `/tools learn` | 总结工作流经验，与经济学 `/learn` 区分 |

当前主线：`research/PROJECT_BRIEF.md`。重要证据/决定按需建 `research/EVIDENCE_LEDGER.md`、`research/DECISIONS.md`。文件身份与恢复规则见 `.claude/references/research-collaboration.md`。

普通任务在已有授权内继续；重大研究选择先给具体推荐和备选。重要结果需核对单位、样本、规格和来源。PASS/FAIL/NOT_RUN/NOT_APPLICABLE按检查分别记录，旧结果STALE。没有评分通关、固定问卷或每个任务都跑全套agents。
