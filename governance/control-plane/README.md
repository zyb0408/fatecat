---
id: CONTROL-PLANE-README
type: control-plane
status: active
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P90D
---

# 控制面

FateCat 企业化迁移采用 7 个控制面，不建设大一统编排器。

## 控制面清单

- 工程交付控制面：根 `scripts/`、`.github/workflows/acceptance.yml`、pytest、ruff、mypy、导出 smoke。
- 治理与任务控制面：`governance/`。
- 服务运行控制面：`domains/*/services/*/service.yaml` 与后续 `infra/runtime/`。
- 数据与计算控制面：`contracts/fate`、golden 数据、规则 evidence。
- 基础设施控制面：`infra/`。
- 安全与策略控制面：source/export hygiene、privacy fixtures、secret policy。
- 可观测与可靠性控制面：health、delivery smoke、production-readiness。
