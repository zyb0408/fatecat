# Task Overview
- Task ID: `0004`
- Slug: `bazi-professional-system-100`
- Objective: `把 FateCat 八字体系从当前工程可验收状态推进到专业八字体系 100% 验收口径：基础排盘、历法时间、证据解释、常规分析、高级格局、合化成败、用神裁决、岁运专题、Golden 回归和样本外 benchmark 全部具备可追溯规则、可验证测试、失败边界和发布门禁。`
- Status: `In Progress`

## In Scope
- 以现有 fate-core、contracts/fate、data-products/bazi、MingLi evaluation 和 regression tests 为主线推进八字专业体系。
- 把 10 个完成度维度全部转成可执行任务、verify 命令、gate、输出物和失败边界。
- 保留 lunar-python 为生产历法底座，sxtwl/bazica/sxwnl/paipan 只作为 oracle 或 reference，不进入生产请求链路。
- 新增或升级规则必须进入 registry/evaluator/golden/report contract，不能只写自然语言报告。
- MingLi-Bench/BaziQA 只用于离线样本外评测和失败归因，不作为生产规则来源。

## Out of Scope
- 不宣称预测命中率 100%。本任务的 100% 指工程和专业验收闭环成熟。
- 不把健康、财务、法律、心理等高风险专题输出成现实处方或确定未来。
- 不引入单一新开源库替换现有八字主链，除非先通过 license、oracle、golden 和回滚审查。
- 不做大爆炸重写；每次只迁移一个 evaluator 或规则切片。
- 不把 benchmark expected answer、question_id 或选项文本硬编码进预测逻辑。

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 锁定 100% Scorecard 与资源边界
  │  ├─ TP-01.01 [leaf] [P0] 刷新八字 100% Scorecard
  │  ├─ TP-01.02 [leaf] [P0] 刷新资源地图和复用边界
  │  └─ TP-01.03 [leaf] [P0] 建立规则来源缺口台账
  ├─ TP-02 [branch] [P0] 基础排盘与历法时间边界 100%
  │  ├─ TP-02.01 [leaf] [P0] 扩展 calendar boundary matrix
  │  ├─ TP-02.02 [leaf] [P0] 锁定 CalendarProvider 升级合同
  │  └─ TP-02.03 [leaf] [P0] 基础排盘回归矩阵
  ├─ TP-03 [branch] [P0] 证据化与可解释 100%
  │  ├─ TP-03.01 [leaf] [P0] 补齐 ruleId 覆盖审计
  │  ├─ TP-03.02 [leaf] [P0] 标准化 evidenceFields 合同
  │  └─ TP-03.03 [leaf] [P0] 高风险输出边界回归
  ├─ TP-04 [branch] [P0] 常规八字分析 100%
  │  ├─ TP-04.01 [leaf] [P0] 强弱与月令 evaluator
  │  ├─ TP-04.02 [leaf] [P0] 十神结构 evaluator
  │  └─ TP-04.03 [leaf] [P0] 常规格局 evaluator
  ├─ TP-05 [branch] [P0] 高级格局 100%
  │  ├─ TP-05.01 [leaf] [P0] 高级格局规则矩阵
  │  ├─ TP-05.02 [leaf] [P0] 高级格局正反例 golden
  │  └─ TP-05.03 [leaf] [P0] 高级格局 evaluator
  ├─ TP-06 [branch] [P0] 合化成败 100%
  │  ├─ TP-06.01 [leaf] [P0] 干支关系条件目录
  │  ├─ TP-06.02 [leaf] [P0] 合化状态链 evaluator
  │  └─ TP-06.03 [leaf] [P0] 合化反例矩阵
  ├─ TP-07 [branch] [P0] 用神裁决 100%
  │  ├─ TP-07.01 [leaf] [P0] 用神策略矩阵
  │  ├─ TP-07.02 [leaf] [P0] 用神决策 evaluator
  │  └─ TP-07.03 [leaf] [P0] 用神冲突正反例
  ├─ TP-08 [branch] [P0] 岁运专题 100%
  │  ├─ TP-08.01 [leaf] [P0] 岁运触发矩阵
  │  ├─ TP-08.02 [leaf] [P0] 专题 profile 联合评分
  │  └─ TP-08.03 [leaf] [P0] 专题风险边界
  ├─ TP-09 [branch] [P0] Golden 回归与样本外 Benchmark 100%
  │  ├─ TP-09.01 [leaf] [P0] Golden shard 与 deep gate
  │  ├─ TP-09.02 [leaf] [P0] MingLi full 评测门禁
  │  ├─ TP-09.03 [leaf] [P1] BaziQA 纳入评测审查
  │  └─ TP-09.04 [leaf] [P0] 失败归因回炉到规则任务
  └─ TP-10 [branch] [P0] 维护性、交付边界与最终发布门禁
     ├─ TP-10.01 [leaf] [P1] evaluator 物理拆分
     ├─ TP-10.02 [leaf] [P0] 报告字段与 Markdown 边界收口
     └─ TP-10.03 [leaf] [P0] 最终本地门禁与审查

## Requirement Alignment
- 目标: 把 FateCat 八字体系从当前工程可验收状态推进到专业八字体系 100% 验收口径：基础排盘、历法时间、证据解释、常规分析、高级格局、合化成败、用神裁决、岁运专题、Golden 回归和样本外 benchmark 全部具备可追溯规则、可验证测试、失败边界和发布门禁。
- approved plan 顶层步骤数: 10
- 编译后节点总数: 41
- 编译后叶子节点数: 31
- 对齐项: 用户要求使用 auto-tasks 设计把八字体系推进到 100% 的落地计划，并以任务树作为执行框架。
- 对齐项: 当前口径来自上一轮汇报：基础排盘 93%、历法/时间边界 90%、证据化 88%、常规分析 84%、高级格局 72%、合化成败 76%、用神裁决 78%、岁运专题 70%、Golden/回归 86%、样本外 benchmark 45%。
- 对齐项: 本计划把百分比转成可执行 gate，不把聊天评分当成完成证据。
- 计划摘要: 按终态倒推：先锁定 100% scorecard 和资源边界，再补基础历法、证据契约、常规分析、高级格局、合化、用神、岁运专题、golden benchmark，最后做维护性拆分和 release review。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 把当前完成度表转成不可混淆的工程验收标准、资源角色和禁止路径。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 把 10 个维度的当前值、目标 gate、verify、falsifier、owner 和下一门槛写成任务真相源。 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 确认 lunar-python、sxtwl、bazica、sxwnl、paipan、MingLi-Bench、BaziQA、bazi-1 的 usageRole 和禁止用途。 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 2 | No | No | 把缺规则、缺反例、缺专家样本、缺 license、缺 evaluator 的能力统一进入 gap ledger。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | No | 补齐基础排盘和时间边界的 oracle、golden、依赖升级门禁和差异归因。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | Yes | 补节气秒级、立春年界、早晚子时、真太阳时、跨时区、DST、起运边界样本。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | Yes | 明确 lunar-python 是 production provider，oracle 资源只在测试中使用，依赖升级必须跑指定门禁。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-01.03, TP-02.01, TP-02.02 | 4 | No | No | 把四柱、五行、十神、藏干、起运、真太阳时基础字段纳入稳定回归。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | No | 让 API、Markdown 和 rule-depth 输出的每个专业结论都能追溯到规则、字段、权重和风险边界。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | Yes | 检查报告/API 中所有专业断语是否都有 sourceRuleId 或明确 unsupported/beta 边界。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | Yes | 把 sourceRuleId、evidenceFields、score、weight、doesNotApplyWhen、riskBoundary 做成统一字段契约。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-01.03, TP-03.01, TP-03.02 | 4 | No | No | 锁定健康、财运、灾劫、官非等专题不能输出现实处方、恐吓或保证式判断。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-02.03, TP-03.02 | - | No | No | 把强弱、月令、十神、藏干、五行、常规格局和干支关系做成稳定 evaluator 与 golden。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-02.03, TP-03.02 | 5 | No | Yes | 独立强弱评分、月令、人元司令、通根透干和旺衰证据，避免散落在大函数里。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-02.03, TP-03.02 | 5 | No | Yes | 结构化透干、藏干、十神数量、十神组合和十神族群映射。 |
| TP-04.03 | TP-04 | 2 | P0 | action | Yes | TP-02.03, TP-03.02, TP-04.01, TP-04.02 | 6 | No | No | 覆盖财官印食等常规格局候选、成立依据、破格条件和不确定原因。 |
| TP-05 | ROOT | 1 | P0 | package | No | TP-04.03 | - | No | No | 把从格、假从、化气、专旺、变格等高级格局从 beta 候选推进到 guarded/production 可审查状态。 |
| TP-05.01 | TP-05 | 2 | P0 | action | Yes | TP-04.03 | 7 | No | Yes | 为从格、假从、专旺、化气、变格建立 appliesWhen、doesNotApplyWhen、破格条件和 sourceRuleId。 |
| TP-05.02 | TP-05 | 2 | P0 | action | Yes | TP-04.03 | 7 | No | Yes | 为每个高级格局补正例、反例、边界例和 failureExplanation。 |
| TP-05.03 | TP-05 | 2 | P0 | action | Yes | TP-04.03, TP-05.01, TP-05.02 | 8 | No | No | 实现或抽取高级格局 evaluator，输出候选、置信度、破格原因和风险边界。 |
| TP-06 | ROOT | 1 | P0 | package | No | TP-04.03 | - | No | No | 把干支合化从自然语言关系升级为有条件链、状态机和反例矩阵的 evaluator。 |
| TP-06.01 | TP-06 | 2 | P0 | action | Yes | TP-04.03 | 7 | No | Yes | 登记天干五合、地支六合、三合、三会、冲刑害破、争合、阻隔、冲破的条件字段。 |
| TP-06.02 | TP-06 | 2 | P0 | action | Yes | TP-04.03, TP-06.01 | 8 | No | No | 输出 structural_relation、transform_candidate、transform_success、transform_broken。 |
| TP-06.03 | TP-06 | 2 | P0 | action | Yes | TP-04.03, TP-06.02 | 9 | No | No | 补月令、透干、通根、得令、帮扶、冲破、阻隔导致不成化的反例。 |
| TP-07 | ROOT | 1 | P0 | package | No | TP-04.01, TP-04.03, TP-06.03 | - | No | No | 把调候、扶抑、通关、病药从并列描述升级为可冲突裁决的评分矩阵。 |
| TP-07.01 | TP-07 | 2 | P0 | action | Yes | TP-04.01, TP-04.03, TP-06.03 | 10 | No | Yes | 定义调候、扶抑、通关、病药、格局用神的输入字段、评分、冲突和不适用条件。 |
| TP-07.02 | TP-07 | 2 | P0 | action | Yes | TP-04.01, TP-04.03, TP-06.03, TP-07.01 | 11 | No | No | 输出 scoredStrategies、ranking、conflicts、selectedCandidates、riskBoundary。 |
| TP-07.03 | TP-07 | 2 | P0 | action | Yes | TP-04.01, TP-04.03, TP-06.03, TP-07.02 | 12 | No | No | 补寒暖燥湿、身强身弱、格局优先、通关病药冲突场景的 golden。 |
| TP-08 | ROOT | 1 | P0 | package | No | TP-04.02, TP-05.03, TP-07.03 | - | No | No | 把大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业等专题 profile 联动。 |
| TP-08.01 | TP-08 | 2 | P0 | action | Yes | TP-04.02, TP-05.03, TP-07.03 | 13 | No | Yes | 定义大运、流年、流月、伏吟反吟、天克地冲、刑冲合害与原局关系的 trigger chain。 |
| TP-08.02 | TP-08 | 2 | P0 | action | Yes | TP-04.02, TP-05.03, TP-07.03, TP-08.01 | 14 | No | No | 为婚姻、事业、财运、家庭、健康、学业、迁移建立 score、basis、scoreBasis、evidenceFields、lifecycle。 |
| TP-08.03 | TP-08 | 2 | P0 | action | Yes | TP-04.02, TP-05.03, TP-07.03, TP-08.02 | 15 | No | No | 针对健康、财运、灾劫、官非等高风险专题补安全文案和 policy 测试。 |
| TP-09 | ROOT | 1 | P0 | package | No | TP-08.03 | - | No | No | 把规则样本、deep gate、MingLi/BaziQA 评测和失败归因做成可持续改进系统。 |
| TP-09.01 | TP-09 | 2 | P0 | action | Yes | TP-08.03 | 16 | No | Yes | 把 quick 代表集、deep 300+ matrix、rule-depth、calendar boundary 和 topic fixtures 分层。 |
| TP-09.02 | TP-09 | 2 | P0 | action | Yes | TP-08.03 | 16 | No | Yes | 持续生成 160 题 predictions、report、byCategory 和 failure taxonomy，且无答案泄漏。 |
| TP-09.03 | TP-09 | 2 | P1 | action | Yes | TP-08.03 | 16 | No | Yes | 审查 BaziQA license、题型、输入输出契约和是否可作为 evaluation_only benchmark。 |
| TP-09.04 | TP-09 | 2 | P0 | action | Yes | TP-08.03, TP-09.02 | 17 | No | No | 把 MingLi/BaziQA 失败样本按 owner 能力面映射到婚姻、事业、家庭、健康、财运、学业等规则 backlog。 |
| TP-10 | ROOT | 1 | P0 | package | No | TP-09.01, TP-09.03, TP-09.04 | - | No | No | 把新增专业能力落到 fate-core 边界，delivery 只负责呈现，并用最终 review/ship gate 收口。 |
| TP-10.01 | TP-10 | 2 | P1 | action | Yes | TP-09.01, TP-09.03, TP-09.04 | 18 | No | No | 按 pattern、hehua、yongshen、fortune、topic 逐切片从大文件抽出纯 evaluator，保持 schema 行为不变。 |
| TP-10.02 | TP-10 | 2 | P0 | action | Yes | TP-09.01, TP-09.03, TP-09.04, TP-10.01 | 19 | No | No | 保证 Web/API/Markdown 只消费结构化结果，不在 delivery 二次推断命理结论。 |
| TP-10.03 | TP-10 | 2 | P0 | action | Yes | TP-09.01, TP-09.03, TP-09.04, TP-10.02 | 20 | No | No | 运行 quick/full/deep/review，生成最终 PASS/WARN/BLOCK 结论。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
