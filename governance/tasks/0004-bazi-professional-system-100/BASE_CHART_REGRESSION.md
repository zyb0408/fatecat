# Base Chart Regression

任务节点：`TP-02.03`

## 结论

基础排盘回归门禁通过。当前四柱、基础字段、golden coverage matrix 和 API contract 在本轮任务证据下保持稳定。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py -q
```

Result:

```text
40 passed, 1 skipped in 33.65s
```

## Gate 判定

- `基础字段 schema diff 为零或有迁移说明`：`PASS`
- `coverage matrix 可运行`：`PASS`
- `API contract 未被基础排盘证据破坏`：`PASS`

## 后续边界

基础排盘维度可以进入 100% gate，但前提是后续高级格局、合化、用神、岁运任务不能直接改动 CalendarProvider 或基础四柱输出；如需改动，必须回到 `TP-02` 重新跑 calendar/oracle/base-chart gate。
