---
id: DATA-GOVERNANCE-README
type: data-governance
status: active
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P90D
---

# Data Governance

FateCat 数据资产包括字段 profile、capability 契约、golden fixtures、经典文本、历法表和 vendor manifest。

## 规则

- raw 私有资料不进 Git，不进导出包。
- golden fixture 必须有来源、生成方式和回归测试。
- 数据契约迁入 `contracts/` 后，服务只消费契约，不在交付层重复定义字段口径。
