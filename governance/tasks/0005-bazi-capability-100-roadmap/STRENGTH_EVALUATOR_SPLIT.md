# TP-04.01 Strength Evaluator Split

## Status

- Result: `PASS`
- Scope: strength evaluator 物理拆分。
- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`

## Evidence

- Command result after formatting: `62 passed in 65.80s`.
- Format gate: `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/strength.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/ten_god.py tests/regression/test_bazi_ziwei_rule_depth.py`
  - Result: `4 files already formatted`
- New evaluator: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/strength.py`
- Orchestrator change: `calculate_pure_analysis.py` now imports `build_strength_score` from `fate_core.usecases.evaluators`.
- Regression guard: `tests/regression/test_bazi_ziwei_rule_depth.py::test_bazi_strength_and_ten_god_evaluators_are_physically_split`

## Gate Decision

- schema unchanged: `PASS`
- delivery did not gain domain algorithm: `PASS`
- `strengthScore` still has `score`、`basis`、`sourceRuleId`、`conflicts`、`evidenceFields`、`riskBoundary`: `PASS`
- old `_build_strength_score` no longer lives in `calculate_pure_analysis.py`: `PASS`
