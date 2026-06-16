# TP-05.02 Advanced Pattern Golden Boundary Evidence

## Result

PASS.

高级格局正反边界矩阵已写入 `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` 的 `advancedPatternGoldenMatrix`。

## Verified Scope

覆盖类目：

- 正格
- 变格
- 从格
- 假从
- 专旺
- 化气

边界类型：

- `positive`
- `negative`
- `boundary`

## Evidence

- `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_bazi_golden_coverage_matrix.py`

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `34 passed in 77.85s`
- combined golden/rule-depth/statement regression: `48 passed, 1 skipped in 173.82s`

## Gate

PASS: 每类高级格局都有正例、反例、边界例记录，或显式 `promotionBlocked` 并保持 beta/HITL。

## Remaining Work

- `TP-05.03` 继续实现 guarded advanced-pattern evaluator。
- 变格、假从边界和化气反例仍需真实授权命例或更完整 synthetic oracle，当前不得 promotion。

## Guardrail

这些 fixture 是 `synthetic_anonymous_fixture`，只用于测试和回归，不是专业命例真值库，不得进入 runtime。
