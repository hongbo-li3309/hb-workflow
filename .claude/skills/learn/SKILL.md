---
name: learn
description: Teach an economic concept, model, or research method through intuition, a toy model, assumptions, derivation, and implications for the current project. Use when a new tool could expand the research agenda.
argument-hint: "[concept, model, paper, or research difficulty]"
allowed-tools: Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,Agent
---

# Learn

输入：`$ARGUMENTS`。学习是研究工作的核心部分。帮助 Hongbo 掌握能扩展问题边界的方法，不以当前熟悉程度限制研究方向。

若与当前项目有关，先读 `research/PROJECT_BRIEF.md` 和必要材料；独立学习无需先建项目文件。按需读 [研究协作](../../references/research-collaboration.md) 与 [方法参考](../../references/research-methods.md)。默认中文解释，保留标准英文术语。

## 解释顺序

1. **问题。** 这个概念解决什么经济问题；现有直觉或方法卡在哪里；新工具多回答了什么。
2. **最小例子。** 选 toy model 或具体数据例子，说明参与者、目标、约束、选择和时序。先让对象可理解，再引入一般符号。
3. **推导。** 列关键假设，从定义走到关键式子；区分数学推论与经济解释。不以“显然”省去真正的难点，也不为每一步基础代数打断主线。
4. **识别与应用。** 什么能观察，什么需要假设，哪些参数可识别；区分校准、估计、预测和因果结论。
5. **边界。** 给一个反例、边界情形或竞争模型；说明何时换方法，复杂度与学习成本如何。
6. **下一步。** 将方法连接到当前问题的一个可检验预测、估计对象或最小复现；提供一两份核验过的原论文/作者材料。可给一个简短练习，不强制测验。

按用户反馈加深到证明、均衡、动态选择、结构识别、计算或应用。可调用 `theorist` 处理经济模型/正式推导，`strategist` 讨论识别，`librarian` 找原始材料；仅在独立子任务确有价值时委派。

## 准确与留存

新颖或不熟悉的实质方法断言，核验原论文与作者文档。区分读过全文、读过部分和依据摘要；没有访问能力时说清未核验部分。代码/模拟只在有意义且可执行时使用，未运行写 `NOT_RUN`；数值吻合不能称为证明。

toy model 的假定值和结论标明“教学示例”，不写进项目结果。重要推导检查条件、单位、极限/边界与反例；发现困难时解释尚缺哪一步，不伪装为已证。

只有有复用价值时保存 `research/learning/<topic>.md`，内容保留问题、推导、边界、原始来源和对项目的含义。与主线有关的洞见回链 brief；新方向先作为候选，不自动改变研究计划。
