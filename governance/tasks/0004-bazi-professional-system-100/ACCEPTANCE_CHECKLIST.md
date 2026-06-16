# Acceptance Checklist

# Global Standards
- [ ] 基础排盘 100%：四柱、节气换月、立春年界、起运、真太阳时、早晚子时和跨时区边界都有 oracle 或 golden。
- [ ] 历法时间 100%：production provider、oracle 对照、依赖升级门禁和差异归因齐备。
- [ ] 证据化 100%：报告/API 不出现无 ruleId 的专业断语。
- [ ] 常规分析 100%：强弱、月令、藏干、十神、五行、常规格局、干支关系和喜忌策略都有结构化字段和 golden。
- [ ] 高级格局 100%：正格、变格、从格、假从、专旺、化气均有成立条件、破格条件和反例矩阵。
- [ ] 合化成败 100%：合象、合而不化、成化、破化、争合、阻隔、冲破状态链明确。
- [ ] 用神裁决 100%：调候、扶抑、通关、病药并列评分，冲突裁决可解释。
- [ ] 岁运专题 100%：大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业等 profile 联动。
- [ ] Golden 回归 100%：新增规则均有正例、反例、边界例、failureExplanation 和 shard/deep gate。
- [ ] 样本外 benchmark 100%：MingLi/BaziQA 评测链路成熟、分类门槛明确、无答案泄漏、失败归因可回炉。

# Task Package Checklists
## TP-01
- 标题: 锁定 100% Scorecard 与资源边界
- 验收项:
  - [ ] 达成 `锁定 100% Scorecard 与资源边界` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把当前完成度表转成不可混淆的工程验收标准、资源角色和禁止路径。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 刷新八字 100% Scorecard
- 验收项:
  - [ ] 100% 口径明确写成工程/专业验收成熟度，而不是预测准确率。
- Verify: 人工核对 SCORECARD 与当前完成度表、MINGLI_FULL_EVALUATION、RULE_SOURCE_GAPS 一致。
- Gate: 每个维度都有 current、target、verify、falsifier、owner、next threshold。
- 输出物:
  - [ ] 更新后的 SCORECARD / plan evidence
- 标准清单:
  - [ ] Verify: 人工核对 SCORECARD 与当前完成度表、MINGLI_FULL_EVALUATION、RULE_SOURCE_GAPS 一致。
  - [ ] Gate: 每个维度都有 current、target、verify、falsifier、owner、next threshold。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 刷新资源地图和复用边界
- 验收项:
  - [ ] 无 license 不清资源进入 runtime；MingLi/BaziQA 只作为 evaluation。
- Verify: rg 'usageRole|production_dependency|oracle_only|evaluation_only|reference_only' governance/tasks contracts tools -n
- Gate: production/oracle/evaluation/reference/future_candidate 边界不混写。
- 输出物:
  - [ ] RESOURCE_MAP 更新
  - [ ] 新资源审查队列
- 标准清单:
  - [ ] Verify: rg 'usageRole|production_dependency|oracle_only|evaluation_only|reference_only' governance/tasks contracts tools -n
  - [ ] Gate: production/oracle/evaluation/reference/future_candidate 边界不混写。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.03
- 标题: 建立规则来源缺口台账
- 验收项:
  - [ ] 无来源规则不得进入 evaluator；缺专家样本必须标 beta/HITL。
- Verify: rg 'GAP-BZ-' governance/tasks/0004-bazi-professional-system-100 governance/tasks/0003-bazi-system-100 -n
- Gate: 高级格局、合化、用神、岁运、专题、benchmark 均有 gap id。
- 输出物:
  - [ ] RULE_SOURCE_GAPS 增量
  - [ ] gap id 到任务节点映射
- 标准清单:
  - [ ] Verify: rg 'GAP-BZ-' governance/tasks/0004-bazi-professional-system-100 governance/tasks/0003-bazi-system-100 -n
  - [ ] Gate: 高级格局、合化、用神、岁运、专题、benchmark 均有 gap id。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 基础排盘与历法时间边界 100%
- 验收项:
  - [ ] 达成 `基础排盘与历法时间边界 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: source-gap-ledger
- 输出物:
  - [ ] 补齐基础排盘和时间边界的 oracle、golden、依赖升级门禁和差异归因。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: source-gap-ledger
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 扩展 calendar boundary matrix
- 验收项:
  - [ ] 任一 boundary mismatch 都有 root cause 或 tolerance。
- Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
- Gate: 新增样本都有 source、expected、tolerance、failureExplanation。
- 输出物:
  - [ ] calendar_boundary_cases.json 增量
  - [ ] oracle mismatch report
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
  - [ ] Gate: 新增样本都有 source、expected、tolerance、failureExplanation。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 锁定 CalendarProvider 升级合同
- 验收项:
  - [ ] 上游升级必须触发 calendar oracle、solar terms 和 bazi golden。
- Verify: rg 'lunar-python|sxtwl|oracle_only|CalendarProvider' requirements*.txt pyproject.toml contracts governance tests -n
- Gate: 生产入口不 import oracle；依赖文件声明与锁文件一致。
- 输出物:
  - [ ] CalendarProvider gate 说明
  - [ ] dependency upgrade checklist
- 标准清单:
  - [ ] Verify: rg 'lunar-python|sxtwl|oracle_only|CalendarProvider' requirements*.txt pyproject.toml contracts governance tests -n
  - [ ] Gate: 生产入口不 import oracle；依赖文件声明与锁文件一致。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 基础排盘回归矩阵
- 验收项:
  - [ ] 基础排盘维度可从 93% 提升到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py -q
- Gate: 基础字段 schema diff 为零或有迁移说明。
- 输出物:
  - [ ] 基础排盘 golden 增量
  - [ ] API contract evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: 基础字段 schema diff 为零或有迁移说明。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

## TP-03
- 标题: 证据化与可解释 100%
- 验收项:
  - [ ] 达成 `证据化与可解释 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: source-gap-ledger
- 输出物:
  - [ ] 让 API、Markdown 和 rule-depth 输出的每个专业结论都能追溯到规则、字段、权重和风险边界。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: source-gap-ledger
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 补齐 ruleId 覆盖审计
- 验收项:
  - [ ] ruleIds 全部能回指 registry/classics。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
- Gate: 未登记断语不能进入 production 报告。
- 输出物:
  - [ ] ruleId coverage audit
  - [ ] missing rule backlog
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
  - [ ] Gate: 未登记断语不能进入 production 报告。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 标准化 evidenceFields 合同
- 验收项:
  - [ ] 报告中不再只有自然语言结论。
- Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q
- Gate: 新增字段不破坏现有 API/Web/Markdown 消费者。
- 输出物:
  - [ ] REPORT_FIELD_CONTRACT 更新
  - [ ] API schema regression
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q
  - [ ] Gate: 新增字段不破坏现有 API/Web/Markdown 消费者。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 高风险输出边界回归
- 验收项:
  - [ ] 高风险专题只输出趋势和结构证据。
- Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q
- Gate: 高风险词和保证式话术被 policy regression 拦截。
- 输出物:
  - [ ] policy regression fixtures
  - [ ] riskBoundary report snippets
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q
  - [ ] Gate: 高风险词和保证式话术被 policy regression 拦截。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

## TP-04
- 标题: 常规八字分析 100%
- 验收项:
  - [ ] 达成 `常规八字分析 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: base-chart-regression, evidence-field-contract
- 输出物:
  - [ ] 把强弱、月令、十神、藏干、五行、常规格局和干支关系做成稳定 evaluator 与 golden。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: base-chart-regression, evidence-field-contract
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 强弱与月令 evaluator
- 验收项:
  - [ ] 强弱判断可解释且可被高级格局/用神复用。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
- Gate: strength 输出包含 score、basis、sourceRuleId、conflicts。
- 输出物:
  - [ ] strength evaluator slice
  - [ ] strength golden cases
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
  - [ ] Gate: strength 输出包含 score、basis、sourceRuleId、conflicts。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 十神结构 evaluator
- 验收项:
  - [ ] 事业、财运、婚姻、家庭 profile 可消费十神结构。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
- Gate: 十神解释必须引用盘面证据，不输出孤立断语。
- 输出物:
  - [ ] tenGodStructure fields
  - [ ] topic input mapping
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: 十神解释必须引用盘面证据，不输出孤立断语。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 常规格局 evaluator
- 验收项:
  - [ ] 常规分析维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
- Gate: 无法稳定判定时输出 uncertainty，不强断。
- 输出物:
  - [ ] regularPatternCandidates
  - [ ] 正破格 golden
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q
  - [ ] Gate: 无法稳定判定时输出 uncertainty，不强断。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 高级格局 100%
- 验收项:
  - [ ] 达成 `高级格局 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: regular-pattern-evaluator
- 输出物:
  - [ ] 把从格、假从、化气、专旺、变格等高级格局从 beta 候选推进到 guarded/production 可审查状态。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: regular-pattern-evaluator
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 高级格局规则矩阵
- 验收项:
  - [ ] 缺条件的高级格局只能输出 beta/candidate。
- Verify: rg '从格|假从|专旺|化气|specialPattern' contracts/fate domains/fate-analysis -n
- Gate: 每类高级格局至少有成立条件和反证条件。
- 输出物:
  - [ ] specialPattern rule matrix
  - [ ] registry 增量
- 标准清单:
  - [ ] Verify: rg '从格|假从|专旺|化气|specialPattern' contracts/fate domains/fate-analysis -n
  - [ ] Gate: 每类高级格局至少有成立条件和反证条件。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 高级格局正反例 golden
- 验收项:
  - [ ] 从格/假从/专旺/化气都有可回归样本。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
- Gate: 无 golden 的高级格局不能升 production。
- 输出物:
  - [ ] rule_depth_cases 增量
  - [ ] advanced pattern fixtures
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q
  - [ ] Gate: 无 golden 的高级格局不能升 production。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.03
- 标题: 高级格局 evaluator
- 验收项:
  - [ ] 高级格局维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
- Gate: evaluator 不依赖 delivery；输出 schema 稳定。
- 输出物:
  - [ ] specialPatternCandidates
  - [ ] guarded evaluator evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: evaluator 不依赖 delivery；输出 schema 稳定。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 合化成败 100%
- 验收项:
  - [ ] 达成 `合化成败 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: regular-pattern-evaluator
- 输出物:
  - [ ] 把干支合化从自然语言关系升级为有条件链、状态机和反例矩阵的 evaluator。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: regular-pattern-evaluator
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 干支关系条件目录
- 验收项:
  - [ ] 不再只输出“合”而不区分成败。
- Verify: rg '合化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n
- Gate: 每种关系状态都有 required evidenceFields。
- 输出物:
  - [ ] conditionCatalog
  - [ ] sourceRuleId mapping
- 标准清单:
  - [ ] Verify: rg '合化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n
  - [ ] Gate: 每种关系状态都有 required evidenceFields。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 合化状态链 evaluator
- 验收项:
  - [ ] 合而不化、成化、破化、争合、阻隔可区分。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
- Gate: 每个 transform state 都有证据和反证条件。
- 输出物:
  - [ ] combineTransformMatrix
  - [ ] relation evaluator evidence
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: 每个 transform state 都有证据和反证条件。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.03
- 标题: 合化反例矩阵
- 验收项:
  - [ ] 合化成败维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: 反例失败时能定位到具体 condition。
- 输出物:
  - [ ] hehua negative fixtures
  - [ ] failureExplanation
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [ ] Gate: 反例失败时能定位到具体 condition。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 用神裁决 100%
- 验收项:
  - [ ] 达成 `用神裁决 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: strength-evaluator, regular-pattern-evaluator, hehua-negative-golden
- 输出物:
  - [ ] 把调候、扶抑、通关、病药从并列描述升级为可冲突裁决的评分矩阵。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: strength-evaluator, regular-pattern-evaluator, hehua-negative-golden
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: 用神策略矩阵
- 验收项:
  - [ ] 不能用单一用神覆盖全部策略。
- Verify: rg '调候|扶抑|通关|病药|用神' contracts/fate governance/tasks -n
- Gate: 每个 strategy 都有 basis、score、doesNotApplyWhen。
- 输出物:
  - [ ] yongShen strategy matrix
  - [ ] conflictPolicy
- 标准清单:
  - [ ] Verify: rg '调候|扶抑|通关|病药|用神' contracts/fate governance/tasks -n
  - [ ] Gate: 每个 strategy 都有 basis、score、doesNotApplyWhen。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.02
- 标题: 用神决策 evaluator
- 验收项:
  - [ ] 用神裁决能被专题 profile 消费。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
- Gate: 冲突裁决可解释，不输出唯一绝对结论。
- 输出物:
  - [ ] yongShenDecision
  - [ ] decision trace
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: 冲突裁决可解释，不输出唯一绝对结论。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: 用神冲突正反例
- 验收项:
  - [ ] 用神裁决维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: 冲突 golden 可以解释 ranking 变化。
- 输出物:
  - [ ] yongshen conflict fixtures
  - [ ] strategy regression
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [ ] Gate: 冲突 golden 可以解释 ranking 变化。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 岁运专题 100%
- 验收项:
  - [ ] 达成 `岁运专题 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: ten-god-evaluator, special-pattern-evaluator, yongshen-conflict-golden
- 输出物:
  - [ ] 把大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业等专题 profile 联动。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: ten-god-evaluator, special-pattern-evaluator, yongshen-conflict-golden
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.01
- 标题: 岁运触发矩阵
- 验收项:
  - [ ] 每个 trigger 有 sourceRuleId、evidenceFields、riskBoundary。
- Verify: rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n
- Gate: 动态触发只作为趋势证据，不输出确定未来。
- 输出物:
  - [ ] fortuneTriggers matrix
  - [ ] trend-only riskBoundary
- 标准清单:
  - [ ] Verify: rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n
  - [ ] Gate: 动态触发只作为趋势证据，不输出确定未来。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.02
- 标题: 专题 profile 联合评分
- 验收项:
  - [ ] 专题 profile 不再只是 alias 或自然语言拼接。
- Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: topicProfiles.lifecycle=production 之前必须有 golden 和 policy regression。
- 输出物:
  - [ ] topicProfiles
  - [ ] topic scoring traces
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [ ] Gate: topicProfiles.lifecycle=production 之前必须有 golden 和 policy regression。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.03
- 标题: 专题风险边界
- 验收项:
  - [ ] 岁运专题维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q
- Gate: 高风险专题不输出现实处方、保证、恐吓或法律金融医疗建议。
- 输出物:
  - [ ] topic risk fixtures
  - [ ] safe report snippets
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q
  - [ ] Gate: 高风险专题不输出现实处方、保证、恐吓或法律金融医疗建议。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-09
- 标题: Golden 回归与样本外 Benchmark 100%
- 验收项:
  - [ ] 达成 `Golden 回归与样本外 Benchmark 100%` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: topic-risk-policy
- 输出物:
  - [ ] 把规则样本、deep gate、MingLi/BaziQA 评测和失败归因做成可持续改进系统。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: topic-risk-policy
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.01
- 标题: Golden shard 与 deep gate
- 验收项:
  - [ ] Golden/回归维度达到 100% gate。
- Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
- Gate: 全量慢测不进入日常 quick；deep/release 可分片复现。
- 输出物:
  - [ ] GOLDEN_DEEP_GATE 更新
  - [ ] shard evidence
- 标准清单:
  - [ ] Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
  - [ ] Gate: 全量慢测不进入日常 quick；deep/release 可分片复现。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-09.02
- 标题: MingLi full 评测门禁
- 验收项:
  - [ ] 下一阶段门槛 overall >= 32%、财运 >= 15%、婚姻 failures <= 25。
- Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
- Gate: answered=160；predictions 无 expected/answer/correct/gold/label 字段；accuracy 不低于当前 baseline 或有边界解释。
- 输出物:
  - [ ] MINGLI_FULL_EVALUATION 更新
  - [ ] MINGLI_FAILURE_TAXONOMY 更新
- 标准清单:
  - [ ] Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
  - [ ] Gate: answered=160；predictions 无 expected/answer/correct/gold/label 字段；accuracy 不低于当前 baseline 或有边界解释。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.03
- 标题: BaziQA 纳入评测审查
- 验收项:
  - [ ] 样本外 benchmark 维度的资源路线清楚。
- Verify: 记录 license、dataset schema、adapter plan 和禁止进入 runtime 的 gate。
- Gate: license/source 不清时不得纳入正式 gate；只允许 future_candidate/evaluation_only。
- 输出物:
  - [ ] BaziQA admission note
  - [ ] future benchmark backlog
- 标准清单:
  - [ ] Verify: 记录 license、dataset schema、adapter plan 和禁止进入 runtime 的 gate。
  - [ ] Gate: license/source 不清时不得纳入正式 gate；只允许 future_candidate/evaluation_only。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.04
- 标题: 失败归因回炉到规则任务
- 验收项:
  - [ ] 样本外 benchmark 维度达到 100% gate。
- Verify: MINGLI_FAILURE_TAXONOMY 中每类 failure 都有 owner、缺口类型、回炉方向和禁止路径。
- Gate: 不得按 question_id 或 expected answer 生成规则。
- 输出物:
  - [ ] failure taxonomy backlog
  - [ ] topic owner queue
- 标准清单:
  - [ ] Verify: MINGLI_FAILURE_TAXONOMY 中每类 failure 都有 owner、缺口类型、回炉方向和禁止路径。
  - [ ] Gate: 不得按 question_id 或 expected answer 生成规则。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-10
- 标题: 维护性、交付边界与最终发布门禁
- 验收项:
  - [ ] 达成 `维护性、交付边界与最终发布门禁` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: golden-shard-policy, failure-backlog-to-rules, baziqa-admission
- 输出物:
  - [ ] 把新增专业能力落到 fate-core 边界，delivery 只负责呈现，并用最终 review/ship gate 收口。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: golden-shard-policy, failure-backlog-to-rules, baziqa-admission
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.01
- 标题: evaluator 物理拆分
- 验收项:
  - [ ] 长期维护性维度达到 100% gate。
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py tests/regression/test_bazi_golden_coverage_matrix.py -q
- Gate: 每次只抽一个 evaluator；失败只回滚当前切片；delivery 不新增领域算法。
- 输出物:
  - [ ] fate_core/usecases/evaluators/*
  - [ ] AGENTS.md/边界文档更新
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py tests/regression/test_bazi_golden_coverage_matrix.py -q
  - [ ] Gate: 每次只抽一个 evaluator；失败只回滚当前切片；delivery 不新增领域算法。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.02
- 标题: 报告字段与 Markdown 边界收口
- 验收项:
  - [ ] delivery 交付边界清楚。
- Verify: .venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py -q
- Gate: 报告所有新增专业段落都有 evidence/riskBoundary；前端不重算规则。
- 输出物:
  - [ ] REPORT_FIELD_CONTRACT final
  - [ ] Markdown golden
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py -q
  - [ ] Gate: 报告所有新增专业段落都有 evidence/riskBoundary；前端不重算规则。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.03
- 标题: 最终本地门禁与审查
- 验收项:
  - [ ] 全部任务节点可进入 closeout，八字体系专业验收 100% 口径成立。
- Verify: bash scripts/local-ci.sh --profile quick && bash scripts/local-ci.sh --profile full
- Gate: final review Active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造公网/live bot。
- 输出物:
  - [ ] FINAL_REVIEW.md
  - [ ] CLOSEOUT.md
  - [ ] local-ci evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile quick && bash scripts/local-ci.sh --profile full
  - [ ] Gate: final review Active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造公网/live bot。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
