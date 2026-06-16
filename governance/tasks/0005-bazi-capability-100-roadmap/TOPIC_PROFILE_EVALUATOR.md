# TP-08.02 Topic Profile Evaluator Evidence

## Result

PASS.

P0 专题 profile evaluator 已从 `calculate_pure_analysis.py` 迁入 `fate_core.usecases.evaluators.topic_profile`。

## Implementation

- 新增 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/topic_profile.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/__init__.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- 更新 `domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/AGENTS.md`

## Verified Scope

覆盖专题：

- 事业
- 财运
- 婚姻
- 健康
- 学业
- 迁移
- 家庭

每个 profile 保持：

- `score`
- `basis`
- `scoreBasis`
- `evidenceFields`
- `riskBoundary`
- `status = evidence_seed`
- `lifecycle = beta`
- `productionGate.status = blocked`

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
.venv/bin/python -m ruff check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators tests/regression/test_bazi_ziwei_rule_depth.py
```

Observed:

- API/rule-depth/statement: `71 passed in 121.75s`
- ruff check: `All checks passed!`

## Gate

PASS: 专题 profile 输出不是 benchmark 答案匹配；所有专题仍保留 beta/blocked 和报告风险边界。

## Guardrail

专题 profile 只能作为结构化证据种子，不得替代现实职业、投资、医疗、法律、心理或婚姻决策。
