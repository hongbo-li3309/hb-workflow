# Codex 研究 skill 模板

在 `.agents/skills/<name>/SKILL.md` 中使用，名称与目录一致。description 说明任务和适用时机；不写平台专用工具白名单或命令参数占位。实际工具以当前会话为准。

```markdown
---
name: your-skill-name
description: Describe the concrete research task and when this skill should be used.
---

# Your skill

Read the target and relevant project context. State the intended output, evidence and authorized scope.

## Work

Explain the essential decisions. Link conditional detail to a project-local reference and read it only when relevant. Assign explicit files if delegating; use serial work when independent agents are unavailable.

## Verify and hand off

Check the actual risk. Distinguish static inspection, execution and scientific judgment. Missing tools mean NOT_RUN; old evidence after changed inputs is STALE. Return artifacts, scope, limits and the most useful next step.
```

按需提供脚本或参考，不为每个技能添加额外层级。复杂技能用真实场景独立核验；模板解析通过不等于模型行为已验证。当前用户指定路径与授权优先，不自动安装到个人全局技能目录。
