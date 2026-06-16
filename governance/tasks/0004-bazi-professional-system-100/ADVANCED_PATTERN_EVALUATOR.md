# Advanced Pattern Evaluator

任务节点：`TP-05.03`

## 结论

高级格局 evaluator 已进入 core 端到端链路，输出位于 `baziBenchmark.patternRegistry.specialPatternCandidates`，不依赖 delivery 层。候选项包含条件链、反证、生命周期门禁和风险边界，schema 由 rule-depth 与 API contract 共同锁定。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
```

Result:

```text
61 passed in 64.93s
```

## Gate 判定

- `evaluator 不依赖 delivery`：`PASS`
- `输出 schema 稳定`：`PASS`
- `高级格局未越权升 production`：`PASS`

## 边界

当前高级格局仍是候选 evaluator，不是最终强断层。production 化必须由后续 golden、policy 和报告门禁共同批准。
