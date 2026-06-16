# TP-01.03 Ten Dimension 100% Gate Contract

## Status

- Result: `PASS`
- Scope: 写入十维 100% gate 合同。
- Verify: `rg '100% 不是|100% 是|falsifier|target gate' governance/tasks/0005-bazi-capability-100-roadmap -n`

## 100% 不是

- 100% 不是预测准确率 100%。
- 100% 不是专业推理满分。
- 100% 不是输出确定未来。
- 100% 不是把 benchmark 题库答案刷高。
- 100% 不是把 oracle、评测集或参考仓接入生产 runtime。

## 100% 是

- 100% 是每个能力维度都有 source、schema、evidence、counterEvidence、riskBoundary、golden、regression 和 release gate。
- 100% 是所有生产输出都可追溯、可反证、可测试、可回滚。
- 100% 是缺专家样本或授权材料时保持 beta/HITL/WARN，而不是编造样本。
- 100% 是 benchmark no-leak、失败可归因、规则可回炉。

## Ten Dimension Gate Matrix

| Dimension | Current | target gate | Verify | falsifier |
| --- | ---: | --- | --- | --- |
| 基础排盘 | 93% | 四柱、节气换月、立春年界、起运、真太阳时、早晚子时、跨时区、DST 均有 oracle/golden/mismatch 解释。 | `tests/regression/test_calendar_oracle_contract.py`、`tests/regression/test_solar_terms_golden.py`、`tests/regression/test_bazi_golden_coverage_matrix.py` | 任一边界样本缺 source、expected、tolerance、failureExplanation；或 provider/oracle 差异不可解释仍标绿。 |
| 历法 / 时间边界 | 90% | `lunar-python` provider、oracle-only 对照、依赖升级和回滚合同齐备。 | calendar oracle regression + dependency boundary scan | `sxtwl/sxwnl/paipan/bazica` 被生产入口 import。 |
| 证据化 / 可解释 | 88% | 所有 production 专业断语都有 `sourceRuleId`、`evidenceFields`、`counterEvidence`、`riskBoundary`。 | rule-depth/API/policy regression | 报告或 API 出现未登记 ruleId 或无证据自然语言断语。 |
| 常规八字分析 | 84% | strength、ten-god、regular-pattern、relation evaluator 独立，schema 稳定，golden 覆盖正反边界。 | rule-depth、API、statement golden | 常规规则仍堆在大函数或 delivery；核心字段缺失测试仍绿。 |
| 高级格局 | 72% | 正格、变格、从格、假从、专旺、化气均有 taxonomy、appliesWhen、doesNotApplyWhen、正反边界例和 lifecycle。 | rg taxonomy + rule-depth/golden/API tests | 无专家样本或无反例却 production 强断高级格局。 |
| 合化成败 | 76% | 合象、合而不化、成化、破化、争合、阻隔、冲破有统一状态链和 condition failure。 | transform state regression + counterexample matrix | 只输出“合化”自然语言，不区分成败和反证。 |
| 用神裁决 | 78% | 调候、扶抑、通关、病药、格局用神并列评分，输出 ranking/conflicts/doesNotApplyWhen。 | yongshen rule-depth/API/golden regression | 报告只输出单一绝对用神或丢失策略冲突。 |
| 岁运专题 | 70% | 大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业 profile 联合评分，且只作趋势证据。 | fortune/topic rule-depth/API/policy regression | 输出确定未来、现实处方、恐吓式断语或缺 riskBoundary。 |
| Golden / 回归 | 86% | quick/deep/release 分层；calendar>=50，rule-depth>=120，statement>=80，P0 topic 每类>=20；deep shard 0..3 可复现。 | corpus count + shard release gate | 全量慢测进入日常 quick；新增规则无正反边界例或 failureExplanation。 |
| 样本外 benchmark | 45% | MingLi full answered=160/160 且 no-leak；BaziQA admission 明确；failure taxonomy 回炉到规则 backlog。 | MingLi full scripts + no-leak scan + BaziQA admission | 使用 expected/answer/correct/gold/label、question_id 或选项文本硬编码刷分。 |

## Implementation Guardrails

- 每个后续 leaf 只能提升一个能力切片，不做大爆炸重写。
- 每个 production 规则必须先有 rule contract，再有 evaluator，再有 golden，再进报告/API。
- 每个 benchmark 改动必须先跑 no-leak gate。
- 每个高风险 topic 必须先加 policy regression，再允许报告展示。

## Gate Decision

- 十维 current：`PASS`
- 十维 target gate：`PASS`
- 十维 verify：`PASS`
- 十维 falsifier：`PASS`
- 100% 口径不等于预测准确率：`PASS`
