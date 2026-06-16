# TP-03.02 Evidence CounterEvidence Schema Gate

## Status

- Result: `PASS`
- Scope: evidence/counterEvidence schema 门禁。
- Verify: `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q`

## Evidence

- Combined TP-03 command result: `85 passed in 71.22s`.
- `tests/regression/test_api_contracts.py` 检查：
  - pattern、special pattern、combine、yongshen、fortune/topic 输出必须有 `riskBoundary`。
  - strategy、candidate、conflict、matrix 输出必须有 `evidenceFields`、`counterEvidence` 或 `doesNotApplyWhen`。
- `tests/regression/test_capability_protocol.py` 检查：
  - capability evidence 按 `analysisEvidence` / `ruleIds` 进入协议层。
  - bazi、ziwei、meihua、almanac 能力不丢失 evidence envelope。

## Gate Decision

- API 专业段落 evidence schema：`PASS`
- counterEvidence / doesNotApplyWhen schema：`PASS`
- riskBoundary schema：`PASS`
- capability protocol evidence envelope：`PASS`

## Remaining Boundary

- 该 gate 证明消费者协议不再是纯自然语言空壳。
- `TP-03.03` 仍必须跑高风险输出 policy gate，避免确定未来、现实处方或恐吓式断语进入报告。
