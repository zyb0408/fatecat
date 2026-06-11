# AGENTS.md - contracts

## 目录用途

`contracts/` 承载 API、事件、数据集、AI 工具、资源和策略契约，是机器可读事实源，不是普通说明文档。

## 目录结构

```text
contracts/
└── AGENTS.md
```

## 职责边界

- FateCat capability registry、profile、evidence schema、risk policy 后续迁入 `contracts/fate/`。
- 普通产品说明写入 `docs/`，治理证据写入 `governance/`。

## 依赖方向

- `domains -> contracts`
- `apps/ai -> contracts`
- 禁止契约依赖交付实现。
