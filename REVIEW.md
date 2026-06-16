# FateCat 自审记录

审查时间：2026-06-16 00:06:00 HKT +0800

## 结论

当前仓库保持企业级 canonical roots 结构，公开口径为 TradeCat Labs 实验室项目。按“用户可独立部署单实例”的当前目标，本地代码质量、结构卫生、源码卫生、隐私 fixture、类型检查、格式检查、全量 pytest、导出包、Docker 镜像和容器 `/web` smoke 在当前工作树下为 `PASS`。

外部托管公网发布仍为 `HITL`：当前没有真实公网生产 URL 和真实 Telegram Bot token，因此外部 `/health`、`/ready`、`/metrics` 与 Bot live `get_me` 未执行。不得把真实公网生产验收描述为已通过。

## 当前证据

| 项目 | 证据 |
|---|---|
| 当前分支 | `main` |
| 当前 HEAD | `787111d` |
| 本地/远端差异 | `main...origin/main [ahead 7]` |
| 本地 CI/CD | `bash scripts/local-ci.sh --profile all` -> `PASS`，证据目录 `/tmp/fatecat-local-ci-20260615235920` |
| focused regression | `47 passed in 7.43s` |
| 全量 pytest | `168 passed, 1 skipped in 232.48s` |
| ruff format | `129 files already formatted` |
| ruff lint | `All checks passed!` |
| mypy | `Success: no issues found in 37 source files` |
| delivery smoke | API ready；Bot dry-run 初始化通过 |
| export gate | export lite、export hygiene、strict skill validate、exported pure preflight、clean-runtime 后 hygiene 均通过 |
| container gate | Docker image `fatecat-delivery:local` build 成功；容器 `/web` smoke OK |
| operability runbook | `references/ops-pack.md` |
| production readiness | 静态生产门禁 OK；外部 API URL 与 live Bot 因缺真实输入保持 SKIP |

## 本轮处理

- 八字 legacy 核心迁入 `fate_core.kernel.bazi_calculator`；delivery `src/bazi_calculator.py` 只保留兼容导出。
- `legacy_bazi.py` 不再从 delivery `src` 导入领域算法。
- active catalog 清退 `compatibility_source_root` / `temporary-compatibility-box`，组件状态改为 `canonical-active`。
- 新增 `governance/migration/compatibility-ledger.md`，登记保留兼容入口的 owner、真实契约、保留原因和移除条件。
- 形式工程声明已清退：未实现的 `/graphql`、`/ws`、`/api/v1/batch` 不再被声明为 enabled，`system_optimization.py` 只报告真实能力。
- 假绿测试已修复：核心 smoke 测试捕获异常后改为 `pytest.fail()`，临时输出进入 `tmp_path`。
- API 错误语义已收紧：非法日期/时间返回 422，计算资源耗尽返回 503，内部异常返回 500，不再用 HTTP 200 表达协议失败。
- 单实例独立部署护栏已补齐：请求 body 流式限制、进程内限流、同步计算槽位、Bot 本地 outbox 幂等/原子写入、Prometheus histogram/error/queue/calculation 指标和 runbook 均有回归。
- 规则 registry、future features、oracle、golden matrix、MingLi-Bench gate、SLO/runbook、request id、Bot 队列指标等任务树证据已同步。
- 不运行 GitHub Acceptance；本轮只使用本地 CI/CD 技术工具方案。

## Principle Gate Evidence

- target end state: fate-core owns calculation/rules/evidence; delivery owns API/Web/Bot/report.
- real constraints: existing CLI/API/Bot/report contracts still import stable public symbols.
- inertia constraints: legacy names describe migration history, not the target architecture.
- kill list: delivery-owned domain rules, unowned shims, and undocumented compatibility paths.
- proof point: service contract tests and golden/API/Web regressions pass after kernel migration.
- falsifier: new domain logic appears in delivery or a retained entry lacks owner/removal condition.
- migration slice: keep only registered adapters, then retire them as kernel/provider modules mature.

## 当前门禁状态

| 门禁 | 状态 | 说明 |
|---|---|---|
| 本地 all profile | PASS | `bash scripts/local-ci.sh --profile all` 通过 |
| 结构 / 源码 / 隐私卫生 | PASS | `check-structure`、`check-source-hygiene`、`check-privacy-fixtures` 通过 |
| 格式 / lint / 类型 | PASS | ruff format、ruff check、mypy 均通过 |
| 全量行为回归 | PASS | `168 passed, 1 skipped` |
| Docker / 容器 smoke | PASS | 镜像构建与容器 `/web` smoke 通过 |
| catalog compatibility guard | PASS | active catalog 无 `compatibility_source_root`、`temporary-compatibility-box`、`scripts/project/modules` |
| 真实公网 API / Bot live | HITL | 仅外部托管发布需要；需真实生产 URL、TLS/反向代理、生产 CORS allowlist、真实 `FATE_BOT_TOKEN` |

## 剩余 HITL 验收

独立部署单实例仓库内门禁已通过。若要声明真实公网托管发布，必须在真实公网环境执行：

```bash
bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
```

缺少真实域名、TLS、反向代理、生产 URL、生产 CORS allowlist 和 Bot token 前，外部 live 验收保持 `HITL`，质量结论不做伪证。

## 维护风险

| 文件 | 行数 | 当前边界 |
|---|---:|---|
| `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py` | 2798 | 八字 legacy 核心归属位置，后续继续按历法、四柱、强弱、格局、用神、岁运拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py` | 30 | 历史裸模块导入兼容导出，删除前需完成兼容账本移除条件 |
| `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py` | 1967 | 报告模板、章节渲染、品牌页脚拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/bot.py` | 1153+ | Bot 交互、命令解析、交付编排拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/main.py` | 980+ | API 路由、公共服务护栏、观测指标拆分 |
| `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` | 830 | 表单、工作台、Markdown 输出、页面元信息拆分 |
| `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py` | 1365 | pure-analysis 编排继续瘦身 |

## 发布判断

- 本地开发质量：PASS
- 企业仓库结构与本地发布链路：PASS
- 用户独立部署单实例候选：PASS
- 外部托管公网 live 发布：HITL，等待真实生产输入
