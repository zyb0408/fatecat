# TP-03.01 RuleId Coverage Force Gate

## Status

- Result: `PASS`
- Scope: ruleId 覆盖强制门禁。
- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q`

## Evidence

- Combined TP-03 command result: `85 passed in 71.22s`.
- `tests/regression/test_bazi_ziwei_rule_depth.py` 检查：
  - production rule depth 输出必须有 `ruleId` / `sourceRuleId`。
  - emitted rule id 必须回指 classics registry。
  - applied rules、combination statements、topic/fortune/yongshen 输出必须带 rule/evidence/risk 字段。
- `tests/regression/test_fate_policy_assets.py` 检查：
  - policy schema 要求 `ruleIds`、`riskBoundary`、`evidenceFields`、`sourceRuleIds`。
  - policy registry 中 source rule id 必须落在 classics rule 集合内。

## Gate Decision

- production 断语 ruleId 门禁：`PASS`
- classics registry 回指：`PASS`
- policy asset rule source 约束：`PASS`

## Remaining Boundary

- 该 gate 证明 ruleId 和 policy schema 已接入测试。
- 它不证明高级格局、合化、用神、岁运专题已经专业 100%；这些仍由 `TP-05` 到 `TP-08` 分别推进。
