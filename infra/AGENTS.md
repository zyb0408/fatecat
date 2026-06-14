# AGENTS.md - infra

## 目录用途

`infra/` 承载环境、容器、GitOps、systemd、数据库、观测、安全和灾备的期望状态。

## 目录结构

```text
infra/
├── AGENTS.md
├── docker/
│   ├── AGENTS.md
│   ├── Dockerfile.delivery
│   └── entrypoint.delivery.sh
├── databases/
│   └── bazi/
│       └── schema_v2.sql
├── environments/
│   ├── local/
│   │   ├── .env.example
│   │   ├── agent.env.example
│   │   └── branding.json
│   └── production/
│       └── .env.production.example
└── runtime/
    └── local-state/
        └── database/
            └── bazi/
                └── .gitkeep
```

## 职责边界

- `environments/`：配置模板与非 secret 环境配置。
- `docker/`：容器镜像、entrypoint 和容器运行期健康检查定义。
- `databases/`：schema/migration，不保存数据库实库。
- `runtime/`：本地运行态目录骨架，不提交日志、缓存、数据库和用户输出。
- GitOps、systemd、观测、安全和灾备后续继续归入这里。
- 业务逻辑、报告字段和 capability 契约不放在 `infra/`。

## 依赖方向

- `infra -> domains/*/services/* + contracts/*`
- 领域服务读取 infra 提供的环境，不把 secret 写回源码。
