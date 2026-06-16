# Wave 1 Execution Evidence

日期：2026-06-16

## Scope

Wave 1 覆盖 `SYSTEMIC_IMPROVEMENT_PLAN.md` 中的首批 P0/P1 叶子：

- `TP-09.01` 工作树交付切分
- `TP-09.02` 外部 HITL 边界固化
- `TP-10.01` ruleId/source/riskBoundary 孤儿审计
- `TP-12.01` principle gate active/archive 分流
- `TP-14.01` vendor license 与 usageRole 门禁

本轮只写任务证据，不改业务代码。目标是先把当前真实状态、可交付切片和阻塞点固定下来，防止后续把未验证事项说成已完成。

## Command Evidence

| Node | Command | Result |
| --- | --- | --- |
| TP-09.01 | `git status --short` | PASS：工作树存在大批已修改/新增/迁移文件，需要按主题切分交付。 |
| TP-09.01 | `git diff --stat` | PASS：65 个已跟踪文件变更，约 `1752 insertions / 3703 deletions`，另有新增源码、测试、治理文件。 |
| TP-09.02 | `rg 'HITL|--require-live-bot|--api-url|SKIP|live Bot|真实' REVIEW.md references scripts governance/tasks -n` | PASS：`REVIEW.md`、`production-readiness.sh`、`local-ci.sh`、`references/commands.md`、`references/live-bot-verification.md` 均声明真实 URL/token 缺失时保持 HITL/SKIP。 |
| TP-10.01 | `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | PASS：`35 passed in 62.49s`。 |
| TP-12.01 | `python3 /home/lenovo/.codex/skills/auto-review/scripts/scan_principle_gates.py --repo . --git-mode working --strict` | BLOCK：`42 findings`；需要 active/archive 分流和 active finding 修复。 |
| TP-14.01 | `bash scripts/vendor-health.sh` | PASS：`vendor health ok: required=5 optionalFutureFeatures=12 hashed=17 licenseAuditRequired=5`。 |

## TP-09.01 Worktree Delivery Split

当前工作树不适合一次性混合提交。建议按下面交付单元拆分，且每个单元独立跑对应 gate：

| Unit | Scope | Representative Files | Required Gate | Rollback Boundary |
| --- | --- | --- | --- | --- |
| A | API/运行防护与生产自检 | `src/main.py`, `src/models.py`, `src/rate_limiter.py`, `scripts/production-readiness.sh`, `tests/regression/test_api_contracts.py` | `pytest tests/regression/test_api_contracts.py`; `production-readiness.sh --skip-bootstrap` | 回滚 API guardrail 与 readiness 变更，不触碰命理内核。 |
| B | 八字内核迁移与 fate-core 边界 | `fate_core/kernel/*`, `fate_core/usecases/*`, `src/bazi_calculator.py`, `domains/fate-analysis/services/fate-core/tests/*` | `pytest domains/fate-analysis/services/fate-core/tests/test_service_contract.py`; golden/oracle regression | 回滚 kernel/usecase 迁移，不触碰 Web/Bot 交付层。 |
| C | Web/Bot/报告交付层 | `src/web_ui.py`, `src/web_forms.py`, `src/report_generator.py`, `src/report_markdown.py`, `src/bot.py`, `src/bot_logging.py`, delivery tests | Web/Bot/report targeted pytest 和 delivery smoke | 回滚 UI/传输层，不触碰 fate-core。 |
| D | 治理、任务树、迁移账本、审查材料 | `governance/**`, `REVIEW.md`, `DEBUG.md`, `references/**`, `catalog/**` | `validate_task_docs.py`; governance validation; diff check | 回滚治理文档，不触碰运行时代码。 |
| E | 供应链与 reference/oracle 资产 | `tools/reference-repos/**`, `vendor_sources.json`, `contracts/fate/future_features.json` | `bash scripts/vendor-health.sh`; policy asset tests | 回滚 vendor manifest，不触碰生产路径。 |
| F | 回归测试和数据产品 | `tests/regression/*`, `data-products/bazi/golden/*`, delivery tests | 对应 pytest；必要时 full golden release gate | 回滚测试/fixture，不触碰源码。 |

Gate：每个 Unit 必须有独立验证命令和独立回滚边界；不得把治理、运行时、命理内核和 UI 混成一个提交。

## TP-09.02 HITL Boundary

结论：PASS。

证据要点：

- `REVIEW.md` 明确外部托管公网发布仍为 `HITL`，缺真实公网生产 URL 与真实 Telegram Bot token 时不得宣称通过。
- `scripts/production-readiness.sh` 支持 `--api-url` 与 `--require-live-bot`，缺失时对 live API/Bot 输出 SKIP。
- `scripts/local-ci.sh --profile public-service` 是本地静态准入，不等于真实公网 live 验收。
- `references/live-bot-verification.md` 明确真实 Bot 验收必须使用真实 `FATE_BOT_TOKEN`。

Gate：缺真实 URL/token 时只能说本地自托管和静态准入通过，不能说公网 live 生产通过。

## TP-10.01 Evidence Integrity

结论：PASS。

`test_fate_policy_assets.py` 与 `test_bazi_ziwei_rule_depth.py` 已验证 policy assets、rule depth、risk boundary 和命理证据层的基础完整性。本轮没有发现孤儿 ruleId 造成测试失败。

Ceiling：这只证明当前 registry/test 覆盖的规则可追溯；高级格局、合化成败、用神冲突和岁运专题仍要在 `TP-10.02` / `TP-05.*` 继续补齐。

## TP-12.01 Principle Gate Split

结论：WARN/BLOCK。

扫描器当前返回 `BLOCK / 42 findings`。分流结果：

- Archive informational：`governance/archive/**` 和旧 `project-history` 中的兼容/旧任务文本属于历史证据，不应阻塞 active runtime，但扫描器当前仍计入 BLOCK。
- Active documentation finding：`DEBUG.md`、`README.md`、`REVIEW.md`、`catalog/**`、`references/**` 中若提到兼容、临时、未来扩展，需要补 Future-Optimal/Ponytail 证据或改成不触发误判的准确表述。
- Active runtime finding：`src/bot.py`、`src/report_generator.py`、`src/system_optimization.py`、`fate_core/adapters/legacy_bazi.py`、`calculate_pure_analysis.py` 中仍有兼容/legacy/wrapper 入口，需要保留契约、owner、移除条件或继续 burn-down。
- Active ownership-surface warning：capability contracts、registry、rate limiter、rule depth usecase 等新增所有权面需要补存在性理由和验证路径。

最小修复路径：

1. 给 principle gate 增加 active/archive 分流能力，或在运行命令中排除 `governance/archive/**`。
2. 对 active 文档中的兼容/临时/未来扩展口径补齐 target end state、real constraints、inertia constraints、kill list、proof point、falsifier、migration slice。
3. 对 active runtime 兼容入口更新 `governance/migration/compatibility-ledger.md`，无真实契约项进入 burn-down kill list。
4. 复跑 `scan_principle_gates.py --repo . --git-mode working --strict`，直到 active finding 无 BLOCK。

## TP-14.01 Vendor Health

结论：PASS。

`vendor-health.sh` 证明当前 vendor manifest 可解析，required/optionalFutureFeatures/reference/oracle/license audit 边界存在：

- `required=5`
- `optionalFutureFeatures=12`
- `hashed=17`
- `licenseAuditRequired=5`

Gate：reference-only/oracle-only 资料不得自动进入生产依赖；无 license 或 licenseAuditRequired 的资料只能作为参考、评测或治理输入。

## Wave 1 Status

| Node | Status | Evidence | Next |
| --- | --- | --- | --- |
| TP-09.01 | Done for split design | 工作树交付单元 A-F 已定义 | 后续提交必须按 Unit 切分。 |
| TP-09.02 | Done | HITL/SKIP 边界证据存在 | 真实 URL/token 到位后再跑 live gate。 |
| TP-10.01 | Done | `35 passed` | 进入 TP-10.02 evidence matrix。 |
| TP-12.01 | Blocked for final PASS | principle gate `42 findings` | 先修 active/archive 分流和 active findings。 |
| TP-14.01 | Done | vendor health OK | 进入 TP-14.02/TP-14.03。 |

## Next Wave Gate

可以进入 Wave 2，但 `TP-12.01` 不能视为完全关闭。Wave 2 执行时必须优先处理：

- `TP-09.03` API/协议约束回归。
- `TP-10.02` 高级规则 evidence matrix。
- `TP-12.03` compatibility burn-down。
- `TP-14.02` provider/adapter 合同。
- `TP-14.03` reference-only/oracle-only 隔离。

