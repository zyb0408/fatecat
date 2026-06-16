# FateCat 八字规则来源覆盖矩阵

更新时间：2026-06-16

## 口径

本文件只登记规则来源覆盖和缺口，不新增生产断语。

- `sourceRuleId` 必须来自 `contracts/fate/classics_rule_index.json` 或 `contracts/fate/rule_depth_registry.json`。
- 规则来源只保留短摘要、条件和证据字段，不复制大段典籍原文。
- 没有候选 `sourceRuleId` 的能力不得进入 evaluator 实现。
- 有候选规则但缺 golden/反例/专家命例时，只能进入 `beta`、`evidence_seed` 或 `guarded` 状态。

## 规则资产概览

| 资产 | 总规则 | 八字规则 | 用途 |
| --- | ---: | ---: | --- |
| `contracts/fate/classics_rule_index.json` | 98 | 43 | 短规则来源索引、sourceRuleId 真相源。 |
| `contracts/fate/rule_depth_registry.json` | 44 | 22 | evaluator 深度规则、证据字段、冲突策略和风险边界。 |

## 专业能力来源矩阵

| 能力面 | 当前目标节点 | 候选 sourceRuleId | 当前可实现层级 | 缺口 |
| --- | --- | --- | --- | --- |
| 基础排盘与时间边界 | `TP-02` | `bazi.true_solar_time_pipeline`, `bazi.zi_time_boundary`, `bazi.solar_term_month_boundary`, `bazi.lichun_year_boundary`, `bazi.fortune_start_boundary` | production/golden | 需要扩展更多节气交界、早晚子时、跨时区、DST 和起运边界样本。 |
| 日主强弱 | `TP-03` 前置 | `bazi.day_master_strength`, `bazi.month_command_priority`, `bazi.renyuan_siling_weight`, `bazi.strength_score_golden`, `bazi.depth.strength.month_root_transparency` | production candidate | 需要把 strength score 与高级格局/用神裁决的冲突策略继续解耦。 |
| 常规格局 | `TP-03.01` | `bazi.pattern_by_month_command`, `bazi.pattern_root_transparency`, `bazi.depth.pattern.establishment`, `bazi.depth.pattern.finance_official_seal_food_matrix` | guarded evaluator | 需要正格/财官印食格局的正例、破格例和月令透藏反例。 |
| 高级格局 | `TP-03.01`、`TP-03.02`、`TP-03.03` | `bazi.depth.pattern.regular_vs_special`, `bazi.depth.pattern.follow_transform_guard`, `bazi.depth.pattern.special_pattern_checklist`, `bazi.pattern_by_month_command`, `bazi.pattern_root_transparency` | beta/evidence_seed | 从格、假从、化气、专旺仍缺足量匿名命例 golden；缺完整成败条件时不得强断。 |
| 合化成败 | `TP-04.01`、`TP-04.02`、`TP-04.03` | `bazi.stem_branch_relations`, `bazi.ganzhi_priority`, `bazi.depth.relation.combine_transform_guard`, `bazi.depth.relation.collision_priority`, `bazi.depth.relation.punishment_harm_break_matrix` | guarded evaluator | 需要月令、透干、通根、得令、阻隔、帮扶、冲破、争合的反例矩阵。 |
| 用神策略 | `TP-05.01`、`TP-05.02`、`TP-05.03` | `bazi.regulating_climate`, `bazi.balance_five_elements`, `bazi.yongshen_strategy`, `bazi.pattern_use_god_trace`, `bazi.depth.yongshen.strategy_matrix`, `bazi.depth.yongshen.tiaohou_priority`, `bazi.depth.yongshen.climate_detail_matrix`, `bazi.depth.climate.seasonal_adjustment` | guarded evaluator | 调候、扶抑、通关、病药的冲突裁决仍需评分矩阵、反例和报告字段。 |
| 十神结构 | `TP-06.02` | `bazi.ten_god_structure`, `bazi.depth.tengod.structure_profile`, `bazi.depth.tengod.overlap_profile`, `bazi.depth.tengod.role_family_matrix` | production candidate | 需要把十神族群映射到事业、财运、婚姻、家庭、性格 profile，不输出孤立断语。 |
| 岁运触发 | `TP-06.01` | `bazi.fortune_trigger_boundary`, `bazi.fortune_start_boundary`, `bazi.depth.fortune.trigger_chain`, `bazi.depth.fortune.month_trigger`, `bazi.depth.fortune.decade_year_month_order` | guarded evaluator | 需要大运/流年/流月触发与原局关系的样本；动态触发只能作趋势证据。 |
| 专题 profile | `TP-06.02`、`TP-06.03` | `bazi.topic_profile_boundary`, `bazi.depth.statement.combination_boundary`, `bazi.depth.statement.narrative_markdown`, `bazi.ten_god_structure`, `bazi.depth.tengod.role_family_matrix` | beta/evidence_seed | 事业、财运、婚姻、健康、学业、迁移、家庭需要各自 score/basis/evidenceFields/riskBoundary。 |
| 报告边界 | `TP-08` | `bazi.topic_profile_boundary`, `bazi.spirits_auxiliary_only`, `bazi.depth.auxiliary.boundary_guard`, `bazi.depth.statement.combination_boundary`, `bazi.depth.statement.narrative_markdown` | production guardrail | 需要所有高风险专题回归测试覆盖非医疗、非金融、非法律、非心理替代建议。 |
| 样本外评测 | `TP-07` | `bazi.topic_profile_boundary`, `bazi.depth.fortune.trigger_chain`, `bazi.depth.statement.narrative_markdown` | evaluation_only | MingLi-Bench 不提供生产规则来源，只提供分类失败反馈；不得答案泄漏。 |

## Gap Ledger

| Gap ID | 能力面 | 当前缺口 | 允许推进方式 | 不允许方式 |
| --- | --- | --- | --- | --- |
| `GAP-BZ-PATTERN-001` | 高级格局 | 从格、假从、化气、专旺缺足量匿名命例 golden 和破格反例。 | 先落 `candidate/guarded/evidence_seed`，补正反例后提升。 | 无 golden 即强断为 production。 |
| `GAP-BZ-HEHUA-001` | 合化成败 | 缺成化/破化/阻隔/争合的统一条件链和反例矩阵。 | 先把状态拆成 `structural_relation`、`transform_candidate`、`transform_success`、`transform_broken`。 | 只写“合化”自然语言结论。 |
| `GAP-BZ-YONGSHEN-001` | 用神裁决 | 调候、扶抑、通关、病药之间缺冲突排序和权重理由。 | 建立 strategy matrix，报告保留并列策略。 | 单一用神覆盖全部策略。 |
| `GAP-BZ-FORTUNE-001` | 岁运专题 | 动态触发缺和原局、格局、用神、十神的联合评分。 | 只作趋势证据，进入 topic profile。 | 输出确定未来事件。 |
| `GAP-BZ-TOPIC-001` | 专题 profile | MingLi 分类多，但每个专题缺 score/basis/evidenceFields/riskBoundary。 | 按婚姻、事业、家庭、健康、财运优先拆 profile。 | 把 benchmark 答案写回生产规则。 |
| `GAP-BZ-CALENDAR-001` | 时间边界 | calendar boundary 当前只有 4 个样本。 | 增加节气、立春、早晚子时、真太阳时、跨时区样本。 | 用单一库结果覆盖所有边界。 |
| `GAP-BZ-REPORT-001` | 报告边界 | 高风险专题需要字段和文案回归。 | 接入 policy assets 和 API/Web/Markdown 测试。 | 输出医疗、金融、法律或心理替代建议。 |

## 实现前硬规则

- 新 evaluator 先引用本文件中的候选 `sourceRuleId`，再进入 `rule_depth_registry` 或代码。
- 新 golden 必须写明 source、expected、failureExplanation 和 privacy/license 边界。
- 新报告字段必须保留 evidence/riskBoundary，不允许只加自然语言段落。
- `MingLi-Bench` 失败样本只能驱动缺口归因，不能驱动答案硬编码。

## TP-01.02 Gate 判定

`TP-01.02` 完成条件：

- 高级格局、合化、用神、岁运、专题 profile、报告边界均有候选 `sourceRuleId`。
- 缺口全部进入 Gap Ledger。
- 缺失来源不能进入实现。
- 规则来源只保留短摘要和条件。

