# Ten God Structure Evaluator

任务节点：`TP-04.02`

## 结论

十神结构 evaluator 切片已进入端到端链路。`baziBenchmark.tenGodStructure` 现在保留 `basisEvidence`、`dominant`、`families`、`sourceRuleId`、`evidenceFields` 和 `riskBoundary`；十神统计不再只是孤立 counts，而能回指柱位、透干、藏干和 evidence field。

## 实现文件

- `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_bazi_ziwei_benchmark_hardening.py`

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
```

Result:

```text
61 passed in 65.23s
```

## Gate 判定

- `十神解释必须引用盘面证据`：`PASS`
- `十神结构不输出孤立断语`：`PASS`
- `API contract 未被新增字段破坏`：`PASS`

## 边界

本节点只增加结构证据，不把十神 counts 升级为确定性性格、事件或人生判断。后续专题 profile 可以消费 `families` 与 `basisEvidence`，但必须继续保留风险边界。
