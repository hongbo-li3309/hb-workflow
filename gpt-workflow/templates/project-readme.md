# __PROJECT_NAME__

独立 GPT/Codex 经济学研究项目，主要分析语言：__LANGUAGE__。

在项目根启动 Codex，确认读取 AGENTS.md。可以从“我的经济问题是……”开始，或选择 `$discover brainstorm`；用 `$learn` 深入经济机制和方法，用 `$write` 处理指定主稿，全部入口见 docs/usage.md。

当前主线在 research/PROJECT_BRIEF.md；重要证据和决定出现后再建立 EVIDENCE_LEDGER 和 DECISIONS。数据、作者、主稿和真实结论尚待明确，骨架不会生成假结果。

scripts/ 下只有所选语言入口和必要执行／lint／checkpoint helper。先明确数据和规格，再运行分析。运行记录在 quality_reports/runs/，评审在 quality_reports/reviews/；本地任务交接在忽略的 .workflow-state/。本版没有自动 hooks，交接显式执行。

修改主稿保留原格式和可审阅差异。初始化不创建 GitHub 远端，不上传数据，不修改全局客户端配置。平台差异见 docs/platform.md，升级方式见 docs/migration.md。
