# TP-06.02 Transform Evaluator Evidence

## Result

PASS.

合化条件链 evaluator 已从 `calculate_pure_analysis.py` 迁入 `fate_core.usecases.evaluators.combine_transform`。

## Implementation

- 新增 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/combine_transform.py`
- 新增 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/constants.py`
- 更新 `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- 更新 `tests/regression/test_bazi_ziwei_rule_depth.py`

## Verified Scope

- 输出状态覆盖：
  - `structural_relation`
  - `transform_candidate`
  - `transform_success`
  - `transform_broken`
  - `contested_transform`
- 新增争合 runtime fixture：`combine_contested_transform_contract`。
- `combineTransformCounterexampleMatrix` 的争合项已从 contract-only 升级为 evaluator fixture。

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- rule-depth + API: `66 passed in 65.35s`
- format gate: `12 files already formatted`

## Gate

PASS: 输出状态、证据和反证，不只输出“合化”；争合降低成化置信度，不自动改写格局。

## Guardrail

合化 evaluator 仍只登记传统结构证据，不输出确定现实事件。
