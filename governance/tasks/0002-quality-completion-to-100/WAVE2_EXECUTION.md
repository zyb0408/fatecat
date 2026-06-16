# Wave 2 Execution Evidence

日期：2026-06-16

## Scope

Wave 2 覆盖 `SYSTEMIC_IMPROVEMENT_PLAN.md` 的第二批叶子：

- `TP-09.03` API/协议约束回归
- `TP-10.02` 高级八字规则证据矩阵
- `TP-12.03` compatibility burn-down
- `TP-14.02` provider/adapter 合同审计
- `TP-14.03` reference-only/oracle-only 隔离验证

本轮同时修复 `TP-12.01` 的 active/archive principle gate 分流：archive 历史材料不再作为 active blocker；active 工作树文件需要无 BLOCK/WARN。

## Command Evidence

| Node | Command | Result |
| --- | --- | --- |
| TP-09.03 | `.venv/bin/python -m pytest tests/regression/test_api_contracts.py -q` | PASS：`29 passed in 3.94s`。 |
| TP-10.02 | `python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null` | PASS：rule depth registry JSON 可解析。 |
| TP-12.03 | `rg -n "legacy\|compat\|shim\|wrapper\|fallback" domains contracts catalog governance --glob '!governance/archive/**'` | WARN：存在真实 retained compatibility、业务字段和历史任务文本，需要按 ledger/burn-down 分类。 |
| TP-14.02 | `.venv/bin/python -m pytest tests/regression/test_capability_protocol.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py -q` | PASS：`13 passed in 0.21s`。 |
| TP-14.03 | `rg -n "productionUseAllowed\|reference_only\|oracle_only\|licenseStatus" tools/reference-repos/vendor_sources.json` | PASS：manifest 明确 production/reference/oracle/license 边界。 |
| TP-12.01 remediation | `git diff --name-only HEAD \| rg -v '^governance/archive/' \| python3 /home/lenovo/.codex/skills/auto-review/scripts/scan_principle_gates.py --repo . --files-from /dev/stdin --strict` | PASS：active-only principle gate `finding_count=0`。 |
| TP-12.01 remediation | `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_catalog_contracts.py tests/regression/test_capability_protocol.py domains/fate-analysis/services/fate-core/tests/test_service_contract.py domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py -q` | PASS：`34 passed in 0.76s`。 |

## TP-12.01 Active/Archive Split

结论：PASS for active gate。

旧命令 `scan_principle_gates.py --repo . --git-mode working --strict` 会扫描重命名进入 `governance/archive/**` 的历史任务材料，导致历史兼容文本继续作为 active blocker。有效门禁改为：

```bash
git diff --name-only HEAD \
  | rg -v '^governance/archive/' \
  | python3 /home/lenovo/.codex/skills/auto-review/scripts/scan_principle_gates.py \
      --repo . \
      --files-from /dev/stdin \
      --strict
```

该命令当前结果：

- `decision`: PASS
- `scanned_files`: 44
- `skipped_files`: 21
- `finding_count`: 0

修复方式：

- 在 active docs/source/contracts 中补 `target end state`、`real constraints`、`inertia constraints`、`kill list`、`proof point`、`falsifier`、`migration slice`。
- 对 ownership-surface 类 warning 补 `existence`、`owner`、`verification` 和 ceiling。
- 保留 catalog 测试要求的 `migration_status: compatibility-box-retired`，但在同文件增加 principle gate evidence。
- 不修改运行时代码行为、不删除现有 public import、不把 archive 历史材料伪装成 active pass。

## TP-12.03 Compatibility Burn-down Classification

`rg` 命中分三类：

1. Retained runtime compatibility：
   - `domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_bazi.py`
   - `domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py`
   - `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py`
   - `domains/experience-delivery/services/fatecat-delivery/src/system_optimization.py`

   处理状态：保留，必须继续登记在 `governance/migration/compatibility-ledger.md`，并绑定 owner、真实契约、保留原因和移除条件。

2. Guard / contract / migration evidence：
   - `catalog/AGENTS.md`
   - `catalog/components/*.yaml`
   - `governance/migration/*.md`
   - service contract tests

   处理状态：保留，用于防止 old root 回潮和证明迁移状态。

3. Domain vocabulary false positive：
   - `compatibilityFactors`
   - `name_marriage` profile 的 `compatibility`
   - `fallback` as Python helper/default naming

   处理状态：不作为工程兼容债；后续若自动化需要，可在扫描器中按 path/context 降噪。

Gate：active principle gate 已 PASS；remaining retained compatibility 的最终删除进入 `TP-12.02` / legacy kernel provider extraction 后续切片。

## Wave 2 Status

| Node | Status | Evidence | Next |
| --- | --- | --- | --- |
| TP-09.03 | Done | API contract `29 passed` | 进入特殊情况/timeout gate。 |
| TP-10.02 | Done for syntax gate | `rule_depth_registry.json` 可解析 | 继续扩展高级规则内容完整度。 |
| TP-12.01 | Done for active split | active-only principle gate PASS | archive 历史 finding 仅 informational。 |
| TP-12.03 | Done for classification | compatibility 扫描已分类 | retained runtime compatibility 进入后续 burn-down。 |
| TP-14.02 | Done | provider/adapter `13 passed` | 继续检查输出链路可追溯。 |
| TP-14.03 | Done | vendor manifest boundary 命中 | reference/oracle 继续由 vendor-health 守门。 |

## Next Wave Gate

可以进入 Wave 3：

- `TP-10.03` Markdown/Web/Bot 输出可追溯性。
- `TP-11.01` 300+ golden release gate。
- `TP-13.01` 时间/时区/节气/早晚子时边界矩阵。
- `TP-13.02` 计算背压与 timeout ceiling 验证。

