# AGENTS.md - platform

## 目录用途

`platform/` 承载 Golden Path、CI/CD 模板、供应链能力和开发者平台工具，不承载 FateCat 命理业务规则。

## 目录结构

```text
platform/
└── AGENTS.md
```

## 职责边界

- 后续将结构门禁、供应链验证、SBOM/provenance 策略归到这里。
- 当前根 `scripts/` 仍是本地执行入口，平台化前不得新增黑盒编排器。

## 依赖方向

- `platform -> scripts + governance + catalog`
- 禁止 `platform` 反向定义领域能力。
