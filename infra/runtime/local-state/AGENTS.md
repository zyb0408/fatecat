# AGENTS.md - infra/runtime/local-state

## 目录用途

`infra/runtime/local-state/` 是本地开发和 smoke 的可清理运行态目录。

## 目录结构

```text
infra/runtime/local-state/
├── AGENTS.md
└── database/
    └── bazi/
        └── .gitkeep
```

## 职责边界

- 只提交 `.gitkeep` 与必要目录说明。
- 真实数据库、日志、队列文件、缓存和用户报告不得提交。
- 清理入口由 `scripts/clean-runtime.sh` 和 hygiene 门禁维护。
