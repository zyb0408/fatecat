# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-10.01 | Wave 14 | Depends On: TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | Gate: active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造 100%

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-00 | ROOT | 1 | - | No | Done | 2026-06-16：TP-00.02 SCORECARD.md 与 TP-00.03 BASELINE_EVIDENCE.md 均完成；版本与基线控制面已验收。 | 无 | 无 |
| TP-00.01 | TP-00 | 2 | - | No | Done | 2026-06-16：已提交 `1865e3d chore: checkpoint fatecat quality hardening`。 | 无 | 无 |
| TP-00.02 | TP-00 | 2 | TP-00.01 | No | Done | 2026-06-16：新增 SCORECARD.md；scorecard 关键字段检索通过；10 个维度均有 current%、target evidence、verify command、falsifier。 | 无 | 无 |
| TP-00.03 | TP-00 | 2 | TP-00.02 | No | Done | 2026-06-16：新增 BASELINE_EVIDENCE.md；MingLi 2025 sample10 answered 10/10、correct 3、accuracy 30.00%；local-ci quick PASS，focused regression 47 passed。 | 无 | 无 |
| TP-01 | ROOT | 1 | TP-00.01, TP-00.02, TP-00.03 | No | Done | 2026-06-16：TP-01.01 RESOURCE_MAP.md 与 TP-01.02 RULE_SOURCE_GAPS.md 均完成；资源角色和规则来源覆盖已验收。 | 无 | 无 |
| TP-01.01 | TP-01 | 2 | TP-00.01, TP-00.02, TP-00.03 | No | Done | 2026-06-16：新增 RESOURCE_MAP.md；Verify 通过；reference manifest policy tests 3 passed。 | 无 | 无 |
| TP-01.02 | TP-01 | 2 | TP-00.01, TP-00.02, TP-00.03, TP-01.01 | No | Done | 2026-06-16：新增 RULE_SOURCE_GAPS.md；规则 JSON 校验通过；43 个引用的 bazi sourceRuleId 均能回指现有 classics/rule-depth 资产。 | 无 | 无 |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02 | No | Done | 2026-06-16：TP-02.01/TP-02.02/TP-02.03 均完成；基础排盘与时间边界 golden、oracle 隔离、deep gate 预算已验收。 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-01.01, TP-01.02 | No | Done | 2026-06-16：新增 CALENDAR_ORACLE_AUDIT.md；Verify `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q` 通过，10 passed in 71.82s。 | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-01.01, TP-01.02, TP-02.01 | No | Done | 2026-06-16：`calendar_boundary_cases.json` 从 4 条扩到 9 条；新增秒级立春、DST/纽约、非整点时区/加德满都、女性起运边界；三组 regression 19 passed, 1 skipped。 | 无 | 无 |
| TP-02.03 | TP-02 | 2 | TP-01.01, TP-01.02, TP-02.02 | No | Done | 2026-06-16：新增 GOLDEN_DEEP_GATE.md；quick `9 passed, 1 skipped in 29.44s`；shard0 `10 passed in 578.31s`，75 cases，无 over-budget case。 | 无 | 无 |
| TP-03 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：TP-03.01/TP-03.02/TP-03.03 均完成；高级格局 contract、evaluator、golden 反例已验收。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.pattern.regular_vs_special.patternMatrix` 已补 sourceRuleId/appliesWhen/breaksWhen/riskBoundary；相关 regression 38 passed。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.01 | No | Done | 2026-06-16：specialPatternCandidates 输出 maturity.basis=condition_chain；candidate/guarded/not_supported 由条件计数和 score 决定；38 passed。 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02 | No | Done | 2026-06-16：rule_depth_cases.json 锁定 specialPatternStatuses 和 specialPatternRiskBoundary；聚合覆盖 从格/化气/专旺/假从/从杀/从财；38 passed, 1 skipped。 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：TP-04.01/TP-04.02/TP-04.03 均完成；合化 contract、evaluator state 和四类 state golden 已验收。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.relation.combine_transform_guard.transformStateMatrix` 已补 evidenceFields/appliesWhen/counterConditions/riskBoundary；相关 regression 38 passed。 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.01 | No | Done | 2026-06-16：combineTransformMatrix 输出 stateCatalog 和 candidate.state；API contract 回归 54 passed。 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02 | No | Done | 2026-06-16：rule_depth_cases.json 新增 combineTransform evaluatorStateCases，覆盖 structural_relation/transform_candidate/transform_success/transform_broken 且逐条有 failureExplanation。 | 无 | 无 |
| TP-05 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：TP-05.01/TP-05.02/TP-05.03 均完成；用神策略矩阵、evaluator 和 golden 策略顺序已验收。 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.yongshen.strategy_matrix.strategyScoringMatrix` 已补 appliesWhen/doesNotApplyWhen/scoreBasis/conflictPolicy；相关 regression 38 passed。 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.01 | No | Done | 2026-06-16：yongShenDecision.scoredStrategies 保留 4 种策略，逐项输出 appliesWhen/doesNotApplyWhen/conflictPolicy；38 passed。 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02 | No | Done | 2026-06-16：rule_depth_cases.json 锁定 yongShenStrategyOrder 和 yongShenRiskBoundary；29 passed。 | 无 | 无 |
| TP-06 | ROOT | 1 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | No | Done | 2026-06-16：TP-06.01/TP-06.02/TP-06.03 均完成；岁运触发、专题 profile、报告/API/Web 边界已通过回归。 | 无 | 无 |
| TP-06.01 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | No | Done | 2026-06-16：`bazi.depth.fortune.trigger_chain.triggerMatrix` 覆盖大运、流年、流月、伏吟、反吟、岁运并临、天克地冲；fortuneTriggers 输出 triggerTypes、reasons、riskBoundary；相关 rg 检索通过，regression 32 passed。 | 无 | 无 |
| TP-06.02 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01 | No | Done | 2026-06-16：topicProfiles 覆盖事业、财运、婚姻、健康、学业、迁移、家庭；每项有 score、basis、scoreBasis、evidenceFields、riskBoundary、lifecycle=beta；指定 regression 32 passed，ruff check/format PASS。 | 无 | 无 |
| TP-06.03 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.02 | No | Done | 2026-06-16：Web 工作台新增专题 profile/风险边界折叠块；Markdown API 不输出 topicProfiles 或高风险禁词；指定 regression 52 passed，ruff check/format PASS。 | 无 | 无 |
| TP-07 | ROOT | 1 | TP-06.01, TP-06.02, TP-06.03 | No | Done | 2026-06-16：TP-07.01/TP-07.02/TP-07.03 均完成；MingLi full baseline、失败归因和 benchmark gate policy 已落地。 | 无 | 无 |
| TP-07.01 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03 | No | Done | 2026-06-16：全量 MingLi predictions 160/160；answered 160、correct 45、accuracy 28.12%；report 含 byCategory/results；predictions 无 expected/answer/correct 泄漏字段；证据写入 MINGLI_FULL_EVALUATION.md。 | 无 | 无 |
| TP-07.02 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01 | No | Done | 2026-06-16：新增 MINGLI_FAILURE_TAXONOMY.md；115 个失败样本按分类、owner 能力面、缺规则/缺时间触发/缺格局/缺用神归因；明确禁止答案硬编码。 | 无 | 无 |
| TP-07.03 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.02 | No | Done | 2026-06-16：新增 BENCHMARK_GATE_POLICY.md；明确 28.12% 当前 baseline、next gate、回退条件、不达标处理和禁止刷分规则。 | 无 | 无 |
| TP-08 | ROOT | 1 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | No | Done | 2026-06-16：TP-08.01/TP-08.02 均完成；报告字段契约、风险话术和免责声明回归已落地。 | 无 | 无 |
| TP-08.01 | TP-08 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | No | Done | 2026-06-16：新增 REPORT_FIELD_CONTRACT.md；API 测试锁高级格局、合化、用神、岁运、专题 profile 和 ruleDepth 字段；Web/Markdown 合同回归 40 passed。 | 无 | 无 |
| TP-08.02 | TP-08 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01 | No | Done | 2026-06-16：classics/rule-depth 风险话术统一为边界语言；新增 policy test 防止医疗/金融/法律/心理替代建议和保证类词回潮；指定 regression 45 passed。 | 无 | 无 |
| TP-09 | ROOT | 1 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | No | Done | 2026-06-16：TP-09.01 CORE_FILE_BURNDOWN.md 与 TP-09.02 EVALUATOR_BOUNDARIES.md 完成；registry/evaluator/golden/report 分层边界已记录。 | 无 | 无 |
| TP-09.01 | TP-09 | 2 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | No | Done | 2026-06-16：新增 CORE_FILE_BURNDOWN.md；核心文件关键名检索通过。 | 无 | 无 |
| TP-09.02 | TP-09 | 2 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02, TP-03.01, TP-04.01, TP-05.01, TP-06.01 | No | Done | 2026-06-16：新增 EVALUATOR_BOUNDARIES.md；明确 evaluation 不进生产 kernel、oracle 不进主链、delivery 不承载领域算法，并定义 pattern/hehua/yongshen/fortune/topic 边界。 | 无 | 无 |
| TP-10 | ROOT | 1 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | No | Not Started | 依赖已满足，下一步执行最终六维审查。 | 无 | 无 |
| TP-10.01 | TP-10 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | Yes | Not Started | 依赖已满足，下一步执行 local-ci quick 和六维审查。 | 无 | 无 |
| TP-10.02 | TP-10 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02, TP-10.01 | No | Not Started | 待回填 | 无 | 无 |

# Blockers
- 无当前硬阻塞；真实专家命例和人工标注属于后续 HITL 增强，不阻塞本地任务树设计。

# Runtime State
- Active workflow state: 以任务包 JSON 和 Recent Evidence 为准
- Approval state: 未记录即未授权
