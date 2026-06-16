# Execution Checklist
[x] TP-01.01 | P0 | 修复 ruff format gate | Verify: .venv/bin/python -m ruff format --check . | Gate: format check 0 退出码，git diff 只包含格式化变更。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 刷新 REVIEW.md 质量真相源 | Verify: 人工核对 REVIEW.md 中 HEAD、测试数量、门禁状态与命令输出一致。 | Gate: REVIEW.md 不再写旧 HEAD、旧 120 passed 或无 env 的 production-readiness PASS。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 恢复 local-ci quick 绿色 | Verify: bash scripts/local-ci.sh --profile quick | Gate: quick profile PASS，summary/evidence 目录存在。 | Parallelizable: No
[x] TP-02.01 | P0 | 固化生产 env 合同 | Verify: bash scripts/production-readiness.sh --skip-bootstrap 在生产等价 env 下通过。 | Gate: 无生产等价 env 时保持 FAIL；有 env 时 PASS 且 WARN 项有明确归属。 | Parallelizable: Yes
[x] TP-02.02 | P0 | 恢复 local-ci public-service 绿色 | Verify: bash scripts/local-ci.sh --profile public-service | Gate: public-service profile PASS，且没有伪造外部 URL/Bot live 通过。 | Parallelizable: No
[ ] TP-02.03 | P0 | 真实公网 API 与 Bot live 验收 | Verify: bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot | Gate: 真实 /health、/ready、/metrics 和 Telegram get_me 通过；无 placeholder token。 | Parallelizable: No
[x] TP-03.01 | P0 | 定义并测试出生时间时区语义 | Verify: pytest 覆盖 parse_datetime、CLI、API、pure-analysis 的时区边界。 | Gate: 带时区输入不会被静默 replace 成错误本地时间，文档说明清楚。 | Parallelizable: Yes
[x] TP-03.02 | P0 | Bot 背压与滥用保护 | Verify: pytest domains/experience-delivery/services/fatecat-delivery/tests/test_rate_limiter.py | Gate: 高峰请求不会无限排队；用户冷却/每日限额是否启用有明确产品口径。 | Parallelizable: Yes
[x] TP-03.03 | P0 | API guardrails 特殊输入回归 | Verify: pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py | Gate: 公共 API 护栏行为被测试锁住。 | Parallelizable: Yes
[x] TP-03.04 | P1 | 历法边界 golden 扩展 | Verify: pytest tests/regression/test_solar_terms_golden.py tests/regression/test_bazi_statement_golden.py | Gate: 关键历法边界至少有项目 golden 和 oracle 来源。 | Parallelizable: Yes
[x] TP-04.01 | P1 | 核心字段 evidence 覆盖审计 | Verify: 新增或运行 evidence coverage 测试，确认核心字段均有 ruleIds/source/risk。 | Gate: 无孤儿 ruleId，无核心判断缺 evidence。 | Parallelizable: Yes
[x] TP-04.02 | P1 | 八字 golden case 扩展到 100+ | Verify: pytest 运行新增 golden suite；样本 manifest 通过许可和来源审查。 | Gate: 100+ 样本都有来源、预期、覆盖标签和失败解释路径。 | Parallelizable: No
[x] TP-04.03 | P1 | 专题 profile 评分验证 | Verify: pytest tests/regression/test_bazi_ziwei_rule_depth.py | Gate: profile 只作为 evidence_seed，输出有 riskBoundary。 | Parallelizable: Yes
[x] TP-04.04 | P2 | MingLi-Bench 评测门禁接入 | Verify: bash scripts/run-mingli-bench.sh --stats 和离线 sample evaluation。 | Gate: 评测结果进入 REVIEW/quality report，且不调用外部模型 API。 | Parallelizable: Yes
[x] TP-05.01 | P1 | 绘制核心大文件职责边界图 | Verify: 生成边界文档并通过 auto-review architecture/ponytail 审查。 | Gate: 每个大文件都有保留职责、迁出职责、禁止新增职责。 | Parallelizable: No
[x] TP-05.02 | P1 | 拆分 calculate_pure_analysis 证据构建模块 | Verify: pytest tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_bazi_ziwei_rule_depth.py | Gate: 外部 API 输出不变，模块边界变清楚。 | Parallelizable: No
[x] TP-05.03 | P1 | 迁移 BaziCalculator 领域核心到 fate-core | Verify: golden suite、API contracts、web html、pure-analysis smoke 全通过。 | Gate: delivery 不再是八字领域算法真相源；legacy adapter 只剩迁移窗口和删除条件。 | Parallelizable: No
[x] TP-05.04 | P1 | 收敛 delivery 层 API/Web/Bot/报告边界 | Verify: pytest delivery tests + tests/regression/test_web_html.py + API contract tests。 | Gate: 交付层只负责编排、渲染和传输，不新增命理规则。 | Parallelizable: No
[x] TP-05.05 | P1 | 清退无真实外部契约的 legacy/compat shim | Verify: scan_principle_gates 过滤源码后无真实 BLOCK；structure gate 无 legacy_source_root。 | Gate: 保留的 compat 都有 owner、移除条件和真实 contract。 | Parallelizable: No
[x] TP-06.01 | P1 | CalendarProvider 生产依赖合同 | Verify: 依赖文件、adapter、文档和测试一致声明 lunar-python 生产角色。 | Gate: 没有隐式 vendor 依赖或重复自研历法算法。 | Parallelizable: Yes
[x] TP-06.02 | P1 | 参考源许可和用途 manifest | Verify: vendor/reference manifest 通过治理审查。 | Gate: 无明确 LICENSE 的材料不得作为生产依赖扩散。 | Parallelizable: Yes
[x] TP-06.03 | P2 | 历法/四柱 oracle 对照框架 | Verify: oracle 对照测试只在评测/开发门禁运行，不污染生产路径。 | Gate: 生产路径仍以 CalendarProvider 为单一入口。 | Parallelizable: Yes
[x] TP-06.04 | P1 | 规则 registry owner 和扩展规则 | Verify: policy asset tests 覆盖新增规则字段和禁止项。 | Gate: 新增规则必须有 source、appliesWhen、doesNotApplyWhen、risk boundary。 | Parallelizable: Yes
[x] TP-07.01 | P1 | Prometheus/Grafana 指标和告警计划 | Verify: metrics 输出包含必要 label，runbook 说明告警触发和处理。 | Gate: 公共服务可从指标判断健康，而不是只看 /health。 | Parallelizable: Yes
[x] TP-07.02 | P1 | 请求 ID 与业务日志贯穿 | Verify: API/Bot 错误路径日志包含 requestId 或等价 trace id。 | Gate: 出现 5xx/timeout 时可定位到请求和错误类型。 | Parallelizable: Yes
[x] TP-07.03 | P1 | SLO 与运维 runbook | Verify: runbook 被 REVIEW.md 和 references/ops-pack.md 引用。 | Gate: 上线、回滚、降级、清理 runtime 都有可执行命令。 | Parallelizable: Yes
[x] TP-07.04 | P0 | 本地全链路 CI/CD 汇总 | Verify: bash scripts/local-ci.sh --profile all | Gate: all profile PASS；若 Docker 或外部凭证缺失，必须拆分记录真实 blocker。 | Parallelizable: No
[ ] TP-08.01 | P0 | 执行全仓质量审查 | Verify: auto-review 输出无 BLOCK，WARN 有 owner 和后续任务。 | Gate: 六项质量标准都有 PASS 证据。 | Parallelizable: No
[ ] TP-08.02 | P0 | 处理最终 review findings | Verify: 复跑触发 finding 的最小验证命令。 | Gate: 所有 BLOCK=0；WARN 不影响 100% gate 或被显式排除。 | Parallelizable: No
[ ] TP-08.03 | P0 | 生成任务 closeout 和交付证据 | Verify: validate_task_docs.py --phase closeout；必要时 build_task_closeout.py。 | Gate: TODO 全部完成，STATUS 全部 Done 或外部 HITL 明确 Blocked，质量 100% 不含伪证。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
