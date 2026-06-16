# TP-08.01 Fortune Trigger Matrix Evidence

## Result

PASS.

岁运触发矩阵已由 `fate_core.usecases.evaluators.fortune.build_fortune_trigger_matrix` 承载，并由 `contracts/fate/rule_depth_registry.json` 的 `bazi.depth.fortune.trigger_chain.triggerMatrix` 定义。

## Verified Scope

覆盖动态层级：

- `major_stage`：大运阶段
- `annual_trigger`：流年触发
- `monthly_refinement`：流月细化
- `fu_yin`：伏吟
- `fan_yin`：反吟
- `sui_yun_bing_lin`：岁运并临
- `tian_ke_di_chong`：天克地冲

矩阵口径：

- 原局优先。
- 大运定阶段。
- 流年定触发。
- 流月只细化窗口。
- 动态触发只作趋势证据，不输出确定未来。

## Evidence

- `contracts/fate/rule_depth_registry.json`
- `contracts/fate/classics_rule_index.json`
- `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/fortune.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`

## Commands

```bash
rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
.venv/bin/python -m ruff check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- rule-depth + API: `66 passed in 65.35s`
- ruff check: `All checks passed!`

## Gate

PASS: 动态触发只作趋势证据，且不覆盖原局结构。

## Guardrail

岁运专题不得输出确定未来、恐吓表述或现实高风险决策建议。
