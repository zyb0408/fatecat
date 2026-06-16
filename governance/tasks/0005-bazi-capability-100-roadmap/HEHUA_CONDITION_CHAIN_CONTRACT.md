# TP-06.01 Hehua Condition Chain Contract Evidence

## Result

PASS.

合化条件链状态模型已进入 `contracts/fate/rule_depth_registry.json` 的 `bazi.depth.relation.combine_transform_guard.transformStateMatrix`。

## Verified Scope

状态模型覆盖：

- `structural_relation`：合象登记
- `transform_candidate`：成化候选
- `transform_success`：成化成立
- `transform_broken`：破化/阻隔
- `contested_transform`：争合

每个状态具备：

- `appliesWhen`
- `doesNotApplyWhen`
- `requiredEvidenceFields`
- `conditionChainFields`
- `riskBoundary`

统一条件链字段：

- `month_command`
- `transparent_stems`
- `rooted_branches`
- `blockers`
- `counter_conditions`

## Evidence

- `contracts/fate/rule_depth_registry.json`
- `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`

## Commands

```bash
rg '合象|合而不化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `31 passed in 61.78s`

## Gate

PASS: 月令、透干、通根、阻隔、反证条件已可序列化并被 rule-depth regression 检查。

## Remaining Work

- `TP-06.03` 补破化、争合、阻隔、冲破反例矩阵。
- `TP-06.02` 再迁出/实现 transform evaluator，输出状态、证据和反证。

## Guardrail

当前只是状态合同完成。报告和 API 不得把“合象登记”直接写成“已经成化”。
