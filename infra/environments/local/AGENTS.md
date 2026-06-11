# AGENTS.md - infra/environments/local

## 目录用途

`infra/environments/local/` 保存本地运行配置模板与品牌配置；它替代旧 `assets/config/` 的 active 配置入口。

## 目录结构

```text
infra/environments/local/
├── AGENTS.md
├── .env.example
├── agent.env.example
└── branding.json
```

## 职责边界

- `.env.example`：人工本地运行模板。
- `agent.env.example`：自动 smoke / agent dry-run 模板。
- `branding.json`：统一免责声明、品牌页脚和仓库信息。
- `.env` 只能由本地用户或 smoke 脚本临时创建，退出后必须清理或保持未跟踪。
