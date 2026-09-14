---
name: new-project
description: Start an economics research project with a concise brief and the first useful stage of work, or coordinate a longer explicitly authorized scope. Supports empirical, theoretical, and measurement projects.
argument-hint: "[research topic | existing project path | interactive]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Agent,WebSearch,WebFetch
---

# New Project

输入：`$ARGUMENTS`。默认建立研究设定并完成第一阶段具体工作；执行范围由用户任务决定，不从一个想法自动跑到投稿。

先读已有项目入口、指定主稿和 `research/PROJECT_BRIEF.md`；按需读 [研究协作](../../references/research-collaboration.md)。保留用户文件、目录和已确认设定。已有论文项目不重新初始化；路径不清楚时先检查工作目录，避免把工作流模板库写成实际论文项目。

## 建立可讨论的起点

1. 从上下文提炼一句问题、经济重要性、当前机制与替代解释、可用材料、关键未知、近期可交付工作。研究类型可以是实证、理论、结构、测量或混合，不要求先选熟悉的识别方法。
2. 信息足够时直接写约一页 `research/PROJECT_BRIEF.md`，未知项显式保留。只有答案决定接下来能否开展时才澄清关键问题；`interactive` 是对话入口，不是固定问卷。
3. 默认完成一个最有价值的初步任务，如前沿地图、数据可行性检查、机制小模型或既有结果诊断。独立文献/数据搜索可并行，涉及共同文件的综合由当前协调者完成。
4. 有实质证据或重大选择后再建立 `research/EVIDENCE_LEDGER.md` 和 `research/DECISIONS.md`；空项目不批量生成假状态。模板目录提供结构，按需使用。

若用户要求先计划，先保存可审阅 Markdown 计划并等待确认；否则复杂任务可以简短记录范围和步骤，不把“新项目”本身当成强制审批理由。用户已批准的计划无需重新批准。

## 按实际依赖推进

| 当前需要 | 入口与证据 |
|---|---|
| 找问题、文献、数据 | `/discover`；产物进入 literature/data-assessment 或 brief |
| 解释机制、识别与主线 | `/strategize`；strategy/theory 明确条件与未知 |
| 理解陌生概念或工具 | `/learn`；先直觉、再推导、最后回到项目 |
| 实现已定的分析 | `/analyze`；关键样本、规格和输出可追溯 |
| 提纲、草稿、编辑 | `/write`；按语言、体例、领域与读者选择，不以代码完成为所有写作的前提 |
| 核验与独立审查 | `/review`、`/tools`；按主张所需证据检查 |
| 报告、修订或提交准备 | `/talk`、`/revise`、`/submit`；沿用用户指定主稿与授权范围 |
| 交接 | `/checkpoint`；更新最少状态与下一步 |

已有证据可以直接进入写作，纯理论无需先完成数据环节。需要真实结果支持的段落必须等待可靠输出，暂不能支持的主张使用明确占位。不能用综合分或 agent 意见自动替研究者选贡献、主样本、主规格或投稿目标。

## 每个阶段结束时

说明获得了什么、证据的局限、当前主线及首选下一步。给陌生工具的学习入口，必要时提出有机制和最小检验的新方向。分支暂存及重开条件在已有材料中简短记录，不为每个灵感启动完整 pipeline。

常规工作在已有授权内继续；重大路线变化先准备证据、备选与成本供 Hongbo 判断。公开发布、对外发送、登记或正式投稿依照明确授权执行，项目初始化本身不授权创建远端或上传研究内容。检查按 `PASS` / `FAIL` / `NOT_RUN` / `NOT_APPLICABLE` 记录，输入变化的旧判断标 `STALE`。
