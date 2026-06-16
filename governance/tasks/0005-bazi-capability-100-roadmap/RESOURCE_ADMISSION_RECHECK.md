# TP-01.02 Resource Admission Recheck

## Status

- Result: `PASS`
- Scope: 复核外部资源准入与 license/source 边界。
- Command: `rg 'production_dependency|oracle_only|evaluation_only|reference_only|future_candidate' governance/tasks/0004-bazi-professional-system-100/RESOURCE_MAP.md -n`

## Evidence

`governance/tasks/0004-bazi-professional-system-100/RESOURCE_MAP.md` 已定义资源角色和禁止路径：

| Role | Resource | Production Use |
| --- | --- | --- |
| `production_dependency` | `lunar-python` | allowed |
| `oracle_only` | `sxtwl`、`sxwnl`、`paipan`、`bazica` | forbidden |
| `evaluation_only` | `MingLi-Bench` | forbidden |
| `reference_only` | `bazi-1`、`bazi-calculator-by-alvamind` | forbidden |
| `future_candidate` | `BaziQA`、`rule-engine`、`iztro` | forbidden until admission |

## Gate Decision

- 每个资源有 `usageRole`：`PASS`
- 每个资源有 `productionUseAllowed` 口径：`PASS`
- 每个资源有禁止用途：`PASS`
- `production/oracle/evaluation/reference/future_candidate` 边界不混写：`PASS`

## Next

- 后续任务不得把 `sxtwl`、`sxwnl`、`paipan`、`bazica`、`MingLi-Bench`、`BaziQA` 或 `bazi-1` 升级为 runtime dependency，除非先通过明确 admission gate。
