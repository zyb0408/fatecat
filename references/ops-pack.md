# FateCat Skill 运维包说明

## 目标

把“出问题时临时查命令”改成“平时就能沉淀的 agent 运维包”。

Principle gate evidence：target end state 是日常采集健康、日志、配置和门禁证据；real constraints 是本仓只提供本地自托管运维包；inertia constraints 是事后补日志会丢失排障上下文；kill list 是无证据的线上口头判断；proof point 是 `collect-ops-bundle.sh` 可执行；falsifier 是故障后无法回指命令、日志或 evidence dir；migration slice 是先统一本地采集，再接入真实部署平台。

## 当前仓库已经提供什么

- 健康检查入口：`bash scripts/health.sh --mode pure --json`
- 标准验收入口：`bash scripts/acceptance.sh --with-dev`
- 启动入口：`bash scripts/serve-api.sh`、`bash scripts/serve-bot.sh`
- 交付层烟雾入口：`bash scripts/delivery-smoke.sh --target api`、`bash scripts/delivery-smoke.sh --target bot --startup-timeout 8`
- 容器入口：`bash scripts/container-build.sh`、`bash scripts/container-smoke.sh`、`bash scripts/container-release.sh`
- 生产就绪门禁：`bash scripts/production-readiness.sh --api-url <url> --require-live-bot`
- 生命周期状态入口：`bash scripts/lifecycle-status.sh`
- 运维包采集：`bash scripts/collect-ops-bundle.sh --output <dir>`

## 运维包默认内容

- 采集时间与 git 版本
- skill 根和 project 根路径
- FateCat CLI 帮助输出
- 纯分析健康检查结果
- 生命周期状态摘要
- 当前 skill 的入口文档索引

## 可观察性边界

- 当前仓库能提供“进程前”与“进程内”的检查入口。
- API 交付层提供 `/health`、`/live`、`/ready` 和 `/metrics`，可接入外部探针与指标采集。
- 当前仓库不会自动替你接 Prometheus、Grafana、Sentry、systemd、supervisor、k8s 或云告警平台。
- 如果你要真正实现自动救活，需要把这里提供的健康检查与重启命令接到目标环境的守护体系。

## 公共服务 SLO

| 目标 | SLO | 观测方式 | 处理口径 |
| --- | --- | --- | --- |
| 可用性 | 月度 `/health` 与 `/ready` 成功率 >= 99.5% | 外部探针 + `fatecat_requests_total` | 低于目标时先降级记录接口和 Bot，再查依赖 |
| 延迟 | `/api/v1/bazi/pure-analysis` p95 <= 2s，p99 <= 10s | `fatecat_request_latency_seconds_bucket` | 超阈值时先看 inflight、CPU、Bot 队列和下游计算耗时 |
| 错误率 | 5xx + timeout 5 分钟错误率 < 1% | `fatecat_request_errors_total` | 连续触发时停止发布，回滚镜像或切旧实例 |
| 限流 | 429 可出现但不得持续高于业务预期 | `fatecat_requests_total{status="429"}` | 持续升高时检查攻击流量、网关限流和 Bot 队列容量 |
| 请求体 | 413 不应集中爆发 | `fatecat_request_errors_total{error_class="body_too_large"}` | 集中爆发时检查客户端和边缘 body limit 配置 |
| Bot 队列 | `queue_size / queue_max <= 0.8` | `fatecat_bot_queue_size` / `fatecat_bot_queue_max_size` + `fatecat_bot_queue_scope_info` | 单实例先降低入口或调小并发；托管多副本再迁外部队列 |

## Prometheus / Grafana 建议

最小抓取目标：

```yaml
scrape_configs:
  - job_name: fatecat-delivery
    metrics_path: /metrics
    static_configs:
      - targets: ["<host>:8001"]
```

推荐面板：

```promql
histogram_quantile(0.95, sum(rate(fatecat_request_latency_seconds_bucket[5m])) by (le, route))
histogram_quantile(0.99, sum(rate(fatecat_request_latency_seconds_bucket[5m])) by (le, route))
sum(rate(fatecat_request_errors_total{error_class=~"server_error|timeout"}[5m])) by (route, error_class)
sum(rate(fatecat_requests_total{status="429"}[5m])) by (route)
fatecat_inflight_requests
fatecat_calculation_slots_in_use / fatecat_calculation_slots_max
fatecat_bot_queue_size / fatecat_bot_queue_max_size
fatecat_bot_queue_scope_info
```

最小告警：

| 告警 | 条件 | 处理 |
| --- | --- | --- |
| HighErrorRate | 5xx/timeout 错误率 5 分钟 > 1% | 查 `X-Request-ID` 对应日志，必要时回滚 |
| HighLatencyP99 | p99 10 分钟 > 10s | 查 CPU、inflight、外部限流和 Bot 队列 |
| CalculationSlotSaturation | 计算槽位持续 > 80% | 降低入口速率，排查慢样本；长期触发时升级为独立 worker |
| RateLimitSpike | 429 5 分钟持续高于基线 | 查网关/WAF、爬虫和 `FATE_RATE_LIMIT_PER_MINUTE` |
| BodyTooLargeSpike | 413 突增 | 查客户端请求体和边缘 body limit |
| BotQueueSaturation | Bot 队列占用持续 > 80% | 暂停 Bot 入口、降低并发入口或扩容队列 |

## 日志关联

- HTTP 响应始终返回 `X-Request-ID`。
- 业务异常日志使用 JSON 结构，字段包含 `event`、`requestId`、`errorType`。
- 排障顺序：先从告警路由和状态码定位 `route`，再按 `requestId` 搜索业务日志，最后结合 `/metrics` 的错误分类判断是输入、限流、超时还是服务端异常。
- `fatecat_bot_queue_scope_info{backend="memory",scope="single_process"}` 表示 Bot 补发与背压只覆盖当前进程；用户独立部署单实例可接受，多副本托管必须迁到外部队列或独立 Bot worker。

## 上线 / 回滚 / 降级 / 清理

上线：

```bash
bash scripts/local-ci.sh --profile all
bash scripts/container-release.sh --image <registry/repo> --tag <tag> --push
bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
```

回滚：

```bash
docker pull <registry/repo>:<previous-tag>
docker stop fatecat-delivery || true
docker run --rm -p 8001:8001 --env-file <production-env> <registry/repo>:<previous-tag>
```

降级：

```bash
FATE_RECORDS_ENABLED=0
FATE_RATE_LIMIT_PER_MINUTE=<lower-safe-limit>
FATE_BOT_QUEUE_MAX_SIZE=<safe-queue-size>
```

清理本地运行态：

```bash
bash scripts/clean-runtime.sh
bash scripts/collect-ops-bundle.sh --output /tmp/fatecat-ops-bundle
```

## 推荐落地方式

### 用户独立部署 / 单实例

- 用 `bootstrap.sh` 保证环境一致
- 用 `preflight.sh` 作为默认巡检入口
- 用 `acceptance.sh --with-dev` 作为发布前验收入口；默认同时验证源码仓库静态门禁、API/Bot 入口和导出后的 lite skill 包
- 用 `collect-ops-bundle.sh` 固化每次发布或事故后的证据
- 保留 `FATE_RATE_LIMIT_BACKEND=memory`、SQLite records 和本地 Bot outbox 是可接受的轻量方案；备份 `infra/runtime/local-state/` 或关闭记录接口即可。
- `FATE_REQUEST_TIMEOUT_SECONDS` 负责响应超时；`FATE_MAX_INFLIGHT_CALCULATIONS` 负责同步命理计算背压。底层 Python 线程不能被强制杀死，但槽位会持续占用到计算结束，从而避免超时请求继续无限堆积。需要强杀计算任务时，升级为进程级 worker/队列。

### 服务化交付

- 用 `serve-api.sh` 或 `serve-bot.sh` 作为启动命令
- 在上线前先跑目标入口的 `delivery-smoke.sh`；发布前总验收默认同时覆盖 API 与 Bot dry-run
- 用 `container-smoke.sh` 验证 Docker 镜像真实可启动，且 `/health` 与排盘 API 均可用
- 推送 registry 前用 `container-release.sh --image <registry/repo> --tag <tag> --push`，并先完成 `docker login`
- 纯公共排盘服务优先设置 `FATE_RECORDS_ENABLED=0`；只有明确需要用户记录时才开启记录接口和 token
- 真正公网生产前必须跑 `production-readiness.sh`；没有真实 API URL、真实 Telegram token、生产 CORS allowlist 和记录接口 token 或无状态模式时，只能算仓库内 dry-run 通过
- 生产等价 env 的最小合同：真实 HTTPS CORS allowlist、无状态或真实记录 token、请求体上限、请求超时、非零限流；只有多副本/托管公网才要求外部限流、边缘 body limit、可信代理头和 HSTS 口径。
- 本地静态验收可使用 `FATE_RECORDS_ENABLED=0 FATE_CORS_ALLOW_ORIGINS=https://fatecat.tradecatlabs.example FATE_RATE_LIMIT_BACKEND=gateway FATE_EDGE_BODY_LIMIT_ENABLED=1 FATE_TRUST_PROXY_HEADERS=1 FATE_ENABLE_HSTS=1 bash scripts/production-readiness.sh --skip-bootstrap`；这不等于公网 live 验收。
- 把健康检查接进外部守护器
- 把运维包放进发布记录或事故记录

## 自动救活的最小定义

当前 skill 对“自动救活”的最小支持是：

- 有健康检查入口
- 有确定的启动入口
- 有故障证据采集入口
- 有阶段状态与运维说明

这意味着它已经具备接入自动恢复系统的前提，但不等于仓库已经直接替你安装好了恢复系统。
