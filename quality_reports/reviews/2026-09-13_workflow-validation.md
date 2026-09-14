# 双版 workflow 验收记录

日期：2026-09-13。范围：已批准的经济学工作流重构；本地起点 `c25a7ec`，推送前核对 `origin/main` 也为该提交。本库没有真实论文数据或主稿。

## 已交付的行为与结构

Claude 保留 `CLAUDE.md`、全部既有文件位置及命令名称，更新内容并新增 `/learn`。GPT 独立置于 `gpt-workflow/`，使用 `AGENTS.md`、`.agents/skills/`、20 个 `.codex/agents/*.toml` 和显式 checkpoint。两版各有 12 个技能；GPT 的 `data-explorer` 对应 Claude 的 `explorer`，避免覆盖客户端内置角色。

核心协作围绕研究问题、机制、证据和研究者决定：约一页 brief，重要证据与决定出现后再建 ledger 和 decisions；推荐不自动变成批准，零结果与反证保留。学习、理论和描述研究有独立入口。中英学术／政策四体例分开处理，6 份真实来源的写作样本记录版本、实际读取范围与使用边界。

代码规范收敛到可读入口与关键数据检查。已修复错误模型导出、无效 RNG、方法归属和因果措辞；执行记录保留命令、退出码、声明依赖和输出指纹，失败、旧输出、缺工具或缺证据不能冒充 PASS。初始化器不覆盖项目、不混装版本，不带入私人配置或研究状态。

## 自动检查及实际演练

| 检查 | 状态 | 实际覆盖 |
|---|---|---|
| Claude 库测试 | PASS | 39 项 unittest：hooks 11、分析示例与执行记录 17、初始化 8、结构验证负面对照 3；Python 3.9.6 |
| GPT 库测试 | PASS | 30 项 unittest；包含与 Claude 共用的执行记录案例，数量不是互不重复的 69 个场景；Python 3.9.6／独立副本 Python 3.12 |
| 两版结构／引用 | PASS | 各自运行 validator，0 errors；Python 3.12 完整 TOML 解析，Ruby/Psych 完整技能／Claude 角色 YAML 解析；另检查脚本语法与本地链接 |
| 故障对照 | PASS | 非零退出但输出看似成功、旧／缺／空输出、输入变化、缺运行器、不可覆盖历史、输入输出别名、并发同名记录；刻意坏链接／缺技能／坏 JSON／不存在 hook 均被发现 |
| Claude hooks 直接执行 | PASS | 使用符合事件契约的 JSON 输入运行；`.do`／`.ado` 静态提示、文件路径范围、首次创建、两个会话、错误根目录及重复恢复均有测试 |
| hooks 自动触发 | NOT_RUN | 当前 Claude Code 原生测试未完成，不能把直接脚本执行当成客户端集成成功；直接文件保护也不涵盖 Bash／MCP 写入 |
| 初始化与独立性 | PASS | 两版带空格路径、拒绝已有目标／symlink、缺 helper 前置失败、不携带私人 state；Python 骨架实际执行；GPT 整包在仓库外运行 validator 和全部测试 |
| Claude 原生 smoke | NOT_RUN | Claude Code 2.1.267 在生成的独立项目启动后返回 `Not logged in · Please run /login`；临时新项目也未获信任。没有修改账号或全局信任来绕过 |
| Codex 原生 smoke | PASS | Codex 0.154.0 在仓库外副本加载项目指令，实际读取 learn 并完成两期教学；自定义角色直接发现与完整独立审查另列 NOT_RUN，详见 [原生记录](../../gpt-workflow/docs/native-smoke.md) |
| 研究／写作行为审阅 | PASS | 实际构造四体例改写、竞争机制与下一步、动态学习和无效引用处理；核对单位、证据强度与数值边界。详见 [行为报告](2026-09-13_behavior-review.md)与[重放用例](../../tests/behavior_cases.md) |
| guide 源文件 | PASS | 7 页、内部导航／链接、角色和技能入口一致，保留主题与 GIF |
| Quarto 渲染／视觉检查 | NOT_RUN | 当前 PATH 无 Quarto；源文件检查不代替渲染，没有发布网站 |
| Stata／R／Julia 实际分析 | NOT_RUN | 当前 PATH 无相应运行器，无本次真实分析数据；静态示例和语言骨架不是回归或数值复现 |
| 真实论文编译／投稿 | NOT_APPLICABLE | 没有指定论文主稿或正式投稿任务；未编造完成情况 |
| GitHub Actions 远端执行 | NOT_RUN | 已添加 Claude／GPT 分别执行的 CI jobs；本地检查不预称远端 CI 通过 |

这些状态对应列明的范围。词语扫描不能认证“去 AI 味”，单次模型输出不能认证后续所有研究行为，运行成功也不能证明识别、创新性或可发表性。

## 原稿与边界核对

实施前记录 114 个已跟踪文件和既有未提交工作；所有原路径保留。旧 `cheatsheets/lessons-from-day1.md`、五月历史计划、guide 主题和 GIF 与备份逐字节一致。已修改的 `new-paper-function.md` 及原未跟踪教程以当前工作稿为基础完成本轮重写；旧个人复盘与无关计划不进入提交。

没有修改 `~/.zshrc`、全局 Claude／Codex 指令、既有论文项目或外部笔记。原生客户端按正常机制使用账号和本地缓存，未改账号／模型配置。独立版本之间不自动同步；共同原则变动时需分别核对。提交按 Claude 重构与 GPT 迁移组织，最终哈希、分支及 push 结果见仓库 Git 历史与交付回复。

复查命令：在每版工作流库根运行 `python3 scripts/validate_workflow.py`、`python3 -m unittest discover -s tests`；完整 TOML 解析使用 Python 3.11+。这些库级检查不会被复制到新研究项目，也不成为每轮研究对话的强制流程。
