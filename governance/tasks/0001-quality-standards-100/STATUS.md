# Task Status
- Overall Status: `Blocked`

# Next Executable Leaves
- None. Remaining final closeout leaves are blocked by `TP-02.03` external HITL live-production evidence.

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | TP-01.01 Done；TP-01.02 Done；TP-01.03 Done。 | 无 | 无 |
| TP-01.01 | TP-01 | 2 | - | No | Done | 2026-06-15：复现 `.venv/bin/python -m ruff format --check .` 失败，仅 2 文件需格式化；执行 `ruff format` 后 `.venv/bin/python -m ruff format --check .` -> `113 files already formatted`，`.venv/bin/python -m ruff check .` -> `All checks passed!`；`git diff --check` 无输出；diff 为 Ruff 折行格式化。 | 无 | 无 |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | 2026-06-15：REVIEW.md 已刷新到 HEAD `787111d592be`、pytest `123 passed in 157.07s`、production-readiness 无 env 真实 FAIL；`rg '9106be0\|120 passed\|GitHub Actions\|Acceptance success\|production.*PASS\|scripts/project' REVIEW.md` 无输出。 | 无 | 无 |
| TP-01.03 | TP-01 | 2 | TP-01.01, TP-01.02 | No | Done | 2026-06-15：`bash scripts/local-ci.sh --profile quick` PASS；focused regression `42 passed in 7.46s`；证据目录 `/tmp/fatecat-local-ci-20260615175002` 含 `preflight-pure.json` 和 `summary.txt`；`git diff --check` 无输出。 | 无 | 无 |
| TP-02 | ROOT | 1 | TP-01.03 | No | Blocked | TP-02.01/TP-02.02 已完成；TP-02.03 因缺少真实公网 URL 与真实 Bot token 进入 HITL 阻塞。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 提供生产 HTTPS URL、TLS/反向代理配置、生产 CORS allowlist、真实 FATE_BOT_TOKEN 后运行 `bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot`。 |
| TP-02.01 | TP-02 | 2 | TP-01.03 | No | Done | 2026-06-15：`production-readiness.sh --skip-bootstrap` 无 env 真实 FAIL；生产等价 env 下 PASS；`references/commands.md` 与 `references/ops-pack.md` 已固化 CORS、records、rate backend、edge body limit、proxy headers、HSTS 合同。 | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-01.03, TP-02.01 | No | Done | 2026-06-15：`bash scripts/local-ci.sh --profile public-service` -> PASS；静态 production-readiness OK，Bot live/API URL 按无真实外部输入保持 SKIP，不伪造公网验收。 | 无 | 无 |
| TP-02.03 | TP-02 | 2 | TP-01.03, TP-02.02 | No | Blocked | 2026-06-15：检查环境变量未发现真实生产 API URL 或 `FATE_BOT_TOKEN`；该叶子需要真实域名/TLS/反向代理/生产 URL/真实 Bot token，当前按 HITL 阻塞处理，不伪造 live 验收。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 提供生产 HTTPS URL、TLS/反向代理配置、生产 CORS allowlist、真实 FATE_BOT_TOKEN 后运行 `bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot`。 |
| TP-03 | ROOT | 1 | TP-01.03 | No | Done | 已完成：TP-03.01, TP-03.02, TP-03.03, TP-03.04。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-01.03 | No | Done | 2026-06-15：时区语义改为按 `timezone`/`inputTimezone`/`birthPlace.timezone`/默认 `Asia/Shanghai` 转换 aware datetime；`pytest tests/regression/test_fate_core_cli.py tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_api_contracts.py` -> `38 passed in 4.03s`。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-01.03 | No | Done | 2026-06-15：Bot rate limiter 改为有界队列和可选用户级限制；`pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py` -> `6 passed in 0.02s`。 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-01.03 | No | Done | 2026-06-15：API/Web guardrails 回归 `pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py` -> `33 passed in 5.33s`。 | 无 | 无 |
| TP-03.04 | TP-03 | 2 | TP-01.03, TP-03.01 | No | Done | 2026-06-15：新增 `calendar_boundary_cases.json` 锁定早晚子时、真太阳时、时区转换和历法边界；`pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py` -> `12 passed in 125.38s`。 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-01.03 | No | Done | 已完成：TP-04.01, TP-04.02, TP-04.03, TP-04.04。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-01.03 | No | Done | 2026-06-15：核心 evidence item 增加 `riskBoundary` 并补 schema/test；`pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/fate_core/test_pure_analysis_usecase.py` -> `28 passed in 61.48s`。 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-01.03, TP-03.04, TP-04.01 | No | Done | 2026-06-15：新增 120 样本 `coverage_matrix_cases.json`，覆盖节气边界、子时边界、合化守卫、从格守卫、岁运锚点、证据深度等标签；golden matrix、statement golden、solar terms 回归 `19 passed in 154.96s`；JSON 与 ruff 校验通过。 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-01.03, TP-04.01 | No | Done | 2026-06-15：专题 profile 测试禁止输出 statement/prediction/advice 等断语字段和确定性/专业建议词；`pytest tests/regression/test_bazi_ziwei_rule_depth.py` -> `22 passed in 60.12s`。 | 无 | 无 |
| TP-04.04 | TP-04 | 2 | TP-01.03 | No | Done | 2026-06-15：`bash scripts/run-mingli-bench.sh --stats --sample 5` 离线统计 PASS；`REVIEW.md` 已记录 MingLi-Bench 本地评测入口，不调用外部模型 API。 | 无 | 无 |
| TP-05 | ROOT | 1 | TP-01.03 | No | Done | 已完成：TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05。 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-01.03 | No | Done | 2026-06-15：新增 `governance/evidence/tech-debt/DEBT-0001-fatecat-core-boundary-map.md`；`rg` 验证六个核心大文件均有保留职责、迁出职责、禁止新增职责和承接任务。 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-01.03, TP-04.01, TP-05.01 | No | Done | 2026-06-15：新增 `fate_core/usecases/evidence_builder.py`，从 `calculate_pure_analysis.py` 抽出 evidence 构建、风险边界和 append 流程；pure-analysis/rule-depth 回归 `23 passed in 59.92s`，ruff pass。 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-01.03, TP-04.02, TP-05.01 | No | Done | 2026-06-15：八字 legacy 核心迁入 `fate_core.kernel.bazi_calculator`，delivery `src/bazi_calculator.py` 收缩为兼容导出；`legacy_bazi` 不再从 delivery `src` 导入领域算法；golden/API/Web/pure-analysis/边界/策略回归 `74 passed in 158.97s`；ruff check 与 Python format check 通过。 | 无 | 无 |
| TP-05.04 | TP-05 | 2 | TP-01.03, TP-03.02, TP-03.03, TP-05.01 | No | Done | 2026-06-15：新增 delivery 边界合同测试，API/Web/Bot/report 禁止读取领域规则源，legacy 八字算法只剩 `bazi_calculator.py` 迁移窗口；delivery+web+api 回归 `49 passed in 6.99s`。 | 无 | 无 |
| TP-05.05 | TP-05 | 2 | TP-01.03, TP-05.03, TP-05.04 | No | Done | 2026-06-15：active catalog 清退 `compatibility_source_root`/`temporary-compatibility-box` 并改为 canonical-active；新增 `compatibility-ledger.md` 记录保留兼容入口 owner/真实契约/移除条件；catalog/service 边界测试 `11 passed`，structure gate OK，active 扫描只剩 guard/test/AGENTS 防回潮文本；ruff check/format 通过。 | 无 | 无 |
| TP-06 | ROOT | 1 | TP-01.03 | No | Done | 已完成：TP-06.01, TP-06.02, TP-06.03, TP-06.04。 | 无 | 无 |
| TP-06.01 | TP-06 | 2 | TP-01.03 | No | Done | 2026-06-15：lunar-python 生产依赖合同显式化，adapter 优先包依赖、vendor 仅开发兜底；`pytest test_lunar_python_is_declared_as_runtime_dependency test_lunar_calendar_adapter_prefers_declared_dependency_over_vendor_path tests/regression/test_solar_terms_golden.py` -> `8 passed in 29.33s`。 | 无 | 无 |
| TP-06.02 | TP-06 | 2 | TP-01.03 | No | Done | 2026-06-15：`vendor_sources.json` 升级到 v3，补 `usageRole`/`productionUseAllowed`/风险说明；`bash scripts/vendor-health.sh` PASS；`pytest tests/regression/test_fate_policy_assets.py` -> `9 passed in 0.56s`。 | 无 | 无 |
| TP-06.03 | TP-06 | 2 | TP-01.03, TP-06.01, TP-06.02 | No | Done | 2026-06-15：新增 `test_calendar_oracle_contract.py`，用 `sxtwl` 对照 `lunar-python` 稳定四柱样本，并扫描 oracle 库不得进入生产源码；`pytest tests/regression/test_calendar_oracle_contract.py` -> `3 passed in 0.04s`。 | 无 | 无 |
| TP-06.04 | TP-06 | 2 | TP-01.03, TP-04.01 | No | Done | 2026-06-15：`rule_depth_registry.json`、`classics_rule_index.json`、`future_features.json` 增加 owner 与 extensionPolicy；policy/rule-depth 回归 `33 passed in 60.84s`。 | 无 | 无 |
| TP-07 | ROOT | 1 | TP-02.01, TP-03.03 | No | Done | 已完成：TP-07.01, TP-07.02, TP-07.03, TP-07.04；TP-07.04 已刷新到当前工作树 all-profile PASS。 | 无 | 无 |
| TP-07.01 | TP-07 | 2 | TP-02.01, TP-03.03 | No | Done | 2026-06-15：`/metrics` 增加 Bot 队列 gauge；`references/ops-pack.md` 记录 Prometheus/Grafana 面板与告警；API/operability 回归 `26 passed in 4.04s`，ruff pass。 | 无 | 无 |
| TP-07.02 | TP-07 | 2 | TP-02.01, TP-03.03 | No | Done | 2026-06-15：API 中间件使用 `ContextVar` 贯穿 `X-Request-ID` 到业务异常日志；新增业务异常日志测试，`test_api_contracts.py` -> `25 passed in 3.84s`。 | 无 | 无 |
| TP-07.03 | TP-07 | 2 | TP-02.01, TP-03.03 | No | Done | 2026-06-15：`references/ops-pack.md` 增加公共服务 SLO、上线、回滚、降级和清理 runbook；`test_operability_docs.py` 锁定 REVIEW/ops-pack/commands 引用。 | 无 | 无 |
| TP-07.04 | TP-07 | 2 | TP-02.01, TP-02.02, TP-03.02, TP-03.03, TP-07.01, TP-07.03 | No | Done | 2026-06-15：当前工作树 `bash scripts/local-ci.sh --profile all` -> PASS；quick/focused regression `43 passed in 7.22s`；full pytest `158 passed in 222.09s`；ruff/mypy PASS；delivery API/Bot smoke、export hygiene、Docker image build、容器 `/web` smoke OK；production-readiness 静态门禁 OK，外部 API URL 与 live Bot 因缺真实输入保持 SKIP；证据目录 `/tmp/fatecat-local-ci-20260615193100`。 | 无 | 无 |
| TP-08 | ROOT | 1 | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04 | No | Blocked | 内部前置任务已完成；最终审查/closeout 仍依赖 TP-02.03 真实公网 API 与 Bot live 验收，当前按外部 HITL 阻塞，不伪造 100% 完成。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 提供生产 HTTPS URL、TLS/反向代理配置、生产 CORS allowlist、真实 FATE_BOT_TOKEN 后运行 `bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot`，再执行最终 review/closeout。 |
| TP-08.01 | TP-08 | 2 | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04 | No | Blocked | 内部前置任务已完成；最终审查仍依赖 TP-02.03 真实公网 API 与 Bot live 验收。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 完成 TP-02.03 后执行最终全仓质量审查。 |
| TP-08.02 | TP-08 | 2 | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04, TP-08.01 | No | Blocked | 内部前置任务已完成；review finding 处理依赖 TP-08.01。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 完成 TP-02.03 与 TP-08.01 后处理最终 findings。 |
| TP-08.03 | TP-08 | 2 | TP-02.03, TP-04.02, TP-05.05, TP-06.03, TP-07.04, TP-08.02 | No | Blocked | 内部前置任务已完成；closeout 依赖 TP-08.02。 | 缺少真实公网生产 URL 和真实 Telegram Bot token | 完成 TP-02.03、TP-08.01、TP-08.02 后生成最终 closeout。 |

# Blockers
- `TP-02.03`: 缺少真实公网生产 URL 和真实 Telegram Bot token；解除条件：提供生产 HTTPS URL、TLS/反向代理配置、生产 CORS allowlist、真实 FATE_BOT_TOKEN 后运行 `bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot`。
- `TP-08.*`: 最终 review/closeout 依赖 `TP-02.03` 的真实公网 API 与 Bot live 验收；在外部证据未提供前保持 Blocked。

# Runtime State
- Active workflow state: 以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Stop condition: 需要真实公网 URL 或 Bot token 但未提供时，停止对应 HITL 叶子，不伪造通过。
- Stop condition: 命理核心输出变化但 golden/oracle 无法解释时，停止迁移，进入 debug/review。
- Stop condition: local-ci 或 full acceptance 出现未知失败时，转 auto-debug。
- TP-01.01: status=Done; verifier_context=自审；evidence=2026-06-15：复现 `.venv/bin/python -m ruff format --check .` 失败，仅 2 文件需格式化；执行 `ruff format` 后 `.venv/bin/python -m ruff format --check .` -> `113 files already formatted`，`.venv/bin/python -m ruff check .` -> `All checks passed!`；`git diff --check` 无输出；diff 为 Ruff 折行格式化。
- TP-01.02: status=Done; verifier_context=自审；evidence=2026-06-15：REVIEW.md 已刷新到 HEAD `787111d592be`、pytest `123 passed in 157.07s`、production-readiness 无 env 真实 FAIL；`rg '9106be0|120 passed|GitHub Actions|Acceptance success|production.*PASS|scripts/project' REVIEW.md` 无输出。
- TP-01.03: status=Done; verifier_context=自审；evidence=2026-06-15：`bash scripts/local-ci.sh --profile quick` PASS；focused regression `42 passed in 7.46s`；证据目录 `/tmp/fatecat-local-ci-20260615175002` 含 `preflight-pure.json` 和 `summary.txt`；`git diff --check` 无输出。
- TP-02.01: status=Done; verifier_context=自审；evidence=2026-06-15：`production-readiness.sh --skip-bootstrap` 无 env 真实 FAIL；生产等价 env 下 PASS；`references/commands.md` 与 `references/ops-pack.md` 已固化 CORS、records、rate backend、edge body limit、proxy headers、HSTS 合同。
- TP-02.02: status=Done; verifier_context=自审；evidence=2026-06-15：`bash scripts/local-ci.sh --profile public-service` -> PASS；静态 production-readiness OK，Bot live/API URL 按无真实外部输入保持 SKIP，不伪造公网验收。
- TP-02.03: status=Blocked; verifier_context=自审；evidence=2026-06-15：检查环境变量未发现真实生产 API URL 或 `FATE_BOT_TOKEN`；该叶子需要真实域名/TLS/反向代理/生产 URL/真实 Bot token，当前按 HITL 阻塞处理，不伪造 live 验收。
- TP-03.01: status=Done; verifier_context=自审；evidence=2026-06-15：时区语义改为按 `timezone`/`inputTimezone`/`birthPlace.timezone`/默认 `Asia/Shanghai` 转换 aware datetime；`pytest tests/regression/test_fate_core_cli.py tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_api_contracts.py` -> `38 passed in 4.03s`。
- TP-03.02: status=Done; verifier_context=自审；evidence=2026-06-15：Bot rate limiter 改为有界队列和可选用户级限制；`pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py` -> `6 passed in 0.02s`。
- TP-03.03: status=Done; verifier_context=自审；evidence=2026-06-15：API/Web guardrails 回归 `pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py` -> `33 passed in 5.33s`。
- TP-03.04: status=Done; verifier_context=自审；evidence=2026-06-15：新增 `calendar_boundary_cases.json` 锁定早晚子时、真太阳时、时区转换和历法边界；`pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py` -> `12 passed in 125.38s`。
- TP-04.01: status=Done; verifier_context=自审；evidence=2026-06-15：核心 evidence item 增加 `riskBoundary` 并补 schema/test；`pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/fate_core/test_pure_analysis_usecase.py` -> `28 passed in 61.48s`。
- TP-04.02: status=Done; verifier_context=自审；evidence=2026-06-15：新增 120 样本 `coverage_matrix_cases.json`，覆盖节气边界、子时边界、合化守卫、从格守卫、岁运锚点、证据深度等标签；golden matrix、statement golden、solar terms 回归 `19 passed in 154.96s`；JSON 与 ruff 校验通过。
- TP-04.03: status=Done; verifier_context=自审；evidence=2026-06-15：专题 profile 测试禁止输出 statement/prediction/advice 等断语字段和确定性/专业建议词；`pytest tests/regression/test_bazi_ziwei_rule_depth.py` -> `22 passed in 60.12s`。
- TP-04.04: status=Done; verifier_context=自审；evidence=2026-06-15：`bash scripts/run-mingli-bench.sh --stats --sample 5` 离线统计 PASS；`REVIEW.md` 已记录 MingLi-Bench 本地评测入口，不调用外部模型 API。
- TP-05.01: status=Done; verifier_context=自审；evidence=2026-06-15：新增 `governance/evidence/tech-debt/DEBT-0001-fatecat-core-boundary-map.md`；`rg` 验证六个核心大文件均有保留职责、迁出职责、禁止新增职责和承接任务。
- TP-05.02: status=Done; verifier_context=自审；evidence=2026-06-15：新增 `fate_core/usecases/evidence_builder.py`，从 `calculate_pure_analysis.py` 抽出 evidence 构建、风险边界和 append 流程；pure-analysis/rule-depth 回归 `23 passed in 59.92s`，ruff pass。
- TP-05.03: status=Done; verifier_context=自审；evidence=2026-06-15：八字 legacy 核心迁入 `fate_core.kernel.bazi_calculator`，delivery `src/bazi_calculator.py` 收缩为兼容导出；`legacy_bazi` 不再从 delivery `src` 导入领域算法；golden/API/Web/pure-analysis/边界/策略回归 `74 passed in 158.97s`；ruff check 与 Python format check 通过。
- TP-05.04: status=Done; verifier_context=自审；evidence=2026-06-15：新增 delivery 边界合同测试，API/Web/Bot/report 禁止读取领域规则源，legacy 八字算法只剩 `bazi_calculator.py` 迁移窗口；delivery+web+api 回归 `49 passed in 6.99s`。
- TP-05.05: status=Done; verifier_context=自审；evidence=2026-06-15：active catalog 清退 `compatibility_source_root`/`temporary-compatibility-box` 并改为 canonical-active；新增 `compatibility-ledger.md` 记录保留兼容入口 owner/真实契约/移除条件；catalog/service 边界测试 `11 passed`，structure gate OK，active 扫描只剩 guard/test/AGENTS 防回潮文本；ruff check/format 通过。
- TP-06.01: status=Done; verifier_context=自审；evidence=2026-06-15：lunar-python 生产依赖合同显式化，adapter 优先包依赖、vendor 仅开发兜底；`pytest test_lunar_python_is_declared_as_runtime_dependency test_lunar_calendar_adapter_prefers_declared_dependency_over_vendor_path tests/regression/test_solar_terms_golden.py` -> `8 passed in 29.33s`。
- TP-06.02: status=Done; verifier_context=自审；evidence=2026-06-15：`vendor_sources.json` 升级到 v3，补 `usageRole`/`productionUseAllowed`/风险说明；`bash scripts/vendor-health.sh` PASS；`pytest tests/regression/test_fate_policy_assets.py` -> `9 passed in 0.56s`。
- TP-06.03: status=Done; verifier_context=自审；evidence=2026-06-15：新增 `test_calendar_oracle_contract.py`，用 `sxtwl` 对照 `lunar-python` 稳定四柱样本，并扫描 oracle 库不得进入生产源码；`pytest tests/regression/test_calendar_oracle_contract.py` -> `3 passed in 0.04s`。
- TP-06.04: status=Done; verifier_context=自审；evidence=2026-06-15：`rule_depth_registry.json`、`classics_rule_index.json`、`future_features.json` 增加 owner 与 extensionPolicy；policy/rule-depth 回归 `33 passed in 60.84s`。
- TP-07.01: status=Done; verifier_context=自审；evidence=2026-06-15：`/metrics` 增加 Bot 队列 gauge；`references/ops-pack.md` 记录 Prometheus/Grafana 面板与告警；API/operability 回归 `26 passed in 4.04s`，ruff pass。
- TP-07.02: status=Done; verifier_context=自审；evidence=2026-06-15：API 中间件使用 `ContextVar` 贯穿 `X-Request-ID` 到业务异常日志；新增业务异常日志测试，`test_api_contracts.py` -> `25 passed in 3.84s`。
- TP-07.03: status=Done; verifier_context=自审；evidence=2026-06-15：`references/ops-pack.md` 增加公共服务 SLO、上线、回滚、降级和清理 runbook；`test_operability_docs.py` 锁定 REVIEW/ops-pack/commands 引用。
- TP-07.04: status=Done; verifier_context=自审；evidence=2026-06-15：当前工作树 `bash scripts/local-ci.sh --profile all` -> PASS；quick/focused regression `43 passed in 7.22s`；full pytest `158 passed in 222.09s`；ruff/mypy PASS；delivery API/Bot smoke、export hygiene、Docker image build、容器 `/web` smoke OK；production-readiness 静态门禁 OK，外部 API URL 与 live Bot 因缺真实输入保持 SKIP；证据目录 `/tmp/fatecat-local-ci-20260615193100`。
- TP-08.01: status=Blocked; verifier_context=自审；evidence=内部前置任务已完成；最终审查仍依赖 TP-02.03 真实公网 API 与 Bot live 验收。
- TP-08.02: status=Blocked; verifier_context=自审；evidence=内部前置任务已完成；review finding 处理依赖 TP-08.01。
- TP-08.03: status=Blocked; verifier_context=自审；evidence=内部前置任务已完成；closeout 依赖 TP-08.02。
