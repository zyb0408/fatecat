# Planning Summary
以 gate-first 方式推进：先修当前本地阻塞，再补生产准入，再扩测试和边界，再推进八字解释与维护性，最后用 full review 和 ship gate 收口。
- 编译节点总数: 38
- 叶子执行项: 30
- 执行波次数: 11
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：当前质量缺口、目标 100% gate、真实/惯性约束已记录。
- PLAN：任务树、依赖、执行波次和 next executable leaves 由 auto-tasks 生成。
- BUILD：后续只按当前 wave 的叶子节点执行，不混入无关重构。
- TEST：每个叶子节点必须记录命令输出或明确未执行原因。
- REVIEW：每个 package 结束后运行对应 auto-review profile；最终执行 full/release gate。
- SHIP：只有全部 BLOCK 为零、外部 HITL 关闭或明确豁免，才允许宣称 100%。
- 不得跳过 gate；未闭合当前 gate 前不得进入后续阶段或宣称质量 100%。

# Simplest Path
第一波只修格式、REVIEW 和本地 quick gate；第二波补 production readiness 配置与 Bot/API 边界；后续按可验证 vertical slice 推进核心质量。

# Split Strategy
按质量标准和发布路径拆成八个 package；叶子任务优先 vertical slice，每个都绑定 verify 和 gate；外部生产验收单独隔离为 HITL。

# Execution Waves
- Wave 1: TP-01.01
- Wave 2: TP-01.02
- Wave 3: TP-01.03
- Wave 4: TP-02.01, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.04, TP-05.01, TP-06.01, TP-06.02
- Wave 5: TP-02.02, TP-03.04, TP-04.03, TP-05.02, TP-05.04, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03
- Wave 6: TP-02.03, TP-04.02, TP-07.04
- Wave 7: TP-05.03
- Wave 8: TP-05.05
- Wave 9: TP-08.01
- Wave 10: TP-08.02
- Wave 11: TP-08.03

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 优先 P0/P1 阻塞项；P2 长期优化不得阻塞本地质量 100%。
- 全局预算: 每个执行波次结束必须保留 git diff、测试输出、review evidence。
- 全局停止条件: 需要真实公网 URL 或 Bot token 但未提供时，停止对应 HITL 叶子，不伪造通过。
- 全局停止条件: 命理核心输出变化但 golden/oracle 无法解释时，停止迁移，进入 debug/review。
- 全局停止条件: local-ci 或 full acceptance 出现未知失败时，转 auto-debug。
- 需要审批: 真实生产部署、真实 Bot token 使用、push 远端、公开域名配置、删除 legacy 兼容入口。
- TP-02.03: tools=default; forbidden=none; evidence=default; budget=default; stop=缺少 real-url 或 real bot token 时停止，不伪造证据。

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: format check 0 退出码，git diff 只包含格式化变更。

# Dependency Graph
TP-01.01 -> TP-01.02
TP-01.01 -> TP-01.03
TP-01.02 -> TP-01.03
TP-01.03 -> TP-02.01
TP-01.03 -> TP-02.02
TP-02.01 -> TP-02.02
TP-01.03 -> TP-02.03
TP-02.02 -> TP-02.03
TP-01.03 -> TP-03.01
TP-01.03 -> TP-03.02
TP-01.03 -> TP-03.03
TP-01.03 -> TP-03.04
TP-03.01 -> TP-03.04
TP-01.03 -> TP-04.01
TP-01.03 -> TP-04.02
TP-03.04 -> TP-04.02
TP-04.01 -> TP-04.02
TP-01.03 -> TP-04.03
TP-04.01 -> TP-04.03
TP-01.03 -> TP-04.04
TP-01.03 -> TP-05.01
TP-01.03 -> TP-05.02
TP-04.01 -> TP-05.02
TP-05.01 -> TP-05.02
TP-01.03 -> TP-05.03
TP-04.02 -> TP-05.03
TP-05.01 -> TP-05.03
TP-01.03 -> TP-05.04
TP-03.02 -> TP-05.04
TP-03.03 -> TP-05.04
TP-05.01 -> TP-05.04
TP-01.03 -> TP-05.05
TP-05.03 -> TP-05.05
TP-05.04 -> TP-05.05
TP-01.03 -> TP-06.01
TP-01.03 -> TP-06.02
TP-01.03 -> TP-06.03
TP-06.01 -> TP-06.03
TP-06.02 -> TP-06.03
TP-01.03 -> TP-06.04
TP-04.01 -> TP-06.04
TP-02.01 -> TP-07.01
TP-03.03 -> TP-07.01
TP-02.01 -> TP-07.02
TP-03.03 -> TP-07.02
TP-02.01 -> TP-07.03
TP-03.03 -> TP-07.03
TP-02.01 -> TP-07.04
TP-02.02 -> TP-07.04
TP-03.02 -> TP-07.04
TP-03.03 -> TP-07.04
TP-07.01 -> TP-07.04
TP-07.03 -> TP-07.04
TP-02.03 -> TP-08.01
TP-04.02 -> TP-08.01
TP-05.05 -> TP-08.01
TP-06.03 -> TP-08.01
TP-07.04 -> TP-08.01
TP-02.03 -> TP-08.02
TP-04.02 -> TP-08.02
TP-05.05 -> TP-08.02
TP-06.03 -> TP-08.02
TP-07.04 -> TP-08.02
TP-08.01 -> TP-08.02
TP-02.03 -> TP-08.03
TP-04.02 -> TP-08.03
TP-05.05 -> TP-08.03
TP-06.03 -> TP-08.03
TP-07.04 -> TP-08.03
TP-08.02 -> TP-08.03

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
