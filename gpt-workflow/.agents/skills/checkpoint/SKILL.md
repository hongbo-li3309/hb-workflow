---
name: checkpoint
description: Save or restore a concise economics research handoff using explicit local task state, while preserving project and session boundaries and actual evidence status.
---

# Checkpoint

根据当前请求保存或恢复。调用示例是 `$checkpoint save`、`$checkpoint resume task-key` 或自然语言“保存这次主线和下一步”。本技能显式执行，不承诺压缩或退出时自动触发。

无需每次回复后自动 checkpoint。实际调用时，复用当前 brief 与同一任务指针；用户仅需一句总结时直接在对话回复，不额外生成 Markdown 交接文件。

## 保存

先核对项目根目录的 `AGENTS.md`、当前用户任务、已确认决定和磁盘差异。只在判断变化时更新 `research/PROJECT_BRIEF.md`；重要证据和决定按各自用途写入 EVIDENCE_LEDGER／DECISIONS。代码、数据、样本或模型改变后，相关旧证据标 `STALE`。不把 AI 建议写为 approved。

为当前任务选择一个稳定的本地 `task-key`，例如 `ai-hiring-intro`。这是本工作流的任务名称，不是伪造的客户端会话 ID；并行会话使用不同 key。若当前已经绑定 key，沿用，不再猜最新文件。用实际计划相对路径；没有计划就省略。

```bash
python3 scripts/checkpoint.py save --task-key ai-hiring-intro --task "修订引言的机制段" --next-action "核对两个竞争解释的证据" --plan quality_reports/plans/active-plan.md
```

此例要求计划真实存在。真实运行时提供可靠会话 ID 才加 `--session-id`；未知就省略。脚本保存 `.workflow-state/tasks/<hash>.json`，不自动批准计划或更改研究结论；公共 brief 与各任务记录分开。

## 恢复

```bash
python3 scripts/checkpoint.py load --task-key ai-hiring-intro
```

脚本核对实际 project_root，不删除记录；反复恢复应可重复读取。如果请求使用 `--session-id`，会核对与记录的一致性。没有指定 key 时可运行 `list` 展示当前项目记录，不能自动按最新时间选择一个作为授权。只读记录包含旧任务线索；恢复后仍比较用户最新要求、Git 差异和实际证据。

项目移动／复制后旧记录的绝对根目录不匹配，脚本拒绝恢复；读公共 brief 并确认当前任务后另存。它不会从其他项目自动搬入会话状态。

## 交付与选项

说明当前主线、改了什么、哪些为 FAIL／NOT_RUN／STALE、下一步和真正待作者判断的事项。没有变化不重复保存多份日志。

`--dry-run` 表示仅展示拟保存信息；`--scaffold-only` 与本版默认一样只处理项目内状态；`--memory-only` 只整理已确认的稳定偏好到项目 MEMORY.md，不声称修改客户端内部记忆。旧外部笔记同步意图可先准备差异，只有实际工具和明确授权时执行；此版本不配置 Obsidian 自动同步。
