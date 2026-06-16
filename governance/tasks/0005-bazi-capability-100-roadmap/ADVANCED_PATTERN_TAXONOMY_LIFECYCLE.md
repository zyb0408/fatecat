# TP-05.01 Advanced Pattern Taxonomy Lifecycle Evidence

## Result

PASS.

高级格局 taxonomy 已进入 `contracts/fate/rule_depth_registry.json` 的 `bazi.depth.pattern.regular_vs_special.patternMatrix`。

## Verified Scope

- 覆盖类目：正格、变格、从格、假从、专旺、化气。
- 每个类目具备：
  - `appliesWhen`
  - `doesNotApplyWhen`
  - `riskBoundary`
  - `lifecycle`
  - `lifecycleGate`
- 生命周期口径：
  - 正格：`production_guarded`
  - 变格：`beta`
  - 从格、假从、专旺、化气：`beta_hitl`

## Evidence

- `contracts/fate/rule_depth_registry.json`
- `tests/regression/test_bazi_ziwei_rule_depth.py`

## Commands

```bash
rg '从格|假从|专旺|化气|lifecycle' contracts/fate domains/fate-analysis -n
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
.venv/bin/python -m ruff format --check tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `31 passed in 61.78s`
- `ruff format --check`: `1 file already formatted`

## Gate

PASS: 每类高级格局已有 `appliesWhen` / `doesNotApplyWhen` / lifecycle。

## Remaining Work

- `TP-05.02` 继续补高级格局正例、反例、边界例 golden。
- `TP-05.03` 才允许推进 guarded advanced-pattern evaluator。

## Guardrail

当前只是 taxonomy/lifecycle 合同完成。除正格的 guarded 解释外，高级格局不得被报告层强断为 production 结论。
