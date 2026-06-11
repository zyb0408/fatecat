# AGENTS.md - domains/experience-delivery

## 目录用途

`domains/experience-delivery/` 管理 FateCat 的用户交付领域：API、Web HTML、Telegram Bot、Markdown 报告和文件交付。

## 目录结构

```text
experience-delivery/
└── services/
    └── fatecat-delivery/
```

## 职责边界

- 只编排交付体验和展示格式，不定义命理核心字段口径。
- 所有领域计算必须通过 `fate-core` 或 `contracts/fate` 暴露的能力协议。
- 配置、secret、运行态和部署期望状态不放在服务源码目录。

## 依赖方向

- `fatecat-delivery -> domains/fate-analysis/services/fate-core + contracts/fate + infra/environments`
- 禁止把报告展示逻辑下沉到纯分析内核。
