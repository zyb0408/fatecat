# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-02.02 | Wave 7 | Depends On: TP-01.01, TP-01.02, TP-02.01 | Gate: 新增边界样本均有 source、expected、failureExplanation 和 privacy/license 说明

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
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02 | No | In Progress | 2026-06-16：TP-02.01 CALENDAR_ORACLE_AUDIT.md 完成；oracle 隔离 PASS，现有 boundary fixture 字段缺口转交 TP-02.02。 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-01.01, TP-01.02 | No | Done | 2026-06-16：新增 CALENDAR_ORACLE_AUDIT.md；Verify `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q` 通过，10 passed in 71.82s。 | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-01.01, TP-01.02, TP-02.01 | Yes | Not Started | 下一步补齐 boundary case 逐条 source/failureExplanation/privacy/license，并扩展时间边界 golden。 | 无 | 无 |
| TP-02.03 | TP-02 | 2 | TP-01.01, TP-01.02, TP-02.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-03 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-03.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-04.02 | No | Not Started | 待回填 | 无 | 无 |
| TP-05 | ROOT | 1 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-02.03, TP-05.02 | No | Not Started | 待回填 | 无 | 无 |
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
