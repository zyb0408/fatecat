# High-Risk Output Regression

任务节点：`TP-03.03`

## 结论

高风险输出边界回归通过。当前 policy assets 和 bazi statement golden 能拦截医疗、金融、法律、心理替代建议、保证式话术和恐吓式表达。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q
```

Result:

```text
19 passed in 55.70s
```

## Gate 判定

- `高风险词和保证式话术被 policy regression 拦截`：`PASS`
- `健康、财运、灾劫、官非等专题只允许趋势/结构证据`：`PASS`
- `旧地区隐藏文案不作为隐私策略继续使用`：`PASS`

## 后续边界

后续 `TP-08` 岁运专题和 topic profile 增强时，必须继续复用本节点的输出边界：不得输出确定未来、现实处方、投资建议、诊疗建议、法律建议或心理替代建议。
