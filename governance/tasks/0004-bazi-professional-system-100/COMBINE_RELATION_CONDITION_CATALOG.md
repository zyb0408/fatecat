# Combine Relation Condition Catalog

任务节点：`TP-06.01`

## 结论

合化/成化/破化/争合/阻隔条件目录已闭合到 registry 与 runtime 输出。`baziBenchmark.combineTransformMatrix.stateCatalog` 现在包含 `structural_relation`、`transform_candidate`、`transform_success`、`transform_broken`、`contested_transform`，并通过 `stateContracts` 暴露每个状态的 `evidenceFields`、`counterConditions` 和 `riskBoundary`。

## Verify

```bash
rg '合化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n
```

Result:

```text
PASS
```

Additional API check:

```text
31 passed in 5.14s
```

## Gate 判定

- `每种关系状态都有 required evidenceFields`：`PASS`
- `每种关系状态都有 counterConditions`：`PASS`
- `缺少成化证据时不宣称已经成化`：`PASS`

## 边界

本节点只定义和暴露状态目录，不把任一合象自动提升为成化结论。真正合化状态链 evaluator 由 `TP-06.02` 承接。
