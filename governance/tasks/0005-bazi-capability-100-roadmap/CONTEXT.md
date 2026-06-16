# Repo Evidence

- 当前基线来自 `governance/tasks/0004-bazi-professional-system-100/SCORECARD.md`。
- 当前 final review 来自 `governance/tasks/0004-bazi-professional-system-100/FINAL_REVIEW.md`。
- 当前缺口台账来自 `governance/tasks/0004-bazi-professional-system-100/RULE_SOURCE_GAPS.md`。
- 当前样本外失败归因来自 `governance/tasks/0004-bazi-professional-system-100/MINGLI_FAILURE_TAXONOMY.md`。
- 当前资源边界来自 `governance/tasks/0004-bazi-professional-system-100/RESOURCE_MAP.md`。
- 当前任务树 `0004` 已 closeout，但 `governance/tasks/INDEX.md` 仍有历史状态滞后，需要后续治理时同步修正。

# Constraints Matrix

| 约束 | 决策 |
| --- | --- |
| 不能伪造 100% | 100% 只代表工程与专业验收成熟度，不代表预测准确率 100%。 |
| 不能答案泄漏 | benchmark 任务必须 no-leak，禁止读取 expected/answer/correct/gold/label。 |
| 不能混用资源角色 | production/oracle/evaluation/reference/future_candidate 必须分层。 |
| 不能输出高风险现实处方 | 医疗、金融、法律、心理、灾祸、婚姻确定断语必须被 policy regression 拦截。 |
| 不能大爆炸重写 | 每次只迁移一个 evaluator 或规则切片。 |
| 不能改 delivery 算命逻辑 | delivery 只消费结构化结果，不新增领域算法。 |

# Change Boundary

- 本任务只设计计划和任务树。
- 后续实现任务允许改动 `contracts/fate/`、`domains/fate-analysis/`、`tests/regression/`、`governance/tasks/`。
- 后续实现任务不得把 oracle/evaluation/reference 资源接入生产请求链路。
- 后续实现任务若涉及架构移动，必须更新相应目录 `AGENTS.md`。

# Risk Matrix

| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| 把 benchmark 分数当专业能力 | High | `TP-10` 强制 no-leak 和 failure taxonomy，不以题号/答案调参。 |
| 高级格局缺专家样本仍 production | High | `TP-05` 缺正反边界例时只能 beta/HITL。 |
| 岁运专题输出确定未来 | High | `TP-08` policy regression 先行。 |
| 排盘边界差异不可解释 | High | `TP-02` oracle mismatch report 作为 gate。 |
| golden corpus 过慢拖垮日常 CI | Medium | `TP-09` quick/deep/release 分层。 |
| 大文件继续膨胀 | Medium | `TP-11` evaluator 物理拆分。 |

# Assumptions and Falsification

- 假设：`lunar-python` 继续作为 production provider。若升级后 calendar/oracle/golden 失败，必须暂停升级并写 mismatch report。
- 假设：MingLi/BaziQA 只作为 evaluation。若发现生产代码读取 benchmark 数据，直接 BLOCK。
- 假设：100% 是验收成熟度。若用户要求预测准确率 100%，该目标不可承诺，必须改写为可验证阈值。
- 假设：没有授权专家命例时不编造样本。若某规则缺来源，只能 reference/beta/HITL。

# Critical Ambiguities

- 是否有可授权的专家命例库：当前未知，计划以 HITL gate 表达。
- BaziQA 远端 license 与本地历史审查不完全一致：必须重新 admission。
- MingLi 最终 accuracy 阈值需要基于多轮无泄漏提升确定；本计划只设阶段目标，不承诺 100% 命中。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务是计划设计，不需要 `DEBUG.md`。
- 后续如果 implementation gate 出现 regression、flaky、CI-only 或 benchmark 泄漏，必须新建或更新对应任务 `DEBUG.md`。

# Task Package Context Map

| Context | 读取文件 |
| --- | --- |
| 基线百分比 | `SCORECARD.md` |
| 规则缺口 | `RULE_SOURCE_GAPS.md` |
| 资源边界 | `RESOURCE_MAP.md` |
| 样本外失败 | `MINGLI_FAILURE_TAXONOMY.md` |
| 收口口径 | `FINAL_REVIEW.md`、`CLOSEOUT.md` |
