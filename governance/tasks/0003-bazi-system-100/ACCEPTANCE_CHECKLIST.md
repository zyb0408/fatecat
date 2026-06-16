# Acceptance Checklist

# Global Standards
- [ ] 任何 100% 结论都有可执行命令或可检查文件
- [ ] 任一高级规则都有 sourceRuleId、conditions、doesNotApplyWhen、riskBoundary
- [ ] 任一专题断法都有 benchmark/golden 或明确 evidence_seed 边界
- [ ] MingLi 评估按 total/answered/correct/accuracy/byCategory 输出
- [ ] full golden 不进入 quick；deep/release 使用 shard 或预算说明
- [ ] 无 license 参考源不作为 production dependency
- [ ] 新增代码/文档同步 AGENTS.md 或任务上下文

# Task Package Checklists
## TP-00
- 标题: 版本与基线控制面
- 验收项:
  - [ ] `版本与基线控制面` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 在干净版本边界上建立八字 100% 的 scorecard 和当前缺口基线
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-00.01
- 标题: 提交当前质量 hardening checkpoint
- 验收项:
  - [ ] commit hash 可追溯
  - [ ] 后续 0003 计划改动不混入 checkpoint
- Verify: git log --oneline -1 && git status --short
- Gate: 最新提交为质量 hardening checkpoint，且提交后可明确区分 0003 新改动
- 输出物:
  - [ ] git commit checkpoint
- 标准清单:
  - [ ] Verify: git log --oneline -1 && git status --short
  - [ ] Gate: 最新提交为质量 hardening checkpoint，且提交后可明确区分 0003 新改动
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-00.02
- 标题: 建立八字 100% scorecard
- 验收项:
  - [x] 100% 是工程验收定义，不是预测绝对准确
  - [x] MingLi 准确率目标分阶段记录
- Verify: test -s governance/tasks/0003-bazi-system-100/SCORECARD.md && rg '基础排盘|高级格局|MingLi|100%' governance/tasks/0003-bazi-system-100/SCORECARD.md
- Gate: 每个维度有 current%、target evidence、verify command、falsifier
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/SCORECARD.md
- 标准清单:
  - [x] Verify: test -s governance/tasks/0003-bazi-system-100/SCORECARD.md && rg '基础排盘|高级格局|MingLi|100%' governance/tasks/0003-bazi-system-100/SCORECARD.md
  - [x] Gate: 每个维度有 current%、target evidence、verify command、falsifier
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-00.03
- 标题: 生成当前能力基线证据
- 验收项:
  - [x] 当前 76% 估算有命令证据支撑
  - [x] 失败最多的专题分类进入后续优先级
- Verify: bash scripts/generate-mingli-predictions.sh --year 2025 --sample 10 --output-jsonl /tmp/fatecat-mingli-baseline.jsonl && bash scripts/run-mingli-bench.sh --year 2025 --sample 10 --predictions-file /tmp/fatecat-mingli-baseline.jsonl --output-json /tmp/fatecat-mingli-baseline.json
- Gate: baseline report 记录 total/answered/correct/accuracy/byCategory，且不把 sample 10 当最终能力
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/BASELINE_EVIDENCE.md
- 标准清单:
  - [x] Verify: bash scripts/generate-mingli-predictions.sh --year 2025 --sample 10 --output-jsonl /tmp/fatecat-mingli-baseline.jsonl && bash scripts/run-mingli-bench.sh --year 2025 --sample 10 --predictions-file /tmp/fatecat-mingli-baseline.jsonl --output-json /tmp/fatecat-mingli-baseline.json
  - [x] Gate: baseline report 记录 total/answered/correct/accuracy/byCategory，且不把 sample 10 当最终能力
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-01
- 标题: 材料与资源治理
- 验收项:
  - [x] `材料与资源治理` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 明确哪些库、典籍、benchmark 和 oracle 用于补齐 100%，以及每类资源的生产边界
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 整理资源地图
- 验收项:
  - [x] 无 license 资源只标 reference_only
  - [x] oracle 不进入生产主链
- Verify: test -s governance/tasks/0003-bazi-system-100/RESOURCE_MAP.md && rg 'lunar-python|MingLi-Bench|oracle_only|reference_only' governance/tasks/0003-bazi-system-100/RESOURCE_MAP.md
- Gate: 每个资源有 usageRole、license boundary、可补能力和禁止用途
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/RESOURCE_MAP.md
- 标准清单:
  - [x] Verify: test -s governance/tasks/0003-bazi-system-100/RESOURCE_MAP.md && rg 'lunar-python|MingLi-Bench|oracle_only|reference_only' governance/tasks/0003-bazi-system-100/RESOURCE_MAP.md
  - [x] Gate: 每个资源有 usageRole、license boundary、可补能力和禁止用途
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 建立规则来源覆盖矩阵
- 验收项:
  - [x] 缺失来源不能进入实现
  - [x] 规则来源只保留短摘要和条件
- Verify: python3 -m json.tool contracts/fate/classics_rule_index.json >/dev/null && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
- Gate: 每个待实现专业能力至少有候选 sourceRuleId；缺口列入 RULE_SOURCE_GAPS.md
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/RULE_SOURCE_GAPS.md
- 标准清单:
  - [x] Verify: python3 -m json.tool contracts/fate/classics_rule_index.json >/dev/null && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
  - [x] Gate: 每个待实现专业能力至少有候选 sourceRuleId；缺口列入 RULE_SOURCE_GAPS.md
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 基础排盘与时间边界 100%
- 验收项:
  - [x] `基础排盘与时间边界 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把基础排盘从约 90% 推到可审计 100%，重点补节气、真太阳时、早晚子时、起运和跨时区边界
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 历法 oracle 覆盖审计
- 验收项:
  - [x] `历法 oracle 覆盖审计` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
- Gate: oracle 只用于测试/评估；差异样本有 failureExplanation
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/CALENDAR_ORACLE_AUDIT.md
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
  - [x] Gate: oracle 只用于测试/评估；差异样本有 failureExplanation
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 扩展时间边界 golden
- 验收项:
  - [x] `扩展时间边界 golden` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
- Gate: 新增边界样本均有 source、expected、failureExplanation 和 privacy/license 说明
- 输出物:
  - [x] domains/fate-analysis/data-products/bazi/golden/*
  - [x] tests/regression/test_*calendar*.py
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_calendar_oracle_contract.py tests/regression/test_solar_terms_golden.py -q
  - [x] Gate: 新增边界样本均有 source、expected、failureExplanation 和 privacy/license 说明
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 全量 golden deep gate 性能预算
- 验收项:
  - [x] `全量 golden deep gate 性能预算` 达到其 objective，且依赖关系保持一致
- Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
- Gate: deep gate 有 shard、case-level timing 或明确耗时预算；quick 不跑全量
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/GOLDEN_DEEP_GATE.md
- 标准清单:
  - [x] Verify: FATECAT_RUN_FULL_GOLDEN_MATRIX=1 FATECAT_GOLDEN_SHARD_TOTAL=4 FATECAT_GOLDEN_SHARD_INDEX=0 .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py -q
  - [x] Gate: deep gate 有 shard、case-level timing 或明确耗时预算；quick 不跑全量
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 高级格局规则体系
- 验收项:
  - [x] `高级格局规则体系` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把高级格局从约 58% 推到规则来源、条件链、反例和报告边界齐备
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 格局分类语法矩阵
- 验收项:
  - [x] `格局分类语法矩阵` 达到其 objective，且依赖关系保持一致
- Verify: python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null && rg '从格|化气|专旺|假从|格局正变' contracts/fate -n
- Gate: 每类格局有 sourceRuleId、成立条件、破格条件、riskBoundary
- 输出物:
  - [x] contracts/fate/rule_depth_registry.json
  - [x] contracts/fate/classics_rule_index.json
- 标准清单:
  - [x] Verify: python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null && rg '从格|化气|专旺|假从|格局正变' contracts/fate -n
  - [x] Gate: 每类格局有 sourceRuleId、成立条件、破格条件、riskBoundary
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 格局 evaluator 与候选成熟度
- 验收项:
  - [x] `格局 evaluator 与候选成熟度` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
- Gate: candidate/guarded/not_supported 状态由条件链决定，不由文案硬写
- 输出物:
  - [x] fate_core usecase/kernel evaluator
  - [x] rule-depth regression
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
  - [x] Gate: candidate/guarded/not_supported 状态由条件链决定，不由文案硬写
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 高级格局 golden 与反例
- 验收项:
  - [x] `高级格局 golden 与反例` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: 每类高级格局至少有可回归样本；无样本能力只能保持 beta/evidence_seed
- 输出物:
  - [x] domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [x] Gate: 每类高级格局至少有可回归样本；无样本能力只能保持 beta/evidence_seed
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 合化成败引擎
- 验收项:
  - [x] `合化成败引擎` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把合化成败从约 60% 推到月令、透干、通根、得令、阻隔、帮扶、冲破条件链完整
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 合化条件链 registry
- 验收项:
  - [x] `合化条件链 registry` 达到其 objective，且依赖关系保持一致
- Verify: rg '合化|成化|破化|阻隔|争合' contracts/fate -n && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
- Gate: 合化规则不再只有保护文案；每个状态有证据字段和反例条件
- 输出物:
  - [x] contracts/fate/rule_depth_registry.json
- 标准清单:
  - [x] Verify: rg '合化|成化|破化|阻隔|争合' contracts/fate -n && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
  - [x] Gate: 合化规则不再只有保护文案；每个状态有证据字段和反例条件
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 合化 evaluator 与优先级
- 验收项:
  - [x] `合化 evaluator 与优先级` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
- Gate: 输出区分 structural_relation、transform_candidate、transform_success、transform_broken
- 输出物:
  - [x] fate_core combine transform evaluator
  - [x] API/rule-depth regression
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py -q
  - [x] Gate: 输出区分 structural_relation、transform_candidate、transform_success、transform_broken
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 合化 golden 反例集
- 验收项:
  - [x] `合化 golden 反例集` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: 每类合化状态至少有一组回归样本和 failureExplanation
- 输出物:
  - [x] domains/fate-analysis/data-products/bazi/golden/*
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [x] Gate: 每类合化状态至少有一组回归样本和 failureExplanation
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 用神裁决体系
- 验收项:
  - [x] `用神裁决体系` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把用神裁决从约 64% 推到调候、扶抑、通关、病药并列策略和冲突裁决完整
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 用神策略评分矩阵
- 验收项:
  - [x] `用神策略评分矩阵` 达到其 objective，且依赖关系保持一致
- Verify: rg '调候|扶抑|通关|病药|用神' contracts/fate -n && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
- Gate: 每种策略有 appliesWhen、doesNotApplyWhen、score basis、conflictPolicy
- 输出物:
  - [x] contracts/fate/rule_depth_registry.json
- 标准清单:
  - [x] Verify: rg '调候|扶抑|通关|病药|用神' contracts/fate -n && python3 -m json.tool contracts/fate/rule_depth_registry.json >/dev/null
  - [x] Gate: 每种策略有 appliesWhen、doesNotApplyWhen、score basis、conflictPolicy
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 用神冲突裁决 evaluator
- 验收项:
  - [x] `用神冲突裁决 evaluator` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
- Gate: 报告/API 保留并列策略，不用单一用神覆盖全部
- 输出物:
  - [x] fate_core yongshen decision evaluator
  - [x] rule-depth tests
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_fate_policy_assets.py -q
  - [x] Gate: 报告/API 保留并列策略，不用单一用神覆盖全部
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.03
- 标题: 用神裁决 golden
- 验收项:
  - [x] `用神裁决 golden` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
- Gate: 每类用神冲突有 expected strategy order 和 riskBoundary
- 输出物:
  - [x] domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_golden_coverage_matrix.py tests/regression/test_bazi_ziwei_rule_depth.py -q
  - [x] Gate: 每类用神冲突有 expected strategy order 和 riskBoundary
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 岁运与专题推理
- 验收项:
  - [ ] `岁运与专题推理` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把岁运专题从约 55% 推到事业、财运、婚姻、健康、学业、迁移、家庭均有规则证据和 benchmark 反馈
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 岁运触发规则矩阵
- 验收项:
  - [x] `岁运触发规则矩阵` 达到其 objective，且依赖关系保持一致
- Verify: rg '大运|流年|流月|伏吟|反吟|岁运' contracts/fate domains/fate-analysis/services/fate-core/src -n
- Gate: 动态触发只作趋势证据，不输出确定未来
- 输出物:
  - [x] contracts/fate/rule_depth_registry.json
  - [x] fate_core fortune trigger evaluator
- 标准清单:
  - [x] Verify: rg '大运|流年|流月|伏吟|反吟|岁运' contracts/fate domains/fate-analysis/services/fate-core/src -n
  - [x] Gate: 动态触发只作趋势证据，不输出确定未来
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 专题 profile 推理器
- 验收项:
  - [ ] `专题 profile 推理器` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_mingli_bench_gate.py -q
- Gate: 每个专题 profile 有 score、basis、evidenceFields、riskBoundary 和 beta/production lifecycle
- 输出物:
  - [ ] topic profile evaluator
  - [ ] MingLi category mapping
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_mingli_bench_gate.py -q
  - [ ] Gate: 每个专题 profile 有 score、basis、evidenceFields、riskBoundary 和 beta/production lifecycle
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.03
- 标题: 专题报告边界
- 验收项:
  - [ ] `专题报告边界` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py tests/regression/test_fate_policy_assets.py -q
- Gate: 报告不输出医疗、金融、法律或心理确定建议
- 输出物:
  - [ ] report/API/Web evidence boundary
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py tests/regression/test_fate_policy_assets.py -q
  - [ ] Gate: 报告不输出医疗、金融、法律或心理确定建议
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: Benchmark 与样本外闭环
- 验收项:
  - [ ] `Benchmark 与样本外闭环` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把样本外 benchmark 从约 42% 推到全量可评测、可归因、可回炉的工程闭环
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: MingLi 全量 160 评测
- 验收项:
  - [ ] `MingLi 全量 160 评测` 达到其 objective，且依赖关系保持一致
- Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
- Gate: 全量报告包含 total/answered/correct/accuracy/byCategory/results，且无答案泄漏
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/MINGLI_FULL_EVALUATION.md
- 标准清单:
  - [ ] Verify: bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl && bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
  - [ ] Gate: 全量报告包含 total/answered/correct/accuracy/byCategory/results，且无答案泄漏
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.02
- 标题: 失败样本归因和回炉队列
- 验收项:
  - [ ] `失败样本归因和回炉队列` 达到其 objective，且依赖关系保持一致
- Verify: test -s governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md && rg '缺规则|缺时间触发|缺格局|缺用神' governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md
- Gate: 失败样本有 owner 能力面；不得用人工答案修预测脚本
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md
- 标准清单:
  - [ ] Verify: test -s governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md && rg '缺规则|缺时间触发|缺格局|缺用神' governance/tasks/0003-bazi-system-100/MINGLI_FAILURE_TAXONOMY.md
  - [ ] Gate: 失败样本有 owner 能力面；不得用人工答案修预测脚本
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: Benchmark 门槛和回归策略
- 验收项:
  - [ ] `Benchmark 门槛和回归策略` 达到其 objective，且依赖关系保持一致
- Verify: test -s governance/tasks/0003-bazi-system-100/BENCHMARK_GATE_POLICY.md
- Gate: 明确当前 baseline、下一门槛、回退条件和不达标处理
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/BENCHMARK_GATE_POLICY.md
- 标准清单:
  - [ ] Verify: test -s governance/tasks/0003-bazi-system-100/BENCHMARK_GATE_POLICY.md
  - [ ] Gate: 明确当前 baseline、下一门槛、回退条件和不达标处理
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 报告和 API 证据化 100%
- 验收项:
  - [ ] `报告和 API 证据化 100%` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 确保 Web/API/Markdown 报告只展示可追溯结论，并能暴露必要证据和边界
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.01
- 标题: 报告字段契约
- 验收项:
  - [ ] `报告字段契约` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py -q
- Gate: 核心结果由服务端写入页面；证据块默认可折叠；无未登记断语
- 输出物:
  - [ ] API/Web/Markdown report contract
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_web_html.py -q
  - [ ] Gate: 核心结果由服务端写入页面；证据块默认可折叠；无未登记断语
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.02
- 标题: 风险话术和免责声明回归
- 验收项:
  - [ ] `风险话术和免责声明回归` 达到其 objective，且依赖关系保持一致
- Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_api_contracts.py -q
- Gate: 禁止医疗/金融/法律/心理替代建议；风险边界字段可追溯
- 输出物:
  - [ ] policy tests
  - [ ] report risk boundary
- 标准清单:
  - [ ] Verify: .venv/bin/python -m pytest tests/regression/test_fate_policy_assets.py tests/regression/test_api_contracts.py -q
  - [ ] Gate: 禁止医疗/金融/法律/心理替代建议；风险边界字段可追溯
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-09
- 标题: 长期维护性和模块边界
- 验收项:
  - [ ] `长期维护性和模块边界` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 把八字规则体系从大文件堆叠推进到 registry/evaluator/golden/report 分层维护
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.01
- 标题: 大文件职责切片路线
- 验收项:
  - [x] `大文件职责切片路线` 达到其 objective，且依赖关系保持一致
- Verify: test -s governance/tasks/0003-bazi-system-100/CORE_FILE_BURNDOWN.md && rg 'bazi_calculator|calculate_pure_analysis|report_generator' governance/tasks/0003-bazi-system-100/CORE_FILE_BURNDOWN.md
- Gate: 每个拆分候选有行为保持测试和回滚路径；不做大爆炸重写
- 输出物:
  - [x] governance/tasks/0003-bazi-system-100/CORE_FILE_BURNDOWN.md
- 标准清单:
  - [x] Verify: test -s governance/tasks/0003-bazi-system-100/CORE_FILE_BURNDOWN.md && rg 'bazi_calculator|calculate_pure_analysis|report_generator' governance/tasks/0003-bazi-system-100/CORE_FILE_BURNDOWN.md
  - [x] Gate: 每个拆分候选有行为保持测试和回滚路径；不做大爆炸重写
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.02
- 标题: 规则 evaluator 模块边界
- 验收项:
  - [ ] `规则 evaluator 模块边界` 达到其 objective，且依赖关系保持一致
- Verify: test -s governance/tasks/0003-bazi-system-100/EVALUATOR_BOUNDARIES.md
- Gate: evaluation 不进生产 kernel；oracle 不进主链；delivery 不承载领域算法
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/EVALUATOR_BOUNDARIES.md
- 标准清单:
  - [ ] Verify: test -s governance/tasks/0003-bazi-system-100/EVALUATOR_BOUNDARIES.md
  - [ ] Gate: evaluation 不进生产 kernel；oracle 不进主链；delivery 不承载领域算法
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-10
- 标题: 最终审查和交付
- 验收项:
  - [ ] `最终审查和交付` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [ ] 汇总八字 100% 推进结果，区分 Done、WARN、Blocked，并生成最终交付证据
- 标准清单:
  - [ ] Verify: 核对目标完成并补充执行证据
  - [ ] Gate: 任务目标与上下文已确认
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.01
- 标题: 八字体系 100% 六维审查
- 验收项:
  - [ ] `八字体系 100% 六维审查` 达到其 objective，且依赖关系保持一致
- Verify: bash scripts/local-ci.sh --profile quick && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase decompose
- Gate: active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造 100%
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/FINAL_REVIEW.md
- 标准清单:
  - [ ] Verify: bash scripts/local-ci.sh --profile quick && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase decompose
  - [ ] Gate: active BLOCK=0；WARN 有 owner、证据和下一步；不得伪造 100%
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.02
- 标题: Closeout 和版本交付
- 验收项:
  - [ ] `Closeout 和版本交付` 达到其 objective，且依赖关系保持一致
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase closeout && git status --short
- Gate: closeout 可校验；提交边界清晰；最终结论不越过证据
- 输出物:
  - [ ] governance/tasks/0003-bazi-system-100/CLOSEOUT.md
  - [ ] git delivery evidence
- 标准清单:
  - [ ] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-bazi-system-100 --phase closeout && git status --short
  - [ ] Gate: closeout 可校验；提交边界清晰；最终结论不越过证据
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
