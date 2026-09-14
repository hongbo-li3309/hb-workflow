# Hongbo 的 GPT/Codex 经济学研究工作流

这个目录可完整复制出去，作为独立工作流库使用。它覆盖文献与创新讨论、经济机制与理论学习、实证代码、四类写作、审查、R&R、演讲及提交准备。默认中文交流、Stata 分析；项目已有工具和指定主稿优先。

核心是让研究者看得懂项目的判断与选择：一页主线 `research/PROJECT_BRIEF.md`，重要主张有证据账，重大选择有决定记录。AI 完成已授权工作，同时保留反证、未知和可供作者判断的备选。

## 创建一个独立项目

在本目录运行，目标目录必须尚不存在且位于本工作流库之外：

```bash
python3 scripts/new_project.py "/你的项目目录/ai-labor" --lang stata
```

可选 `--lang python`、`r` 或 `julia`；`--git` 仅初始化本地 Git，不提交、不创建远端。初始化器按显式清单复制本版资产，不复制库状态、私有数据、凭据或原版本库。已有项目请按 [迁移说明](docs/migration.md) 逐文件更新，不能运行初始化器覆盖。

然后在新项目根目录启动 Codex，例如：

```bash
codex -C "/你的项目目录/ai-labor"
```

使用你自己的模型、权限和 MCP 设置；项目配置不预填型号、账户路径或密钥。项目指令在 `AGENTS.md`，技能在 `.agents/skills/`。首次使用请核对客户端实际发现的指令和技能；配置的加载还取决于项目是否受信任，详见 [平台能力](docs/platform.md)。

## 从具体研究问题开始

下面是在 Codex 对话中输入的例子，**不是终端命令**：

```text
$discover brainstorm 我看到 AI 采用企业减少招聘，先帮助我区分任务替代、需求变化和招聘渠道迁移，并核对最接近的文献。
$learn 用一个最小任务模型解释生产率上升为什么未必降低劳动需求，再带我走一遍假设和推导。
$strategize spine 根据现有证据整理一条主线，保留反证，给我最值得先做的一个检验。
$write intro --lang en --genre academic 以我指定的主稿为准，参考贴近主题的真实论文，另存修订并给差异。
```

也可直接用中文描述任务。没有数据或结果时可以先做理论、提纲和明确占位的初稿。一次 brainstorm 不会自动启动所有分支，一次新项目请求不会自动跑到投稿。

完整入口与场景见 [使用说明](docs/usage.md)。研究方法、四种体例、真实原文片段和个人偏好在 `references/`；参考只按任务加载，少读无关上下文。

## 验证与交接

- 适用检查分别报告 PASS、FAIL、NOT_RUN、NOT_APPLICABLE；旧输入证据标 STALE。程序成功、证明有效、因果可信、文风合适是不同判断。
- `scripts/run_check.py` 保存当前命令、指纹、退出码、输出和日志；执行 JSON／log 放 `quality_reports/runs/`，评审放 `quality_reports/reviews/`。
- `scripts/lint_research.py` 是静态提示。没有 Stata／MCP 环境时不能声称运行过回归。
- `$checkpoint` 显式保存最少状态；本地 task key 区分并行任务，记录不产生授权，恢复不会删记录。本版不自动运行 hooks。

工作流库本身的结构及脚本测试：

```bash
python3 scripts/validate_workflow.py
python3 -m unittest discover -s tests -v
```

新研究项目只获得必要执行脚本，不带库专用 validator／tests／初始化器。其分析和稿件按真实任务验收，不对空骨架宣称已通过实证复现。

[版本记录](docs/VERSION.md) 标注当前迁移基线；实际范围见[离线验证](docs/verification.md)与[原生 smoke](docs/native-smoke.md)。本版以本地 Codex 为主要执行环境；普通网页聊天不会仅因上传这些文件就拥有本地文件、脚本和 agent 能力。未安装到全局目录，也未修改现有论文项目或外部笔记。
