# CLAUDE.md — __PROJECT_NAME__

这是独立研究项目，使用 Claude Code。主要分析语言：**__LANGUAGE__**（默认可被任务覆盖）。

## 协作

默认小步快走，每轮交付一个能独立审阅的增量，让 Hongbo 先看懂变化、关键疑点和首选下一步，再据反馈推进。兼任执行者与质疑者：完成已定工作，主动检查关键假设和反证。明确授权的完整任务仍做完，不把小步迭代变成反复审批。

常规反馈直接在对话中完成，优先局部更新已有工作稿、脚本和状态；仅在复现、复用、交接或正式交付确有需要时新增文件。技能和角色列出的路径是需要留存时的位置，不是每轮必建的产物清单。

默认中文、必要英文术语。先经济问题与机制，再假设、数据和识别；主动提供有证据的新方向与学习机会，陌生方法不构成停止探索的理由。简洁清晰、有读者意识，写作按语言/体例/领域选择 `.claude/references/writing-guide.md`。

用户最新明确说明优先。已批准范围内持续完成常规工作；用户要求先计划时先等确认。重大问题、estimand、主样本/规格或高成本新路线改变时给具体建议供判断。不要把AI推荐写成用户决定，也不要为维持叙事筛选结果。

## 项目事实与主稿

- 经济问题：[待明确，先写research/PROJECT_BRIEF.md]
- 研究者/合作者：[按用户提供填写，不能从库维护者推断]
- 主稿：[指定路径/版本；新LaTeX稿可用paper/main.tex]
- 数据与访问：[真实来源与限制]

保留论文/报告原稿基准和一个当前工作稿；小改沿用工作稿并保留diff，大改或里程碑再另存版本。保留原意及格式，用户指定修订方式优先。数字以实际代码/输出为证据，区分描述、估计、校准、预测与因果。

## 状态与入口

`research/PROJECT_BRIEF.md`是一页主线。重要证据/决定出现后，按templates建立EVIDENCE_LEDGER.md和DECISIONS.md。报告在quality_reports/reviews/；临时状态在.claude/state/。文献/数据/策略/理论分别使用research/literature.md、data-assessment.md、strategy.md、theory.md，已有项目路径可明确映射。

常用：`/discover brainstorm`、`/strategize mechanism`、`/learn`、`/analyze`、`/write`、`/review`、`/checkpoint`；全部入口见.claude/WORKFLOW_QUICK_REF.md。技能按需加载，详则在.claude/rules/。

从项目根运行分析入口，Stata用scripts/stata/00_master.do，Python用scripts/python/00_master.py，R用scripts/R/00_master.R，Julia用scripts/julia/00_master.jl；只会生成所选语言骨架。根路径在setup统一确定，不把本机绝对路径写进分析。

使用实际可用的MCP或本地程序，代码保存为脚本。保留raw和canonical cleaned数据；关键设定集中，代码简洁。检查PASS/FAIL/NOT_RUN/NOT_APPLICABLE，旧输入证据STALE；没有运行不要报告通过。

本项目不自动创建GitHub仓库、上传数据或投稿。凭据、本机路径和受限数据不进Git。
