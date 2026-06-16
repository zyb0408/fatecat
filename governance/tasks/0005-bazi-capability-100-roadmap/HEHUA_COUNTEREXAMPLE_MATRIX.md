# TP-06.03 Hehua Counterexample Matrix Evidence

## Result

PASS.

破化、争合、阻隔、冲破反例矩阵已写入 `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` 的 `combineTransformCounterexampleMatrix`。

## Verified Scope

覆盖场景：

- 破化
- 阻隔
- 冲破
- 争合

每个场景具备：

- `state`
- `conditionChainField`
- `failedCondition`
- `failureExplanation`

## Evidence

- `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- `contracts/fate/rule_depth_registry.json`
- `tests/regression/test_bazi_ziwei_rule_depth.py`

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `34 passed in 77.85s`
- combined golden/rule-depth/statement regression: `48 passed, 1 skipped in 173.82s`

## Gate

PASS: 失败能定位到具体 condition field；争合当前标记为 contract-only + promotionBlocked，等待 `TP-06.02` evaluator。

## Remaining Work

- `TP-06.02` 继续实现 transform evaluator，把争合从 contract-only 变成 runtime 可检测状态。

## Guardrail

合化输出不得从关系名称直接跳到成化结论。缺证据时只保留合象、候选或破化/争合边界。
