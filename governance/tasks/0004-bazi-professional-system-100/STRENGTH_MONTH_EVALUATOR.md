# Strength And Month Command Evaluator

任务节点：`TP-04.01`

## 结论

强弱与月令 evaluator 切片已进入端到端链路。`baziBenchmark.strengthScore` 现在保留 `score`、`basis`、`sourceRuleId`、`conflicts`、`evidenceFields` 和 `riskBoundary`；`baziRuleDepth.appliedRules` 同步消费这些字段。

## 实现文件

- `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_bazi_ziwei_benchmark_hardening.py`

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
```

Result:

```text
39 passed, 1 skipped in 88.40s
```

## Gate 判定

- `strength 输出包含 score、basis、sourceRuleId、conflicts`：`PASS`
- `新增强弱字段进入 rule-depth 证据链`：`PASS`
- `基础排盘 golden coverage 未回归`：`PASS`

## 边界

本节点不改变底层四柱、真太阳时、五行分数或 strongScore 算法，只把已有计算结果整理为可审计 evaluator 输出。后续如调整强弱算法，必须重新进入 `TP-02.03` 基础排盘回归和 `TP-04.01` evaluator gate。
