# 用神决策 Evaluator

## Scope

- Task: `TP-07.02`
- Objective: 输出 `scoredStrategies`、`ranking`、`conflicts`、`selectedCandidates`、`riskBoundary`。
- Runtime owner: `fate-core`
- Implementation file: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- Output path: `data.baziBenchmark.yongShenDecision`

## Decision Contract

| Field | Meaning | Gate |
| --- | --- | --- |
| `scoredStrategies` | 调候、扶抑、通关、病药的证据评分项 | 每项必须有 `basis`、`score`、`scoreBasis`、`doesNotApplyWhen` |
| `ranking` | 按证据完整度降序生成的策略排名 | rank 连续，score 降序，不代表绝对结论 |
| `selectedCandidates` | 最高分附近策略和至少一个并列审查策略 | 必须保留 `parallel_review`，避免单一用神覆盖全部策略 |
| `conflicts` | 调候/扶抑、通关/病药等冲突和边界 | 每项必须有 `type`、`explanation`、`counterEvidence` |
| `decisionTrace` | 评分、排序、候选选择、冲突附加的步骤链 | step 必须可追溯到输出字段 |
| `noAbsoluteConclusion` | 禁止把评分结果写成唯一绝对用神结论 | 必须为 `true` |
| `riskBoundary` | 文化解释边界 | 不承诺现实事件结果 |

## Conflict Policy

- 调候解释季节气候偏性，不覆盖扶抑。
- 扶抑解释日主强弱，不覆盖调候、通关、病药。
- 通关只解释冲突缓冲，不替代调候或扶抑主策略。
- 病药只解释偏枯和结构病处，不输出医疗、金融、法律或生活处方。
- 排名只表达证据完整度，报告必须保留并列策略和反证条件。

## Verification

| Check | Result |
| --- | --- |
| `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q` | `61 passed in 75.53s` |

## Gate

- PASS: 冲突裁决可解释。
- PASS: `selectedCandidates` 保留并列审查策略。
- PASS: `noAbsoluteConclusion=true`，不输出唯一绝对结论。
- PASS: API contract 和 rule-depth regression 都覆盖真实端到端输出。
