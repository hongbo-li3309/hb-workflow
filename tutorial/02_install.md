# 环境与工具

本库不自动安装客户端、依赖或改全局设置。先用实际安装与官方说明确认能力。

| 工具 | 什么时候需要 | 检查 |
|---|---|---|
| Python 3 | 初始化和工作流测试 | `python3 --version` |
| Claude Code | Claude版研究技能 | `claude --version` |
| Git | 版本管理 | `git --version` |
| Stata及许可 | Stata分析实际运行 | 在本机Stata确认版本与执行方式 |
| LaTeX | 编译LaTeX稿件 | `latexmk -v` |
| Quarto | 渲染guide或Quarto稿 | `quarto --version` |

Claude安装与认证见 [官方Quickstart](https://code.claude.com/docs/en/quickstart)。账户能用哪些模型、工具和认证方式以当前实际环境为准。

Stata可以通过已配置的MCP或本地batch执行。先确认连接提供的工具名和Stata路径，不能因模板出现`stata-mcp`就认为已连接。不同连接器的传输、端口和工具名由其实际文档决定；不要强制采用旧教程的localhost端口。最终分析仍保存为`.do`脚本。

Python/R/Julia依赖在真实项目需要时准备。记录版本与来源，Stata用户包需固定实际ado环境；安装成功不证明分析正确。认证信息只放本地配置，不粘进仓库。

GPT版的配置单独看 [说明](../gpt-workflow/README.md)，本教程不会向全局Codex目录安装技能。
