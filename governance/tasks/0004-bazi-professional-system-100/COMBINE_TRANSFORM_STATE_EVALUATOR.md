# Combine Transform State Evaluator

任务节点：`TP-06.02`

## 结论

合化状态链 evaluator 已进入 core 端到端链路。`baziBenchmark.combineTransformMatrix` 同时暴露候选条件链、`stateCatalog`、`stateContracts`、状态风险边界和反证条件；API contract 已锁定这些字段。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
```

Result:

```text
61 passed in 64.93s
```

## Gate 判定

- `每个 transform state 都有证据和反证条件`：`PASS`
- `stateCatalog 与 stateContracts 一致`：`PASS`
- `缺少成化证据时不宣称已成化`：`PASS`

## 边界

本节点锁定状态链输出，不把 transform candidate 自动升级为 transform success。合化反例矩阵由 `TP-06.03` 承接。
