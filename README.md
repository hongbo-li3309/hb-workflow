# Hongbo 的经济学研究工作流

用于研究讨论、前沿文献、经济机制、实证分析、论文和政策写作。默认中文交流、Stata分析；AI负责检索、实现和核查，并把主线、证据和重要选择清楚交还研究者。学习新理论和方法是工作的一部分。

本库由 [clo-author](https://github.com/hugosantanna/clo-author) 和 [Pedro Sant’Anna 的工作流](https://github.com/pedrohcgs/claude-code-my-workflow) 改造。原路径继续为Claude版，文件与命令命名保持。

## 两个独立版本

| 版本 | 入口 | 使用 |
|---|---|---|
| Claude Code | [CLAUDE.md](CLAUDE.md)、[快速参考](.claude/WORKFLOW_QUICK_REF.md) | 使用当前目录的技能；新论文由下面的初始化命令创建 |
| GPT / Codex | [gpt-workflow/README.md](gpt-workflow/README.md) | 完整独立目录，使用其AGENTS.md、skills、配置和初始化工具；可复制出去 |

研究原则相同，调用和执行能力分别适配。Claude初始化不复制GPT版，GPT初始化不复制Claude版；两版不会自动互写记忆或研究状态。

## 创建第一个项目

本地需要Python 3.9+和所用客户端；Stata/LaTeX等只在任务实际用到时需要，不在初始化时安装。

```bash
python3 scripts/new_project.py ../paper-my-question --lang stata
```

进入新目录并启动Claude Code。可以直接说：

> 我想研究AI如何改变企业的任务分工与招聘。先帮助我比较机制、最近相关文献和能区分这些解释的证据，再建议值得先做的一步。

生成器读取当前工作区模板，拒绝覆盖已有目录，不带入本库的历史、数据、私人设置或另一版。默认不初始化Git；`--git`只建立本地仓库，不commit或创建远端。旧 `new-paper` 入口的简短调用方式见 [cheatsheet](cheatsheets/new-paper-function.md)，不会自动改你的 `~/.zshrc`。

## 日常使用

| 你在做什么 | 入口与结果 |
|---|---|
| 想问题、找新方向 | `/discover brainstorm`；机制、证据、替代解释、最小检验 |
| 跟踪前沿 | `/discover frontier`；日期、版本、读取范围与相邻/相反文献 |
| 设计或收敛项目 | `/strategize mechanism`、`/strategize focus`；主线与下一项判断 |
| 学一个新方法 | `/learn`；问题→直觉→toy model→假设/推导→项目应用 |
| 分析 | `/analyze`；简洁脚本、关键检查、真实输出 |
| 写作 | `/write`；中英学术/政策分体例，按领域实际范文调整 |
| 审查与修订 | `/review`、`/revise`；具体证据、重要问题与可审阅修订 |
| 演讲与投稿准备 | `/talk`、`/submit`；匹配受众及经核实的目标要求 |
| 收工与恢复 | `/checkpoint`；简短状态与可接续任务 |

自然语言请求同样有效；不必先学完全部命令。主线程在授权范围内连续完成工作，重大研究方向选择给具体建议供你判断。

## 研究状态与写作

先只维护一页 `research/PROJECT_BRIEF.md`。有重要结果或选择时，再建立 `EVIDENCE_LEDGER.md` 和 `DECISIONS.md`。文献与代码的详细记录通过链接展开，避免靠几十份日志重建研究背景。主线服从证据，零结果和反证保留。

写作先修经济逻辑和主张—证据关系，再修句子。保留指定主稿、格式与个人偏好；大改另存并提供diff。四类体例、范文观察与实际出处见 [writing guide](.claude/references/writing-guide.md)。不以固定句长、被动句比例或期刊刻板印象定义好文章。

模板包括[主线](templates/project-brief.md)、[证据账](templates/evidence-ledger.md)、[决定](templates/decision-record.md)、[审查](templates/quality-report.md)、[交接](templates/session-log.md)、[探索](templates/exploration-readme.md)、[归档](templates/archive-readme.md)、[任务范围](templates/requirements-spec.md)、[可选项目约定](templates/constitutional-governance.md)、[skill](templates/skill-template.md)、[项目指令](templates/project-claude.md)与[项目README](templates/project-readme.md)。按需使用。

## 验证与维护

```bash
python3 scripts/validate_workflow.py
python3 -m unittest discover -s tests
```

状态为PASS/FAIL/NOT_RUN/NOT_APPLICABLE；输入变化使旧证据STALE。静态检查、编译、实际分析、识别判断和写作审查分别报告；模型分数不认证研究质量。hooks只覆盖声明的事件和操作范围，能力边界与实际运行情况见[验证报告](quality_reports/reviews/2026-09-13_workflow-validation.md)。

更多说明见 [中文上手](tutorial/QUICKSTART_zh.md)、[迁移与维护](cheatsheets/workflow-architecture.md)及 [guide](guide/index.qmd)。升级先看差异，保留项目定制；不删除整个 `.claude/`。本库不自动安装全局设置、不发布网站、不上传研究数据。
