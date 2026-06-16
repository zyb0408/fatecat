# 专题 Profile 联合评分

## Scope

- Task: `TP-08.02`
- Objective: 为婚姻、事业、财运、家庭、健康、学业、迁移建立 `score`、`basis`、`scoreBasis`、`evidenceFields`、`lifecycle`。
- Runtime owner: `fate-core`
- Implementation file: `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- Output path: `data.baziBenchmark.topicProfiles`

## Runtime Contract

每个 topic profile 必须包含：

- `basis`: 专题结构依据。
- `score`: capped score，范围 0-100。
- `scoreBasis`: 基础因子 + 联合评分因子。
- `scoreTrace`: raw score、capped score、全部 factor、joint inputs。
- `jointScoreInputs`: 十神族群、主格局、用神候选、岁运触发类型、动态层级。
- `evidenceFields`: 必须包含 `baziBenchmark.yongShenDecision` 和 `baziBenchmark.fortuneTriggerMatrix`。
- `lifecycle`: 当前必须为 `beta`。
- `productionGate`: 当前必须为 `blocked`，进入 production 前必须有 topic golden、MingLi 分类回归、policy regression 和报告边界验收。
- `riskBoundary`: 每个专题必须说明不能替代现实专业决策。

## Verification

| Check | Result |
| --- | --- |
| `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py` | PASS |
| `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | `61 passed in 64.99s` |

## Gate

- PASS: 专题 profile 不再只是 alias 或自然语言拼接。
- PASS: topic profile 联合消费十神、格局、用神决策和岁运触发矩阵。
- PASS: 所有 topic profile 保持 `lifecycle=beta`。
- PASS: `productionGate.status=blocked`，production 升级前必须补 golden 与 policy regression。
