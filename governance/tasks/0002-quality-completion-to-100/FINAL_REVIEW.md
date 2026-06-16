# Final Six-Dimension Review

日期：2026-06-16

## Verdict

结论：`WARN / HITL`。

本轮已经把 v2 六维任务树 Wave 1-4 全部执行并落盘证据。当前仓库具备本地自托管、单实例独立部署、容器 smoke 和静态生产准入能力；但不能诚实声明“企业长期生产稳定 100%”或“命理专业完整度 100%”。

## Evidence Summary

| Evidence | Result |
| --- | --- |
| active-only principle gate | PASS：`finding_count=0` |
| task docs decompose validation | PASS：`ok=true` |
| quick local CI | PASS：证据 `/tmp/fatecat-local-ci-20260616013124` |
| all local CI | PASS：证据 `/tmp/fatecat-local-ci-20260616012307` |
| full pytest in all CI | PASS：`169 passed, 1 skipped in 247.47s` |
| full 300+ golden release gate | PASS/WARN：`9 passed in 2211.71s (0:36:51)`；已补 shard selector 合同 |
| MingLi FateCat prediction eval | PASS/WARN：sample 10 answered `10/10`，accuracy `30%`；sample 2 smoke `2/2` |
| Bot outbox local recovery | PASS：`2 passed in 0.44s` |
| Docker/container smoke | PASS：container `/web` smoke OK |
| public-service static readiness | PASS/HITL：static PASS；live API/Bot SKIP |

## Six-Dimension Matrix

| Dimension | Status | Evidence | Remaining Risk |
| --- | --- | --- | --- |
| 满足约束 | PASS | local-ci all, active principle gate, HITL boundary docs | 真实公网 API/Bot live 仍需外部 URL/token。 |
| 可解释 | PASS/WARN | rule/risk tests, policy assets, report/API/Web tests | 高级专题推理和 MingLi 准确率仍不足。 |
| 可测试 | PASS | quick/all CI, full golden, API/Web/Bot/outbox tests | full golden 36m51s，需优化为可观测 deep gate。 |
| 可维护 | WARN | active principle gate PASS, compatibility classification, line-count map | 仍有 2500/1941/1375/1152/1015 行级核心大文件。 |
| 处理特殊情况 | PASS/HITL | API 4xx/5xx/503/429、calendar/oracle、Bot outbox | live Bot/API 需要真实环境；多副本仍需外部限流设施。 |
| 复用建立在理解上 | PASS | vendor-health, capability/provider tests, manifest boundaries | reference/oracle 材料继续受 license/audit gate 限制。 |

## BLOCK

无 active 本地门禁 BLOCK。

## WARN

- `TP-11.01`：full 300+ golden release gate 通过但耗时 `36m51s`；已补 shard selector，但仍只能作为 deep/release gate。
- `TP-11.02`：FateCat-generated MingLi scored baseline 链路通过，但 sample 10 accuracy 只有 `30%`；不能宣称专业样本外能力达标。
- `TP-12.02`：核心大文件仍偏大，维护性不能宣称 100%。

## HITL

- 真实公网 API：需要真实 HTTPS URL、TLS/反向代理、生产 CORS allowlist。
- 真实 Telegram Bot：需要真实 `FATE_BOT_TOKEN`，并运行 `production-readiness.sh --api-url <real-url> --require-live-bot`。

## Decision

允许作为本地独立部署单实例候选继续使用。

不允许声明：

- 托管公网 live 生产已通过。
- 命理专业完整度 100%。
- 长期维护性 100%。
- MingLi-Bench 样本外推理准确率达标。
