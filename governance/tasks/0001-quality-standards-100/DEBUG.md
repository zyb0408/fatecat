# Debug Evidence

## Bug

当前质量推进任务包含两个已复现门禁失败和多个高风险回归面：

- `ruff format --check .` 当前失败，影响 `local-ci quick` 和 acceptance 本地门禁。
- `bash scripts/production-readiness.sh` 在无生产 env 时因 `FATE_CORS_ALLOW_ORIGINS` 为空失败。
- 时区语义、Bot 背压、legacy Bazi 迁移后续可能改变用户可见行为。

## Environment

- Repository: `/home/lenovo/.projects/fatecat`
- HEAD: `787111d592be`
- Branch: `main`
- Remote delta: local ahead `origin/main` by 7 commits, remote behind count `0`
- Python runtime: project `.venv`
- Current known passing checks: `pytest -q` -> `123 passed`; `ruff check .` PASS; `mypy -p fate_core` PASS

## Reproduction

Known failing commands:

```bash
.venv/bin/python -m ruff format --check .
bash scripts/production-readiness.sh
```

Expected:

- Format gate exits 0.
- Production readiness either passes under production-equivalent env or fails with an explicit HITL blocker when real env is absent.

Actual:

- Format gate reports two files would be reformatted.
- Production readiness fails on empty `FATE_CORS_ALLOW_ORIGINS`.

## Observations

- The repository has a valid local test baseline, but the fastest local CI profile is not currently green because format check is part of `scripts/local-ci.sh --profile quick`.
- `REVIEW.md` is stale and records old HEAD/test evidence, so the review truth source cannot be trusted until refreshed.
- Production readiness is intentionally strict; failing without real env is correct, but `REVIEW.md` must not describe that state as PASS.
- Bot rate limiting currently has a high queue limit and no per-user cooldown accounting, so public Bot traffic still needs backpressure work.

## Hypotheses

### H1 (ROOT HYPOTHESIS): quality gates are fragmented

- Supports: format gate, review truth, local CI, production readiness, live smoke and final review are not currently synchronized into one closed loop.
- Conflicts: if `local-ci all`, production readiness, final review and task closeout all pass without code/doc changes, this hypothesis is wrong.
- Test: execute the planned waves and verify whether each gate closes only after its evidence is updated.

### H2: format failure is mechanical drift

- Supports: `ruff check .` passes and only `ruff format --check .` reports two files would be reformatted.
- Conflicts: if formatting changes behavior tests or introduces lint/type failures, the issue is not purely mechanical.
- Test: run `ruff format`, then `ruff format --check .`, `ruff check .`, and targeted regression tests.

### H3: production readiness failure is environment-contract absence

- Supports: `production-readiness.sh` fails specifically because `FATE_CORS_ALLOW_ORIGINS` is empty.
- Conflicts: if production-equivalent env is configured and readiness still fails on application behavior, this is not only env contract absence.
- Test: run `production-readiness.sh --skip-bootstrap` under explicit production-equivalent env and record each OK/WARN/FAIL.

### H4: maintainability cannot reach 100% while delivery owns domain core

- Supports: `legacy_bazi.py` still routes fate-core through delivery `BaziCalculator`, and large files hold mixed calculation/report/delivery responsibilities.
- Conflicts: if boundary review proves the current ownership is intentional, stable, and not blocking future changes, this hypothesis weakens.
- Test: produce a boundary map, then run architecture/future-optimal/ponytail review against the migration plan.

## Experiments

Planned by task leaves:

- `TP-01.01`: run `ruff format`, then `ruff format --check .`.
- `TP-01.03`: run `bash scripts/local-ci.sh --profile quick`.
- `TP-02.01`: run `bash scripts/production-readiness.sh --skip-bootstrap` with production-equivalent env.
- `TP-02.03`: run `bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot` when real external inputs exist.

## Root Cause

Partial conclusion:

- `TP-01.01` confirms H2: the format failure was mechanical Ruff drift in two files, not a behavior defect.

Remaining root hypothesis is that quality evidence is still fragmented across stale review docs, production env assumptions and unexecuted external validation.

## Fix

- `TP-01.01`: executed `.venv/bin/python -m ruff format domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_bazi_ziwei_rule_depth.py`.

## Regression Evidence

Initial baseline only:

- `pytest -q`: `123 passed`
- `ruff check .`: PASS
- `mypy -p fate_core`: PASS

Completed evidence:

- `TP-01.01`: `.venv/bin/python -m ruff format --check .` -> `113 files already formatted`
- `TP-01.01`: `.venv/bin/python -m ruff check .` -> `All checks passed!`
- `TP-01.01`: `git diff --check -- <formatted files>` -> no output
- `TP-01.02`: `REVIEW.md` refreshed to HEAD `787111d592be`, pytest `123 passed in 157.07s`, production-readiness FAIL without `FATE_CORS_ALLOW_ORIGINS`
- `TP-01.02`: `rg '9106be0|120 passed|GitHub Actions|Acceptance success|production.*PASS|scripts/project' REVIEW.md` -> no output
- `TP-01.03`: `bash scripts/local-ci.sh --profile quick` -> PASS; focused regression `42 passed in 7.46s`
- `TP-01.03`: evidence directory `/tmp/fatecat-local-ci-20260615175002` contains `preflight-pure.json` and `summary.txt`; `git diff --check` -> no output
- `TP-02.01`: `bash scripts/production-readiness.sh --skip-bootstrap` without env -> expected FAIL on empty `FATE_CORS_ALLOW_ORIGINS`; production-equivalent env with CORS/records/rate/backend/edge/proxy/HSTS -> PASS.
- `TP-03.01`: timezone-aware input now converts through `timezone` / `inputTimezone` / `birthPlace.timezone` / default `Asia/Shanghai`; targeted regression `38 passed`.
- `TP-03.02`: Bot rate limiter now has bounded queue and optional user limits; `pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py` -> `6 passed`.
- `TP-03.03`: API/Web guardrails `pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py` -> `33 passed`.
- `TP-04.01`: core evidence items now carry `riskBoundary`; evidence/policy/pure-analysis regression `28 passed`.
- `TP-04.04`: `bash scripts/run-mingli-bench.sh --stats --sample 5` -> local stats PASS; REVIEW records no external model API call.
- `TP-05.01`: `DEBT-0001-fatecat-core-boundary-map.md` covers six large core files with keep/migrate/forbid boundaries; `rg` verified required rows and fields.
- `TP-06.01`: CalendarProvider dependency contract verified; lunar-python is declared dependency and adapter prefers package import before vendor fallback.
- `TP-06.02`: vendor manifest v3 verified by `bash scripts/vendor-health.sh`; policy tests `9 passed`; missing-license materials are blocked from production role.

- `TP-02.02`: 2026-06-15：`bash scripts/local-ci.sh --profile public-service` -> PASS；静态 production-readiness OK，Bot live/API URL 按无真实外部输入保持 SKIP，不伪造公网验收。
- `TP-03.04`: 2026-06-15：新增 `calendar_boundary_cases.json` 锁定早晚子时、真太阳时、时区转换和历法边界；`pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py` -> `12 passed in 125.38s`。
- `TP-04.03`: 2026-06-15：专题 profile 测试禁止输出 statement/prediction/advice 等断语字段和确定性/专业建议词；`pytest tests/regression/test_bazi_ziwei_rule_depth.py` -> `22 passed in 60.12s`。
- `TP-05.02`: 2026-06-15：新增 `fate_core/usecases/evidence_builder.py`，从 `calculate_pure_analysis.py` 抽出 evidence 构建、风险边界和 append 流程；pure-analysis/rule-depth 回归 `23 passed in 59.92s`，ruff pass。
- `TP-05.04`: 2026-06-15：新增 delivery 边界合同测试，API/Web/Bot/report 禁止读取领域规则源，legacy 八字算法只剩 `bazi_calculator.py` 迁移窗口；delivery+web+api 回归 `49 passed in 6.99s`。
- `TP-06.03`: 2026-06-15：新增 `test_calendar_oracle_contract.py`，用 `sxtwl` 对照 `lunar-python` 稳定四柱样本，并扫描 oracle 库不得进入生产源码；`pytest tests/regression/test_calendar_oracle_contract.py` -> `3 passed in 0.04s`。
- `TP-06.04`: 2026-06-15：`rule_depth_registry.json`、`classics_rule_index.json`、`future_features.json` 增加 owner 与 extensionPolicy；policy/rule-depth 回归 `33 passed in 60.84s`。
- `TP-07.01`: 2026-06-15：`/metrics` 增加 Bot 队列 gauge；`references/ops-pack.md` 记录 Prometheus/Grafana 面板与告警；API/operability 回归 `26 passed in 4.04s`，ruff pass。
- `TP-07.02`: 2026-06-15：API 中间件使用 `ContextVar` 贯穿 `X-Request-ID` 到业务异常日志；新增业务异常日志测试，`test_api_contracts.py` -> `25 passed in 3.84s`。
- `TP-07.03`: 2026-06-15：`references/ops-pack.md` 增加公共服务 SLO、上线、回滚、降级和清理 runbook；`test_operability_docs.py` 锁定 REVIEW/ops-pack/commands 引用。
- `TP-02.03`: 2026-06-15：检查环境变量未发现真实生产 API URL 或 `FATE_BOT_TOKEN`；该叶子需要真实域名/TLS/反向代理/生产 URL/真实 Bot token，当前按 HITL 阻塞处理，不伪造 live 验收。
- `TP-04.02`: 2026-06-15：新增 120 样本 `coverage_matrix_cases.json`，覆盖节气边界、子时边界、合化守卫、从格守卫、岁运锚点、证据深度等标签；`pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_statement_golden.py tests/regression/test_solar_terms_golden.py` -> `19 passed in 154.96s`；JSON 与 ruff 校验通过。
- `TP-07.04`: 2026-06-15：`bash scripts/local-ci.sh --profile all` -> PASS；full pytest `152 passed in 226.19s`；Docker image build 与容器 `/web` smoke OK；production-readiness 静态门禁 OK，外部 API URL 与 live Bot 因缺真实输入保持 SKIP；证据目录 `/tmp/fatecat-local-ci-20260615185918`。
- `TP-05.03`: 2026-06-15：八字 legacy 核心迁入 `fate_core.kernel.bazi_calculator`，delivery `src/bazi_calculator.py` 收缩为兼容导出；`legacy_bazi` 不再从 delivery `src` 导入领域算法；`pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_statement_golden.py tests/regression/test_solar_terms_golden.py tests/regression/test_api_contracts.py tests/regression/test_web_html.py tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_fate_policy_assets.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py` -> `74 passed in 158.97s`；ruff check 与 Python format check 通过。
- `TP-05.05`: 2026-06-15：active catalog 清退 `compatibility_source_root`/`temporary-compatibility-box` 并改为 canonical-active；新增 `compatibility-ledger.md` 记录保留兼容入口 owner/真实契约/移除条件；`pytest tests/regression/test_catalog_contracts.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py` -> `11 passed`；`bash scripts/check-structure.sh` -> `structure gate ok`；active 扫描只剩 guard/test/AGENTS 防回潮文本；ruff check/format 通过。
- `TP-07.04`: 2026-06-15 当前工作树刷新：`bash scripts/local-ci.sh --profile all` -> PASS；quick/focused regression `43 passed in 7.22s`；full pytest `158 passed in 222.09s`；ruff/mypy PASS；delivery API/Bot smoke、export hygiene、Docker image build、容器 `/web` smoke OK；production-readiness 静态门禁 OK，外部 API URL 与 live Bot 因缺真实输入保持 SKIP；证据目录 `/tmp/fatecat-local-ci-20260615193100`。
Closeout requires continuing this section with actual executed evidence for each completed leaf task.
