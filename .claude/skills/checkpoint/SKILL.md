---
name: checkpoint
description: Save a minimal, project-scoped research handoff with the current brief, important evidence and decisions, and an explicit active task pointer. Optional existing memory or Obsidian integration remains opt-in.
argument-hint: "[--auto | --memory-only | --scaffold-only | --dry-run | --setup-obsidian]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash
---

# Checkpoint

输入：`$ARGUMENTS`。保存真实进展和可恢复的下一步。用户调用本技能即授权更新本项目交接；不再每次先问“是否保存”。默认不向全局目录、Obsidian 或外部应用同步。

按需读 [研究协作](../../references/research-collaboration.md)。当前任务、用户最新明确指令和已确认决定优先于旧日志、文件时间及 AI 推测。

## 恢复与保存

1. 确定实际项目根目录与当前会话任务；读取当前 `research/PROJECT_BRIEF.md`、相关 DECISIONS/EVIDENCE_LEDGER、显式计划路径及 Git 差异。Git 可以核对文件变化，不能代替判断用户授权。
2. 仅在内容改变时更新 brief；重要证据和重大决定按各自用途更新。主样本、代码、数据、模型或版本已变时，将受影响旧输出/主张标 `STALE`，不要把历史 `PASS` 带入新输入。
3. 写 `.claude/state/active-task.json`，用真实绝对项目路径与明确任务指针；没有计划用 `null`，不按“最新修改的计划”猜选。

```json
{
  "project_root": "/absolute/path/to/project",
  "plan_path": "quality_reports/plans/actual-plan.md",
  "task": "当前已授权的具体任务",
  "next_action": "下一个可以直接执行的动作"
}
```

实际运行时提供可靠会话 ID 时可加 `"session_id": "真实会话ID"`，以绑定指针。不要用猜测或未经支持的环境变量制造 ID。这个文件是项目当前任务指针；会话快照由 hooks 按 project_root 和 session_id 管理，checkpoint 不覆盖其他会话的 snapshot。

4. 保存后说明更新了哪些路径、什么已完成、哪些检查为 `FAIL` / `NOT_RUN` / `STALE`、下一步以及待研究者决定的具体事项。没有运行的工作不能写为完成；没有新内容就说明无需重复保存。

## 并行会话与最少日志

项目公共状态和每个会话的临时任务不同。恢复时核对 project_root 和可靠 session_id；未匹配/未知的 active pointer 仅作项目线索，不能据此继承另一会话任务或授权。未找到已绑定快照时，先读公共 brief，再按当前用户任务开展工作。

不要删除已读快照，重复 resume 仍应可恢复。不要把相同决定重写到多份日志；DECISIONS 是决定来源，brief 保持当前摘要，审查/运行报告保留细节链接。旧 `SESSION_REPORT.md`、research journal 和 session logs 保留历史；仅当现有项目明确使用它们且有额外交接价值时简短追加链接。

本地状态可能包含路径或研究内容；先检查项目 `.gitignore` 的 state 规则，不把会话状态顺手提交。所有路径均属于当前项目；不因一个 vault 配置存在就获得外部写入权限。

## 兼容旧选项

| 选项 | 当前行为 |
|---|---|
| `--auto` | 与默认一致：在授权范围内直接保存 |
| `--dry-run` | 只展示拟保存内容，不写文件 |
| `--memory-only` | 仅整理已配置且获授权的 Claude memory 中的长期偏好/稳定信息；环境不可写时交付建议文本，不假报保存 |
| `--scaffold-only` | 只保存项目内 brief、必要证据/决定与活动指针；不外部同步 |
| `--setup-obsidian` | 按现有 `.claude/state/obsidian-config.md.example` 准备本地配置，核验工具是否存在；不安装/连接或上传内容 |

长期 memory 仅记录用户明确偏好和稳定事实，不承载瞬时结果或复制整个研究状态。现有 `.claude/state/obsidian-config.md` 可以帮助定位已配置目标，**配置存在本身不是授权**；本次或先前已有明确同步授权且工具可用时才执行。采用读取—局部修改—核对，禁止把删除整篇再重建作为常规同步方式。未授权的外部写入先准备可审阅差异，实际权限机制需要批准时按机制处理。
