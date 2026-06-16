# Report Field Contract

任务节点：`TP-03.02`

## 结论

`TP-03.02` 的 API/capability regression 已通过。后续新增专业结论必须优先进入结构化字段，再由 Markdown/Web/Bot 渲染；delivery 不得基于文案二次推断命理规则。

## 必需字段

| 字段 | 要求 |
| --- | --- |
| `sourceRuleId` | 必须能回指 `classics_rule_index` 或 `rule_depth_registry` |
| `evidenceFields` | 必须列出实际使用的盘面、时间、十神、关系或岁运字段 |
| `score` / `weight` | 涉及排序、候选、强弱和专题 profile 时必须保留 |
| `doesNotApplyWhen` | 高级格局、合化、用神、专题判断必须给反证条件 |
| `riskBoundary` | 高风险专题和非确定判断必须保留边界 |
| `lifecycle` | `beta`、`guarded`、`production`、`unsupported` 不得混写 |

## 消费边界

- `fate-core` 负责领域算法、证据构建和 topic profile。
- `delivery API/Web/Bot/Markdown` 只消费结构化结果和风险边界。
- Web 页面不得重新计算命理规则。
- Markdown 报告不得新增无 ruleId 的强断段落。

## Verify

```bash
.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q
```

Result:

```text
41 passed in 5.64s
```

## Gate 判定

- `新增字段不破坏 API/Web/Markdown 消费者`：`PASS`
- `报告中不再只有自然语言结论`：`PASS with backlog`
- `后续新增专业段落必须带 evidence/riskBoundary`：`ENFORCED BY TASK TREE`
