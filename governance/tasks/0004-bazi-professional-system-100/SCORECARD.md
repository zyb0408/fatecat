# FateCat 专业八字体系 100% Scorecard

更新时间：2026-06-16

## 口径

本任务的 `100%` 指专业八字体系达到可审查、可验证、可维护的工程与专业验收成熟度，不是预测命中率 100%，也不是宣称命理判断绝对正确。

达成 100% 必须同时满足：

- 10 个能力维度都有 `current`、`target gate`、`verify`、`falsifier`、`owner` 和 `next threshold`。
- 生产输出的专业结论都有 `sourceRuleId`、`evidenceFields`、`riskBoundary` 和反证条件。
- 高级格局、合化、用神、岁运和专题 profile 均有正例、反例、边界例和失败解释。
- MingLi-Bench / BaziQA 只作为样本外评测层，不作为生产排盘或规则真相源。
- 缺真实专家命例、标注或授权材料时，必须标为 `HITL/WARN`，不得编造样本补齐。

## 当前基线证据

| 证据项 | 当前值 | 来源 |
| --- | ---: | --- |
| 八字 rule-depth 规则 | 22 | `contracts/fate/rule_depth_registry.json` |
| 八字 classics 规则索引 | 43 | `contracts/fate/classics_rule_index.json` |
| 八字 coverage golden | 300 | `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json` |
| 八字 rule-depth golden | 8 | `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` |
| 八字 statement golden | 5 | `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` |
| 八字 calendar boundary golden | 9 | `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json` |
| MingLi full answered | 160 | `governance/tasks/0003-bazi-system-100/MINGLI_FULL_EVALUATION.md` |
| MingLi full correct | 45 | `governance/tasks/0003-bazi-system-100/MINGLI_FULL_EVALUATION.md` |
| MingLi full accuracy | 28.12% | `governance/tasks/0003-bazi-system-100/MINGLI_FULL_EVALUATION.md` |
| 当前任务树叶子节点 | 31 | `governance/tasks/0004-bazi-professional-system-100/TODO.md` |

## 完成度矩阵

| 维度 | current | target gate | verify | falsifier | owner | next threshold |
| --- | ---: | --- | --- | --- | --- | --- |
| 基础排盘 | 93% | 四柱、节气换月、立春年界、起运、真太阳时、早晚子时、跨时区边界均有 oracle 或 golden。 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_golden_coverage_matrix.py -q` | 任一边界样本缺 `source`、`expected`、`tolerance` 或 `failureExplanation`。 | `fate-core calendar` | calendar boundary case 覆盖节气秒级、立春、早晚子时、真太阳时、跨时区、DST、起运。 |
| 历法 / 时间边界 | 90% | `lunar-python` 是 production provider；oracle 只进入测试；依赖升级有差异归因。 | `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_fate_policy_assets.py -q` | `sxtwl`、`sxwnl`、`bazica`、`paipan` 等 oracle 被生产入口 import。 | `calendar provider` | 完成 `CalendarProvider` 升级合同和 oracle mismatch report。 |
| 证据化 / 可解释 | 88% | 报告/API 不出现无 `sourceRuleId` 的专业断语；所有 rule id 可回指 registry/classics。 | `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py tests/regression/test_api_contracts.py -q` | 报告出现未登记断语，或 rule id 无法回指规则来源。 | `fate-core evidence` | 所有专业段落补齐 `evidenceFields`、`score/weight`、`riskBoundary`、反证条件。 |
| 常规八字分析 | 84% | 强弱、月令、藏干、十神、五行、常规格局、干支关系和喜忌策略都有结构化字段和 golden。 | `.venv/bin/python -m pytest tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py -q` | 仍依赖不可追溯自然语言拼接，或核心字段缺失时测试仍通过。 | `regular evaluator` | 抽出 strength、ten-god、regular-pattern evaluator，并保持 API schema 稳定。 |
| 高级格局 | 72% | 正格、变格、从格、假从、专旺、化气均有成立条件、破格条件、反例和 lifecycle。 | `rg '从格|假从|专旺|化气|specialPattern' contracts/fate domains/fate-analysis -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 高级格局没有条件链或反例，却被报告强断为 production。 | `pattern evaluator` | 每类高级格局至少 1 正例、1 反例、1 边界例；缺专家样本保持 beta。 |
| 合化成败 | 76% | 合象、合而不化、成化、破化、争合、阻隔、冲破均有状态链和条件字段。 | `rg '合化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 只展示“合”而不区分成化/破化/阻隔，或缺反例仍标 Done。 | `hehua evaluator` | 输出 `structural_relation`、`transform_candidate`、`transform_success`、`transform_broken`。 |
| 用神裁决 | 78% | 调候、扶抑、通关、病药、格局用神并列评分，冲突裁决可解释。 | `rg '调候|扶抑|通关|病药|用神' contracts/fate governance/tasks -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q` | 报告/API 只输出单一用神结论且丢失策略冲突。 | `yongshen evaluator` | 建立 `scoredStrategies`、`ranking`、`conflicts`、`doesNotApplyWhen`。 |
| 岁运专题 | 70% | 大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业等 profile 联动。 | `rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers|topicProfiles' contracts domains/fate-analysis -n` | 输出确定未来、现实处方，或 profile 缺 evidence/riskBoundary。 | `fortune/topic evaluator` | 完成 fortune trigger matrix 与 topic profile 联合评分。 |
| Golden / 回归 | 86% | quick 只跑代表集；deep/release 跑 shard；新增规则均有正例、反例、边界例和 failureExplanation。 | `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q` | 全量慢测进入日常 quick，或失败 case 无法定位到规则/输入/期望。 | `QA/golden` | Golden shard policy 固化，高级规则和 topic fixtures 补齐。 |
| 样本外 benchmark | 45% | MingLi/BaziQA 评测链路成熟，predictions 无答案泄漏，分类失败有 owner 和回炉队列。 | `bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json` | 使用 expected answer、question_id、gold label 或人工改 prediction 文件刷分。 | `evaluation` | MingLi next：overall >= 32%、财运 >= 15%、婚姻 failures <= 25。 |

## 执行映射

| 维度 | 任务节点 |
| --- | --- |
| 基础排盘 | `TP-02.01`、`TP-02.03` |
| 历法 / 时间边界 | `TP-02.01`、`TP-02.02` |
| 证据化 / 可解释 | `TP-03.01`、`TP-03.02`、`TP-03.03` |
| 常规八字分析 | `TP-04.01`、`TP-04.02`、`TP-04.03` |
| 高级格局 | `TP-05.01`、`TP-05.02`、`TP-05.03` |
| 合化成败 | `TP-06.01`、`TP-06.02`、`TP-06.03` |
| 用神裁决 | `TP-07.01`、`TP-07.02`、`TP-07.03` |
| 岁运专题 | `TP-08.01`、`TP-08.02`、`TP-08.03` |
| Golden / 回归 | `TP-09.01` |
| 样本外 benchmark | `TP-09.02`、`TP-09.03`、`TP-09.04` |
| 维护与交付边界 | `TP-10.01`、`TP-10.02`、`TP-10.03` |

## TP-01.01 Gate 判定

- `每个维度有 current`：`PASS`
- `每个维度有 target gate`：`PASS`
- `每个维度有 verify`：`PASS`
- `每个维度有 falsifier`：`PASS`
- `每个维度有 owner`：`PASS`
- `每个维度有 next threshold`：`PASS`
