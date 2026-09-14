# Codex 研究角色与分工

20 个角色位于 `.codex/agents/*.toml`，包含 name、description、developer_instructions；审查角色默认 read-only。模型／推理强度及其他配置不写死，继承当前父会话和用户设置。实际生效权限仍由当前客户端、运行时覆盖和组织设置决定；提示中的角色限制不会授予额外权限。

| 工作 | 执行角色 | 有必要时独立审查 |
|---|---|---|
| 文献与前沿 | librarian | librarian-critic |
| 数据发现与可行性 | data-explorer | explorer-critic |
| 数据构建／测量／图形 | data-engineer | coder-critic |
| 机制与策略 | strategist | strategist-critic |
| 理论与证明 | theorist | theorist-critic |
| 实证代码 | coder | coder-critic、verifier |
| 写作 | writer | writer-critic |
| 演讲 | storyteller | storyteller-critic |
| 模拟编辑综合 | editor | domain-referee、methods-referee |
| 范围协调与实际核验 | orchestrator、verifier | 主会话复核证据 |

`data-explorer` 是研究数据发现角色，避免覆盖 Codex 内置的代码浏览角色 `explorer`。其他名称保持研究分工的可辨认性。

先检查当前会话能否调用子 agent。支持自定义角色时按实际工具契约选择角色；工具仅支持通用子 agent 时，把对应 TOML 的 developer_instructions、输入和权限边界作为具体任务传入。只有真正启动了不同角色／线程才能称独立并行；没有工具时由当前会话按同样问题串行复核，标明独立性未验证。

委派说明经济问题、授权范围、输入及版本、允许写入的文件、预期结果和验收证据。独立只读任务可并行，共用文件或依赖结果顺序整合。PROJECT_BRIEF、EVIDENCE_LEDGER、DECISIONS 默认由主会话整合，避免相互覆盖。

所有 critic、referee 和 editor 只返回报告，不修改文件；由主会话存 `quality_reports/reviews/`。其只读配置不会自动移除所有 MCP 能力，因此仍不得调用产生外部修改的工具。实际执行检查交给具备授权执行能力的 verifier／worker，结果入 `quality_reports/runs/`。不以角色自报完成代替产物核验。

主会话处理审稿分歧：区分实质错误、证据缺口和偏好，核对关键证据，给能改变判断的下一步。不要为了一个段落改写启动全套角色，也不要让作者从二十份报告中拼出项目背景。
