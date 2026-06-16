# TP-07.03 Yongshen Report Boundary Evidence

## Result

PASS.

用神反例与报告边界矩阵已写入 `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` 的 `yongShenCounterexampleMatrix`。

## Verified Scope

覆盖场景：

- 禁止唯一绝对用神结论
- 调候 vs 扶抑冲突
- 通关/病药关系覆盖
- 专题报告 beta/blocked 边界

每个场景具备：

- `caseId`
- `expectedNoAbsoluteConclusion`
- `failureExplanation`
- 必要的冲突类型或禁止用语边界

## Evidence

- `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- `tests/regression/test_bazi_ziwei_rule_depth.py`
- `tests/regression/test_bazi_statement_golden.py`

## Commands

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
```

Observed:

- `test_bazi_ziwei_rule_depth.py`: `34 passed in 77.85s`
- combined golden/rule-depth/statement regression: `48 passed, 1 skipped in 173.82s`

## Gate

PASS: 冲突样本解释 ranking 变化，报告保留边界，不输出确定未来、现实处方或恐吓式断语。

## Remaining Work

- `TP-07.02` 继续实现用神冲突排序 evaluator，纳入格局用神并保持 `noAbsoluteConclusion`。

## Guardrail

用神输出仍是传统文化解释优先级，不是医疗、金融、法律、心理或婚姻现实决策建议。
