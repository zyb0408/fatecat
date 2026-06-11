# AGENTS.md - domains/fate-analysis

## 目录用途

`domains/fate-analysis/` 管理 FateCat 的核心命理分析领域，优先复用成熟开源排盘与历法实现，自研代码只做连接、编排、适配和业务规则表达。

## 目录结构

```text
fate-analysis/
└── services/
    └── fate-core/
```

## 职责边界

- 承载纯分析、capability 执行、字段 profile 消费和报告 evidence 生成。
- 不承载 Telegram、FastAPI、Web HTML 的展示逻辑。
- 不直接魔改 vendor 快照；外部算法通过 adapter 层消费。

## 依赖方向

- `fate-analysis/services/fate-core -> contracts/fate + tools/reference-repos`
- 禁止依赖 `domains/experience-delivery`。
