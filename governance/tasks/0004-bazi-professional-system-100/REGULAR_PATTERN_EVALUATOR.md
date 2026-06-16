# Regular Pattern Evaluator

任务节点：`TP-04.03`

## 结论

常规格局 evaluator 切片已进入端到端链路。`baziBenchmark.patternRegistry.regularPatternCandidates` 现在保留正格候选、条件链、破格条件、`uncertainty`、`sourceRuleId`、`evidenceFields` 和 `riskBoundary`。证据不足时只输出 `uncertain`，不把候选写成定格。

## 实现文件

- `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_api_contracts.py`

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
```

Result:

```text
35 passed in 117.98s
```

Additional API check:

```text
31 passed in 5.18s
```

## Gate 判定

- `无法稳定判定时输出 uncertainty`：`PASS`
- `常规格局候选具备 conditions 和 breaksWhen`：`PASS`
- `statement golden 未被新增结构破坏`：`PASS`

## 边界

本节点不调整历史 `geju.main` 口径，不把正格候选替换成最终定格。后续高级格局、合化、用神任务必须消费候选结构，而不是重新解析自然语言格局文本。
