# Advanced Pattern Golden

任务节点：`TP-05.02`

## 结论

高级格局正反例 golden gate 通过。`domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` 当前覆盖 8 个 rule-depth cases，锁定从格、化气、专旺、假从、从杀、从财候选成熟度；coverage matrix 继续覆盖特殊格局保护标签。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
```

Result:

```text
39 passed, 1 skipped in 89.54s
```

## Gate 判定

- `无 golden 的高级格局不能升 production`：`PASS`
- `specialPatternCandidates.lifecycle 仍为 beta`：`PASS`
- `coverage matrix 未被新增字段破坏`：`PASS`

## 边界

当前 golden 只锁定候选状态、分数和条件链，不证明专业命中率 100%。后续如要把具体高级格局升 production，必须新增对应正反例、失败解释和报告 policy regression。
