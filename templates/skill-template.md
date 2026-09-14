# Claude skill 模板

在 `.claude/skills/<name>/SKILL.md` 中使用，名称与目录一致。写清何时使用与真正改变决策的规则，不堆通用提醒。保留自然语言调用。

```markdown
---
name: your-skill-name
description: Describe the concrete research task and when this skill applies.
argument-hint: "[task or target]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent
---
# Your skill

Read the actual target and relevant project context. State the output and preserve the user's scope.

## Workflow
Explain the essential decisions. Link substantial conditional detail to a relevant reference. Use only tools actually available and only write the assigned files.

## Verification
State how to check the result and distinguish execution evidence from judgment. Missing tools mean NOT_RUN, not PASS.

## Example
Give one representative task and its expected useful output. Do not hardcode its research conclusion.
```

按实际需要裁剪工具，不声称只读agent已执行代码。实质修订用一个正常任务和一个易失败案例验证行为；发现率和文风改善不能用未经测量的百分比宣称。
