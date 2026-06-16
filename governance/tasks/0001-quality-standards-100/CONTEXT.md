# Repo Evidence
- 当前仓库：/home/lenovo/.projects/fatecat。
- 当前 HEAD：787111d592be。
- git 状态：main 本地领先 origin/main 7 个提交，远端无新提交。
- 最近审查证据：pytest 123 passed；ruff check PASS；mypy fate_core PASS；structure/source/privacy/governance PASS。
- 当前阻塞证据：ruff format --check 会重格式化 calculate_pure_analysis.py 和 test_bazi_ziwei_rule_depth.py。
- 当前阻塞证据：production-readiness.sh 在缺少 FATE_CORS_ALLOW_ORIGINS 时 FAIL。
- 当前警告证据：REVIEW.md 记录旧 HEAD、旧测试数量和过期生产门禁结论。
- 当前维护风险：bazi_calculator.py 2775 行、report_generator.py 1967 行、calculate_pure_analysis.py 1463 行、bot.py 1145 行、main.py 908 行、web_ui.py 830 行。
- 当前运行态干扰：infra/runtime/local-state 下有未跟踪 vendor-build 和 bazi.db，未入 Git 但影响搜索和本地审查。

# Constraints Matrix
- 禁止运行 GitHub Acceptance；只使用本地 CI/CD 技术工具方案。
- 执行阶段不得伪造公网生产或 Bot live 结果。
- 业务代码改动必须小步、可回滚、带测试。
- 公共生产验收必须用真实域名、TLS、反向代理、生产 URL 和真实 Bot token。
- 架构变更必须同步对应 AGENTS.md 或治理资产。

# Change Boundary
- 本轮只写 governance/tasks/0001-quality-standards-100/ 任务包和 governance/tasks/INDEX.md。
- 后续实现波次按叶子节点修改代码、测试、文档和治理资产。
- 不把 unrelated refactor、无关 UI 改造、营销文案和远端推送混入计划阶段。

# Risk Matrix
- high：生产发布涉及公网配置、限流、真实 token、反向代理、TLS 和观测。
- high：legacy BaziCalculator 迁移涉及核心命理结果，必须用 golden case 和 oracle 防回归。
- medium：时区/真太阳时语义修正可能改变输出，需要显式兼容边界。
- medium：Bot 背压和限流会改变用户体验，需要错误态和队列行为测试。
- medium：大文件拆分可能引入 import/path 循环，需要逐切片验证。
- low：纯格式化，但仍需确认无业务 diff。
- low：文档修正，但错误结论会误导后续 agent。
- medium：会暴露更多本地门禁失败，失败时转 auto-debug。
- high：生产配置错误会暴露公共服务。
- medium：环境默认值可能掩盖真实部署，需要 REVIEW 标明。
- high：需要外部凭证和真实基础设施；缺失时 Blocked/HITL。
- medium：可能改变当前解释，需要兼容说明。
- high：公共 Bot 滥用会影响可用性。
- medium：测试可能暴露 middleware 行为缺陷。
- medium：样本来源必须可追溯。
- medium：证据覆盖不足会阻塞可解释 100%。
- high：样本版权和专业可信度必须治理。
- medium：解释性增强不能越界成预测承诺。
- low：评测数据不应污染生产计算。
- medium：错误边界会导致重构方向错误。
- medium：拆分可能引入循环 import。
- high：命理核心行为变化必须由 golden/oracle 解释。
- medium：UI/报告输出必须保持契约。
- high：删除前必须确认无外部调用方。
- medium：错误替换历法库会影响核心结果。
- high：许可不清会影响公共发布。
- medium：多 oracle 冲突需要记录裁决规则。
- medium：规则膨胀会降低可解释性。
- medium：没有外部 Prometheus 时只能保留平台接入待办。
- medium：日志不得泄漏用户隐私。
- low：文档必须跟脚本一致。
- high：container/public-service 失败会阻塞最终 100%。
- high：review 发现 BLOCK 时不得 ship。
- medium：不得为了通过 review 删除必要保护。
- low：closeout 不等于 push，push 需 auto-github。

# Assumptions and Falsification
- 100% 不是代码覆盖率 100%，而是六项质量标准对应 gate 全部闭合。
- 可维护性 100% 不要求一次性删除全部 legacy，而要求新增领域规则不再进入错误边界，且迁移路径和 kill list 被执行到可审查状态。
- 真实公网验收需要用户提供外部 URL、域名、TLS、Bot token 或部署权限；缺失时对应叶子节点保持 Blocked/HITL。

# Critical Ambiguities
- 真实生产域名、TLS 和 Bot token 是否已可用；没有这些信息不能关闭 public-service live gate。
- 可维护性 100% 对大文件拆分的硬阈值需在执行中用 review gate 校准，避免为行数牺牲正确性。
- 八字 golden case 扩展到 100+ 的样本来源、版权和专业可信度需要治理确认。

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: format gate failure
- 调试关注点: production-readiness env failure
- 调试关注点: timezone semantic edge cases
- 调试关注点: Bot queue/backpressure correctness
- 强制调试叶子节点: TP-01.01, TP-03.03, TP-08.02

# Task Package Context Map
## TP-01
- Step Key: `baseline-gates`
- 标题: 修复当前本地质量阻塞
- 类型: `package`
- 目标: 先把当前已知 BLOCK 清零，恢复本地 CI 可信度。
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
- Step Key: `format-gate`
- 标题: 修复 ruff format gate
- 类型: `action`
- 目标: 格式化当前失败文件，让 ruff format --check 全仓通过。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 格式化后的 calculate_pure_analysis.py；格式化后的 test_bazi_ziwei_rule_depth.py
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: low：纯格式化，但仍需确认无业务 diff。
- 备注: Existence check: 当前 local-ci quick 会执行 format check，因此必须修。；Selected ladder rung: project-native ruff format。；Minimal runnable check: ruff format --check .

### TP-01.02
- Step Key: `review-refresh`
- 标题: 刷新 REVIEW.md 质量真相源
- 类型: `action`
- 目标: 把 REVIEW.md 更新到当前 HEAD、当前测试数量、当前 production-readiness 真实状态。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: format-gate
- 依赖节点 ID: TP-01.01
- 输入: 无
- 输出: REVIEW.md 当前质量记录
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: low：文档修正，但错误结论会误导后续 agent。
- 备注: Target end state: REVIEW.md 是当前审查结果真相源，不保留过期乐观口径。；Rejected short-term patches: 不只追加新段落掩盖旧结论。

### TP-01.03
- Step Key: `quick-local-ci`
- 标题: 恢复 local-ci quick 绿色
- 类型: `action`
- 目标: 用本地 CI 快速入口证明基础质量门禁闭合。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: format-gate, review-refresh
- 依赖节点 ID: TP-01.01, TP-01.02
- 输入: 无
- 输出: local-ci quick evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：会暴露更多本地门禁失败，失败时转 auto-debug。
- 备注: 无

## TP-02
- Step Key: `production-constraints`
- 标题: 关闭生产准入约束缺口
- 类型: `package`
- 目标: 让公共服务发布前的静态和真实环境门禁可执行、可失败、可追溯。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02, TP-02.03
- 依赖步骤 Key: quick-local-ci
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
- Step Key: `production-env-contract`
- 标题: 固化生产 env 合同
- 类型: `action`
- 目标: 把 CORS、records、rate limit backend、edge body limit、proxy headers、HSTS 的生产配置要求写成可验证合同。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: production env checklist；readiness evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：生产配置错误会暴露公共服务。
- 备注: risk_level: high；affected_flows: public API, web, bot delivery；rollout: env-driven no code deployment first；rollback: revert env to previous known-good values

### TP-02.02
- Step Key: `public-service-local-ci`
- 标题: 恢复 local-ci public-service 绿色
- 类型: `action`
- 目标: 使用 scripts/local-ci.sh --profile public-service 验证生产静态准入路径。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: production-env-contract
- 依赖节点 ID: TP-02.01
- 输入: 无
- 输出: public-service local CI evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：环境默认值可能掩盖真实部署，需要 REVIEW 标明。
- 备注: 无

### TP-02.03
- Step Key: `external-live-readiness`
- 标题: 真实公网 API 与 Bot live 验收
- 类型: `action`
- 目标: 在真实域名/TLS/反向代理/生产 URL/真实 Bot token 下执行 live readiness。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: public-service-local-ci
- 依赖节点 ID: TP-02.02
- 输入: 无
- 输出: live API readiness evidence；live Bot evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 缺少 real-url 或 real bot token 时停止，不伪造证据。
- 风险: high：需要外部凭证和真实基础设施；缺失时 Blocked/HITL。
- 备注: 无

## TP-03
- Step Key: `edge-case-hardening`
- 标题: 补齐特殊情况与韧性
- 类型: `package`
- 目标: 把时区、真太阳时、节气、早晚子时、Bot 背压、多副本限流和异常输入变成测试化契约。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02, TP-03.03, TP-03.04
- 依赖步骤 Key: quick-local-ci
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
- Step Key: `timezone-contract`
- 标题: 定义并测试出生时间时区语义
- 类型: `action`
- 目标: 明确 naive、Z、+08:00、出生地时区和真太阳时之间的输入语义。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 时区语义契约；时区边界测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：可能改变当前解释，需要兼容说明。
- 备注: 无

### TP-03.02
- Step Key: `bot-backpressure`
- 标题: Bot 背压与滥用保护
- 类型: `action`
- 目标: 把 Bot 队列从近似无限等待改成有界并发、有界队列、用户级反馈和测试。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: Bot rate limiter contract；rate limiter tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：公共 Bot 滥用会影响可用性。
- 备注: 无

### TP-03.03
- Step Key: `api-guardrail-tests`
- 标题: API guardrails 特殊输入回归
- 类型: `action`
- 目标: 补齐请求体超限、无 Content-Length、超时、429、错误分类、安全头的回归测试。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: API guardrail regression tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：测试可能暴露 middleware 行为缺陷。
- 备注: 无

### TP-03.04
- Step Key: `calendar-boundary-golden`
- 标题: 历法边界 golden 扩展
- 类型: `action`
- 目标: 扩展节气边界、早晚子时、真太阳时、地域经纬度边界 golden case。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: timezone-contract
- 依赖节点 ID: TP-03.01
- 输入: 无
- 输出: calendar/bazi boundary golden cases
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：样本来源必须可追溯。
- 备注: 无

## TP-04
- Step Key: `explainability-bazi`
- 标题: 八字解释性与证据化补齐
- 类型: `package`
- 目标: 让核心命理判断具备可追溯 evidence、ruleIds、权重和风险边界。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02, TP-04.03, TP-04.04
- 依赖步骤 Key: quick-local-ci
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `evidence-coverage`
- 标题: 核心字段 evidence 覆盖审计
- 类型: `action`
- 目标: 审计 baziBenchmark、baziRuleDepth、analysisEvidence 的核心字段覆盖率。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: evidence coverage report；regression tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：证据覆盖不足会阻塞可解释 100%。
- 备注: 无

### TP-04.02
- Step Key: `bazi-golden-expand`
- 标题: 八字 golden case 扩展到 100+
- 类型: `action`
- 目标: 优先覆盖节气边界、早晚子时、特殊格局、合化、从格、岁运触发。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: calendar-boundary-golden, evidence-coverage
- 依赖节点 ID: TP-03.04, TP-04.01
- 输入: 无
- 输出: 100+ golden case manifest；golden regression suite
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：样本版权和专业可信度必须治理。
- 备注: 无

### TP-04.03
- Step Key: `topic-profile-validation`
- 标题: 专题 profile 评分验证
- 类型: `action`
- 目标: 验证事业、财运、婚姻、健康、学业、迁移 profile 不输出确定性断语。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: evidence-coverage
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: topic profile tests；risk wording checks
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：解释性增强不能越界成预测承诺。
- 备注: 无

### TP-04.04
- Step Key: `mingli-bench-gate`
- 标题: MingLi-Bench 评测门禁接入
- 类型: `action`
- 目标: 把 MingLi-Bench 作为报告/推理质量评测层，不作为生产排盘层。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: MingLi-Bench local evaluation evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: low：评测数据不应污染生产计算。
- 备注: 无

## TP-05
- Step Key: `maintainability-architecture`
- 标题: 长期维护性与 legacy 边界治理
- 类型: `package`
- 目标: 从大文件和 delivery legacy 中迁出领域核心，让 fate-core 成为命理能力真相源。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-05.05
- 依赖步骤 Key: quick-local-ci
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `boundary-map`
- 标题: 绘制核心大文件职责边界图
- 类型: `action`
- 目标: 给 bazi_calculator、report_generator、calculate_pure_analysis、bot、main、web_ui 建立职责地图和迁移 kill list。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: module boundary map；legacy kill list
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：错误边界会导致重构方向错误。
- 备注: Target end state: fate-core owns calculation/rules/evidence; delivery owns API/Web/Bot/report presentation.；Inertia constraints: existing import paths and legacy names must not define terminal architecture.；Kill list: scattered sys.path, delivery-owned domain rules, compatibility-only wrappers without public contract.

### TP-05.02
- Step Key: `split-pure-analysis`
- 标题: 拆分 calculate_pure_analysis 证据构建模块
- 类型: `action`
- 目标: 把输入归一化、benchmark、rule depth、topic profile 和 evidence append 拆到 fate-core 内部清晰模块。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: boundary-map, evidence-coverage
- 依赖节点 ID: TP-05.01, TP-04.01
- 输入: 无
- 输出: fate-core pure_analysis submodules；updated AGENTS.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：拆分可能引入循环 import。
- 备注: 无

### TP-05.03
- Step Key: `migrate-bazi-core`
- 标题: 迁移 BaziCalculator 领域核心到 fate-core
- 类型: `action`
- 目标: 逐步把历法、四柱、旺衰、格局、用神、岁运从 delivery 大类迁入 fate-core。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: boundary-map, bazi-golden-expand
- 依赖节点 ID: TP-05.01, TP-04.02
- 输入: 无
- 输出: fate-core bazi providers/evaluators；legacy adapter shrink plan
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：命理核心行为变化必须由 golden/oracle 解释。
- 备注: 无

### TP-05.04
- Step Key: `split-delivery-surfaces`
- 标题: 收敛 delivery 层 API/Web/Bot/报告边界
- 类型: `action`
- 目标: 把 main、web_ui、bot、report_generator 的交付职责分层，避免继续混入领域算法。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: boundary-map, bot-backpressure, api-guardrail-tests
- 依赖节点 ID: TP-05.01, TP-03.02, TP-03.03
- 输入: 无
- 输出: delivery boundary refactor slices；updated AGENTS.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：UI/报告输出必须保持契约。
- 备注: 无

### TP-05.05
- Step Key: `remove-legacy-shims`
- 标题: 清退无真实外部契约的 legacy/compat shim
- 类型: `action`
- 目标: 删除或收缩无真实公共 API、持久化数据、外部集成支撑的兼容层。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: migrate-bazi-core, split-delivery-surfaces
- 依赖节点 ID: TP-05.03, TP-05.04
- 输入: 无
- 输出: legacy removal diff；migration ledger update
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：删除前必须确认无外部调用方。
- 备注: 无

## TP-06
- Step Key: `reuse-supply-chain`
- 标题: 复用与供应链理解闭环
- 类型: `package`
- 目标: 确保外部库、参考仓、oracle 和规则材料都在正确边界内被复用。
- 父节点: `ROOT`
- 子节点: TP-06.01, TP-06.02, TP-06.03, TP-06.04
- 依赖步骤 Key: quick-local-ci
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.01
- Step Key: `calendar-provider-contract`
- 标题: CalendarProvider 生产依赖合同
- 类型: `action`
- 目标: 明确 lunar-python 为主生产历法底座，sxtwl/bazica/其他项目只作为 oracle 或参考。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: CalendarProvider contract；dependency tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：错误替换历法库会影响核心结果。
- 备注: 无

### TP-06.02
- Step Key: `reference-license-manifest`
- 标题: 参考源许可和用途 manifest
- 类型: `action`
- 目标: 为 bazi-1、MingLi-Bench、sxtwl、iztro、lunar-python 等建立许可/用途/风险清单。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: reference source manifest；license risk notes
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：许可不清会影响公共发布。
- 备注: 无

### TP-06.03
- Step Key: `oracle-harness`
- 标题: 历法/四柱 oracle 对照框架
- 类型: `action`
- 目标: 保留 sxtwl、bazica、alvamind 等作为对照 oracle，不进入主运行链。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: calendar-provider-contract, reference-license-manifest
- 依赖节点 ID: TP-06.01, TP-06.02
- 输入: 无
- 输出: oracle comparison harness
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：多 oracle 冲突需要记录裁决规则。
- 备注: 无

### TP-06.04
- Step Key: `rule-registry-governance`
- 标题: 规则 registry owner 和扩展规则
- 类型: `action`
- 目标: 明确 rule_depth_registry、classics_rule_index、future_features 的 owner、字段、升级 gate。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: evidence-coverage
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: rule registry governance note；policy tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：规则膨胀会降低可解释性。
- 备注: 无

## TP-07
- Step Key: `observability-operations`
- 标题: 公共服务观测和运行闭环
- 类型: `package`
- 目标: 把当前应用内 metrics/logs/readiness 扩展到真实运行平台可用的 SLO、告警和排障包。
- 父节点: `ROOT`
- 子节点: TP-07.01, TP-07.02, TP-07.03, TP-07.04
- 依赖步骤 Key: production-env-contract, api-guardrail-tests
- 依赖节点 ID: TP-02.01, TP-03.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-07.01
- Step Key: `metrics-dashboard`
- 标题: Prometheus/Grafana 指标和告警计划
- 类型: `action`
- 目标: 定义 p95/p99、错误率、429、413、504、inflight、Bot 队列等指标和告警阈值。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: metrics dashboard spec；alert runbook
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：没有外部 Prometheus 时只能保留平台接入待办。
- 备注: 无

### TP-07.02
- Step Key: `trace-log-correlation`
- 标题: 请求 ID 与业务日志贯穿
- 类型: `action`
- 目标: 确保 X-Request-ID 能关联 HTTP 日志、错误分类、业务计算失败和 Bot 交付。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: trace/log correlation tests or runbook
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：日志不得泄漏用户隐私。
- 备注: 无

### TP-07.03
- Step Key: `slo-runbook`
- 标题: SLO 与运维 runbook
- 类型: `action`
- 目标: 定义公共服务 SLO、降级策略、恢复步骤、清理本地 runtime 的流程。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: SLO/runbook update
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: low：文档必须跟脚本一致。
- 备注: 无

### TP-07.04
- Step Key: `run-local-ci-all`
- 标题: 本地全链路 CI/CD 汇总
- 类型: `action`
- 目标: 运行 quick/full/container/public-service 的本地 all profile，作为最终本地质量证据。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: public-service-local-ci, bot-backpressure, api-guardrail-tests, metrics-dashboard, slo-runbook
- 依赖节点 ID: TP-02.02, TP-03.02, TP-03.03, TP-07.01, TP-07.03
- 输入: 无
- 输出: local-ci all evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：container/public-service 失败会阻塞最终 100%。
- 备注: 无

## TP-08
- Step Key: `final-review-ship`
- 标题: 最终审查和交付收口
- 类型: `package`
- 目标: 用 auto-review 和任务 closeout 证明六项质量标准全部达到 100% gate。
- 父节点: `ROOT`
- 子节点: TP-08.01, TP-08.02, TP-08.03
- 依赖步骤 Key: run-local-ci-all, remove-legacy-shims, bazi-golden-expand, oracle-harness, external-live-readiness
- 依赖节点 ID: TP-07.04, TP-05.05, TP-04.02, TP-06.03, TP-02.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-08.01
- Step Key: `full-quality-review`
- 标题: 执行全仓质量审查
- 类型: `action`
- 目标: 按 correctness/security/reliability/performance/architecture/operability/repo-hygiene 做最终 review。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: final REVIEW.md；quality score matrix
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: high：review 发现 BLOCK 时不得 ship。
- 备注: 无

### TP-08.02
- Step Key: `fix-review-findings`
- 标题: 处理最终 review findings
- 类型: `action`
- 目标: 修复 full-quality-review 发现的 BLOCK，记录无法关闭的外部 blocker。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: full-quality-review
- 依赖节点 ID: TP-08.01
- 输入: 无
- 输出: review finding fix evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: medium：不得为了通过 review 删除必要保护。
- 备注: 无

### TP-08.03
- Step Key: `task-closeout`
- 标题: 生成任务 closeout 和交付证据
- 类型: `action`
- 目标: 把任务树、执行证据、质量矩阵、review 结论和剩余 HITL 状态收口。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: fix-review-findings
- 依赖节点 ID: TP-08.02
- 输入: 无
- 输出: Task Closeout Packet；handoff to auto-github/auto-assets/auto-governance
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: low：closeout 不等于 push，push 需 auto-github。
- 备注: 无
