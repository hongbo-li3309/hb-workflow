# 使用说明

先打开实际研究项目根目录，确认 `AGENTS.md` 和目标主稿。工作流库只提供资产；研究内容保存在初始化后的项目。对话默认中文，作品语言与格式由目标决定。

## 十二个研究入口

表中的 `$` 用法适用于支持技能选择的 Codex 对话；也可以自然语言描述，或从客户端技能列表选择。它们不是注册的十二个终端命令。

| 入口 | 可用模式与交付 |
|---|---|
| `$discover` | interview、lit、data、ideate、brainstorm、frontier；建立问题、文献关系与数据可行性 |
| `$strategize` | strategy、mechanism、theory、spine／focus、pap、pap interactive；机制、设计、主线与计划 |
| `$learn` | 经济概念、论文或方法；直觉、最小例子、推导、边界和项目应用 |
| `$analyze` | 已明确的分析任务，可选显式 dual language；可读脚本与真实运行证据 |
| `$write` | intro、strategy、model、data、results、conclusion、abstract、full、outline、edit、diagnose、humanize、style-guide；可说明语言、体例和领域 |
| `$review` | proofread、code、methods、theory、peer、stress、r2、replicate、all；针对需要的检查 |
| `$revise` | 真实或模拟 referee 意见；修订稿、差异、tracker 与 point-by-point response |
| `$talk` | create、audit、compile；job-market、seminar、short、lightning，Beamer 或 Quarto RevealJS |
| `$submit` | target、package、audit、final；目标要求与提交准备，final 本身不发送投稿 |
| `$new-project` | 经济问题、已有项目或 interactive；brief 和第一个有价值的具体任务 |
| `$checkpoint` | save、resume、本地 task key、dry-run；明确任务和可重复恢复 |
| `$tools` | commit、compile、validate-bib、lint、journal、context、deploy、learn、upgrade |

`$learn` 用于经济学学习；`$tools learn` 用于总结经证实的工作流经验。`$review` 的模拟编辑判断不代表期刊决定或录用概率。

## 一轮讨论如何有进展

可以直接说：“先别继续加回归。告诉我当前主线、最有力的反证和最值得做的下一步。”协作者应整理已有判断与来源，提出有机制和最小检验的建议，把尚未选择的分支留作候选。关键转向由你判断，已授权的普通核验继续做。

学习请求无需先建整套项目。可以要求先用 toy model，再逐步深入均衡、搜寻匹配、信息、合约、组织或结构识别，并说明复杂方法增加了什么认识。教学用假定数值不能进入项目证据账冒充发现。

## 写作与作者声音

提供主稿和用途，说明想要提纲、局部修订、结构改写还是诊断。大改另存、保留差异与原格式；只有你明确确认后候选稿才升级为主稿。四体例分别看 `references/writing-guide.md`，领域样本看 `references/writing-exemplars.md`，个人明确偏好看 `references/personal-style-guide.md`。

风格从具体经济问题、段落任务和真实样本提炼，不按固定词数、被动句或禁词配额。中文不会逐句翻译英文；政策报告围绕读者的政策工具、取舍和执行条件。不会通过删限定语把关联润色为因果。

## 从运行到证据

新项目只生成所选语言的 master 与 setup。设置主样本、变量、处理、推断和依赖后，再增加实际分析。Stata 的入口为 `scripts/stata/00_master.do`；Python 为 `scripts/python/00_master.py`；R 为 `scripts/R/00_master.R`；Julia 为 `scripts/julia/00_master.jl`。

运行记录示例（要求文件和脚本已经存在）：

```bash
python3 scripts/run_check.py --input scripts/python/describe.py --input data/cleaned/sample.csv --output paper/tables/group_means.json --report quality_reports/runs/describe_01.json -- python3 scripts/python/describe.py
```

声明真正相关的代码、数据和配置；每次选择新记录名。wrapper 不证明因果识别，也不能捕获所有软件内部静默错误；Stata batch 仍需核查本次日志的错误码。审查文件链接对应运行记录。

## 显式交接

本版没有自动 hooks。重要进展后在对话中请求 `$checkpoint save`，或从项目根执行：

```bash
python3 scripts/checkpoint.py save --task-key intro --task "修订引言" --next-action "检查机制与证据的对应"
python3 scripts/checkpoint.py load --task-key intro
python3 scripts/checkpoint.py list
```

有真实计划时加 `--plan` 及其项目相对路径；有可靠客户端会话 ID 时才加 `--session-id`。task key 是本地任务标签，并行会话使用不同 key。恢复时继续核对最新任务及真实文件；记录中的建议或旧批准不会自动成为本次授权。

当前研究状态看 PROJECT_BRIEF，主张及出处看 EVIDENCE_LEDGER，重大决定看 DECISIONS。三个文件按需维护，不要求你阅读每个 agent 的所有过程日志。
