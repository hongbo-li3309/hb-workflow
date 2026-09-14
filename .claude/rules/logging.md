# 状态与日志

当前状态是 `research/PROJECT_BRIEF.md`；重要证据是 `research/EVIDENCE_LEDGER.md`；重大决定是 `research/DECISIONS.md`。模板在 `templates/`。不为每个 agent 调用重复生成日志，也不把 AI 推荐记录为已确认决定。

有必要交接时，在 `SESSION_REPORT.md` 追加一条简短记录：任务、发生变化的认识/文件、验证证据、下一步、待确认事项。重大变更可用 `quality_reports/session_logs/YYYY-MM-DD_<task>.md`。已有 `quality_reports/research_journal.md` 保留为历史；不强制继续重复写同一内容。

每次 `/checkpoint` 先检查是否已有相同记录；无变化不追加。知识偏好只记录用户明确确认或有证据的经验，注明日期与适用范围。MEMORY 不保存猜测的研究事实，不声称自动记忆一定写入成功。

原始执行日志保存在 `quality_reports/runs/`，应与本次命令、输入/脚本指纹和输出对应；体积大、敏感内容不要进 Git。审查产物在 `quality_reports/reviews/`。主稿修订日志记录基准版本、输出和重要含义变化。
