# AGENTS.md - infra/databases

## 目录用途

`infra/databases/` 保存数据库 schema、migration 和数据结构说明，不保存运行时数据库实库。

## 目录结构

```text
infra/databases/
├── AGENTS.md
└── bazi/
    └── schema_v2.sql
```

## 职责边界

- `bazi/schema_v2.sql`：八字相关本地数据库 schema。
- 运行期 `*.db`、`*.sqlite`、缓存和备份进入 `infra/runtime/` 或外部托管，不进入此目录。
- schema 变更必须配套测试、回滚说明和服务契约影响说明。
