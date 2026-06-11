---
id: BASELINE-GATE-NEGATIVE-TEST-SUITE-FATECAT
type: baseline-gate-negative-test-suite
status: active
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P30D
---

# Baseline Gate Negative Test Suite

## Required Negative Tests

| Negative case | Gate | Expected result | Status |
| --- | --- | --- | --- |
| 新增 active `scripts/project` fallback | structure guard | BLOCK | TODO |
| 导出包包含 `.env` | export hygiene | BLOCK | existing gate, needs new path coverage |
| 导出包包含 `.db` / `.sqlite` | export hygiene | BLOCK | existing gate, needs new path coverage |
| raw 私有资料进入 Git | source hygiene | BLOCK | existing gate, needs new path coverage |
| 非北京真实地区样例进入第一方前端 | privacy fixtures | BLOCK | existing gate, needs new path coverage |
| service 缺少 `service.yaml` | structure gate | BLOCK | TODO |
| governance 缺 required frontmatter | governance strict validate | BLOCK/WARN | existing validator |

## Next

Phase 1 需要把上述负例接入 `scripts/check-structure.sh` 或等价结构门禁，再纳入 `scripts/acceptance.sh`。
