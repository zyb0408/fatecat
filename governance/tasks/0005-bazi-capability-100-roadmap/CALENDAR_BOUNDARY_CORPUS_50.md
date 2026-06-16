# TP-02.02 Calendar Boundary Corpus 50+

## Status

- Result: `PASS`
- Scope: 扩展 calendar boundary corpus 到 `>=50` 并让测试强制检查 schema。
- Verify: `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_bazi_golden_coverage_matrix.py -q`

## Evidence

- Command result: `12 passed, 1 skipped in 29.61s`.
- Corpus file: `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json`
- Current counts:
  - declared `caseCount`: 51
  - actual cases: 51
  - `runtime_full`: 9
  - `schema_catalog`: 42
- `coverageRequirements.minCaseCount`: 50
- `coverageRequirements.minRuntimeFullCaseCount`: 9

## Required Coverage Tags

- `dst_boundary`
- `early_zi`
- `fortune_start`
- `future_boundary`
- `gender_female`
- `historical_year`
- `late_zi`
- `lichun_boundary`
- `non_east_8`
- `non_whole_hour_timezone`
- `second_level_boundary`
- `southern_hemisphere`
- `timezone_normalization`
- `true_solar_time`
- `utc_input`
- `western_longitude`

## Gate Decision

- corpus count `>=50`: `PASS`
- each case has `source`: `PASS`
- each case has `expected`: `PASS`
- each case has `expected.tolerance`: `PASS`
- each case has `failureExplanation`: `PASS`
- runtime_full minimum remains enforced: `PASS`

## Remaining Boundary

- 42 个 `schema_catalog` 样本还不是完整 provider 输出 oracle。
- 后续提升到 100% 时，必须逐步把高价值 schema catalog 样本晋升为 `runtime_full`，并记录 mismatch decision。
