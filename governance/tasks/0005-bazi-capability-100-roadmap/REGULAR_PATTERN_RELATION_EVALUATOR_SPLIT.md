# TP-04.03 Regular Pattern / Relation Evaluator Split

## Status

- Result: `PASS`
- Scope: regular-pattern/relation evaluator 拆分。
- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py -q`

## Evidence

- Command result: `36 passed in 132.06s`.
- API schema cross-check: `.venv/bin/python -m pytest tests/regression/test_api_contracts.py -q`
  - Result: `31 passed in 6.89s`.
- Format gate: `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/relation.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/regular_pattern.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/__init__.py tests/regression/test_bazi_ziwei_rule_depth.py`
  - Result: `5 files already formatted`
- New evaluators:
  - `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/relation.py`
  - `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/regular_pattern.py`
- Regression guard: `tests/regression/test_bazi_ziwei_rule_depth.py::test_bazi_strength_and_ten_god_evaluators_are_physically_split`

## Gate Decision

- relation order evaluator moved out of large usecase: `PASS`
- regular pattern candidate evaluator moved out of large usecase: `PASS`
- unstable regular pattern keeps `uncertainty` / `breaksWhen` / `riskBoundary`: `PASS`
- statement golden unchanged: `PASS`
- API schema unchanged: `PASS`

## Remaining Boundary

- TP-04 closes the current regular-analysis split.
- Advanced special patterns, hehua state machine and yongshen conflict ranking remain separate TP-05/TP-06/TP-07 work, not hidden inside TP-04.
