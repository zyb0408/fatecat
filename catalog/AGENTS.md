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

## 依赖方向

- `catalog -> domains + contracts + infra + governance`
