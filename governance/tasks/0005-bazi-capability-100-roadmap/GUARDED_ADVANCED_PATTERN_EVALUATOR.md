# TP-05.03 Guarded Advanced Pattern Evaluator Evidence

## Result

PASS.

高级格局候选 evaluator 已从 `calculate_pure_analysis.py` 迁入 `fate_core.usecases.evaluators.advanced_pattern`。

## Implementation

- 新增 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/advanced_pattern.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/__init__.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/AGENTS.md`

## Verified Scope

- `calculate_pure_analysis.py` 只编排 `_build_special_pattern_candidates(...)`，不再持有本地实现。
- 高级格局仍输出 candidate / guarded / not_supported，不满足条件时不 production 强断。
- 高级格局正反边界继续由 `advancedPatternGoldenMatrix` 锁定。

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- rule-depth + API: `66 passed in 65.35s`
- format gate: `12 files already formatted`

## Gate

PASS: 不满足条件时不得 production 强断；外部 API schema 未变。

## Guardrail

高级格局仍处于 guarded/beta/HITL 路径，不能因为 evaluator 已迁出就宣称专业断法 100%。
