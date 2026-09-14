---
name: revise
description: Handle economics R&R revisions by tracking referee comments, completing authorized changes, and drafting evidence-backed responses with reviewable manuscript versions.
---

# Revise

处理真实或明确标注的模拟 referee reports。保留 point-by-point response、评论分类、专业分工和 R&R 复审；不把修回任务变成未经授权的新研究项目。

## 读入与定位

读取报告、编辑信、用户指定主稿、现有 response letter、`references/protocols/revision.md` 和有关研究状态。确认轮次及本轮明确要求；编辑信优先级不等于可以忽略 referee 的每项问题。若主稿未明确且存在多个竞争版本，先完成报告梳理，再提出具体主稿问题。

按 referee 和原编号给每项评论稳定 ID。复合评论拆为子项且保留对应关系，简述诉求和原文位置；用户提供的报告可按需精确引用，不能捏造或改变对方意见。

## 分类并完成授权范围

| 类别 | 处理 |
|---|---|
| `NEW ANALYSIS` | 说明它解决何种疑问、成本与结果如何影响主线；已授权的必要可逆分析直接路由 coder／strategist，重要样本或 estimand 改变仍由作者决定 |
| `CLARIFICATION` | 检查真实方法与证据后由 writer 澄清；不能用更有说服力的语言掩盖识别缺口 |
| `REWRITE` | 提出结构或主张调整并给具体修订；改变核心问题／主结论的部分单列供作者判断 |
| `DISAGREE` | 起草有依据的回复与可行替代，不自动承诺让步；保留作者最终决定及已授权立场 |
| `MINOR` | 在已确认范围内直接修复，仍保留可审阅差异 |

已确认的授权不重复询问。对于影响研究方向或对外立场的未决选择，先准备建议、依据和修订候选，普通修改继续完成；不因存在一个待决定项停止整轮工作。

## 修订记录与回复

沿用已有 R&R 目录；无约定时在 `paper/revisions/<round>/` 保存 tracker、response letter 和修订稿／差异。主稿处理和版本命名遵循 revision rule，保留原格式，不默认把 Word 改成 LaTeX，也不擅自把候选稿升为主稿。

Tracker 只记必要信息：评论 ID 与位置、作者建议立场／已确认决定、行动及负责角色、证据或修改定位、响应状态（待处理／进行中／已完成／待作者决定）。验证状态另用 `PASS / FAIL / NOT_RUN / NOT_APPLICABLE`；状态“已回复”不等于证据已通过。必要证据变动后标 `STALE` 并重验相关主张。

回复信先概述实质变化，再逐项写：理解的问题、采取的行动、获得的证据、稿件位置。未完成分析保留 `[PENDING: 所需证据]`，不能写成“we have shown”。页码未重新渲染时使用稳定章节／表图定位并标页码待核。

不同意某意见时准确承认问题，再解释证据与适用边界，必要时给替代处理。礼貌不要求虚假赞同，不以“审稿人错了”代替论证。所有对外回复仍由作者确认；本技能不发送或投稿。

## 复审与交付

重大修订可委派原角色独立复审：逐一判断已解决／部分解决／未解决，以及什么证据能解决；因修订产生的新问题单列。新问题确有实质影响才扩展范围，不能换一套偏好无限抬高要求。

将本轮核验报告保存 `quality_reports/reviews/YYYY-MM-DD_<task>.md`。交付修订稿、差异、回复信、tracker 和待作者决定的少数关键项；说明完成哪些分析、哪些仅是文字改动及尚未运行的检查。重要研究决定链接到 `research/DECISIONS.md`，不重复抄录多份状态。
