# FateCat 专业八字体系规则来源缺口台账

更新时间：2026-06-16

## 口径

本文件是 `TP-01.03` 的任务真相源：任何新增八字专业规则、evaluator、golden 或报告字段，都必须能回指这里的 gap、`contracts/fate/classics_rule_index.json` 或 `contracts/fate/rule_depth_registry.json`。

规则推进边界：

- 没有候选 `sourceRuleId` 的能力不得进入 production evaluator。
- 有候选规则但缺正例/反例/边界例时，只能进入 `beta`、`guarded` 或 `evidence_seed`。
- MingLi-Bench / BaziQA 失败样本只能驱动缺口归因，不得变成答案硬编码。
- license/source 不清的材料只能作为 `reference_only` 或 `HITL`，不得进入 runtime dependency。

## Gap Ledger

| Gap ID | 能力面 | 当前缺口 | 允许推进方式 | 不允许方式 | 对应任务 |
| --- | --- | --- | --- | --- | --- |
| `GAP-BZ-CALENDAR-001` | 基础排盘 / 历法时间 | 节气秒级、立春年界、早晚子时、真太阳时、跨时区、DST、起运边界样本仍不足。 | 增加 oracle/golden，写明 source、expected、tolerance、failureExplanation。 | 用单一库结果覆盖所有边界，或无法解释差异仍标绿。 | `TP-02.01`、`TP-02.02`、`TP-02.03` |
| `GAP-BZ-EVIDENCE-001` | 证据化 / 可解释 | 报告/API 仍可能出现无 `sourceRuleId`、无 `evidenceFields`、无 `riskBoundary` 的自然语言结论。 | 统一 evidence contract，补 ruleId coverage 和 policy regression。 | 把自然语言润色当作专业证据。 | `TP-03.01`、`TP-03.02`、`TP-03.03` |
| `GAP-BZ-REGULAR-001` | 常规八字分析 | 强弱、月令、十神、常规格局还需要 evaluator 边界和 golden 更稳定。 | 抽出 strength、ten-god、regular-pattern evaluator，保持 API schema 不变。 | 继续把常规规则堆入大函数或 delivery。 | `TP-04.01`、`TP-04.02`、`TP-04.03` |
| `GAP-BZ-PATTERN-001` | 高级格局 | 从格、假从、专旺、化气、变格缺完整成立条件、破格条件、正反例和专家样本。 | 建立 rule matrix、正反例 golden 和 guarded evaluator。 | 无 golden 即强断为 production。 | `TP-05.01`、`TP-05.02`、`TP-05.03` |
| `GAP-BZ-HEHUA-001` | 合化成败 | 合而不化、成化、破化、争合、阻隔、冲破缺统一状态链和反例矩阵。 | 拆成 `structural_relation`、`transform_candidate`、`transform_success`、`transform_broken`。 | 只输出“合化”自然语言结论。 | `TP-06.01`、`TP-06.02`、`TP-06.03` |
| `GAP-BZ-YONGSHEN-001` | 用神裁决 | 调候、扶抑、通关、病药、格局用神之间缺评分矩阵、冲突排序和不适用条件。 | 输出 `scoredStrategies`、`ranking`、`conflicts`、`doesNotApplyWhen`。 | 单一用神覆盖全部策略。 | `TP-07.01`、`TP-07.02`、`TP-07.03` |
| `GAP-BZ-FORTUNE-001` | 岁运触发 | 大运、流年、流月、伏吟反吟、天克地冲与原局关系缺联合 trigger chain。 | 只作趋势证据，接入 topic profile，禁止确定未来。 | 把动态触发写成确定事件。 | `TP-08.01` |
| `GAP-BZ-TOPIC-001` | 专题 profile | 婚姻、事业、财运、家庭、健康、学业等 profile 缺 score/basis/evidenceFields/riskBoundary 的稳定联合评分。 | 按专题建立 profile evaluator 和 policy regression。 | 用 benchmark 答案或关键词替代盘面证据。 | `TP-08.02`、`TP-08.03` |
| `GAP-BZ-GOLDEN-001` | Golden / 回归 | 高级规则、topic profile、用神冲突和合化反例样本不足；deep gate 需要分层。 | quick 代表集 + deep shard + release gate；新增规则必须有正反边界例。 | 把全量慢测塞进日常 quick，或失败无归因。 | `TP-09.01` |
| `GAP-BZ-BENCHMARK-001` | 样本外 benchmark | MingLi full 28.12% 只能证明链路可跑；分类失败多，BaziQA 尚未准入。 | MingLi full no-leak gate、failure taxonomy、BaziQA admission。 | 按 `question_id`、expected answer、gold label 刷分。 | `TP-09.02`、`TP-09.03`、`TP-09.04` |
| `GAP-BZ-MAINTAIN-001` | 维护与交付边界 | 大文件仍承担过多职责；新增规则若继续进入大函数会削弱长期维护性。 | 按 pattern/hehua/yongshen/fortune/topic 逐切片抽 evaluator。 | 大爆炸重写或在 delivery 新增领域算法。 | `TP-10.01`、`TP-10.02`、`TP-10.03` |

## Owner 能力面

| Owner | 负责 Gap | 关键证据 |
| --- | --- | --- |
| `fate-core calendar` | `GAP-BZ-CALENDAR-001` | calendar oracle、solar terms golden、base chart regression |
| `fate-core evidence` | `GAP-BZ-EVIDENCE-001` | rule-depth registry、classics index、API/report contract |
| `regular evaluator` | `GAP-BZ-REGULAR-001` | strength、ten-god、regular pattern fields |
| `pattern evaluator` | `GAP-BZ-PATTERN-001` | special pattern matrix、positive/negative golden |
| `hehua evaluator` | `GAP-BZ-HEHUA-001` | combine transform state machine |
| `yongshen evaluator` | `GAP-BZ-YONGSHEN-001` | strategy matrix、conflict ranking |
| `fortune/topic evaluator` | `GAP-BZ-FORTUNE-001`、`GAP-BZ-TOPIC-001` | fortune triggers、topicProfiles |
| `QA/golden` | `GAP-BZ-GOLDEN-001` | shard/deep gate、failureExplanation |
| `evaluation` | `GAP-BZ-BENCHMARK-001` | MingLi/BaziQA predictions、taxonomy、no-leak gate |
| `architecture` | `GAP-BZ-MAINTAIN-001` | evaluator extraction、delivery boundary |

## TP-01.03 Gate 判定

- `高级格局有 gap id`：`PASS`，`GAP-BZ-PATTERN-001`
- `合化有 gap id`：`PASS`，`GAP-BZ-HEHUA-001`
- `用神有 gap id`：`PASS`，`GAP-BZ-YONGSHEN-001`
- `岁运有 gap id`：`PASS`，`GAP-BZ-FORTUNE-001`
- `专题有 gap id`：`PASS`，`GAP-BZ-TOPIC-001`
- `benchmark 有 gap id`：`PASS`，`GAP-BZ-BENCHMARK-001`
