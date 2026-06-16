# Task Status
- Overall Status: `In Progress`

# Systemic Improvement Plan V2
- Plan file: `SYSTEMIC_IMPROVEMENT_PLAN.md`
- Wave 1 evidence: `WAVE1_EXECUTION.md`
- Wave 2 evidence: `WAVE2_EXECUTION.md`
- Wave 3 evidence: `WAVE3_EXECUTION.md`
- Wave 4 evidence: `WAVE4_EXECUTION.md`
- Final review: `FINAL_REVIEW.md`
- Closeout: `CLOSEOUT.md`
- Planning status: `Closed with WARN/HITL`
- Quality dimensions: `满足约束` / `可解释` / `可测试` / `可维护` / `处理特殊情况` / `复用建立在理解上`
- Current verdict from six-dimension audit: `WARN`
- Latest evidence:
  - 2026-06-16：`bash scripts/local-ci.sh --profile quick` -> PASS，证据目录 `/tmp/fatecat-local-ci-20260616000719`，focused regression `47 passed in 7.40s`。
  - 2026-06-16：命理/能力专项 pytest -> `44 passed, 1 skipped in 89.30s`。
  - 2026-06-16：`bash scripts/vendor-health.sh` -> `vendor health ok: required=5 optionalFutureFeatures=12 hashed=17 licenseAuditRequired=5`。
  - 2026-06-16：`production-readiness.sh --skip-bootstrap` 静态门禁 PASS；live API/Bot 因缺真实 URL/token 保持 SKIP。
  - 2026-06-16：principle gate scan 返回 `BLOCK / 42 findings`；需按 active/archive 分流处理。
  - 2026-06-16：Wave 1 执行记录已落盘到 `WAVE1_EXECUTION.md`；`TP-09.02`、`TP-10.01`、`TP-14.01` PASS，`TP-09.01` 完成交付切分设计，`TP-12.01` 因 principle gate active/archive 分流未完成保持 BLOCK。
  - 2026-06-16：Wave 2 执行记录已落盘到 `WAVE2_EXECUTION.md`；API contracts `29 passed`，provider/adapter `13 passed`，active-only principle gate `finding_count=0`，policy/catalog/capability/service contract 回归 `34 passed`。
  - 2026-06-16：Wave 3 执行记录已落盘到 `WAVE3_EXECUTION.md`；Web/branding/API `47 passed`，calendar/solar/golden representative `18 passed, 1 skipped`，API/operability `30 passed`，full 300+ golden release gate `9 passed in 36m51s`。
  - 2026-06-16：Wave 4 执行记录已落盘到 `WAVE4_EXECUTION.md`；FateCat-generated MingLi scored baseline 生成和 evaluator 通过，sample 10 accuracy `30%`，local-ci all PASS `/tmp/fatecat-local-ci-20260616012307`，Bot outbox `2 passed`，大文件治理仍 WARN。
  - 2026-06-16：Wave 5 最终审查已落盘到 `FINAL_REVIEW.md` 与 `CLOSEOUT.md`；active 本地门禁无 BLOCK，剩余 WARN/HITL 包括 full golden 过慢、MingLi sample 10 accuracy 30%、核心大文件、真实公网 live 输入缺失。
  - 2026-06-16：本轮 MingLi/golden 修复后 `bash scripts/local-ci.sh --profile quick` -> PASS，证据目录 `/tmp/fatecat-local-ci-20260616022256`；本轮实际改动文件 principle gate -> PASS，`finding_count=0`。
- Recommended next wave:
  - 修 full golden 性能观测
  - 建设 MingLi 专题推理器
  - 继续大文件切片
  - 等真实公网 URL/token 后跑 live gate

# Systemic Wave Node Status
| Node ID | Status | Evidence | Blocker | Next |
| --- | --- | --- | --- | --- |
| TP-09.01 | Done | `WAVE1_EXECUTION.md` 定义交付单元 A-F、验证命令和回滚边界。 | 无 | 后续提交必须按单元切分。 |
| TP-09.02 | Done | `rg 'HITL\|--require-live-bot\|--api-url\|SKIP\|live Bot\|真实' REVIEW.md references scripts governance/tasks -n` 命中 REVIEW、production-readiness、local-ci、commands、live-bot-verification。 | 无 | 真实 URL/token 到位后执行 live gate。 |
| TP-10.01 | Done | `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_ziwei_rule_depth.py -q` -> `35 passed in 62.49s`。 | 无 | 进入 TP-10.02。 |
| TP-12.01 | Done | active-only principle gate：`git diff --name-only HEAD \| rg -v '^governance/archive/' \| scan_principle_gates.py --files-from /dev/stdin --strict` -> `PASS / finding_count=0`。 | 无 | 全量 archive finding 仅 informational。 |
| TP-14.01 | Done | `bash scripts/vendor-health.sh` -> `vendor health ok: required=5 optionalFutureFeatures=12 hashed=17 licenseAuditRequired=5`。 | 无 | 进入 TP-14.02/TP-14.03。 |
| TP-09.03 | Done | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py -q` -> `29 passed in 3.94s`。 | 无 | 进入 TP-13.02。 |
| TP-10.02 | Done | `python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null` -> PASS。 | 无 | 继续扩展高级规则内容完整度。 |
| TP-12.03 | Done | `rg legacy/compat/shim/wrapper/fallback` 已分类 retained runtime、guard/evidence、domain vocabulary。 | 无 | retained runtime compatibility 进入后续 burn-down。 |
| TP-14.02 | Done | `.venv/bin/python -m pytest tests/regression/test_capability_protocol.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py -q` -> `13 passed in 0.21s`。 | 无 | 进入输出链路可追溯性。 |
| TP-14.03 | Done | `rg productionUseAllowed/reference_only/oracle_only/licenseStatus tools/reference-repos/vendor_sources.json -n` -> manifest 边界明确。 | 无 | 继续由 vendor-health 守门。 |
| TP-10.03 | Done | `.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_branding_support.py tests/regression/test_api_contracts.py -q` -> `47 passed in 7.38s`。 | 无 | 进入最终输出审查。 |
| TP-11.01 | Done with WARN | `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q` -> `9 passed in 2211.71s`；分片覆盖测试通过。 | 全量 gate 太慢，不适合 quick profile。 | 保持 deep/release-only；后续补 case-level timing 与并行执行。 |
| TP-13.01 | Done | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py -q` -> `18 passed, 1 skipped in 97.87s`。 | 无 | 继续新增边界样本。 |
| TP-13.02 | Done | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py -q` -> `30 passed in 3.89s`。 | 无 | 进入 Bot outbox/live 恢复路径。 |
| TP-11.02 | Done with WARN | `generate-mingli-predictions.sh --year 2025 --sample 10` 生成 FateCat scored baseline；`run-mingli-bench.sh` answered `10/10`，accuracy `30%`；MingLi/golden 专项 `11 passed, 1 skipped`。 | 当前弱关键词 baseline 不证明专业准确率。 | 后续建设专题推理器和真实样本外评分。 |
| TP-11.03 | Done | `bash scripts/local-ci.sh --profile all` -> PASS，证据目录 `/tmp/fatecat-local-ci-20260616012307`，full pytest `169 passed, 1 skipped`，container `/web` smoke OK。 | 无 | 作为当前本地 CI/CD 主证据。 |
| TP-12.02 | WARN | line-count map：`bazi_calculator.py` 2500、`report_generator.py` 1941、`calculate_pure_analysis.py` 1375、`bot.py` 1152、`main.py` 1015。 | 大文件仍未完全治理。 | 继续切 bazi kernel、report、pure_analysis、bot、main、web_ui。 |
| TP-13.03 | Done with HITL note | `.venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests/test_bot_send_queue.py -q` -> `2 passed in 0.44s`。 | live Bot 需真实 token。 | 真实 token 到位后跑 live gate。 |
| TP-15.01 | Done | `FINAL_REVIEW.md` 六维审查完成。 | 无 active BLOCK。 | 处理剩余 WARN/HITL。 |
| TP-15.02 | Done with WARN/HITL | active local BLOCK=0；WARN/HITL 已列入 `FINAL_REVIEW.md`。 | full golden 性能、MingLi sample 10 accuracy 30%、大文件、真实 live 输入。 | 后续任务继续推进。 |
| TP-15.03 | Done with WARN/HITL | `CLOSEOUT.md` 生成；不伪造无条件 100%。 | 旧 TODO 原七维任务树未强行勾选。 | 若要正式 closeout 原树，需重编 v2 到 TASK_PACKAGE_SET。 |

# Next Executable Leaves
- TP-05.01 | Wave 5 | Depends On: TP-04.01, TP-04.02, TP-04.03 | Gate: 每条高级格局规则有 source、appliesWhen、doesNotApplyWhen、riskBoundary
- TP-06.01 | Wave 5 | Depends On: TP-03.01, TP-03.02, TP-03.03 | Gate: 本地生产等价静态门禁 PASS；没有真实公网时 live 项保持 SKIP
- TP-06.02 | Wave 5 | Depends On: TP-03.01, TP-03.02, TP-03.03 | Gate: 单实例/多副本限流边界明确；公网入口必须有 edge body limit
- TP-06.03 | Wave 5 | Depends On: TP-03.01, TP-03.02, TP-03.03 | Gate: 5xx/timeout/rate-limit 可从 metrics/log/runbook 定位
- TP-07.01 | Wave 5 | Depends On: TP-04.01, TP-04.02, TP-04.03 | Gate: 外部 API 输出不漂移；kernel/AGENTS.md 同步更新；旧 wrapper 不新增领域逻辑
- TP-07.02 | Wave 5 | Depends On: TP-04.01, TP-04.02, TP-04.03 | Gate: delivery 不新增命理规则；边界合同测试通过；AGENTS.md 同步更新
- TP-07.03 | Wave 5 | Depends On: TP-04.01, TP-04.02, TP-04.03 | Gate: 保留的兼容面均写入 compatibility-ledger；无契约项进入 kill list 或删除

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-00 | ROOT | 1 | - | No | Done | 2026-06-15：0001 INDEX 状态修正完成；0002 任务容器创建、TREE_SPEC.json 写入并通过 apply_task_tree decompose 校验。 | 无 | 无 |
| TP-00.01 | TP-00 | 2 | - | No | Done | 2026-06-15：已将 0001 INDEX 状态改为 Blocked；validate_task_docs.py --phase decompose 返回 ok=true。 | 无 | 无 |
| TP-00.02 | TP-00 | 2 | TP-00.01 | No | Done | 2026-06-15：materialize_task_docs.py 创建 0002 容器；apply_task_tree.py 使用 TREE_SPEC.json 回填 README/CONTEXT/ACCEPTANCE/PLAN/TODO/STATUS；validate_task_docs.py --phase decompose 返回 ok=true。 | 无 | 无 |
| TP-01 | ROOT | 1 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：TP-01.01/TP-01.02/TP-01.03 全部完成；本地开发入口、恢复路径、quick smoke 和 delivery API smoke 均有证据。 | 无 | 无 |
| TP-01.01 | TP-01 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`rg local-ci\|delivery-smoke\|uvicorn\|/web\|Bot references README.md Makefile scripts -n` 命中 README、Makefile、scripts/local-ci.sh、delivery-smoke.sh、references/commands.md、execution-playbook.md、ops-pack.md；本地开发入口存在且不依赖 GitHub Actions。 | 无 | 无 |
| TP-01.02 | TP-01 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`rg venv\|clean-runtime\|pip cache\|pytest_cache\|build/\|dist/ references README.md scripts -n` 命中 bootstrap、clean-runtime、troubleshooting、commands、ops-pack；覆盖 .venv 重建、缓存清理、runtime 清理和导出排除。 | 无 | 无 |
| TP-01.03 | TP-01 | 2 | TP-00.01, TP-00.02, TP-01.01, TP-01.02 | No | Done | 2026-06-15：`bash scripts/local-ci.sh --profile quick` -> PASS，focused regression 43 passed in 7.38s，证据目录 `/tmp/fatecat-local-ci-20260615214051`；`bash scripts/delivery-smoke.sh --target api --port 8011` -> api ready http://127.0.0.1:8011/health。 | 无 | 无 |
| TP-02 | ROOT | 1 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：TP-02.01/TP-02.02/TP-02.03 全部完成；结构/source/export/tasks tree 均通过。 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`bash scripts/check-structure.sh` -> structure gate ok；清理 active README/prompt 中旧口径，剩余 scripts/project 命中均为 CHANGELOG/REVIEW/DEBUG、catalog guard、负例测试、迁移账本、历史证据或 vendor reference archive。 | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`python3 governance/tools/validate_governance_package.py --strict` -> PASS issue_count=0；`rg fate-core\|fatecat-delivery\|compatibility-ledger\|DEBT-0001 catalog governance -n` 证明 catalog、migration ledger、tech-debt evidence 可互相回指。 | 无 | 无 |
| TP-02.03 | TP-02 | 2 | TP-00.01, TP-00.02, TP-02.01, TP-02.02 | No | Done | 2026-06-15：首次裸 `check-export-hygiene.sh` 暴露任务命令缺导出包参数；修正为临时 lite export 后复跑通过：structure gate ok、source hygiene ok、export hygiene ok、validate_tasks_tree ok=true task_total=2 valid=2；历史 `project-history` 已迁入 `governance/archive/tasks/project-history/`。 | 无 | 无 |
| TP-03 | ROOT | 1 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：TP-03.01/TP-03.02/TP-03.03 全部完成；本地 CI/CD all profile 最新通过。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`bash scripts/local-ci.sh --help` 输出 quick/full/container/public-service/all 职责，明确本地 CI/CD 不调用 GitHub Actions。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：`bash scripts/vendor-health.sh` -> vendor health ok；`bash scripts/export-runtime.sh --help` 输出 full/lite export 合同；`docker image inspect fatecat-delivery:local` -> sha256:f025e727b49e97558cc3167fcd9ff8951b1a0b059c1f086c77dbab34b7fac6a3。 | 无 | 无 |
| TP-03.03 | TP-03 | 2 | TP-00.01, TP-00.02, TP-03.01, TP-03.02 | No | Done | 2026-06-15：第一次 `bash scripts/local-ci.sh --profile all` 因 REVIEW.md 缺 `references/ops-pack.md` 引用失败；修复后 `.venv/bin/python -m pytest tests/regression/test_operability_docs.py` -> 1 passed；复跑 `bash scripts/local-ci.sh --profile all` -> PASS，证据目录 `/tmp/fatecat-local-ci-20260615215009`，覆盖 quick、full 158 passed、ruff、mypy、API/Bot dry-run、export、Docker build/container smoke、public-service 静态 readiness。 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：TP-04.01/TP-04.02/TP-04.03 全部完成；八字基础 golden/oracle/evidence/policy 回归通过。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：coverage_matrix_cases.json 从 120 扩展到 300 个匿名北京合成样本，minCaseCount=300；使用 lunar-python EightChar/Yun 生成四柱/起运期望值；`python3 -m json.tool` PASS；`.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py` -> 7 passed in 28.91s。 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-00.01, TP-00.02 | No | Done | 2026-06-15：裸 pytest 因系统 Python 缺 lunar_python 失败，已将任务树 pytest 命令统一改为 `.venv/bin/python -m pytest`；`.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py` -> 10 passed in 70.39s。 | 无 | 无 |
| TP-04.03 | TP-04 | 2 | TP-00.01, TP-00.02, TP-04.01, TP-04.02 | No | Done | 2026-06-15：`.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_golden_coverage_matrix.py` -> 41 passed in 90.53s。 | 无 | 无 |
| TP-05 | ROOT | 1 | TP-04.01, TP-04.02, TP-04.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-05.02 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.03 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.04 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-05.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-05.05 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-05.02, TP-05.03, TP-05.04 | No | Not Started | 待回填 | 无 | 无 |
| TP-06 | ROOT | 1 | TP-03.01, TP-03.02, TP-03.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-06.01 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-06.02 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-06.03 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-06.04 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-06.01, TP-06.02, TP-06.03 | No | Blocked | 待回填 | 缺少真实公网生产 HTTPS URL、TLS/反向代理配置、生产 CORS allowlist 和真实 FATE_BOT_TOKEN | 提供真实生产 URL 和 Bot token 后运行 production-readiness --api-url <real-url> --require-live-bot |
| TP-07 | ROOT | 1 | TP-04.01, TP-04.02, TP-04.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-07.01 | TP-07 | 2 | TP-04.01, TP-04.02, TP-04.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-07.02 | TP-07 | 2 | TP-04.01, TP-04.02, TP-04.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-07.03 | TP-07 | 2 | TP-04.01, TP-04.02, TP-04.03 | Yes | Not Started | 待回填 | 无 | 无 |
| TP-07.04 | TP-07 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-07.01, TP-07.02, TP-07.03 | No | Not Started | 待回填 | 无 | 无 |
| TP-08 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04 | No | Not Started | 待回填 | 无 | 无 |
| TP-08.01 | TP-08 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04 | No | Not Started | 待回填 | 无 | 无 |
| TP-08.02 | TP-08 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.01 | No | Not Started | 待回填 | 无 | 无 |
| TP-08.03 | TP-08 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05, TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02, TP-07.03, TP-07.04, TP-08.02 | No | Not Started | 待回填 | 无 | 无 |

# Blockers
- 无

# Runtime State
- Active workflow state: 以任务包 JSON 和 Recent Evidence 为准
- Approval state: 未记录即未授权
