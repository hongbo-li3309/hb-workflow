# new-paper — 保留原命令，使用唯一项目模板

原先内嵌大段 `CLAUDE.md` 的函数容易与库规则漂移。现在正文统一来自 `templates/project-claude.md`，执行由 `scripts/new_project.py` 完成。本文件按当前工作稿改写，未改你机器上的 `~/.zshrc`。

可以直接运行：

```bash
python3 ~/claude-workflow/scripts/new_project.py ~/Research/paper-my-question --lang stata
```

如需继续使用 `new-paper`，将下面函数用于你的shell配置；现有全局函数不会随仓库更新自动变化：

```zsh
new-paper() {
  if (( $# == 0 )); then
    print -u2 'Usage: new-paper <name> [--lang stata|python|r|julia] [--git|--no-git]'
    return 1
  fi
  local research_project_name="$1"
  shift
  if [[ "$research_project_name" == */* || "$research_project_name" == '.' || "$research_project_name" == '..' ]]; then
    print -u2 'Use a project name; for an explicit path call new_project.py directly.'
    return 1
  fi
  python3 "$HOME/claude-workflow/scripts/new_project.py" "$HOME/Research/$research_project_name" "$@"
}
```

原有 `--lang`、`--no-git` 继续可用；默认只建本地文件，`--git`显式建立本地Git仓库，不自动commit/push。拒绝已存在目录或symlink，不建议先删除旧项目来重试。支持含空格项目名，调用时加引号。

Claude项目不会复制 `gpt-workflow/`、私人settings/state、历史计划或旧Git记录。Stata setup要求从新项目根运行并检查入口文件，不写死这台机器路径。只生成所选语言的最小骨架；没有数据就没有回归或论文结果。

GPT/Codex版使用 `gpt-workflow/scripts/new_project.py` 及该目录内的说明，两者不要混装。
