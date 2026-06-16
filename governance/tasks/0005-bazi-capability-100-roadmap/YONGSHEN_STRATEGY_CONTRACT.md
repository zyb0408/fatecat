# TP-07.01 Yongshen Strategy Contract Evidence

## Result

PASS.

用神策略合同已进入 `contracts/fate/rule_depth_registry.json` 的 `bazi.depth.yongshen.strategy_matrix.strategyScoringMatrix`。

## Verified Scope

并列策略覆盖：

- 调候
- 扶抑
- 通关
- 病药
- 格局用神

每个策略具备：

- `appliesWhen`
- `doesNotApplyWhen`
- `scoreBasis`
- `conflictPolicy`

合同口径：

- 多策略并列评分，不输出唯一绝对用神。
- 调候、扶抑、通关、病药、格局用神互不覆盖。
- 高风险现实建议仍由 policy gate 拦截。

## Evidence

- `contracts/fate/rule_depth_registry.json`
- `contracts/fate/classics_rule_index.json`
- `tests/regression/test_bazi_ziwei_rule_depth.py`

## Commands

```bash
rg '调候|扶抑|通关|病药|格局用神|doesNotApplyWhen' contracts/fate governance/tasks -n
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `31 passed in 61.78s`

## Gate

PASS: 每个策略都有 basis、score 来源字段和 `doesNotApplyWhen`。

## Remaining Work

- `TP-07.03` 补用神反例与报告边界。
- `TP-07.02` 再推进冲突排序 evaluator，输出 ranking/conflicts，不输出唯一绝对结论。

## Guardrail

当前只是策略合同完成。运行时评分仍需在后续 evaluator 任务中补齐格局用神与冲突排序，不得提前宣称用神裁决 100%。
