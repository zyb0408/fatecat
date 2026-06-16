# 专题风险边界

## Scope

- Task: `TP-08.03`
- Objective: 高风险专题不输出现实处方、保证、恐吓或法律金融医疗建议。
- Runtime owner: `fate-core`
- Implementation file: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- Test files:
  - `tests/regression/test_fate_policy_assets.py`
  - `tests/regression/test_bazi_statement_golden.py`
  - `tests/regression/test_api_contracts.py`
  - `tests/regression/test_bazi_ziwei_rule_depth.py`

## Runtime Guard

每个 `topicProfiles[]` 现在必须包含：

- `lifecycle=beta`
- `productionGate.status=blocked`
- `riskPolicy.riskLevel=high_topic_boundary`
- `riskPolicy.disclaimerRequired=true`
- `riskPolicy.forbiddenClaims` 至少包含 `deterministic_future`、`professional_replacement`、`guarantee`、`fear_claim`
- `riskBoundary`，且不得输出医疗、金融、法律、心理替代建议或保证式话术

## Verification

| Check | Result |
| --- | --- |
| `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q` | `19 passed in 56.93s` |
| `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | `61 passed in 68.73s` |

## Gate

- PASS: 高风险专题不输出现实处方。
- PASS: 不输出保证、恐吓或确定未来。
- PASS: 不输出法律、金融、医疗、心理替代建议。
- PASS: 专题 profile 必须保持 beta，production 升级被 gate 阻断。
