# AGENTS.md - tools/reference-repos

## 目录用途

`tools/reference-repos/` 保存第三方开源仓库快照与 vendor manifest，是命理算法复用的供应链参考层。

## 目录结构

```text
tools/reference-repos/
├── AGENTS.md
├── README.md
├── vendor_sources.json
├── github/
└── web/
```

## 职责边界

- `vendor_sources.json`：所有 vendor 快照的来源、用途、许可证、生产角色、分发边界、revision 和 sha256 登记。
- `github/`：来自 GitHub 的只读参考实现；禁止直接魔改 vendor 源码。
- `web/`：网页参考快照，只能作为 fixture / 解析参考，不承载真实用户数据。
- 服务代码通过 adapter、manifest 和明确路径读取这里，不把供应商代码复制进业务模块。
- `usageRole=production_dependency` 只允许用于 SPDX 许可证明确、`productionUseAllowed=true` 且已通过测试证明的条目。
- 缺少上游 LICENSE 的条目只能作为 `reference_only`、`oracle_only` 或 `future_candidate`，不得扩大成生产依赖。

## Ponytail Evidence

- existence: this directory is the current offline source for licensed dependencies, oracle fixtures, and reference-only material.
- owner: tradecatlabs/fate-core supply-chain boundary.
- verification: `bash scripts/vendor-health.sh` and policy asset tests.
- ceiling: production code must prefer package-manager dependencies over copying vendor source.
