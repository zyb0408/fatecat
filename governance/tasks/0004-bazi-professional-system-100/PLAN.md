# Planning Summary
按终态倒推：先锁定 100% scorecard 和资源边界，再补基础历法、证据契约、常规分析、高级格局、合化、用神、岁运专题、golden benchmark，最后做维护性拆分和 release review。
- 编译节点总数: 41
- 叶子执行项: 31
- 执行波次数: 20
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：锁定 100% 定义、真实约束、惯性约束和禁止伪装口径。
- PLAN：任务树、依赖、执行波次、验收标准和 next executable leaves 全部落盘。
- BUILD：按叶子节点逐项执行，不能跳到后续 package 先做结果包装。
- TEST：每个叶子节点必须有命令、样本、diff 或 HITL evidence。
- REVIEW：每个 package 完成后做 auto-review，重点检查 future-optimal-drift、ponytail-complexity、benchmark leakage 和 unsafe output。
- SHIP：只有全部 P0/P1 gate 关闭且 final review 无 BLOCK，才允许把专业体系验收标为 100%。
- 不得跳过 gate；未闭合当前 gate 前不得进入后续阶段或宣称质量 100%。

# Simplest Path
不换主链、不引入重型规则引擎；优先复用现有 lunar-python、contracts registry、fate-core evaluator、golden matrix、MingLi evaluation，并按缺口逐项补规则、测试和证据。

# Split Strategy
按 10 个完成度维度拆顶层 package；每个 package 下面只保留可直接执行的 vertical slice 叶子任务；所有 leaf 都有 verify、gate、输出物和依赖。

# Execution Waves
- Wave 1: TP-01.01, TP-01.02
- Wave 2: TP-01.03
- Wave 3: TP-02.01, TP-02.02, TP-03.01, TP-03.02
- Wave 4: TP-02.03, TP-03.03
- Wave 5: TP-04.01, TP-04.02
- Wave 6: TP-04.03
- Wave 7: TP-05.01, TP-05.02, TP-06.01
- Wave 8: TP-05.03, TP-06.02
- Wave 9: TP-06.03
- Wave 10: TP-07.01
- Wave 11: TP-07.02
- Wave 12: TP-07.03
- Wave 13: TP-08.01
- Wave 14: TP-08.02
- Wave 15: TP-08.03
- Wave 16: TP-09.01, TP-09.02, TP-09.03
- Wave 17: TP-09.04
- Wave 18: TP-10.01
- Wave 19: TP-10.02
- Wave 20: TP-10.03

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局停止条件: 发现 benchmark answer leakage，立即停止 benchmark 提升任务并回滚泄漏路径。
- 全局停止条件: 核心排盘结果与 oracle/golden 不一致且无法解释，停止相关 evaluator 迁移。
- 全局停止条件: 专家样本或资料 license 不清，相关规则只能停在 reference/beta，不得 production 化。
- 全局停止条件: 高风险专题出现现实处方或保证式话术，停止报告发布并补 policy regression。
- 需要审批: 引入新的生产依赖。
- 需要审批: 删除旧 public facade 或兼容入口。
- 需要审批: 把 beta topic profile 升级为 production。
- 需要审批: 纳入外部专家命例或未确认版权资料。

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: 每个维度都有 current、target、verify、falsifier、owner、next threshold。
- TP-01.02 | Wave 1 | Depends On: 无 | Gate: production/oracle/evaluation/reference/future_candidate 边界不混写。

# Dependency Graph
TP-01.01 -> TP-01.03
TP-01.02 -> TP-01.03
TP-01.03 -> TP-02.01
TP-01.03 -> TP-02.02
TP-01.03 -> TP-02.03
TP-02.01 -> TP-02.03
TP-02.02 -> TP-02.03
TP-01.03 -> TP-03.01
TP-01.03 -> TP-03.02
TP-01.03 -> TP-03.03
TP-03.01 -> TP-03.03
TP-03.02 -> TP-03.03
TP-02.03 -> TP-04.01
TP-03.02 -> TP-04.01
TP-02.03 -> TP-04.02
TP-03.02 -> TP-04.02
TP-02.03 -> TP-04.03
TP-03.02 -> TP-04.03
TP-04.01 -> TP-04.03
TP-04.02 -> TP-04.03
TP-04.03 -> TP-05.01
TP-04.03 -> TP-05.02
TP-04.03 -> TP-05.03
TP-05.01 -> TP-05.03
TP-05.02 -> TP-05.03
TP-04.03 -> TP-06.01
TP-04.03 -> TP-06.02
TP-06.01 -> TP-06.02
TP-04.03 -> TP-06.03
TP-06.02 -> TP-06.03
TP-04.01 -> TP-07.01
TP-04.03 -> TP-07.01
TP-06.03 -> TP-07.01
TP-04.01 -> TP-07.02
TP-04.03 -> TP-07.02
TP-06.03 -> TP-07.02
TP-07.01 -> TP-07.02
TP-04.01 -> TP-07.03
TP-04.03 -> TP-07.03
TP-06.03 -> TP-07.03
TP-07.02 -> TP-07.03
TP-04.02 -> TP-08.01
TP-05.03 -> TP-08.01
TP-07.03 -> TP-08.01
TP-04.02 -> TP-08.02
TP-05.03 -> TP-08.02
TP-07.03 -> TP-08.02
TP-08.01 -> TP-08.02
TP-04.02 -> TP-08.03
TP-05.03 -> TP-08.03
TP-07.03 -> TP-08.03
TP-08.02 -> TP-08.03
TP-08.03 -> TP-09.01
TP-08.03 -> TP-09.02
TP-08.03 -> TP-09.03
TP-08.03 -> TP-09.04
TP-09.02 -> TP-09.04
TP-09.01 -> TP-10.01
TP-09.03 -> TP-10.01
TP-09.04 -> TP-10.01
TP-09.01 -> TP-10.02
TP-09.03 -> TP-10.02
TP-09.04 -> TP-10.02
TP-10.01 -> TP-10.02
TP-09.01 -> TP-10.03
TP-09.03 -> TP-10.03
TP-09.04 -> TP-10.03
TP-10.02 -> TP-10.03

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
