# Repo Evidence
- 现有任务 `governance/tasks/0003-bazi-system-100` 已 closeout，结论是工程验收 PASS with WARN，不是专业推理 100%。
- `contracts/fate/rule_depth_registry.json` 当前八字 rule-depth 规则约 22 条。
- `contracts/fate/classics_rule_index.json` 当前八字 classics 规则约 43 条。
- `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json` 当前有 300 个覆盖样本。
- `MINGLI_FULL_EVALUATION.md` 记录 MingLi full：160 answered / 45 correct / 28.12% accuracy。
- `MINGLI_FAILURE_TAXONOMY.md` 显示失败集中在婚姻、事业、家庭、健康、财运、学业等专题。
- `EVALUATOR_BOUNDARIES.md` 已明确 kernel/usecase/evaluation/oracle/delivery 边界。
- `CORE_FILE_BURNDOWN.md` 显示 bazi_calculator.py、calculate_pure_analysis.py、report_generator.py 仍是主要维护风险。

# Constraints Matrix
- 不能伪造 100%，不能把工程验收 100% 写成预测准确率 100%。
- 不能把 oracle/evaluation/reference 资源引入生产请求链路。
- 不能跳过 sourceRuleId、evidenceFields、riskBoundary 和反证条件。
- 不能输出医疗、金融、法律、心理替代建议或确定未来。
- 不能因大文件拆分破坏现有 API/Web/Bot/Markdown 行为。

# Change Boundary
- 本计划阶段只新增 `governance/tasks/0004-bazi-professional-system-100` 和更新 `governance/tasks/INDEX.md`。
- 后续执行按任务树叶子节点逐项修改 contracts、fate-core、data-products、tests、reports 和 governance evidence。
- 每个叶子任务只允许处理其对应能力面，不顺手扩散到 UI、营销文案或无关生产部署。

# Risk Matrix
- high：高级格局、用神、岁运专题涉及专业规则裁决，错误强断会制造假专业能力。
- high：benchmark 提升容易被误做成答案硬编码，必须有防泄漏门禁。
- medium：历法/时间边界变更可能影响历史输出，需要 oracle 和 golden 解释。
- medium：大文件拆分可能造成 schema drift 或 import 循环。
- medium：真实专家命例和经典资料有 license/source 边界，需要 HITL 审查。

# Assumptions and Falsification
- 本任务的 100% 是专业体系验收成熟度，不是命理预测绝对正确。
- 真实专家命例不足时允许标记 HITL/WARN，不允许编造样本补数。
- MingLi 下一阶段先以 overall >= 32%、财运 >= 15%、婚姻 failures <= 25 作为增量门槛，而不是一次要求高不可证的命中率。

# Critical Ambiguities
- 专业命例来源、版权、专家标注流程仍需后续 HITL 确认。
- BaziQA 是否纳入正式评测需要 license、数据质量和题型适配审查。
- 高级断法升 production 的阈值需要结合专家评审和 benchmark 分类表现，不由单次代码实现决定。

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: calendar/oracle mismatch
- 调试关注点: golden regression drift
- 调试关注点: benchmark answer leakage
- 调试关注点: topic profile unsafe output
- 调试关注点: schema drift after evaluator extraction
- 强制调试叶子节点: TP-02.03, TP-03.03, TP-09.01

# Task Package Context Map
## TP-01
- Step Key: `scorecard-contract`
- 标题: 锁定 100% Scorecard 与资源边界
- 类型: `package`
- 目标: 把当前完成度表转成不可混淆的工程验收标准、资源角色和禁止路径。
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `scorecard-refresh`
- 标题: 刷新八字 100% Scorecard
- 类型: `action`
- 目标: 把 10 个维度的当前值、目标 gate、verify、falsifier、owner 和下一门槛写成任务真相源。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 更新后的 SCORECARD / plan evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: Target end state: Scorecard 是八字专业体系的单一完成度口径。；Falsifier: 任一维度没有 verify 或 falsifier 时，不能进入实现波次。

### TP-01.02
- Step Key: `resource-boundary-refresh`
- 标题: 刷新资源地图和复用边界
- 类型: `action`
- 目标: 确认 lunar-python、sxtwl、bazica、sxwnl、paipan、MingLi-Bench、BaziQA、bazi-1 的 usageRole 和禁止用途。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: RESOURCE_MAP 更新；新资源审查队列
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: Existence check: 资源边界防止把开源库误当专业能力捷径。；Selected ladder rung: project-native governance resource map。

### TP-01.03
- Step Key: `source-gap-ledger`
- 标题: 建立规则来源缺口台账
- 类型: `action`
- 目标: 把缺规则、缺反例、缺专家样本、缺 license、缺 evaluator 的能力统一进入 gap ledger。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: scorecard-refresh, resource-boundary-refresh
- 依赖节点 ID: TP-01.01, TP-01.02
- 输入: 无
- 输出: RULE_SOURCE_GAPS 增量；gap id 到任务节点映射
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `calendar-base-chart`
- 标题: 基础排盘与历法时间边界 100%
- 类型: `package`
- 目标: 补齐基础排盘和时间边界的 oracle、golden、依赖升级门禁和差异归因。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02, TP-02.03
- 依赖步骤 Key: source-gap-ledger
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.01
- Step Key: `calendar-boundary-matrix`
- 标题: 扩展 calendar boundary matrix
- 类型: `action`
- 目标: 补节气秒级、立春年界、早晚子时、真太阳时、跨时区、DST、起运边界样本。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: calendar_boundary_cases.json 增量；oracle mismatch report
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.02
- Step Key: `calendar-provider-contract`
- 标题: 锁定 CalendarProvider 升级合同
- 类型: `action`
- 目标: 明确 lunar-python 是 production provider，oracle 资源只在测试中使用，依赖升级必须跑指定门禁。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: CalendarProvider gate 说明；dependency upgrade checklist
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.03
- Step Key: `base-chart-regression`
- 标题: 基础排盘回归矩阵
- 类型: `action`
- 目标: 把四柱、五行、十神、藏干、起运、真太阳时基础字段纳入稳定回归。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: calendar-boundary-matrix, calendar-provider-contract
- 依赖节点 ID: TP-02.01, TP-02.02
- 输入: 无
- 输出: 基础排盘 golden 增量；API contract evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `evidence-contract`
- 标题: 证据化与可解释 100%
- 类型: `package`
- 目标: 让 API、Markdown 和 rule-depth 输出的每个专业结论都能追溯到规则、字段、权重和风险边界。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02, TP-03.03
- 依赖步骤 Key: source-gap-ledger
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.01
- Step Key: `rule-id-coverage`
- 标题: 补齐 ruleId 覆盖审计
- 类型: `action`
- 目标: 检查报告/API 中所有专业断语是否都有 sourceRuleId 或明确 unsupported/beta 边界。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: ruleId coverage audit；missing rule backlog
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.02
- Step Key: `evidence-field-contract`
- 标题: 标准化 evidenceFields 合同
- 类型: `action`
- 目标: 把 sourceRuleId、evidenceFields、score、weight、doesNotApplyWhen、riskBoundary 做成统一字段契约。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: REPORT_FIELD_CONTRACT 更新；API schema regression
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.03
- Step Key: `unsafe-output-regression`
- 标题: 高风险输出边界回归
- 类型: `action`
- 目标: 锁定健康、财运、灾劫、官非等专题不能输出现实处方、恐吓或保证式判断。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: rule-id-coverage, evidence-field-contract
- 依赖节点 ID: TP-03.01, TP-03.02
- 输入: 无
- 输出: policy regression fixtures；riskBoundary report snippets
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `regular-analysis`
- 标题: 常规八字分析 100%
- 类型: `package`
- 目标: 把强弱、月令、十神、藏干、五行、常规格局和干支关系做成稳定 evaluator 与 golden。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02, TP-04.03
- 依赖步骤 Key: base-chart-regression, evidence-field-contract
- 依赖节点 ID: TP-02.03, TP-03.02
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `strength-evaluator`
- 标题: 强弱与月令 evaluator
- 类型: `action`
- 目标: 独立强弱评分、月令、人元司令、通根透干和旺衰证据，避免散落在大函数里。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: strength evaluator slice；strength golden cases
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.02
- Step Key: `ten-god-evaluator`
- 标题: 十神结构 evaluator
- 类型: `action`
- 目标: 结构化透干、藏干、十神数量、十神组合和十神族群映射。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: tenGodStructure fields；topic input mapping
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.03
- Step Key: `regular-pattern-evaluator`
- 标题: 常规格局 evaluator
- 类型: `action`
- 目标: 覆盖财官印食等常规格局候选、成立依据、破格条件和不确定原因。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: strength-evaluator, ten-god-evaluator
- 依赖节点 ID: TP-04.01, TP-04.02
- 输入: 无
- 输出: regularPatternCandidates；正破格 golden
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `advanced-patterns`
- 标题: 高级格局 100%
- 类型: `package`
- 目标: 把从格、假从、化气、专旺、变格等高级格局从 beta 候选推进到 guarded/production 可审查状态。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02, TP-05.03
- 依赖步骤 Key: regular-pattern-evaluator
- 依赖节点 ID: TP-04.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `special-pattern-rule-matrix`
- 标题: 高级格局规则矩阵
- 类型: `action`
- 目标: 为从格、假从、专旺、化气、变格建立 appliesWhen、doesNotApplyWhen、破格条件和 sourceRuleId。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: specialPattern rule matrix；registry 增量
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.02
- Step Key: `special-pattern-golden`
- 标题: 高级格局正反例 golden
- 类型: `action`
- 目标: 为每个高级格局补正例、反例、边界例和 failureExplanation。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: rule_depth_cases 增量；advanced pattern fixtures
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.03
- Step Key: `special-pattern-evaluator`
- 标题: 高级格局 evaluator
- 类型: `action`
- 目标: 实现或抽取高级格局 evaluator，输出候选、置信度、破格原因和风险边界。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: special-pattern-rule-matrix, special-pattern-golden
- 依赖节点 ID: TP-05.01, TP-05.02
- 输入: 无
- 输出: specialPatternCandidates；guarded evaluator evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `hehua-transform`
- 标题: 合化成败 100%
- 类型: `package`
- 目标: 把干支合化从自然语言关系升级为有条件链、状态机和反例矩阵的 evaluator。
- 父节点: `ROOT`
- 子节点: TP-06.01, TP-06.02, TP-06.03
- 依赖步骤 Key: regular-pattern-evaluator
- 依赖节点 ID: TP-04.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.01
- Step Key: `relation-condition-catalog`
- 标题: 干支关系条件目录
- 类型: `action`
- 目标: 登记天干五合、地支六合、三合、三会、冲刑害破、争合、阻隔、冲破的条件字段。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: conditionCatalog；sourceRuleId mapping
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.02
- Step Key: `combine-transform-state-machine`
- 标题: 合化状态链 evaluator
- 类型: `action`
- 目标: 输出 structural_relation、transform_candidate、transform_success、transform_broken。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: relation-condition-catalog
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: combineTransformMatrix；relation evaluator evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.03
- Step Key: `hehua-negative-golden`
- 标题: 合化反例矩阵
- 类型: `action`
- 目标: 补月令、透干、通根、得令、帮扶、冲破、阻隔导致不成化的反例。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: combine-transform-state-machine
- 依赖节点 ID: TP-06.02
- 输入: 无
- 输出: hehua negative fixtures；failureExplanation
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-07
- Step Key: `yongshen-arbitration`
- 标题: 用神裁决 100%
- 类型: `package`
- 目标: 把调候、扶抑、通关、病药从并列描述升级为可冲突裁决的评分矩阵。
- 父节点: `ROOT`
- 子节点: TP-07.01, TP-07.02, TP-07.03
- 依赖步骤 Key: strength-evaluator, regular-pattern-evaluator, hehua-negative-golden
- 依赖节点 ID: TP-04.01, TP-04.03, TP-06.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-07.01
- Step Key: `yongshen-strategy-matrix`
- 标题: 用神策略矩阵
- 类型: `action`
- 目标: 定义调候、扶抑、通关、病药、格局用神的输入字段、评分、冲突和不适用条件。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: yongShen strategy matrix；conflictPolicy
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-07.02
- Step Key: `yongshen-decision-evaluator`
- 标题: 用神决策 evaluator
- 类型: `action`
- 目标: 输出 scoredStrategies、ranking、conflicts、selectedCandidates、riskBoundary。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: yongshen-strategy-matrix
- 依赖节点 ID: TP-07.01
- 输入: 无
- 输出: yongShenDecision；decision trace
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-07.03
- Step Key: `yongshen-conflict-golden`
- 标题: 用神冲突正反例
- 类型: `action`
- 目标: 补寒暖燥湿、身强身弱、格局优先、通关病药冲突场景的 golden。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: yongshen-decision-evaluator
- 依赖节点 ID: TP-07.02
- 输入: 无
- 输出: yongshen conflict fixtures；strategy regression
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-08
- Step Key: `fortune-topic-profiles`
- 标题: 岁运专题 100%
- 类型: `package`
- 目标: 把大运、流年、流月触发与婚姻、事业、财运、家庭、健康、学业等专题 profile 联动。
- 父节点: `ROOT`
- 子节点: TP-08.01, TP-08.02, TP-08.03
- 依赖步骤 Key: ten-god-evaluator, special-pattern-evaluator, yongshen-conflict-golden
- 依赖节点 ID: TP-04.02, TP-05.03, TP-07.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-08.01
- Step Key: `fortune-trigger-matrix`
- 标题: 岁运触发矩阵
- 类型: `action`
- 目标: 定义大运、流年、流月、伏吟反吟、天克地冲、刑冲合害与原局关系的 trigger chain。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: fortuneTriggers matrix；trend-only riskBoundary
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-08.02
- Step Key: `topic-profile-scoring`
- 标题: 专题 profile 联合评分
- 类型: `action`
- 目标: 为婚姻、事业、财运、家庭、健康、学业、迁移建立 score、basis、scoreBasis、evidenceFields、lifecycle。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: fortune-trigger-matrix
- 依赖节点 ID: TP-08.01
- 输入: 无
- 输出: topicProfiles；topic scoring traces
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-08.03
- Step Key: `topic-risk-policy`
- 标题: 专题风险边界
- 类型: `action`
- 目标: 针对健康、财运、灾劫、官非等高风险专题补安全文案和 policy 测试。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: topic-profile-scoring
- 依赖节点 ID: TP-08.02
- 输入: 无
- 输出: topic risk fixtures；safe report snippets
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-09
- Step Key: `golden-and-benchmark`
- 标题: Golden 回归与样本外 Benchmark 100%
- 类型: `package`
- 目标: 把规则样本、deep gate、MingLi/BaziQA 评测和失败归因做成可持续改进系统。
- 父节点: `ROOT`
- 子节点: TP-09.01, TP-09.02, TP-09.03, TP-09.04
- 依赖步骤 Key: topic-risk-policy
- 依赖节点 ID: TP-08.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-09.01
- Step Key: `golden-shard-policy`
- 标题: Golden shard 与 deep gate
- 类型: `action`
- 目标: 把 quick 代表集、deep 300+ matrix、rule-depth、calendar boundary 和 topic fixtures 分层。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: GOLDEN_DEEP_GATE 更新；shard evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-09.02
- Step Key: `mingli-full-gate`
- 标题: MingLi full 评测门禁
- 类型: `action`
- 目标: 持续生成 160 题 predictions、report、byCategory 和 failure taxonomy，且无答案泄漏。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: MINGLI_FULL_EVALUATION 更新；MINGLI_FAILURE_TAXONOMY 更新
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-09.03
- Step Key: `baziqa-admission`
- 标题: BaziQA 纳入评测审查
- 类型: `action`
- 目标: 审查 BaziQA license、题型、输入输出契约和是否可作为 evaluation_only benchmark。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: BaziQA admission note；future benchmark backlog
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-09.04
- Step Key: `failure-backlog-to-rules`
- 标题: 失败归因回炉到规则任务
- 类型: `action`
- 目标: 把 MingLi/BaziQA 失败样本按 owner 能力面映射到婚姻、事业、家庭、健康、财运、学业等规则 backlog。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: mingli-full-gate
- 依赖节点 ID: TP-09.02
- 输入: 无
- 输出: failure taxonomy backlog；topic owner queue
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-10
- Step Key: `maintainability-and-delivery`
- 标题: 维护性、交付边界与最终发布门禁
- 类型: `package`
- 目标: 把新增专业能力落到 fate-core 边界，delivery 只负责呈现，并用最终 review/ship gate 收口。
- 父节点: `ROOT`
- 子节点: TP-10.01, TP-10.02, TP-10.03
- 依赖步骤 Key: golden-shard-policy, failure-backlog-to-rules, baziqa-admission
- 依赖节点 ID: TP-09.01, TP-09.04, TP-09.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-10.01
- Step Key: `evaluator-physical-extraction`
- 标题: evaluator 物理拆分
- 类型: `action`
- 目标: 按 pattern、hehua、yongshen、fortune、topic 逐切片从大文件抽出纯 evaluator，保持 schema 行为不变。
- 父节点: `TP-10`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: fate_core/usecases/evaluators/*；AGENTS.md/边界文档更新
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-10.02
- Step Key: `report-contract-finalize`
- 标题: 报告字段与 Markdown 边界收口
- 类型: `action`
- 目标: 保证 Web/API/Markdown 只消费结构化结果，不在 delivery 二次推断命理结论。
- 父节点: `TP-10`
- 子节点: 无
- 依赖步骤 Key: evaluator-physical-extraction
- 依赖节点 ID: TP-10.01
- 输入: 无
- 输出: REPORT_FIELD_CONTRACT final；Markdown golden
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-10.03
- Step Key: `final-local-and-review-gates`
- 标题: 最终本地门禁与审查
- 类型: `action`
- 目标: 运行 quick/full/deep/review，生成最终 PASS/WARN/BLOCK 结论。
- 父节点: `TP-10`
- 子节点: 无
- 依赖步骤 Key: report-contract-finalize
- 依赖节点 ID: TP-10.02
- 输入: 无
- 输出: FINAL_REVIEW.md；CLOSEOUT.md；local-ci evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
