---
id: GOV-CONTEXT-MAP
type: index
status: current
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P90D
---

# Context Map

## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `context/PROJECT-TOPOLOGY.md` | `decisions/adr/INDEX.md` | governance strict validate |
| 治理包 | `governance/` | `context/AGENT-ENTRY.md` | `decisions/adr/INDEX.md` | governance health report |
| 任务容器 | `governance/tasks/` | `tasks/INDEX.md` | `decisions/adr/INDEX.md` | task tree validation |
| FateCat Web HTML 语义界面 | `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` | `context/module-contexts/domains-experience-delivery-services-fatecat-delivery-src-web-ui-py/CONTEXT.md` | `GATE-0001` | `bash scripts/local-ci.sh --profile quick` |

## 维护规则

- 不把模块上下文散落到代码目录。
- 模块上下文统一放在 `context/module-contexts/`。
- 原有模块 README 只被引用，不被治理包覆盖。
- 新增稳定模块后，再创建 `context/module-contexts/<module>/CONTEXT.md` 并更新本表。
