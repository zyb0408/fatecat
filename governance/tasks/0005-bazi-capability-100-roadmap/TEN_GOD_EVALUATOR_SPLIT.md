# TP-04.02 Ten-God Evaluator Split

## Status

- Result: `PASS`
- Scope: ten-god evaluator 物理拆分。
- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`

## Evidence

- Command result after formatting: `62 passed in 65.80s`.
- Format gate: `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/strength.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/ten_god.py tests/regression/test_bazi_ziwei_rule_depth.py`
  - Result: `4 files already formatted`
- New evaluator: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/ten_god.py`
- Orchestrator change: `calculate_pure_analysis.py` now imports `build_ten_god_structure`、`ten_god_values`、`ten_god_families` from `fate_core.usecases.evaluators`.
- Regression guard: `tests/regression/test_bazi_ziwei_rule_depth.py::test_bazi_strength_and_ten_god_evaluators_are_physically_split`

## Gate Decision

- schema unchanged: `PASS`
- ten-god output references pillar/stem/hidden-stem evidence through `basisEvidence`: `PASS`
- `tenGodStructure` still has `counts`、`basisEvidence`、`dominant`、`families`、`sourceRuleId`、`evidenceFields`、`riskBoundary`: `PASS`
- old `_ten_god_position_evidence` and `_ten_god_values` no longer live in `calculate_pure_analysis.py`: `PASS`
