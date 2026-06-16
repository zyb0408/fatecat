# Task Status

- Overall Status: `Blocked`

# Next Executable Leaves

- None. `TP-09.01` remains blocked by corpus volume, so `TP-09.02`/`TP-09.03` and `TP-11.*` are not executable.

# Task Package Status Table

| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | `BASELINE_RECHECK.md`、`RESOURCE_ADMISSION_RECHECK.md`、`TEN_DIMENSION_100_GATE_CONTRACT.md` 已新增；100% 口径与资源准入闭合。 | 无 | 无 |
| TP-01.01 | TP-01 | 2 | - | No | Done | `BASELINE_RECHECK.md` 已新增；rg gate PASS，确认十维基线、Active BLOCK=0 和禁止口径一致。 | 无 | 无 |
| TP-01.02 | TP-01 | 2 | - | No | Done | `RESOURCE_ADMISSION_RECHECK.md` 已新增；rg gate PASS，确认资源角色和 productionUseAllowed 边界。 | 无 | 无 |
| TP-01.03 | TP-01 | 2 | TP-01.01, TP-01.02 | No | Done | `TEN_DIMENSION_100_GATE_CONTRACT.md` 已新增；rg gate PASS，确认 100% 不等于预测准确率。 | 无 | 无 |
| TP-02 | ROOT | 1 | - | No | Done | `CALENDAR_PROVIDER_GATE.md`、`CALENDAR_BOUNDARY_CORPUS_50.md`、`CALENDAR_ORACLE_MISMATCH_REPORT.md` 已新增；历法 provider/corpus/mismatch gate 本地通过。 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-01.03 | No | Done | `CALENDAR_PROVIDER_GATE.md` 已新增；`tests/regression/test_calendar_oracle_contract.py` + `tests/regression/test_solar_terms_golden.py` 为 `10 passed in 138.17s`。 | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-01.03 | No | Done | `CALENDAR_BOUNDARY_CORPUS_50.md` 已新增；calendar corpus 51 cases，coverage matrix 为 `12 passed, 1 skipped in 29.61s`。 | 无 | 无 |
| TP-02.03 | TP-02 | 2 | TP-02.01, TP-02.02 | No | Done | `CALENDAR_ORACLE_MISMATCH_REPORT.md` 已新增；machine-readable mismatch report 受 pytest 约束，`11 passed in 146.80s`。 | 无 | 无 |
| TP-03 | ROOT | 1 | - | No | Done | `RULE_ID_COVERAGE_FORCE_GATE.md`、`EVIDENCE_COUNTEREVIDENCE_SCHEMA_GATE.md`、`HIGH_RISK_POLICY_GATE.md` 已新增；证据化和高风险 policy gate 本地通过。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-01.03 | No | Done | `RULE_ID_COVERAGE_FORCE_GATE.md` 已新增；combined TP-03 regression 为 `85 passed in 71.22s`。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-01.03 | No | Done | `EVIDENCE_COUNTEREVIDENCE_SCHEMA_GATE.md` 已新增；API/capability evidence envelope gate 通过。 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-03.01, TP-03.02 | No | Done | `HIGH_RISK_POLICY_GATE.md` 已新增；policy/statement golden 为 `19 passed in 55.56s`。 | 无 | 无 |
| TP-04 | ROOT | 1 | - | No | Done | `STRENGTH_EVALUATOR_SPLIT.md`、`TEN_GOD_EVALUATOR_SPLIT.md`、`REGULAR_PATTERN_RELATION_EVALUATOR_SPLIT.md` 已新增；常规分析 evaluator 拆分与 API/statement/rule-depth 回归通过。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-02.03, TP-03.03 | No | Done | `STRENGTH_EVALUATOR_SPLIT.md` 已新增；TP-04 regression 为 `62 passed in 65.80s`，format check 通过。 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-02.03, TP-03.03 | No | Done | `TEN_GOD_EVALUATOR_SPLIT.md` 已新增；tenGodStructure schema 与 basisEvidence regression 通过。 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-04.01, TP-04.02 | No | Done | `REGULAR_PATTERN_RELATION_EVALUATOR_SPLIT.md` 已新增；statement/rule-depth 为 `36 passed in 132.06s`，API contract 为 `31 passed in 6.89s`。 | 无 | 无 |
| TP-05 | ROOT | 1 | - | No | Done | `ADVANCED_PATTERN_TAXONOMY_LIFECYCLE.md`、`ADVANCED_PATTERN_GOLDEN_BOUNDARIES.md`、`GUARDED_ADVANCED_PATTERN_EVALUATOR.md` 已新增；高级格局合同、正反边界和 guarded evaluator 通过。 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-04.03 | No | Done | `ADVANCED_PATTERN_TAXONOMY_LIFECYCLE.md` 已新增；rg gate PASS，`test_bazi_ziwei_rule_depth.py` 为 `31 passed in 61.78s`。 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | `ADVANCED_PATTERN_GOLDEN_BOUNDARIES.md` 已新增；combined regression 为 `48 passed, 1 skipped in 173.82s`。 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-05.02 | No | Done | `GUARDED_ADVANCED_PATTERN_EVALUATOR.md` 已新增；rule-depth + API 为 `66 passed in 65.35s`，format gate 为 `12 files already formatted`。 | 无 | 无 |
| TP-06 | ROOT | 1 | - | No | Done | `HEHUA_CONDITION_CHAIN_CONTRACT.md`、`HEHUA_COUNTEREXAMPLE_MATRIX.md`、`TRANSFORM_EVALUATOR_SPLIT.md` 已新增；合化合同、反例矩阵和 evaluator 通过。 | 无 | 无 |
| TP-06.01 | TP-06 | 2 | TP-04.03 | No | Done | `HEHUA_CONDITION_CHAIN_CONTRACT.md` 已新增；rg gate PASS，`test_bazi_ziwei_rule_depth.py` 为 `31 passed in 61.78s`。 | 无 | 无 |
| TP-06.03 | TP-06 | 2 | TP-06.01 | No | Done | `HEHUA_COUNTEREXAMPLE_MATRIX.md` 已新增；破化/争合/阻隔/冲破矩阵受 regression 检查。 | 无 | 无 |
| TP-06.02 | TP-06 | 2 | TP-06.01, TP-06.03 | No | Done | `TRANSFORM_EVALUATOR_SPLIT.md` 已新增；争合 runtime fixture 已纳入 rule-depth regression。 | 无 | 无 |
| TP-07 | ROOT | 1 | - | No | Done | `YONGSHEN_STRATEGY_CONTRACT.md`、`YONGSHEN_REPORT_BOUNDARY_GOLDEN.md`、`YONGSHEN_CONFLICT_RANKING_EVALUATOR.md` 已新增；用神合同、反例、报告边界和排序 evaluator 通过。 | 无 | 无 |
| TP-07.01 | TP-07 | 2 | TP-04.03 | No | Done | `YONGSHEN_STRATEGY_CONTRACT.md` 已新增；rg gate PASS，`test_bazi_ziwei_rule_depth.py` 为 `31 passed in 61.78s`。 | 无 | 无 |
| TP-07.03 | TP-07 | 2 | TP-07.01 | No | Done | `YONGSHEN_REPORT_BOUNDARY_GOLDEN.md` 已新增；statement/report boundary 组合回归通过。 | 无 | 无 |
| TP-07.02 | TP-07 | 2 | TP-07.01, TP-07.03 | No | Done | `YONGSHEN_CONFLICT_RANKING_EVALUATOR.md` 已新增；ranking/conflicts/noAbsoluteConclusion regression 通过。 | 无 | 无 |
| TP-08 | ROOT | 1 | - | No | Done | `FORTUNE_TRIGGER_MATRIX_EVIDENCE.md`、`TOPIC_PROFILE_EVALUATOR.md`、`TOPIC_POLICY_REGRESSION.md` 已新增；岁运专题阶段通过。 | 无 | 无 |
| TP-08.01 | TP-08 | 2 | TP-05.03, TP-06.02, TP-07.02 | No | Done | `FORTUNE_TRIGGER_MATRIX_EVIDENCE.md` 已新增；动态触发矩阵受 rule-depth regression 覆盖。 | 无 | 无 |
| TP-08.02 | TP-08 | 2 | TP-08.01 | No | Done | `TOPIC_PROFILE_EVALUATOR.md` 已新增；API/rule-depth/statement 为 `71 passed in 121.75s`。 | 无 | 无 |
| TP-08.03 | TP-08 | 2 | TP-08.02 | No | Done | `TOPIC_POLICY_REGRESSION.md` 已新增；policy + statement 为 `19 passed in 55.51s`。 | 无 | 无 |
| TP-09 | ROOT | 1 | - | No | Blocked | `GOLDEN_CORPUS_TARGET_GAP.md` 已新增；calendar 达标，但 rule-depth/statement/topic corpus 数量未达 gate。 | corpus 数量不足 | 扩展 rule-depth>=120、statement>=80、P0 topic 每类>=20 |
| TP-09.01 | TP-09 | 2 | TP-08.03 | No | Blocked | `GOLDEN_CORPUS_TARGET_GAP.md` 已新增；真实统计为 calendar=51、rule-depth=8、statement=5、topic=0。 | corpus 数量不足 | 生成或准入足量可追溯 golden |
| TP-09.02 | TP-09 | 2 | TP-09.01 | No | Not Started | shard release gate。 | 无 | 无 |
| TP-09.03 | TP-09 | 2 | TP-09.02 | No | Not Started | mutation/schema regression。 | 无 | 无 |
| TP-10 | ROOT | 1 | - | No | Done | `MINGLI_FULL_NO_LEAK_GATE.md`、`MINGLI_FAILURE_TAXONOMY.md`、`BAZIQA_ADMISSION_GATE.md` 已新增；benchmark no-leak、failure backlog、BaziQA admission 均完成。 | 无 | 无 |
| TP-10.01 | TP-10 | 2 | TP-08.03 | No | Done | `MINGLI_FULL_NO_LEAK_GATE.md` 已新增；answered=160/160，accuracy=27.50%，leakCount=0。 | 无 | 无 |
| TP-10.02 | TP-10 | 2 | TP-10.01 | No | Done | `MINGLI_FAILURE_TAXONOMY.md` 已新增；每类 failure 有 owner、缺口、回炉方向、禁止路径。 | 无 | 无 |
| TP-10.03 | TP-10 | 2 | TP-10.01 | No | Done | `BAZIQA_ADMISSION_GATE.md` 已新增；BaziQA 保持 `future_candidate/evaluation_only`，未接入 runtime。 | 无 | 无 |
| TP-11 | ROOT | 1 | - | No | Not Started | 维护边界与交付 100% 阶段已规划。 | 无 | 无 |
| TP-11.01 | TP-11 | 2 | TP-09.03, TP-10.02, TP-10.03 | No | Not Started | evaluator 物理拆分收口。 | 无 | 无 |
| TP-11.02 | TP-11 | 2 | TP-11.01 | No | Not Started | Web/API/Markdown 消费边界。 | 无 | 无 |
| TP-11.03 | TP-11 | 2 | TP-11.02 | No | Not Started | final local release gate。 | 无 | 无 |

# Blockers

- TP-09.01 corpus 数量不足：rule-depth=8/120、statement=5/80、topic=0/20 each。
- BaziQA 已完成准入审查，结论为 PASS with WARN：保持 `future_candidate/evaluation_only`，不得进入 runtime、production rule source 或正式 release gate。
- 专家命例授权未知；缺授权时高级格局和专题规则只能保持 beta/HITL。
- MingLi benchmark 不能作为生产规则来源，只能驱动 failure backlog。

# Runtime State

- Active workflow state: no ready executable leaf; `TP-09.01` is blocked by corpus volume.
- Remote push: not allowed in this task.
- GitHub Acceptance: not allowed in this task.
- Stop condition: 发现计划要求答案泄漏、评测数据 runtime 接入、无来源强断或高风险现实处方时，必须停止并改写任务。
