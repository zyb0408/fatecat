# AGENTS.md - infra/environments

## 目录用途

`infra/environments/` 承载环境模板和非 secret 配置，是服务读取运行配置的入口。

## 目录结构

```text
infra/environments/
├── AGENTS.md
├── local/
│   ├── AGENTS.md
│   ├── .env.example
│   ├── agent.env.example
│   └── branding.json
└── production/
    ├── AGENTS.md
    └── .env.production.example
```

## 职责边界

- `local/`：本地开发、smoke 和 dry-run 的配置模板与品牌配置。
- `production/`：公网生产配置模板，只保存变量口径，不保存真实 secret。
- 真实 `.env`、token、cookie、证书和私钥不得进入 Git 或导出包。
- 业务代码只能读取配置，不把运行期 secret 写回这里。
