# AGENTS.md — __PROJECT_NAME__

这是独立 GPT/Codex 研究项目，主要分析语言为 **__LANGUAGE__**。以用户指定主稿、当前问题和真实证据为准，不把工作流模板或维护者身份当作论文事实。

## 协作与作者决定

默认中文，保留必要英文术语。先经济问题与机制，再假设、数据与识别。主动提出有文献依据的机制、竞争解释和最小检验；帮助研究者学习陌生理论与方法，不因暂不熟悉缩小探索范围。

每轮实质讨论说明认识变化、证据和反证、主要未知及首选下一步；简单操作不附加议程。已授权工作持续完成；用户要求先计划则先保存计划待确认。更换核心问题、主要 estimand、影响解释的主样本／规格或高成本方向时，准备推荐、备选与代价供作者判断。建议不能自动记录成已批准。

## 项目事实与状态

- 经济问题：[待明确，先形成 research/PROJECT_BRIEF.md]
- 研究者／合作者：[按用户提供填写]
- 主稿：[指定路径／版本]
- 数据与访问：[真实来源及限制]

`research/PROJECT_BRIEF.md` 是一页主线；有实际重要内容再用 templates 建 EVIDENCE_LEDGER.md 与 DECISIONS.md。详细文献、数据、策略和理论分别放 research/literature.md、data-assessment.md、strategy.md、theory.md。检查用 PASS／FAIL／NOT_RUN／NOT_APPLICABLE，输入变化的旧证据为 STALE；未运行不能报告通过。

修改论文／报告按 `references/protocols/revision.md` 另存修订并保留差异和原格式。写作按 `references/writing-guide.md` 的四体例及真实 exemplar，个人明确修改优先。不为去 AI 味删除必要条件或加强因果含义。

## 工具与入口

从项目根使用所选语言 master：Stata 为 scripts/stata/00_master.do；Python 为 scripts/python/00_master.py；R 为 scripts/R/00_master.R；Julia 为 scripts/julia/00_master.jl。只生成所选语言。代码清楚、集中关键设定，保护原始数据，检查样本、merge、单位、推断及导出。

运行时发现实际 MCP／本地程序，保存脚本和证据。执行 JSON／log 在 quality_reports/runs/，评审在 quality_reports/reviews/。`scripts/lint_research.py` 只是静态提示，`scripts/run_check.py` 不证明识别正确。

技能在 .agents/skills/，可用自然语言或 `$技能名`：discover、strategize、learn、analyze、write、review、revise、talk、submit、new-project、checkpoint、tools。完整用法见 docs/usage.md。new-project 在已有项目中只开展研究设定，不覆盖初始化。

角色在 .codex/agents/；只在独立工作有价值且工具可用时委派，说明文件所有权。critic／referee／editor 只返回报告，主会话保存；公共状态由主会话整合。无子 agent 时明确串行。模型与权限保留当前用户设置，实际能力见 docs/platform.md。

重要进展后显式 `$checkpoint` 或运行 scripts/checkpoint.py；本地 task key 保存在忽略的 .workflow-state/，不自动恢复授权。本项目未配置自动 hooks。研究协作／方法／协议按需读 references/，不预装全目录。

初始化不授权创建远端、发送研究内容或正式投稿；凭据、本机状态和受限数据不进 Git。
