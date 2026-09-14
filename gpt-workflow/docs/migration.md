# 独立使用与迁移

这是同一经济学研究原则的 GPT/Codex 实现，当前开发基线见 VERSION.md。保留文献、理论、学习、实证、写作、审查和交接的深度，平台入口、角色权限、状态和初始化单独适配。

## 内容对应表

| Claude 版 | GPT/Codex 版 | 适配方式 |
|---|---|---|
| CLAUDE.md | AGENTS.md | 精简项目指令及按需引用，说明原生发现与父级继承 |
| .claude/skills/ 与原命令 | .agents/skills/ 与 `$技能名`／自然语言 | 移除专用工具白名单和参数占位，保留 12 个研究入口 |
| .claude/agents/*.md | .codex/agents/*.toml | 原生角色字段，模型继承；critic／referee／editor 只读返回，由主会话保存 |
| explorer | data-explorer | 数据发现角色改名，避免覆盖 Codex 内置 explorer；explorer-critic 名称保留 |
| .claude/references/ | references/ | 完整迁移方法、写作、四体例、样本、风格、领域及四种语言代码规范 |
| .claude/rules/ | references/protocols/ | 共同原则按需读取；原生分工和显式交接协议重写 |
| Claude hooks／state | 显式 scripts/checkpoint.py、lint_research.py 和 .workflow-state/ | 不移植事件或伪称自动触发；task key 区分并行任务 |
| project-claude 模板 | templates/project-agents.md | 新项目只生成 AGENTS.md 主入口及所选语言骨架 |
| 初始化器 | scripts/new_project.py | 仅复制显式 GPT 资产；缺必要 helper 先失败，不覆盖目标 |
| 执行记录 | scripts/run_check.py 与 quality_reports/runs/ | 保留退出码、指纹、时效核对；reviews 链接运行证据 |

20 个角色完整表见 `references/protocols/agents.md`。没有子 agent 能力时串行执行并标明审查独立性限制。共同科学规则没有因为换平台而降低要求；中文和英文、学术和政策的差异在两版中保留。

## 新项目与现有项目

新项目从本版独立目录运行初始化器，目标必须不存在。不要在原工作流库内部创建研究项目，也不要把两套隐藏配置一次复制到同一个论文项目。初始化不创建 GitHub 远端、上传数据或填写虚构研究进展。

已有项目先读取实际主稿、定制规则、证据和已有运行入口，再准备逐文件差异。保留现稿和个人定制，复制需要的本版资产，明确主指令入口与客户端；不要删除整套旧目录。若准备分开使用两客户端，优先独立目录／分支并明确哪一个是研究主稿，防止两份都被当成当前结果。

迁移研究状态时单独选择经确认的 PROJECT_BRIEF、EVIDENCE_LEDGER、DECISIONS 和必要专题材料，核对数据／稿件版本。不要迁移 `.workflow-state/`、原客户端会话快照、认证文件或私有缓存作为新会话授权。共享研究状态与本地客户端记忆是两件事。

## 升级与维护

记录源版本和本地修改，先比较差异再应用。共同研究原则变动时核对另一版是否仍一致；平台专用工具和事件按各自契约处理，不靠批量替换品牌名升级。更新个人风格时只把用户确认的偏好长期保留。

本目录的 references、templates、scripts 和角色都是内部文件，不通过符号链接读取父目录。独立性测试在仓库外临时副本进行；初始化测试覆盖带空格路径、已有目录、缺 helper、四种语言、私有状态不复制和本地任务恢复。

来源沿革：本工作流由 Hongbo 的 Claude Code 研究工作流重构迁移，原库源于 hugosantanna/clo-author 及相关经济学工作流。保留 LICENSE；原文献样本和方法材料的来源分别保留于对应 reference，不把第三方论文内容当作本库原创。
