# Advanced Pattern Rule Matrix

任务节点：`TP-05.01`

## 结论

高级格局规则矩阵已闭合到 registry 与 runtime 输出。`从格`、`假从`、`专旺`、`化气` 均在 `contracts/fate/rule_depth_registry.json` 中保留 `appliesWhen`、`breaksWhen`、`sourceRuleId` 和 `riskBoundary`；runtime 的 `specialPatternCandidates` 同步暴露 `appliesWhen`、`breaksWhen`、`counterEvidence`、`lifecycle` 和 `lifecycleGate`。

## Verify

```bash
rg '从格|假从|专旺|化气|specialPattern' contracts/fate domains/fate-analysis -n
```

Result:

```text
PASS
```

## Gate 判定

- `每类高级格局至少有成立条件和反证条件`：`PASS`
- `候选输出带 counterEvidence 和 lifecycleGate`：`PASS`
- `未达完整条件时不得强断`：`PASS`

## 边界

本节点只把高级格局定义成证据矩阵与候选层，不把任何高级格局升为最终 production 定格。
