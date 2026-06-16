# Execution Checklist

[x] TP-01.01 | P0 | 复核当前十维基线与 `0004` final review | Verify: rg '基础排盘|样本外 benchmark|Active BLOCK' governance/tasks/0004-bazi-professional-system-100 -n | Gate: current 百分比、WARN、禁止口径一致。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 复核外部资源准入与 license/source 边界 | Verify: rg 'production_dependency|oracle_only|evaluation_only|reference_only|future_candidate' governance/tasks/0004-bazi-professional-system-100/RESOURCE_MAP.md -n | Gate: 每个资源有 usageRole、productionUseAllowed、禁止用途。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 写入十维 100% gate 合同 | Verify: rg '100% 不是|100% 是|falsifier|target gate' governance/tasks/0005-bazi-capability-100-roadmap -n | Gate: 100% 不被解释成预测准确率 100%。 | Parallelizable: No
[x] TP-02.01 | P0 | CalendarProvider 升级合同 | Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q | Gate: production provider 与 oracle import 边界清楚。 | Parallelizable: Yes
[x] TP-02.02 | P0 | 扩展 calendar boundary corpus 到 >=50 | Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: 每个边界样本有 source、expected、tolerance、failureExplanation。 | Parallelizable: Yes
[x] TP-02.03 | P0 | oracle mismatch report | Verify: 生成 calendar mismatch report 并跑 local regression | Gate: 差异可解释；不可解释差异不得标绿。 | Parallelizable: No
[x] TP-03.01 | P0 | ruleId 覆盖强制门禁 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q | Gate: production 断语无未登记 ruleId。 | Parallelizable: Yes
[x] TP-03.02 | P0 | evidence/counterEvidence schema | Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q | Gate: 专业段落必须有 evidenceFields、riskBoundary、counterEvidence。 | Parallelizable: Yes
[x] TP-03.03 | P0 | 高风险输出 policy gate | Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q | Gate: 禁止医疗、金融、法律、心理、灾祸、婚姻确定断语。 | Parallelizable: No
[x] TP-04.01 | P1 | strength evaluator 物理拆分 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: schema 不变，delivery 不新增领域算法。 | Parallelizable: Yes
[x] TP-04.02 | P1 | ten-god evaluator 物理拆分 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 十神输出引用柱位、透干、藏干证据。 | Parallelizable: Yes
[x] TP-04.03 | P1 | regular-pattern/relation evaluator 拆分 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 不稳定格局输出 uncertainty，不强断。 | Parallelizable: No
[x] TP-05.01 | P0 | 高级格局 taxonomy 与 lifecycle | Verify: rg '从格|假从|专旺|化气|lifecycle' contracts/fate domains/fate-analysis -n | Gate: 每类高级格局有 appliesWhen/doesNotApplyWhen。 | Parallelizable: Yes
[x] TP-05.02 | P0 | 高级格局正反边界 golden | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 每类至少正例、反例、边界例；无样本保持 beta/HITL。 | Parallelizable: Yes
[x] TP-05.03 | P0 | guarded advanced-pattern evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 不满足条件时不得 production 强断。 | Parallelizable: No
[x] TP-06.01 | P0 | 合化条件链状态模型 | Verify: rg '合象|合而不化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n | Gate: 月令、透干、通根、阻隔、帮扶、冲破均可表达。 | Parallelizable: Yes
[x] TP-06.02 | P0 | transform evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 输出状态、证据和反证，不只输出“合化”。 | Parallelizable: No
[x] TP-06.03 | P0 | 破化/争合/阻隔反例矩阵 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 失败能定位具体 condition。 | Parallelizable: Yes
[x] TP-07.01 | P0 | 用神策略合同 | Verify: rg '调候|扶抑|通关|病药|格局用神|doesNotApplyWhen' contracts/fate governance/tasks -n | Gate: 每个策略有 basis、score、doesNotApplyWhen。 | Parallelizable: Yes
[x] TP-07.02 | P0 | 用神冲突排序 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 输出 ranking/conflicts，不输出唯一绝对结论。 | Parallelizable: No
[x] TP-07.03 | P0 | 用神反例与报告边界 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_statement_golden.py -q | Gate: 冲突样本解释 ranking 变化，报告保留边界。 | Parallelizable: Yes
[x] TP-08.01 | P0 | 岁运触发矩阵 | Verify: rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n | Gate: 动态触发只作趋势证据。 | Parallelizable: Yes
[x] TP-08.02 | P0 | P0 专题 profile evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 婚姻、事业、财运、家庭、健康、学业都有 score/basis/evidence/riskBoundary。 | Parallelizable: No
[x] TP-08.03 | P0 | 高风险专题 policy regression | Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q | Gate: 不输出确定未来、现实处方或恐吓式断语。 | Parallelizable: No
[ ] TP-09.01 | P0 | golden corpus 扩展目标 | Verify: 统计 calendar/rule-depth/statement/topic golden 数量并跑对应 pytest | Gate: calendar>=50, rule-depth>=120, statement>=80, P0 topic 每类>=20。 | Parallelizable: Yes
[ ] TP-09.02 | P0 | shard release gate | Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 逐 shard 跑 tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: shard 0..3 全通过；quick 不跑全量慢测。 | Parallelizable: Yes
[ ] TP-09.03 | P1 | mutation/schema regression | Verify: schema diff、API contract、policy regression 全过 | Gate: 字段缺失、规则缺证据、policy 失效时测试红。 | Parallelizable: No
[x] TP-10.01 | P0 | MingLi full no-leak gate | Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json | Gate: answered=160/160，predictions 无 expected/answer/correct/gold/label。 | Parallelizable: Yes
[x] TP-10.02 | P0 | failure-driven rule backlog | Verify: MINGLI_FAILURE_TAXONOMY 每类 failure 有 owner、缺口、回炉方向、禁止路径 | Gate: 禁止按 question_id/答案/选项调参。 | Parallelizable: No
[x] TP-10.03 | P1 | BaziQA admission gate | Verify: license、schema、adapter、privacy、no-runtime 审查文档 | Gate: license/source 不清时保持 future_candidate/evaluation_only。 | Parallelizable: Yes
[ ] TP-11.01 | P1 | evaluator 物理拆分收口 | Verify: rg 'build_.*evaluator|fate_core.usecases.evaluators' domains/fate-analysis/services/fate-core/src -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: pattern/hehua/yongshen/topic 等切片从大函数迁出。 | Parallelizable: No
[ ] TP-11.02 | P0 | Web/API/Markdown 消费边界 | Verify: .venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py -q | Gate: delivery 不重算命理规则，不泄漏内部 lifecycle 字段。 | Parallelizable: No
[ ] TP-11.03 | P0 | final local release gate | Verify: bash scripts/local-ci.sh --profile quick && bash scripts/local-ci.sh --profile full | Gate: Active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造公网/live bot。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
