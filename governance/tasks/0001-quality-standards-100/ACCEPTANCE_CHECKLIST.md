# Acceptance Checklist

# Global Standards
- [ ] 满足约束 100%：format、lint、typecheck、pytest、structure、source hygiene、privacy、local-ci quick/full 均 PASS，REVIEW.md 与当前 HEAD 一致。
- [ ] 可解释 100%：生产输出的核心判断都有 evidence、ruleIds、source、weight、risk boundary，ruleIds 全部能回指 classics/rule registry。
- [ ] 可测试 100%：关键能力、特殊时间边界、生产 guardrails、Bot 背压、容器、public-service readiness 和外部 live smoke 都有测试或验收证据。
- [ ] 可维护 100%：核心 legacy 边界被收敛，fate-core 与 delivery 职责清晰，大文件不再继续承担新增领域规则。
- [ ] 处理特殊情况 100%：时区、真太阳时、节气边界、早晚子时、异常输入、超大请求、多副本限流、Bot 高峰队列都有明确行为。
- [ ] 复用建立在理解上 100%：lunar-python、sxtwl、iztro、bazi-1、MingLi-Bench 的角色、许可、生产/评测边界和回归 oracle 均明确。

# Task Package Checklists
## TP-01
- 标题: 修复当前本地质量阻塞
- 验收项:
  - [ ] 达成 `修复当前本地质量阻塞` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 先把当前已知 BLOCK 清零，恢复本地 CI 可信度。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 修复 ruff format gate
- 验收项:
  - [ ] ruff check 和 format check 均 PASS。
- Verify: .venv/bin/python -m ruff format --check .
- Gate: format check 0 退出码，git diff 只包含格式化变更。
- 输出物:
  - [ ] 格式化后的 calculate_pure_analysis.py
  - [ ] 格式化后的 test_bazi_ziwei_rule_depth.py
- 标准清单:
  - [ ] Verify: .venv/bin/python -m ruff format --check .
  - [ ] Gate: format check 0 退出码，git diff 只包含格式化变更。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-01.02
- 标题: 刷新 REVIEW.md 质量真相源
- 验收项:
  - [ ] REVIEW.md 明确区分本地 PASS、生产配置 FAIL、外部 live 未执行。
- Verify: 人工核对 REVIEW.md 中 HEAD、测试数量、门禁状态与命令输出一致。
- Gate: REVIEW.md 不再写旧 HEAD、旧 120 passed 或无 env 的 production-readiness PASS。
- 输出物:
  - [ ] REVIEW.md 当前质量记录
- 标准清单:
  - [ ] Verify: 人工核对 REVIEW.md 中 HEAD、测试数量、门禁状态与命令输出一致。
  - [ ] Gate: REVIEW.md 不再写旧 HEAD、旧 120 passed 或无 env 的 production-readiness PASS。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.03
- 标题: 恢复 local-ci quick 绿色
- 验收项:
  - [ ] shell、preflight、structure、source hygiene、privacy、ruff、format、mypy、focused tests、diff check 全通过。
- Verify: bash scripts/local-ci.sh --profile quick
- Gate: quick profile PASS，summary/evidence 目录存在。
- 输出物:
  - [ ] local-ci quick evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile quick
  - [ ] Gate: quick profile PASS，summary/evidence 目录存在。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 关闭生产准入约束缺口
- 验收项:
  - [ ] 达成 `关闭生产准入约束缺口` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: quick-local-ci
- 输出物:
  - [ ] 让公共服务发布前的静态和真实环境门禁可执行、可失败、可追溯。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: quick-local-ci
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 固化生产 env 合同
- 验收项:
  - [ ] FATE_CORS_ALLOW_ORIGINS 非空且非 *；多副本不使用 memory 限流；edge/proxy/HSTS 口径清楚。
- Verify: bash scripts/production-readiness.sh --skip-bootstrap 在生产等价 env 下通过。
- Gate: 无生产等价 env 时保持 FAIL；有 env 时 PASS 且 WARN 项有明确归属。
- 输出物:
  - [ ] production env checklist
  - [ ] readiness evidence
- 标准清单:
  - [ ] Verify: bash scripts/production-readiness.sh --skip-bootstrap 在生产等价 env 下通过。
  - [ ] Gate: 无生产等价 env 时保持 FAIL；有 env 时 PASS 且 WARN 项有明确归属。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 恢复 local-ci public-service 绿色
- 验收项:
  - [ ] 本地 public-service readiness PASS；外部 live 项清晰 SKIP 或 HITL。
- Verify: bash scripts/local-ci.sh --profile public-service
- Gate: public-service profile PASS，且没有伪造外部 URL/Bot live 通过。
- 输出物:
  - [ ] public-service local CI evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile public-service
  - [ ] Gate: public-service profile PASS，且没有伪造外部 URL/Bot live 通过。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 真实公网 API 与 Bot live 验收
- 验收项:
  - [ ] 真实公网验收 PASS 后，公共生产服务稳定性才可从 55% 提升到 100%。
- Verify: bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
- Gate: 真实 /health、/ready、/metrics 和 Telegram get_me 通过；无 placeholder token。
- 输出物:
  - [ ] live API readiness evidence
  - [ ] live Bot evidence
- 标准清单:
  - [ ] Verify: bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot
  - [ ] Gate: 真实 /health、/ready、/metrics 和 Telegram get_me 通过；无 placeholder token。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 补齐特殊情况与韧性
- 验收项:
  - [ ] 达成 `补齐特殊情况与韧性` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: quick-local-ci
- 输出物:
  - [ ] 把时区、真太阳时、节气、早晚子时、Bot 背压、多副本限流和异常输入变成测试化契约。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: quick-local-ci
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 定义并测试出生时间时区语义
- 验收项:
  - [ ] Z/+08:00/无时区输入各自有明确预期。
- Verify: pytest 覆盖 parse_datetime、CLI、API、pure-analysis 的时区边界。
- Gate: 带时区输入不会被静默 replace 成错误本地时间，文档说明清楚。
- 输出物:
  - [ ] 时区语义契约
  - [ ] 时区边界测试
- 标准清单:
  - [ ] Verify: pytest 覆盖 parse_datetime、CLI、API、pure-analysis 的时区边界。
  - [ ] Gate: 带时区输入不会被静默 replace 成错误本地时间，文档说明清楚。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: Bot 背压与滥用保护
- 验收项:
  - [ ] QUEUE_MAX_SIZE 有生产合理默认值；拒绝原因可测试。
- Verify: pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py
- Gate: 高峰请求不会无限排队；用户冷却/每日限额是否启用有明确产品口径。
- 输出物:
  - [ ] Bot rate limiter contract
  - [ ] rate limiter tests
- 标准清单:
  - [ ] Verify: pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py
  - [ ] Gate: 高峰请求不会无限排队；用户冷却/每日限额是否启用有明确产品口径。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: API guardrails 特殊输入回归
- 验收项:
  - [ ] 413/429/504/安全头/metrics error_class 均有可验证路径。
- Verify: pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- Gate: 公共 API 护栏行为被测试锁住。
- 输出物:
  - [ ] API guardrail regression tests
- 标准清单:
  - [ ] Verify: pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py
  - [ ] Gate: 公共 API 护栏行为被测试锁住。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-03.04
- 标题: 历法边界 golden 扩展
- 验收项:
  - [ ] 边界样本来源、预期结果、oracle 说明齐全。
- Verify: pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py
- Gate: 关键历法边界至少有项目 golden 和 oracle 来源。
- 输出物:
  - [ ] calendar/bazi boundary golden cases
- 标准清单:
  - [ ] Verify: pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py
  - [ ] Gate: 关键历法边界至少有项目 golden 和 oracle 来源。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 八字解释性与证据化补齐
- 验收项:
  - [ ] 达成 `八字解释性与证据化补齐` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: quick-local-ci
- 输出物:
  - [ ] 让核心命理判断具备可追溯 evidence、ruleIds、权重和风险边界。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: quick-local-ci
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 核心字段 evidence 覆盖审计
- 验收项:
  - [ ] ruleIds 全部能回指 contracts/fate/classics_rule_index.json 或 rule_depth_registry.json。
- Verify: 新增或运行 evidence coverage 测试，确认核心字段均有 ruleIds/source/risk。
- Gate: 无孤儿 ruleId，无核心判断缺 evidence。
- 输出物:
  - [ ] evidence coverage report
  - [ ] regression tests
- 标准清单:
  - [ ] Verify: 新增或运行 evidence coverage 测试，确认核心字段均有 ruleIds/source/risk。
  - [ ] Gate: 无孤儿 ruleId，无核心判断缺 evidence。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 八字 golden case 扩展到 100+
- 验收项:
  - [ ] 八字证据化能力从 70% 提升到可审查 100%。
- Verify: pytest 运行新增 golden suite；样本 manifest 通过许可和来源审查。
- Gate: 100+ 样本都有来源、预期、覆盖标签和失败解释路径。
- 输出物:
  - [ ] 100+ golden case manifest
  - [ ] golden regression suite
- 标准清单:
  - [ ] Verify: pytest 运行新增 golden suite；样本 manifest 通过许可和来源审查。
  - [ ] Gate: 100+ 样本都有来源、预期、覆盖标签和失败解释路径。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 专题 profile 评分验证
- 验收项:
  - [ ] 报告透明但不恐吓、不替代现实决策。
- Verify: pytest tests/regression/test_bazi_ziwei_rule_depth.py
- Gate: profile 只作为 evidence_seed，输出有 riskBoundary。
- 输出物:
  - [ ] topic profile tests
  - [ ] risk wording checks
- 标准清单:
  - [ ] Verify: pytest tests/regression/test_bazi_ziwei_rule_depth.py
  - [ ] Gate: profile 只作为 evidence_seed，输出有 riskBoundary。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.04
- 标题: MingLi-Bench 评测门禁接入
- 验收项:
  - [ ] 评测层和生产层边界清晰。
- Verify: bash scripts/run-mingli-bench.sh --stats 和离线 sample evaluation。
- Gate: 评测结果进入 REVIEW/quality report，且不调用外部模型 API。
- 输出物:
  - [ ] MingLi-Bench local evaluation evidence
- 标准清单:
  - [ ] Verify: bash scripts/run-mingli-bench.sh --stats 和离线 sample evaluation。
  - [ ] Gate: 评测结果进入 REVIEW/quality report，且不调用外部模型 API。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 长期维护性与 legacy 边界治理
- 验收项:
  - [ ] 达成 `长期维护性与 legacy 边界治理` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: quick-local-ci
- 输出物:
  - [ ] 从大文件和 delivery legacy 中迁出领域核心，让 fate-core 成为命理能力真相源。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: quick-local-ci
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 绘制核心大文件职责边界图
- 验收项:
  - [ ] 后续任务不再靠猜测拆大文件。
- Verify: 生成边界文档并通过 auto-review architecture/ponytail 审查。
- Gate: 每个大文件都有保留职责、迁出职责、禁止新增职责。
- 输出物:
  - [ ] module boundary map
  - [ ] legacy kill list
- 标准清单:
  - [ ] Verify: 生成边界文档并通过 auto-review architecture/ponytail 审查。
  - [ ] Gate: 每个大文件都有保留职责、迁出职责、禁止新增职责。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 拆分 calculate_pure_analysis 证据构建模块
- 验收项:
  - [ ] 新增八字规则不必继续堆进单一 1400+ 行文件。
- Verify: pytest tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_bazi_ziwei_rule_depth.py
- Gate: 外部 API 输出不变，模块边界变清楚。
- 输出物:
  - [ ] fate-core pure_analysis submodules
  - [ ] updated AGENTS.md
- 标准清单:
  - [ ] Verify: pytest tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_bazi_ziwei_rule_depth.py
  - [ ] Gate: 外部 API 输出不变，模块边界变清楚。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.03
- 标题: 迁移 BaziCalculator 领域核心到 fate-core
- 验收项:
  - [ ] 长期维护性从 58% 提升到可审查 100% 的核心切片。
- Verify: golden suite、API contracts、web html、pure-analysis smoke 全通过。
- Gate: delivery 不再是八字领域算法真相源；legacy adapter 只剩迁移窗口和删除条件。
- 输出物:
  - [ ] fate-core bazi providers/evaluators
  - [ ] legacy adapter shrink plan
- 标准清单:
  - [ ] Verify: golden suite、API contracts、web html、pure-analysis smoke 全通过。
  - [ ] Gate: delivery 不再是八字领域算法真相源；legacy adapter 只剩迁移窗口和删除条件。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.04
- 标题: 收敛 delivery 层 API/Web/Bot/报告边界
- 验收项:
  - [ ] Web/Bot/API 改动不会迫使领域算法同文件变更。
- Verify: pytest delivery tests + tests/regression/test_web_html.py + API contract tests。
- Gate: 交付层只负责编排、渲染和传输，不新增命理规则。
- 输出物:
  - [ ] delivery boundary refactor slices
  - [ ] updated AGENTS.md
- 标准清单:
  - [ ] Verify: pytest delivery tests + tests/regression/test_web_html.py + API contract tests。
  - [ ] Gate: 交付层只负责编排、渲染和传输，不新增命理规则。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.05
- 标题: 清退无真实外部契约的 legacy/compat shim
- 验收项:
  - [ ] future-optimal-drift 不再因 active legacy 边界触发真实 BLOCK。
- Verify: scan_principle_gates 过滤源码后无真实 BLOCK；structure gate 无 legacy_source_root。
- Gate: 保留的 compat 都有 owner、移除条件和真实 contract。
- 输出物:
  - [ ] legacy removal diff
  - [ ] migration ledger update
- 标准清单:
  - [ ] Verify: scan_principle_gates 过滤源码后无真实 BLOCK；structure gate 无 legacy_source_root。
  - [ ] Gate: 保留的 compat 都有 owner、移除条件和真实 contract。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 复用与供应链理解闭环
- 验收项:
  - [ ] 达成 `复用与供应链理解闭环` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: quick-local-ci
- 输出物:
  - [ ] 确保外部库、参考仓、oracle 和规则材料都在正确边界内被复用。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: quick-local-ci
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: CalendarProvider 生产依赖合同
- 验收项:
  - [ ] 复用建立在理解上：生产、oracle、参考三类边界清晰。
- Verify: 依赖文件、adapter、文档和测试一致声明 lunar-python 生产角色。
- Gate: 没有隐式 vendor 依赖或重复自研历法算法。
- 输出物:
  - [ ] CalendarProvider contract
  - [ ] dependency tests
- 标准清单:
  - [ ] Verify: 依赖文件、adapter、文档和测试一致声明 lunar-python 生产角色。
  - [ ] Gate: 没有隐式 vendor 依赖或重复自研历法算法。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 参考源许可和用途 manifest
- 验收项:
  - [ ] 参考材料和生产代码边界可审计。
- Verify: vendor/reference manifest 通过治理审查。
- Gate: 无明确 LICENSE 的材料不得作为生产依赖扩散。
- 输出物:
  - [ ] reference source manifest
  - [ ] license risk notes
- 标准清单:
  - [ ] Verify: vendor/reference manifest 通过治理审查。
  - [ ] Gate: 无明确 LICENSE 的材料不得作为生产依赖扩散。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.03
- 标题: 历法/四柱 oracle 对照框架
- 验收项:
  - [ ] 复用不变成多主链或重复造轮子。
- Verify: oracle 对照测试只在评测/开发门禁运行，不污染生产路径。
- Gate: 生产路径仍以 CalendarProvider 为单一入口。
- 输出物:
  - [ ] oracle comparison harness
- 标准清单:
  - [ ] Verify: oracle 对照测试只在评测/开发门禁运行，不污染生产路径。
  - [ ] Gate: 生产路径仍以 CalendarProvider 为单一入口。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.04
- 标题: 规则 registry owner 和扩展规则
- 验收项:
  - [ ] 规则扩展不靠散落代码或口头解释。
- Verify: policy asset tests 覆盖新增规则字段和禁止项。
- Gate: 新增规则必须有 source、appliesWhen、doesNotApplyWhen、risk boundary。
- 输出物:
  - [ ] rule registry governance note
  - [ ] policy tests
- 标准清单:
  - [ ] Verify: policy asset tests 覆盖新增规则字段和禁止项。
  - [ ] Gate: 新增规则必须有 source、appliesWhen、doesNotApplyWhen、risk boundary。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 公共服务观测和运行闭环
- 验收项:
  - [ ] 达成 `公共服务观测和运行闭环` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: production-env-contract, api-guardrail-tests
- 输出物:
  - [ ] 把当前应用内 metrics/logs/readiness 扩展到真实运行平台可用的 SLO、告警和排障包。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: production-env-contract, api-guardrail-tests
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: Prometheus/Grafana 指标和告警计划
- 验收项:
  - [ ] 生产稳定性有可观测证据。
- Verify: metrics 输出包含必要 label，runbook 说明告警触发和处理。
- Gate: 公共服务可从指标判断健康，而不是只看 /health。
- 输出物:
  - [ ] metrics dashboard spec
  - [ ] alert runbook
- 标准清单:
  - [ ] Verify: metrics 输出包含必要 label，runbook 说明告警触发和处理。
  - [ ] Gate: 公共服务可从指标判断健康，而不是只看 /health。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.02
- 标题: 请求 ID 与业务日志贯穿
- 验收项:
  - [ ] 排障不依赖猜测。
- Verify: API/Bot 错误路径日志包含 requestId 或等价 trace id。
- Gate: 出现 5xx/timeout 时可定位到请求和错误类型。
- 输出物:
  - [ ] trace/log correlation tests or runbook
- 标准清单:
  - [ ] Verify: API/Bot 错误路径日志包含 requestId 或等价 trace id。
  - [ ] Gate: 出现 5xx/timeout 时可定位到请求和错误类型。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: SLO 与运维 runbook
- 验收项:
  - [ ] 生产故障有操作路径。
- Verify: runbook 被 REVIEW.md 和 references/ops-pack.md 引用。
- Gate: 上线、回滚、降级、清理 runtime 都有可执行命令。
- 输出物:
  - [ ] SLO/runbook update
- 标准清单:
  - [ ] Verify: runbook 被 REVIEW.md 和 references/ops-pack.md 引用。
  - [ ] Gate: 上线、回滚、降级、清理 runtime 都有可执行命令。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.04
- 标题: 本地全链路 CI/CD 汇总
- 验收项:
  - [ ] 本地开发质量、结构治理、公共服务静态门禁达到 100%。
- Verify: bash scripts/local-ci.sh --profile all
- Gate: all profile PASS；若 Docker 或外部凭证缺失，必须拆分记录真实 blocker。
- 输出物:
  - [ ] local-ci all evidence
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile all
  - [ ] Gate: all profile PASS；若 Docker 或外部凭证缺失，必须拆分记录真实 blocker。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 最终审查和交付收口
- 验收项:
  - [ ] 达成 `最终审查和交付收口` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: run-local-ci-all, remove-legacy-shims, bazi-golden-expand, oracle-harness, external-live-readiness
- 输出物:
  - [ ] 用 auto-review 和任务 closeout 证明六项质量标准全部达到 100% gate。
- 标准清单:
  - [ ] Verify: 确认子节点范围、依赖与状态闭环
  - [ ] Gate: 前置步骤已完成: run-local-ci-all, remove-legacy-shims, bazi-golden-expand, oracle-harness, external-live-readiness
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.01
- 标题: 执行全仓质量审查
- 验收项:
  - [ ] 综合质量从 72% 提升到 100% 的证据闭环。
- Verify: auto-review 输出无 BLOCK，WARN 有 owner 和后续任务。
- Gate: 六项质量标准都有 PASS 证据。
- 输出物:
  - [ ] final REVIEW.md
  - [ ] quality score matrix
- 标准清单:
  - [ ] Verify: auto-review 输出无 BLOCK，WARN 有 owner 和后续任务。
  - [ ] Gate: 六项质量标准都有 PASS 证据。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.02
- 标题: 处理最终 review findings
- 验收项:
  - [ ] 无阻塞风险进入最终 closeout。
- Verify: 复跑触发 finding 的最小验证命令。
- Gate: 所有 BLOCK=0；WARN 不影响 100% gate 或被显式排除。
- 输出物:
  - [ ] review finding fix evidence
- 标准清单:
  - [ ] Verify: 复跑触发 finding 的最小验证命令。
  - [ ] Gate: 所有 BLOCK=0；WARN 不影响 100% gate 或被显式排除。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-08.03
- 标题: 生成任务 closeout 和交付证据
- 验收项:
  - [ ] 任务级 closeout 可交接，可恢复，可审计。
- Verify: validate_task_docs.py --phase closeout；必要时 build_task_closeout.py。
- Gate: TODO 全部完成，STATUS 全部 Done 或外部 HITL 明确 Blocked，质量 100% 不含伪证。
- 输出物:
  - [ ] Task Closeout Packet
  - [ ] handoff to auto-github/auto-assets/auto-governance
- 标准清单:
  - [ ] Verify: validate_task_docs.py --phase closeout；必要时 build_task_closeout.py。
  - [ ] Gate: TODO 全部完成，STATUS 全部 Done 或外部 HITL 明确 Blocked，质量 100% 不含伪证。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
