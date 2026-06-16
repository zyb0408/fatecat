# tools/reference-repos

`tools/reference-repos/` 是 FateCat 的第三方命理与历法参考仓库快照层。这里保存的是供应链证据，不是业务源码目录。

## 目录结构

```text
tools/reference-repos/
├── AGENTS.md
├── README.md
├── vendor_sources.json
├── github/
└── web/
```

## 真相源

`vendor_sources.json` 是 vendor 来源、用途、许可、分发边界和快照 hash 的真相源。

核心字段：

| 字段 | 含义 |
| --- | --- |
| `usageRole` | 当前项目允许的用途：`production_dependency`、`oracle_only`、`evaluation_only`、`reference_only`、`future_candidate` |
| `productionUseAllowed` | 是否允许进入生产运行链路 |
| `licenseStatus` | 许可证状态；生产依赖必须是 `spdx` |
| `distributionAllowed` | 当前快照是否允许随仓库或导出包分发 |
| `auditRequired` | 是否必须人工复核后才能扩大用途 |
| `snapshotSha256` | 快照完整性校验值 |

## 当前边界

| 仓库 | 角色 | 生产链路 |
| --- | --- | --- |
| `lunar-python` | 主历法底座 | 允许；已在 Python 依赖文件显式声明 |
| `bazi-1` | 八字规则与资料参考 | 不允许作为新增生产依赖扩散；缺少上游 LICENSE |
| `sxwnl` | 节气/历法离线 oracle | 不进入主生产链；缺少上游 LICENSE |
| `bazica` | Go 八字排盘 oracle | 不进入 Python 主链 |
| `bazi-calculator-by-alvamind` | TypeScript 基础结构参考 | 不进入生产链；本地快照无独立 LICENSE 文件 |
| `MingLi-Bench` | 离线评测基准 | 不进入请求链路，不默认调用模型 API runner |
| `iztro` / `dantalion` | 未来候选能力 | 启用前必须重新完成架构、许可和验收 |

## 维护规则

1. 不在 `tools/reference-repos/github/*` 内魔改第三方源码。
2. 新增快照必须登记到 `vendor_sources.json`，并补齐来源、用途、许可、hash 和风险说明。
3. 缺少独立 LICENSE 或 `licenseStatus=missing_upstream_license` 的材料不得标为 `production_dependency`。
4. Benchmark 类仓库只作为离线评测资产，不默认调用外部模型、云 API 或生产服务。
5. 更新 manifest 后运行：

```bash
bash scripts/vendor-health.sh
```

## 使用方式

服务代码只能通过 adapter、manifest 或明确的路径常量读取这里的资产。新增生产依赖必须优先走包管理器声明，并用测试证明不会隐式依赖 vendor 快照。

Ponytail evidence：existence 来自离线 smoke、oracle 对照和 license manifest；owner 是 tradecatlabs/fate-core supply-chain boundary；verification 是 `bash scripts/vendor-health.sh`；ceiling 是生产依赖优先进入包管理器，vendor 快照不作为通用代码仓。
