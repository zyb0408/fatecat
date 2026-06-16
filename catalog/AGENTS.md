# AGENTS.md - catalog

## 目录用途

`catalog/` 承载组件发现、owner、生命周期、依赖和运行指针，不承载部署 manifest 或运行逻辑。

## 目录结构

```text
catalog/
├── AGENTS.md
└── components/
```

## 职责边界

- 每个生产候选服务必须有 catalog 组件登记。
- catalog 只引用 service.yaml、runbook、contracts 和 governance 证据。
- 不把 catalog 当成运行期望状态真相源。
- active 组件不得声明 `compatibility_source_root` 或 `temporary-compatibility-box`；旧路径只允许出现在迁移账本和历史证据中。

## Principle Gate Evidence

- target end state: active catalog only points to canonical service roots and lifecycle metadata.
- real constraints: negative guard strings must remain testable to prevent old roots returning.
- inertia constraints: retired source roots remain in migration evidence but cannot guide runtime.
- kill list: active source/runtime pointers that name old project modules or compatibility boxes.
- proof point: `test_catalog_contracts.py` passes and components keep `canonical-active`.
- falsifier: any component adds an active old root pointer or source root outside canonical services.
- migration slice: keep guard text here, keep historical detail in governance migration evidence.

## 依赖方向

- `catalog -> domains + contracts + infra + governance`
