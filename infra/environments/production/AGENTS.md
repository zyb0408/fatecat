# AGENTS.md - infra/environments/production

## 目录用途

`infra/environments/production/` 保存公网生产配置模板，只描述变量口径，不保存真实 secret。

## 目录结构

```text
infra/environments/production/
├── AGENTS.md
└── .env.production.example
```

## 职责边界

- `.env.production.example`：生产容器或平台 secret 注入的参考模板。
- 真实 `.env.production`、token、证书、cookie、私钥和云凭证不得进入 Git。
- 公共服务可设置 `FATE_RECORDS_ENABLED=0` 进入无状态模式；启用记录服务时必须配置 token 和持久化策略。
- 多副本公网服务必须把限流真相源放在 gateway、Redis、WAF 或云平台侧；应用内 memory 限流只作为单副本兜底。
- 请求体大小限制应在反向代理/CDN 与应用层同时配置；`FATE_EDGE_BODY_LIMIT_ENABLED` 只记录外部层已落地，不替代真实网关配置。
