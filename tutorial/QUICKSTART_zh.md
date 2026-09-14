# 从一个研究问题开始

本库原位置是Claude版；[gpt-workflow](../gpt-workflow/README.md)是独立GPT/Codex版。选择一版创建项目，避免混装。

## 已有Claude Code

在本库运行：

```bash
python3 scripts/new_project.py ../paper-my-question --lang stata
```

在新项目目录打开Claude Code，输入：

> 我的问题是……。先解释重要的经济机制和相邻文献，帮我明确最有信息价值的下一步。把事实、你的推测和待我决定的事项分开。

初始只有项目说明、工具骨架和一页主线，不会自动生成论文结论。`--lang python`、`r`、`julia`也支持；已有数据或主稿按你指定的路径工作。

## 常用的四个动作

- 想方向：`/discover brainstorm`；跟进文献：`/discover frontier`。
- 学方法：`/learn 搜寻匹配模型与这个项目的关系`。
- 写作：`/write` 加主稿、语言、读者和目的；研究类型不同，组织方式也不同。
- 收工：`/checkpoint`。下次先读 `research/PROJECT_BRIEF.md` 和指向的证据。

需要你判断的是核心问题、主要估计对象、影响解释的主规格和重大投入。日常实现、修复和必要检查在已授权范围内继续。计划批准后无需为普通步骤重复确认。

## 还没安装

先按 [官方Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) 安装、认证，再按 [环境说明](02_install.md) 检测。不要复制旧教程的固定订阅、端口或版本承诺。Stata和LaTeX只在对应任务需要时配置。

原 `new-paper` 命令可按 [cheatsheet](../cheatsheets/new-paper-function.md) 接到同一个生成器；仓库更新不会自动改 `~/.zshrc`。确认生成目录后再自行配置项目远端；初始化不上传数据或提交论文。
