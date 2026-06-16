# TP-02.01 CalendarProvider Gate

## Status

- Result: `PASS`
- Scope: CalendarProvider 升级合同与 provider/oracle 边界复核。
- Verify: `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q`

## Evidence

- Command result: `10 passed in 138.17s`.
- `tests/regression/test_calendar_oracle_contract.py` 继续约束 production provider 与 oracle/reference 资源边界。
- `tests/regression/test_solar_terms_golden.py` 继续执行节气 golden 与八字历法边界 regression。
- `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json` 现在显式区分：
  - `runtime_full`: 9 个真实排盘回归样本。
  - `schema_catalog`: 42 个边界目录样本。

## Gate Decision

- production provider 边界：`PASS`
- oracle-only/reference-only 边界：`PASS`
- solar terms golden regression：`PASS`
- runtime_full calendar golden regression：`PASS`

## Remaining Boundary

- `schema_catalog` 不是完整 provider oracle，只锁定边界输入语义。
- `TP-02.03` 必须补 oracle mismatch report；不可解释 provider/oracle 差异不得标绿。
