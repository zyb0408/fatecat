# TP-07.02 Yongshen Conflict Ranking Evaluator Evidence

## Result

PASS.

用神策略排序 evaluator 已从 `calculate_pure_analysis.py` 迁入 `fate_core.usecases.evaluators.yongshen`。

## Implementation

- 新增 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/yongshen.py`
- 迁出：
  - `five_element_spread`
  - `temperature_band`
  - `build_yongshen_decision`
- 保持原 `temperatureScore` 语义，不改报告边界。

## Verified Scope

- 输出 `ranking`、`selectedCandidates`、`conflicts`、`decisionTrace`。
- 保持 `noAbsoluteConclusion = True`。
- 保持调候、扶抑、通关、病药并列策略，不输出唯一绝对结论。

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- rule-depth + API: `66 passed in 65.35s`
- format gate: `12 files already formatted`

## Gate

PASS: 输出 ranking/conflicts，不输出唯一绝对结论。

## Guardrail

格局用神已在合同中存在，但 runtime 仍只排序当前四类策略；后续若纳入格局用神，必须先扩 runtime scoreBasis 和 golden。
