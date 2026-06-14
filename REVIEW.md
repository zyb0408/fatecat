# FateCat 自审记录

审查时间：2026-06-15 HKT +0800

## 结论

当前仓库已迁移到企业级 canonical roots，公开口径已统一为 TradeCat Labs 实验室项目。本地代码质量、结构卫生、生产静态门禁、Web 回归和容器运行 smoke 为 `PASS`。

直接公网生产发布仍为 `WARN`：缺少真实域名/TLS/反向代理、生产 URL、真实 Telegram Bot token、真实 HSTS/proxy/header 验收和远端 CI 对本轮提交的最终结果。必须在推送后等待 GitHub Actions 通过，并在真实环境执行：

```bash
bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
```

## 当前证据

| 项目 | 证据 |
|---|---|
| 当前分支 | `main` |
| 本轮基线 HEAD | `9106be0 fix: track production env template` |
| 当前目录形态 | 根目录使用 `apps/`、`ai/`、`domains/`、`platform/`、`infra/`、`contracts/`、`catalog/`、`governance/`、`shared/`、`tools/`、`docs/`、`scripts/`、`tests/` canonical roots |
| 最新远端 CI 基线 | `FateCat Acceptance` success `27504782295`；`FateCat Container` success `27504782301`，均对应 `9106be0` |
| 全量 pytest | `.venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests domains/experience-delivery/services/fatecat-delivery/tests tests/regression`：`120 passed in 158.44s` |
| ruff / format / mypy | `ruff check .` 通过；`ruff format --check .` 为 `113 files already formatted`；`mypy -p fate_core` 为 `Success: no issues found in 31 source files` |
| 结构与卫生门禁 | `check-structure.sh`、`check-source-hygiene.sh`、`check-privacy-fixtures.sh`、`git diff --check` 通过 |
| 生产静态门禁 | 带生产等价 env 的 `scripts/production-readiness.sh --skip-bootstrap` 通过；真实 API URL 与 live Bot 验收未执行 |
| 容器 smoke | BuildKit 本地 cache 导出失败；使用 `DOCKER_BUILDKIT=0 docker build -f infra/docker/Dockerfile.delivery -t fatecat-delivery:legacybuilder .` 构建成功，`scripts/container-smoke.sh --skip-build --image fatecat-delivery:legacybuilder --port 8003` 通过 |

## 本轮处理

- `REVIEW.md` 已从 2026-05-07 的旧 `scripts/project/` 口径更新为当前企业仓库与生产化状态。
- `/web` 页面保留原生 HTML 表单和服务端直出 Markdown，底部“页面说明与元信息”保持默认收起，并补齐轻量 CSS、移动端可读性、错误态层级和结果锚点导航。
- TradeCat Labs 项目口径已进入 branding、README、报告页脚、Bot 按钮、配置和相关文档。
- 请求体大小限制不再只依赖 `Content-Length`：应用层会按 request stream 限额缓冲，缺失或绕过 `Content-Length` 的超大 body 返回 413。
- `/metrics` 增加 `fatecat_request_latency_seconds_bucket/count/sum` histogram 和 `fatecat_request_errors_total` 错误分类计数。
- 请求链路增加 `X-Request-ID` 响应头和结构化 HTTP 访问日志，日志包含 route、status、elapsedMs、client、errorClass。
- `production-readiness.sh` 增加多副本限流门禁：`FATE_DEPLOYMENT_REPLICAS>1` 时禁止继续使用 `FATE_RATE_LIMIT_BACKEND=memory`。
- 生产配置模板补齐 `FATE_DEPLOYMENT_REPLICAS`、`FATE_RATE_LIMIT_BACKEND`、`FATE_EDGE_BODY_LIMIT_ENABLED`，并记录边缘层 body limit 与应用层兜底的职责边界。

## 剩余风险

### 外部生产验收

- 真实公网域名、TLS、反向代理、生产 URL、CORS allowlist、HSTS、可信代理头和真实 Bot token 仍需在外部环境验证。
- 当前 production-readiness 静态门禁只能证明配置口径，不证明公网链路、证书、代理转发、Bot API 和云侧限流真实可用。
- 推送本轮提交后，远端 `FateCat Acceptance` 与 `FateCat Container` 结果才是最终 CI 证据。

### 多副本公共服务

- 应用内 memory 限流只适合单副本兜底；多副本公共服务必须迁到网关、Redis、WAF 或云平台统一限流。
- 请求体上限已做应用层流式兜底；公网仍应在 Nginx、Traefik、Cloudflare 或等价边缘层配置 body limit。

### 可观测性

- 当前已具备 `/metrics`、`/ready`、延迟 histogram、错误分类和 request id 日志。
- 尚未接入外部 Prometheus/Grafana 告警、集中日志、分布式 tracing 或业务级 p95/p99 看板；公共服务上线前应补齐运行平台侧仪表盘和告警规则。

### 代码维护

当前核心文件仍偏大，应按后续业务改动逐步收边界，不建议在本轮为了行数做大拆：

| 文件 | 行数 | 后续边界 |
|---|---:|---|
| `domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py` | 2775 | 计算内核、规则索引、评分/触发拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py` | 1967 | 报告模板、章节渲染、品牌页脚拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/bot.py` | 1145 | Bot 交互、命令解析、交付编排拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/main.py` | 905 | API 路由、公共服务护栏、观测指标拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` | 669 | 表单、工作台、Markdown 输出、页面元信息拆分 |

## 当前门禁

- 本地功能回归：PASS
- 本地结构 / 源码 / 隐私卫生：PASS
- 生产静态配置：PASS，外部 live API 和 live Bot 为未执行
- 容器运行 smoke：PASS，BuildKit 本机 cache 需要清理或重建 builder 后再恢复默认构建路径
- 直接公网生产发布：WARN，等待真实环境验收与本轮远端 CI
