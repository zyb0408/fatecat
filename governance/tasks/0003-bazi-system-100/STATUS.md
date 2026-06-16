# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-03.03 | Wave 11 | Depends On: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02 | Gate: 每类高级格局至少有可回归样本；无样本能力只能保持 beta/evidence_seed
- TP-04.03 | Wave 11 | Depends On: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02 | Gate: 每类合化状态至少有一组回归样本和 failureExplanation
- TP-05.03 | Wave 11 | Depends On: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02 | Gate: 每类用神冲突有 expected strategy order 和 riskBoundary

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
| TP-03 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | In Progress | 2026-06-16：TP-03.01/TP-03.02 完成；高级格局矩阵和候选成熟度输出已接通。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.pattern.regular_vs_special.patternMatrix` 已补 sourceRuleId/appliesWhen/breaksWhen/riskBoundary；相关 regression 38 passed。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.01 | No | Done | 2026-06-16：specialPatternCandidates 输出 maturity.basis=condition_chain；candidate/guarded/not_supported 由条件计数和 score 决定；38 passed。 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | In Progress | 2026-06-16：TP-04.01/TP-04.02 完成；合化条件链和 evaluator state 输出已接通。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.relation.combine_transform_guard.transformStateMatrix` 已补 evidenceFields/appliesWhen/counterConditions/riskBoundary；相关 regression 38 passed。 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.01 | No | Done | 2026-06-16：combineTransformMatrix 输出 stateCatalog 和 candidate.state；API contract 回归 54 passed。 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-05 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | In Progress | 2026-06-16：TP-05.01/TP-05.02 完成；用神并列策略、评分依据和冲突政策已进入 evaluator 输出。 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Done | 2026-06-16：`bazi.depth.yongshen.strategy_matrix.strategyScoringMatrix` 已补 appliesWhen/doesNotApplyWhen/scoreBasis/conflictPolicy；相关 regression 38 passed。 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.01 | No | Done | 2026-06-16：yongShenDecision.scoredStrategies 保留 4 种策略，逐项输出 appliesWhen/doesNotApplyWhen/conflictPolicy；38 passed。 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-06 | ROOT | 1 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-06.01 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-06.02 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-06.03 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-07 | ROOT | 1 | TP-06.01, TP-06.02, TP-06.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-07.01 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-07.02 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-07.03 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-08 | ROOT | 1 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-08.01 | TP-08 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-08.02 | TP-08 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-09 | ROOT | 1 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | No | In Progress | 2026-06-16：TP-09.01 CORE_FILE_BURNDOWN.md 完成；核心大文件拆分候选、行为保持测试与回滚路径已记录。 | 无 | 无 |
| TP-09.01 | TP-09 | 2 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02 | No | Done | 2026-06-16：新增 CORE_FILE_BURNDOWN.md；核心文件关键名检索通过。 | 无 | 无 |
| TP-09.02 | TP-09 | 2 | TP-00.01, TP-00.02, TP-00.03, TP-01.01, TP-01.02, TP-03.01, TP-04.01, TP-05.01, TP-06.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-10 | ROOT | 1 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-10.01 | TP-10 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-10.02 | TP-10 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-05.03, TP-06.01, TP-06.02, TP-06.03, TP-07.01, TP-07.02, TP-07.03, TP-08.01, TP-08.02, TP-09.01, TP-09.02, TP-10.01 | No | Not Started | 待回填 | 无 | 无 |

# Blockers
- 无当前硬阻塞；真实专家命例和人工标注属于后续 HITL 增强，不阻塞本地任务树设计。

# Runtime State
- Active workflow state: 以任务包 JSON 和 Recent Evidence 为准
- Approval state: 未记录即未授权
