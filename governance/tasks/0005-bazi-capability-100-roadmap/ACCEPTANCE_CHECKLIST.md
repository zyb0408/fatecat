# Acceptance Checklist

# Global Standards

- [x] 十个维度全部覆盖。
- [x] 每个维度有 100% gate。
- [x] 每个维度有执行任务。
- [x] 每个任务有 verify 和 falsifier。
- [x] benchmark 禁止答案泄漏。
- [x] 高风险输出有 policy gate。
- [x] 资源角色边界清楚。
- [x] 不宣称预测准确率 100%。

# Task Package Checklists

## TP-01.01 复核当前十维基线与 final review

- Verify: `rg '基础排盘|样本外 benchmark|Active BLOCK' governance/tasks/0004-bazi-professional-system-100 -n`
- Gate: current 百分比、WARN、禁止口径一致。
- [x] 记录真实基线和证据文件。

## TP-01.02 复核外部资源准入与 license/source 边界

- Verify: `rg 'production_dependency|oracle_only|evaluation_only|reference_only|future_candidate' governance/tasks/0004-bazi-professional-system-100/RESOURCE_MAP.md -n`
- Gate: 每个资源有 usageRole、productionUseAllowed、禁止用途。
- [x] 记录可生产、oracle、评测、参考、候选边界。

## TP-01.03 写入十维 100% gate 合同

- Verify: `rg '100% 不是|100% 是|falsifier|target gate' governance/tasks/0005-bazi-capability-100-roadmap -n`
- Gate: 100% 不被解释成预测准确率 100%。
- [x] 十个维度都有 target gate 和 falsifier。

## TP-02.01 CalendarProvider 升级合同

- Verify: `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q`
- Gate: production provider 与 oracle import 边界清楚。
- [x] provider 升级路径、回滚路径、锁文件和 oracle 边界清楚。

## TP-02.02 扩展 calendar boundary corpus 到 >=50

- Verify: `.venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_bazi_golden_coverage_matrix.py -q`
- Gate: 每个边界样本有 source、expected、tolerance、failureExplanation。
- [x] 覆盖节气秒级、立春、早晚子时、真太阳时、跨时区和起运。

## TP-02.03 oracle mismatch report

- Verify: 生成 calendar mismatch report 并跑 local regression。
- Gate: 差异可解释；不可解释差异不得标绿。
- [x] 每个 mismatch 有 provider、oracle、input、expected、actual、decision。

## TP-03.01 ruleId 覆盖强制门禁

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q`
- Gate: production 断语无未登记 ruleId。
- [x] ruleId 可回指 registry/classics。

## TP-03.02 evidence/counterEvidence schema

- Verify: `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -q`
- Gate: 专业段落必须有 evidenceFields、riskBoundary、counterEvidence。
- [x] API/Web/Markdown 消费者不破坏。

## TP-03.03 高风险输出 policy gate

- Verify: `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q`
- Gate: 禁止医疗、金融、法律、心理、灾祸、婚姻确定断语。
- [x] 高风险样本缺口进入 statement golden。

## TP-04.01 strength evaluator 物理拆分

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`
- Gate: schema 不变，delivery 不新增领域算法。
- [x] strength 输出包含 score、basis、sourceRuleId、conflicts。

## TP-04.02 ten-god evaluator 物理拆分

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`
- Gate: 十神输出引用柱位、透干、藏干证据。
- [x] 十神解释不输出孤立断语。

## TP-04.03 regular-pattern/relation evaluator 拆分

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py -q`
- Gate: 不稳定格局输出 uncertainty，不强断。
- [x] 常规格局和干支关系 schema 稳定。

## TP-05.01 高级格局 taxonomy 与 lifecycle

- Verify: `rg '从格|假从|专旺|化气|lifecycle' contracts/fate domains/fate-analysis -n`
- Gate: 每类高级格局有 appliesWhen/doesNotApplyWhen。
- [x] 正格、变格、从格、假从、专旺、化气均有生命周期定义。

## TP-05.02 高级格局正反边界 golden

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q`
- Gate: 每类至少正例、反例、边界例；无样本保持 beta/HITL。
- [x] failureExplanation 能定位格局条件。

## TP-05.03 guarded advanced-pattern evaluator

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`
- Gate: 不满足条件时不得 production 强断。
- [x] evaluator 输出候选、信心、反证和 lifecycle。

## TP-06.01 合化条件链状态模型

- Verify: `rg '合象|合而不化|成化|破化|争合|阻隔|冲破' contracts/fate domains/fate-analysis -n`
- Gate: 月令、透干、通根、阻隔、帮扶、冲破均可表达。
- [x] condition chain 可序列化和测试。

## TP-06.02 transform evaluator

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`
- Gate: 输出状态、证据和反证，不只输出“合化”。
- [x] evaluator 不依赖 delivery。

## TP-06.03 破化/争合/阻隔反例矩阵

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q`
- Gate: 失败能定位具体 condition。
- [x] 反例样本覆盖破化、争合、阻隔、冲破。

## TP-07.01 用神策略合同

- Verify: `rg '调候|扶抑|通关|病药|格局用神|doesNotApplyWhen' contracts/fate governance/tasks -n`
- Gate: 每个策略有 basis、score、doesNotApplyWhen。
- [x] 调候、扶抑、通关、病药、格局用神并列存在。

## TP-07.02 用神冲突排序 evaluator

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q`
- Gate: 输出 ranking/conflicts，不输出唯一绝对结论。
- [x] 冲突裁决可解释。

## TP-07.03 用神反例与报告边界

- Verify: `.venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_statement_golden.py -q`
- Gate: 冲突样本解释 ranking 变化，报告保留边界。
- [x] 单一用神强断被 policy 或 golden 拦截。

## TP-08.01 岁运触发矩阵

- Verify: `rg '大运|流年|流月|伏吟|反吟|天克地冲|fortuneTriggers' contracts domains/fate-analysis -n`
- Gate: 动态触发只作趋势证据。
- [x] 触发链覆盖原局、大运、流年、流月。

## TP-08.02 P0 专题 profile evaluator

- Verify: `.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_rule_depth.py -q`
- Gate: 婚姻、事业、财运、家庭、健康、学业都有 score/basis/evidence/riskBoundary。
- [x] topic profile 输出不是 benchmark 答案匹配。

## TP-08.03 高风险专题 policy regression

- Verify: `.venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_bazi_statement_golden.py -q`
- Gate: 不输出确定未来、现实处方或恐吓式断语。
- [x] P0 专题均有高风险负例。

## TP-09.01 golden corpus 扩展目标

- Verify: 统计 calendar/rule-depth/statement/topic golden 数量并跑对应 pytest。
- Gate: calendar>=50, rule-depth>=120, statement>=80, P0 topic 每类>=20。
- [ ] corpus 统计写入 evidence。

## TP-09.02 shard release gate

- Verify: `FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4` 逐 shard 跑 `tests/regression/test_bazi_golden_coverage_matrix.py -q`
- Gate: shard 0..3 全通过；quick 不跑全量慢测。
- [ ] shard 结果可复现。

## TP-09.03 mutation/schema regression

- Verify: schema diff、API contract、policy regression 全过。
- Gate: 字段缺失、规则缺证据、policy 失效时测试红。
- [ ] regression 能证明不是形式工程。

## TP-10.01 MingLi full no-leak gate

- Verify: `bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json`
- Gate: answered=160/160，predictions 无 expected/answer/correct/gold/label。
- [x] 输出 accuracy 和按主题 failure taxonomy。

## TP-10.02 failure-driven rule backlog

- Verify: `MINGLI_FAILURE_TAXONOMY` 每类 failure 有 owner、缺口、回炉方向、禁止路径。
- Gate: 禁止按 question_id/答案/选项调参。
- [x] 失败只进入可解释规则 backlog。

## TP-10.03 BaziQA admission gate

- Verify: license、schema、adapter、privacy、no-runtime 审查文档。
- Gate: license/source 不清时保持 future_candidate/evaluation_only。
- [x] admission 输出 PASS/WARN/BLOCK。

## TP-11.01 evaluator 物理拆分收口

- Verify: `rg 'build_.*evaluator|fate_core.usecases.evaluators' domains/fate-analysis/services/fate-core/src -n && .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q`
- Gate: pattern/hehua/yongshen/topic 等切片从大函数迁出。
- [ ] AGENTS.md 边界同步更新。

## TP-11.02 Web/API/Markdown 消费边界

- Verify: `.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_statement_golden.py -q`
- Gate: delivery 不重算命理规则，不泄漏内部 lifecycle 字段。
- [ ] Web/API/Markdown 只消费结构化结果。

## TP-11.03 final local release gate

- Verify: `bash scripts/local-ci.sh --profile quick && bash scripts/local-ci.sh --profile full`
- Gate: Active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造公网/live bot。
- [ ] final review 和 closeout 落盘。
