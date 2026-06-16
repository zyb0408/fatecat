# Wave 3 Execution Evidence

日期：2026-06-16

## Scope

Wave 3 覆盖：

- `TP-10.03` Markdown/Web/Bot 输出可追溯性
- `TP-11.01` 300+ golden release gate
- `TP-13.01` 时间/时区/节气/早晚子时边界矩阵
- `TP-13.02` 计算背压与 timeout ceiling 验证

## Command Evidence

| Node | Command | Result |
| --- | --- | --- |
| TP-10.03 | `.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_branding_support.py tests/regression/test_api_contracts.py -q` | PASS：`47 passed in 7.38s`。 |
| TP-13.01 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py -q` | PASS：`18 passed, 1 skipped in 97.87s`。 |
| TP-13.02 | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py -q` | PASS：`30 passed in 3.89s`。 |
| TP-11.01 | `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q` | PASS：`9 passed in 2211.71s (0:36:51)`。 |

## Findings

### PASS: 输出链路可追溯

Web HTML、TradeCat Labs branding、API contract 回归通过。当前 `/web` 和 API 输出链路没有在本轮暴露协议失败或页面契约失败。

### PASS: 时间边界矩阵

calendar oracle、solar terms golden、bazi golden representative gate 通过。默认门禁覆盖 requiredTags 代表集，全量矩阵独立作为 release/deep gate。

### PASS: Timeout / Rate / Operability

API contract 和 operability docs 回归通过，覆盖 4xx/5xx/503/429、metrics、runbook 等运行语义。

### WARN: 300+ Golden Gate 成本过高

全量 300+ golden gate 通过，但耗时 `36m51s`。这证明矩阵真实执行，不是文档摆设；同时也证明它不能进入 quick profile。

后续最小治理：

- 保持 representative golden 在默认 regression/quick gate。
- 将 `FATECAT_RUN_FULL_GOLDEN_MATRIX=1` 固定为 release/deep gate。
- 增加 `FATECAT_GOLDEN_SHARD_TOTAL` / `FATECAT_GOLDEN_SHARD_INDEX` 分片选择器；分片覆盖测试 `test_bazi_golden_coverage_matrix_shards_cover_all_cases_without_overlap` 已通过。
- 若要提升 release gate 体验，给全量矩阵增加 case-level timing、失败样本定位和可选并行执行。
- 不在未 profiling 前改命理核心算法；先定位每 case 计算耗时分布。

## Wave 3 Status

| Node | Status | Evidence | Next |
| --- | --- | --- | --- |
| TP-10.03 | Done | Web/branding/API `47 passed` | 进入最终输出审查。 |
| TP-11.01 | Done with performance WARN | full golden `9 passed in 36m51s`；分片合同测试通过。 | 记录为 deep/release-only gate；后续做 timing 优化和并行执行。 |
| TP-13.01 | Done | calendar/solar/golden representative `18 passed, 1 skipped` | 增量样本继续走 golden fixture。 |
| TP-13.02 | Done | API/operability `30 passed` | 进入 Bot outbox/live 恢复路径。 |

## Next Wave Gate

进入 Wave 4：

- `TP-11.02` MingLi-Bench 从 evaluator smoke 升级为 FateCat prediction eval。
- `TP-11.03` local-ci profile 与证据目录固化。
- `TP-12.02` 大文件职责切片。
- `TP-13.03` Bot outbox/live 恢复路径。
