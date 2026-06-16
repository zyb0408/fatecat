# Closeout

日期：2026-06-16

## Status

`Closed with WARN/HITL` for v2 execution waves.

旧 `TODO.md` 仍是原七维任务树，不强行勾选为 Done；本轮实际执行对象是 `SYSTEMIC_IMPROVEMENT_PLAN.md` 的六维 v2 覆盖层，证据分别落在：

- `WAVE1_EXECUTION.md`
- `WAVE2_EXECUTION.md`
- `WAVE3_EXECUTION.md`
- `WAVE4_EXECUTION.md`
- `FINAL_REVIEW.md`

## Completed

- Wave 1：工作树切分、HITL 边界、rule/risk 审计、vendor health。
- Wave 2：API contract、rule registry、active principle gate、compatibility 分类、provider/adapter、reference/oracle 隔离。
- Wave 3：Web/branding/API、calendar/oracle/golden、full 300+ golden release gate、operability。
- Wave 4：FateCat-generated MingLi prediction eval、本地 all CI、big-file map、Bot outbox。
- Wave 5：最终六维审查、WARN/HITL 收口。

## Latest Gates

- `bash scripts/local-ci.sh --profile quick` -> PASS，`/tmp/fatecat-local-ci-20260616013124`
- `bash scripts/local-ci.sh --profile all` -> PASS，`/tmp/fatecat-local-ci-20260616012307`
- active-only principle gate -> PASS，`finding_count=0`
- task docs decompose validation -> PASS，`ok=true`
- diff whitespace check -> PASS

## Remaining Work

| Type | Item | Required Next Step |
| --- | --- | --- |
| WARN | full golden 过慢 | 已加 shard selector；继续补 case timing、失败定位和并行执行；保持 release/deep-only。 |
| WARN | MingLi sample 10 accuracy 30% | 建设真正的专题推理器和样本外评测，不用弱关键词 baseline 冒充能力。 |
| WARN | 核心大文件 | 继续拆 `bazi_calculator.py`、`report_generator.py`、`calculate_pure_analysis.py`、`bot.py`、`main.py`。 |
| HITL | 真实公网 API/Bot live | 提供真实 URL/TLS/Bot token 后运行 `production-readiness.sh --api-url <real-url> --require-live-bot`。 |

## Final Statement

本轮没有发现 active 本地门禁 BLOCK。当前可交付结论是：本地自托管单实例候选可用，六维质量证据已补齐到可审查状态；剩余 WARN/HITL 不允许被写成无条件 100%。
