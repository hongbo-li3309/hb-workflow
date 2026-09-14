# 最少的文件与Git知识

一个论文项目是一个独立目录。`data/raw/`存原始数据，`data/cleaned/`存规范数据，`scripts/`存分析逻辑，`paper/`是新LaTeX项目的默认稿件位置；指定的其他主稿格式与路径同样适用。`research/PROJECT_BRIEF.md`解释现在为什么做这些工作。

常用只读命令：

```bash
pwd
git status --short
git diff
git log -5 --oneline
```

修改后看diff：是否只改了任务需要的内容，数字/单位/因果措辞是否变化，是否保留你的已有工作。暂存具体文件，不把数据、凭据和旧未跟踪文件一起加入。

```bash
git add path/to/reviewed-file
git commit -m "Describe the concrete change"
```

push会改变远端，只有明确要推送时执行；不使用强推修补常规问题。Git能记录已提交版本，不能自动保住所有未提交和未跟踪文件。重要主稿另存修订版本与diff。
