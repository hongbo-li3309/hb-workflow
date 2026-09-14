# 研究与写作行为审阅及合成示范

日期：2026-09-13。范围：更新后的 Claude 根入口、rules、研究和写作模块，以及它们与分析/核验产物的契约。本文由本次独立审查会话读取这些文件后实际完成示范与核对；**不是 Claude Code 或 GPT/Codex 原生客户端的自动集成测试**，也不是对模型稳定性的认证。可重复任务见 [behavior_cases.md](../../tests/behavior_cases.md)。

## 实际完成与未覆盖

| 工作 | 状态 | 证据与范围 |
|---|---|---|
| 根指令、协作/状态/角色与写作规则静态对照 | PASS | 实际读取 CLAUDE、全部相关 rules、研究/写作 skills 与 agents、两类 references 及核心状态模板；发现的日志路径冲突已修复并重读核对，见下 |
| 对数与百分点换算 | PASS | 本会话实际用 Python math.exp 核算；具体结果见共同事实表 |
| 四体例文字及 brainstorm / 教学示范 | PASS | 本文给出本次实际撰写的完整示范，并逐项核对证据强度；只涵盖这些示范 |
| 近期文献有限检索 | PASS | 实际检索得到 NBER 一手页面的索引摘要和版本信息；直接 open 三页均返回 403，完整页面/全文精读为 NOT_RUN |
| 无效引用处理 | PASS | 对标题与 DOI 作精确检索；返回内容无匹配原论文，未补造元数据或引用 |
| 两期教学模型数值/边界 | PASS | 实际用 Python 核对四组参数的净值；公式人工推导，不是形式化证明器验证 |
| Claude Code 原生模型行为、技能发现、工具委派 | NOT_RUN | 本审阅会话未启动该客户端的独立行为运行；须由主线程另行记录 |
| 独立 GPT/Codex 迁移后的原生行为 | NOT_RUN | 尚未在独立复制的目标项目重放这些任务；不能沿用本次 Claude 指令审阅代替 |
| 原始研究估计复现、样本/SE核验 | NOT_RUN | 只有合成统计量，无真实数据/代码/运行记录 |
| 论文编译和 Word/PDF 视觉格式 | NOT_APPLICABLE | 本次产物是 Markdown 示范，没有指定论文主稿或版式交付 |

这里的 PASS 只说明列明工作确实完成及相应结果，不能认证所有八项用户目标在所有未来任务中必然满足。没有综合分或自动晋级。

## 规则与契约发现

**发现 1：执行记录存放位置不一致。** `.claude/rules/logging.md` 要求原始执行日志放 `quality_reports/runs/`；审阅当时 analyze skill 的说明/示例和 verifier 的说明/示例却将记录放在 reviews 附近。已向主线程指出原句和位置；runtime 模块完成修复后，本会话重新读取这三个文件，确认说明及两个 run_check 示例均统一到 runs，审查报告仍在 reviews。状态从发现时 FAIL 改为修复后 PASS；这是文档契约复查，不代替 run_check 的运行测试。

**未发现三份状态材料成为强制前置条件。** 根入口、research-collaboration、new-project、write 和模板明确只按需建立；新项目通常只有约一页 brief，重要证据/决定出现后再增加 ledger/decisions。局部改句可以直接交付，不要求先填表。需要在真实客户端 B2/B6 案例继续防止模型把“按需”解释成每轮都保存。

**AI 推荐和用户批准已有一致边界。** 根规则与研究模块使用 proposed / approved / superseded，重大主问题/estimand/主样本/主规格变化需用户决定；已授权的常规修复继续。checkpoint 的项目指针不是新授权，未知 session_id 不得推测或继承其他会话授权。下面的示范没有把候选写成已批准研究路线。

**角色工具与报告职责可成立。** 研究 critics 配置 Write 但限定自己的报告；writer-critic、方法/领域 referees 的工具只读并返回报告，由主线程保存。两种方式都与各自工具一致；不能要求只读 critic 亲自写文件或运行软件。Agent 工具已统一，现有角色名未改变。

**方法与写作口径已对齐。** BJS 异质性、sensemakr 归属、AEA registration/preregistration 已按原始来源纠正。前趋势不显著不能证实平行趋势，系数/样本/单位/因果强度不能被去 AI 味修改。纯理论和描述/测量都有入口，校准不被冒称估计。具体状态适用范围仍需实际任务判断。

## 合成事实与算术核验

**以下统计量、模型参数和无效文献都是人工构造的演练输入，不是真实项目发现。** A 是二元 AI 采用变量；工资因变量为自然对数，就业率按 0–1 计量。原始样本单位、规模、年份、控制集、SE 构造及采用的识别来源均未给出，不能自行补造。

| 输入或变换 | 核对结果 | 解释边界 |
|---|---:|---|
| log wage 系数 / SE | 0.04 / 0.02 | 观察性回归关联 |
| `100 × (exp(0.04) − 1)` | 4.0810774% | 相应对数差的指数转换；可解释几何均值之比，不能无条件说算术均值工资效应 |
| 就业率系数 / SE | 0.04 / 0.015 | 0–1 尺度 |
| 换算为百分点 | 4 / 1.5 个百分点 | 基准就业率未知，不能报告相对就业增幅 |
| 前趋势联合检验 | p = 0.40 | 未拒绝相应零假设，不证明平行趋势或内生采用已解决 |

本会话也核对了 `beta ± 1.96 × SE` 的纯算术结果，但没有将其当作已验证置信区间写进段落：未给抽样结构、自由度或适用推断条件。给定系数和 SE 可准确重述，不能因此认证原估计或统计显著性。

## 四种体例的实际示范

下面各段都仅用于展示写法。工资与就业率是两个回归对象，未声称它们使用相同可见样本；假如工资只在就业者中观察，还需要另查选择与构成。

### 英文学术论文

AI adoption is positively associated with both wages and employment in these observational regressions. The coefficient on adoption is 0.04 in the log-wage regression (SE = 0.02), corresponding to a geometric-mean wage contrast of about 4.1% under the log specification. The employment-rate coefficient is 0.04 (SE = 0.015), a difference of 4 percentage points rather than 4%. These patterns do not identify the effect of adoption: firms or workers may select into AI use in response to prospects that also shape labor-market outcomes. The pre-trend test does not reject its null (p = 0.40), but this result alone establishes neither parallel trends nor exogenous adoption.

### 中文学术论文

观察性回归显示，AI 采用与工资和就业率均呈正相关。对数工资回归中的系数为 0.04，标准误为 0.02；将对数差作指数转换，对应的几何均值工资差异约为 4.1%。就业率回归的系数同为 0.04，标准误为 0.015，但其含义是就业率相差 4 个百分点，不能与工资的比例差异混写。两项结果尚不足以识别 AI 采用的因果影响，因为采用决策可能受同时影响劳动市场表现的预期和条件驱动。前趋势检验的 p 值为 0.40，只能说明未拒绝相应零假设，不能据此认定平行趋势成立。

### 中文政策报告

对于考虑支持 AI 采用的政策部门，当前更值得优先解决的是：这些正相关有多少来自技术本身，又有多少反映采用者原有的优势。示例数据中，采用 AI 对应的工资对数差为 0.04（标准误 0.02），指数转换后约为 4.1% 的几何均值差异；就业率则相差 4 个百分点（标准误 1.5 个百分点）。这些数值不能直接用作推广政策的预期收益。前趋势检验 p = 0.40 也没有解决这一问题。可考虑先核实采用时点与劳动结果的变化，并比较既有观察数据评估和小范围、可评估试点的成本；是否投入试点，应在明确数据条件和实施成本后另作判断。

### 英文政策报告

For policymakers considering support for AI adoption, the immediate question is whether the observed advantage reflects AI use or the circumstances of those who adopt it. The illustrative wage association is 0.04 in log units (SE = 0.02), equivalent to about 4.1% in geometric means; the employment-rate gap is 4 percentage points (SE = 1.5 percentage points). These are not estimates of the gains a support program would deliver. A pre-trend p-value of 0.40 does not resolve selection into adoption. A useful next step is to assess whether existing data can establish the timing of adoption and outcomes, then compare that option with a small, evaluable pilot before committing to broader support.

### 对照结果

四段共用事实清单，均没有把 adoption 改成外生处理，没有把工资写成百分点或将就业率换成无基准的相对增幅。学术段先讲结果与解释边界；政策段先讲读者所需判断和可选择的评估行动。中英段落的组织相近是因为证据相同，但句法和政策技术细节有所调整；这不是从真实中文政策范文精读所得的机构特定文风认证。

改写没有补出样本、年份、控制变量、全国影响或财政成本。政策试点是候选，不是已批准的新工程。纯文字工作不需要创建项目 brief、ledger、decisions；本轮只保存这份演练记录。

## Brainstorm：实际回答示范

我们现在知道的是：在给定回归里，AI 采用与工资、就业率的关系同为正。还不知道的是这种关联主要反映技术的净影响、采用选择，还是样本构成。当前主线可以暂写为“理解正相关从何而来”，不能写成“AI 已创造就业”。

| 候选解释 | 为何可能出现两项正相关 | 优先寻找的判别证据 |
|---|---|---|
| 生产率提升与需求扩张 | 节约成本或改善质量扩大产出，抵消部分任务的劳动节省；工资传导还取决于劳动力市场与分配 | 采用时点后的价格/销量/任务/工时变化；工资和产出之间的联系 |
| 选择与预期需求 | 本来有更好前景或互补能力的采用者，既更早采用也有更好劳动结果 | 采用前的规模、增长和组织投入；采用决策及宣布时间；可信的采用变化来源 |
| 构成变化 | 低工资岗位减少、高工资岗位占比上升，均值上升不代表同一劳动者加薪 | 留任者/流入/流出、同一劳动者工资、职位与工时变化；先确认数据是否允许追踪 |
| 雇佣边界或测量变化 | 内部岗位、外包、招聘渠道及采用定义变化，可能改变观测关系而非同一个经济对象 | 实际使用 vs 采用声明、招聘 vs 雇佣、内部人员 vs 承包工、样本覆盖变化 |

这里没有一种机制已被本例识别。工资和就业率的两个正系数本身也不能排除它们同时存在。

**有限的当期文献线索。** 2026-09-13 实际搜索了 `site.nber.org papers artificial intelligence employment adoption labor demand 2026`，以下信息来自搜索工具返回的一手 NBER 页面索引摘要；直接打开页面均返回 403，未读全文。它们可以帮助细化问题，不能用于宣称该方向已经完成前沿综述或新颖性验证。

| 文献与版本 | 摘要层面可用的线索 | 对本例的启发（本审阅推断） |
|---|---|---|
| Bick, Blandin, Deming & Schumacher，2026 年 8 月，*What Work Does Generative AI Do?*，[NBER 35677](https://www.nber.org/papers/w35677) | 摘要区分 exposure 与实际 adoption，以及同类任务内的采用差异 | 先核验采用变量测什么，再讨论谁采用；不把职业暴露直接当外生采用 |
| Bonney 等，2026 年 4 月，*The Microstructure of AI Diffusion*，[NBER 35141](https://www.nber.org/papers/w35141) | 摘要区分企业、业务职能、劳动者任务三个采用层次 | 净劳动结果可能与部署层次有关，测量应更具体 |
| Humlum & Vestergaard，2025 年 5 月、2026 年 3 月修订，*Still Waters, Rapid Currents*，[NBER 33777](https://www.nber.org/papers/w33777) | 摘要同时讨论工作内容调整与工资/工时的精确零结果 | 工作重组与工资/就业变化需要分别观察；不能预设平均结果必须上升 |

**我建议先做的只有一件事：** 对采用变量、两个结果样本和真实可用的时序作一个小型数据核查。先确认“采用”何时发生、工资与就业率对谁观察、是否能区分留任者与人员流动。现在没有原始数据，实际核查为 NOT_RUN，不能假报已经完成。如果能追踪，再做采用前后的描述图及构成分解，明确这仍不是解决内生性的因果设计；如果不能，就先把可支持的描述对象界定清楚，不直接申请新数据。

一个跨度较大的候选是把研究对象从就业数量转到**雇佣边界与控制权**：AI 降低协调或监督成本后，企业可能更容易使用外包，也可能收回任务。它连接组织经济学与平台劳动，方向并不预定；最小检验是判断现有数据能否同时观察内部人员、承包支付和任务分配。只有这些对象可测、且初步证据表明该机制能解释主结果时，才值得提交为新的研究路线。此处状态是 proposed，不是 Hongbo 已批准转向。

## 学习示范：“我不会动态模型”

不会动态模型不构成放弃这个问题的理由。先用一个两期模型看清“为什么现在采用”受未来收益影响，再判断研究是否真的需要完整动态结构估计。

考虑企业只有一次采用选择 a ∈ {0,1}。采用在第一期支付成本 K，当期新增利润为 b；因为学习和组织适配，第二期新增利润为 b + ℓ。折现因子为 β ∈ [0,1]。先假设成本和收益确定，价格与工资外生、没有后续退出/等待选择；这只是部分均衡教学模型。

第二期价值是 `V₂(a) = a(b + ℓ)`。第一期比较：

```text
V₁ = max_{a∈{0,1}} { a(b − K) + β V₂(a) }
采用的净现值 ΔV = b + β(b + ℓ) − K
采用条件：ΔV ≥ 0
```

这个式子比“当期收益超过成本才采用”多了一件事：企业会为未来的学习收益提前付费。令 b = 2、K = 10、ℓ = 8、β = 0.9，则当期净收益是 -8，两期净现值却为 1。因此采用是最优选择。参数全部是教学假设，没有校准或估计过。

本会话实际核算了边界：β = 0 时净值 -8；ℓ = 0 且 β = 0.9 时净值 -6.2；K = 12、其他取原值时净值 -1。这个模型让我们看到学习收益、折现与固定成本如何改变采用；没有证明现实 AI 会涨工资，也尚未建模劳动需求。

它与回归的联系是：更看好未来收益、成本更低或更容易学习的企业，会更可能采用。采用者后来的结果较好，可以同时反映选择和技术收益。下一步值得学的是如何把 `状态—当前选择—未来状态—价值函数` 对应起来，再引入一个必要的新因素，例如不确定需求或可选择的培训投入；不必立刻上高维 Bellman 方程和结构估计。

进一步学习可用 Sargent 与 Stachurski 的 [QuantEcon McCall 搜寻模型讲义](https://python.quantecon.org/mccall_model.html)：本次实际读取 Overview、模型设定、value function 与 Bellman equation 部分，未执行代码。用劳动者“现在接受工资还是继续等待”的选择练习价值函数，再迁回企业采用问题，经济对象更容易把握。

可先做一个小练习：在模型里画出 K 与 ℓ 的采用边界，并解释为何高学习收益的企业更愿意在本期采用。然后回到数据问：我们能观察成本、培训、采用时间或结果轨迹中的哪一部分？只有这些对象能帮助区分机制，才考虑建立更完整的动态研究；尚未确认前保留为学习与候选路线。

## 无效引用的实际处理

收到夹具 `Synthetic Reference (2026), “Universal Wage Gains from AI Everywhere”, DOI 10.0000/NOT-A-REAL-PAPER` 后，实际对完整题名和 DOI 作了精确检索。工具返回无关结果，没有匹配的原论文记录；没有把无关网页替作论文，也未补作者、期刊或 BibTeX。测试者已明确这是人为构造的无效条目。

可交付的回答是：“这条文献目前不能核实，不能据此主张 AI 总会提高工资或证明本文贡献。它不进入正式 bibliography；若后来提供真实原文，再核对版本与其实际支持的结论。现在可以继续分析给定关联和竞争机制。”真实检索中仅凭未找到匹配不应断言世界上不存在该研究，但更不能用一个听起来合理的引用补齐故事。

## 仍需后续核验的边界

原生客户端的技能加载、自动遵循、并行隔离和实际模型输出仍需两版分别测试；本报告没有提供这类证据。四体例示范遵循现有写作原则，尚未以 Hongbo 满意样稿或中文/政策原文做个人声音校准。有限文献检索没有阅读全文，不能支持本例的因果、新颖性或完整方法评议。

行为任务不应转变为每轮工作的额外检查表。今后共享研究规则、写作路由或平台能力改变时，挑受影响的案例重放；保留输出和失败证据，由研究者判断结果是否更有助于理解、创新与介入。
