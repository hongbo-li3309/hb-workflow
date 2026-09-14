---
name: tools
description: Maintain an economics research workspace with scoped Git work, compilation, bibliography checks, static lint, handoff, and reviewable workflow upgrades.
---

# Tools

处理用户指定的维护任务；不因一次编译或 Git 请求启动整个研究流程。保留原有修改，使用当前实际可用的本地／连接工具；工具缺失时报告具体 NOT_RUN 并继续独立工作。

| 子任务 | 行为 |
|---|---|
| `commit` | 查看 status／diff，完成必要检查，按明确路径暂存并提交；push 在已有授权内执行。commit 不授权合并他人 PR 或部署。 |
| `compile [file]` | 按主稿配置执行，保留退出码和日志并查看实际渲染。用 `scripts/run_check.py` 时声明所需代码／数据／配置和输出。 |
| `validate-bib` | 引用键、重复身份和版本核对；存在条目不代表原文支持句子，重要主张核验一手来源。 |
| `lint [path]` | 运行 `python3 scripts/lint_research.py <path>`；这是有范围的静态提示，不是实际分析通过。 |
| `journal / context` | 根据当前 brief、证据、决定、改动与任务记录给最少交接；不能声称读取不可用的上下文计数器。 |
| `learn` | 从实际修订提炼有依据的工作流经验，候选与用户确认分开；经济学学习用 `$learn`。 |
| `deploy` | 先准备并验证目标产物，只在明确授权内实际发布。 |
| `upgrade` | 读版本和当前定制，准备逐文件差异，保留状态、稿件和用户配置；不删除整套目录或自动改全局配置。 |

本工作流库检查使用 `python3 scripts/validate_workflow.py`（如果库中已提供）和 `python3 -m unittest discover -s tests`；新研究项目没有库自测文件，按分析／稿件真正依赖的脚本运行。`python3 scripts/new_project.py <destination> --lang stata` 只在工作流库创建全新本地项目，已有项目改用逐文件迁移。

执行 JSON／log 放 `quality_reports/runs/`，评审放 `quality_reports/reviews/` 并链接执行证据。缺工具是 NOT_RUN，输入改变是 STALE。不要用 tail、忽略失败的 shell 命令或旧 PDF 伪造成功；本版未安装自动 hooks。
