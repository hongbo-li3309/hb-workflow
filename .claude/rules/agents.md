# Agents — 专业分工与证据整合

Claude 版保留既有角色名。当前 Claude 工具名为 Agent（旧 Task 是兼容别名）；只使用当前会话提供的能力。分工按信息价值和独立性决定，不按固定人数或配对仪式决定。

| 工作 | 执行角色 | 需要独立核查时 |
|---|---|---|
| 文献 | librarian | librarian-critic |
| 数据发现 | explorer | explorer-critic |
| 数据构建/可视化 | data-engineer | coder-critic |
| 机制与识别 | strategist | strategist-critic |
| 理论与证明 | theorist | theorist-critic |
| 分析代码 | coder | coder-critic + verifier（实际运行证据） |
| 写作 | writer | writer-critic |
| 演讲 | storyteller | storyteller-critic |
| 模拟同行审查 | editor | domain-referee、methods-referee |
| 协调与验证 | orchestrator、verifier | 主线程检查范围和证据 |

委派时给出当前问题、具体输入/版本、产出、允许修改的文件、已确认决定和未知事项。没有共同上下文的 agent 不能从项目名推测研究设定。独立任务可并行；互相依赖或会编辑同一文件的任务顺序执行。

Critic 不改主稿、数据、代码或用户决定；可写自己负责的审查报告。权限与报告中声称的工作必须一致，只读检查不能称已运行。Worker 自检仍必要，重要方法或结果可请独立 critic 核验；小修直接完成并核对。

主线程不盲从 critic：复核关键发现，区分错误、缺口与偏好，解释分歧及可判别证据。不因累计评分自动推进，不通过角色扮演预测期刊决策。陷入重复争论时提出具体研究选择或执行障碍，不能让用户从大量 agent 对话重建背景。
