# 用神冲突正反例 Golden

## Scope

- Task: `TP-07.03`
- Objective: 补寒暖燥湿、身强身弱、格局优先、通关病药冲突场景的 golden。
- Fixture: `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- Test: `tests/regression/test_bazi_ziwei_rule_depth.py`

## Golden Additions

`rule_depth_cases.json` 已把用神冲突裁决从单一 strategy order 扩展为以下字段：

- `yongShenRanking`: 锁定每个样本的 strategy + score。
- `yongShenSelectedCandidates`: 锁定 primary 和 parallel review 候选。
- `yongShenConflictMatrix`: 锁定冲突类型、severity、delta 和涉及策略。
- `yongShenDecisionTraceSteps`: 锁定评分、排序、候选选择和冲突附加步骤。
- `yongShenNoAbsoluteConclusion`: 锁定不输出唯一绝对结论。

## Covered Conflict Types

| Conflict Type | Meaning |
| --- | --- |
| `strategy_ranking_delta` | 最高分与次高分之间的证据差距，需要解释 ranking 变化。 |
| `climate_vs_strength` | 调候和扶抑分别解释气候与日主强弱，冲突时只排序不覆盖。 |
| `relationship_or_imbalance_overlay` | 通关和病药只作冲突缓冲与偏枯修正，不替代主策略。 |

## Verification

| Check | Result |
| --- | --- |
| `.venv/bin/python -m ruff format --check tests/regression/test_bazi_ziwei_rule_depth.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_api_contracts.py` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | `39 passed, 1 skipped in 90.40s` |

## Gate

- PASS: 冲突 golden 可以解释 ranking 变化。
- PASS: 每个 rule-depth golden case 都锁定 ranking 分数、候选策略和冲突矩阵。
- PASS: `noAbsoluteConclusion` 被 golden 锁定为 `true`。
- PASS: JSON fixture 已重新校验为合法 JSON；不再使用 ruff 格式化 JSON 数据文件。
