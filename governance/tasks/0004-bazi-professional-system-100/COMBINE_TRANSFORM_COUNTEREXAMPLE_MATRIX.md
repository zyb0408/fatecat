# Combine Transform Counterexample Matrix

任务节点：`TP-06.03`

## 结论

合化反例矩阵 gate 通过。`rule_depth_cases.json` 的 `evaluatorStateCases.combineTransform` 已覆盖 `transform_candidate`、`transform_success`、`transform_broken` 等状态；失败解释能定位到具体 condition 或 blocker。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
```

Result:

```text
39 passed, 1 skipped in 89.35s
```

## Gate 判定

- `反例失败时能定位到具体 condition`：`PASS`
- `transform_broken 能定位 blocker`：`PASS`
- `coverage matrix 未回归`：`PASS`

## 边界

本节点只锁定状态与反例，不输出成化确定断语。后续用神和岁运专题只能消费状态链证据，不能反向改写合化事实。
