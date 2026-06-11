# fate-core

FateCat 纯分析领域服务。它把成熟历法、八字、紫微和相关预测流派的外部能力整理成稳定 capability、profile 和 evidence 输出。

## 当前状态

- Lifecycle: `active-canonical`
- 当前源码根：`domains/fate-analysis/services/fate-core/src/`
- 运行资产：`contracts/fate/`、`domains/fate-analysis/data-products/`、`infra/databases/`、`tools/reference-repos/`

## 验证入口

```bash
python -m pytest -q domains/fate-analysis/services/fate-core/tests
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

## 维护原则

- 不改变 pure-analysis JSON 结构。
- 不改变 capability registry 对外语义。
- 不修改 vendor 源码。
- 行为保持验证先于大规模重构。
