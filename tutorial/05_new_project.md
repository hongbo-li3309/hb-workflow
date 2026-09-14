# 新建与迁移论文项目

Claude版使用库根目录的 `scripts/new_project.py`；GPT版使用独立目录内的同名脚本。两者读取各自的模板，不能相互替代。

```bash
python3 scripts/new_project.py ../paper-my-question --lang stata
```

支持含空格路径，给路径加引号。目标必须不存在；已有项目应走逐文件迁移。默认不初始化Git，`--git`显式初始化本地仓库，不创建commit或远端。

新项目生成所选语言的最小master/setup、原始/规范数据目录、稿件目录、研究主线模板和所选平台的skills。没有数据不会编造分析，作者信息不从Hongbo的维护者身份推断。

先填写PROJECT_BRIEF或与AI共同明确问题，再加入数据说明/主稿。Stata从项目根运行 `do "scripts/stata/00_master.do"`，setup检查根标志；Python运行 `python3 scripts/python/00_master.py`。

已有项目升级：记录当前改动→对照库版本→选择相关文件→保留个人style/agent/local settings→执行相关核验。不要删整个`.claude/`或覆盖主稿。旧 `new-paper` 函数的更新见 [cheatsheet](../cheatsheets/new-paper-function.md)，本次仓库更新不修改你的shell配置。
