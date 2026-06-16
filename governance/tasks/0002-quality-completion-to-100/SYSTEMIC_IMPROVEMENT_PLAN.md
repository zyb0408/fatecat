# Systemic Improvement Plan

日期：2026-06-16

## Objective

把 FateCat 从“本地可用、局部生产候选”推进到按六个质量标准可审计的稳定状态：

- 满足约束
- 可解释
- 可测试
- 可维护
- 处理特殊情况
- 复用建立在理解上

本计划是 `0002-quality-completion-to-100` 的 v2 执行覆盖层。它不删除旧任务树证据；后续若要进入执行，应把这里的 `TP-09` 到 `TP-15` 编译进正式 `TREE_SPEC.json` / `TASK_PACKAGE_SET.json`，再由 `auto-tasks` 生成执行波次。

## Current Evidence

- `bash scripts/local-ci.sh --profile quick`：PASS，证据目录 `/tmp/fatecat-local-ci-20260616000719`，focused regression `47 passed in 7.40s`。
- 命理/能力专项：`.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_mingli_bench_gate.py tests/regression/test_capability_protocol.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py -q` -> `44 passed, 1 skipped in 89.30s`。
- `bash scripts/vendor-health.sh`：`vendor health ok: required=5 optionalFutureFeatures=12 hashed=17 licenseAuditRequired=5`。
- `production-readiness.sh --skip-bootstrap`：静态生产配置 PASS；live API 和 live Bot 因缺真实 URL/token 保持 SKIP。
- `scan_principle_gates.py --repo . --git-mode working --strict`：返回 `BLOCK`，42 findings。多数来自 archive/history 文本，但 active 兼容入口、大文件边界和原则 gate 仍需治理。
- Wave 1：`WAVE1_EXECUTION.md` 已固化工作树交付切分、HITL 边界、rule/risk 测试、principle gate 分流结论和 vendor health 证据；`TP-12.01` 仍为 BLOCK。
- Wave 2：`WAVE2_EXECUTION.md` 已固化 API/协议、规则 registry、compatibility burn-down、provider/adapter、reference/oracle 隔离证据；active-only principle gate 已修到 `PASS / finding_count=0`。
- Wave 3：`WAVE3_EXECUTION.md` 已固化 Web/branding/API、calendar/oracle/golden、operability 和 full 300+ golden release gate 证据；full golden 通过但耗时 `36m51s`。
- Wave 4：`WAVE4_EXECUTION.md` 已固化 MingLi prediction eval、local-ci all、big-file line-count map 和 Bot outbox 证据；大文件治理和 MingLi accuracy 仍为 WARN。
- Wave 5：`FINAL_REVIEW.md` 与 `CLOSEOUT.md` 已固化最终六维审查；active local BLOCK=0，剩余状态为 WARN/HITL。

## Target End State

系统最终状态不是“文档宣称 100%”，而是：

- 六个质量标准均有代码、测试、命令、运行证据或明确 HITL 阻塞。
- 本地独立部署单实例可用，不依赖 GitHub Acceptance。
- 外部公网 live 验收只在真实 HTTPS URL、TLS/反代、生产 CORS 和真实 Bot token 提供后声明通过。
- 命理报告每个核心判断都能回指 `ruleId`、source、risk boundary 或明确标为 evidence seed。
- 长期维护不再把新职责塞进 `main.py`、`bot.py`、`report_generator.py`、`calculate_pure_analysis.py`、`bazi_calculator.py`。
- reference/oracle/vendor 依赖的 license、usage role、productionUseAllowed 边界可由 `vendor-health` 和测试证明。

## Real Constraints

- 当前目标是用户可独立部署，不是托管平台级高并发公共服务。
- 不跑 GitHub Acceptance；本轮证据来自本地 CI/CD、pytest、Docker/container smoke、production-readiness 静态门禁。
- 真实公网 API / Bot live 验收需要用户或部署环境提供真实 URL 和 token。
- 无 license 或 reference-only 的资料不能扩散成生产依赖。
- 命理能力不得输出确定性人生、医疗、财务、法律替代建议。

## Inertia Constraints

- 旧 `legacy` / `compat` / `wrapper` 文本不能决定目标结构。
- 旧任务树的七维口径不能阻止本轮按六个质量标准重新编排。
- 已有大文件不能继续作为新增职责入口。
- `governance/archive` 历史材料只能作为历史证据，不能被原则扫描误判为 active blocker。

## Kill List

- 无真实端点的能力声明。
- 吞异常后假绿的测试。
- 未绑定移除条件的兼容入口。
- 无 owner 的临时 wrapper / shim。
- 只跑 stats、不验证 FateCat 输出的 benchmark 口径。
- 无 source / ruleId / riskBoundary 的专业命理文案。

## Rejected Short-Term Patches

- 不通过简单改文案把 WARN 伪装成 PASS。
- 不把 `scan_principle_gates.py` 直接关掉；应区分 archive false positive 与 active finding。
- 不把全量 300 golden matrix 强塞进每次 quick CI；它应作为 release/deep gate。
- 不用 Redis/WAF/分布式队列替代当前自托管目标，除非进入多副本托管场景。

## Systemic Task Tree

```text
ROOT
├─ TP-09 满足约束闭环
│  ├─ TP-09.01 工作树交付切分
│  ├─ TP-09.02 外部 HITL 边界固化
│  └─ TP-09.03 API/协议约束回归
├─ TP-10 可解释闭环
│  ├─ TP-10.01 ruleId/source/riskBoundary 孤儿审计
│  ├─ TP-10.02 高级八字规则证据矩阵
│  └─ TP-10.03 Markdown/Web/Bot 输出可追溯性
├─ TP-11 可测试闭环
│  ├─ TP-11.01 300+ golden release gate
│  ├─ TP-11.02 MingLi-Bench 从 evaluator smoke 升级为 FateCat prediction eval
│  └─ TP-11.03 local-ci profile 与证据目录固化
├─ TP-12 可维护闭环
│  ├─ TP-12.01 principle gate active/archive 分流
│  ├─ TP-12.02 大文件职责切片
│  └─ TP-12.03 compatibility burn-down
├─ TP-13 特殊情况闭环
│  ├─ TP-13.01 时间/时区/节气/早晚子时边界矩阵
│  ├─ TP-13.02 计算背压与 timeout ceiling 验证
│  └─ TP-13.03 Bot outbox/live 恢复路径
├─ TP-14 复用理解闭环
│  ├─ TP-14.01 vendor license 与 usageRole 门禁
│  ├─ TP-14.02 provider/adapter 合同审计
│  └─ TP-14.03 reference-only/oracle-only 隔离验证
└─ TP-15 最终六维审查与 closeout
   ├─ TP-15.01 六维 auto-review
   ├─ TP-15.02 处理 BLOCK/WARN
   └─ TP-15.03 closeout 与交付证据
```

## Task Packages

| Node | Priority | Objective | Depends On | Verify | Gate |
| --- | --- | --- | --- | --- | --- |
| TP-09.01 | P0 | 把当前大工作树按可审查主题切分为交付单元 | - | `git status --short && git diff --stat` | 每个交付单元有范围、证据、回滚点；不混提交 |
| TP-09.02 | P0 | 固化 live API/Bot HITL 与本地自托管 PASS 的边界 | - | `rg 'HITL|--require-live-bot|--api-url|SKIP' REVIEW.md references scripts governance/tasks -n` | 缺真实 URL/token 时不宣称公网通过 |
| TP-09.03 | P0 | 确认 4xx/5xx/503/metrics/security headers 契约 | TP-09.02 | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py -q` | API 协议失败不返回 HTTP 200 |
| TP-10.01 | P0 | 扫描 ruleId/source/riskBoundary 是否可回指 | - | `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | 无孤儿 ruleId；风险边界齐全 |
| TP-10.02 | P0 | 为高级格局、合化、用神、岁运建立 evidence matrix | TP-10.01 | `python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null` | 每条新增专业规则有 source、appliesWhen、doesNotApplyWhen、riskBoundary |
| TP-10.03 | P1 | 确认 Markdown/Web/Bot 输出保留必要证据，不泄露隐私 | TP-10.01 | `.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_branding_support.py tests/regression/test_api_contracts.py -q` | 输出可追溯且不暴露非北京地点 |
| TP-11.01 | P0 | 把全量 300+ golden 作为 release/deep gate 固化 | TP-10.01 | `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q` | 全量矩阵通过或失败样本进入 DEBUG.md |
| TP-11.02 | P0 | MingLi-Bench 连接 FateCat 真实预测输出，而非只测 evaluator | TP-10.02 | `bash scripts/run-mingli-bench.sh --predictions-file <generated> --output-json <out>` | predictions 由 FateCat 生成，报告 accuracy/coverage/unknowns |
| TP-11.03 | P1 | local-ci quick/all/container/public-service 证据目录固定 | TP-09.03 | `bash scripts/local-ci.sh --profile all` | all profile PASS；Docker 缺失时记录环境 blocker |
| TP-12.01 | P0 | 把 principle scan 分成 active gate 与 archive informational | - | `python3 /home/lenovo/.codex/skills/auto-review/scripts/scan_principle_gates.py --repo . --git-mode working --strict` | active finding 无 BLOCK；archive finding 不阻塞运行时 |
| TP-12.02 | P0 | 大文件按职责切片，禁止继续新增职责 | TP-12.01 | `find domains/experience-delivery/services/fatecat-delivery/src domains/fate-analysis/services/fate-core/src -name '*.py' -print0 \| xargs -0 wc -l \| sort -nr \| head -25` | 新逻辑进入明确子模块；API 输出不漂移 |
| TP-12.03 | P1 | 审计 remaining legacy/compat/shim/wrapper | TP-12.01 | `rg 'legacy|compat|shim|wrapper|fallback' domains contracts catalog governance -n` | 保留项有真实 contract、owner、移除条件；无契约项进 kill list |
| TP-13.01 | P0 | 扩充时间边界：时区、DST、节气、早晚子时、真太阳时 | TP-11.01 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py -q` | 边界样本有 expected/failureExplanation |
| TP-13.02 | P1 | 验证 calculation slots、timeout、rate limit 的 ceiling | TP-09.03 | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py -q` | 503/504/429 可观测且 runbook 有升级路径 |
| TP-13.03 | P1 | 验证 Bot outbox 幂等、ACK、live 恢复边界 | TP-13.02 | `.venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests/test_bot_send_queue.py -q` | 本地 outbox 可恢复；live Bot 仍需真实 token |
| TP-14.01 | P0 | vendor license、usageRole、productionUseAllowed 门禁 | - | `bash scripts/vendor-health.sh` | reference-only/oracle-only 不进入生产依赖 |
| TP-14.02 | P1 | provider/adapter 合同审计，复用成熟库而不是重造轮子 | TP-14.01 | `.venv/bin/python -m pytest tests/regression/test_capability_protocol.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py -q` | provider 状态和 capability registry 一致 |
| TP-14.03 | P1 | 隔离 reference-only/oracle-only 快照 | TP-14.01 | `rg 'productionUseAllowed|reference_only|oracle_only|licenseStatus' tools/reference-repos/vendor_sources.json -n` | 无 license 快照只作参考/评测 |
| TP-15.01 | P0 | 按六维重新执行 auto-review | TP-09.03, TP-10.03, TP-11.03, TP-12.03, TP-13.03, TP-14.03 | 审查报告 | 六维 PASS/WARN/BLOCK 有证据 |
| TP-15.02 | P0 | 处理最终 BLOCK 和影响 100% 的 WARN | TP-15.01 | 复跑对应最小命令 | BLOCK=0；WARN 有 owner 和升级触发 |
| TP-15.03 | P0 | 生成 closeout | TP-15.02 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-quality-completion-to-100 --phase closeout` | TODO 完成或 HITL Blocked 明确；不含伪证 |

## Execution Waves

- Wave 1：TP-09.01、TP-09.02、TP-10.01、TP-12.01、TP-14.01
- Wave 2：TP-09.03、TP-10.02、TP-12.03、TP-14.02、TP-14.03
- Wave 3：TP-10.03、TP-11.01、TP-13.01、TP-13.02
- Wave 4：TP-11.02、TP-11.03、TP-12.02、TP-13.03
- Wave 5：TP-15.01、TP-15.02、TP-15.03

## Ponytail Contract

- Existence check：本计划存在是因为旧 0002 任务树与当前六维质量审计不完全同构；直接执行旧树会遗漏 principle scan、工作树收敛、MingLi prediction eval 等新 findings。
- Selected ladder rung：项目原生任务文档补充，不新增新工具、不新增新依赖。
- Skipped scope：不在本文件直接改源码、不直接重编 `TREE_SPEC.json`、不制造新的 public service 高并发平台需求。
- Ceiling / upgrade path：若用户确认进入执行，应把本计划编译为正式 `TASK_PACKAGE_SET.json` 并生成 execution wave packet。
- Do-not-simplify：不得删除安全/隐私/错误处理/证据边界来追求表面 100%。
- Minimal runnable check：`validate_task_docs.py --phase decompose` 和对应任务包 Verify 命令。
- Complexity review owner：`auto-review` with `ponytail-complexity`。

## Future-Optimal Contract

- Target end state：六维质量标准成为任务和审查的单一质量语言。
- Real constraints：本地自托管、真实 live HITL、license、命理风险边界、现有公开 API。
- Inertia constraints：旧七维任务树、legacy 文本、大文件惯性、历史 archive。
- Wrong concept / wrong boundary：把“GitHub/公网/高并发平台”混入当前自托管目标；把 evaluator smoke 当 FateCat 样本外能力。
- Proof point：Wave 1 完成后 principle scan active finding 与 HITL 边界清楚；Wave 3/4 完成后 full golden 与真实 prediction eval 可复现。
- Falsifier：如果 full golden 或真实 prediction eval 证明核心规则不可稳定解释，则不得声明命理专业 100%。
- Migration slice：先补计划覆盖层，再经用户确认编译到正式任务树。
- Rejected short-term patches：不改数字、不伪造 live 验收、不隐藏 BLOCK。

## Wave 1 Result

执行记录：`WAVE1_EXECUTION.md`。

| Node | Result |
| --- | --- |
| TP-09.01 | Done for split design：已将当前工作树切成 API/运行防护、命理内核、Web/Bot/报告、治理、供应链、测试数据六个交付单元。 |
| TP-09.02 | PASS：真实公网 API/Bot live 验收边界已在 REVIEW、scripts、references 中明确。 |
| TP-10.01 | PASS：policy/rule depth 专项 `35 passed in 62.49s`。 |
| TP-12.01 | BLOCK：principle gate 仍返回 `42 findings`，需要 active/archive 分流和 active finding 修复。 |
| TP-14.01 | PASS：vendor health OK。 |

## Wave 2 Result

执行记录：`WAVE2_EXECUTION.md`。

| Node | Result |
| --- | --- |
| TP-09.03 | PASS：API contract `29 passed in 3.94s`。 |
| TP-10.02 | PASS：`rule_depth_registry.json` 可解析。 |
| TP-12.01 | PASS：active-only principle gate `finding_count=0`；archive finding 降为 informational。 |
| TP-12.03 | PASS/WARN：compatibility 扫描已分类，retained runtime compatibility 继续进入 burn-down。 |
| TP-14.02 | PASS：capability/provider/service contract `13 passed in 0.21s`。 |
| TP-14.03 | PASS：vendor manifest 明确 production/reference/oracle/license 边界。 |

## Wave 3 Result

执行记录：`WAVE3_EXECUTION.md`。

| Node | Result |
| --- | --- |
| TP-10.03 | PASS：Web/branding/API `47 passed in 7.38s`。 |
| TP-11.01 | PASS/WARN：full 300+ golden `9 passed in 2211.71s`，可作为 release/deep gate，不能进入 quick。 |
| TP-13.01 | PASS：calendar/solar/golden representative `18 passed, 1 skipped in 97.87s`。 |
| TP-13.02 | PASS：API/operability `30 passed in 3.89s`。 |

## Wave 4 Result

执行记录：`WAVE4_EXECUTION.md`。

| Node | Result |
| --- | --- |
| TP-11.02 | PASS/WARN：FateCat-generated predictions 进入 MingLi evaluator；answered `2/2`，accuracy `0%`。 |
| TP-11.03 | PASS：local-ci all 通过，证据目录 `/tmp/fatecat-local-ci-20260616012307`。 |
| TP-12.02 | WARN：大文件 line-count map 已生成，但核心文件仍有 1000+ 行级维护债。 |
| TP-13.03 | PASS/HITL：Bot outbox `2 passed`；live Bot 仍需真实 token。 |

## Wave 5 Result

执行记录：`FINAL_REVIEW.md` 与 `CLOSEOUT.md`。

| Node | Result |
| --- | --- |
| TP-15.01 | PASS/WARN：六维审查完成，active local BLOCK=0。 |
| TP-15.02 | PASS/WARN/HITL：本地 BLOCK 已处理；remaining WARN/HITL 有 owner 和下一步。 |
| TP-15.03 | PASS/WARN/HITL：closeout 生成；不把 remaining WARN/HITL 伪造成无条件 100%。 |

## Next Action

当前建议：

1. 优化 full golden release gate 的 case-level timing 与并行能力。
2. 建设 MingLi 专题推理器，替代 deterministic baseline。
3. 继续拆大文件。
4. 等真实公网 URL/token 后跑 live gate。

本轮 v2 任务树已处理完毕；最终状态是 `Closed with WARN/HITL`，不是无条件 100%。
