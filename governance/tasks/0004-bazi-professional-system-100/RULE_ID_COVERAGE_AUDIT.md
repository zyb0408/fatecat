# RuleId Coverage Audit

任务节点：`TP-03.01`

## 结论

当前 rule-depth、policy 和 API/Web 组合回归已通过。`TP-03.01` 的直接失败来自旧隐私断言要求 Web 不显示“上海”，而当前产品口径要求提交后的出生地区必须显示；已修正测试为显示提交地区且禁止旧“非北京地区已隐藏”文案回潮。

## 当前规则来源

| 资产 | 八字规则数 | 用途 |
| --- | ---: | --- |
| `contracts/fate/rule_depth_registry.json` | 22 | 深度规则、证据字段、冲突策略、风险边界 |
| `contracts/fate/classics_rule_index.json` | 43 | sourceRuleId 来源索引、短规则摘要、适用条件 |

## 缺口队列

缺口不在本节点直接实现，已进入 `RULE_SOURCE_GAPS.md`：

- `GAP-BZ-EVIDENCE-001`
- `GAP-BZ-PATTERN-001`
- `GAP-BZ-HEHUA-001`
- `GAP-BZ-YONGSHEN-001`
- `GAP-BZ-FORTUNE-001`
- `GAP-BZ-TOPIC-001`
- `GAP-BZ-BENCHMARK-001`

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
```

Result:

```text
44 passed in 61.80s
```

## Gate 判定

- `未登记断语不能进入 production 报告`：`PASS with backlog`
- `旧地区隐藏断言已退役`：`PASS`
- `高风险输出仍由 policy assets 保护`：`PASS`
