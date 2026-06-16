# TP-02.03 Calendar Oracle Mismatch Report

## Status

- Result: `PASS`
- Scope: oracle mismatch report。
- Verify: `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q`

## Evidence

- Command result: `11 passed in 146.80s`.
- Machine-readable report: `domains/fate-analysis/data-products/bazi/golden/calendar_oracle_mismatch_report.json`
- Report summary:
  - `runtimeFullCaseCount`: 9
  - `schemaCatalogExcludedCount`: 42
  - `acceptedRegressionCount`: 9
  - `explainedMismatchCount`: 0
  - `unexplainedMismatchCount`: 0
- Regression hook: `tests/regression/test_calendar_oracle_contract.py::test_calendar_oracle_mismatch_report_covers_runtime_full_boundary_cases`

## Gate Decision

- report covers all `runtime_full` boundary cases: `PASS`
- `schema_catalog` cases are excluded from exact oracle claims: `PASS`
- unexplained mismatch count is zero: `PASS`
- provider/oracle/input/expected/actual/decision/failureExplanation fields are present: `PASS`

## Remaining Boundary

- This closes the current TP-02 gate for the 9 full runtime samples.
- The 42 catalog-only samples are a backlog for future runtime promotion, not a production accuracy claim.
