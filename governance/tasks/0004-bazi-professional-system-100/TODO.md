# Execution Checklist
[x] TP-01.01 | P0 | 刷新八字 100% Scorecard | Verify: 人工核对 SCORECARD 与当前完成度表、MINGLI_FULL_EVALUATION、RULE_SOURCE_GAPS 一致。 | Gate: 每个维度都有 current、target、verify、falsifier、owner、next threshold。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 刷新资源地图和复用边界 | Verify: rg 'usageRole|production_dependency|oracle_only|evaluation_only|reference_only' governance/tasks contracts tools -n | Gate: production/oracle/evaluation/reference/future_candidate 边界不混写。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 建立规则来源缺口台账 | Verify: rg 'GAP-BZ-' governance/tasks/0004-bazi-professional-system-100 governance/tasks/0003-bazi-system-100 -n | Gate: 高级格局、合化、用神、岁运、专题、benchmark 均有 gap id。 | Parallelizable: No
[x] TP-02.01 | P0 | 扩展 calendar boundary matrix | Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q | Gate: 新增样本都有 source、expected、tolerance、failureExplanation。 | Parallelizable: Yes
[x] TP-02.02 | P0 | 锁定 CalendarProvider 升级合同 | Verify: rg 'lunar-python|sxtwl|oracle_only|CalendarProvider' requirements*.txt pyproject.toml contracts governance tests -n | Gate: 生产入口不 import oracle；依赖文件声明与锁文件一致。 | Parallelizable: Yes
[x] TP-02.03 | P0 | 基础排盘回归矩阵 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_api_contracts.py -q | Gate: 基础字段 schema diff 为零或有迁移说明。 | Parallelizable: No
[x] TP-03.01 | P0 | 补齐 ruleId 覆盖审计 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q | Gate: 未登记断语不能进入 production 报告。 | Parallelizable: Yes
[x] TP-03.02 | P0 | 标准化 evidenceFields 合同 | Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q | Gate: 新增字段不破坏现有 API/Web/Markdown 消费者。 | Parallelizable: Yes
[x] TP-03.03 | P0 | 高风险输出边界回归 | Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q | Gate: 高风险词和保证式话术被 policy regression 拦截。 | Parallelizable: No
[x] TP-04.01 | P0 | 强弱与月令 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: strength 输出包含 score、basis、sourceRuleId、conflicts。 | Parallelizable: Yes
[x] TP-04.02 | P0 | 十神结构 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 十神解释必须引用盘面证据，不输出孤立断语。 | Parallelizable: Yes
[x] TP-04.03 | P0 | 常规格局 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_statement_golden.py -q | Gate: 无法稳定判定时输出 uncertainty，不强断。 | Parallelizable: No
[x] TP-05.01 | P0 | 高级格局规则矩阵 | Verify: rg '从格|假从|专旺|化气|specialPattern' contracts/fate domains/fate-analysis -n | Gate: 每类高级格局至少有成立条件和反证条件。 | Parallelizable: Yes
[x] TP-05.02 | P0 | 高级格局正反例 golden | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: 无 golden 的高级格局不能升 production。 | Parallelizable: Yes
[x] TP-05.03 | P0 | 高级格局 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: evaluator 不依赖 delivery；输出 schema 稳定。 | Parallelizable: No
[x] TP-06.01 | P0 | 干支关系条件目录 | Verify: rg '合化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n | Gate: 每种关系状态都有 required evidenceFields。 | Parallelizable: Yes
[x] TP-06.02 | P0 | 合化状态链 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 每个 transform state 都有证据和反证条件。 | Parallelizable: No
[x] TP-06.03 | P0 | 合化反例矩阵 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 反例失败时能定位到具体 condition。 | Parallelizable: No
[x] TP-07.01 | P0 | 用神策略矩阵 | Verify: rg '调候|扶抑|通关|病药|用神' contracts/fate governance/tasks -n | Gate: 每个 strategy 都有 basis、score、doesNotApplyWhen。 | Parallelizable: Yes
[x] TP-07.02 | P0 | 用神决策 evaluator | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q | Gate: 冲突裁决可解释，不输出唯一绝对结论。 | Parallelizable: No
[x] TP-07.03 | P0 | 用神冲突正反例 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: 冲突 golden 可以解释 ranking 变化。 | Parallelizable: No
[x] TP-08.01 | P0 | 岁运触发矩阵 | Verify: rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n | Gate: 动态触发只作为趋势证据，不输出确定未来。 | Parallelizable: Yes
[x] TP-08.02 | P0 | 专题 profile 联合评分 | Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q | Gate: topicProfiles.lifecycle=production 之前必须有 golden 和 policy regression。 | Parallelizable: No
[x] TP-08.03 | P0 | 专题风险边界 | Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q | Gate: 高风险专题不输出现实处方、保证、恐吓或法律金融医疗建议。 | Parallelizable: No
[x] TP-09.01 | P0 | Golden shard 与 deep gate | Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: 全量慢测不进入日常 quick；deep/release 可分片复现。 | Parallelizable: Yes
[x] TP-09.02 | P0 | MingLi full 评测门禁 | Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json | Gate: answered=160；predictions 无 expected/answer/correct/gold/label 字段；accuracy 不低于当前 baseline 或有边界解释。 | Parallelizable: Yes
[x] TP-09.03 | P1 | BaziQA 纳入评测审查 | Verify: 记录 license、dataset schema、adapter plan 和禁止进入 runtime 的 gate。 | Gate: license/source 不清时不得纳入正式 gate；只允许 future_candidate/evaluation_only。 | Parallelizable: Yes
[x] TP-09.04 | P0 | 失败归因回炉到规则任务 | Verify: MINGLI_FAILURE_TAXONOMY 中每类 failure 都有 owner、缺口类型、回炉方向和禁止路径。 | Gate: 不得按 question_id 或 expected answer 生成规则。 | Parallelizable: No
[x] TP-10.01 | P1 | evaluator 物理拆分 | Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py tests/regression/test_bazi_golden_coverage_matrix.py -q | Gate: 每次只抽一个 evaluator；失败只回滚当前切片；delivery 不新增领域算法。 | Parallelizable: No
[x] TP-10.02 | P0 | 报告字段与 Markdown 边界收口 | Verify: .venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py -q | Gate: 报告所有新增专业段落都有 evidence/riskBoundary；前端不重算规则。 | Parallelizable: No
[x] TP-10.03 | P0 | 最终本地门禁与审查 | Verify: bash scripts/local-ci.sh --profile quick && bash scripts/local-ci.sh --profile full | Gate: final review Active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造公网/live bot。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
