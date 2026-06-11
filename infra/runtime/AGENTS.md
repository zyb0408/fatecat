# AGENTS.md - infra/runtime

## 目录用途

`infra/runtime/` 只承载本地运行态占位和目录骨架，真实运行数据不得入库。

## 目录结构

```text
infra/runtime/
├── AGENTS.md
└── local-state/
    ├── AGENTS.md
    └── database/
        └── bazi/
            └── .gitkeep
```

## 职责边界

- `local-state/`：本地 smoke、Bot、API 和临时数据库的默认落点。
- `*.db`、日志、队列、缓存和用户输出必须被 Git 与导出卫生门禁排除。
- 生产运行态应迁往外部数据库、对象存储或受管平台，不依赖仓库目录。
